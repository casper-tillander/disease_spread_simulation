import unittest
from unittest import mock
import random
from world import World
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
The classes in this file handles the testing of the disease simulation
"""

class TestDiseaseLogic(unittest.TestCase):

    """
    The _create_test_environment function creates a 5x5 world with 9 AI instances. AI instances are placed in a 3x3 grid
    centered in the world with a specific AI (AI1) in the center. The test_infection_spread function sets a random seed,
    creates the test environment, infects AI1, and updates the disease status of all AIs. The test checks if AI1 is
    sick and if all adjacent AIs are infected.

    The _create_test_environment_2 function is similar to _create_test_environment, but it creates a 5x5 world with 25 AI
    instances, using a spread type of 1. The AI instances are placed in every position of the world, except for the center.
    The test_infection_spread_2 function also sets a random seed, creates the test environment,
    infects AI1 (in the center), and updates the disease status of all AIs. The test checks if AI1 is sick and
    if all other AIs are infected.

    The seed is needed because of the randomly generated attributes that affect the susceptibility of an AI.
    """

    def create_test_environment(self, world_size=5):
        world = World(world_size, world_size)
        ais = [AI(name=f"AI{i}", spread_type=0, infection_chance=100, death_chance=0,
                  incubation_duration=3, recovery_duration=7, vaccination_rate=0)
               for i in range(1, 10)]
        brains = [SmartAI(ai) for ai in ais]
        for ai, brain in zip(ais, brains):
            ai.set_brain(brain)
        locations = [Coordinates(2, 2), Coordinates(1, 1), Coordinates(2, 1),
                     Coordinates(3, 1), Coordinates(1, 2), Coordinates(3, 2),
                     Coordinates(1, 3), Coordinates(2, 3), Coordinates(3, 3)]
        for ai, loc in zip(ais, locations):
            world.add_AI(ai, loc, facing=Direction.NORTH)
        return world, ais

    def test_infection_spread(self):
        random.seed(3)
        world, ais = self.create_test_environment()
        ais[0].get_sick()  # Infect AI1

        for ai in ais:
            ai.update_disease_status()

        # Check if the adjacent AIs got infected
        for i, ai in enumerate(ais):
            if i == 0:  # AI1 should be infected
                self.assertTrue(ai.is_sick())
            else:
                self.assertTrue(ai.is_infected())

    def create_test_environment_2(self, world_size=5):
        world = World(world_size, world_size)
        ais = [AI(name=f"AI{i}", spread_type=1, infection_chance=100, death_chance=0,
                  incubation_duration=3, recovery_duration=7, vaccination_rate=0)
               for i in range(1, 26)]
        brains = [SmartAI(ai) for ai in ais]
        for ai, brain in zip(ais, brains):
            ai.set_brain(brain)
        locations = [Coordinates(x, y) for x in range(world_size) for y in range(world_size) if (x, y) != (2, 2)]
        locations.insert(0, Coordinates(2, 2))
        for ai, loc in zip(ais, locations):
            world.add_AI(ai, loc, facing=Direction.NORTH)
        return world, ais

    def test_infection_spread_2(self):
        random.seed(11)
        world, ais = self.create_test_environment_2()
        ais[0].get_sick()  # Infect AI1

        for ai in ais:
            ai.update_disease_status()

        # Check if the adjacent AIs got infected
        for i, ai in enumerate(ais):
            if i == 0:  # AI1 should be infected
                self.assertTrue(ai.is_sick())
            else:
                self.assertTrue(ai.is_infected())

class TestDataStorage(unittest.TestCase):
    """
    The checks if the save_simulation_data method of the SimulationDataStorage class
    correctly saves the simulation data to a CSV file. The test uses the unittest module and the patch decorator from
    the unittest.mock module to mock the write_simulation_data method of the SimulationDataStorage class.
    The test creates a mock input data, calls the save_simulation_data method with the input data, and checks if
    the write_simulation_data method was called with the expected arguments. The test ensures that the method
    calculates the correct rates and writes the expected values to the CSV file.
    """
    @mock.patch('data_storage.SimulationDataStorage.write_simulation_data')
    def test_data_storage(self, mock_write_simulation_data):
        # Define mock input values for save_simulation_data method
        turn = 1
        dead_count = 2
        infected_count = 3
        recovered_count = 4
        vaccinated_count = 5
        cured_count = 6
        total_population = 100
        gender_count = {"male": 50, "female": 50}
        smoker_count = {"smoker": 20, "non-smoker": 80}
        pre_existing_conditions_count = {"yes": 30, "no": 70}
        lifestyle_count = {"active": 40, "sedentary": 30, "moderate": 30}

        # Create a SimulationDataStorage instance
        storage = SimulationDataStorage()

        # Call save_simulation_data method with mock input values
        storage.save_simulation_data(turn, dead_count, infected_count, recovered_count,
                                     vaccinated_count, cured_count, total_population,
                                     gender_count, smoker_count, pre_existing_conditions_count,
                                     lifestyle_count)

        # Check that the write_simulation_data method was called with the expected arguments
        expected_simulation_data = {
            "turn": turn,
            "dead_count": dead_count,
            "infected_count": infected_count,
            "recovered_count": recovered_count,
            "vaccinated_count": vaccinated_count,
            "cured_count": cured_count,
            "total_population": total_population,
            "rates": {
                "mortality_rate": dead_count / total_population,
                "infection_rate": infected_count / total_population,
                "recovery_rate": recovered_count / total_population,
                "vaccination_rate": vaccinated_count / total_population,
                "cured_rate": cured_count / total_population
            },
            "gender_count": gender_count,
            "smoker_count": smoker_count,
            "pre_existing_conditions_count": pre_existing_conditions_count,
            "lifestyle_count": lifestyle_count
        }
        mock_write_simulation_data.assert_called_once_with(expected_simulation_data)

class TestDoctors(unittest.TestCase):
    """
    This class tests the functions in the class Doctor
    """
    def setUp(self):
        self.world = World(10, 10)
        self.ai1 = AI(name="AI1", spread_type=0, infection_chance=100, death_chance=0,
                      incubation_duration=3, recovery_duration=7, vaccination_rate=0)
        self.ai2 = AI(name="AI2", spread_type=0, infection_chance=100, death_chance=0,
                      incubation_duration=3, recovery_duration=7, vaccination_rate=0)
        self.ai2.get_sick()  # Infect AI2
        self.world.add_AI(self.ai1, Coordinates(4, 4), facing=Direction.NORTH)
        self.world.add_AI(self.ai2, Coordinates(6, 6), facing=Direction.NORTH)
        self.doctors = Doctors(self.ai1)
        self.ai1.set_brain(self.doctors)

    def test_find_sick_AI(self):
        sick_AI = self.doctors.find_sick_AI()
        self.assertEqual(sick_AI, self.ai2)

    def test_distance_to(self):
        distance = self.doctors.distance_to(self.ai2)
        self.assertEqual(distance, 4)

    def test_determine_direction(self):
        current_location = self.ai1.get_location()
        sick_AI = self.doctors.find_sick_AI()
        direction = self.doctors.determine_direction(current_location, sick_AI)
        self.assertIn(direction, [Direction.EAST, Direction.SOUTH])

    def test_move_body(self):
        initial_location = self.ai1.get_location()
        self.doctors.move_body()
        new_location = self.ai1.get_location()
        self.assertNotEqual(initial_location, new_location)

    def test_cure_nearby_AI(self):
        self.ai1.move(Direction.EAST)
        self.ai1.move(Direction.EAST)
        self.ai1.move(Direction.SOUTH)
        self.ai1.move(Direction.SOUTH)
        self.doctors.cure_nearby_AI()
        self.assertFalse(self.ai2.is_sick())

class TestAvoidingAI(unittest.TestCase):
    """
    This class tests the functions in the class AvoidingAI
    """
    def setUp(self):
        self.world = World(10, 10)
        self.ai1 = AI(name="AI1", spread_type=0, infection_chance=100, death_chance=0,
                      incubation_duration=3, recovery_duration=7, vaccination_rate=0)
        self.ai2 = AI(name="AI2", spread_type=0, infection_chance=100, death_chance=0,
                      incubation_duration=3, recovery_duration=7, vaccination_rate=0)
        self.world.add_AI(self.ai1, Coordinates(4, 4), facing=Direction.NORTH)
        self.world.add_AI(self.ai2, Coordinates(6, 6), facing=Direction.NORTH)
        self.avoiding_ai = AvoidingAI(self.ai1)
        self.ai1.set_brain(self.avoiding_ai)

    def test_find_closest_AI(self):
        closest_AI = self.avoiding_ai.find_closest_AI()
        self.assertEqual(closest_AI, self.ai2)

    def test_determine_direction_away_from_AI(self):
        current_location = self.ai1.get_location()
        closest_AI = self.avoiding_ai.find_closest_AI()
        direction = self.avoiding_ai.determine_direction_away_from_AI(current_location, closest_AI)
        self.assertIn(direction, [Direction.WEST, Direction.NORTH])

    def test_move_body(self):
        initial_location = self.ai1.get_location()
        self.avoiding_ai.move_body()
        new_location = self.ai1.get_location()
        self.assertNotEqual(initial_location, new_location)

class TestSmartAI(unittest.TestCase):
    """
    This class tests the functions in the class SmartAI
    """
    def setUp(self):
        self.world = World(10, 10)
        self.ai1 = AI(name="AI1", spread_type=0, infection_chance=100, death_chance=0,
                      incubation_duration=3, recovery_duration=100, vaccination_rate=0)
        self.ai2 = AI(name="AI2", spread_type=0, infection_chance=100, death_chance=0,
                      incubation_duration=3, recovery_duration=100, vaccination_rate=0)
        self.world.add_AI(self.ai1, Coordinates(4, 4), facing=Direction.NORTH)
        self.world.add_AI(self.ai2, Coordinates(6, 6), facing=Direction.NORTH)
        self.smart_ai = SmartAI(self.ai1)
        self.ai1.set_brain(self.smart_ai)

    def test_find_healthy_AI(self):
        healthy_AI = self.smart_ai.find_healthy_AI()
        self.assertEqual(healthy_AI, self.ai2)

    def test_move_body(self):
        initial_location = self.ai1.get_location()
        self.smart_ai.move_body()
        new_location = self.ai1.get_location()
        self.assertNotEqual(initial_location, new_location)

    def test_move_to_quarantine(self):
        self.ai1.get_sick()
        for _ in range(50):
            self.smart_ai.move_to_quarantine()
        quarantine_square = self.world.get_square(Coordinates(0, 0))
        self.assertFalse(quarantine_square.is_empty())

    def test_determine_direction_to_AI(self):
        current_location = self.ai1.get_location()
        direction = self.smart_ai.determine_direction_to_AI(current_location, self.ai2)
        self.assertIn(direction, [Direction.EAST, Direction.SOUTH])

    def test_determine_direction_to_quarantine(self):
        current_location = self.ai1.get_location()
        direction = self.smart_ai.determine_direction_to_quarantine(current_location, Coordinates(0, 0))
        self.assertIn(direction, [Direction.WEST, Direction.NORTH])

    def test_is_target_AI_in_neighboring_square(self):
        self.ai1.move(Direction.EAST)
        self.ai1.move(Direction.SOUTH)
        result = self.smart_ai.is_target_AI_in_neighboring_square()
        self.assertTrue(result)

class TestVaccinator(unittest.TestCase):
    """
    This class tests the functions in the class Vaccinator
    """
    def setUp(self):
        self.world = World(10, 10)
        self.ai1 = AI(name="AI1", spread_type=0, infection_chance=100, death_chance=0,
                      incubation_duration=3, recovery_duration=100, vaccination_rate=0)
        self.ai2 = AI(name="AI2", spread_type=0, infection_chance=100, death_chance=0,
                      incubation_duration=3, recovery_duration=100, vaccination_rate=0)
        self.world.add_AI(self.ai1, Coordinates(4, 4), facing=Direction.NORTH)
        self.world.add_AI(self.ai2, Coordinates(6, 6), facing=Direction.NORTH)
        self.vaccinator = Vaccinator(self.ai1)
        self.ai1.set_brain(self.vaccinator)

    def test_move_body(self):
        initial_location = self.ai1.get_location()
        self.vaccinator.move_body()
        new_location = self.ai1.get_location()
        self.assertNotEqual(initial_location, new_location)

    def test_vaccinate_nearby_AI(self):
        self.ai1.move(Direction.EAST)
        self.ai1.move(Direction.SOUTH)
        self.vaccinator.vaccinate_nearby_AI()
        self.assertTrue(self.ai2.is_vaccinated())

class TestBuilder(unittest.TestCase):
    """
    This class tests the functions in the class Builder
    """
    def setUp(self):
        self.world = World(30, 30)
        self.ai = AI(name="AI1", spread_type=0, infection_chance=100, death_chance=0,
                     incubation_duration=3, recovery_duration=100, vaccination_rate=0)
        self.world.add_AI(self.ai, Coordinates(0, 0), facing=Direction.NORTH)
        self.builder = Builder(self.ai)
        self.ai.set_brain(self.builder)

    def test_move_body(self):
        initial_location = self.ai.get_location()
        self.builder.move_body()
        new_location = self.ai.get_location()
        self.assertNotEqual(initial_location, new_location)

    def test_build_wall_after_1000_turns(self):
        for _ in range(1000):
            self.builder.move_body()

        for x in range(30):  # Iterate through all x-coordinates on line 15
            wall_location = Coordinates(x, 15)
            wall_square = self.world.get_square(wall_location)
            self.assertTrue(wall_square.is_wall_square())


if __name__ == '__main__':
    unittest.main()
