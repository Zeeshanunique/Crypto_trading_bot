# agents/summarize_crypto_tool.py
from .agent_base import AgentBase

class SummarizeCryptoTool(AgentBase):
    def __init__(self, max_retries=3, verbose=True):
        super().__init__(name="SummarizeCryptoTool", max_retries=max_retries, verbose=verbose)

    def execute(self, text):
        messages = [
            {"role": "system", "content": "You are an AI assistant that summarizes cryptocurrency articles."},
            {"role": "user", "content": f"Summarize the following cryptocurrency article:\n\n{text}"}
        ]
        summary = self.call_openai(messages, max_tokens=300)
        return summary
