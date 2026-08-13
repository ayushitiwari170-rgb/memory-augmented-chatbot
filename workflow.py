from langgraph.graph import StateGraph, END
from typing import TypedDict
from memory import save_memory, get_memory
from rag import rag_answer
from graph import graph_answer
from tools import get_weather

class State(TypedDict):
    query: str
    response: str

USER = "Ayushi"

def memory_node(state: State):
    q = state["query"].lower()
    if "my favorite language is" in q:
        lang = state["query"].split("is")[-1].strip()
        save_memory(USER, "favorite_language", lang)
        state["response"] = f"Okay, I will remember that your favorite language is {lang}."
    elif "what is my favorite language" in q:
        mem = get_memory(USER)
        state["response"] = mem.get("favorite_language", "I do not know your favorite language yet.")
    return state

def tool_node(state: State):
    city = state["query"].split()[-1].strip("?.,!")
    state["response"] = get_weather(city)
    return state

def graph_node(state: State):
    g = graph_answer(state["query"])
    state["response"] = g
    return state

def rag_node(state: State):
    state["response"] = rag_answer(state["query"])
    return state

def route(state: State):
    q = state["query"].lower()
    if "favorite language" in q:
        return "memory"
    if "weather" in q:
        return "tool"
    if graph_answer(state["query"]):
        return "graph"
    return "rag"

workflow = StateGraph(State)
workflow.add_node("memory", memory_node)
workflow.add_node("tool", tool_node)
workflow.add_node("graph", graph_node)
workflow.add_node("rag", rag_node)

workflow.set_conditional_entry_point(route, {
    "memory": "memory",
    "tool": "tool",
    "graph": "graph",
    "rag": "rag"
})

for node in ["memory", "tool", "graph", "rag"]:
    workflow.add_edge(node, END)

app_graph = workflow.compile()

def route_query(query: str):
    result = app_graph.invoke({"query": query, "response": ""})
    return result["response"]