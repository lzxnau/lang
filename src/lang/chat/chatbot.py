"""
Chatbot Module.

Version: 2024.08.05.02
"""

from datetime import datetime
from pathlib import Path

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
        elif st.session_state.chat_input is not None:
            Chatbot.chat_submit()
        else:
            Chatbot.msg_print()

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
            elif (
                len(st.session_state.messages) == 0
                or st.session_state.messages[-1]["role"] == "ai"
            ):
                return
            else:
                Chatbot.msg_print()

            req_msg = st.session_state.messages[-1]["content"]
            if st.session_state.sw_class:
                act = True
            elif st.session_state.sw_save:
                act = False
            else:
                act = None

            out_msg, rtime = st.session_state.lg.graph_proc(
                req_msg,
                st.session_state.timestamp,
                act,
            )

            out_msg = Chatbot.file_save(act, out_msg, rtime)

            st.session_state.messages.append(
                {
                    "role": "ai",
                    "content": out_msg,
                    "rtime": rtime,
                    "name": st.session_state.model_key,
                }
            )
            st.chat_message("ai").write(out_msg)
            st.caption(
                (
                    "<div style='text-align: right;"
                    "padding: 0 10px 20px 10px;'>"
                    "<p style='border: 1px solid grey; display: inline;"
                    "border-radius: 5px; padding: 2px;'>"
                    f"{st.session_state.model_key}: {rtime}</p></div>"
                ),
                unsafe_allow_html=True,
            )

    @staticmethod
    def file_save(act: bool | None, out_msg: str, rtime: str) -> str:
        """Save conversation file."""
        file = (
            f"/{st.session_state.timestamp}-"
            f"{st.session_state.model_key}-{rtime}.msg"
        )
        path = "out/{}"
        match act:
            case True:
                path = path.format("topics")
            case False:
                path = path.format("normal")
                out_msg, tags = out_msg.split("#### Tag List:")
                tags = "#### Tag List:" + tags
                tags_file = f"{path}/taglist.tag"
                try:
                    with open(tags_file, "w") as tf:
                        tf.write(tags)
                except FileNotFoundError as fe:
                    print(fe)
            case None:
                path = path.format("history")
        file = path + file
        try:
            # delete old conversation message with the same context
            for mfile in Path(path).iterdir():
                if mfile.name.startswith(f"{st.session_state.timestamp}-"):
                    mfile.unlink()
            # save the latest conversation message to disk
            with open(file, "w") as f:
                f.write(out_msg)
        except FileNotFoundError as fe:
            print(fe)

        return out_msg

    @staticmethod
    def msg_append() -> None:
        """Merge message fxn."""
        if any(msgs := st.session_state.messages) and (
            msgs[-1]["role"] == "user"
        ):
            msgs[-1]["content"] += "\n\n" + st.session_state.chat_input
            print(msgs[-1]["content"])
        else:
            st.session_state.messages.append(
                {"role": "user", "content": st.session_state.chat_input}
            )
        Chatbot.msg_print()

    @staticmethod
    def msg_print():
        """Print messages."""
        for msg in st.session_state.messages:
            st.chat_message(msg["role"]).write(msg["content"])
            if msg["role"] == "ai":
                st.caption(
                    (
                        "<div style='text-align: right;"
                        "padding: 0 10px 20px 10px;'>"
                        "<p style='border: 1px solid grey; display: inline;"
                        "border-radius: 5px; padding: 2px;'>"
                        f"{msg['name']}: {msg['rtime']}</p></div>"
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
