from langgraph.graph import StateGraph, END
from backend.schemas import AuditState
from backend.agents.parser_agent import parser_node
from backend.agents.slither_agent import slither_node
from backend.agents.reviewer_agent import reviewer_node
from backend.agents.report_agent import report_node

def should_review(state: AuditState) -> str:
    """条件边：有漏洞才走 Reviewer，否则直接出报告"""
    detectors = state["slither_result"].get("results", {}).get("detectors", [])
    if detectors:
        return "reviewer"
    return "report"

def build_graph():
    builder = StateGraph(AuditState)
    
    builder.add_node("parser", parser_node)
    builder.add_node("slither", slither_node)
    builder.add_node("reviewer", reviewer_node)
    builder.add_node("report", report_node)
    
    builder.set_entry_point("parser")
    builder.add_edge("parser", "slither")
    builder.add_conditional_edges(
        "slither",
        should_review,
        {"reviewer": "reviewer", "report": "report"}
    )
    builder.add_edge("reviewer", "report")
    builder.add_edge("report", END)
    
    return builder.compile()

graph = build_graph()