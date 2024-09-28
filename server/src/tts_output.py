import parse_rss
import goog_tts
from goog_llm import summarize_news
import vertexai
from vertexai.generative_models import GenerativeModel

if __name__ == "__main__":
    # Fetch the RSS feed
    rss_url = 'https://www.cbsnews.com/latest/rss/politics'
    summarized_output = summarize_news(parse_rss.get_topn_articles(rss_url))
	
    # Save the summarized output to a .txt file
    with open("summarized_output.txt", "w") as file:
        file.write(summarized_output)
	
	# Split the summarized output into individual articles
    articles = summarized_output.split("the next article is from")

	# Convert each article to audio
    first_article = True
    for article in articles:
        if article.strip():
            # Skip the first "the next article is from" in the list
            if not first_article and not article.startswith("The next article is from"):
                article = "The next article is from" + article
            first_article = False
            print(article)
            goog_tts.text_to_audio_stream("en-US-Studio-O", article)