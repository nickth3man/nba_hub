use leptos::*;
use leptos_meta::*;
use leptos_router::*;

mod components;
mod convex;
mod data;
mod models;
mod pages;
mod styles;
mod utils;

use components::AppLayout;
use pages::{
    AwardsPage, DraftPage, GlossaryPage, Home, LeadersPage, PlayerProfile, Players, SeasonDetail,
    SeasonsIndex, TeamProfile, Teams, TransactionsPage,
};
use styles::APP_STYLES;

#[component]
pub fn App() -> impl IntoView {
    provide_meta_context();

    view! {
        <Stylesheet id="leptos" href="/pkg/nba_frontend.css"/>
        <Title text="NBA Hub"/>
        <style>{APP_STYLES}</style>
        <Router>
            <AppLayout>
                <Routes>
                    <Route path="/" view=Home/>
                    <Route path="/players" view=Players/>
                    <Route path="/players/:player_bref_id" view=PlayerProfile/>
                    <Route path="/teams" view=Teams/>
                    <Route path="/teams/:team_abbrev" view=TeamProfile/>
                    <Route path="/seasons" view=SeasonsIndex/>
                    <Route path="/seasons/:year" view=SeasonDetail/>
                    <Route path="/leaders" view=LeadersPage/>
                    <Route path="/leaders/:year" view=LeadersPage/>
                    <Route path="/awards" view=AwardsPage/>
                    <Route path="/awards/:year" view=AwardsPage/>
                    <Route path="/draft" view=DraftPage/>
                    <Route path="/draft/:year" view=DraftPage/>
                    <Route path="/transactions" view=TransactionsPage/>
                    <Route path="/transactions/:year" view=TransactionsPage/>
                    <Route path="/glossary" view=GlossaryPage/>
                </Routes>
            </AppLayout>
        </Router>
    }
}
