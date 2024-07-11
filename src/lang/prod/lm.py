"""
LM Module.

Version: 2024.07.11.01
"""

from langchain_community.chat_models import ChatOllama


class OLM:  # ChatOllama local model
    """OLM Class."""

    def __init__(self, mn: str, form: str = "", temp: float = 0.1):
        """Class initialization."""
        # model name
        self.mn: str = mn

        # model temperature
        self.temp: float = temp

        # model format
        self.form: str = form

        # llm model
        self.llm: ChatOllama = (
            ChatOllama(model=self.mn, temperature=self.temp)
            if self.form == ""
            else ChatOllama(
                model=self.mn, format=self.form, temperature=self.temp
            )
        )

    def get_model(self) -> ChatOllama:
        """Get LLM model."""
        return self.llm
