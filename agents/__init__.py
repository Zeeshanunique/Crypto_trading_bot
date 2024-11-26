# agents/__init__.py
from agents.crypto_education_tool import CryptoEducationTool
from .chatbot_agent import ChatbotAgent
from .prediction_agent import PredictionAgent
from .summarize_crypto_tool import SummarizeCryptoTool
from .summarize_crypto_validator import SummarizeCryptoValidatorAgent

class AgentManager:
    def __init__(self, max_retries=2, verbose=True):
        self.agents = {
            "chatbot": ChatbotAgent(max_retries=max_retries, verbose=verbose),
            "predictor": PredictionAgent(max_retries=max_retries, verbose=verbose),
            "summarize": SummarizeCryptoTool(max_retries=max_retries, verbose=verbose),
            "summarize_validator": SummarizeCryptoValidatorAgent(max_retries=max_retries, verbose=verbose),
            "education_tool": CryptoEducationTool(max_retries=max_retries, verbose=verbose)
        }

    def get_agent(self, agent_name):
        agent = self.agents.get(agent_name)
        if not agent:
            raise ValueError(f"Agent '{agent_name}' not found.")
        return agent
