from collections import deque


class TreeNode:
    def __init__(self, label, children=None):
        self.label = label
        self.children = children if children is not None else []


def check_subtree(t_node, s_node, memo):
    print(t_node.label, s_node.label)
    if (id(t_node), id(s_node)) in memo:
        return memo[(id(t_node), id(s_node))]

    if t_node.label != s_node.label:
        memo[(id(t_node), id(s_node))] = False
        return False

    s_children = s_node.children
    t_children = t_node.children

    if len(s_children) > len(t_children):
        memo[(id(t_node), id(s_node))] = False
        return False

    if not s_children:
        memo[(id(t_node), id(s_node))] = True
        return True
    graph = {}
    s_nodes = list(enumerate(s_children))
    t_indices = list(range(len(t_children)))

    for i, s_child in s_nodes:
        graph[i] = []
        for j in t_indices:
            t_child = t_children[j]
            if t_child.label == s_child.label:
                if check_subtree(t_child, s_child, memo):
                    graph[i].append(j)

    def hopcroft_karp():
        pair_u = {u: None for u in graph}
        pair_v = {v: None for v in t_indices}
        dist = {}

        def bfs():
            queue = deque()
            for u in graph:
                if pair_u[u] is None:
                    dist[u] = 0
                    queue.append(u)
                else:
                    dist[u] = float("inf")
            dist[None] = float("inf")
            while queue:
                u = queue.popleft()
                if u is not None:
                    for v in graph[u]:
                        if dist[pair_v[v]] == float("inf"):
                            dist[pair_v[v]] = dist[u] + 1
                            queue.append(pair_v[v])
            return dist[None] != float("inf")

        def dfs(u):
            if u is not None:
                for v in graph[u]:
                    if dist[pair_v[v]] == dist[u] + 1:
                        if dfs(pair_v[v]):
                            pair_u[u] = v
                            pair_v[v] = u
                            return True
                dist[u] = float("inf")
                return False
            return True

        result = 0
        while bfs():
            for u in graph:
                if pair_u[u] is None:
                    if dfs(u):
                        result += 1
        return result

    max_matching = hopcroft_karp()
    result = max_matching == len(s_children)
    memo[(id(t_node), id(s_node))] = result
    return result


def is_subtree_isomorphic(S, T):
    """
    Checks if tree T contains a subgraph that is isomorphic to tree S.
    """
    memo = {}
    queue = deque([T])
    while queue:
        current = queue.popleft()
        if current.label == S.label:
            if check_subtree(current, S, memo):
                return True
        queue.extend(current.children)
    return False


# Example
if __name__ == "__main__":
    # S
    # ├─ 2
    # │  ├─ 3
    # │  └─ 4
    S = TreeNode(2, [TreeNode(3), TreeNode(4)])

    # T
    # 1
    # ├─ 2 - 8
    # │  ├─ 3 - 7
    # │  └─ 4 ─ 6
    # └─ 5
    T = TreeNode(
        1,
        [
            TreeNode(
                2, [TreeNode(3, [TreeNode(7)]), TreeNode(4, [TreeNode(6)]), TreeNode(8)]
            ),
            TreeNode(5),
        ],
    )

    print(is_subtree_isomorphic(S, T))
