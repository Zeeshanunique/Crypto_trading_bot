# agents/crypto_education_validator.py
from .agent_base import AgentBase

class CryptoEducationValidatorAgent(AgentBase):
    def __init__(self, max_retries=2, verbose=True):
        super().__init__(name="CryptoEducationValidatorAgent", max_retries=max_retries, verbose=verbose)

    def execute(self, topic, explanation):
        messages = [
            {"role": "system", "content": "You validate cryptocurrency educational explanations for accuracy and clarity."},
            {"role": "user", "content": (
                f"Topic:\n{topic}\n\n"
                f"Explanation Provided:\n{explanation}\n\n"
                "Validate whether the explanation is accurate, clear, and covers the topic effectively. "
                "Point out any inaccuracies or missing information."
            )}
        ]
        validation = self.call_openai(messages, max_tokens=300)
        return validation
