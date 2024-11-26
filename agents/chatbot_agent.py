# agents/chatbot_agent.py
import requests
from .agent_base import AgentBase
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
from bs4 import BeautifulSoup
import logging

# Configure logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

class ChatbotAgent(AgentBase):
    def __init__(self, max_retries=2, verbose=True):
        super().__init__(name="ChatbotAgent", max_retries=max_retries, verbose=verbose)
        self.llm = ChatOpenAI(
            model="gpt-4",
            max_tokens=500,
            streaming=True,
            temperature=0.7
        )
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        self.chain = LLMChain(
            llm=self.llm,
            prompt=PromptTemplate(
                input_variables=["chat_history", "human_input"],
                template="""You are a helpful cryptocurrency expert assistant. 
                Previous conversation:
                {chat_history}
                Human: {human_input}
                Assistant:"""
            ),
            memory=self.memory,
            verbose=verbose
        )

    def scrape_web(self, query):
        try:
            url = f"https://www.google.com/search?q={query}"
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            web_data = soup.get_text()
            return web_data[:1000]  # Limit to first 1000 characters
        except Exception as e:
            logger.error(f"Error scraping web data: {e}")
            return "No web data available."

    def fetch_news(self, query):
        try:
            url = f"https://newsapi.org/v2/everything?q={query}&apiKey=396be96b6f55440d86db6752e4b79a27"
            response = requests.get(url)
            response.raise_for_status()
            news_data = response.json()
            articles = news_data.get('articles', [])
            news_summary = "\n".join([article['title'] for article in articles[:5]])  # Limit to first 5 articles
            return news_summary
        except Exception as e:
            logger.error(f"Error fetching news data: {e}")
            return "No news data available."

    # def fetch_finance_data(self, query):
    #     try:
    #         url = f"https://financialmodelingprep.com/api/v3/quote/{query}?apikey=9glmKR6yJm8TrCOMEWv54f2fad8VsTfz"
    #         response = requests.get(url)
    #         response.raise_for_status()
    #         finance_data = response.json()
    #         if finance_data:
    #             return f"Price: {finance_data[0]['price']}, Change: {finance_data[0]['changesPercentage']}"
    #         return "No financial data available."
    #     except Exception as e:
    #         logger.error(f"Error fetching financial data: {e}")
    #         return "No financial data available."

    def execute(self, query):
        try:
            response = self.chain.run(human_input=query)
            return response
        except Exception as e:
            logger.error(f"Error executing ChatbotAgent: {e}")
            return "An error occurred while processing your request."
