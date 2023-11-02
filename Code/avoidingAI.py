from direction import Direction
from AI_brain import AIbrain
import random

"""
The AvoidingAI class is a subclass of AIbrain, representing a type of AI that actively avoids other AI in the world.
It always tries to move away from the closest AI. The AI also considers staying away from the edges of the world 
and moves towards the center if possible.
"""

class AvoidingAI(AIbrain):
    def __init__(self, body):
        super(AvoidingAI, self).__init__(body)
        self.random = random.Random()

    def move_body(self):
        """
        AvoidingAI avoids the other AI:s at all cost. However, when two directions are equally good, it chooses the
        one that takes it closer to the center, to avoid getting stuck.
        """
        closest_AI = self.find_closest_AI()

        if closest_AI is not None:
            distance_to_closest_AI = self.distance_to(closest_AI)
            if distance_to_closest_AI > 10:
                self.random_move()
            else:
                location = self.body.get_location()
                next_direction = self.determine_direction_away_from_AI(location, closest_AI)
                if next_direction:
                    moved = self.body.move(next_direction)
                    if moved:
                        self.body.spin(next_direction)
        else:
            self.random_move()

    def find_closest_AI(self):
        """
        Finds the closest AI
        """
        AI_list = [ai for ai in self.body.world.AI if ai is not self.body]
        if not AI_list:
            return None

        closest_AI = min(AI_list, key=lambda ai: self.distance_to(ai))
        return closest_AI

    def distance_to(self, other_AI):
        """
        Calculates the Manhattan distance to another AI
        """
        dx = self.body.get_location().get_x() - other_AI.get_location().get_x()
        dy = self.body.get_location().get_y() - other_AI.get_location().get_y()
        return abs(dx) + abs(dy)

    def determine_direction_away_from_AI(self, current_location, closest_AI):
        """
        Determines the direction that moves the AI away from the closest AI
        """
        world_width = self.body.world.get_width()
        world_height = self.body.world.get_height()
        target_location = closest_AI.get_location()

        if target_location is not None and current_location is not None:
            distance_x = target_location.get_x() - current_location.get_x()
            distance_y = target_location.get_y() - current_location.get_y()

            x_middle = world_width // 2
            y_middle = world_height // 2

            possible_directions = []

            if distance_x > 0:
                possible_directions.append(Direction.WEST)
            elif distance_x < 0:
                possible_directions.append(Direction.EAST)

            if distance_y > 0:
                possible_directions.append(Direction.NORTH)
            elif distance_y < 0:
                possible_directions.append(Direction.SOUTH)

            if len(possible_directions) > 1:
                if current_location.get_x() < x_middle:
                    preferred_x = Direction.EAST
                else:
                    preferred_x = Direction.WEST

                if current_location.get_y() < y_middle:
                    preferred_y = Direction.SOUTH
                else:
                    preferred_y = Direction.NORTH

                preferred_directions = [d for d in possible_directions if d in [preferred_x, preferred_y]]

                if preferred_directions:
                    return random.choice(preferred_directions)

            if possible_directions:
                return random.choice(possible_directions)

        return None

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

