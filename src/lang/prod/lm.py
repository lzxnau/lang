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
    L008 = "llama3.1"  # 8k = 5.3GB, 128k = 56GB
    L070 = "llama3.1:70b"  # 8k = 47 GB

    # Microsoft
    P003 = "phi3:mini-128k"
    P014 = "phi3:medium-128k"  # context window 128k

    # Mistral and Nvidia
    M012 = "mistral-nemo"  # 8k = 7.8GB, 128k = 69GB
    M123 = "mistral-large:123b-instruct-2407-q2_K"

    # Google
    G009 = "gemma2"  # context window 8k
    G027 = "gemma2:27b"  # context window 8k


class OLM:  # ChatOllama local model
    """OLM Class."""

    def __init__(
        self,
        name: str,
        mn: str,
        form: str = "",
    ):
        """Class initialization."""
        temp: float = 0.1
        keep_alive: str = "-1m"  # 0 for stop
        num_thread: int = 16  # max 16
        num_ctx: int = 8192  # max 131072 for llama3.1 and mistral-nemo
        num_predict: int = 1024  # -1 for infinite

        # assistant name
        self.name = name

        # model name
        self.mn: str = mn

        # model temperature
        self.temp: float = temp

        # model format
        self.form: str = form

        # cpu cores: 16 cores in the system
        self.num_thread = num_thread

        # model keep alive time frame
        self.keep_alive = keep_alive

        # model context window: input token
        self.num_ctx = num_ctx
        # model generating text: output token
        self.num_predict = num_predict

        # llm model
        self.llm: ChatOllama = (
            ChatOllama(
                model=self.mn,
                temperature=self.temp,
                keep_alive=self.keep_alive,
                num_thread=self.num_thread,
                num_ctx=self.num_ctx,
                num_predict=self.num_predict,
            )
            if self.form == ""
            else ChatOllama(
                model=self.mn,
                format=self.form,
                temperature=self.temp,
                keep_alive=self.keep_alive,
                num_thread=self.num_thread,
                num_ctx=self.num_ctx,
                num_predict=self.num_predict,
            )
        )

    def get_chain(self) -> Runnable:
        """Get LLM model chain."""
        chain = self.llm | StrOutputParser()
        return chain

    def get_llm(self) -> ChatOllama:
        """Get Ollama local LLM model."""
        return self.llm
