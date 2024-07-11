"""
KnowledgeBase Module.

Version: 2024.07.10.01
"""

import bs4
from lang.util.decorators import Timer
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_huggingface import HuggingFaceEmbeddings


class KB:
    """KB Class."""

    def __init__(self, urls: list[str]):
        """Class initialization."""
        self.urls = urls

        # Embedding model
        self.em = "sentence-transformers/all-MiniLM-L6-v2"

    @Timer.fxn_run
    def get_retriever(self) -> VectorStoreRetriever:
        """Get retriever."""
        loader = WebBaseLoader(
            web_paths=self.urls,
            bs_kwargs=dict(
                parse_only=bs4.SoupStrainer(
                    class_=(
                        "post-content",
                        # "post-title",
                        # "post-header"
                    )
                )
            ),
        )
        docs = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=250, chunk_overlap=20
        )
        doc_splits = text_splitter.split_documents(docs)
        embeddings = HuggingFaceEmbeddings(model_name=self.em)
        vectorstore = Chroma.from_documents(
            documents=doc_splits,
            embedding=embeddings,
        )
        retriever = vectorstore.as_retriever()

        return retriever
