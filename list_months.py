import os
from bs4 import BeautifulSoup

base_url = "https://www.basketball-reference.com"
html_dir = "data/raw/html"
files = [f for f in os.listdir(html_dir) if f.endswith("_games.html")]

urls = []
for f in files:
    path = os.path.join(html_dir, f)
    with open(path, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file.read(), "html.parser")
        filter_div = soup.find("div", class_="filter")
        if filter_div:
            for a in filter_div.find_all("a"):
                if "_games-" in a["href"]:
                    urls.append(base_url + a["href"])

with open("month_urls.txt", "w") as f:
    for url in urls:
        f.write(url + "\n")

print(f"Found {len(urls)} month URLs.")
