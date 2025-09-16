# SIH Data Scraper

This Python script scrapes problem statement data from the Smart India Hackathon (SIH) 2025 website and saves it to an Excel file. It uses hashing to detect changes in the data and only updates the Excel file when new data is available.

## Features

- Fetches webpage content using requests with a custom User-Agent header.
- Parses HTML table data using BeautifulSoup.
- Extracts specific columns: S.no, PS number, Category, Organization, Submitted count, Problem statement, Description, and Theme.
- Computes MD5 hash of the data to detect changes.
- Updates Excel file only if data has changed.
- Logs operations for monitoring.

## Requirements

- Python 3.x
- requests
- beautifulsoup4
- pandas
- openpyxl (for Excel writing)

## Installation

1. Clone or download the repository.
2. Install the required packages:

   ```
   pip install requests beautifulsoup4 pandas openpyxl
   ```

## Usage

Run the script directly:

```
python scraper.py
```

The script will:
1. Fetch the webpage from https://www.sih.gov.in/sih2025PS.
2. Parse the table data.
3. Check if the data has changed by comparing hashes.
4. If changed, update `sih_data.xlsx` and save the new hash to `data_hash.txt`.
5. Log the results.

## Output Files

- `sih_data.xlsx`: Excel file containing the scraped data.
- `data_hash.txt`: Text file storing the MD5 hash of the current data.
