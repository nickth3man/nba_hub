use leptos::*;
use serde_json::json;

use crate::components::{DataTable, PageHeader, Section, TableColumn};
use crate::convex::convex_query;
use crate::models::SeasonRow;

async fn fetch_seasons() -> Result<Vec<SeasonRow>, String> {
    convex_query("seasons:listSeasons", json!({})).await
}

fn league_label(league_id: i32) -> &'static str {
    match league_id {
        1 => "NBA",
        2 => "BAA",
        3 => "ABA",
        _ => "Unknown",
    }
}

#[component]
pub fn SeasonsIndex() -> impl IntoView {
    let seasons = create_resource(|| (), |_| fetch_seasons());

    view! {
        <section class="page">
            <PageHeader
                title="Seasons Index".to_string()
                subtitle="Jump to standings, leaders, and team stats for any year.".to_string()
                callout=Some("Beginner tip: start with the most recent season to see leaders and team ratings.".to_string())
            />

            <Section id={"season-list".to_string()} title={"All Seasons".to_string()}>
                {move || match seasons.get() {
                    None => view! { <p>"Loading seasons..."</p> }.into_view(),
                    Some(Err(message)) => view! { <p class="error">{message}</p> }.into_view(),
                    Some(Ok(list)) => {
                        let columns = vec![
                            TableColumn::new("Season"),
                            TableColumn::new("League"),
                            TableColumn::new("Start"),
                            TableColumn::new("End"),
                        ];

                        let rows = list
                            .into_iter()
                            .map(|season| {
                                let link = format!("/seasons/{}", season.season_year);
                                vec![
                                    view! { <a href={link}>{season.season_year}</a> }.into_view(),
                                    view! { <span>{league_label(season.league_id)}</span> }.into_view(),
                                    view! { <span>{season.start_date.unwrap_or_else(|| "-".to_string())}</span> }
                                        .into_view(),
                                    view! { <span>{season.end_date.unwrap_or_else(|| "-".to_string())}</span> }
                                        .into_view(),
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
