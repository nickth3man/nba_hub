use leptos::*;
use serde_json::json;

use crate::components::{DataTable, PageHeader, Section, TableColumn};
use crate::convex::convex_query;
use crate::models::PlayerDirectoryEntry;

async fn fetch_players() -> Result<Vec<PlayerDirectoryEntry>, String> {
    convex_query("players:listPlayerDirectory", json!({})).await
}

#[component]
pub fn Players() -> impl IntoView {
    let players = create_resource(|| (), |_| fetch_players());
    let (search, set_search) = create_signal(String::new());

    view! {
        <section class="page">
            <PageHeader
                title="Players Directory".to_string()
                subtitle="Browse players by Basketball-Reference ID with season ranges.".to_string()
                callout=Some("Beginner tip: click any player to view season totals and advanced metrics.".to_string())
            />

            <Section id={"player-search".to_string()} title={"Search".to_string()}>
                <div class="control-row">
                    <input
                        class="input"
                        type="text"
                        placeholder="Search by player name"
                        on:input=move |ev| set_search.set(event_target_value(&ev))
                    />
                </div>
            </Section>

            <Section id={"player-list".to_string()} title={"All Players".to_string()}>
                {move || match players.get() {
                    None => view! { <p>"Loading players..."</p> }.into_view(),
                    Some(Err(message)) => view! { <p class="error">{message}</p> }.into_view(),
                    Some(Ok(list)) => {
                        let filter = search.get().to_lowercase();
                        let mut filtered = list;
                        if !filter.is_empty() {
                            filtered.retain(|player| {
                                player.player_name.to_lowercase().contains(&filter)
                                    || player.player_bref_id.to_lowercase().contains(&filter)
                            });
                        }

                        if filtered.is_empty() {
                            return view! { <p>"No players match that search."</p> }.into_view();
                        }

                        let columns = vec![
                            TableColumn::new("Player"),
                            TableColumn::new("First").with_class("num"),
                            TableColumn::new("Last").with_class("num"),
                            TableColumn::new("Seasons").with_class("num"),
                            TableColumn::new("Teams").with_class("num"),
                        ];

                        let rows = filtered
                            .into_iter()
                            .map(|player| {
                                let link = format!("/players/{}", player.player_bref_id);
                                vec![
                                    view! { <a href={link}>{player.player_name}</a> }.into_view(),
                                    view! { <span>{player.first_season}</span> }.into_view(),
                                    view! { <span>{player.last_season}</span> }.into_view(),
                                    view! { <span>{player.seasons_count}</span> }.into_view(),
                                    view! { <span>{player.teams_count}</span> }.into_view(),
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
