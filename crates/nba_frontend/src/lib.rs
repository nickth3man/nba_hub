use leptos::*;
use leptos_router::*;
use leptos_meta::*;

mod pages;
use pages::players::Players;
use pages::teams::Teams;

#[component]
pub fn App() -> impl IntoView {
    provide_meta_context();

    view! {
        <Stylesheet id="leptos" href="/pkg/nba_frontend.css"/>
        <Title text="NBA Hub"/>
        <Router>
            <main>
                <nav>
                    <a href="/">"Home"</a>
                    <a href="/players">"Players"</a>
                    <a href="/teams">"Teams"</a>
                </nav>
                <Routes>
                    <Route path="/" view=|| view! { <h1>"Welcome to NBA Hub"</h1> }/>
                    <Route path="/players" view=Players/>
                    <Route path="/teams" view=Teams/>
                </Routes>
            </main>
        </Router>
    }
}
