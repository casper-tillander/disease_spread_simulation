import math
from direction import Direction
from coordinates import Coordinates
from AI_brain import AIbrain
import random

"""
The Doctors class is a subclass of AIbrain, representing a type of AI that navigates through the world and cures
sick AI. The class primarily focuses on finding the closest sick AI, determining the direction to move towards it,
and curing any sick AI in neighboring squares upon reaching the target. If there are no sick AI in the world,
the Doctors move randomly.
"""

class Doctors(AIbrain):
    cured_count = 1
    def __init__(self, body):
        super(Doctors, self).__init__(body)
        self.random = random.Random()

    def move_body(self):
        """
        Finds the closest sick AI, determines the direction to move towards it,
        and cures any sick AI in neighboring squares upon reaching the target.
        If there are no sick AI in the world, moves randomly.
        """
        # Find the closest sick AI
        sick_AI = self.find_sick_AI()
        if sick_AI is not None:
            location = self.body.get_location()
            # Determine the direction to move towards the sick AI
            next_direction = self.determine_direction(location, sick_AI)
            if next_direction:
                moved = self.body.move(next_direction)
                if moved:
                    # Spin the AI in the direction it moved and cure nearby AI
                    self.body.spin(next_direction)
                    self.cure_nearby_AI()
        else:
            # If there are no sick AI, perform a random move
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

    def find_sick_AI(self):
        """
        Returns the closest sick AI
        """
        # Find all sick AI in the world
        sick_AI = [ai for ai in self.body.world.AI if ai.is_sick() and ai is not self.body]
        if not sick_AI:
            return None
        # Find the closest sick AI to the current AI
        closest_AI = min(sick_AI, key=lambda ai: self.distance_to(ai))
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
        Determine the direction to move towards the target AI
        """
        target_location = target_AI.get_location()
        if target_location != None and current_location != None:
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

    def cure_nearby_AI(self):
        """
        Cure any sick AI in the neighboring squares
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

                    if neighbor_square.get_AI() is not None and neighbor_square.get_AI().is_sick():
                        neighbor_square.get_AI().get_healthy()
                        Doctors.cured_count += 1

