"""
KnowledgeBase Module.

Version: 2024.07.10.01
"""

import bs4
from langchain_community.document_loaders import WebBaseLoader


class KB:
    """KB Class."""

    def __init__(self, urls: list[str]):
        """Class initialization."""
        self.urls = urls

    def get_retriever(self):
        """Get retriever."""
        loader = WebBaseLoader(
            web_paths=self.urls,
            bs_kwargs=dict(
                parse_only=bs4.SoupStrainer(
                    class_=("post-content", "post-title", "post-header")
                )
            ),
        )
        docs = loader.load()
        print(docs)
