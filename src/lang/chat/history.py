"""
SAIA: Chat History Page Module.

Version: 2024.08.04.01
"""

import streamlit as st


class History:
    """History Class."""

    def __init__(self) -> None:
        """Class Initialization."""
        st.subheader("对话历史")


if __name__ == "__page__":
    History()
