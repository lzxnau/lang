"""
Lang Chain Module.

Version: 2024.07.11.01
"""

from lang.util.decorators import Timer
from langchain_core.runnables.base import Runnable


class LC:
    """LC Class."""

    def __init__(self, query: str, chain: Runnable):
        """Class initialization."""
        self.query: str = query
        self.chain: Runnable = chain

    @Timer.fxn_run
    def stream_out(self) -> None:
        """Get lang chain stream output."""
        for chunk in self.chain.stream(self.query):
            print(chunk, end="", flush=True)
        print()
