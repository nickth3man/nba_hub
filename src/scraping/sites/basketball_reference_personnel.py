import random
import time

import requests
from bs4 import BeautifulSoup

from src.core.database import get_db_connection


def scrape_coaches():
    url = "https://www.basketball-reference.com/coaches/NBA_stats.html"
    print(f"Scraping coaches from {url}...")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except Exception as e:
        print(f"Error fetching coaches: {e}")
        return

    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("table", {"id": "coaches"})
    if not table:
        print("Could not find coaches table.")
        return

    tbody = table.find("tbody")
    rows = []
    for tr in tbody.find_all("tr"):
        if "class" in tr.attrs and "thead" in tr.attrs["class"]:
            continue

        coach_td = tr.find("td", {"data-stat": "coach"})
        if not coach_td:
            continue

        coach_name = coach_td.get_text().strip()
        coach_link = coach_td.find("a")["href"]
        # /coaches/adelmri01c.html -> adelmri01c
        coach_id = coach_link.split("/")[-1].replace(".html", "")

        # Split name
        name_parts = coach_name.split()
        first_name = name_parts[0] if name_parts else ""
        last_name = " ".join(name_parts[1:]) if len(name_parts) > 1 else ""

        rows.append((coach_id, first_name, last_name, coach_name))

    con = get_db_connection()
    # Ensure table exists (using old schema for now, will migrate later)
    con.execute(
        "CREATE TABLE IF NOT EXISTS coaches (coach_id VARCHAR PRIMARY KEY, name VARCHAR)"
    )

    print(f"Inserting {len(rows)} coaches...")
    con.executemany(
        "INSERT OR IGNORE INTO coaches (coach_id, name) VALUES (?, ?)",
        [(r[0], r[3]) for r in rows],
    )
    con.close()
    print("Coaches ingestion complete.")


def scrape_referees():
    url = "https://www.basketball-reference.com/referees/"
    print(f"Scraping referees from {url}...")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except Exception as e:
        print(f"Error fetching referees: {e}")
        return

    soup = BeautifulSoup(response.content, "html.parser")
    # Referees are in a table with id "referees"
    table = soup.find("table", {"id": "referees"})
    if not table:
        print("Could not find referees table.")
        return

    tbody = table.find("tbody")
    rows = []
    for tr in tbody.find_all("tr"):
        if "class" in tr.attrs and "thead" in tr.attrs["class"]:
            continue

        ref_td = tr.find("td", {"data-stat": "referee"})
        if not ref_td:
            continue

        ref_name = ref_td.get_text().strip()
        ref_link = ref_td.find("a")["href"]
        # /referees/abaziag99r.html -> abaziag99r
        ref_id = ref_link.split("/")[-1].replace(".html", "")

        rows.append((ref_id, ref_name))

    con = get_db_connection()
    # Ensure table exists
    con.execute(
        "CREATE TABLE IF NOT EXISTS referees (referee_id VARCHAR PRIMARY KEY, name VARCHAR)"
    )

    print(f"Inserting {len(rows)} referees...")
    con.executemany(
        "INSERT OR IGNORE INTO referees (referee_id, name) VALUES (?, ?)", rows
    )
    con.close()
    print("Referees ingestion complete.")


if __name__ == "__main__":
    scrape_coaches()
    time.sleep(random.uniform(3, 5))
    scrape_referees()
