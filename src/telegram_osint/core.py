"""Privacy-minded analysis of user-supplied public Telegram links and exports."""
from __future__ import annotations
import csv
import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit

USERNAME = re.compile(r"^[A-Za-z][A-Za-z0-9_]{4,31}$")
PUBLIC_HOSTS = {"t.me", "telegram.me", "www.t.me", "www.telegram.me"}
EXCLUDED_PATHS = {"joinchat", "addstickers", "addemoji", "share", "proxy", "socks", "iv", "login", "c"}


def parse_public_link(raw: str) -> dict:
    """Accept only canonical public Telegram username links; reject invite/private URLs."""
    raw = raw.strip()
    if raw.startswith("@"):
        username = raw[1:]
    else:
        candidate = raw if "://" in raw else "https://" + raw
        url = urlsplit(candidate)
        if url.scheme != "https" or url.hostname not in PUBLIC_HOSTS or url.username or url.password or url.port:
            raise ValueError("Only HTTPS public Telegram links are supported")
        parts = [p for p in url.path.split("/") if p]
        if len(parts) != 1 or parts[0].lower() in EXCLUDED_PATHS or url.query or url.fragment:
            raise ValueError("Private, invite, message, or parameterized links are excluded")
        username = parts[0]
    if not USERNAME.fullmatch(username):
        raise ValueError("Invalid public username")
    return {"username": username, "url": f"https://t.me/{username}", "type": "public_username"}


def analyze_links(items: list[str]) -> dict:
    valid, rejected = {}, []
    for item in items:
        if not item.strip() or item.lstrip().startswith("#"):
            continue
        try:
            record = parse_public_link(item)
            valid[record["username"].lower()] = record
        except ValueError:
            rejected.append({"input": "[redacted]", "reason": "unsupported or invalid public link"})
    return {"scope": "user-supplied public references only", "entities": sorted(valid.values(), key=lambda x: x["username"].lower()), "rejected_count": len(rejected)}


def analyze_export(path: Path) -> dict:
    """Aggregate counts from a Telegram Desktop JSON export; do not retain message text or identities."""
    data = json.loads(path.read_text(encoding="utf-8"))
    messages = data.get("messages")
    if not isinstance(messages, list):
        raise ValueError("Expected a Telegram Desktop JSON export with a 'messages' array")
    by_month = Counter()
    types = Counter()
    for message in messages:
        if not isinstance(message, dict):
            continue
        types[str(message.get("type", "unknown"))] += 1
        date = message.get("date")
        if isinstance(date, str):
            try:
                dt = datetime.fromisoformat(date.replace("Z", "+00:00"))
                by_month[dt.strftime("%Y-%m")] += 1
            except ValueError:
                pass
    return {"scope": "local user-provided export", "total_messages": sum(types.values()),
            "messages_by_month": dict(sorted(by_month.items())), "message_types": dict(sorted(types.items())),
            "privacy": "No message bodies, participant names, phone numbers, or identifiers are saved."}


def save_report(report: dict, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
