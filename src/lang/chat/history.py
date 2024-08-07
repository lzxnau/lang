"""
SAIA: Chat History Page Module.

Version: 2024.08.04.01
"""

from pathlib import Path

import streamlit as st


class History:
    """History Class."""

    def __init__(self) -> None:
        """Class Initialization."""
        st.subheader("对话历史")

        path = Path("out/history")
        files = sorted(
            [file for file in path.iterdir() if file.is_file()],
            key=lambda x: x.stat().st_mtime,
            reverse=True,
        )

        date = ""
        for file in files:
            name = file.name
            name = name.split(".msg")[0]
            dt, ai, dura = name.split("-")
            dd = dt[:8]
            tt = dt[8:]
            if dd != date:
                date = dd
                tmp = date[:4] + "-" + date[4:6] + "-" + date[6:]
                st.subheader(tmp, divider=True)

            contents = file.read_text()
            idx = contents.index("\n")
            with st.expander(contents[:idx]):
                st.write(f"{contents[idx+1:]}")
                st.caption(
                    (
                        "<p style='text-align: right'>"
                        f"{tt[:2]}:{tt[2:4]}:{tt[4:]}  "
                        f"{ai}  {dura}  </p>"
                    ),
                    unsafe_allow_html=True,
                )


if __name__ == "__page__":
    History()
