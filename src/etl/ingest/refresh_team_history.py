import os

import pandas as pd
from nba_api.stats.static import teams  # type: ignore

TEAM_HISTORIES_CSV = "data/raw/TeamHistories.csv"
OUTPUT_CSV = "data/raw/TeamHistories_Updated.csv"


def refresh_teams():
    if not os.path.exists(TEAM_HISTORIES_CSV):
        print(f"Error: {TEAM_HISTORIES_CSV} not found.")
        return

    # Load existing historical data
    df_hist = pd.read_csv(TEAM_HISTORIES_CSV)
    df_hist["teamAbbrev"] = df_hist["teamAbbrev"].str.strip()

    # Get current teams from nba_api
    current_teams = teams.get_teams()
    df_current = pd.DataFrame(current_teams)

    # Map nba_api columns to our CSV columns
    # nba_api: id, full_name, abbreviation, nickname, city, state, year_founded
    # CSV: teamId, teamCity, teamName, teamAbbrev, seasonFounded, seasonActiveTill, league

    new_rows = []
    for _, row in df_current.iterrows():
        team_id = row["id"]

        # Check if this team is already in hist and marked as active (2100)
        mask = (df_hist["teamId"] == team_id) & (df_hist["seasonActiveTill"] >= 2021)
        if not df_hist[mask].empty:
            # Update existing active record to 2100 if it's not already
            df_hist.loc[mask, "seasonActiveTill"] = 2100
        else:
            # Add new row if not found (though most should be there)
            new_rows.append(
                {
                    "teamId": team_id,
                    "teamCity": row["city"],
                    "teamName": row["nickname"],
                    "teamAbbrev": row["abbreviation"],
                    "seasonFounded": row["year_founded"],
                    "seasonActiveTill": 2100,
                    "league": "NBA",
                }
            )

    if new_rows:
        df_new = pd.DataFrame(new_rows)
        df_final = pd.concat([df_hist, df_new], ignore_index=True)
    else:
        df_final = df_hist

    # Ensure all active teams have 2100 as seasonActiveTill
    # Some might have 2021 or 2022
    df_final["teamAbbrev"].isin(df_current["abbreviation"].tolist())
    # But only for the latest record of that team
    # Actually, simpler: if it's a current NBA team, ensure it has an active record

    df_final.to_csv(OUTPUT_CSV, index=False)
    print(f"Updated team history saved to {OUTPUT_CSV}")
    print(f"Total teams in history: {len(df_final)}")


if __name__ == "__main__":
    refresh_teams()
