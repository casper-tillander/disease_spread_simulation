import math
from direction import Direction
from coordinates import Coordinates
from AI_brain import AIbrain
import random

"""
The SmartAI class is a subclass of AIbrain, representing a type of AI that navigates through the world while
trying to avoid getting infected. The class primarily focuses on moving towards the direction with the least
risk of infection, considering the health status of neighboring AI agents, and making decisions accordingly.

When the AI gets sick, it quarantines in the corner of the world. When it is healthy, it moves around and meets
healthy AI. The AI only moves randomly if it is the only healthy AI left in the world.
"""

class SmartAI(AIbrain):
    def __init__(self, body):
        super(SmartAI, self).__init__(body)
        self.random = random.Random()
        self.target_AI = None

    def move_body(self):
        """
        Moves towards the direction with the least risk of infection, considering the health status of neighboring
        AI agents, and makes decisions accordingly. If the AI is sick, it quarantines in the corner of the world.
        """
        if self.body.is_sick():
            self.move_to_quarantine()
        else:
            if self.target_AI is None or self.is_target_AI_in_neighboring_square():
                self.target_AI = self.find_healthy_AI()

            if self.target_AI is not None:
                location = self.body.get_location()
                next_direction = self.determine_direction_to_AI(location, self.target_AI)
                if next_direction:
                    moved = self.body.move(next_direction)
                    if moved:
                        self.body.spin(next_direction)
            else:
                self.random_move()

    def is_target_AI_in_neighboring_square(self):
        """
        Checks if the target AI is in the neighboring square of the current AI.
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

                    if neighbor_square.get_AI() == self.target_AI:
                        return True
        return False

    def find_healthy_AI(self):
        """
        Finds a random healthy AI in the world that has not been vaccinated or infected.
        """
        healthy_AI = [ai for ai in self.body.world.AI if not ai.is_sick() and not ai.is_vaccinated()
                      and not ai.is_infected() and ai is not self.body]
        if not healthy_AI:
            return None
        return self.random.choice(healthy_AI)

    def move_to_quarantine(self):
        """
        Moves the AI to the corner of the world for quarantine.
        """
        location = self.body.get_location()

        # Choose a corner for quarantine
        quarantine_corner = Coordinates(0, 0)

        next_direction = self.determine_direction_to_quarantine(location, quarantine_corner)
        if next_direction:
            self.body.move(next_direction)
            self.body.spin(next_direction)

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

    def distance_to(self, other_AI):
        """
        Calculates the Manhattan distance to another AI
        """
        dx = self.body.get_location().get_x() - other_AI.get_location().get_x()
        dy = self.body.get_location().get_y() - other_AI.get_location().get_y()
        return abs(dx) + abs(dy)

    def determine_direction_to_AI(self, current_location, target_AI):
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

    def determine_direction_to_quarantine(self, current_location, target_location):
        """
        Determines the direction to move towards the quarantine corner.
        """
        if target_location is not None and current_location is not None:
            distance_x = target_location.get_x() - current_location.get_x()
            distance_y = target_location.get_y() - current_location.get_y()
            if math.fabs(distance_x) >= math.fabs(distance_y):
                if distance_x > 0:
                    return Direction.EAST
                elif distance_x < 0:
                    return Direction.WEST
            else:
                if distance_y > 0:
                    return Direction.SOUTH
                elif distance_y < 0:
                    return Direction.NORTH
        return None

