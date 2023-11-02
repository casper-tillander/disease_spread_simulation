import sys
import random
from PyQt6.QtWidgets import QApplication
from Input_page import InputWindow
from Stats_page import StatsWindow
from world import World
from GUI import GUI
from direction import Direction
from AI import AI
from coordinates import Coordinates
from doctors import Doctors
from vaccinator import Vaccinator
from smartAI import SmartAI
from avoidingAI import AvoidingAI
from data_storage import SimulationDataStorage
from builder import Builder

"""
This disease simulation project aims to provide a graphical representation of the spread of a disease within a confined
population, taking into account various factors such as infection rates, vaccination rates, and the behavior of
individuals.The simulation displays the interactions between different types of individuals in a grid-based environment,
providing a visual insight into how various factors influence the progression of a disease outbreak.

INSTRUCTIONS FOR USING THE SIMULATION
1. Ensure that the necessary dependencies (e.g., PyQt6) are installed.
2. Run the main.py script (this file) to start the simulation.
3. Input the desired parameters and click the "Submit" button to initiate the simulation.
4. Observe the simulation in the grid-based environment, and monitor the real-time status of individuals.
5. After the simulation ends, view the statistics in a separate window, providing insights into the disease's impact on
    the population. The statistics will also be saved to the file simulation_data.csv.
"""


def main():
    # Step 1: Display input page
    app = QApplication(sys.argv)
    input_window = InputWindow()
    input_window.show()

    # Step 2: Wait for user to fill in values and press submit

    app.exec()
    # If the user closes the window, the simulation closes without crashing
    if not input_window.is_submit_pressed():
        sys.exit()

    # Step 3: Retrieve input values
    num_smart_healthy, num_avoiding_healthy, num_smart_sick, num_avoiding_sick, num_doctors, \
    num_vaccinators, num_builders, spread_type, infection_chance, death_chance, incubation_duration, \
    recovery_duration, vaccination_rate = input_window.return_input()

    # Step 4: Create world object using input values
    test_world = World(30, 30)

    # Step 5: Add things to world

    for i in range(num_smart_healthy):
        while True:
            x = random.randint(0, 29)
            y = random.randint(0, 29)

            if test_world.squares[x][y].is_empty():
                location = Coordinates(x, y)
                body = AI('SmartAI_healthy', spread_type, infection_chance, death_chance, incubation_duration,
                          recovery_duration, vaccination_rate)
                brain = SmartAI(body)
                body.set_brain(brain)
                test_world.add_AI(body, location, Direction.EAST)
                break

    for i in range(num_smart_sick):
        while True:
            x = random.randint(0, 29)
            y = random.randint(0, 29)

            if test_world.squares[x][y].is_empty():
                location = Coordinates(x, y)
                body = AI('SmartAI_sick', spread_type, infection_chance, death_chance, incubation_duration,
                          recovery_duration, vaccination_rate)
                brain = SmartAI(body)
                body.set_brain(brain)
                body.get_sick()
                test_world.add_AI(body, location, Direction.EAST)
                break

    for i in range(num_avoiding_healthy):
        while True:
            x = random.randint(0, 29)
            y = random.randint(0, 29)

            if test_world.squares[x][y].is_empty():
                location = Coordinates(x, y)
                body = AI('AvoidingAI_healthy', spread_type, infection_chance, death_chance, incubation_duration,
                          recovery_duration, vaccination_rate, is_avoiding=True)
                brain = AvoidingAI(body)
                body.set_brain(brain)
                test_world.add_AI(body, location, Direction.EAST)
                break

    for i in range(num_avoiding_sick):
        while True:
            x = random.randint(0, 29)
            y = random.randint(0, 29)

            if test_world.squares[x][y].is_empty():
                location = Coordinates(x, y)
                body = AI('AvoidingAI_sick', spread_type, infection_chance, death_chance, incubation_duration,
                          recovery_duration, vaccination_rate, is_avoiding=True)
                brain = AvoidingAI(body)
                body.set_brain(brain)
                body.get_sick()
                test_world.add_AI(body, location, Direction.EAST)
                break

    for i in range(num_doctors):
        while True:
            x = random.randint(0, 29)
            y = random.randint(0, 29)

            if test_world.squares[x][y].is_empty():
                location = Coordinates(x, y)
                body = AI('Doctor', spread_type, infection_chance, death_chance, incubation_duration,
                          recovery_duration, vaccination_rate, is_doctor=True)
                brain = Doctors(body)
                body.set_brain(brain)
                test_world.add_AI(body, location, Direction.EAST)
                break

    for i in range(num_vaccinators):
        while True:
            x = random.randint(0, 29)
            y = random.randint(0, 29)

            if test_world.squares[x][y].is_empty():
                location = Coordinates(x, y)
                body = AI('Vaccinators', spread_type, infection_chance, death_chance, incubation_duration,
                          recovery_duration, vaccination_rate, is_vaccinator=True)
                brain = Vaccinator(body)
                body.set_brain(brain)
                test_world.add_AI(body, location, Direction.EAST)
                break

    for i in range(num_builders):
        while True:
            x = random.randint(0, 29)
            y = random.randint(0, 29)

            if test_world.squares[x][y].is_empty():
                location = Coordinates(x, y)
                body = AI('SmartAI_healthy', spread_type, infection_chance, death_chance, incubation_duration,
                          recovery_duration, vaccination_rate, is_builder=True)
                brain = Builder(body)
                body.set_brain(brain)
                test_world.add_AI(body, location, Direction.EAST)
                break

    # Step 6: Display simulation window
    gui = GUI(test_world, 20)
    gui.show()

    # Step 7: Start event loop
    app.exec()

    # Step 8: Read turn number from csv file
    turn = SimulationDataStorage.get_last_turn() + 1

    # Step 9: Calculate statistics
    dead_count = AI.dead_count
    infected_count = AI.infected_count
    recovered_count = AI.recovered_count
    vaccinated_count = AI.vaccinated_count
    cured_count = Doctors.cured_count
    total_population = num_smart_healthy + num_avoiding_healthy + num_smart_sick \
                       + num_avoiding_sick + num_doctors + num_vaccinators + num_builders

    mortality_rate = (dead_count / total_population)
    infection_rate = (infected_count / total_population)
    recovery_rate = (recovered_count / total_population)
    vaccination_rate = (vaccinated_count / total_population)
    cured_rate = (cured_count / total_population)

    gender_count = AI.gender_count
    smoker_count = AI.smoker_count
    pre_existing_conditions_count = AI.pre_existing_conditions_count
    lifestyle_count = AI.lifestyle_count

    # Step 10: Display statistics window
    stats_window = StatsWindow(gender_count, smoker_count, pre_existing_conditions_count, lifestyle_count,
                               mortality_rate, infection_rate, recovery_rate, vaccination_rate, cured_rate)
    stats_window.show()

    # Step 11: Store statistics in csv file
    data_storage = SimulationDataStorage()
    data_storage.save_simulation_data(turn, dead_count, infected_count, recovered_count, vaccinated_count,
                                      cured_count, total_population, gender_count, smoker_count,
                                      pre_existing_conditions_count, lifestyle_count)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
