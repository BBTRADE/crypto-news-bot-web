import feedparser
import os
from datetime import datetime, timedelta, timezone

# ニュースフィードの一覧
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
    today = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    yaml = f'update_time: "{today}"\n'
    yaml += 'summary_post_generation:\n'
    yaml += '  purpose: "過去24時間の暗号資産関連ニュースを調査し、まとめ投稿を作成する"\n'
    yaml += 'structure:\n'
    yaml += '  order:\n'
    yaml += '    - "最新ニュースまとめ"\n'
    yaml += '    - "トレード戦略・見解"\n'
    yaml += '    - "今週の米国経済指標＆イベント（日本時間で記載）：https://www.gaikaex.com/gaikaex/mark/calendar/index.phpを参照"\n'
    yaml += f'  news_summary:\n    - title: "📢 最新ニュース（{datetime.now().strftime("%m/%d")}）"\n'
    yaml += 'items:\n'
    for item in news_items:
        yaml += f'  - headline: "✅{item["title"]}"\n'
        yaml += f'    summary: "📝要約（未入力）"\n'
        yaml += f'    url: "🔗{item["url"]}"\n'
        yaml += f'    comment: "▶コメント＆解説（未入力）"\n'
    yaml += '''strategy_commentary:
  title: "📊マーケット反応とトレード戦略"
  body: "現在、国際的な情勢の影響で市場が不安定です。リスク管理と情報収集を徹底しましょう。"
economic_events:
  title: "📅今週の重要経済指標・イベント"
  schedule:
    - date: "📌06月05日（水）"
      event: "✅21:30 米国・雇用統計（予想あり）"
  note: "指標発表前後は急変動に注意"
disclaimer: "※本投稿は情報提供を目的としたものであり、特定の投資行動を推奨するものではありません。投資判断はご自身の責任でお願いいたします。"
rules:
  forbidden:
    - "ハルシネーション"
    - "過去24時間より前のニュース掲載"
    - "不完全なURLの掲載"
    - "機能しないURLの掲載"
  recommended:
    - "ハルシネーションチェックの実施"
    - "ファクトチェックの実施"
    - "URLの正確性確認"
    - "プロ視点としてのコメント確認（犬郎として）"
    - "以下の絵文字を使用推奨：📅✅📌💣🚀▶📢🎉⚠️📝📊📉📈"
'''
    return yaml

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
    button {{ margin-bottom: 15px; padding: 8px 16px; font-size: 14px; }}
  </style>
</head>
<body>
  <h2>📄 山田犬郎のまとめ用YAML</h2>
  <button onclick="copyYAML()">📋 コピー</button>
  <pre id="yamlBlock" class="YAML">{yaml_content}</pre>
  <script>
    function copyYAML() {{
      const text = document.getElementById("yamlBlock").innerText;
      navigator.clipboard.writeText(text).then(() => {{
        alert("コピーしました！");
      }});
    }}
  </script>
</body>
</html>"""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

if __name__ == "__main__":
    news = fetch_news()
    yaml_text = generate_yaml(news)
    generate_html_with_yaml(yaml_text)
