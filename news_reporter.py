import os
import datetime
import feedparser
import json

def load_sources(path='sources.json'):
    with open(path, encoding='utf-8') as f:
        return json.load(f)

def fetch_news(feeds, limit=20):
    news_list = []
    for x in feeds:
        url = x['url']
        d = feedparser.parse(url)
        for entry in d.entries:
            news_list.append({
                "title": str(entry.title).strip(),
                "summary": str(entry.get("summary", "") or "").strip(),
                "link": entry.link
            })
            if len(news_list) >= limit:
                break
        if len(news_list) >= limit:
            break
    return news_list[:limit]

def write_markdown(zh_news, en_news, path, date_str, chinese_sources, english_sources):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(f"# 每日科技资讯报告\n\n")
        f.write(f"**日期：{date_str}**\n\n")
        f.write("## 快捷入口  \n")
        f.write("- [✏️ 编辑采集源（sources.json）](https://github.com/zsxdgithub/DailyTechNewsReport/edit/main/sources.json)\n")
        f.write("- [🚀 立即采集（Actions页面）](https://github.com/zsxdgithub/DailyTechNewsReport/actions)\n\n")
        
        f.write("## 当前采集来源\n\n### 中文\n")
        for src in chinese_sources:
            name = src.get("name", src["url"])
            url = src["url"]
            f.write(f"- [{name}]({url})\n")
        f.write("\n### English\n")
        for src in english_sources:
            name = src.get("name", src["url"])
            url = src["url"]
            f.write(f"- [{name}]({url})\n")
        f.write("\n---\n\n")

        f.write("## 中文科技资讯\n\n")
        for i, news in enumerate(zh_news, 1):
            f.write(f"{i}. [{news['title']}]({news['link']})  \n{news['summary']}\n\n")
        f.write("\n---\n\n## English Tech News\n\n")
        for i, news in enumerate(en_news, 1):
            f.write(f"{i}. [{news['title']}]({news['link']})  \n{news['summary']}\n\n")

def generate_index(docs_dir):
    # 生成简易首页
    files = sorted([f for f in os.listdir(docs_dir) if f.endswith('.md') and f != 'index.md'], reverse=True)
    with open(os.path.join(docs_dir, "index.md"), "w", encoding="utf-8") as idx:
        idx.write("# 每日科技资讯汇总\n\n")
        # 快捷操作入口
        idx.write("## 快捷入口  \n")
        idx.write("- [✏️ 编辑采集源（sources.json）](https://github.com/zsxdgithub/DailyTechNewsReport/edit/main/sources.json)\n")
        idx.write("- [🚀 立即采集（Actions页面）](https://github.com/zsxdgithub/DailyTechNewsReport/actions)\n\n")
        if files:
            idx.write("## 日期归档\n\n")
            for f in files:
                date_str = f.replace('.md', '')
                idx.write(f"- [{date_str}](./{f})\n")
        else:
            idx.write("> 暂无记录\n")

def main():
    today = datetime.date.today()
    date_str = today.isoformat()
    docs_dir = 'docs'
    os.makedirs(docs_dir, exist_ok=True)
    file_path = os.path.join(docs_dir, f"{date_str}.md")

    sources = load_sources('sources.json')
    chinese_sources = sources.get('chinese', [])
    english_sources = sources.get('english', [])
    zh_news = fetch_news(chinese_sources, 20)
    en_news = fetch_news(english_sources, 20)

    write_markdown(zh_news, en_news, file_path, date_str, chinese_sources, english_sources)
    generate_index(docs_dir)

if __name__ == '__main__':
    main()
