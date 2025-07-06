# Times-Person-Of-The-Year-Prediction-Algorithm

This repository contains utilities for collecting data related to TIME's Person of the Year.

## Scripts

- `times_covers` – Scrapes Wikipedia for a list of TIME magazine covers between 2000 and 2024 and saves them to `time_magazine_covers_2000_2024.csv`.
- `candidate_scraper.py` – Gathers media and popularity metrics for nine 2023 finalists and stores the results in `candidate_metrics.csv`.

## Usage

Install the required Python packages and run the scraper:

```bash
pip install feedparser requests vaderSentiment pytrends pandas
python3 candidate_scraper.py
```

The script outputs a CSV file with Google News article counts, average sentiment, Google Trends scores and recent Wikipedia page views for each candidate.
