use leptos::*;
use leptos_router::use_params_map;
use serde_json::json;

use crate::components::{
    Badge, BeginnerToggle, DataTable, OnThisPage, PageHeader, Section, TableColumn,
};
use crate::convex::convex_query;
use crate::data::stat_definition;
use crate::models::{PlayerProfileResponse, PlayerSeasonAdvanced, PlayerSeasonTotal};
use crate::utils::{format_optional_f64, format_optional_i32, format_percent, percent_from_counts};

async fn fetch_player_profile(player_bref_id: String) -> Result<PlayerProfileResponse, String> {
    convex_query(
        "players:getPlayerProfile",
        json!({ "playerBrefId": player_bref_id }),
    )
    .await
}

fn stat_column(label: &str) -> TableColumn {
    let mut column = TableColumn::new(label).with_class("num");
    if let Some(stat) = stat_definition(label) {
        column = column.with_description(stat.description.to_string());
    }
    column
}

fn totals_rows(rows: &[PlayerSeasonTotal]) -> Vec<Vec<View>> {
    rows.iter()
        .map(|row| {
            let fg_pct = format_percent(percent_from_counts(row.fgm, row.fga));
            let fg3_pct = format_percent(percent_from_counts(row.fg3m, row.fg3a));
            let ft_pct = format_percent(percent_from_counts(row.ftm, row.fta));
            vec![
                view! { <span>{row.season_year}</span> }.into_view(),
                view! { <span>{row.team_abbrev.clone()}</span> }.into_view(),
                view! { <span>{row.games}</span> }.into_view(),
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

fn advanced_rows(rows: &[PlayerSeasonAdvanced]) -> Vec<Vec<View>> {
    rows.iter()
        .map(|row| {
            vec![
                view! { <span>{row.season_year}</span> }.into_view(),
                view! { <span>{row.team_abbrev.clone()}</span> }.into_view(),
                view! { <span>{format_optional_f64(row.per, 1)}</span> }.into_view(),
                view! { <span>{format_percent(row.ts_percent)}</span> }.into_view(),
                view! { <span>{format_percent(row.usg_percent)}</span> }.into_view(),
                view! { <span>{format_optional_f64(row.ws, 1)}</span> }.into_view(),
                view! { <span>{format_optional_f64(row.bpm, 1)}</span> }.into_view(),
                view! { <span>{format_optional_f64(row.vorp, 1)}</span> }.into_view(),
            ]
        })
        .collect()
}

#[component]
pub fn PlayerProfile() -> impl IntoView {
    let params = use_params_map();
    let player_id = move || {
        params
            .with(|params| params.get("player_bref_id").cloned())
            .unwrap_or_default()
    };

    let profile = create_resource(player_id, |id| async move {
        if id.is_empty() {
            return Err("Missing player id".to_string());
        }
        fetch_player_profile(id).await
    });

    let (beginner, set_beginner) = create_signal(true);

    view! {
        <section class="page">
            {move || match profile.get() {
                None => view! { <p>"Loading player profile..."</p> }.into_view(),
                Some(Err(message)) => view! { <p class="error">{message}</p> }.into_view(),
                Some(Ok(data)) => {
                    let player = data.player;
                    let season_range = match (player.first_season, player.last_season) {
                        (Some(first), Some(last)) => format!("{}-{}", first, last),
                        _ => "-".to_string(),
                    };

                    let totals_columns = vec![
                        TableColumn::new("Season"),
                        TableColumn::new("Team"),
                        stat_column("G"),
                        stat_column("PTS"),
                        stat_column("REB"),
                        stat_column("AST"),
                        stat_column("FG%"),
                        stat_column("3P%"),
                        stat_column("FT%"),
                    ];

                    let advanced_columns = vec![
                        TableColumn::new("Season"),
                        TableColumn::new("Team"),
                        stat_column("PER"),
                        stat_column("TS%"),
                        stat_column("USG%"),
                        stat_column("WS"),
                        stat_column("BPM"),
                        stat_column("VORP"),
                    ];

                    view! {
                        <PageHeader
                            title=player.player_name.clone()
                            subtitle=format!("Seasons: {} · Teams: {}", season_range, player.teams.join(", "))
                            callout=Some("What am I looking at? This page shows season-by-season totals and advanced metrics from Basketball-Reference data.".to_string())
                        />

                        <OnThisPage
                            items=vec![
                                ("overview".to_string(), "Overview".to_string()),
                                ("season-totals".to_string(), "Season Totals".to_string()),
                                ("advanced".to_string(), "Advanced Metrics".to_string()),
                            ]
                        />

                        <Section id={"overview".to_string()} title={"Overview".to_string()}>
                            <div class="control-row">
                                <Badge text=format!("BRef ID: {}", player.player_bref_id) />
                                <Badge text=format!("Seasons: {}", season_range) />
                                <Badge text=format!("Teams: {}", player.teams.join(", ")) />
                            </div>
                        </Section>

                        <Section id={"season-totals".to_string()} title={"Season Totals".to_string()}>
                            <div class="control-row">
                                <BeginnerToggle is_on=beginner set_on=set_beginner />
                            </div>
                            <DataTable columns=totals_columns rows=totals_rows(&data.totals) />
                        </Section>

                        <Section id={"advanced".to_string()} title={"Advanced Metrics".to_string()}>
                            {move || {
                                if beginner.get() {
                                    view! { <p>"Switch off Beginner mode to view advanced metrics."</p> }.into_view()
                                } else {
                                    view! { <DataTable columns=advanced_columns.clone() rows=advanced_rows(&data.advanced) /> }
                                        .into_view()
                                }
                            }}
                        </Section>
                    }
                    .into_view()
                }
            }}
        </section>
    }
}
