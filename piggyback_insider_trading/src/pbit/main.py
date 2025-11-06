import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from sqlalchemy.orm import Session
from .config import settings
from .db import init_db, SessionLocal
from .sec_fetch import get_new_filing_paths, download_xml_file
from .parser import parse_form4_xml
from .store import save_filing_to_db
from .analyze import run_cluster_analysis
from .alert import format_alert_message, send_discord_webhook

logging.basicConfig(level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO))
log = logging.getLogger("pbit")

def job_cycle():
    init_db()
    with SessionLocal() as db:  # type: Session
        try:
            paths = get_new_filing_paths()
            log.info("Found %d new Form 4 paths", len(paths))
            for p in paths:
                try:
                    xml = download_xml_file(p)
                    items = parse_form4_xml(xml)
                    for it in items:
                        it["filing_url"] = p
                        save_filing_to_db(db, it)
                    db.commit()
                except Exception as e:
                    db.rollback()
                    log.exception("Failed to process %s: %s", p, e)
        except Exception as e:
            log.exception("Fetcher failed: %s", e)

        try:
            rows = run_cluster_analysis(db)
            msg = format_alert_message(rows)
            if rows:
                send_discord_webhook(msg)
            log.info(msg)
        except Exception as e:
            log.exception("Analysis/Alert failed: %s", e)

def main():
    sched = BlockingScheduler()
    sched.add_job(job_cycle, "interval", minutes=30, id="pbit-cycle", coalesce=True, max_instances=1)
    log.info("Scheduler started. Running every 30 minutes.")
    sched.start()

if __name__ == "__main__":
    main()
