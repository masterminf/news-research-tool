
from langchain_core.prompts import PromptTemplate
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI 
from newsapi import NewsApiClient

# Load environment variables from .env file
load_dotenv()

# Get API keys from environment variables
openai_api_key = os.getenv('OPENAI_API_KEY')
newsapi_key = os.getenv('NEWSAPI_KEY')

# Initialize OpenAI model
llm = ChatOpenAI(
    api_key=openai_api_key,
    model="gpt-3.5-turbo",
    temperature=0.7
)

# Initialize NewsAPI client
newsapi = NewsApiClient(api_key=newsapi_key)

def get_news_articles(query):
    """
    Fetch news articles from NewsAPI based on the query
    """
    try:
        articles = newsapi.get_everything(
            q=query,
            language='en',
            sort_by='relevancy',
            page_size=5  # Get top 5 articles
        )
        return articles['articles']
    except Exception as e:
        print(f"Error fetching news: {e}")
        return []

def summarize_articles(articles):
    """
    Extract descriptions from articles
    """
    summaries = []
    for article in articles:
        if article.get('description'):
            summaries.append(article['description'])
    return ' '.join(summaries)

def get_summary(query):
    """
    Get news articles and their summaries
    """
    articles = get_news_articles(query)
    if not articles:
        return "No articles found for this query."
    summary = summarize_articles(articles)
    return summary

# Create prompt template for LLM
template = """
You are an AI assistant helping an equity research analyst. 

Query: {query}

News Article Summaries:
{summaries}

Please provide a concise, professional summary of the key insights from these news articles. 
Focus on the most important information relevant to equity research.

Summary:
"""

prompt = PromptTemplate(
    template=template,
    input_variables=['query', 'summaries']
)

def get_ai_summary(query, summaries):
    """
    Generate AI summary using the LLM directly (without LLMChain)
    """
    try:
        formatted_prompt = prompt.format(query=query, summaries=summaries)
        response = llm.invoke(formatted_prompt)
        return response.content
    except Exception as e:
        return f"Error generating summary: {e}"