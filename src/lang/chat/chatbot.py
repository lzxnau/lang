"""
Chatbot Module.

Version: 2024.08.01.01
"""

from datetime import datetime

import streamlit as st
from lang.llms.info import Info
from lang.prod.lg import LG


class Chatbot:
    """Chatbot class."""

    def __init__(self) -> None:
        """Class Ini."""
        if "timestamp" not in st.session_state:
            st.session_state.timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        self.model = Info.Assistant_List[0]
        self.ass = Info.Model_List.get(self.model[0])
        self.lg = LG(self.ass)
        self.chat_page()

    def model_change(self) -> None:
        """Change model fxn."""
        key = st.session_state.model_key
        idx = [mode for mode in Info.Assistant_List if mode[0] == key]
        self.model = idx[0]
        self.ass = Info.Model_List.get(self.model[0])
        self.lg.change_llm(self.ass)

    @staticmethod
    def topic_save() -> None:
        """Save topic call back method."""
        st.session_state.sw_class = False

    def chat_submit(self) -> None:
        """Submit request."""
        if st.session_state.chat_input == "#":
            st.session_state.timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            st.session_state.messages = []
        elif (st.session_state.chat_input is None) or (
            st.session_state.sw_batch and st.session_state.chat_input != "@"
        ):
            if st.session_state.chat_input is not None:
                st.session_state.messages.append(
                    {"role": "human", "content": st.session_state.chat_input}
                )
            for msg in st.session_state.messages:
                st.chat_message(msg["role"]).write(msg["content"])
        else:
            if st.session_state.chat_input != "@":
                st.session_state.messages.append(
                    {"role": "human", "content": st.session_state.chat_input}
                )
            elif len(st.session_state.messages) == 0:
                return

            req_msg = [
                f"{m['role']}: {m['content']}"
                for m in st.session_state.messages
            ]
            if st.session_state.sw_class:
                act = True
            elif st.session_state.sw_save:
                act = False
            else:
                act = None

            out_msg = self.lg.graph_proc(
                "\n".join(req_msg),
                st.session_state.timestamp,
                act,
            )
            st.session_state.messages.append({"role": "ai", "content": out_msg})
            for msg in st.session_state.messages:
                st.chat_message(msg["role"]).write(msg["content"])

    def chat_page(self) -> None:
        """Show chat page."""
        if "model_key" not in st.session_state:
            st.session_state.model_key = self.model[0]
        if "sw_batch" not in st.session_state:
            st.session_state.sw_batch = False
        if "sw_save" not in st.session_state:
            st.session_state.sw_save = False
        if "sw_class" not in st.session_state:
            st.session_state.sw_class = False
        if "messages" not in st.session_state:
            st.session_state.messages = []

        st.radio(
            "选择你的AI秘书:",
            [ass[0] for ass in Info.Assistant_List],
            captions=[mode[1] for mode in Info.Assistant_List],
            key="model_key",
            horizontal=True,
        )
        self.model_change()
        st.subheader(f":blue[{st.session_state.model_key}] 现在为您服务")
        col1, col2, col3, _ = st.columns([1, 1, 1, 2])
        with col1:
            st.toggle("分段输入", key="sw_batch")
        with col2:
            st.toggle("归档对话", key="sw_save", on_change=Chatbot.topic_save)
        with col3:
            st.toggle(
                "主题分类",
                key="sw_class",
                disabled=not st.session_state.sw_save,
            )
        st.chat_input(key="chat_input")
        self.chat_submit()


if __name__ == "__main__":
    Chatbot()
