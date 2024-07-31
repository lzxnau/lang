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

    # Meta
    L008 = "llama3.1"          # context window 128k
    L070 = "llama3.1:70b"      # context window 128k

    # Microsoft
    P003 = "phi3:mini-128k"    # context window 128k
    P014 = "phi3:medium-128k"  # context window 128k

    # Mistral and Nvidia
    M012 = "mistral-nemo"      # context window 128k
    M123 = "mistral-large"     # context window 128k

    # Google
    G009 = "gemma2"            # context window 8k
    G027 = "gemma2:27b"        # context window 8k


class OLM:  # ChatOllama local model
    """OLM Class."""

    def __init__(self, name: str, mn: str, form: str = "", temp: float = 0.1):
        """Class initialization."""
        # assistant name
        self.name = name

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
