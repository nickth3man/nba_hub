use leptos::*;
use leptos_router::use_params_map;
use serde_json::json;

use crate::components::{DataTable, OnThisPage, PageHeader, SeasonSelect, Section, TableColumn};
use crate::convex::convex_query;
use crate::data::stat_definition;
use crate::models::{
    LeaderRow, SeasonLeadersResponse, SeasonRow, SeasonSummaryResponse, StandingRow,
    TeamHistoryRow, TeamSeasonAdvanced, TeamSeasonTotal,
};
use crate::utils::{
    build_team_lookup, format_optional_f64, format_optional_i32, format_percent,
    percent_from_counts,
};

async fn fetch_summary(season_year: i32) -> Result<SeasonSummaryResponse, String> {
    convex_query(
        "seasons:getSeasonSummary",
        json!({ "seasonYear": season_year }),
    )
    .await
}

async fn fetch_leaders(season_year: i32) -> Result<SeasonLeadersResponse, String> {
    convex_query(
        "leaders:getSeasonLeaders",
        json!({ "seasonYear": season_year }),
    )
    .await
}

async fn fetch_seasons() -> Result<Vec<SeasonRow>, String> {
    convex_query("seasons:listSeasons", json!({})).await
}

async fn fetch_team_history() -> Result<Vec<TeamHistoryRow>, String> {
    convex_query("teams:listTeams", json!({ "activeOnly": false })).await
}

fn stat_column(label: &str) -> TableColumn {
    let mut column = TableColumn::new(label).with_class("num");
    if let Some(stat) = stat_definition(label) {
        column = column.with_description(stat.description.to_string());
    }
    column
}

fn leader_rows(leaders: &[LeaderRow]) -> Vec<Vec<View>> {
    leaders
        .iter()
        .map(|leader| {
            let link = format!("/players/{}", leader.player_bref_id);
            vec![
                view! { <a href={link}>{leader.player_name.clone()}</a> }.into_view(),
                view! { <span>{leader.teams.join(", ")}</span> }.into_view(),
                view! { <span>{format!("{:.0}", leader.value)}</span> }.into_view(),
                view! { <span>{format!("{:.1}", leader.per_game)}</span> }.into_view(),
                view! { <span>{leader.games}</span> }.into_view(),
            ]
        })
        .collect()
}

fn standings_rows(
    rows: &[StandingRow],
    team_lookup: &std::collections::HashMap<String, String>,
) -> Vec<Vec<View>> {
    rows.iter()
        .map(|row| {
            let team = team_lookup
                .get(&row.team_abbrev)
                .cloned()
                .unwrap_or_else(|| row.team_abbrev.clone());
            vec![
                view! { <span>{team}</span> }.into_view(),
                view! { <span>{row.wins}</span> }.into_view(),
                view! { <span>{row.losses}</span> }.into_view(),
                view! { <span>{if row.playoffs { "Yes" } else { "No" }}</span> }.into_view(),
            ]
        })
        .collect()
}

fn team_totals_rows(
    rows: &[TeamSeasonTotal],
    team_lookup: &std::collections::HashMap<String, String>,
) -> Vec<Vec<View>> {
    rows.iter()
        .map(|row| {
            let team = team_lookup
                .get(&row.team_abbrev)
                .cloned()
                .unwrap_or_else(|| row.team_abbrev.clone());
            let fg_pct = format_percent(percent_from_counts(row.fgm, row.fga));
            let fg3_pct = format_percent(percent_from_counts(row.fg3m, row.fg3a));
            let ft_pct = format_percent(percent_from_counts(row.ftm, row.fta));
            vec![
                view! { <span>{team}</span> }.into_view(),
                view! { <span>{format_optional_i32(row.points)}</span> }.into_view(),
                view! { <span>{format_optional_i32(row.rebounds_total)}</span> }.into_view(),
                view! { <span>{format_optional_i32(row.assists)}</span> }.into_view(),
                view! { <span>{fg_pct}</span> }.into_view(),
                view! { <span>{fg3_pct}</span> }.into_view(),
                view! { <span>{ft_pct}</span> }.into_view(),
            ]
        })
        .collect()
}

fn team_advanced_rows(
    rows: &[TeamSeasonAdvanced],
    team_lookup: &std::collections::HashMap<String, String>,
) -> Vec<Vec<View>> {
    rows.iter()
        .map(|row| {
            let team = team_lookup
                .get(&row.team_abbrev)
                .cloned()
                .unwrap_or_else(|| row.team_abbrev.clone());
            vec![
                view! { <span>{team}</span> }.into_view(),
                view! { <span>{row.wins}</span> }.into_view(),
                view! { <span>{row.losses}</span> }.into_view(),
                view! { <span>{format_optional_f64(row.srs, 1)}</span> }.into_view(),
                view! { <span>{format_optional_f64(row.pace, 1)}</span> }.into_view(),
                view! { <span>{format_optional_f64(row.off_rtg, 1)}</span> }.into_view(),
                view! { <span>{format_optional_f64(row.def_rtg, 1)}</span> }.into_view(),
                view! { <span>{format_optional_f64(row.net_rtg, 1)}</span> }.into_view(),
            ]
        })
        .collect()
}

#[component]
pub fn SeasonDetail() -> impl IntoView {
    let params = use_params_map();
    let route_year = move || {
        params
            .with(|params| params.get("year").cloned())
            .and_then(|value| value.parse::<i32>().ok())
    };

    let selected_year = create_rw_signal(route_year());

    create_effect(move |_| {
        if let Some(route) = route_year() {
            selected_year.set(Some(route));
        }
    });

    let seasons = create_resource(|| (), |_| fetch_seasons());
    let teams = create_resource(|| (), |_| fetch_team_history());

    let summary = create_resource(
        move || selected_year.get(),
        |year| async move {
            match year {
                Some(year) => fetch_summary(year).await.map(Some),
                None => Ok(None),
            }
        },
    );

    let leaders = create_resource(
        move || selected_year.get(),
        |year| async move {
            match year {
                Some(year) => fetch_leaders(year).await.map(Some),
                None => Ok(None),
            }
        },
    );

    view! {
        <section class="page">
            <PageHeader
                title="Season Summary".to_string()
                subtitle="Standings, team stats, and leaders for a single season.".to_string()
                callout=Some("Beginner tip: start with the Standings and Team Ratings sections.".to_string())
            />

            <Section id={"season-picker".to_string()} title={"Season".to_string()}>
                {move || match seasons.get() {
                    None => view! { <p>"Loading seasons..."</p> }.into_view(),
                    Some(Err(message)) => view! { <p class="error">{message}</p> }.into_view(),
                    Some(Ok(list)) => {
                        let options = list.iter().map(|season| season.season_year).collect::<Vec<_>>();
                        let selected = selected_year.get().unwrap_or_else(|| list.first().map(|season| season.season_year).unwrap_or(0));
                        view! {
                            <SeasonSelect
                                options=options
                                selected=selected
                                on_change=Callback::new(move |year| selected_year.set(Some(year)))
                            />
                        }
                        .into_view()
                    }
                }}
            </Section>

            <OnThisPage
                items=vec![
                    ("standings".to_string(), "Standings".to_string()),
                    ("team-totals".to_string(), "Team Totals".to_string()),
                    ("team-ratings".to_string(), "Team Ratings".to_string()),
                    ("leaders".to_string(), "Leaders".to_string()),
                ]
            />

            {move || {
                let team_lookup = teams
                    .get()
                    .and_then(|data| data.ok())
                    .map(|list| build_team_lookup(&list))
                    .unwrap_or_default();

                match summary.get() {
                    None => view! { <p>"Loading season data..."</p> }.into_view(),
                    Some(Err(message)) => view! { <p class="error">{message}</p> }.into_view(),
                    Some(Ok(None)) => view! { <p>"Select a season to view summary."</p> }.into_view(),
                    Some(Ok(Some(data))) => {
                        let standings_columns = vec![
                            TableColumn::new("Team"),
                            stat_column("W"),
                            stat_column("L"),
                            TableColumn::new("Playoffs"),
                        ];
                        let totals_columns = vec![
                            TableColumn::new("Team"),
                            stat_column("PTS"),
                            stat_column("REB"),
                            stat_column("AST"),
                            stat_column("FG%"),
                            stat_column("3P%"),
                            stat_column("FT%"),
                        ];
                        let ratings_columns = vec![
                            TableColumn::new("Team"),
                            stat_column("W"),
                            stat_column("L"),
                            stat_column("SRS"),
                            stat_column("PACE"),
                            stat_column("ORtg"),
                            stat_column("DRtg"),
                            stat_column("NetRtg"),
                        ];

                        let standings_data = standings_rows(&data.standings, &team_lookup);
                        let totals_data = team_totals_rows(&data.team_totals, &team_lookup);
                        let ratings_data = team_advanced_rows(&data.team_advanced, &team_lookup);

                        view! {
                            <Section id={"standings".to_string()} title={"Standings".to_string()}>
                                <DataTable columns=standings_columns rows=standings_data />
                            </Section>

                            <Section id={"team-totals".to_string()} title={"Team Totals".to_string()}>
                                <DataTable columns=totals_columns rows=totals_data />
                            </Section>

                            <Section id={"team-ratings".to_string()} title={"Team Ratings".to_string()}>
                                <DataTable columns=ratings_columns rows=ratings_data />
                            </Section>
                        }
                        .into_view()
                    }
                }
            }}

            <Section id={"leaders".to_string()} title={"Leaders".to_string()}>
                {move || match leaders.get() {
                    None => view! { <p>"Loading leaders..."</p> }.into_view(),
                    Some(Err(message)) => view! { <p class="error">{message}</p> }.into_view(),
                    Some(Ok(None)) => view! { <p>"Select a season to view leaders."</p> }.into_view(),
                    Some(Ok(Some(data))) => {
                        let columns = vec![
                            TableColumn::new("Player"),
                            TableColumn::new("Teams"),
                            TableColumn::new("Value").with_class("num"),
                            TableColumn::new("Per Game").with_class("num"),
                            stat_column("G"),
                        ];
                        view! {
                            <DataTable columns=columns.clone() rows=leader_rows(&data.points) />
                            <DataTable columns=columns.clone() rows=leader_rows(&data.rebounds) />
                            <DataTable columns=columns.clone() rows=leader_rows(&data.assists) />
                        }
                        .into_view()
                    }
                }}
            </Section>
        </section>
    }
}
