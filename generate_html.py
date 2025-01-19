import os
import feedparser
from jinja2 import Template

# 必要なディレクトリを作成
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

# RSSフィードのカテゴリ分け
RSS_FEEDS = {
    "ビジネス・国際": [
        {"name": "BBC News", "url": "https://news.yahoo.co.jp/rss/media/bbc/all.xml"},
        {"name": "Forbes JAPAN", "url": "https://news.yahoo.co.jp/rss/media/forbes/all.xml"},
        {"name": "日経ビジネス", "url": "https://news.yahoo.co.jp/rss/media/business/all.xml"},
    ],
    "食": [
        {"name": "食品新聞", "url": "https://news.yahoo.co.jp/rss/media/shokuhin/all.xml"},
        {"name": "食品産業新聞社", "url": "https://news.yahoo.co.jp/rss/media/ssnp/all.xml"},
        {"name": "日本食糧新聞", "url": "https://news.yahoo.co.jp/rss/media/nissyoku/all.xml"},
    ],
    "農業": [
        {"name": "日本農業新聞", "url": "https://news.yahoo.co.jp/rss/media/agrinews/all.xml"},
        {"name": "農水省", "url": "https://www.maff.go.jp/j/press/rss.xml"},
        {"name": "農研機構", "url": "https://www.naro.go.jp/PUBLICITY_REPORT/press/top_new_feed.xml"},
        {"name": "東京農工大学 研究", "url": "http://www.tuat.ac.jp/NEWS/research/rss.xml"},
        {"name": "農林水産技術会議", "url": "https://www.affrc.maff.go.jp/rss.xml"},
        {"name": "森林総合研究所", "url": "https://www.ffpri.affrc.go.jp/ffpri-chumokujoho.xml"},
    ],
    "宇宙": [
        {"name": "sorae 宇宙ニュース", "url": "https://news.yahoo.co.jp/rss/media/sorae_jp/all.xml"},
    ]
}

# ニュースデータをカテゴリごとに収集
all_news = {}

for category, feeds in RSS_FEEDS.items():
    all_news[category] = []
    for feed in feeds:
        rss_feed = feedparser.parse(feed["url"])
        for entry in rss_feed.entries[:5]:  # 各RSSフィードから最新5件を取得
            all_news[category].append({
                "source": feed["name"],
                "title": entry.title,
                "link": entry.link,
                "published": entry.get("published", "日付不明"),
            })

# HTMLテンプレート（カテゴリ分け＆多くの情報を表示）
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RSSニュースダッシュボード</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; line-height: 1.6; }
        h1 { color: #2c3e50; text-align: center; }
        .category { margin-bottom: 40px; }
        .news-container { display: flex; flex-wrap: wrap; gap: 20px; }
        .news-item {
            background: #f9f9f9;
            border-top: solid 1px #red;
            border-bottom: solid 1px #red;
            padding: 5px 10px;
        }
        .news-item h2 { font-size: .9em; color: #3498db; }
        .news-item p { margin: 5px 0; font-size: 0.8em; color: #666; }
        .source { font-size: 0.9em; color: #888; }
        a { color: #3498db; text-decoration: none; }
        a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <h1>RSSニュースダッシュボード</h1>
    {% for category, news_items in all_news.items() %}
        <div class="category">
            <h2>{{ category }}</h2>
            <div class="news-container">
                {% for news in news_items %}
                <div class="news-item">
                    <h2>{{ news.title }}</h2>
                    <p class="source">提供元: {{ news.source }}</p>
                    <p>公開日: {{ news.published }}</p>
                    <a href="{{ news.link }}" target="_blank">続きを読む</a>
                </div>
                {% endfor %}
            </div>
        </div>
    {% endfor %}
</body>
</html>
"""

# テンプレートをレンダリング
template = Template(HTML_TEMPLATE)
html_content = template.render(all_news=all_news)

# HTMLを保存
output_path = os.path.join(output_dir, "index.html")
with open(output_path, "w", encoding="utf-8") as file:
    file.write(html_content)

print(f"HTMLファイルを生成しました: {output_path}")
