"""
Test Model.

Version: 2024.07.09.01
"""

from lang.imsg.icmd import ICMD


class Test:
    """Test Class."""

    def __init__(self):
        """Class initialization."""
        self.name = "Test"

    def process(self) -> None:
        """Process function."""
        print(f"This is {self.name} class.\n")
        self.test_icmd()

    def test_icmd(self) -> None:
        """Test user command line input process."""
        ICMD()


if __name__ == "__main__":
    t = Test()
    t.process()
