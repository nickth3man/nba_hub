use leptos::*;
use leptos_router::use_params_map;
use serde_json::json;

use crate::components::{DataTable, PageHeader, SeasonSelect, Section, TableColumn};
use crate::convex::convex_query;
use crate::models::{DraftRow, SeasonRow};

async fn fetch_seasons() -> Result<Vec<SeasonRow>, String> {
    convex_query("seasons:listSeasons", json!({})).await
}

async fn fetch_draft(season_year: i32) -> Result<Vec<DraftRow>, String> {
    convex_query(
        "drafts:listDraftBySeason",
        json!({ "seasonYear": season_year }),
    )
    .await
}

#[component]
pub fn DraftPage() -> impl IntoView {
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
    let drafts = create_resource(
        move || selected_year.get(),
        |year| async move {
            match year {
                Some(year) => fetch_draft(year).await.map(Some),
                None => Ok(None),
            }
        },
    );

    view! {
        <section class="page">
            <PageHeader
                title="Draft History".to_string()
                subtitle="All draft picks for a selected season.".to_string()
                callout=Some("Beginner tip: focus on the first round to see the most prominent picks.".to_string())
            />

            <Section id={"draft-season".to_string()} title={"Season".to_string()}>
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

            <Section id={"draft-table".to_string()} title={"Draft Picks".to_string()}>
                {move || match drafts.get() {
                    None => view! { <p>"Loading draft..."</p> }.into_view(),
                    Some(Err(message)) => view! { <p class="error">{message}</p> }.into_view(),
                    Some(Ok(None)) => view! { <p>"Select a season to view the draft."</p> }.into_view(),
                    Some(Ok(Some(list))) => {
                        let columns = vec![
                            TableColumn::new("Pick"),
                            TableColumn::new("Round"),
                            TableColumn::new("Team"),
                            TableColumn::new("Player"),
                            TableColumn::new("College"),
                        ];

                        let rows = list
                            .into_iter()
                            .map(|pick| {
                                let player_name = pick
                                    .player_name
                                    .clone()
                                    .or(pick.player_bref_id.clone())
                                    .unwrap_or_else(|| "-".to_string());
                                let player_cell = if let Some(player_id) = pick.player_bref_id.clone() {
                                    let link = format!("/players/{}", player_id);
                                    view! { <a href={link}>{player_name}</a> }.into_view()
                                } else {
                                    view! { <span>{player_name}</span> }.into_view()
                                };
                                vec![
                                    view! { <span>{pick.pick_overall}</span> }.into_view(),
                                    view! { <span>{pick.round_number.map(|val| val.to_string()).unwrap_or_else(|| "-".to_string())}</span> }.into_view(),
                                    view! { <span>{pick.team_abbrev.unwrap_or_else(|| "-".to_string())}</span> }.into_view(),
                                    player_cell,
                                    view! { <span>{pick.college.unwrap_or_else(|| "-".to_string())}</span> }.into_view(),
                                ]
                            })
                            .collect();

                        view! { <DataTable columns=columns rows=rows /> }.into_view()
                    }
                }}
            </Section>
        </section>
    }
}
