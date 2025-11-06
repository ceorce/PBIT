import requests
from datetime import datetime
from .config import HEADERS

SEC_DAILY_INDEX = "https://www.sec.gov/Archives/edgar/daily-index/{year}/QTR{qtr}/master.{date}.idx"

def _qtr(month: int) -> int:
    return (month - 1) // 3 + 1

def get_new_filing_paths():
    today = datetime.utcnow().date()
    url = SEC_DAILY_INDEX.format(year=today.year, qtr=_qtr(today.month), date=today.strftime("%Y%m%d"))
    r = requests.get(url, headers=HEADERS, timeout=30)
    r.raise_for_status()
    lines = r.text.splitlines()
    xml_paths = []
    for ln in lines:
        # Master index is pipe-delimited: CIK|Company Name|Form Type|Date Filed|Filename
        if "|4|" in ln:  # Form 4
            parts = ln.split("|")
            if len(parts) >= 5:
                xml_paths.append("https://www.sec.gov/Archives/" + parts[4])
    return xml_paths

def download_xml_file(url: str) -> str:
    r = requests.get(url, headers=HEADERS, timeout=30)
    r.raise_for_status()
    return r.text
