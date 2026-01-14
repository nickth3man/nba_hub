import gradio as gr
import pandas as pd
from src.frontend.queries import (
    get_seasons,
    get_teams,
    get_player_search,
    get_player_profile,
    get_standings,
)


def home_page():
    with gr.Blocks() as home:
        gr.Markdown("# NBA Data Hub")
        gr.Markdown("Welcome to the 1:1 Replica of Basketball-Reference Data.")

        with gr.Row():
            with gr.Column():
                gr.Markdown("### 2024-25 Standings")
                standings = get_standings(2025)
                gr.Dataframe(standings, label="Standings")
    return home


def player_page():
    with gr.Blocks() as player:
        gr.Markdown("## Player Search")
        name_input = gr.Textbox(
            label="Player Name", placeholder="Enter name (e.g. LeBron)"
        )
        search_btn = gr.Button("Search")
        results = gr.Dataframe(label="Search Results", interactive=False)

        player_id_input = gr.Number(label="Player ID (from results)", visible=True)
        profile_btn = gr.Button("View Profile")

        profile_info = gr.Dataframe(label="Bio")
        season_stats = gr.Dataframe(label="Season Stats")

        search_btn.click(get_player_search, inputs=name_input, outputs=results)

        def load_profile(pid):
            info, stats = get_player_profile(pid)
            return info, stats

        profile_btn.click(
            load_profile, inputs=player_id_input, outputs=[profile_info, season_stats]
        )
    return player


def team_page():
    with gr.Blocks() as team:
        gr.Markdown("## Teams")
        teams_df = get_teams()
        gr.Dataframe(teams_df, label="All Franchises")
    return team


def draft_page():
    with gr.Blocks() as draft:
        gr.Markdown("## Draft History")
        # Placeholder
        gr.Markdown("Coming soon...")
    return draft


with gr.Blocks(title="NBA Hub") as app:
    with gr.Tabs():
        with gr.Tab("Home"):
            home_page()
        with gr.Tab("Players"):
            player_page()
        with gr.Tab("Teams"):
            team_page()
        with gr.Tab("Draft"):
            draft_page()

if __name__ == "__main__":
    app.launch()
