knowledge_graph = {
    ("Python", "USED_IN"): "Artificial Intelligence",
    ("Machine Learning", "PART_OF"): "Artificial Intelligence",
    ("LangGraph", "USED_FOR"): "Workflow Orchestration"
}

def graph_answer(query):
    q = query.lower()

    if "python" in q and ("Python", "USED_IN") in knowledge_graph:
        return "Python is related to " + knowledge_graph[("Python", "USED_IN")]

    if "langgraph" in q:
        return "LangGraph is used for " + knowledge_graph[("LangGraph", "USED_FOR")]

    return None