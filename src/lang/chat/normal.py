"""
SAIA: Normal Chats Page Module.

Version: 2024.08.07.02
"""

import math
from pathlib import Path

import streamlit as st
from lang.chat.utils import Utils


class Normal:
    """Normal Class."""

    def __init__(self) -> None:
        """Class Initialization."""
        if "base_path" not in st.session_state:
            st.session_state.base_path = Path("out")
        if "norm_path" not in st.session_state:
            st.session_state.norm_path = st.session_state.base_path / "normal"
        if "tags_file" not in st.session_state:
            st.session_state.tags_file = (
                st.session_state.norm_path / "taglist.tag"
            )
        if "tags_list" not in st.session_state:
            lines = st.session_state.tags_file.read_text(
                encoding="utf-8"
            ).strip()
            tags = lines.split("\n- ")[1:]
            st.session_state.tags_list = [t.strip() for t in tags]
        if "tags_stat" not in st.session_state:
            st.session_state.tags_stat = [False] * len(
                st.session_state.tags_list
            )
        if "docs_show" not in st.session_state:
            st.session_state.docs_show = []

        Normal.norm_page()

    @staticmethod
    def norm_page() -> None:
        """Show normal page fxn."""
        st.subheader("普通话题", divider=True)
        Normal.load_tags()
        st.button(":material/search:", key="norm_find", help="查询")
        st.subheader("话题列表", divider=True)
        Normal.find_tags()

    @staticmethod
    def load_tags() -> None:
        """Load tags fxn."""
        count = 4  # columns per row
        with st.expander("请选择标签:material/tag:"):
            tags = st.session_state.tags_list
            size = len(tags)
            for i in range(math.ceil(size / count)):
                cols = st.columns([1] * count)
                for j, col in enumerate(cols):
                    with cols[j % count]:
                        try:
                            tag = tags[i * count + j]
                        except IndexError:
                            return
                        cb_key = st.checkbox(tag, key=f"norm_{tag}", help="0")
                        st.session_state.tags_stat[i * count + j] = cb_key

    @staticmethod
    def find_tags() -> None:
        """Find tags' docs fxn."""
        if st.session_state.norm_find:
            st.session_state.docs_show = [
                name
                for i, name in enumerate(st.session_state.tags_list)
                if st.session_state.tags_stat[i]
            ]
        if not any(tags := st.session_state.docs_show):
            return

        for file in st.session_state.norm_path.glob("*.msg"):
            if file.is_file():
                contents = file.read_text()
                if all(f"\n- {tag}" in contents for tag in tags):
                    Utils.file_item(file)


if __name__ == "__page__":
    Normal()
