"""
LM Module.

Version: 2024.07.11.01
"""

from enum import StrEnum

from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.base import Runnable


class EOM(StrEnum):
    """Enum of Ollama Local Model Names."""

    L08 = "llama3"
    P14 = "phi3:medium"
    G27 = "gemma2:27b"
    L70 = "llama3:70b"


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

    def get_chain(self) -> Runnable:
        """Get LLM model chain."""
        chain = self.llm | StrOutputParser()
        return chain

    def get_llm(self) -> ChatOllama:
        """Get Ollama local LLM model."""
        return self.llm
