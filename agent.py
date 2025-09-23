import argparse
from langgraph.graph import StateGraph, END
from agentic_ai.llm_tool import generate_parser_code
from agentic_ai.check_tool import save_parser_code, run_test

# -----------------------------
# Agent State
# -----------------------------
class AgentState(dict):
    bank: str = None
    code: str = None
    error: str = None
    success: bool = False
    attempts: int = 0

# -----------------------------
# Nodes
# -----------------------------
def llm_generate(state: AgentState) -> AgentState:
    """Node: Ask LLM to generate parser code"""
    state["code"] = generate_parser_code(state["bank"], state.get("error"))
    return state

def save_code(state: AgentState) -> AgentState:
    """Node: Save parser code into custom_parser"""
    save_parser_code(state["bank"], state["code"])
    return state

def test_parser(state: AgentState) -> AgentState:
    """Node: Run pytest to check parser correctness"""
    success = run_test(state["bank"])
    state["success"] = success
    if not success:
        state["error"] = "Parser test failed"
    return state

def decide_next(state: AgentState) -> str:
    """Control logic: decide next node"""
    state["attempts"] += 1
    if state["success"]:
        print("[AGENT] ✅ Parser passed all tests")
        return END
    elif state["attempts"] >= 3:
        print("[AGENT] ❌ Failed after 3 attempts")
        return END
    else:
        print("[AGENT] 🔁 Retrying...")
        return "llm_generate"

# -----------------------------
# Build Graph
# -----------------------------
def build_graph():
    graph = StateGraph(AgentState)
    graph.add_node("llm_generate", llm_generate)
    graph.add_node("save_code", save_code)
    graph.add_node("test_parser", test_parser)

    graph.set_entry_point("llm_generate")
    graph.add_edge("llm_generate", "save_code")
    graph.add_edge("save_code", "test_parser")
    graph.add_conditional_edges("test_parser", decide_next)

    return graph.compile()

# -----------------------------
# CLI Entrypoint
# -----------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", required=True, help="Bank target (e.g. icici, sbi)")
    args = parser.parse_args()

    workflow = build_graph()
    initial_state = AgentState(bank=args.target,attempts=0, success=False)
    workflow.invoke(initial_state, config={"recursion_limit": 10})
