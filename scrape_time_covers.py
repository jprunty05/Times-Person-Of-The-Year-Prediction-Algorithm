import requests
from bs4 import BeautifulSoup
import csv
import time


def scrape_time_covers(start_year=2000, end_year=2024):
    """Scrape TIME magazine cover subjects and dates from the vault."""
    base_url = "https://time.com/vault/year/"
    all_data = []

    for year in range(start_year, end_year + 1):
        url = f"{base_url}{year}"
        print(f"Scraping {url}")
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')

        issues = soup.find_all("div", class_="partial cover-item")

        for issue in issues:
            date = issue.find("span", class_="vault-cover-date").text.strip()
            cover_subject = issue.find("h3", class_="headline")
            subject = cover_subject.text.strip() if cover_subject else "Unknown"
            all_data.append([year, date, subject])

        time.sleep(1)  # be nice to their servers

    with open("time_covers_2000_2024.csv", "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Year", "Issue Date", "Cover Subject"])
        writer.writerows(all_data)

    print("✅ Finished scraping TIME covers.")


if __name__ == "__main__":
    scrape_time_covers()
