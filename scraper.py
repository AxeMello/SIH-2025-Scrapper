import requests
from bs4 import BeautifulSoup
import pandas as pd
import hashlib
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

URL = "https://www.sih.gov.in/sih2025PS"
EXCEL_FILE = "sih_data.xlsx"
HASH_FILE = "data_hash.txt"


def fetch_page(url):
    """Fetch webpage HTML using requests."""
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/91.0.4472.124 Safari/537.36"
        )
    }
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        logging.info("Successfully fetched the webpage using requests.")
        return response.text
    except Exception as e:
        logging.error(f"Error fetching the webpage: {e}")
        return None


def parse_table(html):
    """Parse table and return DataFrame with fixed column mapping."""
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table")
    if not table:
        logging.error("No table found on the webpage.")
        return None

    rows = []
    for tr in table.find_all("tr")[1:]:  # skip header
        cols = tr.find_all("td")
        if len(cols) < 7:
            continue

        row = {
            "S.no": cols[0].get_text(strip=True),
            "PS number": cols[3].get_text(strip=True),
            "Category": cols[8].get_text(strip=True),
            "Organization": cols[1].get_text(strip=True),
            "Submitted count": cols[-2].get_text(strip=True),
            "Problem statement": cols[2].find("a").get_text(strip=True) if cols[2].find("a") else cols[2].get_text(strip=True),
            "Description": cols[5].get_text(strip=True),
            "Theme": cols[9].get_text(strip=True),
        }
        rows.append(row)

    if not rows:
        logging.error("No data rows found in the table.")
        return None

    df = pd.DataFrame(rows)
    return df


def compute_hash(df):
    return hashlib.md5(df.to_csv(index=False).encode("utf-8")).hexdigest()


def read_stored_hash():
    return open(HASH_FILE).read().strip() if os.path.exists(HASH_FILE) else None


def write_stored_hash(hash_value):
    with open(HASH_FILE, "w") as f:
        f.write(hash_value)


def update_excel(df):
    df.to_excel(EXCEL_FILE, index=False)
    logging.info(f"Excel file '{EXCEL_FILE}' updated/created.")


def main():
    html = fetch_page(URL)
    if not html:
        return

    df = parse_table(html)
    if df is None or df.empty:
        logging.error("No data parsed from the table.")
        return

    current_hash = compute_hash(df)
    stored_hash = read_stored_hash()

    if current_hash != stored_hash:
        update_excel(df)
        write_stored_hash(current_hash)
        logging.info("Data changed. Excel updated.")
    else:
        logging.info("No changes detected. Excel not updated.")


if __name__ == "__main__":
    main()
