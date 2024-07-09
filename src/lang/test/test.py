"""
Test Model.

Version: 2024.07.09.01
"""


class Test:
    """Test Class."""

    def __init__(self):
        """Class initialization."""
        self.name = "Test"

    def process(self) -> None:
        """Process function."""
        print(f"This is {self.name} class.")
        self.test_lang()

    def test_lang(self) -> None:
        """Test Python Language function."""
        x = [[i, i + 2, i + 4] for i in range(5)]
        print(x)

        y = [itme for key in x for itme in key]
        print(y)


if __name__ == '__main__':
    t = Test()
    t.process()
