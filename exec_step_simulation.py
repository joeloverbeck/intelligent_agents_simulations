import argparse

from simulation import Simulation


def main():
    parser = argparse.ArgumentParser(
        description="Executes a step of a particular simulation"
    )
    parser.add_argument("simulation_name", help="Name of the simulation that will run")

    args = parser.parse_args()

    if not args.simulation_name:
        print("Error: The name of the simulation cannot be empty")
        return None

    test_simulation = Simulation(args.simulation_name)

    test_simulation.initialize()

    test_simulation.step()


if __name__ == "__main__":
    main()
