# utils.py
"""
    utils.py acts as a shared toolbox. Any repeated functionality—making requests, formatting output, parsing dates, validating input is stored here, 
    without having to repeat code across all tables. 
"""
import config
import urllib3
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry         
from curl_cffi import requests as cffi_requests
from dateutil import parser as dateparser



urllib3.util.connection.HAS_IPV6 = False

session = None  # Will be initialized once

def get_session():
    global session

    if session is None:
        session = cffi_requests.Session()

    return session

def make_request(method, url, json_data=None):
    try:
        headers = config.HEADERS.copy()
        if json_data is None:
            headers.pop("Content-Type", None)

        resp = get_session().request(
            method,
            url,
            headers=headers,
            json=json_data,
            timeout=60,
            impersonate="chrome124"
        )
        print(f"DEBUG -> {method} {url} -> Status: {resp.status_code}")
        resp.raise_for_status()
        return resp
    except Exception as e:
        print(f"ERROR: {e}")
        if hasattr(e, "response") and e.response is not None:
            print(f"Response: {e.response.text[:800]}")
        return None

def print_table(records):
    if not records:
        print("No records found.")
        return
    keys = [k for k in records[0].keys() if k != 'links']
    max_width = 35
    widths = {key: min(max(len(key), max(len(str(row.get(key, ''))) for row in records)), max_width) 
              for key in keys}

    header = " | ".join(f"{key.upper():<{widths[key]}}" for key in keys)
    print("\n" + header)
    print("-" * (len(header) + 10))

    for row in records:
        line_parts = [str(row.get(key, ''))[:widths[key]-3] + "..." 
                     if len(str(row.get(key, ''))) > widths[key] else f"{str(row.get(key, '')):<{widths[key]}}"
                     for key in keys]
        print(" | ".join(line_parts))

def parse_joindate(raw):
    raw = raw.strip()
    if not raw:
        return None
    try:
        dt = dateparser.parse(raw, dayfirst=False, yearfirst=False)
        if dt:
            return dt.strftime("%Y-%m-%dT00:00:00Z")
        else:
            print(f"WARNING: Could not understand date: '{raw}'")
            return None
    except Exception as e:
        print(f"⚠️ Date parsing error for '{raw}': {e}")
        return None
    
def continue_prompt():
    while True:
        choice = input("\nReturn to main menu? (Y/N): ").strip().lower()

        if choice == "y":
            return True
        elif choice == "n":
            print("\nClosing Arcane Keeper Database...")
            exit()
        else:
            print("Please enter Y or N.")