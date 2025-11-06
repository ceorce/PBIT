import requests
from .config import settings

def format_alert_message(rows):
    if not rows:
        return "No cluster buys detected in the last 3 days."
    lines = ["**Cluster Buys (last 3 days)**"]
    for r in rows:
        lines.append(f"- {r['ticker']}: {r['insider_count']} executives bought (open-market, non-10b5-1)")
    return "\n".join(lines)

def send_discord_webhook(message: str):
    if not settings.DISCORD_WEBHOOK_URL:
        return False
    r = requests.post(settings.DISCORD_WEBHOOK_URL, json={"content": message}, timeout=15)
    r.raise_for_status()
    return True
