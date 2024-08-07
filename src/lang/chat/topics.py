"""
SAIA: Chat Topics Page Module.

Version: 2024.08.04.01
"""

from pathlib import Path

import streamlit as st


class Topics:
    """Topics Class."""

    def __init__(self) -> None:
        """Class Initialization."""
        if "base_path" not in st.session_state:
            st.session_state.base_path = Path("out")
        if "topi_path" not in st.session_state:
            st.session_state.topi_path = st.session_state.base_path / "topics"
            if not st.session_state.topi_path.exists():
                st.session_state.topi_path.mkdir()
        if "list_update" not in st.session_state:
            st.session_state.list_update = False
        if "topi_list" not in st.session_state or st.session_state.list_update:
            try:
                st.session_state.topi_list = [
                    f.name
                    for f in st.session_state.topi_path.iterdir()
                    if f.is_dir()
                ]
            except Exception:
                st.session_state.topi_list = []
            st.session_state.list_update = False
        if "vers_update" not in st.session_state:
            st.session_state.vers_update = False
        if "topi_vers" not in st.session_state or st.session_state.vers_update:
            st.session_state.topi_vers = []
            st.session_state.vers_update = False

        Topics.topi_page()

    @staticmethod
    def topi_page() -> None:
        """Show topics page fxn."""
        st.subheader("分类主题", divider=True)
        col1, col2, col3 = st.columns(3, vertical_alignment="bottom")
        with col1:
            st.selectbox("选择主题", st.session_state.topi_list)
        with col2:
            st.selectbox("主题版本", st.session_state.topi_vers)
        with col3:
            st.button(
                ":material/add:",
                key="topi_add",
                on_click=Topics.add_new,
                help="新建主题",
            )

    @staticmethod
    @st.dialog("新建主题")
    def add_new() -> None:
        """Add new topic failed fxn."""
        name = st.text_input("主题名称")
        save = st.button(":material/save:", help="保存")
        if save:
            name = name.strip()
            if name == "":
                st.write(":warning:主题名字不能为空")
            else:
                try:
                    path = st.session_state.topi_path / name
                    path.mkdir(exist_ok=False)
                    st.write(":ok_hand:主题创建成功")
                    st.session_state.list_update = True
                    st.rerun()
                except FileExistsError:
                    st.write(":warning:主题已经存在")
                except Exception:
                    st.write(":warning:主题名字格式错误")


if __name__ == "__page__":
    Topics()
