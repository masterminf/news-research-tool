import streamlit as st
from langchain_config import get_ai_summary, get_summary, get_news_articles

# Set page configuration
st.set_page_config(
    page_title="News Research Tool",
    page_icon="📰",
    layout="wide"
)

# Title and description
st.title('📰 Equity Research News Tool')
st.markdown("""
This tool helps you research companies and topics by:
- Fetching the latest news articles
- Summarizing key insights using AI
- Providing equity research perspective
""")

st.divider()

# Input section
st.subheader("Enter Your Research Query")
query = st.text_input(
    'What would you like to research?',
    placeholder='e.g., Tesla earnings, Apple stock, tech industry trends',
    help='Enter a company name, stock symbol, or topic'
)

# Search button
if st.button('🔍 Get News Summary', type='primary'):
    if query:
        with st.spinner('Fetching and analyzing news articles...'):
            try:
                # Get article summaries
                summaries = get_summary(query)
                
                if summaries == "No articles found for this query.":
                    st.warning("⚠️ No articles found for this query. Try a different search term.")
                else:
                    # Get AI summary using the new function
                    response = get_ai_summary(query, summaries)
                    
                    # Display results
                    st.success('✅ Analysis Complete!')
                    st.subheader('📊 AI-Generated Summary')
                    st.write(response)
                    
                    # Show individual articles
                    st.divider()
                    st.subheader('📄 Source Articles')
                    articles = get_news_articles(query)
                    
                    for idx, article in enumerate(articles[:5], 1):
                        with st.expander(f"Article {idx}: {article['title']}"):
                            st.write(f"**Source:** {article['source']['name']}")
                            st.write(f"**Published:** {article['publishedAt'][:10]}")
                            st.write(f"**Description:** {article.get('description', 'No description available')}")
                            st.write(f"**[Read full article]({article['url']})**")
            
            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")
                st.info("Please check your API keys in the .env file")
    else:
        st.warning('⚠️ Please enter a query to search.')

# Sidebar with information
with st.sidebar:
    st.header("ℹ️ About")
    st.markdown("""
    This tool uses:
    - **NewsAPI** for fetching articles
    - **OpenAI GPT** for summarization
    - **LangChain** for orchestration
    - **Streamlit** for the interface
    """)
    
    st.divider()
    
    st.header("💡 Tips")
    st.markdown("""
    - Use specific company names for best results
    - Try stock symbols (e.g., AAPL, TSLA)
    - Search for industry trends
    - Look up recent earnings reports
    """)
    
    st.divider()
    
    st.caption("Built with ❤️ using LangChain & Streamlit")

    
    