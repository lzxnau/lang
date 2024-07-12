"""
KnowledgeBase Module.

Version: 2024.07.10.01
"""

import bs4
from lang.util.decorators import Timer
from langchain import hub
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.documents import Document
from langchain_core.runnables import RunnablePassthrough
from langchain_core.runnables.base import Runnable
from langchain_huggingface import HuggingFaceEmbeddings


class KB:
    """KB Class."""

    def __init__(self, urls: list[str]):
        """Class initialization."""
        self.urls = urls

        # Embedding model
        self.em = "sentence-transformers/all-MiniLM-L6-v2"

    @Timer.fxn_run
    def get_chain(self) -> Runnable:
        """Get KnowledgeBase Chain."""
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
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=250, chunk_overlap=20
        )
        splits = splitter.split_documents(docs)
        embeddings = HuggingFaceEmbeddings(model_name=self.em)
        vectorstore = Chroma.from_documents(
            documents=splits,
            embedding=embeddings,
        )
        retriever = vectorstore.as_retriever()
        prompt = hub.pull("rlm/rag-prompt")
        chain = {
            "context": retriever | KB.format_docs,
            "question": RunnablePassthrough(),
        } | prompt

        return chain

    @staticmethod
    def format_docs(docs: list[Document]) -> str:
        """Format docs."""
        return "\n\n".join(doc.page_content for doc in docs)
