from typing import Dict, Any, List
import networkx as nx
from backend.models.proof import ProofGraph, ProofStep


class ProofDAG:
    """Directed Acyclic Graph utility wrapper for proof trees."""

    def __init__(self, proof_graph: ProofGraph):
        self.proof_graph = proof_graph
        self.graph = nx.DiGraph()
        self._build_graph()

    def _build_graph(self):
        for step in self.proof_graph.steps:
            self.graph.add_node(
                step.id,
                statement=step.statement,
                type=step.type,
                depth=step.depth
            )
            for parent_id in step.from_steps:
                self.graph.add_edge(parent_id, step.id)

    def is_dag(self) -> bool:
        return nx.is_directed_acyclic_graph(self.graph)

    def get_ancestors(self, node_id: int) -> List[int]:
        return list(nx.ancestors(self.graph, node_id))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "nodes": [
                {"id": n, "label": d.get("statement"), "type": d.get("type"), "depth": d.get("depth")}
                for n, d in self.graph.nodes(data=True)
            ],
            "edges": [{"from": u, "to": v} for u, v in self.graph.edges()]
        }
