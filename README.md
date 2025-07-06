# Times Person Of The Year Prediction Algorithm

This repository contains example scripts that collect public data and train a
simple machine learning model to estimate who might become TIME's "Person of
the Year".

## Setup

Install dependencies with:

```bash
pip install -r requirements.txt
```

For Twitter data you also need an API token. Set it in the environment as
`TWITTER_BEARER_TOKEN`.

## Data Collection

1. **Scrape TIME covers**
   ```bash
   python scrape_time_covers.py
   ```
   This creates `time_covers_2000_2024.csv` containing the date and subject of
   each magazine cover between 2000 and 2024.

2. **Wikipedia page views**
   Prepare a CSV called `shortlist_2024.csv` with a column `Name` listing the
   people you want to track. Then run:
   ```bash
   python wikipedia_pageviews.py
   ```
   The script stores monthly view counts in `wikipedia_views.csv`.

3. **Twitter mentions**
   ```bash
   python twitter_mentions.py
   ```
   This uses the Twitter API to fetch monthly counts and saves them to
   `twitter_mentions.csv`.

## Preparing Training Data

Combine the collected page views and mention counts into a file
`training_features.csv` with columns:
`Year,Name,Views,Tweet Count`. Create another file `winners.csv` containing the
historical winners with columns `Year,Winner` (these can be copied from
Wikipedia).

For the year you want predictions for, assemble a similar features file (for
example `features_2024.csv`).

## Training and Prediction

Run the model script:

```bash
python poty_model.py
```

The script performs a simple grid search over a RandomForest classifier,
outputs classification metrics, saves the model to
`person_of_the_year_model.pkl`, and prints predicted scores for the upcoming
year based on `features_2024.csv`.

## Disclaimer

These scripts rely only on public metadata (such as Wikipedia view counts and
Twitter mention totals). They do not redistribute any copyrighted TIME
content.
