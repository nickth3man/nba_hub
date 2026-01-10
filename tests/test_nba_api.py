from nba_api.stats.endpoints import playbyplayv3, shotchartdetail
from nba_api.stats.static import teams
import pandas as pd
import time

game_id = '0022200411' # 2022-12-13 HOU vs PHX

print(f"Testing nba_api for Game {game_id}...")

try:
    # 1. Play by Play (uses game_id)
    print("Fetching PlayByPlayV3...")
    pbp = playbyplayv3.PlayByPlayV3(game_id=game_id)
    df_pbp = pbp.play_by_play.get_data_frame()
    print(f"✅ PBP Success! Rows: {len(df_pbp)}")
    
    time.sleep(1)
    
    # 2. Shot Chart (uses game_id_nullable)
    print("\nFetching ShotChartDetail...")
    phx_id = [t for t in teams.get_teams() if t['abbreviation'] == 'PHX'][0]['id']
    
    shots = shotchartdetail.ShotChartDetail(
        team_id=phx_id,
        player_id=0,
        game_id_nullable=game_id, # Correct param
        context_measure_simple='FGA'
    )
    df_shots = shots.shot_chart_detail.get_data_frame()
    print(f"✅ Shot Chart Success! Rows: {len(df_shots)}")

except Exception as e:
    print(f"❌ Error: {e}")
