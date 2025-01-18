import os
import feedparser
from jinja2 import Template

# 必要なディレクトリを作成
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

# RSSフィードのURL
RSS_URL = "https://www.maff.go.jp/j/press/rss.xml"

# RSSフィードを取得
feed = feedparser.parse(RSS_URL)

# ニュースリストを作成
news_list = []
for entry in feed.entries[:5]:  # 最新5件
    news_list.append({
        "title": entry.title,
        "link": entry.link,
        "published": entry.get("published", "日付不明"),
    })

# HTMLテンプレート
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>農水省ニュース</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; line-height: 1.6; }
        h1 { color: #2c3e50; }
        .news-item { margin-bottom: 20px; padding: 10px; border-bottom: 1px solid #ddd; }
        a { color: #3498db; text-decoration: none; }
        a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <h1>農水省 最新ニュース</h1>
    <div id="news-container">
        {% for news in news_list %}
        <div class="news-item">
            <h2>{{ news.title }}</h2>
            <p>公開日: {{ news.published }}</p>
            <a href="{{ news.link }}" target="_blank">続きを読む</a>
        </div>
        {% endfor %}
    </div>
</body>
</html>
"""

# テンプレートをレンダリング
template = Template(HTML_TEMPLATE)
html_content = template.render(news_list=news_list)

# HTMLを保存
output_path = os.path.join(output_dir, "index.html")
with open(output_path, "w", encoding="utf-8") as file:
    file.write(html_content)

print(f"HTMLファイルを生成しました: {output_path}")
