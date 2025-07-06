import requests
from bs4 import BeautifulSoup
import csv
from pytrends.request import TrendReq
import pandas as pd
from datetime import datetime

# Phase 1: Get shortlists and winners

def get_shortlist(year):
    url = f"https://time.com/{year}-person-of-the-year-shortlist/"
    r = requests.get(url)
    if r.status_code != 200:
        return []
    soup = BeautifulSoup(r.text, 'html.parser')
    names = set(
        tag.get_text(strip=True)
        for tag in soup.select('h3, h2, li')
        if any(c in tag.get_text() for c in tag.get_text().split())
    )
    return sorted(names)

def get_winner(year):
    resp = requests.get("https://en.wikipedia.org/wiki/Time_Person_of_the_Year")
    soup = BeautifulSoup(resp.text, 'html.parser')
    table = soup.find('table', {'class': 'wikitable'})
    year_str = str(year)
    for row in table.find_all('tr'):
        cols = [c.text.strip() for c in row.find_all(['th','td'])]
        if cols and cols[0].startswith(year_str):
            return cols[1].split(' and ')[0]
    return None

def collect_shortlists():
    with open('shortlists.csv','w',newline='',encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['year','name','shortlisted'])
        for y in range(2000, 2025):
            shortlist = get_shortlist(y)
            winner = get_winner(y)
            for name in shortlist:
                writer.writerow([y, name, 1])
            if winner and winner not in shortlist:
                writer.writerow([y, winner, 1])
    print("Shortlists collected!")

# Phase 2: Add features

def wiki_views(name, year):
    s, e = f"{year}0101", f"{year}1231"
    url = (
        "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/"
        f"en.wikipedia.org/all-access/all-agents/{name.replace(' ','_')}/daily/{s}/{e}"
    )
    r = requests.get(url)
    if r.status_code != 200:
        return 0, 0
    items = r.json().get('items', [])
    views = [i['views'] for i in items]
    return sum(views), (sum(views)//len(views)) if views else (0,0)

def google_trend(name, year):
    py = TrendReq(hl='en-US', tz=360)
    tf = f"{year}-01-01 {year}-12-31"
    try:
        py.build_payload([name], timeframe=tf)
        df = py.interest_over_time()
        return int(df[name].mean()) if not df.empty else 0
    except Exception:
        return 0

def add_features():
    df = pd.read_csv("shortlists.csv")
    for year in df['year'].unique():
        mask = df['year']==year
        for idx in df[mask].index:
            nm = df.at[idx,'name']
            tot, avg = wiki_views(nm, year)
            df.at[idx,'wiki_views_total'] = tot
            df.at[idx,'wiki_views_avg'] = avg
            df.at[idx,'google_trend'] = google_trend(nm, year)
    df.to_csv("features.csv", index=False)
    print("Features added!")

# Phase 3: Master dataset

def build_master():
    short = pd.read_csv("shortlists.csv")
    feat = pd.read_csv("features.csv")
    df = short.merge(feat, on=['year','name','shortlisted'], how='left')
    extras = []
    for year in df.year.unique():
        top = df[df.year == year].nlargest(50, 'wiki_views_total')['name']
        for name in top:
            if name not in set(df[df.year == year]['name']):
                extras.append({'year':year,'name':name,'shortlisted':0})
    df = pd.concat([df, pd.DataFrame(extras)], ignore_index=True)
    df = df.fillna(0)
    df.to_csv("master_dataset_2000_2024.csv", index=False)
    print("Pipeline complete! Dataset ready.")
    print(df.head())

if __name__ == '__main__':
    collect_shortlists()
    add_features()
    build_master()
