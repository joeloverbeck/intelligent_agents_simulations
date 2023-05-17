from anytree import Node, iterators


def calculate_number_of_nodes_in_tree(environment_tree: Node):
    """Calculates the number of nodes in a tree

    Args:
        environment_tree (Node): the environment tree whose number of nodes will be counted

    Returns:
        int: the number of nodes in the environment tree
    """
    return len(list(iterators.PreOrderIter(environment_tree)))
