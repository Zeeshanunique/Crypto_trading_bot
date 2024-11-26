# agents/summarize_crypto_validator.py
from .agent_base import AgentBase

class SummarizeCryptoValidatorAgent(AgentBase):
    def __init__(self, max_retries=2, verbose=True):
        super().__init__(name="SummarizeCryptoValidatorAgent", max_retries=max_retries, verbose=verbose)

    def execute(self, original_text, summary):
        messages = [
            {"role": "system", "content": "You validate summaries of cryptocurrency articles."},
            {"role": "user", "content": (
                f"Original Text:\n{original_text}\n\n"
                f"Summary:\n{summary}\n\n"
                "Validate whether the summary accurately captures the main points."
            )}
        ]
        validation = self.call_openai(messages, max_tokens=300)
        return validation
