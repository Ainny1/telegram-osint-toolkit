"""Command-line interface."""
import argparse
import json
from pathlib import Path
from .core import analyze_links, analyze_export, save_report


def main(argv=None):
    parser = argparse.ArgumentParser(prog="tg-osint", description="Privacy-first Telegram public-link and offline export analyzer")
    sub = parser.add_subparsers(dest="command", required=True)
    links = sub.add_parser("links", help="Normalize user-provided public Telegram links")
    links.add_argument("inputs", nargs="*", help="Public @usernames or HTTPS t.me/username links")
    links.add_argument("--file", type=Path, help="UTF-8 text file containing one reference per line")
    links.add_argument("--output", type=Path, help="Write summary JSON to this path")
    export = sub.add_parser("export", help="Summarize an offline Telegram Desktop JSON export")
    export.add_argument("json_file", type=Path)
    export.add_argument("--output", type=Path, help="Write summary JSON to this path")
    args = parser.parse_args(argv)
    try:
        if args.command == "links":
            inputs = list(args.inputs)
            if args.file:
                inputs.extend(args.file.read_text(encoding="utf-8").splitlines())
            report = analyze_links(inputs)
        else:
            report = analyze_export(args.json_file)
        if args.output:
            save_report(report, args.output)
            print(f"Summary saved to {args.output}")
        else:
            print(json.dumps(report, indent=2, ensure_ascii=False))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        parser.exit(2, f"Error: {exc}\n")

if __name__ == "__main__":
    main()
