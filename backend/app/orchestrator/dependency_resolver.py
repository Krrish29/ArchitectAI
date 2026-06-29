from collections import deque
from typing import Dict, Iterable, List, Set

DEPENDENCY_GRAPH: Dict[str, List[str]] = {
    "requirement": [],
    "architecture": ["requirement"],
    "database": ["requirement"],
    "api": ["requirement", "database"],
    "planner": ["requirement"],
}

VALID_AGENTS: List[str] = list(DEPENDENCY_GRAPH.keys())


def validate_agents(selected_agents: Iterable[str]) -> List[str]:
    if selected_agents is None:
        raise ValueError("selected_agents cannot be None")

    normalized = []
    for agent in selected_agents:
        if not isinstance(agent, str):
            continue
        candidate = agent.strip().lower()
        if candidate in VALID_AGENTS:
            normalized.append(candidate)

    if not normalized:
        raise ValueError("No valid agents provided")

    return list(dict.fromkeys(normalized))


def _collect_dependencies(selected_agents: Iterable[str]) -> Set[str]:
    selected = validate_agents(selected_agents)
    resolved: Set[str] = set()

    def visit(agent: str) -> None:
        if agent in resolved:
            return
        if agent not in DEPENDENCY_GRAPH:
            raise ValueError(f"Unknown agent '{agent}'")
        for dependency in DEPENDENCY_GRAPH[agent]:
            visit(dependency)
        resolved.add(agent)

    for agent in selected:
        visit(agent)

    return resolved


def topological_sort(nodes: Iterable[str]) -> List[str]:
    node_set = set(nodes)
    if not node_set:
        return []

    incoming: Dict[str, int] = {node: 0 for node in node_set}
    children: Dict[str, List[str]] = {node: [] for node in node_set}

    for node in node_set:
        for dependency in DEPENDENCY_GRAPH.get(node, []):
            if dependency in node_set:
                incoming[node] += 1
                children[dependency].append(node)

    queue = deque(
        [node for node in VALID_AGENTS if node in node_set and incoming[node] == 0]
    )
    ordered: List[str] = []

    while queue:
        node = queue.popleft()
        ordered.append(node)

        for child in children[node]:
            incoming[child] -= 1
            if incoming[child] == 0:
                queue.append(child)

    if len(ordered) != len(node_set):
        raise ValueError("Dependency graph contains a cycle or unresolved nodes")

    return ordered


def resolve_execution_plan(selected_agents: Iterable[str]) -> List[str]:
    node_set = _collect_dependencies(selected_agents)
    return topological_sort(node_set)
