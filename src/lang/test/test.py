"""
Test Model.

Version: 2024.07.09.01
"""

from src.lang.prod.kbs import KB


class Test:
    """Test Class."""

    def __init__(self):
        """Class initialization."""
        self.name = "Test"

    def process(self) -> None:
        """Process function."""
        print(f"This is {self.name} class.")

        urls = [
            "https://lilianweng.github.io/posts/2023-06-23-agent/",
            "https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/",
            "https://lilianweng.github.io/posts/2023-10-25-adv-attack-llm/",
        ]

        kb = KB(urls)
        kb.get_retriever()

    def test_lang(self) -> None:
        """Test Python Language function."""
        x = [[i, i + 2, i + 4] for i in range(5)]
        print(x)

        y = [itme for key in x for itme in key]
        print(y)


if __name__ == "__main__":
    t = Test()
    t.process()
