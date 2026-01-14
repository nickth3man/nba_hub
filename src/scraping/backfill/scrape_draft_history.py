import argparse
import time
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup, Tag
from typing import cast
from src.core.database import get_db_connection
from src.core.utils import retry_on_failure, get_random_user_agent


@retry_on_failure(retries=3, delay=5)
def fetch_page(page, url):
    page.goto(url, timeout=60000, wait_until="domcontentloaded")
    return page


def scrape_draft_history(start_year=2020, end_year=None):
    con = get_db_connection()

    con.execute("DROP TABLE IF EXISTS draft_history")

    con.execute("""
        CREATE TABLE draft_history (
            season_year INTEGER,
            pick_overall INTEGER,
            round_number INTEGER,
            pick_in_round INTEGER,
            team_id VARCHAR,
            player_id VARCHAR,
            player_name VARCHAR,
            college VARCHAR,
            years_active INTEGER,
            g INTEGER,
            mp_per_g DOUBLE,
            pts_per_g DOUBLE,
            trb_per_g DOUBLE,
            ast_per_g DOUBLE,
            ws DOUBLE,
            ws_48 DOUBLE,
            bpm DOUBLE,
            vorp DOUBLE,
            PRIMARY KEY (season_year, pick_overall)
        )
    """)

    # Get seasons from DB
    seasons = con.execute(
        "SELECT start_year FROM raw_dim_seasons WHERE league='NBA' ORDER BY start_year"
    ).fetchall()
    years = [s[0] for s in seasons]

    if start_year:
        years = [y for y in years if y >= start_year]
    if end_year:
        years = [y for y in years if y <= end_year]

    print(
        f"Scraping draft history for {len(years)} seasons (Start: {start_year}, End: {end_year})..."
    )

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent=get_random_user_agent())
        page = context.new_page()

        for year in years:
            bref_year = year + 1
            url = f"https://www.basketball-reference.com/draft/NBA_{bref_year}.html"
            print(f"Scraping {year} ({url})...")

            try:
                fetch_page(page, url)
                title = page.title()
                print(f"  Page title: {title}")

                if "403" in title or "Access Denied" in title:
                    print("  Access Denied (403)")
                    continue

                try:
                    page.wait_for_selector("#stats", timeout=5000)
                except:
                    print(f"  Table #stats not found (timeout)")

                content = page.content()
                soup = BeautifulSoup(content, "html.parser")

                table = soup.find("table", {"id": "stats"})
                if not table:
                    print(f"  #stats not found. Searching in comments...")
                    import re

                    comments = soup.find_all(
                        string=lambda text: "table" in text if text else False
                    )
                    for comment in comments:
                        if 'id="stats"' in comment:
                            comment_soup = BeautifulSoup(comment, "html.parser")
                            table = comment_soup.find("table", {"id": "stats"})
                            if table:
                                print("  Found #stats in comments.")
                                break

                if not table:
                    print(f"  No table found for {year}")
                    continue

                found_tbody = table.find("tbody")
                if not isinstance(found_tbody, Tag):
                    continue
                tbody = found_tbody

                rows_data = []
                all_rows = tbody.find_all("tr")

                current_round = 1
                pick_in_round = 0

                for tr in all_rows:
                    if "class" in tr.attrs and "thead" in tr.attrs["class"]:
                        continue

                    # Check if it's a valid row
                    pick_td = tr.find("td", {"data-stat": "pick_overall"})
                    if not pick_td:
                        continue

                    pick_overall = int(pick_td.get_text())

                    # Logic to determine round (simple approx: 1-30 is R1, 31-60 is R2 usually, but varies by year)
                    # Better: B-Ref doesn't explicitly state round in the table rows?
                    # Actually, we can infer it or just store overall pick.
                    # For now, let's just store overall pick.

                    team_td = tr.find("td", {"data-stat": "team_id"})
                    team_id = team_td.get_text() if team_td else None

                    player_td = tr.find("td", {"data-stat": "player"})
                    player_name = player_td.get_text().strip() if player_td else None
                    player_link = player_td.find("a") if player_td else None
                    player_id = (
                        player_link["href"].split("/")[-1].replace(".html", "")
                        if player_link
                        else None
                    )

                    college_td = tr.find("td", {"data-stat": "college"})
                    college = college_td.get_text().strip() if college_td else None

                    years_active_td = tr.find("td", {"data-stat": "years_active"})
                    years_active = (
                        int(years_active_td.get_text())
                        if years_active_td and years_active_td.get_text()
                        else 0
                    )

                    def get_val(stat, type_func=float):
                        td = tr.find("td", {"data-stat": stat})
                        if td and td.get_text():
                            try:
                                return type_func(td.get_text())
                            except:
                                return 0
                        return 0

                    g = get_val("g", int)
                    mp = get_val("mp_per_g")
                    pts = get_val("pts_per_g")
                    trb = get_val("trb_per_g")
                    ast = get_val("ast_per_g")
                    ws = get_val("ws")
                    ws_48 = get_val("ws_per_48")
                    bpm = get_val("bpm")
                    vorp = get_val("vorp")

                    # Dummy round logic
                    round_num = 1 if pick_overall <= 30 else 2
                    pick_in_round_val = (
                        pick_overall if round_num == 1 else pick_overall - 30
                    )

                    rows_data.append(
                        (
                            year,
                            pick_overall,
                            round_num,
                            pick_in_round_val,
                            team_id,
                            player_id,
                            player_name,
                            college,
                            years_active,
                            g,
                            mp,
                            pts,
                            trb,
                            ast,
                            ws,
                            ws_48,
                            bpm,
                            vorp,
                        )
                    )

                if rows_data:
                    con.executemany(
                        """
                        INSERT OR REPLACE INTO draft_history 
                        (season_year, pick_overall, round_number, pick_in_round, team_id, player_id, player_name, college,
                         years_active, g, mp_per_g, pts_per_g, trb_per_g, ast_per_g, ws, ws_48, bpm, vorp)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                        rows_data,
                    )
                    print(f"  Inserted {len(rows_data)} rows.")

                time.sleep(2)

            except Exception as e:
                print(f"  Error scraping {year}: {e}")

        browser.close()
    con.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape NBA draft history")
    parser.add_argument(
        "--start-year", type=int, default=2020, help="Start year (default: 2020)"
    )
    parser.add_argument("--end-year", type=int, help="End year (optional)")
    args = parser.parse_args()

    scrape_draft_history(start_year=args.start_year, end_year=args.end_year)
