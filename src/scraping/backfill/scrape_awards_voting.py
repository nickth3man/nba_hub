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


def scrape_awards_voting():
    con = get_db_connection()

    # Create table for voting results
    con.execute("""
        CREATE TABLE IF NOT EXISTS awards_voting (
            season_year INTEGER,
            award_category VARCHAR,
            rank INTEGER,
            player_id VARCHAR,
            player_name VARCHAR,
            age INTEGER,
            team_id VARCHAR,
            first_place_votes INTEGER,
            points_won INTEGER,
            points_max INTEGER,
            share DOUBLE,
            g INTEGER,
            mp_per_g DOUBLE,
            pts_per_g DOUBLE,
            trb_per_g DOUBLE,
            ast_per_g DOUBLE,
            stl_per_g DOUBLE,
            blk_per_g DOUBLE,
            fg_pct DOUBLE,
            three_pct DOUBLE,
            ft_pct DOUBLE,
            ws DOUBLE,
            ws_48 DOUBLE,
            PRIMARY KEY (season_year, award_category, player_id)
        )
    """)

    # Get seasons from DB
    seasons = con.execute(
        "SELECT start_year FROM raw_dim_seasons WHERE league='NBA' ORDER BY start_year"
    ).fetchall()
    years = [s[0] for s in seasons]

    # Filter years (start from 1955 for MVP, others later)
    years = [y for y in years if y >= 2020]  # Test with recent years first

    print(f"Scraping awards voting for {len(years)} seasons...")

    awards_map = {
        "mvp": "MVP",
        "roy": "ROY",
        "dpoy": "DPOY",
        "smoy": "SMOY",
        "mip": "MIP",
    }

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent=get_random_user_agent())
        page = context.new_page()

        for year in years:
            bref_year = year + 1
            url = f"https://www.basketball-reference.com/awards/awards_{bref_year}.html"
            print(f"Scraping {year} ({url})...")

            try:
                fetch_page(page, url)
                title = page.title()
                print(f"  Page title: {title}")

                if "403" in title or "Access Denied" in title:
                    print("  Access Denied (403)")
                    continue

                # Wait for at least one table
                try:
                    page.wait_for_selector("table", timeout=5000)
                except:
                    print(f"  No tables found (timeout)")

                content = page.content()
                soup = BeautifulSoup(content, "html.parser")

                for table_id, award_code in awards_map.items():
                    table = soup.find("table", {"id": table_id})

                    # Check comments if not found
                    if not table:
                        comments = soup.find_all(
                            string=lambda text: "table" in text if text else False
                        )
                        for comment in comments:
                            if f'id="{table_id}"' in comment:
                                comment_soup = BeautifulSoup(comment, "html.parser")
                                table = comment_soup.find("table", {"id": table_id})
                                if table:
                                    break

                    if not table:
                        # print(f"  Table {table_id} not found for {year}")
                        continue

                    found_tbody = table.find("tbody")
                    if not isinstance(found_tbody, Tag):
                        continue
                    tbody = found_tbody

                    rows_data = []
                    all_rows = tbody.find_all("tr")

                    for tr in all_rows:
                        if "class" in tr.attrs and "thead" in tr.attrs["class"]:
                            continue

                        # Rank
                        rank_td = tr.find(["th", "td"], {"data-stat": "rank"})
                        rank = (
                            int(rank_td.get_text().replace("T", ""))
                            if rank_td and rank_td.get_text()
                            else None
                        )

                        # Player
                        player_td = tr.find("td", {"data-stat": "player"})
                        if not player_td:
                            continue
                        player_name = player_td.get_text().strip()
                        player_link = player_td.find("a")
                        player_id = (
                            player_link["href"].split("/")[-1].replace(".html", "")
                            if player_link
                            else None
                        )

                        if not player_id:
                            continue

                        # Stats
                        def get_val(stat, type_func=float):
                            td = tr.find("td", {"data-stat": stat})
                            if td and td.get_text():
                                try:
                                    return type_func(td.get_text())
                                except:
                                    return 0
                            return 0

                        age = get_val("age", int)
                        team_id = (
                            tr.find("td", {"data-stat": "team_id"}).get_text()
                            if tr.find("td", {"data-stat": "team_id"})
                            else None
                        )
                        first_place = get_val("votes_first", int)
                        points_won = get_val("points_won", int)
                        points_max = get_val("points_max", int)
                        share = get_val("award_share")
                        g = get_val("g", int)
                        mp = get_val("mp_per_g")
                        pts = get_val("pts_per_g")
                        trb = get_val("trb_per_g")
                        ast = get_val("ast_per_g")
                        stl = get_val("stl_per_g")
                        blk = get_val("blk_per_g")
                        fg = get_val("fg_pct")
                        three = get_val("fg3_pct")
                        ft = get_val("ft_pct")
                        ws = get_val("ws")
                        ws_48 = get_val("ws_per_48")

                        rows_data.append(
                            (
                                year,
                                award_code,
                                rank,
                                player_id,
                                player_name,
                                age,
                                team_id,
                                first_place,
                                points_won,
                                points_max,
                                share,
                                g,
                                mp,
                                pts,
                                trb,
                                ast,
                                stl,
                                blk,
                                fg,
                                three,
                                ft,
                                ws,
                                ws_48,
                            )
                        )

                    if rows_data:
                        con.executemany(
                            """
                            INSERT OR REPLACE INTO awards_voting 
                            (season_year, award_category, rank, player_id, player_name, age, team_id, 
                             first_place_votes, points_won, points_max, share, g, mp_per_g, pts_per_g, 
                             trb_per_g, ast_per_g, stl_per_g, blk_per_g, fg_pct, three_pct, ft_pct, ws, ws_48)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                            rows_data,
                        )
                        print(f"  Inserted {len(rows_data)} rows for {award_code}")

                time.sleep(2)

            except Exception as e:
                print(f"  Error scraping {year}: {e}")

        browser.close()
    con.close()


if __name__ == "__main__":
    scrape_awards_voting()
