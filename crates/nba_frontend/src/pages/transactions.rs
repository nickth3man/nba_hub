use leptos::*;
use leptos_router::use_params_map;
use serde_json::json;

use crate::components::{DataTable, PageHeader, SeasonSelect, Section, TableColumn};
use crate::convex::convex_query;
use crate::models::{SeasonRow, TransactionRow};

async fn fetch_seasons() -> Result<Vec<SeasonRow>, String> {
    convex_query("seasons:listSeasons", json!({})).await
}

async fn fetch_transactions(season_year: i32) -> Result<Vec<TransactionRow>, String> {
    convex_query(
        "transactions:listTransactionsBySeason",
        json!({ "seasonYear": season_year }),
    )
    .await
}

#[component]
pub fn TransactionsPage() -> impl IntoView {
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
    let transactions = create_resource(
        move || selected_year.get(),
        |year| async move {
            match year {
                Some(year) => fetch_transactions(year).await.map(Some),
                None => Ok(None),
            }
        },
    );

    view! {
        <section class="page">
            <PageHeader
                title="Transactions".to_string()
                subtitle="Trades, signings, and roster changes by season.".to_string()
                callout=Some("Beginner tip: use team abbreviations to spot your franchise quickly.".to_string())
            />

            <Section id={"transaction-season".to_string()} title={"Season".to_string()}>
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

            <Section id={"transaction-table".to_string()} title={"Transactions".to_string()}>
                {move || match transactions.get() {
                    None => view! { <p>"Loading transactions..."</p> }.into_view(),
                    Some(Err(message)) => view! { <p class="error">{message}</p> }.into_view(),
                    Some(Ok(None)) => view! { <p>"Select a season to view transactions."</p> }.into_view(),
                    Some(Ok(Some(list))) => {
                        let columns = vec![
                            TableColumn::new("Team"),
                            TableColumn::new("Player"),
                            TableColumn::new("Details"),
                        ];

                        let rows = list
                            .into_iter()
                            .map(|transaction| {
                                let player = transaction
                                    .player_bref_id
                                    .clone()
                                    .unwrap_or_else(|| "-".to_string());
                                let player_cell = if transaction.player_bref_id.is_some() {
                                    let link = format!("/players/{}", player);
                                    view! { <a href={link}>{player}</a> }.into_view()
                                } else {
                                    view! { <span>{player}</span> }.into_view()
                                };
                                vec![
                                    view! { <span>{transaction.team_abbrev.unwrap_or_else(|| "-".to_string())}</span> }.into_view(),
                                    player_cell,
                                    view! { <span>{transaction.details}</span> }.into_view(),
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
