from typing import TypedDict
from langgraph.graph import StateGraph, END

from agents.relevance_checker import RelevanceChecker
from agents.research_agent import ResearchAgent
from agents.verification_agent import VerificationAgent

class State(TypedDict, total=False):
    question: str
    retriever: object
    relevance: str
    answer: str
    context: str
    verification: dict
    attempts: int

class AgentWorkflow:
    def __init__(self):
        self.relevance = RelevanceChecker()
        self.research = ResearchAgent()
        self.verify = VerificationAgent()
        self.graph = self._build()

    def _build(self):
        g = StateGraph(State)
        g.add_node("relevance", self.check_relevance)
        g.add_node("research", self.research_step)
        g.add_node("verification", self.verify_step)

        g.set_entry_point("relevance")
        g.add_conditional_edges(
            "relevance",
            lambda s: "research" if s["relevance"] != "NO_MATCH" else "end",
            {"research": "research", "end": END},
        )
        g.add_edge("research", "verification")
        g.add_conditional_edges(
            "verification",
            lambda s: "end" if (
                s["verification"]["supported"] == "YES"
                or s.get("attempts", 0) >= 2
            ) else "research",
            {"research": "research", "end": END},
        )
        return g.compile()

    def check_relevance(self, state):
        return {
            **state,
            "relevance": self.relevance.check(
                state["question"], state["retriever"]
            ),
            "attempts": state.get("attempts", 0),
        }

    def research_step(self, state):
        result = self.research.generate(
            state["question"], state["retriever"]
        )
        return {
            **state,
            "answer": result["answer"],
            "context": result["context"],
        }

    def verify_step(self, state):
        verification = self.verify.verify(
            state["answer"], state["context"]
        )
        return {
            **state,
            "verification": verification,
            "attempts": state.get("attempts", 0) + 1,
        }

    def run(self, question, retriever):
        result = self.graph.invoke({
            "question": question,
            "retriever": retriever,
            "attempts": 0,
        })

        if result.get("relevance") == "NO_MATCH":
            return {
                "answer": "The uploaded documents do not contain enough information to answer this question.",
                "verification": "RELEVANCE: NO_MATCH",
            }

        v = result.get("verification", {})
        report = (
            f"**Supported:** {v.get('supported', 'NO')}\n\n"
            f"**Verification:** {v.get('raw', 'Unavailable')}"
        )

        return {
            "answer": result.get("answer", ""),
            "verification": report,
        }
