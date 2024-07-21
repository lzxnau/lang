"""
Smart Platform Project: icmd module.

User input from command line interface.

Version: 2024.07.17.01
"""

from datetime import datetime

from aioconsole import ainput
from lang.prod.lg import LG
from lang.prod.lm import EOM, OLM
from lang.prod.prompt import Prompt


class ICMD:
    """Class ICMD."""

    Prompt_Welcome: str = (
        "*: Change your smart AI assistant.\n"
        "#: The next question will be in the same context.\n"
        "@: The next question will be in a new context.\n"
        "^: Retrieve answers from a web link's domain and path.\n"
        "$: Quit.\n"
        "Please enter your question:\n"
    )
    Prompt_Assistant: str = (
        "1: L08, 2: P14, 3: G27, 4: L70\n"
        "Please select your assistant and enter the number accordingly:"
    )
    Prompt_Normal: str = "User(#:same/@:new context):\n"
    Prompt_Blank: str = ""

    Assistant_List: list[list[str]] = [
        ["L08", EOM.L08],
        ["P14", EOM.P14],
        ["G27", EOM.G27],
        ["L70", EOM.L70],
    ]

    def __init__(self):
        """Class initialization."""
        # Context ID
        self.cid = datetime.now().strftime("%Y%m%d%H%M%S")
        # Smart Assistant
        self.ass = OLM(
            self.Assistant_List[0][0],
            self.Assistant_List[0][1],
        )
        self.lg = LG(self.ass)

    async def input(self, size: int = 6) -> None:
        """Input method from user."""
        print(self.Prompt_Welcome)
        prompt = self.Prompt_Normal
        # concat message
        cmsg = ""
        while True:
            # Is new  context
            inc: bool = False
            # User input message
            uimsg = await ainput(prompt)
            uimsg = uimsg.strip()
            if uimsg == "$":
                break
            elif uimsg == "*":
                self.change_assistant()
            elif uimsg == "^":
                cmsg += Prompt.Search_Website
            elif uimsg in ["#", "@"] or len(uimsg) > size:
                match uimsg[:1]:
                    case "#":
                        pass
                    case "@":
                        inc = True
                    case _:
                        cmsg += uimsg + " "
                        prompt = ""
                        continue

                uimsg = uimsg[1:].strip()
                cmsg += uimsg
                if (inc and cmsg) or not inc:
                    self.lg.graph_proc(cmsg, self.cid)
                if inc:
                    datetime.now().strftime("%Y%m%d%H%M%S")
                prompt = self.Prompt_Normal
                cmsg = ""

    def change_assistant(self) -> None:
        """Change assistant."""
        # Smart assistant count
        count: int = len(self.Assistant_List) + 1
        uimsg = input(self.Prompt_Assistant).strip()
        for i in range(3):
            if uimsg.isdigit() and 0 < int(uimsg) < count:
                self.ass = OLM(
                    self.Assistant_List[int(uimsg) - 1][0],
                    self.Assistant_List[int(uimsg) - 1][1],
                )
                self.lg.change_llm(self.ass)
                break
            uimsg = input("Wrong format, please enter your number:").strip()
        print(f"Smart AI {self.ass.name} is your assistant.\n")
