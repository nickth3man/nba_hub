use std::collections::HashMap;
use std::collections::HashSet;
use std::path::PathBuf;

use anyhow::{Context, Result};
use chrono::Datelike;
use clap::Parser;
use csv::ReaderBuilder;
use log::{info, warn};
use serde::Deserialize;

use nba_core::awards::build_award_key;
use nba_core::schema::{
    Award, Draft, Game, Player, PlayerBoxscore, PlayerSeasonAdvanced, PlayerSeasonTotal, Season,
    Standing, Team, TeamBoxscore, TeamHistory, TeamSeasonAdvanced, TeamSeasonTotal,
};

use crate::convex::{ConvexClient, ConvexError};
use crate::csv_utils::{parse_opt_bool, parse_opt_f64, parse_opt_i32, parse_opt_string};

#[derive(Parser, Debug)]
#[command(name = "nba-etl")]
#[command(about = "NBA Hub ETL Tool")]
pub struct Args {
    #[arg(long, default_value = "data/raw")]
    pub csv_dir: String,

    #[arg(long, default_value_t = 200)]
    pub batch_size: usize,
}

pub async fn run_seed(args: Args) -> Result<()> {
    let csv_dir = PathBuf::from(args.csv_dir);
    let convex = ConvexClient::new()?;

    seed_reference_data(&convex, args.batch_size).await?;

    let (team_history, team_map, history_spans) = load_team_history(&csv_dir)?;
    send_batches(
        &convex,
        "ingest:upsertTeamHistory",
        "history",
        team_history,
        args.batch_size,
    )
    .await?;
    let teams = build_teams_from_history(&team_map);
    send_batches(
        &convex,
        "ingest:upsertTeams",
        "teams",
        teams,
        args.batch_size,
    )
    .await?;

    let all_players = load_all_players(&csv_dir)?;
    let players = load_players(&csv_dir, &all_players)?;
    send_batches(
        &convex,
        "ingest:upsertPlayers",
        "players",
        players,
        args.batch_size,
    )
    .await?;

    let games = load_games(&csv_dir, &history_spans)?;
    send_batches(
        &convex,
        "ingest:upsertGames",
        "games",
        games,
        args.batch_size,
    )
    .await?;

    let boxscores = load_player_boxscores(&csv_dir, &team_map)?;
    send_batches(
        &convex,
        "ingest:upsertPlayerBoxscores",
        "boxscores",
        boxscores,
        args.batch_size,
    )
    .await?;

    let team_boxscores = load_team_boxscores(&csv_dir)?;
    send_batches(
        &convex,
        "ingest:upsertTeamBoxscores",
        "boxscores",
        team_boxscores,
        args.batch_size,
    )
    .await?;

    let drafts = load_drafts(&csv_dir)?;
    send_batches(
        &convex,
        "ingest:upsertDrafts",
        "drafts",
        drafts,
        args.batch_size,
    )
    .await?;

    let player_totals = load_player_season_totals(&csv_dir)?;
    send_batches(
        &convex,
        "ingest:upsertPlayerSeasonTotals",
        "totals",
        player_totals,
        args.batch_size,
    )
    .await?;

    let player_advanced = load_player_season_advanced(&csv_dir)?;
    send_batches(
        &convex,
        "ingest:upsertPlayerSeasonAdvanced",
        "advanced",
        player_advanced,
        args.batch_size,
    )
    .await?;

    let team_totals = load_team_season_totals(&csv_dir)?;
    send_batches(
        &convex,
        "ingest:upsertTeamSeasonTotals",
        "totals",
        team_totals,
        args.batch_size,
    )
    .await?;

    let (team_advanced, standings) = load_team_summaries(&csv_dir)?;
    send_batches(
        &convex,
        "ingest:upsertTeamSeasonAdvanced",
        "advanced",
        team_advanced,
        args.batch_size,
    )
    .await?;
    send_batches(
        &convex,
        "ingest:upsertStandings",
        "standings",
        standings,
        args.batch_size,
    )
    .await?;

    let awards = load_awards(&csv_dir)?;
    send_batches(
        &convex,
        "ingest:upsertAwards",
        "awards",
        awards,
        args.batch_size,
    )
    .await?;

    Ok(())
}

async fn seed_reference_data(convex: &ConvexClient, batch_size: usize) -> Result<()> {
    let leagues = vec![
        serde_json::json!({"league_id": 1, "league_code": "NBA", "league_name": "National Basketball Association"}),
        serde_json::json!({"league_id": 2, "league_code": "BAA", "league_name": "Basketball Association of America"}),
        serde_json::json!({"league_id": 3, "league_code": "ABA", "league_name": "American Basketball Association"}),
    ];
    send_batches(
        convex,
        "ingest:upsertLeagues",
        "leagues",
        leagues,
        batch_size,
    )
    .await?;

    let mut seasons = Vec::new();
    for year in 1946..=1948 {
        seasons.push(Season {
            season_id: season_id_for_league_year(2, year),
            league_id: 2,
            season_year: year,
            start_date: None,
            end_date: None,
        });
    }
    for year in 1949..=current_year() {
        seasons.push(Season {
            season_id: season_id_for_league_year(1, year),
            league_id: 1,
            season_year: year,
            start_date: None,
            end_date: None,
        });
    }
    for year in 1967..=1976 {
        seasons.push(Season {
            season_id: season_id_for_league_year(3, year),
            league_id: 3,
            season_year: year,
            start_date: None,
            end_date: None,
        });
    }
    send_batches(
        convex,
        "ingest:upsertSeasons",
        "seasons",
        seasons,
        batch_size,
    )
    .await?;

    Ok(())
}

fn load_team_history(
    csv_dir: &PathBuf,
) -> Result<(
    Vec<TeamHistory>,
    HashMap<String, TeamMapEntry>,
    HashMap<i64, Vec<TeamHistorySpan>>,
)> {
    let path = csv_dir.join("TeamHistories.csv");
    let mut reader = ReaderBuilder::new()
        .has_headers(true)
        .from_path(&path)
        .with_context(|| format!("Failed to open {}", path.display()))?;

    let mut history = Vec::new();
    let mut map = HashMap::new();
    let mut spans: HashMap<i64, Vec<TeamHistorySpan>> = HashMap::new();
    let mut counter = 1;

    for result in reader.deserialize::<TeamHistoryRow>() {
        let row = result?;
        let team_id = row.team_id;
        let league_code = row.league.as_deref().unwrap_or("NBA");
        let league_id = match league_id_from_code(league_code) {
            Some(league_id) => league_id,
            None => {
                warn!(
                    "Skipping team history row with unknown league: {}",
                    league_code
                );
                continue;
            }
        };
        let season_end = row.season_active_till.unwrap_or(current_year());
        let is_active = row
            .season_active_till
            .map(|year| year >= current_year())
            .unwrap_or(true);

        let entry = TeamMapEntry {
            team_id,
            league_id,
            abbreviation: row.team_abbrev.clone(),
        };

        map.insert(team_key(&row.team_city, &row.team_name), entry);
        spans.entry(team_id).or_default().push(TeamHistorySpan {
            league_id,
            season_start: row.season_founded,
            season_end,
        });

        history.push(TeamHistory {
            team_history_id: counter,
            team_id,
            effective_start: format!("{}-01-01", row.season_founded),
            effective_end: row.season_active_till.map(|year| format!("{}-12-31", year)),
            city: row.team_city,
            nickname: row.team_name,
            abbreviation: Some(row.team_abbrev),
            is_active,
        });
        counter += 1;
    }

    Ok((history, map, spans))
}

fn build_teams_from_history(map: &HashMap<String, TeamMapEntry>) -> Vec<Team> {
    let mut teams = Vec::new();
    let mut seen = HashMap::new();
    for entry in map.values() {
        if seen.insert(entry.team_id, true).is_none() {
            teams.push(Team {
                team_id: entry.team_id,
                league_id: entry.league_id,
                franchise_code: Some(entry.abbreviation.clone()),
                nba_api_team_id: Some(entry.team_id),
            });
        }
    }
    teams
}

fn load_all_players(csv_dir: &PathBuf) -> Result<HashMap<i64, (i32, i32)>> {
    let path = csv_dir.join("all_players.csv");
    if !path.exists() {
        info!("Optional file missing, skipping: {}", path.display());
        return Ok(HashMap::new());
    }

    let mut reader = ReaderBuilder::new()
        .has_headers(true)
        .flexible(true)
        .from_path(&path)
        .with_context(|| format!("Failed to open {}", path.display()))?;

    let mut map = HashMap::new();
    for result in reader.deserialize::<AllPlayersRow>() {
        match result {
            Ok(row) => {
                map.insert(row.person_id, (row.from_year, row.to_year));
            }
            Err(err) => {
                warn!("Skipping malformed all_players row: {}", err);
            }
        }
    }

    Ok(map)
}

fn load_players(csv_dir: &PathBuf, all_players: &HashMap<i64, (i32, i32)>) -> Result<Vec<Player>> {
    let path = csv_dir.join("Players.csv");
    let mut reader = ReaderBuilder::new()
        .has_headers(true)
        .from_path(&path)
        .with_context(|| format!("Failed to open {}", path.display()))?;

    let mut players = Vec::new();
    for result in reader.deserialize::<PlayerRow>() {
        let row = result?;
        let display_name = format!("{} {}", row.first_name, row.last_name)
            .trim()
            .to_string();
        let (from_year, to_year) = all_players.get(&row.person_id).copied().unwrap_or((0, 0));

        players.push(Player {
            player_id: row.person_id,
            nba_api_person_id: Some(row.person_id),
            first_name: Some(row.first_name),
            last_name: Some(row.last_name),
            display_name: if display_name.is_empty() {
                None
            } else {
                Some(display_name)
            },
            birth_date: row.birthdate,
            from_year: if from_year == 0 {
                None
            } else {
                Some(from_year)
            },
            to_year: if to_year == 0 { None } else { Some(to_year) },
        });
    }

    Ok(players)
}

fn load_games(
    csv_dir: &PathBuf,
    history_spans: &HashMap<i64, Vec<TeamHistorySpan>>,
) -> Result<Vec<Game>> {
    let path = csv_dir.join("Games.csv");
    let mut reader = ReaderBuilder::new()
        .has_headers(true)
        .from_path(&path)
        .with_context(|| format!("Failed to open {}", path.display()))?;

    let mut games = Vec::new();
    for result in reader.deserialize::<GameRow>() {
        let row = result?;
        let game_date = normalize_date(&row.game_date_time);
        let season_year = season_year_from_date(&game_date);
        let league_id = league_id_for_game(row.home_team_id, season_year, history_spans)
            .unwrap_or_else(|| if season_year < 1949 { 2 } else { 1 });
        let season_id = season_id_for_league_year(league_id, season_year);

        games.push(Game {
            game_id: row.game_id,
            league_id,
            season_id,
            season_type: row.game_type.unwrap_or_else(|| "Regular".to_string()),
            game_date,
            home_team_id: row.home_team_id,
            away_team_id: row.away_team_id,
            home_points: row.home_score,
            away_points: row.away_score,
            attendance: row.attendance,
            arena_id: row.arena_id,
        });
    }

    Ok(games)
}

fn load_player_boxscores(
    csv_dir: &PathBuf,
    team_map: &HashMap<String, TeamMapEntry>,
) -> Result<Vec<PlayerBoxscore>> {
    let path = csv_dir.join("PlayerStatistics.csv");
    let mut reader = ReaderBuilder::new()
        .has_headers(true)
        .from_path(&path)
        .with_context(|| format!("Failed to open {}", path.display()))?;

    let mut boxscores = Vec::new();
    let mut missing_team_keys = HashSet::new();
    for result in reader.deserialize::<PlayerStatRow>() {
        let row = result?;
        let team_key = team_key(&row.team_city, &row.team_name);
        let team_id = match team_map.get(&team_key) {
            Some(entry) => entry.team_id,
            None => {
                if missing_team_keys.insert(team_key.clone()) {
                    warn!("Missing team mapping for {}", team_key);
                }
                continue;
            }
        };

        boxscores.push(PlayerBoxscore {
            game_id: row.game_id.to_string(),
            player_id: row.player_id,
            team_id,
            minutes: row.minutes,
            points: row.points,
            assists: row.assists,
            rebounds_total: row.rebounds_total,
            steals: row.steals,
            blocks: row.blocks,
            fgm: row.fgm,
            fga: row.fga,
            fg3m: row.fg3m,
            fg3a: row.fg3a,
            ftm: row.ftm,
            fta: row.fta,
            pf: row.pf,
            turnovers: row.turnovers,
            plus_minus: row.plus_minus,
        });
    }

    Ok(boxscores)
}

fn load_team_boxscores(csv_dir: &PathBuf) -> Result<Vec<TeamBoxscore>> {
    let path = csv_dir.join("TeamStatistics.csv");
    let mut reader = ReaderBuilder::new()
        .has_headers(true)
        .from_path(&path)
        .with_context(|| format!("Failed to open {}", path.display()))?;

    let mut boxscores = Vec::new();
    for result in reader.deserialize::<TeamStatRow>() {
        let row = result?;
        boxscores.push(TeamBoxscore {
            game_id: row.game_id.to_string(),
            team_id: row.team_id,
            minutes: row.minutes,
            points: row.points,
            assists: row.assists,
            rebounds_total: row.rebounds_total,
            fgm: row.fgm,
            fga: row.fga,
            fg3m: row.fg3m,
            fg3a: row.fg3a,
            ftm: row.ftm,
            fta: row.fta,
            turnovers: row.turnovers,
            pf: row.pf,
        });
    }

    Ok(boxscores)
}

fn load_drafts(csv_dir: &PathBuf) -> Result<Vec<Draft>> {
    let path = csv_dir.join("Draft Pick History.csv");
    let mut reader = ReaderBuilder::new()
        .has_headers(true)
        .from_path(&path)
        .with_context(|| format!("Failed to open {}", path.display()))?;

    let mut drafts = Vec::new();
    for result in reader.deserialize::<DraftRow>() {
        let row = result?;
        let overall_pick = match row.overall_pick {
            Some(pick) => pick,
            None => {
                warn!(
                    "Skipping draft row with missing overall_pick (season {})",
                    row.season
                );
                continue;
            }
        };
        drafts.push(Draft {
            season_year: row.season,
            pick_overall: overall_pick,
            round_number: row.round,
            pick_in_round: None,
            team_abbrev: row.team_abbrev,
            player_bref_id: row.player_id,
            player_name: row.player_name,
            college: row.college,
        });
    }

    Ok(drafts)
}

fn load_player_season_totals(csv_dir: &PathBuf) -> Result<Vec<PlayerSeasonTotal>> {
    let path = csv_dir.join("Player Totals.csv");
    let mut reader = ReaderBuilder::new()
        .has_headers(true)
        .from_path(&path)
        .with_context(|| format!("Failed to open {}", path.display()))?;

    let mut totals = Vec::new();
    for result in reader.deserialize::<PlayerSeasonTotalsRow>() {
        let row = result?;
        totals.push(PlayerSeasonTotal {
            season_year: row.season,
            player_bref_id: row.player_id,
            player_name: row.player_name,
            team_abbrev: row.team_abbrev,
            games: row.games,
            games_started: row.games_started,
            minutes: row.minutes,
            points: row.points,
            assists: row.assists,
            rebounds_total: row.rebounds_total,
            steals: row.steals,
            blocks: row.blocks,
            fgm: row.fgm,
            fga: row.fga,
            fg3m: row.fg3m,
            fg3a: row.fg3a,
            ftm: row.ftm,
            fta: row.fta,
            turnovers: row.turnovers,
            pf: row.pf,
        });
    }

    Ok(totals)
}

fn load_player_season_advanced(csv_dir: &PathBuf) -> Result<Vec<PlayerSeasonAdvanced>> {
    let path = csv_dir.join("Advanced.csv");
    let mut reader = ReaderBuilder::new()
        .has_headers(true)
        .from_path(&path)
        .with_context(|| format!("Failed to open {}", path.display()))?;

    let mut advanced = Vec::new();
    for result in reader.deserialize::<PlayerSeasonAdvancedRow>() {
        let row = result?;
        advanced.push(PlayerSeasonAdvanced {
            season_year: row.season,
            player_bref_id: row.player_id,
            team_abbrev: row.team_abbrev,
            minutes: row.minutes,
            per: row.per,
            ts_percent: row.ts_percent,
            usg_percent: row.usg_percent,
            ows: row.ows,
            dws: row.dws,
            ws: row.ws,
            bpm: row.bpm,
            vorp: row.vorp,
        });
    }

    Ok(advanced)
}

fn load_team_season_totals(csv_dir: &PathBuf) -> Result<Vec<TeamSeasonTotal>> {
    let path = csv_dir.join("Team Totals.csv");
    let mut reader = ReaderBuilder::new()
        .has_headers(true)
        .from_path(&path)
        .with_context(|| format!("Failed to open {}", path.display()))?;

    let mut totals = Vec::new();
    for result in reader.deserialize::<TeamSeasonTotalsRow>() {
        let row = result?;
        let games = match row.games {
            Some(games) => games,
            None => {
                warn!(
                    "Skipping team totals row with missing games (season {}, team {})",
                    row.season, row.team_abbrev
                );
                continue;
            }
        };
        totals.push(TeamSeasonTotal {
            season_year: row.season,
            team_abbrev: row.team_abbrev,
            games,
            minutes: row.minutes,
            points: row.points,
            assists: row.assists,
            rebounds_total: row.rebounds_total,
            fgm: row.fgm,
            fga: row.fga,
            fg3m: row.fg3m,
            fg3a: row.fg3a,
            ftm: row.ftm,
            fta: row.fta,
            turnovers: row.turnovers,
            pf: row.pf,
        });
    }

    Ok(totals)
}

fn load_team_summaries(csv_dir: &PathBuf) -> Result<(Vec<TeamSeasonAdvanced>, Vec<Standing>)> {
    let path = csv_dir.join("Team Summaries.csv");
    let mut reader = ReaderBuilder::new()
        .has_headers(true)
        .from_path(&path)
        .with_context(|| format!("Failed to open {}", path.display()))?;

    let mut advanced = Vec::new();
    let mut standings = Vec::new();

    for result in reader.deserialize::<TeamSummaryRow>() {
        let row = result?;
        let wins = match row.wins {
            Some(wins) => wins,
            None => {
                warn!(
                    "Skipping team summary row with missing wins (season {}, team {})",
                    row.season, row.team_abbrev
                );
                continue;
            }
        };
        let losses = match row.losses {
            Some(losses) => losses,
            None => {
                warn!(
                    "Skipping team summary row with missing losses (season {}, team {})",
                    row.season, row.team_abbrev
                );
                continue;
            }
        };
        advanced.push(TeamSeasonAdvanced {
            season_year: row.season,
            team_abbrev: row.team_abbrev.clone(),
            wins,
            losses,
            srs: row.srs,
            pace: row.pace,
            off_rtg: row.off_rtg,
            def_rtg: row.def_rtg,
            net_rtg: row.net_rtg,
        });

        standings.push(Standing {
            season_year: row.season,
            team_abbrev: row.team_abbrev,
            wins,
            losses,
            playoffs: row.playoffs.unwrap_or(false),
        });
    }

    Ok((advanced, standings))
}

fn load_awards(csv_dir: &PathBuf) -> Result<Vec<Award>> {
    let mut awards = Vec::new();
    awards.extend(load_all_star_awards(csv_dir)?);
    awards.extend(load_end_of_season_awards(csv_dir)?);
    awards.extend(load_end_of_season_votes(csv_dir)?);
    Ok(awards)
}

fn award_with_key(
    award_type: String,
    season_year: i32,
    player_bref_id: Option<String>,
    player_name: Option<String>,
    team_abbrev: Option<String>,
    rank: Option<i32>,
    points_won: Option<i32>,
    points_max: Option<i32>,
    share: Option<f64>,
) -> Option<Award> {
    let award_key = match build_award_key(
        &award_type,
        season_year,
        player_bref_id.as_deref(),
        player_name.as_deref(),
    ) {
        Some(key) => key,
        None => {
            warn!(
                "Skipping award row with missing player identifier for {} {}",
                award_type, season_year
            );
            return None;
        }
    };

    Some(Award {
        award_key,
        award_type,
        season_year,
        player_bref_id,
        player_name,
        team_abbrev,
        rank,
        points_won,
        points_max,
        share,
    })
}

fn load_all_star_awards(csv_dir: &PathBuf) -> Result<Vec<Award>> {
    let path = csv_dir.join("All-Star Selections.csv");
    if !path.exists() {
        info!("Optional file missing, skipping: {}", path.display());
        return Ok(Vec::new());
    }
    let mut reader = ReaderBuilder::new()
        .has_headers(true)
        .flexible(true)
        .from_path(&path)
        .with_context(|| format!("Failed to open {}", path.display()))?;

    let mut awards = Vec::new();
    for result in reader.deserialize::<AllStarRow>() {
        match result {
            Ok(row) => {
                if let Some(award) = award_with_key(
                    "ALL_STAR".to_string(),
                    row.season,
                    row.player_id,
                    row.player_name,
                    row.team_abbrev,
                    None,
                    None,
                    None,
                    None,
                ) {
                    awards.push(award);
                }
            }
            Err(err) => {
                warn!("Skipping malformed All-Star row: {}", err);
            }
        }
    }
    Ok(awards)
}

fn load_end_of_season_awards(csv_dir: &PathBuf) -> Result<Vec<Award>> {
    let path = csv_dir.join("End of Season Teams.csv");
    if !path.exists() {
        info!("Optional file missing, skipping: {}", path.display());
        return Ok(Vec::new());
    }
    let mut reader = ReaderBuilder::new()
        .has_headers(true)
        .flexible(true)
        .from_path(&path)
        .with_context(|| format!("Failed to open {}", path.display()))?;

    let mut awards = Vec::new();
    for result in reader.deserialize::<EndSeasonRow>() {
        match result {
            Ok(row) => {
                let award_type = format!(
                    "{}_{}",
                    row.award_type.to_uppercase(),
                    row.team_number.to_uppercase()
                );
                if let Some(award) = award_with_key(
                    award_type,
                    row.season,
                    row.player_id,
                    row.player_name,
                    None,
                    None,
                    None,
                    None,
                    None,
                ) {
                    awards.push(award);
                }
            }
            Err(err) => {
                warn!("Skipping malformed End of Season row: {}", err);
            }
        }
    }
    Ok(awards)
}

fn load_end_of_season_votes(csv_dir: &PathBuf) -> Result<Vec<Award>> {
    let path = csv_dir.join("End of Season Teams (Voting).csv");
    if !path.exists() {
        info!("Optional file missing, skipping: {}", path.display());
        return Ok(Vec::new());
    }
    let mut reader = ReaderBuilder::new()
        .has_headers(true)
        .flexible(true)
        .from_path(&path)
        .with_context(|| format!("Failed to open {}", path.display()))?;

    let mut awards = Vec::new();
    for result in reader.deserialize::<EndSeasonVoteRow>() {
        match result {
            Ok(row) => {
                if let Some(award) = award_with_key(
                    row.award_type.to_uppercase(),
                    row.season,
                    row.player_id,
                    row.player_name,
                    None,
                    row.team_number.and_then(parse_rank),
                    row.points_won,
                    row.points_max,
                    row.share,
                ) {
                    awards.push(award);
                }
            }
            Err(err) => {
                warn!("Skipping malformed End of Season voting row: {}", err);
            }
        }
    }
    Ok(awards)
}

fn parse_rank(value: String) -> Option<i32> {
    let digits: String = value.chars().filter(|c| c.is_ascii_digit()).collect();
    digits.parse::<i32>().ok()
}

async fn send_batches<T: serde::Serialize>(
    convex: &ConvexClient,
    function: &str,
    key: &str,
    items: Vec<T>,
    batch_size: usize,
) -> Result<()> {
    if items.is_empty() {
        return Ok(());
    }

    let mut start = 0;
    let mut current_batch_size = batch_size.max(1);
    while start < items.len() {
        let mut end = (start + current_batch_size).min(items.len());
        loop {
            let slice = &items[start..end];
            let payload = serde_json::json!({ key: slice });
            match convex.mutation(function, &payload).await {
                Ok(_) => {
                    info!("Inserted {} items into {}", slice.len(), function);
                    start = end;
                    break;
                }
                Err(err) => {
                    let should_shrink = err
                        .downcast_ref::<ConvexError>()
                        .map(|convex_err| convex_err.is_payload_limit())
                        .unwrap_or(false);
                    if should_shrink && current_batch_size > 1 {
                        let next_size = (current_batch_size / 2).max(1);
                        warn!(
                            "Batch too large for {} ({} items). Retrying with {}",
                            function, current_batch_size, next_size
                        );
                        current_batch_size = next_size;
                        end = (start + current_batch_size).min(items.len());
                        continue;
                    }
                    return Err(err);
                }
            }
        }
    }
    Ok(())
}

fn team_key(city: &str, name: &str) -> String {
    let normalized_city = normalize_team_city(city);
    format!("{}|{}", normalized_city.trim(), name.trim())
}

fn normalize_team_city(city: &str) -> &str {
    match city.trim() {
        "LA" => "Los Angeles",
        _ => city,
    }
}

fn league_id_from_code(code: &str) -> Option<i32> {
    match code.to_uppercase().as_str() {
        "NBA" => Some(1),
        "BAA" => Some(2),
        "ABA" => Some(3),
        _ => None,
    }
}

fn normalize_date(datetime: &str) -> String {
    if let Some((date, _)) = datetime.split_once(' ') {
        date.to_string()
    } else {
        datetime.to_string()
    }
}

fn season_year_from_date(date: &str) -> i32 {
    let parts: Vec<&str> = date.split('-').collect();
    if parts.len() < 2 {
        return date.parse::<i32>().unwrap_or(0);
    }
    let year = parts[0].parse::<i32>().unwrap_or(0);
    let month = parts[1].parse::<i32>().unwrap_or(1);
    if month >= 7 {
        year + 1
    } else {
        year
    }
}

fn season_id_for_league_year(league_id: i32, season_year: i32) -> i32 {
    league_id * 10000 + season_year
}

fn league_id_for_game(
    team_id: i64,
    season_year: i32,
    history_spans: &HashMap<i64, Vec<TeamHistorySpan>>,
) -> Option<i32> {
    history_spans.get(&team_id).and_then(|spans| {
        spans
            .iter()
            .find(|span| season_year >= span.season_start && season_year <= span.season_end)
            .map(|span| span.league_id)
    })
}

fn current_year() -> i32 {
    chrono::Utc::now().year()
}

#[derive(Debug, Deserialize)]
struct TeamHistoryRow {
    #[serde(rename = "teamId")]
    team_id: i64,
    #[serde(rename = "teamCity")]
    team_city: String,
    #[serde(rename = "teamName")]
    team_name: String,
    #[serde(rename = "teamAbbrev")]
    team_abbrev: String,
    #[serde(rename = "seasonFounded")]
    season_founded: i32,
    #[serde(rename = "seasonActiveTill", deserialize_with = "parse_opt_i32")]
    season_active_till: Option<i32>,
    #[serde(rename = "league", deserialize_with = "parse_opt_string")]
    league: Option<String>,
}

#[derive(Debug)]
struct TeamMapEntry {
    team_id: i64,
    league_id: i32,
    abbreviation: String,
}

#[derive(Debug)]
struct TeamHistorySpan {
    league_id: i32,
    season_start: i32,
    season_end: i32,
}

#[derive(Debug, Deserialize)]
struct AllPlayersRow {
    #[serde(rename = "person_id")]
    person_id: i64,
    #[serde(rename = "from_year")]
    from_year: i32,
    #[serde(rename = "to_year")]
    to_year: i32,
}

#[derive(Debug, Deserialize)]
struct PlayerRow {
    #[serde(rename = "personId")]
    person_id: i64,
    #[serde(rename = "firstName")]
    first_name: String,
    #[serde(rename = "lastName")]
    last_name: String,
    #[serde(rename = "birthdate", deserialize_with = "parse_opt_string")]
    birthdate: Option<String>,
}

#[derive(Debug, Deserialize)]
struct GameRow {
    #[serde(rename = "gameId")]
    game_id: String,
    #[serde(rename = "gameDateTimeEst")]
    game_date_time: String,
    #[serde(rename = "hometeamId")]
    home_team_id: i64,
    #[serde(rename = "awayteamId")]
    away_team_id: i64,
    #[serde(rename = "homeScore", deserialize_with = "parse_opt_i32")]
    home_score: Option<i32>,
    #[serde(rename = "awayScore", deserialize_with = "parse_opt_i32")]
    away_score: Option<i32>,
    #[serde(rename = "gameType", deserialize_with = "parse_opt_string")]
    game_type: Option<String>,
    #[serde(rename = "attendance", deserialize_with = "parse_opt_i32")]
    attendance: Option<i32>,
    #[serde(rename = "arenaId", deserialize_with = "parse_opt_i32")]
    arena_id: Option<i32>,
}

#[derive(Debug, Deserialize)]
struct PlayerStatRow {
    #[serde(rename = "personId")]
    player_id: i64,
    #[serde(rename = "gameId")]
    game_id: i64,
    #[serde(rename = "playerteamCity")]
    team_city: String,
    #[serde(rename = "playerteamName")]
    team_name: String,
    #[serde(rename = "numMinutes", deserialize_with = "parse_opt_f64")]
    minutes: Option<f64>,
    #[serde(rename = "points", deserialize_with = "parse_opt_i32")]
    points: Option<i32>,
    #[serde(rename = "assists", deserialize_with = "parse_opt_i32")]
    assists: Option<i32>,
    #[serde(rename = "reboundsTotal", deserialize_with = "parse_opt_i32")]
    rebounds_total: Option<i32>,
    #[serde(rename = "steals", deserialize_with = "parse_opt_i32")]
    steals: Option<i32>,
    #[serde(rename = "blocks", deserialize_with = "parse_opt_i32")]
    blocks: Option<i32>,
    #[serde(rename = "fieldGoalsMade", deserialize_with = "parse_opt_i32")]
    fgm: Option<i32>,
    #[serde(rename = "fieldGoalsAttempted", deserialize_with = "parse_opt_i32")]
    fga: Option<i32>,
    #[serde(rename = "threePointersMade", deserialize_with = "parse_opt_i32")]
    fg3m: Option<i32>,
    #[serde(rename = "threePointersAttempted", deserialize_with = "parse_opt_i32")]
    fg3a: Option<i32>,
    #[serde(rename = "freeThrowsMade", deserialize_with = "parse_opt_i32")]
    ftm: Option<i32>,
    #[serde(rename = "freeThrowsAttempted", deserialize_with = "parse_opt_i32")]
    fta: Option<i32>,
    #[serde(rename = "foulsPersonal", deserialize_with = "parse_opt_i32")]
    pf: Option<i32>,
    #[serde(rename = "turnovers", deserialize_with = "parse_opt_i32")]
    turnovers: Option<i32>,
    #[serde(rename = "plusMinusPoints", deserialize_with = "parse_opt_i32")]
    plus_minus: Option<i32>,
}

#[derive(Debug, Deserialize)]
struct TeamStatRow {
    #[serde(rename = "gameId")]
    game_id: i64,
    #[serde(rename = "teamId")]
    team_id: i64,
    #[serde(rename = "numMinutes", deserialize_with = "parse_opt_f64")]
    minutes: Option<f64>,
    #[serde(rename = "teamScore", deserialize_with = "parse_opt_i32")]
    points: Option<i32>,
    #[serde(rename = "assists", deserialize_with = "parse_opt_i32")]
    assists: Option<i32>,
    #[serde(rename = "reboundsTotal", deserialize_with = "parse_opt_i32")]
    rebounds_total: Option<i32>,
    #[serde(rename = "fieldGoalsMade", deserialize_with = "parse_opt_i32")]
    fgm: Option<i32>,
    #[serde(rename = "fieldGoalsAttempted", deserialize_with = "parse_opt_i32")]
    fga: Option<i32>,
    #[serde(rename = "threePointersMade", deserialize_with = "parse_opt_i32")]
    fg3m: Option<i32>,
    #[serde(rename = "threePointersAttempted", deserialize_with = "parse_opt_i32")]
    fg3a: Option<i32>,
    #[serde(rename = "freeThrowsMade", deserialize_with = "parse_opt_i32")]
    ftm: Option<i32>,
    #[serde(rename = "freeThrowsAttempted", deserialize_with = "parse_opt_i32")]
    fta: Option<i32>,
    #[serde(rename = "turnovers", deserialize_with = "parse_opt_i32")]
    turnovers: Option<i32>,
    #[serde(rename = "foulsPersonal", deserialize_with = "parse_opt_i32")]
    pf: Option<i32>,
}

#[derive(Debug, Deserialize)]
struct DraftRow {
    #[serde(rename = "season")]
    season: i32,
    #[serde(rename = "overall_pick", deserialize_with = "parse_opt_i32")]
    overall_pick: Option<i32>,
    #[serde(rename = "round", deserialize_with = "parse_opt_i32")]
    round: Option<i32>,
    #[serde(rename = "tm", deserialize_with = "parse_opt_string")]
    team_abbrev: Option<String>,
    #[serde(rename = "player_id", deserialize_with = "parse_opt_string")]
    player_id: Option<String>,
    #[serde(rename = "player", deserialize_with = "parse_opt_string")]
    player_name: Option<String>,
    #[serde(rename = "college", deserialize_with = "parse_opt_string")]
    college: Option<String>,
}

#[derive(Debug, Deserialize)]
struct PlayerSeasonTotalsRow {
    #[serde(rename = "season")]
    season: i32,
    #[serde(rename = "player_id")]
    player_id: String,
    #[serde(rename = "player", default, deserialize_with = "parse_opt_string")]
    player_name: Option<String>,
    #[serde(rename = "team")]
    team_abbrev: String,
    #[serde(rename = "g")]
    games: i32,
    #[serde(rename = "gs", deserialize_with = "parse_opt_i32")]
    games_started: Option<i32>,
    #[serde(rename = "mp", deserialize_with = "parse_opt_f64")]
    minutes: Option<f64>,
    #[serde(rename = "pts", deserialize_with = "parse_opt_i32")]
    points: Option<i32>,
    #[serde(rename = "ast", deserialize_with = "parse_opt_i32")]
    assists: Option<i32>,
    #[serde(rename = "trb", deserialize_with = "parse_opt_i32")]
    rebounds_total: Option<i32>,
    #[serde(rename = "stl", deserialize_with = "parse_opt_i32")]
    steals: Option<i32>,
    #[serde(rename = "blk", deserialize_with = "parse_opt_i32")]
    blocks: Option<i32>,
    #[serde(rename = "fg", deserialize_with = "parse_opt_i32")]
    fgm: Option<i32>,
    #[serde(rename = "fga", deserialize_with = "parse_opt_i32")]
    fga: Option<i32>,
    #[serde(rename = "x3p", deserialize_with = "parse_opt_i32")]
    fg3m: Option<i32>,
    #[serde(rename = "x3pa", deserialize_with = "parse_opt_i32")]
    fg3a: Option<i32>,
    #[serde(rename = "ft", deserialize_with = "parse_opt_i32")]
    ftm: Option<i32>,
    #[serde(rename = "fta", deserialize_with = "parse_opt_i32")]
    fta: Option<i32>,
    #[serde(rename = "tov", deserialize_with = "parse_opt_i32")]
    turnovers: Option<i32>,
    #[serde(rename = "pf", deserialize_with = "parse_opt_i32")]
    pf: Option<i32>,
}

#[derive(Debug, Deserialize)]
struct PlayerSeasonAdvancedRow {
    #[serde(rename = "season")]
    season: i32,
    #[serde(rename = "player_id")]
    player_id: String,
    #[serde(rename = "team")]
    team_abbrev: String,
    #[serde(rename = "mp", deserialize_with = "parse_opt_f64")]
    minutes: Option<f64>,
    #[serde(rename = "per", deserialize_with = "parse_opt_f64")]
    per: Option<f64>,
    #[serde(rename = "ts_percent", deserialize_with = "parse_opt_f64")]
    ts_percent: Option<f64>,
    #[serde(rename = "usg_percent", deserialize_with = "parse_opt_f64")]
    usg_percent: Option<f64>,
    #[serde(rename = "ows", deserialize_with = "parse_opt_f64")]
    ows: Option<f64>,
    #[serde(rename = "dws", deserialize_with = "parse_opt_f64")]
    dws: Option<f64>,
    #[serde(rename = "ws", deserialize_with = "parse_opt_f64")]
    ws: Option<f64>,
    #[serde(rename = "bpm", deserialize_with = "parse_opt_f64")]
    bpm: Option<f64>,
    #[serde(rename = "vorp", deserialize_with = "parse_opt_f64")]
    vorp: Option<f64>,
}

#[derive(Debug, Deserialize)]
struct TeamSeasonTotalsRow {
    #[serde(rename = "season")]
    season: i32,
    #[serde(rename = "abbreviation")]
    team_abbrev: String,
    #[serde(rename = "g", deserialize_with = "parse_opt_i32")]
    games: Option<i32>,
    #[serde(rename = "mp", deserialize_with = "parse_opt_f64")]
    minutes: Option<f64>,
    #[serde(rename = "pts", deserialize_with = "parse_opt_i32")]
    points: Option<i32>,
    #[serde(rename = "ast", deserialize_with = "parse_opt_i32")]
    assists: Option<i32>,
    #[serde(rename = "trb", deserialize_with = "parse_opt_i32")]
    rebounds_total: Option<i32>,
    #[serde(rename = "fg", deserialize_with = "parse_opt_i32")]
    fgm: Option<i32>,
    #[serde(rename = "fga", deserialize_with = "parse_opt_i32")]
    fga: Option<i32>,
    #[serde(rename = "x3p", deserialize_with = "parse_opt_i32")]
    fg3m: Option<i32>,
    #[serde(rename = "x3pa", deserialize_with = "parse_opt_i32")]
    fg3a: Option<i32>,
    #[serde(rename = "ft", deserialize_with = "parse_opt_i32")]
    ftm: Option<i32>,
    #[serde(rename = "fta", deserialize_with = "parse_opt_i32")]
    fta: Option<i32>,
    #[serde(rename = "tov", deserialize_with = "parse_opt_i32")]
    turnovers: Option<i32>,
    #[serde(rename = "pf", deserialize_with = "parse_opt_i32")]
    pf: Option<i32>,
}

#[derive(Debug, Deserialize)]
struct TeamSummaryRow {
    #[serde(rename = "season")]
    season: i32,
    #[serde(rename = "abbreviation")]
    team_abbrev: String,
    #[serde(rename = "w", deserialize_with = "parse_opt_i32")]
    wins: Option<i32>,
    #[serde(rename = "l", deserialize_with = "parse_opt_i32")]
    losses: Option<i32>,
    #[serde(rename = "srs", deserialize_with = "parse_opt_f64")]
    srs: Option<f64>,
    #[serde(rename = "pace", deserialize_with = "parse_opt_f64")]
    pace: Option<f64>,
    #[serde(rename = "o_rtg", deserialize_with = "parse_opt_f64")]
    off_rtg: Option<f64>,
    #[serde(rename = "d_rtg", deserialize_with = "parse_opt_f64")]
    def_rtg: Option<f64>,
    #[serde(rename = "n_rtg", deserialize_with = "parse_opt_f64")]
    net_rtg: Option<f64>,
    #[serde(rename = "playoffs", deserialize_with = "parse_opt_bool")]
    playoffs: Option<bool>,
}

#[derive(Debug, Deserialize)]
struct AllStarRow {
    #[serde(rename = "season")]
    season: i32,
    #[serde(rename = "player_id", deserialize_with = "parse_opt_string")]
    player_id: Option<String>,
    #[serde(rename = "player", deserialize_with = "parse_opt_string")]
    player_name: Option<String>,
    #[serde(rename = "team", deserialize_with = "parse_opt_string")]
    team_abbrev: Option<String>,
}

#[derive(Debug, Deserialize)]
struct EndSeasonRow {
    #[serde(rename = "season")]
    season: i32,
    #[serde(rename = "type")]
    award_type: String,
    #[serde(rename = "number_tm")]
    team_number: String,
    #[serde(rename = "player", deserialize_with = "parse_opt_string")]
    player_name: Option<String>,
    #[serde(rename = "player_id", deserialize_with = "parse_opt_string")]
    player_id: Option<String>,
}

#[derive(Debug, Deserialize)]
struct EndSeasonVoteRow {
    #[serde(rename = "season")]
    season: i32,
    #[serde(rename = "type")]
    award_type: String,
    #[serde(rename = "number_tm", deserialize_with = "parse_opt_string")]
    team_number: Option<String>,
    #[serde(rename = "player", deserialize_with = "parse_opt_string")]
    player_name: Option<String>,
    #[serde(rename = "player_id", deserialize_with = "parse_opt_string")]
    player_id: Option<String>,
    #[serde(rename = "pts_won", deserialize_with = "parse_opt_i32")]
    points_won: Option<i32>,
    #[serde(rename = "pts_max", deserialize_with = "parse_opt_i32")]
    points_max: Option<i32>,
    #[serde(rename = "share", deserialize_with = "parse_opt_f64")]
    share: Option<f64>,
}
