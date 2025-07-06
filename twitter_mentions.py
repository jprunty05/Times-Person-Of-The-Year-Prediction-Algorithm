import requests
import csv
import os

BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")


def create_headers():
    return {"Authorization": f"Bearer {BEARER_TOKEN}"}


def get_mention_count(query, start_time="2024-01-01T00:00:00Z", end_time="2024-12-31T00:00:00Z"):
    url = "https://api.twitter.com/2/tweets/counts/all"
    params = {
        "query": query,
        "start_time": start_time,
        "end_time": end_time,
        "granularity": "month",
    }
    headers = create_headers()
    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        print(f"Error for {query}: {response.text}")
        return []

    data = response.json()
    return [(query, item["start"], item["tweet_count"]) for item in data.get("data", [])]


def save_mentions(data, filename="twitter_mentions.csv"):
    with open(filename, "w", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Month", "Tweet Count"])
        writer.writerows(data)


if __name__ == "__main__":
    names = ["Taylor Swift", "Elon Musk", "Donald Trump"]  # example
    all_data = []

    for name in names:
        query = f'"{name}" lang:en'
        results = get_mention_count(query)
        all_data.extend(results)

    save_mentions(all_data)
    print("✅ Twitter mentions saved.")
