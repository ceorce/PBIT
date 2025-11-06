from sqlalchemy.orm import Session
from .db import Filing
from datetime import date

def save_filing_to_db(db: Session, data: dict):
    f = Filing(
        ticker=data["ticker"],
        company_name=data["company_name"],
        insider_cik=data["insider_cik"],
        insider_name=data["insider_name"],
        insider_title=data["insider_title"],
        transaction_date=data["transaction_date"] if isinstance(data["transaction_date"], date) else date.fromisoformat(data["transaction_date"]),
        is_acquisition=bool(data["is_acquisition"]),
        transaction_code=data["transaction_code"],
        shares=int(data["shares"]),
        price_per_share=data["price_per_share"],
        total_value=data["total_value"],
        is_open_market=bool(data["is_open_market"]),
        is_10b51=bool(data["is_10b51"]),
        filing_url=data.get("filing_url",""),
    )
    db.add(f)
