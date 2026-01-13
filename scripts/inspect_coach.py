import requests
from bs4 import BeautifulSoup


def inspect_coach(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch {url}: {response.status_code}")
        return

    soup = BeautifulSoup(response.content, "html.parser")

    # Print all text containing "Coach"
    print("--- Text containing 'Coach' ---")
    for string in soup.stripped_strings:
        if "Coach" in string:
            print(string)

    # Print all links containing "coaches"
    print("\n--- Links containing '/coaches/' ---")
    for link in soup.find_all("a", href=True):
        if "/coaches/" in link["href"]:
            print(f"Text: {link.text}, Href: {link['href']}")

    # Check comments
    print("\n--- Comments containing 'Coach' ---")
    from bs4 import Comment

    comments = soup.find_all(string=lambda text: isinstance(text, Comment))
    for c in comments:
        if "Coach" in c:
            print(f"Comment found (snippet): {c[:100]}...")
            # Parse comment as soup
            comment_soup = BeautifulSoup(c, "html.parser")
            for link in comment_soup.find_all("a", href=True):
                if "/coaches/" in link["href"]:
                    print(f"  Link in comment: {link.text}, Href: {link['href']}")


if __name__ == "__main__":
    inspect_coach("https://www.basketball-reference.com/boxscores/202310240DEN.html")
