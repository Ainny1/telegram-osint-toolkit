# Telegram OSINT Investigation Toolkit

![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue) ![MIT License](https://img.shields.io/badge/License-MIT-green)

**A privacy-first Python CLI for validating public Telegram username references and analyzing user-provided Telegram Desktop JSON exports offline.**

Maintainer: [Ainny1](https://github.com/Ainny1) · Version: 0.1.0

## Overview

This original cybersecurity portfolio project demonstrates input validation, OSINT methodology, offline forensic analysis, data minimization, testing, and CI. It makes **no network requests**, requires **no Telegram API credentials**, and never bypasses Telegram access controls.

## Features

- Validate public `@username` and `https://t.me/username` references
- Normalize and deduplicate public username links
- Reject private invite, internal, malformed, and parameterized links
- Summarize authorized Telegram Desktop JSON exports by month and message type
- Exclude message text, participant names, phone numbers, and IDs from reports
- Write JSON reports or display results in the terminal
- Run automated tests via GitHub Actions

**Note:** URL validation does not verify whether a Telegram username exists or identify its owner.

## Setup

Requires Python 3.10+.

```bash
git clone https://github.com/Ainny1/telegram-osint-toolkit.git
cd telegram-osint-toolkit
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .
```

On Windows PowerShell, activate with `.venv\Scripts\Activate.ps1`.

## Run

Analyze public references:

```bash
tg-osint links @OpenAI https://t.me/telegram
tg-osint links --file examples/public_links.txt --output reports/links.json
```

Analyze a Telegram Desktop JSON export that you own or have permission to process:

```bash
tg-osint export /path/to/result.json --output reports/summary.json
```

All processing is local. Never upload raw private exports or sensitive results to a public repository.

### Example report

```json
{
  "scope": "user-supplied public references only",
  "entities": [
    {"username": "OpenAI", "url": "https://t.me/OpenAI", "type": "public_username"}
  ],
  "rejected_count": 0
}
```

## Structure

```text
src/telegram_osint/
  core.py         # Link validation and privacy-first export summaries
  cli.py          # Command line application
  __main__.py     # Python module entry point
tests/test_core.py
examples/public_links.txt
.github/workflows/tests.yml
pyproject.toml
LICENSE
```

## Tests

```bash
python -m pip install pytest
python -m pytest -q
```

## Ethical use

Only investigate public references for legitimate purposes and process exports with proper authorization. This software does not scrape profiles, access private chats, enumerate phone numbers, or collect account credentials. Generated reports and local exports should remain private when sensitive.

## Roadmap

- [x] Public reference validation and normalization
- [x] Privacy-preserving offline JSON export aggregation
- [x] JSON reports
- [x] Unit tests and GitHub Actions CI
- [ ] Timeline visualization using synthetic test data
- [ ] Documentation walkthrough with synthetic examples

## Skills demonstrated

Python · OSINT · cybersecurity · CLI design · input validation · local digital forensics · automated testing · GitHub Actions · privacy by design

Licensed under MIT. See [LICENSE](LICENSE).
