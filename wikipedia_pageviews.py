import requests
import csv


def get_pageviews(title, start="20240101", end="20241231"):
    """Fetch monthly Wikipedia pageviews for a title."""
    url = (
        "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/"
        f"en.wikipedia/all-access/all-agents/{title}/monthly/{start}/{end}"
    )
    r = requests.get(url)
    if r.status_code != 200:
        return []

    data = r.json().get("items", [])
    return [(title, item["timestamp"], item["views"]) for item in data]


def load_titles_from_csv(filename):
    with open(filename, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        return [row[0] for row in list(reader)[1:]]


def save_to_csv(data, filename="wikipedia_views.csv"):
    with open(filename, "w", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Title", "Date", "Views"])
        writer.writerows(data)


if __name__ == "__main__":
    titles = load_titles_from_csv("shortlist_2024.csv")  # file with column 'Name'
    all_views = []

    for name in titles:
        title = name.replace(" ", "_")
        print(f"Fetching views for: {title}")
        views = get_pageviews(title)
        all_views.extend(views)

    save_to_csv(all_views)
    print("✅ Wikipedia views saved.")
