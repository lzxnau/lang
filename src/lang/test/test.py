"""
Test Model.

Version: 2024.07.09.01
"""

import time

from lang.prod.kb import KB
from lang.prod.lm import OLM
from langchain import hub
from langchain_core.output_parsers import StrOutputParser


class Test:
    """Test Class."""

    def __init__(self):
        """Class initialization."""
        self.name = "Test"

    def test_cfg_rag(self) -> None:
        """Test config rag."""
        # Knowledgebase urls
        self.urls = [
            "https://lilianweng.github.io/posts/2023-06-23-agent/",
        ]

        # chat model name
        self.mn = "llama3"

        self.test_prod()

    def process(self) -> None:
        """Process function."""
        print(f"This is {self.name} class.\n")
        self.test_cfg_rag()

    def test_prod(self) -> None:
        """Test prod function."""
        kb = KB(self.urls)
        kb_chain = kb.get_chain()

        prompt = hub.pull("rlm/rag-prompt")

        lm = OLM(self.mn)
        llm = lm.get_model()

        rag_chain = kb_chain | prompt | llm | StrOutputParser()

        stime = time.time()
        for chunk in rag_chain.stream("What is Task Decomposition?"):
            print(chunk, end="", flush=True)

        etime = time.time()
        print(f"\nrag_chain took {etime - stime} seconds.")

    def test_lang(self) -> None:
        """Test Python Language function."""
        x = [[i, i + 2, i + 4] for i in range(5)]
        print(x)

        y = [itme for key in x for itme in key]
        print(y)


if __name__ == "__main__":
    t = Test()
    t.process()
