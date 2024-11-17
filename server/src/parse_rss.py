import aiohttp
import asyncio
import feedparser
from bs4 import BeautifulSoup

"""
:param article_url: The URL of the article to fetch and parse
:return: The main content of the article as a string, or an error message
"""


async def get_article_content(article_url):
    # Make a GET request to fetch the article content
    
    # print('============ article url:', article_url) # DEBUG

    async with aiohttp.ClientSession() as session:
        async with session.get(article_url) as response:
            # Check if the request was successful
            if response.status == 200:
                # Parse the page content using BeautifulSoup
                content = await response.text()
                soup = BeautifulSoup(content, 'html.parser')

                # Extract the main content of the article (this will vary depending on the website)
                # Here we assume the main content is inside a <div> with a specific class, adjust as needed
                # only grab text from <p> tags

                # Extract and clean the text
                paragraphs = soup.find_all('p')
                # print(paragraphs) # DEBUG
                article_text = '\n'.join([p.get_text(strip=True) for p in paragraphs])
                return article_text
            else:
                # print(f"Failed to retrieve the article. Status code: {response.status}") # DEBUG
                return ""


# returns a LIST of article bodies
async def get_topn_articles(rss_url, n=5):
    # Fetch the RSS feed
    feed = feedparser.parse(rss_url)
    
    # print('==x=x=x=x============ feed:', feed) # DEBUG

    return await asyncio.gather(*[get_article_content(item["link"]) for item in feed.entries[:n]])

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
        
        # print("about to get article content") # DEBUG
        if (get_article_content(entry.link)) == "Could not find the article body.": # TODO: this is not needed
            continue
        headlines += [entry.title]

    return headlines


# DEBUG
# if __name__ == "__main__":
#     # Fetch the RSS feed
#     rss_url = 'https://www.cbsnews.com/latest/rss/moneywatch'
#     print(get_topn_articles(rss_url))
#     print(len(get_topn_headlines(rss_url)))
