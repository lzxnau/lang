"""
LangGraph Module.

Version: 2024.07.16.03
"""

from collections.abc import Callable, Sequence
from typing import Annotated, TypedDict

from lang.llms.info import OLM
from lang.prod.prompt import Prompt
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
from langchain_core.runnables.config import RunnableConfig
from langchain_core.tools import Tool
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages


class AgentState(TypedDict):
    """State between each agent/node."""

    messages: Annotated[Sequence[BaseMessage], add_messages]
    cid: str  # context id
    sender: str


class AgentNode:
    """Agent Node Class."""

    def __init__(
        self,
        name: str,
        prompt: ChatPromptTemplate,
        llm: BaseChatModel,
        tools: list[Tool] | None = None,
    ):
        """Class initialization."""
        # name of the agent node
        self.name: str = name
        # context id
        self.cid: str | None = None
        self.prompt: ChatPromptTemplate = prompt
        self.llm: BaseChatModel = llm
        self.tools: list[Tool] | None = tools
        if self.tools is not None:
            self.prompt = self.prompt.partial(
                tool_names=", ".join([tool.name for tool in self.tools])
            )

        self.agent: Runnable = self.prompt | (
            self.llm.bind_tools(self.tools)
            if self.tools is not None
            else self.llm
        )
        self.node: Callable[[AgentState], AgentState] = self.build_node

    def change_llm(self, llm: BaseChatModel) -> None:
        """Change agent llm."""
        self.llm = llm
        self.agent = self.prompt | (
            self.llm.bind_tools(self.tools)
            if self.tools is not None
            else self.llm
        )

    def build_node(self, state: AgentState) -> AgentState:
        """
        Build a LangGraph node.

        It is a function to run a specific task.
        """
        if self.cid is None:
            self.cid = state["cid"]
        elif state["cid"] != self.cid:
            # In a new context it keeps the last human message
            state["messages"] = [state["messages"][-1]]
            self.cid = state["cid"]
        else:
            # In an existing context, it keeps all messages
            # with the same context ID
            state["messages"] = [
                msg
                for msg in state["messages"]
                if msg.additional_kwargs.get("cid") == self.cid
            ]

        result = self.agent.invoke(state)

        if isinstance(result, ToolMessage):
            pass
        else:
            result = AIMessage(
                **result.dict(exclude={"type", "name"}),
                name=self.name,
            )
            result.additional_kwargs["cid"] = self.cid
        return {
            "messages": [result],
            "cid": self.cid,
            "sender": self.name,
        }


class LG:
    """LG Class."""

    def __init__(self, olm: OLM):
        """Class Initialization."""
        self.olm = olm
        self.smartAN = self.anode_smart()
        self.workflow = StateGraph(AgentState)
        self.graph_make()
        memory = SqliteSaver.from_conn_string(":memory:")
        self.graph = self.workflow.compile(checkpointer=memory)

    def graph_make(self) -> None:
        """Make LangGraph graph."""
        self.workflow.add_node(self.smartAN.name, self.smartAN.node)
        self.workflow.add_edge(START, self.smartAN.name)
        self.workflow.add_edge(self.smartAN.name, END)

    @Timer.fxn_run
    def graph_proc(
        self,
        umsg: str,  # user message
        cid: str,  # context id
        act: bool | None = None,  # action status
    ) -> str:
        """
        Process LangGraph workflow.

        :param umsg: User message as input.
        :param cid: User message context id.
        :param act:  Whether to save or classify the message.
        :return: The inference from LLM.
        """
        if act is not None and act:
            msg = ""
        else:
            msg = ""

        config = RunnableConfig(configurable={"thread_id": "2"})
        print(f"\nSmart AI {self.olm.name}:")
        for event in self.graph.stream(
            {
                "messages": [
                    HumanMessage(content=umsg, additional_kwargs={"cid": cid}),
                ],
                "cid": cid,
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

        if act is not None:
            if act:
                pass
            else:
                pass
        return msg

    def change_llm(self, olm: OLM) -> None:
        """Change llm model method."""
        self.olm = olm
        self.smartAN.change_llm(self.olm.get_llm())

    def anode_smart(self) -> AgentNode:
        """Create  a smart agent node."""
        name = "SmartAgentNode"
        # system message
        sysmsg = Prompt.System_Message
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", sysmsg),
                MessagesPlaceholder(variable_name="messages"),
            ]
        )
        return AgentNode(
            name,
            prompt,
            self.olm.get_llm(),
        )
