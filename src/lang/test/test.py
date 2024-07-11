"""
Test Model.

Version: 2024.07.09.01
"""

import time

from lang.prod.kb import KB
from lang.prod.lm import OLM
from langchain import hub
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough


class Test:
    """Test Class."""

    def __init__(self):
        """Class initialization."""
        self.name = "Test"

    def process(self) -> None:
        """Process function."""
        print(f"This is {self.name} class.\n")
        self.test_prod()

    def test_prod(self) -> None:
        """Test prod function."""
        urls = [
            "https://lilianweng.github.io/posts/2023-06-23-agent/",
        ]

        kb = KB(urls)
        retriever = kb.get_retriever()

        prompt = hub.pull("rlm/rag-prompt")

        def format_docs(docs) -> str:
            """Format docs."""
            return "\n\n".join(doc.page_content for doc in docs)

        mn = "llama3"
        lm = OLM(mn)
        llm = lm.get_model()

        rag_chain = (
            {
                "context": retriever | format_docs,
                "question": RunnablePassthrough(),
            }
            | prompt
            | llm
            | StrOutputParser()
        )

        stime = time.time()
        for chunk in rag_chain.stream("What is Task Decomposition?"):
            print(chunk, end="", flush=True)

        etime = time.time()
        print(f"rag_chain took {etime - stime} seconds.")

    def test_lang(self) -> None:
        """Test Python Language function."""
        x = [[i, i + 2, i + 4] for i in range(5)]
        print(x)

        y = [itme for key in x for itme in key]
        print(y)


if __name__ == "__main__":
    t = Test()
    t.process()
