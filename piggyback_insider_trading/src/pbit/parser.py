from lxml import etree
import re
from datetime import date

def _text(node, xpath):
    el = node.xpath(xpath)
    return el[0].text.strip() if el else ""

def parse_form4_xml(xml: str) -> list[dict]:
    """Return a list of transaction dicts aligned with the DB schema."""
    root = etree.fromstring(xml.encode("utf-8"))
    company_name = _text(root, "//issuer/issuerName")
    ticker = _text(root, "//issuer/issuerTradingSymbol")
    insider_cik = _text(root, "//reportingOwner/reportingOwnerId/rptOwnerCik")
    insider_name = _text(root, "//reportingOwner/reportingOwnerId/rptOwnerName")
    insider_title = _text(root, "//reportingOwner/reportingOwnerRelationship/officerTitle")
    footnotes_txt = " ".join([etree.tostring(n, method="text", encoding="unicode") for n in root.xpath("//footnotes")])

    filings = []

    def collect(table_xpath, is_derivative: bool):
        rows = root.xpath(table_xpath)
        for row in rows:
            code = _text(row, ".//transactionCoding/transactionCode")
            txn_date = _text(row, ".//transactionDate/value")
            shares = _text(row, ".//transactionAmounts/transactionShares/value") or "0"
            price = _text(row, ".//transactionAmounts/transactionPricePerShare/value") or "0"
            is_acq = code in {"P", "A", "M"}
            total_value = float(price or 0.0) * float(shares or 0.0)
            filings.append({
                "ticker": ticker,
                "company_name": company_name,
                "insider_cik": insider_cik,
                "insider_name": insider_name,
                "insider_title": insider_title or ("Derivative" if is_derivative else ""),
                "transaction_date": date.fromisoformat(txn_date) if txn_date else date.today(),
                "is_acquisition": bool(is_acq),
                "transaction_code": code,
                "shares": int(float(shares)),
                "price_per_share": float(price or 0.0),
                "total_value": float(total_value),
                "is_open_market": code in {"P","S"},
                "is_10b51": bool(re.search(r"10b5-1|10b5\s*-?\s*1|planned trading", footnotes_txt, re.I)),
                "filing_url": "",
            })

    collect("//nonDerivativeTable/nonDerivativeTransaction", is_derivative=False)
    collect("//derivativeTable/derivativeTransaction", is_derivative=True)

    return filings
