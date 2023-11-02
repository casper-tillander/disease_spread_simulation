import math
from direction import Direction
from coordinates import Coordinates
from AI_brain import AIbrain
import random

"""
The Vaccinator class is a subclass of AIbrain, representing a type of AI that navigates through the world and
vaccinates susceptible AI agents. The class primarily focuses on finding the closest susceptible AI, determining
the direction to move towards it, and vaccinating any susceptible AI in neighboring squares upon reaching the
target. If there are no susceptible AI in the world, the Vaccinator moves randomly.
"""

class Vaccinator(AIbrain):
    def __init__(self, body):
        super(Vaccinator, self).__init__(body)
        self.random = random.Random()

    def move_body(self):
        """
        Finds the closest healthy AI that has not been vaccinated or infected, determines the direction to
        move towards it, and vaccinates any healthy AI in neighboring squares upon reaching the target.
        If there are no healthy AI in the world, moves randomly.
        """
        healthy_AI = self.find_healthy_AI()
        if healthy_AI is not None:
            location = self.body.get_location()
            next_direction = self.determine_direction(location, healthy_AI)
            if next_direction:
                moved = self.body.move(next_direction)
                if moved:
                    self.body.spin(next_direction)
                    self.vaccinate_nearby_AI()
        else:
            self.random_move()

    def random_move(self):
        """
        Moves the AI randomly.
        """
        facing = self.body.get_facing()
        if self.body.move(self.get_random_direction()):
            facing = Direction.get_next_clockwise(facing)
            self.body.spin(facing)

    def get_random_direction(self):
        """
        Selects a random direction.
        """
        directions = Direction.get_values()
        return self.random.choice(directions)

    def find_healthy_AI(self):
        """
        Finds all healthy AI in the world that have not been vaccinated or infected,
        and returns the closest one to the current AI.
        """
        healthy_AI = [ai for ai in self.body.world.AI if not ai.is_sick() and not ai.is_vaccinated()
                      and not ai.is_infected() and ai is not self.body]
        if not healthy_AI:
            return None
        closest_AI = min(healthy_AI, key=lambda ai: self.distance_to(ai))
        return closest_AI

    def distance_to(self, other_AI):
        """
        Calculates the Manhattan distance to another AI
        """
        dx = self.body.get_location().get_x() - other_AI.get_location().get_x()
        dy = self.body.get_location().get_y() - other_AI.get_location().get_y()
        return abs(dx) + abs(dy)

    def determine_direction(self, current_location, target_AI):
        """
        Determines the direction to move towards the target AI.
        """
        target_location = target_AI.get_location()
        if target_location is not None and current_location is not None:
            distance_x = target_location.get_x() - current_location.get_x()
            distance_y = target_location.get_y() - current_location.get_y()
            if math.fabs(distance_x) >= math.fabs(distance_y):
                if distance_x > 1:
                    return Direction.EAST
                elif distance_x < -1:
                    return Direction.WEST
            else:
                if distance_y > 1:
                    return Direction.SOUTH
                elif distance_y < -1:
                    return Direction.NORTH
        return None

    def vaccinate_nearby_AI(self):
        """
        Vaccinates any healthy AI in the neighboring squares that have not been vaccinated or infected.
        """
        current_location = self.body.get_location()
        x, y = current_location.get_x(), current_location.get_y()

        for x_offset in range(-1, 2):
            for y_offset in range(-1, 2):
                if x_offset == 0 and y_offset == 0:
                    continue

                neighbor_x = x + x_offset
                neighbor_y = y + y_offset

                if 0 <= neighbor_x < self.body.world.get_width() and 0 <= neighbor_y < self.body.world.get_height():
                    neighbor_square = self.body.world.get_square(Coordinates(neighbor_x, neighbor_y))

                    if neighbor_square.get_AI() is not None and not neighbor_square.get_AI().is_sick() \
                            and not neighbor_square.get_AI().is_vaccinated() and not neighbor_square.get_AI().is_infected():
                        neighbor_square.get_AI().vaccinate()
