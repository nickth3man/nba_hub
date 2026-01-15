use leptos::*;
use leptos_router::use_params_map;
use serde_json::json;

use crate::components::{
    Badge, BeginnerToggle, DataTable, OnThisPage, PageHeader, Section, TableColumn,
};
use crate::convex::convex_query;
use crate::data::stat_definition;
use crate::models::{StandingRow, TeamProfileResponse, TeamSeasonAdvanced, TeamSeasonTotal};
use crate::utils::{
    format_optional_f64, format_optional_i32, format_percent, format_team_label,
    percent_from_counts,
};

async fn fetch_team_profile(team_abbrev: String) -> Result<TeamProfileResponse, String> {
    convex_query("teams:getTeamProfile", json!({ "teamAbbrev": team_abbrev })).await
}

fn stat_column(label: &str) -> TableColumn {
    let mut column = TableColumn::new(label).with_class("num");
    if let Some(stat) = stat_definition(label) {
        column = column.with_description(stat.description.to_string());
    }
    column
}

fn totals_rows(rows: &[TeamSeasonTotal]) -> Vec<Vec<View>> {
    rows.iter()
        .map(|row| {
            let fg_pct = format_percent(percent_from_counts(row.fgm, row.fga));
            let fg3_pct = format_percent(percent_from_counts(row.fg3m, row.fg3a));
            let ft_pct = format_percent(percent_from_counts(row.ftm, row.fta));
            vec![
                view! { <span>{row.season_year}</span> }.into_view(),
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

fn advanced_rows(rows: &[TeamSeasonAdvanced]) -> Vec<Vec<View>> {
    rows.iter()
        .map(|row| {
            vec![
                view! { <span>{row.season_year}</span> }.into_view(),
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

fn standings_rows(rows: &[StandingRow]) -> Vec<Vec<View>> {
    rows.iter()
        .map(|row| {
            vec![
                view! { <span>{row.season_year}</span> }.into_view(),
                view! { <span>{row.wins}</span> }.into_view(),
                view! { <span>{row.losses}</span> }.into_view(),
                view! { <span>{if row.playoffs { "Yes" } else { "No" }}</span> }.into_view(),
            ]
        })
        .collect()
}

#[component]
pub fn TeamProfile() -> impl IntoView {
    let params = use_params_map();
    let team_abbrev = move || {
        params
            .with(|params| params.get("team_abbrev").cloned())
            .unwrap_or_default()
    };

    let profile = create_resource(team_abbrev, |id| async move {
        if id.is_empty() {
            return Err("Missing team abbreviation".to_string());
        }
        fetch_team_profile(id).await
    });

    let (beginner, set_beginner) = create_signal(true);

    view! {
        <section class="page">
            {move || match profile.get() {
                None => view! { <p>"Loading team profile..."</p> }.into_view(),
                Some(Err(message)) => view! { <p class="error">{message}</p> }.into_view(),
                Some(Ok(data)) => {
                    let team_label = data
                        .team
                        .as_ref()
                        .map(|team| format_team_label(&team.city, &team.nickname))
                        .unwrap_or_else(|| "Team Profile".to_string());
                    let status = data
                        .team
                        .as_ref()
                        .map(|team| if team.is_active { "Active" } else { "Inactive" })
                        .unwrap_or("Unknown");

                    let totals_columns = vec![
                        TableColumn::new("Season"),
                        stat_column("PTS"),
                        stat_column("REB"),
                        stat_column("AST"),
                        stat_column("FG%"),
                        stat_column("3P%"),
                        stat_column("FT%"),
                    ];

                    let advanced_columns = vec![
                        TableColumn::new("Season"),
                        stat_column("W"),
                        stat_column("L"),
                        stat_column("SRS"),
                        stat_column("PACE"),
                        stat_column("ORtg"),
                        stat_column("DRtg"),
                        stat_column("NetRtg"),
                    ];

                    let standings_columns = vec![
                        TableColumn::new("Season"),
                        stat_column("W"),
                        stat_column("L"),
                        TableColumn::new("Playoffs"),
                    ];

                    let totals_len = data.totals.len();
                    let totals_data = totals_rows(&data.totals);
                    let advanced_data = advanced_rows(&data.advanced);
                    let standings_data = standings_rows(&data.standings);

                    view! {
                        <PageHeader
                            title=team_label.clone()
                            subtitle=format!("Status: {} · Abbrev: {}", status, data.team.as_ref().and_then(|team| team.abbreviation.clone()).unwrap_or_else(|| "-".to_string()))
                            callout=Some("What am I looking at? This page tracks season totals, ratings, and standings for the franchise.".to_string())
                        />

                        <OnThisPage
                            items=vec![
                                ("overview".to_string(), "Overview".to_string()),
                                ("season-totals".to_string(), "Season Totals".to_string()),
                                ("ratings".to_string(), "Ratings".to_string()),
                                ("standings".to_string(), "Standings".to_string()),
                            ]
                        />

                        <Section id={"overview".to_string()} title={"Overview".to_string()}>
                            <div class="control-row">
                                <Badge text=format!("Status: {}", status) />
                                <Badge text=format!("Seasons tracked: {}", totals_len) />
                            </div>
                        </Section>

                        <Section id={"season-totals".to_string()} title={"Season Totals".to_string()}>
                            <div class="control-row">
                                <BeginnerToggle is_on=beginner set_on=set_beginner />
                            </div>
                            <DataTable columns=totals_columns rows=totals_data />
                        </Section>

                        <Section id={"ratings".to_string()} title={"Ratings".to_string()}>
                            {move || {
                                if beginner.get() {
                                    view! { <p>"Switch off Beginner mode to view ratings."</p> }.into_view()
                                } else {
                                    view! { <DataTable columns=advanced_columns.clone() rows=advanced_data.clone() /> }
                                        .into_view()
                                }
                            }}
                        </Section>

                        <Section id={"standings".to_string()} title={"Standings".to_string()}>
                            <DataTable columns=standings_columns rows=standings_data />
                        </Section>
                    }
                    .into_view()
                }
            }}
        </section>
    }
}
