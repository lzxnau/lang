"""
Test Model.

Version: 2024.07.09.01
"""

import asyncio

from lang.imsg.icmd import ICMD


class Test:
    """Test Class."""

    def __init__(self):
        """Class initialization."""
        self.name = "Test"

    async def process(self) -> None:
        """Process function."""
        print(f"This is {self.name} class.\n")

        await self.test_icmd()

        await asyncio.sleep(0)

    async def test_icmd(self) -> None:
        """Test user command line input process."""
        icmd = ICMD()
        await icmd.input()


if __name__ == "__main__":
    t = Test()
    asyncio.run(t.process())
