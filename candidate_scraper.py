import csv
import datetime
import urllib.parse

import feedparser
import requests
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from pytrends.request import TrendReq

# List of candidates and their corresponding Wikipedia page titles
CANDIDATES = [
    ("Hollywood strikers", "2023_Hollywood_labor_disputes"),
    ("Xi Jinping", "Xi_Jinping"),
    ("Barbie", "Barbie_(film)"),
    ("Taylor Swift", "Taylor_Swift"),
    ("Sam Altman", "Sam_Altman"),
    ("Vladimir Putin", "Vladimir_Putin"),
    ("King Charles III", "Charles_III"),
    ("Trump prosecutors", "Indictments_of_Donald_Trump"),
    ("Jerome Powell", "Jerome_Powell"),
]

UA = {"User-Agent": "Mozilla/5.0"}

# initialize sentiment analyzer
sent_analyzer = SentimentIntensityAnalyzer()

# initialize pytrends
pytrends = TrendReq(hl="en-US", tz=360)

end_date = datetime.date.today() - datetime.timedelta(days=1)
start_date = end_date - datetime.timedelta(days=30)

rows = []
for name, wiki in CANDIDATES:
    row = {"name": name}
    # Google News RSS
    query = urllib.parse.quote_plus(name)
    feed = feedparser.parse(
        f"https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en"
    )
    news_count = len(feed.entries)
    if news_count:
        sentiment = sum(
            sent_analyzer.polarity_scores(e.title)["compound"] for e in feed.entries
        ) / news_count
    else:
        sentiment = 0
    row.update({"news_count": news_count, "news_sentiment": sentiment})

    # Wikipedia pageviews
    url = (
        "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/"
        f"en.wikipedia/all-access/all-agents/{wiki}/daily/"
        f"{start_date.strftime('%Y%m%d')}/{end_date.strftime('%Y%m%d')}"
    )
    r = requests.get(url, headers=UA)
    if r.status_code == 200:
        data = r.json().get("items", [])
        total_views = sum(item["views"] for item in data)
        avg_views = total_views / len(data) if data else 0
    else:
        total_views = avg_views = 0
    row.update({"wiki_views": total_views, "wiki_avg_views": avg_views})

    # Google Trends
    try:
        pytrends.build_payload([name], timeframe="today 1-m")
        trend = pytrends.interest_over_time()
        trend_score = float(trend[name].mean()) if not trend.empty else 0
    except Exception:
        trend_score = 0
    row.update({"google_trends": trend_score})

    rows.append(row)

# Write to CSV
with open("candidate_metrics.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=[
            "name",
            "news_count",
            "news_sentiment",
            "google_trends",
            "wiki_views",
            "wiki_avg_views",
        ],
    )
    writer.writeheader()
    writer.writerows(rows)

print("Saved metrics to candidate_metrics.csv")
