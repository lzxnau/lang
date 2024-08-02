"""
Chatbot Module.

Version: 2024.08.01.01
"""

from datetime import datetime

import streamlit as st

from lang.llms.info import Info
from lang.prod.lg import LG
from lang.prod.lm import OLM


class Chatbot:
    """Chatbot class."""

    def __init__(self) -> None:
        """Class Ini."""
        self.cid = datetime.now().strftime("%Y%m%d%H%M%S")
        self.model = Info.Assistant_List[0]
        self.ass = OLM(
            self.model[1],
            self.model[2],
        )
        self.lg = LG(self.ass)

        if "model_key" not in st.session_state:
            st.session_state.model_key = self.model[0]

        st.radio(
            "选择你的AI秘书:",
            [ass[0] for ass in Info.Assistant_List],
            captions=[mode[1] for mode in Info.Assistant_List],
            key="model_key",
            on_change=self.model_change,
            horizontal=True,
        )
        st.subheader(f":blue[{st.session_state.model_key}]现在为您服务.")
        self.chat_page()

    def model_change(self) -> None:
        """Change model fxn."""
        key = st.session_state.model_key
        idx = [mode for mode in Info.Assistant_List if mode[0] == key]
        self.model = idx[0]
        self.ass = OLM(
            self.model[1],
            self.model[2],
        )
        self.lg.change_llm(self.ass)

    def chat_page(self) -> None:
        """Show chat page."""
        prompt = st.chat_input(key=f"{self.model[1]}:input")
        msgs = f"msg:{self.model[1]}"
        if msgs not in st.session_state:
            st.session_state.msgs = [
                {"role": "assistant", "content": "How can I help you?"}
            ]
        for msg in st.session_state.msgs:
            st.chat_message(msg["role"]).write(msg["content"])

        if prompt:
            st.session_state.msgs.append({"role": "user", "content": prompt})
            st.chat_message("user").write(prompt)
            rmsg = self.lg.graph_proc(prompt, self.cid)
            st.session_state.msgs.append({"role": "assistant", "content": rmsg})
            st.chat_message("assistant").write(rmsg)


if __name__ == "__main__":
    Chatbot()
