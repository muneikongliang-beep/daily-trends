import json
import datetime
import feedparser  # GitHub Actions側でインストールするのでローカル不要

# 安定して取れるRSSソースから始める
SOURCES = {
    "hatena_hotentry": "https://b.hatena.ne.jp/hotentry.rss",
    "hatena_it":       "https://b.hatena.ne.jp/hotentry/it.rss",
    "zenn_trend":      "https://zenn.dev/feed",
    "qiita_popular":   "https://qiita.com/popular-items/feed",
}

def collect():
    results = []
    for name, url in SOURCES.items():
        feed = feedparser.parse(url)
        for entry in feed.entries[:20]:  # 各ソース上位20件
            results.append({
                "source": name,
                "title": entry.get("title", ""),
                "link": entry.get("link", ""),
                "summary": entry.get("summary", "")[:300],
            })
    return results

def main():
    today = datetime.date.today().isoformat()
    data = {
        "date": today,
        "collected_at": datetime.datetime.now().isoformat(),
        "items": collect(),
    }
    with open(f"data/trends_{today}.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"collected {len(data['items'])} items")

if __name__ == "__main__":
    main()
