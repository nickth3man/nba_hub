import requests
from bs4 import BeautifulSoup
import duckdb
import time
import random
import re

DB_PATH = "data/nba.duckdb"

# Map award IDs in HTML to our DB award_type
AWARD_MAPPING = {
    "mvp": "MVP",
    "roy": "ROY",
    "dpoy": "DPOY",
    "smoy": "SMOY",
    "mip": "MIP",
}


def get_player_id(td):
    """Extract player ID from the player cell."""
    # <td ... data-append-csv="jokicni01" ...>...</td>
    if td.has_attr("data-append-csv"):
        return td["data-append-csv"]
    # Fallback: try to parse from link
    a = td.find("a")
    if a and "href" in a.attrs:
        # /players/j/jokicni01.html
        match = re.search(r"/players/[a-z]/(\w+)\.html", a["href"])
        if match:
            return match.group(1)
    return None


def scrape_year(year):
    url = f"https://www.basketball-reference.com/awards/awards_{year}.html"
    print(f"Scraping {url}...")

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 404:
            print(f"Page not found for {year}. Skipping.")
            return
        response.raise_for_status()
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return

    soup = BeautifulSoup(response.content, "html.parser")

    con = duckdb.connect(DB_PATH)

    for html_id, award_type in AWARD_MAPPING.items():
        table = soup.find("table", {"id": html_id})
        if not table:
            continue

        print(f"Found table for {award_type} in {year}")

        tbody = table.find("tbody")
        if not tbody:
            continue

        rows_to_insert = []

        for tr in tbody.find_all("tr"):
            if "class" in tr.attrs and "thead" in tr.attrs["class"]:
                continue

            # Rank
            rank_th = tr.find("th", {"data-stat": "rank"})
            rank_text = rank_th.get_text().strip() if rank_th else None
            if not rank_text:
                continue

            try:
                rank = int(rank_text.replace("T", ""))  # Handle ties like "5T"
            except:
                rank = None

            # Player
            player_td = tr.find("td", {"data-stat": "player"})
            if not player_td:
                continue

            player_id = get_player_id(player_td)
            name = player_td.get_text().strip()

            # Votes
            first_place_td = tr.find("td", {"data-stat": "votes_first"})
            first_place = (
                int(float(first_place_td.get_text().strip() or 0))
                if first_place_td
                else 0
            )

            points_won_td = tr.find("td", {"data-stat": "points_won"})
            points_won = (
                int(float(points_won_td.get_text().strip() or 0))
                if points_won_td
                else 0
            )

            points_max_td = tr.find("td", {"data-stat": "points_max"})
            points_max = (
                int(float(points_max_td.get_text().strip() or 0))
                if points_max_td
                else 0
            )

            share_td = tr.find("td", {"data-stat": "award_share"})
            share = float(share_td.get_text().strip() or 0.0) if share_td else 0.0

            rows_to_insert.append(
                (
                    award_type,
                    year,
                    player_id,
                    name,
                    rank,
                    first_place,
                    points_won,
                    points_max,
                    share,
                )
            )

        # Insert into DB
        if rows_to_insert:
            print(f"Inserting {len(rows_to_insert)} rows for {award_type} {year}")
            try:
                con.executemany(
                    """
                    INSERT INTO awards_voting (award_type, season, player_id, name, rank, first_place_votes, points_won, points_max, share)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT (award_type, season, player_id) DO UPDATE SET
                        name = excluded.name,
                        rank = excluded.rank,
                        first_place_votes = excluded.first_place_votes,
                        points_won = excluded.points_won,
                        points_max = excluded.points_max,
                        share = excluded.share
                """,
                    rows_to_insert,
                )
            except Exception as e:
                print(f"Error inserting data for {award_type} {year}: {e}")

    con.close()


def verify_data():
    print("\nVerifying data in DuckDB...")
    con = duckdb.connect(DB_PATH)

    # Count rows
    try:
        count = con.execute("SELECT COUNT(*) FROM awards_voting").fetchone()[0]
        print(f"Total rows in awards_voting: {count}")

        # Sample MVP voting for 2023
        print("\nSample MVP voting for 2023:")
        sample = con.execute("""
            SELECT name, first_place_votes, points_won, points_max, share 
            FROM awards_voting 
            WHERE award_type = 'MVP' AND season = 2023 
            ORDER BY points_won DESC 
            LIMIT 5
        """).fetchall()

        for row in sample:
            print(row)
    except Exception as e:
        print(f"Error verifying data: {e}")
    finally:
        con.close()


def main():
    # Scrape recent years for testing as per instructions
    # To cover more history, change this to range(1980, 2025)
    years = range(2020, 2025)

    for year in years:
        scrape_year(year)
        time.sleep(random.uniform(3, 5))

    verify_data()


if __name__ == "__main__":
    main()
