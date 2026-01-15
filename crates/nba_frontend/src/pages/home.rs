use leptos::*;
use serde_json::json;

use crate::components::{DataTable, PageHeader, Section, TableColumn};
use crate::convex::convex_query;
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
pub fn Home() -> impl IntoView {
    let seasons = create_resource(|| (), |_| fetch_seasons());
    let selected_year = create_rw_signal::<Option<i32>>(None);

    create_effect(move |_| {
        if selected_year.get().is_none() {
            if let Some(Ok(list)) = seasons.get() {
                if let Some(first) = list.first() {
                    selected_year.set(Some(first.season_year));
                }
            }
        }
    });

    let leaders = create_resource(
        move || selected_year.get(),
        |year| async move {
            match year {
                Some(year) => fetch_leaders(year).await.map(Some),
                None => Ok(None),
            }
        },
    );

    let quick_links = vec![
        (
            "Players",
            "Find player careers and season totals.",
            "/players",
        ),
        (
            "Teams",
            "Browse franchise histories and season stats.",
            "/teams",
        ),
        (
            "Seasons",
            "Start with standings and ratings by year.",
            "/seasons",
        ),
        ("Leaders", "Top performers by season.", "/leaders"),
        ("Awards", "MVP, DPOY, and more by year.", "/awards"),
        ("Draft", "Draft pick history by season.", "/draft"),
        (
            "Transactions",
            "Season transactions overview.",
            "/transactions",
        ),
        (
            "Glossary",
            "Stat definitions and beginner help.",
            "/glossary",
        ),
    ];

    view! {
        <section class="page">
            <PageHeader
                title="NBA Hub".to_string()
                subtitle="A beginner-first clone of Basketball-Reference with fast navigation and stat explanations.".to_string()
                callout=Some("Start with Players, Teams, or Seasons. Toggle Beginner mode on any table to keep things approachable.".to_string())
            />

            <Section id={"quick-links".to_string()} title={"Quick Links".to_string()}>
                <div class="grid">
                    {quick_links
                        .into_iter()
                        .map(|(title, description, href)| {
                            view! {
                                <a class="card" href={href}>
                                    <strong>{title}</strong>
                                    <span>{description}</span>
                                </a>
                            }
                        })
                        .collect_view()}
                </div>
            </Section>

            <Section id={"latest-leaders".to_string()} title={"Latest Season Leaders".to_string()}>
                {move || match leaders.get() {
                    None => view! { <p>"Loading leaders..."</p> }.into_view(),
                    Some(Err(message)) => view! { <p class="error">{message}</p> }.into_view(),
                    Some(Ok(None)) => view! { <p>"Pick a season to see leaders."</p> }.into_view(),
                    Some(Ok(Some(data))) => {
                        let columns = vec![
                            TableColumn::new("Player"),
                            TableColumn::new("Teams"),
                            TableColumn::new("PTS").with_class("num"),
                            TableColumn::new("PTS/G").with_class("num"),
                            TableColumn::new("G").with_class("num"),
                        ];
                        let rows = leader_rows(&data.points);
                        view! { <DataTable columns=columns rows=rows /> }.into_view()
                    }
                }}
                <p class="footer-note">"Use the Leaders page for rebounds, assists, steals, and blocks."</p>
            </Section>
        </section>
    }
}
