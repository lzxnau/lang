# LangGraph

## Agent: State, Nodes and Edges

1. State: A shared data structure that represents the current snapshot of your application.
          It can be any Python type, but is typically a TypedDict or Pydantic BaseModel.
2. Nodes: Python functions that encode the logic of your agents. They receive the current State as input,
          perform some computation or side effect, and return an updated State.
3. Edges: Python functions that determine which Node to execute next based on the current State.
          They can be conditional branches or fixed transitions.
4. By composing Nodes and Edges, you can create complex, looping workflows that evolve the State over time.
5. Nodes and Edges are nothing more than Python functions. Nodes do the work. Edges tell what to do next.