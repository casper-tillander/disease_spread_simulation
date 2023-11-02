import random
import math
from direction import Direction
from AI_brain import AIbrain
from coordinates import Coordinates

"""
The Builder AI tries to divide the world into two parts. It has a list of the coordinates on line 15 in the world.
It gets a random coordinate from the list, moves there and builds a wall. It repeats this process until the world is
divided. It then moves randomly.
"""

class Builder(AIbrain):
    def __init__(self, body):
        super(Builder, self).__init__(body)
        self.random = random.Random()
        self.building_targets = [Coordinates(x, 15) for x in range(30)]
        self.current_target = None

    def move_body(self):
        """
        The builder first moves to a starting position. Then it gets a random coordinate from the list,
        moves there and builds a wall. It repeats this process until the world is divided.
        """
        if self.building_targets:
            if not self.current_target or self.current_target == self.body.get_location():
                self.current_target = self.random.choice(self.building_targets)
            self.move_to_target()
        else:
            self.random_move()

    def move_to_target(self):
        """
        Moves the AI to the starting position
        """
        location = self.body.get_location()
        if self.is_neighboring_square(location, self.current_target):
            self.build_wall()
        else:
            next_direction = self.determine_direction_to_target(location, self.current_target)
            if next_direction:
                self.body.move(next_direction)
                self.body.spin(next_direction)

    def is_neighboring_square(self, current_location, target_location):
        """
        Checks if the neighbouring square is the target square
        """
        return abs(current_location.get_x() - target_location.get_x()) + abs(current_location.get_y() - target_location.get_y()) == 1

    def determine_direction_to_target(self, current_location, target_location):
        """
        Determines the direction to the target square and returns it
        """
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

    def build_wall(self):
        """
        Builds a wall in the target square.
        """
        target_square = self.body.world.get_square(self.current_target)
        if target_square.is_empty():
            target_square.set_wall()
            self.building_targets.remove(self.current_target)
        self.current_target = None

    """
    Generates a random move and direction
    """
    def random_move(self):
        facing = self.body.get_facing()
        if self.body.move(self.get_random_direction()):
            facing = Direction.get_next_clockwise(facing)
            self.body.spin(facing)

    def get_random_direction(self):
        directions = Direction.get_values()
        return self.random.choice(directions)

