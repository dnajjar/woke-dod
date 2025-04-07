# DEI Language in Department of Defense Contracts

This project uses the [USAspending.gov API](https://api.usaspending.gov/) to retrieve and analyze Department of Defense (DoD) contract awards that include diversity, equity, and inclusion (DEI) language. Its long term aim is to investigate how DEI-focused contracts are treated across agencies — especially in contrast to those that have been politically targeted or defunded. It is inspired by [ProPublica's](https://www.propublica.org/article/ted-cruz-woke-grants-national-science-foundation) analysis of "woke" NSF grants. 

## Features

- Queries multiple pages of DoD contract awards using DEI-related keywords
- Extracts and cleans metadata including award description, amount, agency, and timeline
- Flags contracts as `"active"`, `"inactive"`, or `"unknown"` based on the current date and available end dates

## How It Works

1. Defines a query payload for the USAspending API, filtering for:
   - Keywords: `"diversity"`, `"equity"`, `"inclusion"`, `"minority"`, `"underrepresented"`
   - Agency: Department of Defense
   - Award types: Contract awards only
   - Date range

2. Iterates over multiple pages of API results using a configurable `max_pages` parameter

3. Stores and structures the results in a Pandas DataFrame

## How to Run the Project

1. Clone the repository
2. cd into the directory
3. pip install -r requirements.txt
4. Run `python3 scraper.py`

## Limitations

1. The USASpending API does not provide access to the full text of the contract, and so we are limited to using brief summaries and award descriptions, which often lack substantive detail.
2. This analysis is limited to simple keyword matching. A more useful follow-up should further filter results to throw out false positives (or better yet compare the prevalence of false positives in DoD contracts vs NSF grants)
