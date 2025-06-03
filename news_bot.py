import feedparser
import datetime
import os
from datetime import datetime, timedelta, timezone

RSS_URLS = [
    "https://www.coindesk.com/arc/outboundfeeds/rss/",
    "https://cointelegraph.com/rss",
    "https://decrypt.co/feed",
    "https://news.bitcoin.com/feed/",
    "https://cryptonews.com/news/feed/",
    "https://jp.cointelegraph.com/rss",
    "https://coinpost.jp/?feed=rss2",
    "https://www.cnbc.com/id/100003114/device/rss/rss.html",
    "https://www.reuters.com/finance/economy/rss",
    "https://www.aljazeera.com/xml/rss/all.xml",
    "https://www3.nhk.or.jp/rss/news/cat0.xml"
]

def is_recent(entry, hours=24):
    try:
        published = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
        return published > datetime.now(timezone.utc) - timedelta(hours=hours)
    except:
        return True

def is_similar(t1, t2):
    return t1[:15] in t2 or t2[:15] in t1

def fetch_news():
    seen, entries = [], []
    for url in RSS_URLS:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            if is_recent(entry) and not any(is_similar(entry.title, t) for t in seen):
                entries.append({
                    "title": entry.title,
                    "url": entry.link
                })
                seen.append(entry.title)
    return entries

def generate_yaml(news_items):
    today = datetime.now().strftime('%Y-%m-%d')
    yaml_text = f'date: "{today}"\nnews:\n'
    for item in news_items:
        yaml_text += f'  - title: "{item["title"]}"\n'
        yaml_text += f'    url: "{item["url"]}"\n'
    return yaml_text

def generate_html_with_yaml(yaml_content, output_path="output_html/news_embed.html"):
    html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <title>山田犬郎 YAMLニュース</title>
  <meta name="robots" content="noindex">
  <style>
    body {{ font-family: monospace; padding: 20px; background: #f4f4f4; }}
    .YAML {{ white-space: pre-wrap; background: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }}
  </style>
</head>
<body>
  <h2>📄 山田犬郎のまとめ用YAML</h2>
  <div class="YAML">
{yaml_content}
  </div>
</body>
</html>"""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

if __name__ == "__main__":
    news = fetch_news()
    yaml_text = generate_yaml(news)
    generate_html_with_yaml(yaml_text)
