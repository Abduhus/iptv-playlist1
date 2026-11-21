#!/usr/bin/env python3
"""Build an aggregated M3U playlist from iptv-org country stream files."""
from __future__ import annotations
import re
import urllib.request
from pathlib import Path

COUNTRIES = {
    "Middle East": "ae sa bh kw om qa ye iq jo lb sy ps il ir",
    "North Africa": "eg ly tn dz ma mr sd",
    "Turkey": "tr",
    "Europe": "at be bg hr cy cz dk ee fi fr de gr hu ie it lv lt lu mt nl pl pt ro sk si es se gb",
}
BASE = "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/{}.m3u"
OUT = Path(__file__).resolve().parent / "playlist.m3u"


def download(code: str) -> str:
    request = urllib.request.Request(BASE.format(code), headers={"User-Agent": "Mozilla/5.0 custom-m3u-playlist/1.0"})
    with urllib.request.urlopen(request, timeout=25) as r:
        return r.read().decode("utf-8-sig", errors="replace")


def parse(content: str):
    lines = content.splitlines()
    for i, line in enumerate(lines):
        if not line.startswith("#EXTINF:"):
            continue
        metadata = line.strip()
        j = i + 1
        extras = []
        while j < len(lines) and lines[j].strip().startswith("#") and not lines[j].startswith("#EXTINF:"):
            extras.append(lines[j].strip())
            j += 1
        if j < len(lines):
            url = lines[j].strip()
            if url.startswith(("https://", "http://")):
                yield metadata, extras, url


def main():
    lines = ["#EXTM3U"]
    seen = set()
    failures = []
    counts = {}
    for group, countries in COUNTRIES.items():
        counts[group] = 0
        for code in countries.split():
            try:
                data = download(code)
            except Exception as exc:
                failures.append(f"{code}: {exc}")
                continue
            for meta, extras, url in parse(data):
                if url in seen:
                    continue
                seen.add(url)
                # Preserve stream attributes and category grouping for Tizen IPTV apps.
                if 'group-title="' in meta:
                    meta = re.sub(r'group-title="[^"]*"', f'group-title="{group}"', meta, count=1)
                else:
                    meta = meta.replace(' ,', ',')
                    k = meta.index(',') if ',' in meta else len(meta)
                    meta = meta[:k] + f' group-title="{group}"' + meta[k:]
                lines.extend([meta, *extras, url])
                counts[group] += 1
    if not seen:
        raise RuntimeError("No channels could be downloaded; refusing to overwrite playlist")
    if failures:
        print('Warning: source failures:', *failures, sep='\n')
    OUT.write_text('\n'.join(lines) + '\n', encoding="utf-8")
    print(f"Wrote {len(seen)} streams to {OUT}", counts)


if __name__ == "__main__":
    main()
