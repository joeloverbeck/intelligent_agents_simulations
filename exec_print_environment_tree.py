import argparse

from environment import load_environment_tree_from_json

from anytree import Node, RenderTree


def main():
    parser = argparse.ArgumentParser(description="Prints the environment tree of a simulation")
    parser.add_argument(
        "simulation_name", help="Name of the simulation whose environment tree will be printed"
    )

    args = parser.parse_args()

    if not args.simulation_name:
        print("Error: The name of the simulation cannot be empty")
        return None

    environment_tree = load_environment_tree_from_json(args.simulation_name, None)

    for pre, _, node in RenderTree(environment_tree):
        print("%s%s" % (pre, node.name))


if __name__ == "__main__":
    main()
