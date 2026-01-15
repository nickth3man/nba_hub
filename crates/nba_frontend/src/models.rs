use serde::{Deserialize, Serialize};

#[derive(Clone, Debug, Deserialize, Serialize)]
pub struct PlayerDirectoryEntry {
    pub player_bref_id: String,
    pub player_name: String,
    pub first_season: i32,
    pub last_season: i32,
    pub seasons_count: usize,
    pub teams_count: usize,
}

#[derive(Clone, Debug, Deserialize, Serialize)]
pub struct PlayerProfileResponse {
    pub player: PlayerProfileHeader,
    pub totals: Vec<PlayerSeasonTotal>,
    pub advanced: Vec<PlayerSeasonAdvanced>,
}

#[derive(Clone, Debug, Deserialize, Serialize)]
pub struct PlayerProfileHeader {
    pub player_bref_id: String,
    pub player_name: String,
    pub first_season: Option<i32>,
    pub last_season: Option<i32>,
    pub teams: Vec<String>,
}

#[derive(Clone, Debug, Deserialize, Serialize)]
pub struct PlayerSeasonTotal {
    pub season_year: i32,
    pub player_bref_id: String,
    pub player_name: Option<String>,
    pub team_abbrev: String,
    pub games: i32,
    pub games_started: Option<i32>,
    pub minutes: Option<f64>,
    pub points: Option<i32>,
    pub assists: Option<i32>,
    pub rebounds_total: Option<i32>,
    pub steals: Option<i32>,
    pub blocks: Option<i32>,
    pub fgm: Option<i32>,
    pub fga: Option<i32>,
    pub fg3m: Option<i32>,
    pub fg3a: Option<i32>,
    pub ftm: Option<i32>,
    pub fta: Option<i32>,
    pub turnovers: Option<i32>,
    pub pf: Option<i32>,
}

#[derive(Clone, Debug, Deserialize, Serialize)]
pub struct PlayerSeasonAdvanced {
    pub season_year: i32,
    pub player_bref_id: String,
    pub team_abbrev: String,
    pub minutes: Option<f64>,
    pub per: Option<f64>,
    pub ts_percent: Option<f64>,
    pub usg_percent: Option<f64>,
    pub ows: Option<f64>,
    pub dws: Option<f64>,
    pub ws: Option<f64>,
    pub bpm: Option<f64>,
    pub vorp: Option<f64>,
}

#[derive(Clone, Debug, Deserialize, Serialize)]
pub struct TeamHistoryRow {
    pub team_history_id: i32,
    pub team_id: i64,
    pub effective_start: String,
    pub effective_end: Option<String>,
    pub city: String,
    pub nickname: String,
    pub abbreviation: Option<String>,
    pub is_active: bool,
}

#[derive(Clone, Debug, Deserialize, Serialize)]
pub struct TeamProfileResponse {
    pub team: Option<TeamHistoryRow>,
    pub totals: Vec<TeamSeasonTotal>,
    pub advanced: Vec<TeamSeasonAdvanced>,
    pub standings: Vec<StandingRow>,
}

#[derive(Clone, Debug, Deserialize, Serialize)]
pub struct TeamSeasonTotal {
    pub season_year: i32,
    pub team_abbrev: String,
    pub games: i32,
    pub minutes: Option<f64>,
    pub points: Option<i32>,
    pub assists: Option<i32>,
    pub rebounds_total: Option<i32>,
    pub fgm: Option<i32>,
    pub fga: Option<i32>,
    pub fg3m: Option<i32>,
    pub fg3a: Option<i32>,
    pub ftm: Option<i32>,
    pub fta: Option<i32>,
    pub turnovers: Option<i32>,
    pub pf: Option<i32>,
}

#[derive(Clone, Debug, Deserialize, Serialize)]
pub struct TeamSeasonAdvanced {
    pub season_year: i32,
    pub team_abbrev: String,
    pub wins: i32,
    pub losses: i32,
    pub srs: Option<f64>,
    pub pace: Option<f64>,
    pub off_rtg: Option<f64>,
    pub def_rtg: Option<f64>,
    pub net_rtg: Option<f64>,
}

#[derive(Clone, Debug, Deserialize, Serialize)]
pub struct StandingRow {
    pub season_year: i32,
    pub team_abbrev: String,
    pub wins: i32,
    pub losses: i32,
    pub playoffs: bool,
}

#[derive(Clone, Debug, Deserialize, Serialize)]
pub struct SeasonRow {
    pub season_id: i32,
    pub league_id: i32,
    pub season_year: i32,
    pub start_date: Option<String>,
    pub end_date: Option<String>,
}

#[derive(Clone, Debug, Deserialize, Serialize)]
pub struct SeasonSummaryResponse {
    pub season: Option<SeasonRow>,
    pub standings: Vec<StandingRow>,
    #[serde(rename = "teamTotals")]
    pub team_totals: Vec<TeamSeasonTotal>,
    #[serde(rename = "teamAdvanced")]
    pub team_advanced: Vec<TeamSeasonAdvanced>,
}

#[derive(Clone, Debug, Deserialize, Serialize)]
pub struct LeaderRow {
    pub player_bref_id: String,
    pub player_name: String,
    pub teams: Vec<String>,
    pub value: f64,
    pub per_game: f64,
    pub games: i32,
}

#[derive(Clone, Debug, Deserialize, Serialize)]
pub struct SeasonLeadersResponse {
    pub points: Vec<LeaderRow>,
    pub rebounds: Vec<LeaderRow>,
    pub assists: Vec<LeaderRow>,
    pub steals: Vec<LeaderRow>,
    pub blocks: Vec<LeaderRow>,
}

#[derive(Clone, Debug, Deserialize, Serialize)]
pub struct AwardRow {
    pub award_key: String,
    pub award_type: String,
    pub season_year: i32,
    pub player_bref_id: Option<String>,
    pub player_name: Option<String>,
    pub team_abbrev: Option<String>,
    pub rank: Option<i32>,
    pub points_won: Option<i32>,
    pub points_max: Option<i32>,
    pub share: Option<f64>,
}

#[derive(Clone, Debug, Deserialize, Serialize)]
pub struct DraftRow {
    pub season_year: i32,
    pub pick_overall: i32,
    pub round_number: Option<i32>,
    pub pick_in_round: Option<i32>,
    pub team_abbrev: Option<String>,
    pub player_bref_id: Option<String>,
    pub player_name: Option<String>,
    pub college: Option<String>,
}

#[derive(Clone, Debug, Deserialize, Serialize)]
pub struct TransactionRow {
    pub transaction_id: String,
    pub season_year: i32,
    pub team_abbrev: Option<String>,
    pub player_bref_id: Option<String>,
    pub details: String,
}
