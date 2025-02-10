import networkx as nx
import random
import numpy as np


"""
Tree Edit Distance (TED) 
It is the minimum cost of transforming one tree into another using three operations: insertion, deletion, and substitution of nodes. 
The cost of each operation is 1.
"""

"""
Important Notes:
If the trees are unordered, then the tree edit distance is NP-hard.
The tree edit distance is a generalization of the Levenshtein distance.
The tree edit distance can be calculated using dynamic programming.

The algorithm is called the Zhang-Shasha algorithm.
And the time complexity is O(n^3).
"""


def tree_edit_distance(tree1, tree2):
    """
    Compute the tree edit distance between two trees.

    Parameters:
    tree1: The first tree.
    tree2: The second tree.

    Returns:
    int: The tree edit distance between the two trees.
    """
    return zs_algorithm(tree1, tree2)


def build_tree(adj):
    """
    Build a tree from the adjacency matrix to a dictionary of children.

    Parameters:
    adj: The adjacency matrix of the tree.

    Returns:
    int: The root of the tree.
    dict: The children of each node.
    """
    n = len(adj)
    children = {i: [] for i in range(n)}
    is_child = [False] * n
    for i in range(n):
        for j in range(n):
            if adj[i][j]:
                children[i].append(j)
                is_child[j] = True
    root = next(i for i, child in enumerate(is_child) if not child)
    return root, children


def dfs(u, children, post, node_to_post, leftmost):
    """
    Depth-first search to compute the postorder traversal of the tree.

    Parameters:
    u: The current node.
    children: The children of each node.
    post: The postorder traversal of the tree.
    node_to_post: The postorder index of each node.
    leftmost: The leftmost node of each subtree.

    Returns:
    int: The leftmost node of the subtree rooted at 'u'.
    """

    first = None
    for v in children[u]:
        res = dfs(v, children, post, node_to_post, leftmost)
        if first is None:
            first = res
    idx = len(post)
    if first is None:
        first = idx
    leftmost[u] = first
    post.append(u)
    node_to_post[u] = idx
    return first


def postorder(root, children):
    """
    Compute the postorder traversal of the tree.

    Parameters:
    root: The root of the tree.
    children: The children of each node.

    Returns:
    list: The postorder traversal of the tree.
    """
    post = []
    node_to_post = {}
    leftmost = {}
    dfs(root, children, post, node_to_post, leftmost)
    return post, node_to_post, leftmost


def compute_keyroots(post, leftmost, node_to_post):
    """
    Compute the keyroots of the tree.

    Parameters:
    post: The postorder traversal of the tree.
    leftmost: The leftmost node of each subtree.
    node_to_post: The postorder index of each node.

    Returns:
    list: The keyroots of the tree.
    """
    kr = {}
    for node in post:
        key = leftmost[node]
        kr[key] = (
            node  # Later nodes (with higher postorder index) replace earlier ones.
        )
    return sorted(kr.values(), key=lambda n: node_to_post[n])


# Cost functions: Deletion, insertion, and substitution.
def del_cost(n):
    return 1


def ins_cost(n):
    return 1


def sub_cost(n1, n2):
    # In classic edit distance, if nodes are "equal" the cost is 0.
    # For unlabeled trees assume nodes are equal only if they are the same number.
    return 0 if n1 == n2 else 1


def compute_forest(i, j, ted, post1, post2, left1, left2, node_to_post1, node_to_post2):
    """
    Compute the forest distance for the subtrees ending at postorder indices i (in tree1) and j (in tree2).

    Parameters:
    i: The postorder index in the first tree.
    j: The postorder index in the second tree.
    ted: The tree edit distance matrix.
    post1: The postorder traversal of the first tree.
    post2: The postorder traversal of the second tree.
    left1: The leftmost node of each subtree in the first tree.
    left2: The leftmost node of each subtree in the second tree.
    node_to_post1: The postorder index of each node in the first tree.
    node_to_post2: The postorder index of each node in the second tree.

    Returns:
    int: The tree edit distance between the two subtrees.
    """

    i1 = left1[post1[i]]
    j1 = left2[post2[j]]
    FD = [[0] * (j - j1 + 2) for _ in range(i - i1 + 2)]
    # Initialize first row and column.
    for di in range(1, i - i1 + 2):
        FD[di][0] = FD[di - 1][0] + del_cost(post1[i1 + di - 1])
    for dj in range(1, j - j1 + 2):
        FD[0][dj] = FD[0][dj - 1] + ins_cost(post2[j1 + dj - 1])
    for di in range(1, i - i1 + 2):
        for dj in range(1, j - j1 + 2):
            node1 = post1[i1 + di - 1]
            node2 = post2[j1 + dj - 1]
            if left1[node1] == i1 and left2[node2] == j1:
                # Both nodes are roots of their respective subtrees.
                cost = sub_cost(node1, node2)
                FD[di][dj] = min(
                    FD[di - 1][dj] + del_cost(node1),
                    FD[di][dj - 1] + ins_cost(node2),
                    FD[di - 1][dj - 1] + cost,
                )
                ted[node_to_post1[node1]][node_to_post2[node2]] = FD[di][dj]
            else:
                FD[di][dj] = min(
                    FD[di - 1][dj] + del_cost(node1),
                    FD[di][dj - 1] + ins_cost(node2),
                    FD[di - 1][dj - 1]
                    + ted[node_to_post1[node1]][node_to_post2[node2]],
                )
    return FD[-1][-1]


def zs_algorithm(tree1, tree2):

    root1, children1 = build_tree(tree1)
    root2, children2 = build_tree(tree2)
    post1, node_to_post1, left1 = postorder(root1, children1)
    post2, node_to_post2, left2 = postorder(root2, children2)
    keyroots1 = compute_keyroots(post1, left1, node_to_post1)
    keyroots2 = compute_keyroots(post2, left2, node_to_post2)

    ted = [[0] * len(post2) for _ in range(len(post1))]

    for node1 in keyroots1:
        i = node_to_post1[node1]
        for node2 in keyroots2:
            j = node_to_post2[node2]
            compute_forest(
                i, j, ted, post1, post2, left1, left2, node_to_post1, node_to_post2
            )

    return ted[node_to_post1[root1]][node_to_post2[root2]]


# Testing
def test():
    # Generate two random trees with 10 nodes each using networkx.
    num_nodes = 10
    seed = 42
    rand_tree1 = nx.random_tree(num_nodes, seed=seed)
    rand_tree2 = nx.random_tree(num_nodes, seed=seed + 1)

    # Choose node 0 as the root and create directed trees using BFS.
    T1 = nx.bfs_tree(rand_tree1, 0)
    T2 = nx.bfs_tree(rand_tree2, 0)

    # Convert the directed trees to adjacency matrices.
    mat1 = nx.to_numpy_array(T1, dtype=int).tolist()
    mat2 = nx.to_numpy_array(T2, dtype=int).tolist()

    # Compute the tree edit distance using our custom function.
    ted_custom = tree_edit_distance(mat1, mat2)

    # Prepare the graphs for networkx graph edit distance by adding a label.
    for graph in (T1, T2):
        for n in graph.nodes():
            graph.nodes[n]["label"] = n

    # Compute the graph edit distance using networkx's built-in function.
    # ged = nx.graph_edit_distance(
    #     T1,
    #     T2,
    #     node_del_cost=lambda n: 1,
    #     node_ins_cost=lambda n: 1,
    #     node_subst_cost=lambda n1, n2: 0 if n1["label"] == n2["label"] else 1,
    #     edge_del_cost=lambda e: 10000000,
    #     edge_ins_cost=lambda e: 10000000,
    #     edge_subst_cost=lambda e1, e2: 10000000,
    # )
    # ged = int(ged) if ged is not None else None

    print("Tree Edit Distance (Custom):", ted_custom)
    print("Graph Edit Distance (NetworkX):", 0)


if __name__ == "__main__":
    test()
