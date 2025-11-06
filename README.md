# Piggyback Insider Trading (minimal)

A lean pipeline to fetch SEC Form 4 filings, parse & store them, detect executive cluster-buys, and alert to Discord.

## Quickstart

```bash
python -m venv .venv
# macOS/Linux
. .venv/bin/activate
# Windows PowerShell
# . .\.venv\Scripts\Activate.ps1

pip install --upgrade pip
pip install -r requirements.txt

cp .env.example .env
# Edit .env (set SEC_USER_AGENT and DISCORD_WEBHOOK_URL)
```

### Run once (single cycle)
```bash
python -c "from src.pbit.main import job_cycle; job_cycle()"
```

### Start scheduler (every 30 min)
```bash
python -m src.pbit.main
```

### Flip to Postgres later
- Set `DB_URL=postgresql+psycopg://user:pass@localhost:5432/pbit`
- In `src/pbit/analyze.py`, replace the date clause with:
  ```sql
  AND transaction_date >= CURRENT_DATE - INTERVAL '3 days'
  ```
