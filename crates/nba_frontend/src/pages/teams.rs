use leptos::*;
use serde_json::json;

use crate::components::{DataTable, PageHeader, Section, TableColumn};
use crate::convex::convex_query;
use crate::models::TeamHistoryRow;
use crate::utils::format_team_label;

async fn fetch_teams() -> Result<Vec<TeamHistoryRow>, String> {
    convex_query("teams:listTeams", json!({ "activeOnly": true })).await
}

#[component]
pub fn Teams() -> impl IntoView {
    let teams = create_resource(|| (), |_| fetch_teams());
    let (search, set_search) = create_signal(String::new());

    view! {
        <section class="page">
            <PageHeader
                title="Teams Directory".to_string()
                subtitle="Active franchises with quick links to season histories.".to_string()
                callout=Some("Beginner tip: click a team to view season ratings, totals, and standings.".to_string())
            />

            <Section id={"team-search".to_string()} title={"Search".to_string()}>
                <div class="control-row">
                    <input
                        class="input"
                        type="text"
                        placeholder="Search teams by city or nickname"
                        on:input=move |ev| set_search.set(event_target_value(&ev))
                    />
                </div>
            </Section>

            <Section id={"team-list".to_string()} title={"All Teams".to_string()}>
                {move || match teams.get() {
                    None => view! { <p>"Loading teams..."</p> }.into_view(),
                    Some(Err(message)) => view! { <p class="error">{message}</p> }.into_view(),
                    Some(Ok(list)) => {
                        let filter = search.get().to_lowercase();
                        let mut filtered = list;
                        if !filter.is_empty() {
                            filtered.retain(|team| {
                                let label = format_team_label(&team.city, &team.nickname).to_lowercase();
                                label.contains(&filter)
                                    || team
                                        .abbreviation
                                        .as_ref()
                                        .map(|abbr| abbr.to_lowercase().contains(&filter))
                                        .unwrap_or(false)
                            });
                        }

                        if filtered.is_empty() {
                            return view! { <p>"No teams match that search."</p> }.into_view();
                        }

                        let columns = vec![
                            TableColumn::new("Team"),
                            TableColumn::new("Abbrev"),
                            TableColumn::new("Status"),
                            TableColumn::new("Start"),
                            TableColumn::new("End"),
                        ];

                        let rows = filtered
                            .into_iter()
                            .map(|team| {
                                let label = format_team_label(&team.city, &team.nickname);
                                let abbrev = team.abbreviation.clone().unwrap_or_else(|| "-".to_string());
                                let link = format!("/teams/{}", abbrev);
                                let status = if team.is_active { "Active" } else { "Inactive" };
                                vec![
                                    if abbrev == "-" {
                                        view! { <span>{label}</span> }.into_view()
                                    } else {
                                        view! { <a href={link}>{label}</a> }.into_view()
                                    },
                                    view! { <span>{abbrev}</span> }.into_view(),
                                    view! { <span>{status}</span> }.into_view(),
                                    view! { <span>{team.effective_start}</span> }.into_view(),
                                    view! { <span>{team.effective_end.clone().unwrap_or_else(|| "-".to_string())}</span> }.into_view(),
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
