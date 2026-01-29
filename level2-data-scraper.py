import requests
#this have already installed in cmd
from bs4 import BeautifulSoup
import csv

URL = "https://news.ycombinator.com/"
OUTPUT_FILE = "articles.csv"

def fetch_page(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print("Error fetching webpage:", e)
        return None

def parse_articles(html):
    soup = BeautifulSoup(html, "html.parser")
    #this have already installed in cmd
    links = soup.select(".titleline a")
    articles = []

    for link in links:
        title = link.get_text(strip=True)
        href = link.get("href")
        articles.append({
            "title": title,
            "link": href
        })

    return articles

def save_to_csv(articles):
    with open(OUTPUT_FILE, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["title", "link"])
        writer.writeheader()
        for article in articles:
            writer.writerow(article)

    print("Data saved to articles.csv")

def main():
    print("=== DATA SCRAPER ===")
    html = fetch_page(URL)

    if not html:
        print("Failed to retrieve data.")
        return

    articles = parse_articles(html)

    if not articles:
        print("No articles found.")
        return

    save_to_csv(articles)

if __name__ == "__main__":
    main()
