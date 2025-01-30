import aoc.helpers as helpers
import networkx as nx


def update_passes(u: tuple[int, ...], pairs: list[tuple[int, int]]) -> bool:
    """Check if the update order u adheres to constraints in pairs.

    Args:
        u: A tuple containing an update's sequence of items.
        pairs: A list of ordered pairs (bef, aft) indicating before and after relationships.
    Returns:
        bool: True if the order adheres; otherwise, False.
    Example:
        update_passes((3, 1, 2), [(1, 2)]) => True
    """
    for bef, aft in pairs:
        try:
            befi, afti = u.index(bef), u.index(aft)
        except ValueError:
            # skip pairs not in the update
            continue
        if befi >= afti:
            return False
    return True


def assert_acyclic(edges: list[tuple[int, int]]) -> None:
    """Ensure given edges form an acyclic graph.
    Args:
        edges: List of directed graph edges.
    Raises:
        AssertionError: If the graph is cyclic.
    Example:
        assert_acyclic([(1, 2), (2, 3)])  # No error for acyclic
    """
    G = nx.DiGraph(edges)
    assert nx.is_directed_acyclic_graph(G)


def correct_update_order(
    update: tuple[int, ...], pairs: list[tuple[int, int]]
) -> list[int]:
    """Determine correct order of update nodes based on constraints.

    Args:
        update: Tuple representing the initial order of nodes.
        pairs: List of constraint pairs.
    Returns:
        list[int]: List of nodes reordered to satisfy constraints.
    Example:
        correct_update_order((3, 1, 2), [(1, 2)]) => [3, 1, 2]
    """
    nodes: set[int] = set(update)
    node_pairs: list[tuple[int, int]] = [
        p for p in pairs if p[0] in nodes and p[1] in nodes
    ]
    assert_acyclic(node_pairs)
    visit_order: list[int] = helpers.topo_sort(nodes, node_pairs)

    assert update_passes(visit_order, pairs)
    assert set(visit_order) == set(nodes)
    return visit_order


def run(input_file, part):
    sections: list[list[str]] = helpers.read_input_sections(input_file)

    pairs: list[tuple[int, int]] = [tuple(map(int, s.split("|"))) for s in sections[0]]
    updates: list[tuple[int, ...]] = [
        tuple(map(int, s.split(","))) for s in sections[1]
    ]

    total_for_passing: int = sum(
        u[len(u) // 2] for u in updates if update_passes(u, pairs)
    )
    print(f"{total_for_passing=}")

    total_for_not_passing: int = sum(
        correct_update_order(update, pairs)[len(update) // 2]
        for update in updates
        if not update_passes(update, pairs)
    )

    if part == 1:
        return total_for_passing
    else:
        return total_for_not_passing
