use leptos::*;
use leptos_router::use_params_map;
use serde_json::json;
use std::collections::BTreeMap;

use crate::components::{DataTable, PageHeader, SeasonSelect, Section, TableColumn};
use crate::convex::convex_query;
use crate::models::{AwardRow, SeasonRow};

async fn fetch_seasons() -> Result<Vec<SeasonRow>, String> {
    convex_query("seasons:listSeasons", json!({})).await
}

async fn fetch_awards(season_year: i32) -> Result<Vec<AwardRow>, String> {
    convex_query(
        "awards:listAwardsBySeason",
        json!({ "seasonYear": season_year }),
    )
    .await
}

#[component]
pub fn AwardsPage() -> impl IntoView {
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
    let awards = create_resource(
        move || selected_year.get(),
        |year| async move {
            match year {
                Some(year) => fetch_awards(year).await.map(Some),
                None => Ok(None),
            }
        },
    );

    view! {
        <section class="page">
            <PageHeader
                title="Awards".to_string()
                subtitle="MVP, DPOY, All-NBA, and award voting by season.".to_string()
                callout=Some("Beginner tip: start with MVP to see the highest-ranked players.".to_string())
            />

            <Section id={"award-season".to_string()} title={"Season".to_string()}>
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

            {move || match awards.get() {
                None => view! { <p>"Loading awards..."</p> }.into_view(),
                Some(Err(message)) => view! { <p class="error">{message}</p> }.into_view(),
                Some(Ok(None)) => view! { <p>"Select a season to view awards."</p> }.into_view(),
                Some(Ok(Some(list))) => {
                    let mut grouped: BTreeMap<String, Vec<AwardRow>> = BTreeMap::new();
                    for award in list {
                        grouped.entry(award.award_type.clone()).or_default().push(award);
                    }

                    grouped
                        .into_iter()
                        .map(|(award_type, rows)| {
                            let columns = vec![
                                TableColumn::new("Player"),
                                TableColumn::new("Team"),
                                TableColumn::new("Rank"),
                                TableColumn::new("Share"),
                            ];

                            let table_rows = rows
                                .into_iter()
                                .map(|award| {
                                    let player_name = award
                                        .player_name
                                        .clone()
                                        .or(award.player_bref_id.clone())
                                        .unwrap_or_else(|| "-".to_string());
                                    let player_cell = if let Some(player_id) = award.player_bref_id.clone() {
                                        let link = format!("/players/{}", player_id);
                                        view! { <a href={link}>{player_name}</a> }.into_view()
                                    } else {
                                        view! { <span>{player_name}</span> }.into_view()
                                    };
                                    vec![
                                        player_cell,
                                        view! { <span>{award.team_abbrev.unwrap_or_else(|| "-".to_string())}</span> }.into_view(),
                                        view! { <span>{award.rank.map(|val| val.to_string()).unwrap_or_else(|| "-".to_string())}</span> }.into_view(),
                                        view! { <span>{award.share.map(|val| format!("{:.3}", val)).unwrap_or_else(|| "-".to_string())}</span> }.into_view(),
                                    ]
                                })
                                .collect();

                            view! {
                                <Section id={award_type.to_lowercase().replace(' ', "-")}
                                    title={award_type}>
                                    <DataTable columns=columns rows=table_rows />
                                </Section>
                            }
                        })
                        .collect_view()
                        .into_view()
                }
            }}
        </section>
    }
}
