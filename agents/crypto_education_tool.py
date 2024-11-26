# agents/crypto_education_tool.py
from .agent_base import AgentBase

class CryptoEducationTool(AgentBase):
    def __init__(self, max_retries=3, verbose=True):
        super().__init__(name="CryptoEducationTool", max_retries=max_retries, verbose=verbose)

    def execute(self, topic):
        messages = [
            {"role": "system", "content": "You are an AI assistant specializing in cryptocurrency education. Provide clear, concise explanations on crypto-related topics."},
            {"role": "user", "content": f"Explain the following topic in cryptocurrency:\n\n{topic}"}
        ]
        response = self.call_openai(messages, max_tokens=500)
        return response
