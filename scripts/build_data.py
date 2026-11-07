"""Turn the HackerTube dump into small files the HackerTok page can load fast.

Usage: python3 -I scripts/build_data.py   (run from ~/hackertok)

Writes:
  site/data/videos.json        one compact row per video (feed)
  site/data/c/<vid>.json       that video's HN comments, best first (loaded on demand)
"""
import json, os, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "data", "raw", "hackertube-data")
OUT = os.path.join(ROOT, "site", "data")
STANCE_ORDER = {"strong_rec": 0, "rec": 1, "reference": 2, "critical": 3, "joke": 4}

def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(os.path.join(OUT, "c"))

    videos = []
    keep = set()
    with open(os.path.join(RAW, "videos.jsonl"), encoding="utf-8") as f:
        for line in f:
            v = json.loads(line)
            if v.get("shelf_life") == "news":  # only mattered around one event
                continue
            hn = v["hn"]
            keep.add(v["vid"])
            videos.append({
                "v": v["vid"],
                "t": v["title"],
                "ch": v["channel"],
                "why": v.get("why_hn") or "",
                "sum": v.get("summary") or "",
                "type": v.get("content_type") or "",
                "topic": v.get("primary_topic") or "",
                "cats": [c["name"] for c in v.get("categories", [])][:2],
                "tags": (v.get("tags") or [])[:4],
                "q": (v.get("quote") or {}).get("text") or "",
                "s": v.get("score") or 0,
                "recs": hn.get("recommenders", 0),
                "n": hn.get("mentions", 0),
                "y": [hn.get("first_year"), hn.get("last_year")],
            })

    by_vid = {}
    with open(os.path.join(RAW, "mentions.jsonl"), encoding="utf-8") as f:
        for line in f:
            m = json.loads(line)
            if m["vid"] not in keep:
                continue
            by_vid.setdefault(m["vid"], []).append({
                "id": m["hn_comment_id"],
                "a": m["author"],
                "m": m["month"],
                "st": m["stance"],
                "story": m.get("story_title") or "",
                "text": m["text"],
            })

    for vid, ms in by_vid.items():
        ms.sort(key=lambda c: (STANCE_ORDER.get(c["st"], 9), c["m"]))
        with open(os.path.join(OUT, "c", vid + ".json"), "w", encoding="utf-8") as f:
            json.dump(ms, f, ensure_ascii=False, separators=(",", ":"))

    with open(os.path.join(OUT, "videos.json"), "w", encoding="utf-8") as f:
        json.dump(videos, f, ensure_ascii=False, separators=(",", ":"))

    print(f"{len(videos)} videos, {sum(map(len, by_vid.values()))} comments in {len(by_vid)} files")

if __name__ == "__main__":
    main()
