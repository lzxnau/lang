"""
SAIA: Utils Module.

Version: 2024.08.07.02
"""

from pathlib import Path

import streamlit as st


class Utils:
    """Utils Class."""

    @staticmethod
    def file_item(file: Path, sw_dt: bool = True) -> None:
        """Show file expander fxn."""
        name = file.name
        name = name.split(".msg")[0]
        dt, ai, dura = name.split("-")
        dd = dt[:8]
        dd = dd[:4] + "-" + dd[4:6] + "-" + dd[6:]
        tt = dt[8:]
        tt = tt[:2] + ":" + tt[2:4] + ":" + tt[4:]
        if sw_dt:
            tt = dd + " " + tt
        contents = file.read_text()
        idx = contents.index("\n")
        with st.expander(contents[:idx]):
            st.write(f"{contents[idx + 1:]}")
            col1, col2 = st.columns([1] * 2, vertical_alignment="bottom")
            with col1:
                st.write("##### :material/markdown:")
            with col2:
                st.caption(f"{tt}  {ai}  {dura}")
