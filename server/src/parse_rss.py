import requests
import feedparser
from bs4 import BeautifulSoup

"""
:param article_url: The URL of the article to fetch and parse
:return: The main content of the article as a string, or an error message
"""


def get_article_content(article_url):
    # Make a GET request to fetch the article content

    response = requests.get(article_url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the page content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract the main content of the article (this will vary depending on the website)
        # Here we assume the main content is inside a <div> with a specific class, adjust as needed
        # only grab text from <p> tags

        # Extract and clean the text
        paragraphs = soup.find_all('p')
        print(paragraphs) # DEBUG
        article_text = '\n'.join([p.get_text(strip=True) for p in paragraphs])
        return article_text
    else:
        return f"Failed to retrieve the article. Status code: {response.status_code}"


"""
:param rss_url: The URL of the RSS feed to fetch
:param n: The number of articles to fetch

:return: A list of article headlines and a concatenated string of the article content
"""
def get_topn_articles(rss_url, n=5):
    # Fetch the RSS feed
    feed = feedparser.parse(rss_url)

    # Get the top 5 links and
    articles = []
    for entry in feed.entries:
        if len(articles) >= n:
            break
        if (get_article_content(entry.link)) == "Could not find the article body.": # TODO: this is not needed
            continue
        articles.append(get_article_content(entry.link))

    return "\n\n".join(articles) if articles else "No articles found."

def get_topn_headlines(rss_url, n=5):
    # Fetch the RSS feed
    feed = feedparser.parse(rss_url)
    
    headlines = []
    counter = 0
    for entry in feed.entries:
        if counter >= n:
            break
        counter += 1
        
        if len(headlines) >= n:
            break
        
        print("about to get article content")
        if (get_article_content(entry.link)) == "Could not find the article body.": # TODO: this is not needed
            continue
        headlines += [entry.title]

    return headlines


if __name__ == "__main__":
    # Fetch the RSS feed
    rss_url = 'https://www.cbsnews.com/latest/rss/moneywatch'
    print(get_topn_articles(rss_url))
    print(len(get_topn_headlines(rss_url)))
