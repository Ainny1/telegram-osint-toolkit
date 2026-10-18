import json
import pytest
from telegram_osint.core import parse_public_link, analyze_links, analyze_export

@pytest.mark.parametrize("value", ["@OpenAI", "https://t.me/OpenAI", "t.me/OpenAI"])
def test_public_username(value):
    assert parse_public_link(value)["username"] == "OpenAI"

@pytest.mark.parametrize("value", ["https://t.me/+InviteCode", "https://t.me/joinchat/secret", "https://t.me/c/123/4", "http://t.me/OpenAI", "https://evil.com/OpenAI", "https://t.me/OpenAI/12", "https://t.me/OpenAI?start=x", "@a"])
def test_reject_private_and_invalid(value):
    with pytest.raises(ValueError):
        parse_public_link(value)

def test_dedup_and_redact():
    result = analyze_links(["@OpenAI", "https://t.me/openai", "https://t.me/+secret"])
    assert len(result["entities"]) == 1
    assert result["rejected_count"] == 1
    assert "+secret" not in json.dumps(result)

def test_export_privacy(tmp_path):
    data = {"messages": [{"type": "message", "date": "2025-01-02T12:00:00", "text": "TOP_SECRET", "from": "Person"}, {"type": "service", "date": "2025-02-01"}]}
    file = tmp_path / "result.json"
    file.write_text(json.dumps(data))
    report = analyze_export(file)
    assert report["total_messages"] == 2
    assert report["messages_by_month"] == {"2025-01": 1, "2025-02": 1}
    assert "TOP_SECRET" not in json.dumps(report)
    assert "Person" not in json.dumps(report)
