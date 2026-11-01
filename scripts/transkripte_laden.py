#!/usr/bin/env python3
"""Lädt die offiziellen Transkripte des Podcasts „Lanz + Precht“ herunter.

Der Hoster veröffentlicht die Transkripte im RSS-Feed über das Tag
<podcast:transcript>. Das Skript speichert jede Folge als Textdatei und legt
eine Übersicht (index.tsv) an. Vorhandene Dateien werden übersprungen.

Die Transkripte sind urheberrechtlich geschützt und werden nicht committet
(siehe .gitignore).

Aufruf: python3 scripts/transkripte_laden.py [--ziel VERZEICHNIS] [--neu]
"""

from __future__ import annotations

import argparse
import email.utils
import re
import sys
import time
import unicodedata
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Iterator, Tuple

FEED_URL = "https://cdn.julephosting.de/podcasts/1355-lanz-precht/feed.rss"
PODCAST_NS = {"podcast": "https://podcastindex.org/namespace/1.0"}
DEFAULT_TARGET = Path(__file__).resolve().parent.parent / "transkripte"
USER_AGENT = "ostentative-bildungshuberei/transkripte_laden"
PAUSE_SECONDS = 0.2

Episode = Tuple[str, str, str, str]  # Dateiname, Titel, Datum, Transkript-URL


def fetch(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read()


def slugify(text: str) -> str:
    text = text.lower()
    for umlaut, replacement in (("ä", "ae"), ("ö", "oe"), ("ü", "ue"), ("ß", "ss")):
        text = text.replace(umlaut, replacement)
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", text).strip("-")


def episodes(feed: bytes) -> Iterator[Episode]:
    """Liefert jede Folge des Feeds, zu der es ein Klartext-Transkript gibt."""
    for item in ET.fromstring(feed).iterfind("./channel/item"):
        url = next(
            (
                transcript.get("url")
                for transcript in item.iterfind("podcast:transcript", PODCAST_NS)
                if transcript.get("type") == "text/plain"
            ),
            None,
        )
        if url is None:
            continue

        # Titel wie „#269 (Thema)“ oder „AUSGABE 172 (Thema)“; Sonderausgaben haben keine Nummer.
        title = item.findtext("title", "").strip()
        pub_date = item.findtext("pubDate")
        date = email.utils.parsedate_to_datetime(pub_date).date().isoformat() if pub_date else ""
        topic = re.search(r"\((.*)\)", title)
        number = re.match(r"(?:#|AUSGABE\s*)(\d+)", title, re.IGNORECASE)
        if number:
            prefix = f"{int(number.group(1)):03d}"
        else:
            prefix = "-".join(filter(None, [slugify(title.split("(")[0]) or "folge", date]))
        yield f"{prefix}-{slugify(topic.group(1) if topic else title)}.txt", title, date, url


def main() -> int:
    parser = argparse.ArgumentParser(description="Lädt die Transkripte von „Lanz + Precht“ herunter.")
    parser.add_argument(
        "--ziel", type=Path, default=DEFAULT_TARGET, help="Zielverzeichnis (Standard: transkripte/ im Repo)"
    )
    parser.add_argument("--neu", action="store_true", help="vorhandene Dateien erneut herunterladen")
    args = parser.parse_args()

    found = sorted(episodes(fetch(FEED_URL)))
    args.ziel.mkdir(parents=True, exist_ok=True)

    loaded = skipped = 0
    failed = []
    for filename, title, _, url in found:
        path = args.ziel / filename
        if path.exists() and not args.neu:
            skipped += 1
            continue
        try:
            text = fetch(url).decode("utf-8-sig")
        except (OSError, UnicodeDecodeError) as error:
            failed.append(f"{title}: {error}")
            continue
        path.write_text(text, encoding="utf-8")
        loaded += 1
        time.sleep(PAUSE_SECONDS)

    rows = ["datei\ttitel\tdatum\turl"] + ["\t".join(episode) for episode in found]
    (args.ziel / "index.tsv").write_text("\n".join(rows) + "\n", encoding="utf-8")

    print(f"{len(found)} Transkripte im Feed: {loaded} geladen, {skipped} schon vorhanden, {len(failed)} fehlgeschlagen.")
    for line in failed:
        print(f"Fehler: {line}", file=sys.stderr)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
