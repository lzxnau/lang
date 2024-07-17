"""
LangGraph Module.

Version: 2024.07.16.03
"""

from collections.abc import Callable, Sequence
from typing import Annotated, TypedDict

from lang.prod.lm import OLM
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
    coid: str  # context id
    sender: str


class AgentNode:
    """Agent Node Class."""

    def __init__(
        self,
        prompt: ChatPromptTemplate,
        llm: BaseChatModel,
        tools: list[Tool] | None = None,
        **kwargs: str,
    ):
        """Class initialization."""
        # name for the agent and node
        self.name: str = kwargs["name"]
        # context id
        self.coid: str | None = None
        self.prompt: ChatPromptTemplate = prompt
        self.prompt = self.prompt.partial(
            system_message=kwargs["system_message"]
        )
        self.tools: list[Tool] | None = tools
        if self.tools is not None:
            self.prompt = self.prompt.partial(
                tool_names=", ".join([tool.name for tool in self.tools])
            )

        self.agent: Runnable = self.prompt | (
            llm.bind_tools(self.tools) if self.tools is not None else llm
        )
        self.node: Callable[[AgentState], AgentState] = self.build_node

    def change_llm(self, olm: OLM) -> None:
        """Change agent llm."""
        llm = olm.get_llm()
        self.agent = self.prompt | (
            llm.bind_tools(self.tools) if self.tools is not None else llm
        )

    def build_node(self, state: AgentState) -> AgentState:
        """
        Build a LangGraph node.

        It is a function to run a specific task.
        """
        if self.coid is None:
            self.coid = state["coid"]
        elif state["coid"] != self.coid:
            # In a new context it keeps the last human message
            state["messages"] = [state["messages"][-1]]
            self.coid = state["coid"]
        else:
            # In an existing context, it keeps all messages
            # with the same context ID
            state["messages"] = [
                msg
                for msg in state["messages"]
                if msg.additional_kwargs.get("coid") == self.coid
            ]

        result = self.agent.invoke(state)

        if isinstance(result, ToolMessage):
            pass
        else:
            result = AIMessage(
                **result.dict(exclude={"type", "name"}),
                name=self.name,
            )
            result.additional_kwargs["coid"] = self.coid
        return {
            "messages": [result],
            "coid": self.coid,
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
        coid: str,  # context id
    ) -> None:
        """
        Process LangGraph workflow.

        :param umsg: User message as input.
        :param coid: User message context id.
        """
        config = RunnableConfig(configurable={"thread_id": "2"})
        print(f"\nSmart AI {self.olm.name}:")
        for event in self.graph.stream(
            {
                "messages": [
                    HumanMessage(
                        content=umsg, additional_kwargs={"coid": coid}
                    ),
                ],
                "coid": coid,
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

    def change_llm(self, olm: OLM) -> None:
        """Change llm model."""
        self.olm = olm
        self.smartAN.change_llm(olm)

    def anode_smart(self) -> AgentNode:
        """Create  a smart agent node."""
        name = "SmartAgentNode"
        system_message = (
            "Answer users' questions directly and "
            "no prompts should be present before or after answering."
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
        return AgentNode(
            prompt, self.olm.get_llm(), name=name, system_message=system_message
        )
