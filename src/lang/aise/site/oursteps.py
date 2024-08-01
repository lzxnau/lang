"""
Oursteps web site Module.

Version: 2024.07.31.01
"""

from selectolax.lexbor import LexborHTMLParser as HTMLParser


class OurSteps:
    """OurSteps Class."""

    Boards: list[str] = [
        "新闻汇总",
        "国际新闻",
    ]

    @staticmethod
    def list_boards(html: str) -> str:
        """List boards from the forum."""
        tree = HTMLParser(html)
        ref = "a[href^='forum.php?mod=forumdisplay&fid=']"
        nodes = tree.css(f"dt > {ref}, p > {ref}")
        urls: list[str] = []
        idx = 1
        print("Available boards:")
        for node in nodes:
            if node.text() in OurSteps.Boards:
                print(f"{idx}: {node.text()}")
                urls.append(node.attributes["href"])
                idx += 1
                if idx > len(OurSteps.Boards):
                    break
        sel = input("Select board:")
        if sel.isdigit() and 0 < int(sel) <= len(urls):
            return urls[int(sel) - 1]
        return ""

    @staticmethod
    def list_threads(html: str) -> str:
        """List threads from the board."""
        tree = HTMLParser(html)
        ref = "a[href^='forum.php?mod=viewthread']"
        nodes = tree.css(f"tbody > tr > th > {ref}")
        for i, node in enumerate(nodes):
            print(f"{i+1}: {node.text()}")
        return ""
