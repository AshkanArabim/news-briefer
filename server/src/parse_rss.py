import requests
import feedparser
from bs4 import BeautifulSoup


def get_article_content(article_url):
    # Make a GET request to fetch the article content
    response = requests.get(article_url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the page content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract the main content of the article (this will vary depending on the website)
        # Here we assume the main content is inside a <div> with a specific class, adjust as needed
        article_body = soup.find('section', class_='content__body')  # You need to inspect the HTML structure of the site
        # only grab text from <p> tags

        # Extract and clean the text
        if article_body:
            paragraphs = article_body.find_all('p')
            article_text = '\n'.join([p.get_text(strip=True) for p in paragraphs])
            return article_text
        else:
            return "Could not find the article body."
    else:
        return f"Failed to retrieve the article. Status code: {response.status_code}"


if __name__ == "__main__":
    # Fetch the RSS feed
    rss_url = 'https://www.cbsnews.com/latest/rss/main'
    feed = feedparser.parse(rss_url)
    # Get the first headline and its link
    for entry in feed.entries[:1]:  # Get just one article for demo
        article_url = entry.link
        print(article_url)
        print(f"Fetching article: {entry.title}")

        # Fetch and display the article content
        content = get_article_content(article_url)
        print(content)
