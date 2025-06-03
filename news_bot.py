import datetime
import os

def fetch_news():
    return [
        {
            "title": "Crypto Lobbyists Urge U.S. Senators...",
            "url": "https://www.coindesk.com/...",
            "summary": "米国でステーブルコインの...",
            "comment": "これは選挙前の駆け引き。..."
        },
        {
            "title": "Ethereum Foundation Lays Off...",
            "url": "https://www.coindesk.com/...",
            "summary": "Ethereum財団が人員整理...",
            "comment": "一時的には弱材料。構造改革中。"
        }
    ]

def generate_yaml(news_items):
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    yaml_text = 'date: "{}"\nnews:\n'.format(today)
    for item in news_items:
        yaml_text += '  - title: "{}"\n'.format(item['title'])
        yaml_text += '    url: "{}"\n'.format(item['url'])
        yaml_text += '    summary: "{}"\n'.format(item['summary'])
        yaml_text += '    comment: "{}"\n'.format(item['comment'])
    yaml_text += 'strategy: "全体的に様子見ムード。週末要注意。"\n'
    return yaml_text

def generate_html_with_yaml(yaml_content, output_path="output_html/news_embed.html"):
    html = """<!DOCTYPE html>
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
{}
  </div>
</body>
</html>
""".format(yaml_content)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

if __name__ == "__main__":
    news = fetch_news()
    yaml_text = generate_yaml(news)
    generate_html_with_yaml(yaml_text)
