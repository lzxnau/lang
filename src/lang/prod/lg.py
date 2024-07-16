"""
LangGraph Module.

Version: 2024.07.15.02
"""

import datetime
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
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages


class AgentState(TypedDict):
    """State between each agent/node."""

    messages: Annotated[Sequence[BaseMessage], add_messages]
    reid: str
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
        # request id
        self.reid: str | None = None
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
        if self.reid is None:
            self.reid = state["reid"]
        elif state["reid"] != self.reid:
            # A new reqeust just keeps last human message
            state["messages"] = [state["messages"][-1]]
            self.reid = state["reid"]
        else:
            print(state)
            state["messages"] = [
                msg
                for msg in state["messages"]
                if msg.additional_kwargs.get("reid") == self.reid
            ]

        print(state)
        result = self.agent.invoke(state)

        if isinstance(result, ToolMessage):
            pass
        else:
            result = AIMessage(
                **result.dict(exclude={"type", "name"}),
                name=self.name,
            )
            result.additional_kwargs["reid"] = self.reid
        return {
            "messages": [result],
            "reid": self.reid,
            "sender": self.name,
        }


class LG:
    """LG Class."""

    def __init__(self):
        """Class Initialization."""
        self.smartAN = LG.anode_smart()
        self.workflow = StateGraph(AgentState)
        self.graph_make()
        memory = SqliteSaver.from_conn_string(":memory:")

        self.graph = self.workflow.compile(checkpointer=memory)

    def process(self) -> None:
        """Process LangGraph workflow."""
        print("#: Last input for a request without changing session id.")
        print("@: Last input for a request with changing session id.")
        print("$: quit.")
        print("Please enter your question:\n")
        self.user_input()

    def user_input(self, size: int = 6) -> None:
        """User input."""
        # request id
        reid: str = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        req_msg = "User(finish a request with # or @):\n"
        inp_msg = req_msg
        msg = ""
        while True:
            gen_new: bool = False
            umsg = input(inp_msg)
            umsg = umsg.strip()
            if umsg == "$":
                break
            elif umsg in ["#", "@"] or len(umsg) > size:
                match umsg[:1]:
                    case "#":
                        pass
                    case "@":
                        gen_new = True
                    case _:
                        msg += umsg + " "
                        inp_msg = ""
                        continue

                umsg = umsg[1:].strip()
                msg += umsg
                if (gen_new and msg) or not gen_new:
                    self.graph_proc(msg, reid)
                if gen_new:
                    reid = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                inp_msg = req_msg
                msg = ""

    def graph_make(self) -> None:
        """Make LangGraph graph."""
        self.workflow.add_node(self.smartAN.name, self.smartAN.node)
        self.workflow.add_edge(START, self.smartAN.name)
        self.workflow.add_edge(self.smartAN.name, END)

    @Timer.fxn_run
    def graph_proc(
        self,
        umsg: str,  # user message
        reid: str,  # request id
    ) -> None:
        """
        Process LangGraph workflow.

        :param umsg: User message as input.
        :param reid: User request id.
        """
        config = {"configurable": {"thread_id": "2"}}
        print("\nSmart AI Response:")
        for event in self.graph.stream(
            {
                "messages": [
                    HumanMessage(
                        content=umsg, additional_kwargs={"reid": reid}
                    ),
                ],
                "reid": reid,
                "sender": "User",
            },
            config,
            stream_mode="values",
        ):
            msg = event["messages"][-1]
            if isinstance(msg, AIMessage):
                print("-" * 80)
                if isinstance(msg.content, str):
                    msg = msg.content.replace("\n\n", "\n")
                print(msg)
                print("-" * 80)

    @staticmethod
    def anode_smart() -> AgentNode:
        """Create  a smart agent node."""
        name = "SmartAgentNode"
        system_message = (
            "Answer users' questions directly and "
            "no prompts should be present before/after answering."
            "Each sentence in the response should be written on its own line."
        )
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a helpful AI assistant."
                    "Please provide a result with no more than three sentences."
                    "\n{system_message}",
                ),
                MessagesPlaceholder(variable_name="messages"),
            ]
        )
        return AgentNode(prompt, name=name, system_message=system_message)
