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


def scrape_coaches_history(start_year=2020, end_year=None):
    con = get_db_connection()

    con.execute("""
        CREATE TABLE IF NOT EXISTS coach_season_summary (
            season_year INTEGER,
            team_id VARCHAR,
            coach_id VARCHAR,
            coach_name VARCHAR,
            games INTEGER,
            wins INTEGER,
            losses INTEGER,
            PRIMARY KEY (season_year, team_id, coach_id)
        )
    """)

    seasons = con.execute(
        "SELECT start_year FROM raw_dim_seasons WHERE league='NBA' ORDER BY start_year"
    ).fetchall()
    years = [s[0] for s in seasons]

    if start_year:
        years = [y for y in years if y >= start_year]
    if end_year:
        years = [y for y in years if y <= end_year]

    print(
        f"Scraping coaches history for {len(years)} seasons (Start: {start_year}, End: {end_year})..."
    )

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent=get_random_user_agent())
        page = context.new_page()

        for year in years:
            bref_year = year + 1
            url = f"https://www.basketball-reference.com/leagues/NBA_{bref_year}_coaches.html"
            print(f"Scraping {year} ({url})...")

            try:
                fetch_page(page, url)
                title = page.title()
                print(f"  Page title: {title}")

                if "403" in title or "Access Denied" in title:
                    print("  Access Denied (403)")
                    continue

                try:
                    page.wait_for_selector("#NBA_coaches", timeout=5000)
                except:
                    print(f"  Table #NBA_coaches not found (timeout)")

                content = page.content()
                soup = BeautifulSoup(content, "html.parser")

                table = soup.find("table", {"id": "NBA_coaches"})
                if not table:
                    print(f"  #NBA_coaches not found. Searching in comments...")
                    import re

                    comments = soup.find_all(
                        string=lambda text: "table" in text if text else False
                    )
                    for comment in comments:
                        if 'id="NBA_coaches"' in comment:
                            comment_soup = BeautifulSoup(comment, "html.parser")
                            table = comment_soup.find("table", {"id": "NBA_coaches"})
                            if table:
                                print("  Found #NBA_coaches in comments.")
                                break

                if not table:
                    print(f"  No table found for {year}")
                    continue

                found_tbody = table.find("tbody")
                if not isinstance(found_tbody, Tag):
                    print("  No valid tbody found")
                    continue
                tbody = found_tbody

                rows_data = []
                all_rows = tbody.find_all("tr")

                for i, tr in enumerate(all_rows):
                    if "class" in tr.attrs and "thead" in tr.attrs["class"]:
                        continue

                    coach_td = tr.find(["th", "td"], {"data-stat": "coach"})
                    if not coach_td:
                        if i < 3:
                            print(f"  Row {i} skipped. HTML: {str(tr)[:100]}...")
                        continue
                    coach_name = coach_td.get_text().strip()
                    coach_link = coach_td.find("a")
                    coach_id = (
                        coach_link["href"].split("/")[-1].replace(".html", "")
                        if coach_link
                        else None
                    )

                    team_td = tr.find("td", {"data-stat": "team"})
                    if not team_td:
                        if i < 3:
                            print(f"  Row {i} skipped (no team). HTML: {str(tr)[:100]}")
                        continue
                    team_abbr = team_td.get_text().strip()

                    # Stats
                    g = tr.find("td", {"data-stat": "cur_g"})
                    w = tr.find("td", {"data-stat": "cur_w"})
                    l = tr.find("td", {"data-stat": "cur_l"})

                    games = int(g.get_text()) if g and g.get_text() else 0
                    wins = int(w.get_text()) if w and w.get_text() else 0
                    losses = int(l.get_text()) if l and l.get_text() else 0

                    rows_data.append(
                        (year, team_abbr, coach_id, coach_name, games, wins, losses)
                    )

                if rows_data:
                    con.executemany(
                        """
                        INSERT OR REPLACE INTO coach_season_summary 
                        (season_year, team_id, coach_id, coach_name, games, wins, losses)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
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
    parser = argparse.ArgumentParser(description="Scrape NBA coaches history")
    parser.add_argument(
        "--start-year", type=int, default=2020, help="Start year (default: 2020)"
    )
    parser.add_argument("--end-year", type=int, help="End year (optional)")
    args = parser.parse_args()

    scrape_coaches_history(start_year=args.start_year, end_year=args.end_year)
