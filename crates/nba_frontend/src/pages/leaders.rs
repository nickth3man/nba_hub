use leptos::*;
use leptos_router::use_params_map;
use serde_json::json;

use crate::components::{DataTable, OnThisPage, PageHeader, SeasonSelect, Section, TableColumn};
use crate::convex::convex_query;
use crate::data::stat_definition;
use crate::models::{LeaderRow, SeasonLeadersResponse, SeasonRow};

async fn fetch_seasons() -> Result<Vec<SeasonRow>, String> {
    convex_query("seasons:listSeasons", json!({})).await
}

async fn fetch_leaders(season_year: i32) -> Result<SeasonLeadersResponse, String> {
    convex_query(
        "leaders:getSeasonLeaders",
        json!({ "seasonYear": season_year }),
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

#[component]
pub fn LeadersPage() -> impl IntoView {
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
                title="Season Leaders".to_string()
                subtitle="Top performers for each major counting stat.".to_string()
                callout=Some("Beginner tip: focus on value and per-game columns before exploring advanced metrics.".to_string())
            />

            <Section id={"leader-season".to_string()} title={"Season".to_string()}>
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
                    ("points".to_string(), "Points".to_string()),
                    ("rebounds".to_string(), "Rebounds".to_string()),
                    ("assists".to_string(), "Assists".to_string()),
                    ("steals".to_string(), "Steals".to_string()),
                    ("blocks".to_string(), "Blocks".to_string()),
                ]
            />

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
                    let points_columns = columns.clone();
                    let rebounds_columns = columns.clone();
                    let assists_columns = columns.clone();
                    let steals_columns = columns.clone();
                    let blocks_columns = columns.clone();

                    view! {
                        <Section id={"points".to_string()} title={"Points".to_string()}>
                            <DataTable columns=points_columns rows=leader_rows(&data.points) />
                        </Section>
                        <Section id={"rebounds".to_string()} title={"Rebounds".to_string()}>
                            <DataTable columns=rebounds_columns rows=leader_rows(&data.rebounds) />
                        </Section>
                        <Section id={"assists".to_string()} title={"Assists".to_string()}>
                            <DataTable columns=assists_columns rows=leader_rows(&data.assists) />
                        </Section>
                        <Section id={"steals".to_string()} title={"Steals".to_string()}>
                            <DataTable columns=steals_columns rows=leader_rows(&data.steals) />
                        </Section>
                        <Section id={"blocks".to_string()} title={"Blocks".to_string()}>
                            <DataTable columns=blocks_columns rows=leader_rows(&data.blocks) />
                        </Section>
                    }
                    .into_view()
                }
            }}
        </section>
    }
}
