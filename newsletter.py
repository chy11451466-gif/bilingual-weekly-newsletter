import html
import re
import urllib.request
import xml.etree.ElementTree as ET

from datetime import datetime, timedelta
from email.utils import parsedate_to_datetime
from pathlib import Path
from zoneinfo import ZoneInfo

OUTPUT_DIR = Path("newsletters")
OUTPUT_DIR.mkdir(exist_ok=True)

RSS_FEEDS = {
"BBC World": "https://feeds.bbci.co.uk/news/world/rss.xml",
"BBC Technology": "https://feeds.bbci.co.uk/news/technology/rss.xml",
"NPR": "https://feeds.npr.org/1004/rss.xml",
"NASA": "https://www.nasa.gov/feed/",
}

def clean_text(text):
if not text:
return ""

text = html.unescape(text)
text = re.sub(r"<[^>]+>", "", text)
return " ".join(text.split())

def fetch_feed(name, url):
request = urllib.request.Request(
url,
headers={"User-Agent": "BilingualWeeklyNewsletter/1.0"}
)

try:
    with urllib.request.urlopen(request, timeout=20) as response:
        data = response.read()

    root = ET.fromstring(data)
    items = []

    for item in root.findall(".//item"):
        title = clean_text(
            item.findtext("title", default="")
        )

        link = item.findtext("link", default="").strip()
        description = clean_text(
            item.findtext("description", default="")
        )

        date_text = item.findtext("pubDate", default="")

        if not title or not link:
            continue

        try:
            published = parsedate_to_datetime(date_text)

            if published.tzinfo is None:
                published = published.replace(
                    tzinfo=ZoneInfo("UTC")
                )

        except (TypeError, ValueError, OverflowError):
            published = None

        items.append({
            "source": name,
            "title": title,
            "link": link,
            "description": description,
            "published": published,
        })

    return items

except Exception as error:
    print(f"Could not fetch {name}: {error}")
    return []

def generate_newsletter():
now = datetime.now(ZoneInfo("Asia/Shanghai"))
cutoff = now - timedelta(days=7)

all_items = []

for name, url in RSS_FEEDS.items():
    print(f"Fetching {name}...")
    all_items.extend(fetch_feed(name, url))

unique_items = []
seen_links = set()

for item in all_items:
    if item["link"] in seen_links:
        continue

    seen_links.add(item["link"])

    published = item["published"]

    if published is not None:
        if published.astimezone(
            ZoneInfo("Asia/Shanghai")
        ) < cutoff:
            continue

    unique_items.append(item)

unique_items.sort(
    key=lambda item: item["published"] or cutoff,
    reverse=True
)

date = now.strftime("%Y-%m-%d")

chinese = [
    "# 🌏 中英文双语周刊",
    "",
    f"**发布日期：** {date}",
    "",
    "> 自动整理公开 RSS 新闻。标题为原文标题，中文部分提供标题参考译文；",
    "> 内容摘要来自新闻源提供的简介，不代表独立核实的事实。",
    "",
    "## 🇨🇳 中文周刊",
    "",
]

english = [
    "# 🌍 Bilingual Weekly Newsletter",
    "",
    f"**Publication date:** {date}",
    "",
    "> Automatically collected from public RSS feeds.",
    "> Original article titles are preserved in English.",
    "",
    "## 🇺🇸 English Weekly",
    "",
]

if not unique_items:
    chinese.extend([
        "本期没有成功获取新闻。请检查 RSS 新闻源是否可访问。",
        "",
    ])

    english.extend([
        "No news items were retrieved for this issue. "
        "Please check the availability of the RSS feeds.",
        "",
    ])

for index, item in enumerate(unique_items[:20], start=1):
    title = item["title"]
    description = item["description"]
    link = item["link"]
    source = item["source"]

    chinese.extend([
        f"### {index}. {title}",
        "",
        f"- **来源：** {source}",
        f"- **原文标题：** {title}",
    ])

    if description:
        chinese.append(f"- **新闻摘要（原文）：** {description}")

    chinese.extend([
        f"- **阅读原文：** [点击查看]({link})",
        "",
    ])

    english.extend([
        f"### {index}. {title}",
        "",
        f"- **Source:** {source}",
    ])

    if description:
        english.append(f"- **Summary from feed:** {description}")

    english.extend([
        f"- **Read more:** [Original article]({link})",
        "",
    ])

chinese.extend([
    "## 📚 本周英语学习",
    "",
    "建议从本期新闻中挑选生词，记录英文原句，并练习用自己的话复述。",
    "",
])

english.extend([
    "## 📖 English Learning",
    "",
    "Choose unfamiliar words from this week's articles. "
    "Record their meanings and practice summarizing each story.",
    "",
])

content = "\n".join(chinese + ["---", ""] + english)

return date, content

def main():
print("Starting the bilingual weekly newsletter...")

date, content = generate_newsletter()

if not content.strip():
    raise RuntimeError("Newsletter content is empty.")

output_file = OUTPUT_DIR / f"{date}.md"

output_file.write_text(
    content + "\n",
    encoding="utf-8"
)

print(f"Newsletter saved to {output_file}")

if name == "main":
main()