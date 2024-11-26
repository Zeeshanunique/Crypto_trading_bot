# agents/prediction_agent.py
from venv import logger
from .agent_base import AgentBase
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
import requests

class PredictionAgent(AgentBase):
    def __init__(self, max_retries=3, verbose=True, api_key="f82e28df-367a-45be-8ee1-3fbc718ef679"):
        super().__init__(name="PredictionAgent", max_retries=max_retries, verbose=verbose)
        self.llm = ChatOpenAI(model="gpt-4o", max_tokens=500)
        self.prompt_template = PromptTemplate(
            input_variables=["coin"],
            template="You are an expert in cryptocurrency price predictions. Predict the price trend for the cryptocurrency: {coin}"
        )
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt_template)
        self.api_key = api_key
        self.api_url = "https://rest.coinapi.io/v1/exchangerate/{}/USD"

    def get_current_price(self, coin):
        headers = {'X-CoinAPI-Key': self.api_key}
        response = requests.get(self.api_url.format(coin), headers=headers)
        response.raise_for_status()
        data = response.json()
        return data['rate']

    def execute(self, coin):
        try:
            price = self.get_current_price(coin)
            return f"The current price of {coin.upper()} is ${price:.2f}."
        except Exception as e:
            logger.error(f"[{self.name}] Error fetching price: {e}")
            return f"Failed to fetch the price for {coin.upper()}."
