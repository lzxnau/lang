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
        """Class Initialization."""
        if "timestamp" not in st.session_state:
            st.session_state.timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

        if "model" not in st.session_state:
            st.session_state.model = Info.Assistant_List[0]
            st.session_state.ass = Info.Model_List.get(
                st.session_state.model[0]
            )
            st.session_state.lg = LG(st.session_state.ass)

        if "model_key" not in st.session_state:
            st.session_state.model_key = st.session_state.model[0]
        if "sw_batch" not in st.session_state:
            st.session_state.sw_batch = False
        if "sw_save" not in st.session_state:
            st.session_state.sw_save = False
        if "sw_class" not in st.session_state:
            st.session_state.sw_class = False
        if "messages" not in st.session_state:
            st.session_state.messages = []

        Chatbot.chat_page()

    @staticmethod
    def chat_page() -> None:
        """Show chat page fxn."""
        st.radio(
            "选择你的AI秘书:",
            [ass[0] for ass in Info.Assistant_List],
            captions=[mode[1] for mode in Info.Assistant_List],
            key="model_key",
            horizontal=True,
            on_change=Chatbot.model_change,
        )
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
        st.chat_message("ai").write(
            f":blue[{st.session_state.model_key}] 现在为您服务"
        )
        st.chat_input(key="chat_input")
        if st.session_state.chat_input == "#":
            st.session_state.timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            st.session_state.messages = []
        else:
            Chatbot.msg_print()
            if st.session_state.chat_input is not None:
                Chatbot.chat_submit()

    @staticmethod
    def model_change() -> None:
        """Change model fxn."""
        key = st.session_state.model_key
        idx = [mode for mode in Info.Assistant_List if mode[0] == key]
        st.session_state.model = idx[0]
        st.session_state.ass = Info.Model_List.get(key)
        st.session_state.lg.change_llm(st.session_state.ass)

    @staticmethod
    def topic_save() -> None:
        """Save topic call back method."""
        st.session_state.sw_class = False

    @staticmethod
    def chat_submit() -> None:
        """Submit request fxn."""
        if st.session_state.sw_batch and st.session_state.chat_input != "@":
            Chatbot.msg_append()
        else:
            if st.session_state.chat_input != "@":
                Chatbot.msg_append()
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

            out_msg, rtime = st.session_state.lg.graph_proc(
                "\n".join(req_msg),
                st.session_state.timestamp,
                act,
            )

            st.session_state.messages.append(
                {
                    "role": "ai",
                    "content": out_msg,
                    "rtime": rtime,
                }
            )
            st.chat_message("ai").write(out_msg)
            st.caption(
                f"<p style='text-align: right;'>耗时: {rtime}  </p>",
                unsafe_allow_html=True,
            )

    @staticmethod
    def msg_append():
        """Append message."""
        st.session_state.messages.append(
            {"role": "human", "content": st.session_state.chat_input}
        )
        st.chat_message("human").write(st.session_state.chat_input)

    @staticmethod
    def msg_print():
        """Print messages."""
        for msg in st.session_state.messages:
            st.chat_message(msg["role"]).write(msg["content"])
            if msg["role"] == "ai":
                st.caption(
                    (
                        "<p style='text-align: right;'>"
                        f"耗时: {msg['rtime']}  </p>"
                    ),
                    unsafe_allow_html=True,
                )


if __name__ == "__page__":
    Chatbot()

elif __name__ == "__main__":
    pages = {
        "智能AI秘书": [
            st.Page("chatbot.py", title="疑难解答"),
            st.Page("history.py", title="对话历史"),
            st.Page("normal.py", title="普通话题"),
            st.Page("topics.py", title="分类主题"),
        ],
    }
    pg = st.navigation(pages)
    pg.run()
