import json
import vertexai
from vertexai.generative_models import GenerativeModel
import parse_rss

# Load the API key from the config file in your directory
# KEEP API FILE OUTSIDE OF REPO
configpath = '/home/alex/Documents/Personal Projects/Hackathon/API Key/calcium-petal-437012-u5-dc45b7195f9e.json'
with open(configpath, 'r') as f:
    config = json.load(f)
API_KEY = config

# Update with your actual project ID
PROJECT_ID = "calcium-petal-437012-u5"

# Initialize the Vertex AI
vertexai.init(project=PROJECT_ID, location="us-central1")

# Load the generative model
model = GenerativeModel(
    model_name = "gemini-1.5-flash-002",
    system_instruction = [
        "You are a news briefing assistant",
        "Your task is to take one or more articles as an input and generate a short daily news brief per article given that captures the main points of said article.",
        "Keep the summary short, around 3-4 sentences, and focus on the key information provided.",
        "The summary should be clear and presented in an informative and engaging tone for a morning briefing.",
        "Avoid including unnecessary details and focus on the main points of the articles. Do not say anything an AI would say. Only provide the summary",
        "Maintain a non-biased perspective and avoid introducing personal opinions or interpretations.",
        "Depending on the user's preference, the summary can be generated in English or another language."
    ]
)

# Generate the news brief
if __name__ == "__main__":
    content = parse_rss.get_top5_articles("https://www.cbsnews.com/latest/rss/politics")
    output = model.generate_content(content)
    print(output.text)