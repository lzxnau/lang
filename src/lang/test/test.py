"""
Test Model.

Version: 2024.07.09.01
"""

from lang.prod.kb import KB
from lang.prod.lc import LC
from lang.prod.lg import LG
from lang.prod.lm import EOM, OLM


class Test:
    """Test Class."""

    def __init__(self):
        """Class initialization."""
        self.name = "Test"

    def test_cfg_rag1(self) -> None:
        """Test config rag."""
        # Knowledgebase urls
        self.urls = [
            "https://lilianweng.github.io/posts/2023-06-23-agent/",
        ]

        # chat model name
        self.mn = EOM.L70

        # Query
        self.query = "What is Task Decomposition?"

        self.test_rag()

    def process(self) -> None:
        """Process function."""
        print(f"This is {self.name} class.\n")
        self.test_lg()

    def test_lg(self) -> None:
        """Test LangGraph process."""
        lg = LG()
        lg.process()

    def test_rag(self) -> None:
        """Test prod function."""
        kb = KB(self.urls)
        kb_chain = kb.get_chain()

        lm = OLM(self.mn)
        lm_chain = lm.get_chain()

        rag_chain = kb_chain | lm_chain
        lc = LC(self.query, rag_chain)
        lc.stream_out()

    def test_lang(self) -> None:
        """Test Python Language function."""
        x = [[i, i + 2, i + 4] for i in range(5)]
        print(x)

        y = [itme for key in x for itme in key]
        print(y)


if __name__ == "__main__":
    t = Test()
    t.process()
