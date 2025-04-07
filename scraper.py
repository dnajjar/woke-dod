import requests
import pandas as pd
from datetime import datetime
import time
import re
from nltk.tokenize import sent_tokenize
import nltk
nltk.download('punkt_tab')

def get_keyword_matches(keywords) -> list:
    '''Query USASpending API for contracts matching keywords in past 5 years'''
    all_results = []
    max_pages = 300  
    url = "https://api.usaspending.gov/api/v2/search/spending_by_award/"
    page = 1
    payload = {
        "filters": {
            "keywords": keywords,
            "award_type_codes": ["A", "B", "C", "D"], 
            "agencies": [
                {
                    "type": "awarding",
                    "tier": "toptier",
                    "name": "Department of Defense"
                }
            ],
            "time_period": [
                {
                    "start_date": "2020-01-01",
                    "end_date": "2025-03-31"
                }
            ]
        },
        "fields": [
            "Award ID", "Recipient Name", "Award Amount", "Award Description", 
            "Period of Performance Start Date", "Period of Performance Current End Date",
            "Awarding Agency", "Place of Performance State Code"
        ],
        "limit": 100,
        "page": page,
        "sort": "Award Amount",
        "order": "desc" 
    }
    for page in range(1, max_pages + 1):
        payload["page"] = page
        response = requests.post(url, json=payload)

        if response.status_code != 200:
            print(f"Page {page}: Error {response.status_code}")
            break

        results = response.json().get("results", [])
        if not results:
            print("No more results")
            break 

        all_results.extend(results)
        time.sleep(0.5)
        return all_results

def is_active(date) -> bool:
    '''Is the contract still active?'''
    if pd.isna(date):
        return "unknown"
    return "active" if date > datetime.today() else "inactive"

def clean_up_matches(match_df, keywords) -> pd.DataFrame:
    '''
    Clean up results and return dataframe with relevnat fields 
    '''
    text_cols = match_df.select_dtypes(include='object').columns
    sentence_matches = []
    match_df['end_date'] = pd.to_datetime(match_df['Period of Performance Current End Date'], errors='coerce').fillna('')
    match_df['Award Description'] = match_df['Award Description'].fillna('').str.lower()
    match_df['is_active'] = match_df["end_date"].apply(is_active)

    for index, row in match_df.iterrows():
        for keyword in keywords:
            for col in text_cols:
                val = row[col]
                if isinstance(val, str) and re.search(rf"\b{keyword}\b", val, re.IGNORECASE):
                    sentence_matches.append({
                        "Matched On": col,
                        "Matched Text": val,
                        "Keyword": keyword,
                        'Recipient': row.get('Recipient Name', ''),
                        "Award ID": row.get("Award ID", ""),
                        'Active': row.get('is_active', ''),
                        "End Date": row.get('Period of Performance Current End Date', ''),
                    })

    return pd.DataFrame(sentence_matches)

def main():
    keywords = ["diversity", "equity", "inclusion", "minority", "underrepresented"]

    all_matches_list = get_keyword_matches(keywords)
    all_matches_df = pd.DataFrame(all_matches_list)

    print(f"Fetched {len(all_matches_df)} records")

    clean_df = clean_up_matches(all_matches_df, keywords)

    print(clean_df)

if __name__ == '__main__':
    main()
