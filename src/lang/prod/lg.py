"""
LangGraph Module.

Version: 2024.07.15.02
"""

import operator
from collections.abc import Callable, Sequence
from typing import Annotated, TypedDict

from lang.prod.lm import EOM, OLM
from lang.util.decorators import Timer
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    HumanMessage,
    ToolMessage,
)
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.base import Runnable
from langchain_core.tools import Tool
from langgraph.graph import END, START, StateGraph


class AgentState(TypedDict):
    """State between each agent/node."""

    messages: Annotated[Sequence[BaseMessage], operator.add]
    sender: str


class AgentNode:
    """Agent Node Class."""

    def __init__(
        self,
        prompt: ChatPromptTemplate,
        llm: BaseChatModel = OLM(EOM.L08).get_llm(),
        tools: list[Tool] | None = None,
        **kwargs: str,
    ):
        """Class initialization."""
        # name for the agent and node
        self.name: str = kwargs["name"]
        prompt = prompt.partial(system_message=kwargs["system_message"])
        if tools is not None:
            prompt = prompt.partial(
                tool_names=", ".join([tool.name for tool in tools])
            )

        self.agent: Runnable = prompt | (
            llm.bind_tools(tools) if tools is not None else llm
        )
        self.node: Callable[[AgentState], AgentState] = self.build_node

    def build_node(self, state: AgentState) -> AgentState:
        """
        Build a LangGraph node.

        It is a function to run a specific task.
        """
        result = self.agent.invoke(state)

        if isinstance(result, ToolMessage):
            pass
        else:
            result = AIMessage(
                **result.dict(exclude={"type", "name"}), name=self.name
            )

        return {
            "messages": [result],
            "sender": self.name,
        }


class LG:
    """LG Class."""

    def __init__(self):
        """Class Initialization."""
        self.smartAN = LG.anode_smart()
        self.workflow = StateGraph(AgentState)
        self.graph_make()
        self.graph = self.workflow.compile()

    def process(self) -> None:
        """Process LangGraph workflow."""
        print("Please enter your question or Q for quit.")
        self.user_input()

    def user_input(self, size: int = 4) -> None:
        """User input."""
        while True:
            umsg = input("User: ")
            umsg = umsg.strip()
            match umsg:
                case "Q":
                    break
                case umsg if len(umsg) > size:
                    self.graph_proc(umsg)
                    print()
                case _:
                    pass

    def graph_make(self) -> None:
        """Make LangGraph graph."""
        self.workflow.add_node(self.smartAN.name, self.smartAN.node)
        self.workflow.add_edge(START, self.smartAN.name)
        self.workflow.add_edge(self.smartAN.name, END)

    @Timer.fxn_run
    def graph_proc(self, umsg: str) -> None:
        """
        Process LangGraph workflow.

        :param umsg: User message as input.
        """
        events = self.graph.stream(
            {
                "messages": [HumanMessage(content=umsg)],
            },
            # Maximum number of steps to take in the graph
            {"recursion_limit": 150},
        )
        for s in events:
            print()
            print("Smart AI Response:")
            print(s[self.smartAN.name]["messages"][0].content)
            print()

    @staticmethod
    def anode_smart() -> AgentNode:
        """Create  a smart agent node."""
        name = "SmartAgentNode"
        system_message = (
            "You should provide accurate data to use."
            "Answer user question directly without any prompt in front."
            "Join each sentence with new line."
        )
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a helpful AI assistant."
                    "Please provide maximum three sentences as result."
                    "\n{system_message}",
                ),
                MessagesPlaceholder(variable_name="messages"),
            ]
        )
        return AgentNode(prompt, name=name, system_message=system_message)
