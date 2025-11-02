import openai
import requests
from bs4 import BeautifulSoup
import schedule
import time
from config import OPENAI_API_KEY, TRACK_TOPICS, OUTPUT_FILE

openai.api_key = OPENAI_API_KEY

def fetch_news(topic, num_articles=5):
    url = f"https://news.google.com/search?q={topic}&hl=en-US&gl=US&ceid=US:en"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    articles = []
    for item in soup.select("article")[:num_articles]:
        title_tag = item.select_one("h3")
        link_tag = item.select_one("a")
        if title_tag and link_tag:
            title = title_tag.get_text()
            link = "https://news.google.com" + link_tag["href"][1:]
            articles.append({"title": title, "link": link})
    return articles

def summarize_articles(articles):
    summaries = []
    for article in articles:
        prompt = f"Summarize this article in 2 sentences:\nTitle: {article['title']}\nLink: {article['link']}"
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role":"user","content":prompt}],
            max_tokens=100
        )
        summary = response.choices[0].message.content.strip()
        summaries.append(f"{article['title']}: {summary} ({article['link']})")
    return summaries

def run_agent():
    all_summaries = []
    for topic in TRACK_TOPICS:
        articles = fetch_news(topic)
        summaries = summarize_articles(articles)
        all_summaries.extend(summaries)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n\n".join(all_summaries))
    print(f"Weekly summary saved to {OUTPUT_FILE}")

# Example: schedule weekly
schedule.every().monday.at("08:00").do(run_agent)

if __name__ == "__main__":
    print("AI Monitoring Agent started...")
    while True:
        schedule.run_pending()
        time.sleep(60)