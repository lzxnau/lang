"""
SAIA - Models' Information Module.

Version: 2024.08.02.01
"""

from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.base import Runnable


class OLM:  # ChatOllama local model
    """OLM Class."""

    def __init__(
        self,
        name: str,
        model: str,
        load: str,
        **kwargs: str,
    ):
        """Class initialization."""
        # assistant name
        self.name = name

        # model name string
        self.model = model

        # load model when create
        self.load: bool = True if load == "True" else False

        # model output format
        self.form: str | None = kwargs.get("form", None)

        # model temperature
        self.temperature = float(kwargs.get("temperature", "0.1"))

        # model duration time
        self.keep_alive = kwargs.get("keep_alive", "1m")  # 0 for stop

        # model cpu numbers
        self.num_thread = int(kwargs.get("num_thread", "16"))  # max 16

        # model input context window
        # max 131072 for llama3.1 and mistral-nemo
        self.num_ctx = int(kwargs.get("num_ctx", "8192"))

        # model output inference token counts
        # -1 for infinite, -2 to match context window
        self.num_predict = int(kwargs.get("num_predict", "1024"))

        # llm model
        self.llm = ChatOllama(
            model=self.model,
            format=self.form,
            temperature=self.temperature,
            keep_alive=self.keep_alive,
            num_thread=self.num_thread,
            num_ctx=self.num_ctx,
            num_predict=self.num_predict,
        )

        if self.load:
            self.model_load()

    def model_change(self, **kwargs) -> None:
        """Change model."""
        self.form = kwargs.get("form", None)
        self.temperature = float(kwargs.get("temperature", "0.1"))
        self.keep_alive = kwargs.get("keep_alive", "1m")
        self.num_thread = int(kwargs.get("num_thread", "16"))
        self.num_ctx = int(kwargs.get("num_ctx", "8192"))
        self.num_predict = int(kwargs.get("num_predict", "1024"))
        self.llm = ChatOllama(
            model=self.model,
            format=self.form,
            temperature=self.temperature,
            keep_alive=self.keep_alive,
            num_thread=self.num_thread,
            num_ctx=self.num_ctx,
            num_predict=self.num_predict,
        )

    def model_load(self) -> None:
        """Load model."""
        self.llm.invoke("")

    def model_shut(self) -> None:
        """Shutdown model."""
        self.llm.invoke("", keep_alive="0")

    def get_chain(self) -> Runnable:
        """Get LLM model chain."""
        chain = self.llm | StrOutputParser()
        return chain

    def get_llm(self) -> ChatOllama:
        """Get Ollama local LLM model."""
        return self.llm


class Info:
    """Info Class."""

    Assistant_List = (
        ("小娜", "L008", "llama3.1", "False"),
        ("小季", "G009", "gemma2", "False"),
        ("小菲", "P003", "phi3:mini-128k", "False"),
        ("小米", "M012", "mistral-nemo", "False"),
        ("娜姐", "L070", "llama3.1:70b", "False"),
        ("季哥", "G027", "gemma2:27b", "False"),
        ("菲姐", "P014", "phi3:medium-128k", "False"),
        ("米哥", "M123", "mistral-large:123b-instruct-2407-q2_K", "False"),
    )

    Model_List: dict[str, OLM] = {
        ass[0]: OLM(ass[1], ass[2], ass[3]) for ass in Assistant_List
    }
