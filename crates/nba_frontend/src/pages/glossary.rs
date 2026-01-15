use leptos::*;

use crate::components::{DataTable, PageHeader, Section, TableColumn};
use crate::data::STAT_GLOSSARY;

#[component]
pub fn GlossaryPage() -> impl IntoView {
    view! {
        <section class="page">
            <PageHeader
                title="Stat Glossary".to_string()
                subtitle="Plain-language explanations for common basketball stats.".to_string()
                callout=Some("Beginner tip: hover over table headers across the site to see these definitions.".to_string())
            />

            <Section id={"glossary".to_string()} title={"Definitions".to_string()}>
                <DataTable
                    columns=vec![
                        TableColumn::new("Abbr"),
                        TableColumn::new("Label"),
                        TableColumn::new("Description"),
                    ]
                    rows=STAT_GLOSSARY
                        .iter()
                        .map(|stat| {
                            vec![
                                view! { <span>{stat.abbr}</span> }.into_view(),
                                view! { <span>{stat.label}</span> }.into_view(),
                                view! { <span>{stat.description}</span> }.into_view(),
                            ]
                        })
                        .collect()
                />
            </Section>
        </section>
    }
}
