import networkx as nx
import matplotlib.pyplot as plt

"""
Isomorphic trees are trees that have the same structure but different node labels.
"""

"""
Important notes:

Center of a tree:
- eccentricity of a node: maximum distance from that node to any other node in the tree.
- The center of a tree is the node with the smallest eccentricity.

Diameter of a tree: the maximum distance between any two nodes in the tree.

The center node is in the middle of diameter path.

There are two possibilities for the center of a tree:
1. The tree has one center. (diameter is odd)
2. The tree has two centers. (diameter is even)

After find the center nodes.

We can root the tree by the center nodes and use the AHU algorithm to get the canonical form of the tree.

AHU algorithm:
1. Root the tree at the center node.
2. Label the nodes in the tree by their degrees.
3. For each node, sort its children
4. Recursively apply the algorithm to each subtree rooted at the children of the node.
5. Concatenate the labels of the children in sorted order.

Proof: 
If two trees are isomorphs then their canonical forms are the same: 
https://math.stackexchange.com/questions/3282114/can-someone-explain-what-is-this-proof-of-ahu-algorithm-for-tree-isomorphism-mea

Time complexity: O(n log n)
Note: The AHU algorithm is not the most efficient algorithm for tree isomorphism.
The most efficient algorithm is the Weisfeiler-Lehman algorithm.
"""


"""
Tree (type) is a adjacency list representation of a tree.
"""


def are_isomorphic_trees(tree1, tree2):
    """
    Checks whether two trees are isomorphic.

    Parameters:
    tree1: The first tree.
    tree2: The second tree.

    Returns:
    bool: True if the trees are isomorphic, False otherwise.
    """
    if len(tree1) != len(tree2):
        return False

    centers1 = find_centers(tree1)
    centers2 = find_centers(tree2)

    if len(centers1) != len(centers2):
        return False

    return ahu_algorithm(tree1) == ahu_algorithm(tree2)


def ahu_dfs(tree, node, parent):
    """
    Depth-first search to encode the subtree rooted at 'node' into its canonical form using the AHU algorithm.

    Parameters:
    tree: The tree.
    node: The current node.
    parent: The parent of the current node.

    Returns:
    str: The canonical form encoding of the subtree.
    """
    labels = []
    for child in tree[node]:
        if child == parent:
            continue
        labels.append(ahu_dfs(tree, child, node))

    if labels:
        if len(set(labels)) < len(labels) / 2:
            count = {}
            for lab in labels:
                count[lab] = count.get(lab, 0) + 1
            sorted_labels = []
            for lab in sorted(count):
                sorted_labels.extend([lab] * count[lab])
        else:
            sorted_labels = sorted(labels)
    else:
        sorted_labels = labels

    return "(" + "".join(sorted_labels) + ")"


def ahu_algorithm(tree):
    """
    Applies the AHU algorithm to a tree.

    Parameters:
    tree: The tree.

    Returns:
    str: The canonical form of the tree.
    """
    centers = find_centers(tree)
    encodings = [ahu_dfs(tree, center, None) for center in centers]
    return min(encodings)


def find_centers(tree):
    """
    Finds the center nodes of a tree.

    Parameters:
    tree: The tree.

    Returns:
    list: The center nodes of the tree.
    """
    n = len(tree)
    leaves = list(node for node in tree if len(tree[node]) == 1)
    degrees = [len(tree[node]) for node in tree]

    while n > 2:
        n -= len(leaves)
        new_layer = []

        for node in leaves:
            for neighbor in tree[node]:
                degrees[neighbor] -= 1
                if degrees[neighbor] == 1:
                    new_layer.append(neighbor)
        leaves = new_layer

    return leaves


def adapter_nx_to_adj_list(graph: nx.Graph):
    """
    Converts a NetworkX graph to an adjacency list.

    Parameters:
    graph: The NetworkX graph.

    Returns:
    dict: The adjacency list representation of the graph.
    """
    adj_list = {node: [] for node in graph.nodes}
    for u, v in graph.edges:
        adj_list[u].append(v)
        adj_list[v].append(u)
    return adj_list


def test():
    # Test find_centers 1 center
    T = nx.random_tree(20, seed=13)
    nx.draw(T, with_labels=True)
    centers = find_centers(adapter_nx_to_adj_list(T))
    print(centers)
    print(nx.center(T))
    plt.show()

    # Test find_centers 2 centers
    T = nx.random_tree(20, seed=42)
    nx.draw(T, with_labels=True)
    centers = find_centers(adapter_nx_to_adj_list(T))
    print(centers)
    print(nx.center(T))
    plt.show()

    # Test are_isomorphic_trees
    T1 = nx.random_tree(20, seed=13)
    T2 = nx.random_tree(20, seed=13)
    print(are_isomorphic_trees(adapter_nx_to_adj_list(T1), adapter_nx_to_adj_list(T2)))
    print("NetworkX isomorphism check:", nx.is_isomorphic(T1, T2))

    T1 = nx.random_tree(20, seed=13)
    T2 = nx.random_tree(20, seed=42)
    print(are_isomorphic_trees(adapter_nx_to_adj_list(T1), adapter_nx_to_adj_list(T2)))
    print("NetworkX isomorphism check:", nx.is_isomorphic(T1, T2))


if __name__ == "__main__":
    test()


"""
AHU HASH 
"""

MOD = 10**9 + 7
BASE = 131


def ahu_hash_node(children):
    """
    Hashes the children of a node.

    Parameters:
    children: The children of the node.

    Returns:
    int: The hash of the children.
    """
    h = 1
    for ch in children:
        h = (h * BASE + ch) % MOD
    return (h * BASE + 7) % MOD


def ahu_dfs_hash(tree, node, parent):
    """
    Depth-first search to encode the subtree rooted at 'node' into its canonical integer form using the AHU algorithm.

    Parameters:
    tree: The tree.
    node: The current node.
    parent: The parent of the current node.

    Returns:
    int: The canonical integer encoding of the subtree.
    """
    children = []
    for child in tree[node]:
        if child == parent:
            continue
        children.append(ahu_dfs(tree, child, node))

    children.sort()
    return ahu_hash_node(children)
