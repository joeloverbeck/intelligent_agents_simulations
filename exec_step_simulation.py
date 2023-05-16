from simulation import Simulation


def main():
    test_simulation = Simulation("fallout_shelter")

    test_simulation.initialize()

    test_simulation.step()


if __name__ == "__main__":
    main()
