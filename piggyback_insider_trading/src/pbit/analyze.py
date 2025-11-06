from sqlalchemy import text
from sqlalchemy.orm import Session

QUERY = text("""
SELECT
  ticker,
  COUNT(DISTINCT insider_name) AS insider_count
FROM filings
WHERE transaction_code = 'P'
  AND is_10b51 = 0
  AND is_open_market = 1
  AND (insider_title LIKE '%CEO%' OR insider_title LIKE '%CFO%' OR insider_title LIKE '%COO%' OR insider_title LIKE '%President%')
  AND transaction_date >= date('now','-3 day')
GROUP BY ticker
HAVING COUNT(DISTINCT insider_name) >= 2
ORDER BY insider_count DESC
""")

def run_cluster_analysis(db: Session):
    return db.execute(QUERY).mappings().all()
