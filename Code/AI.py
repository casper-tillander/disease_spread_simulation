from direction import Direction
from coordinates import Coordinates
import random

class AI():
    """
    The class AI represents AIs which inhabit two
    dimensional grid worlds. More specifically, each instance of the class represents
    an "AI body" and basic functionality of such an AI.
    Each "AI body" is associated with a "AI brain" that controls the body
    and determines what functionality is activated and when.

    An AI is equipped with the various capabilities:

     - It can sense its own surroundings (location, facing, the world that it is in).

     - It can move forward.

     - It can spin around in any one of the four main compass directions.

     - It can sense its instance and disease status, and act accordingly

     - Every AI are given individual (randomly generated) attributes that affect the susceptibility of the disease

    This class also keeps track of some statistics for the simulation, for example the amount of dead or recovered AI.
    """

    # STATISTICS
    dead_count = 0
    recovered_count = 0
    infected_count = 0
    vaccinated_count = 0

    gender_count = {"male": 0, "female": 0}
    smoker_count = {"smoker": 0, "non-smoker": 0}
    pre_existing_conditions_count = {"yes": 0, "no": 0}
    lifestyle_count = {"active": 0, "sedentary": 0, "moderate": 0}

    def __init__(self, name, spread_type, infection_chance, death_chance, incubation_duration,
                 recovery_duration, vaccination_rate, is_doctor=False, is_vaccinator=False, is_avoiding=False,
                 is_builder=False):
        """
        Creates a new AI with the given name. The newly
        created AI is initially just a "dumb shell" until
        it's given a brain later using the method
        set_brain().

        If the given name is None or an empty
        string, the name is set to "Incognito".
        """

        # Assign random attributes
        self.age = random.randint(0, 100)
        self.gender = random.choice(["male", "female"])
        self.smoker = random.choice([True, False])
        self.pre_existing_conditions = random.choice([True, False])
        self.lifestyle = random.choice(["active", "sedentary", "moderate"])

        # Update class-level dictionaries with the generated attributes
        AI.gender_count[self.gender] += 1
        AI.smoker_count["smoker" if self.smoker else "non-smoker"] += 1
        AI.pre_existing_conditions_count["yes" if self.pre_existing_conditions else "no"] += 1
        AI.lifestyle_count[self.lifestyle] += 1

        # Compute susceptibility
        self.susceptibility = self.calculate_susceptibility()

        #DISEASE information from user
        self.spread_type = spread_type
        self.infection_chance = infection_chance * 0.01
        self.death_chance = death_chance * 0.01
        self.incubation_duration = incubation_duration
        self.recovery_duration = recovery_duration

        #DISEASE information standard
        self.incubation_time = 0
        self.recovery_time = 0

        #General AI information
        self.set_name(name)
        self.world = None        # fixed value
        self.location = None     # most-recent holder
        self.brain = None        # most-recent holder
        self.facing = None       # most-recent holder

        #Instance
        self.is_doctor = is_doctor
        self.is_vaccinator = is_vaccinator
        self.is_avoiding = is_avoiding
        self.is_builder = is_builder

        #DISEASE status
        self.susceptible = True
        self.infected = False
        self.sick = False
        self.recovered = False
        self.dead = False

        # VACCINATION information and status
        self.vaccinated = False
        self.vaccination_rate = 1 - (vaccination_rate * 0.01)

        #AI graphics item
        self.graphics_item = None


    def set_name(self, name):
        """
        Sets the name of the AI
        """
        if not name:
            self.name = "Incognito"   # most-recent holder
        else:
            self.name = name


    def get_name(self):
        """
        Returns the AI name
        """
        return self.name


    def set_brain(self, new_brain):
        """
        Sets a "brain" for the AI (replacing any brain
        previously set, if any)
        Parameter new_brain is the artificial intelligence that controls the AI
        """
        self.brain = new_brain


    def get_brain(self):
        """
        Returns the "brain" (or AI) of the AI
        """
        return self.brain

    """
    These functions return the AI instance
    """
    def is_doctor_instance(self):
        return self.is_doctor

    def is_vaccinator_instance(self):
        return self.is_vaccinator

    def is_avoiding_instance(self):
        return self.is_avoiding

    def is_builder_instance(self):
        return self.is_builder

    def get_world(self):
        """
        Returns the world in which the AI is, or None if the AI has not been placed in any AI world
        """
        return self.world


    def get_location(self):
        """
        Returns the current location of the AI in the AI world, or None if the AI has not been placed in any AI world
        """
        return self.location

    def get_location_square(self):
        """
        Returns the square that the AI is in: Square
        """
        return self.get_world().get_square(self.get_location())


    def get_facing(self):
        """
        Returns the direction the AI is facing
        """
        return self.facing

    def get_infected(self):
        """
        Makes the AI infected but not yet sick.
        """
        self.susceptible = False
        self.infected = True
        self.sick = False
        self.recovered = False
        self.dead = False

    def get_sick(self):
        """
        Makes the AI sick.
        """
        self.susceptible = False
        self.infected = False
        self.sick = True
        self.recovered = False
        self.dead = False

    def get_healthy(self):
        """
        Makes the AI well again.
        """
        self.susceptible = False
        self.infected = False
        self.sick = False
        self.recovered = True
        self.dead = False

    def die(self):
        """
        Kills the AI and removes the graphics item from the simulation
        """
        self.susceptible = False
        self.infected = False
        self.sick = False
        self.recovered = False
        self.dead = True
        AI.dead_count += 1
        self.get_location_square().remove_AI()
        if self.graphics_item:
            self.world.gui.delete_AI_graphics_item(self.graphics_item)

    def vaccinate(self):
        """
        Vaccinates the AI, making it immune to the disease.
        """
        self.vaccinated = True
        AI.vaccinated_count += 1

    def is_vaccinated(self):
        """
        Determines whether the AI is vaccinated or not.
        """
        return self.vaccinated

    """
    These functions determine the health status of the AI
    """
    def is_sick(self):
        return self.sick

    def is_infected(self):
        return self.infected

    def is_recovered(self):
        return self.recovered

    def is_susceptible(self):
        return self.susceptible

    def is_dead(self):
        return self.dead

    def is_stuck(self):
        """
        Determines whether the AI is stuck or not, i.e., are there any
        squares that the AI could move into.  This is done by
        examining the four adjacent squares (diagonally adjacent squares are
        not considered). If there is a wall in all directions, the AI is
        considered stuck. Also, if the AI has not yet been placed in any
        world, it is considered to be stuck.
        """
        world = self.get_world()
        if world is None:
            return True

        for value in Direction.get_values():          # most-recent holder
            if not world.get_square(self.get_location().get_neighbor(value)).is_wall_square():
                return False
        return True


    def set_world(self, world,  location,  facing):
        """
        Places the AI in the given world at the specified
        coordinates.  Note! This method is supposed to be used from the
        addAI method in the World class,
        which makes sure that the AI is appropriately recorded as
        being part of the world.
        """
        target_square = world.get_square(location)
        if not target_square.is_empty() or self.get_world() is not None:
            return False
        else:
            self.world = world
            self.location = location
            self.facing = facing
            return True


    def spin(self, new_facing):
        """
        Turns the AI in the specified direction, if the
        AI is intact. If the AI is broken, the method does nothing.
        """
        self.facing = new_facing


    def move(self, direction):
        """
        Changes the place of the AI within its current world
        from the current square to the square next to it in the
        given direction. The direction does not necessarily have
        to be the same one that the AI is originally facing in.
        This method changes the AI to face the direction it
        moves in.

        Two AI can never be in the same square, neither can
        an AI and a wall. If the square at the given coordinates
        is not empty, a collision occurs instead and the AI
        does not move (but still turns to face whatever it collided
        with).
        """
        target = self.get_location().get_neighbor(direction)
        current_square = self.get_location_square()
        target_square = self.get_world().get_square(target)
        self.spin(direction)
        if target_square.is_empty():
            current_square.remove_AI()
            self.location = target
            target_square.set_AI(self)
            return True
        elif target_square.get_AI() is not None:
            return False
        else:   # collided with wall
            return False


    def move_forward(self):
        """
        Moves the AI forward one square.
        """
        return self.move(self.get_facing())


    def take_turn(self):
        """
        Gives the AI a turn to act. An unstuck AI, however, consults its brain to
        find out what to do. This is done by calling the brain's method move_body().
        Here is a general outline of what happens during a AI's turn:
         1. The AI checks its sensors to see if it is stuck. (If it is, it doesn't do anything.)
         2. If not, it call's it's brain's move_body() method, leaving it up to the brain to decide
            what happens next.
         3. The move_body() method will then determine how the AI behaves, usually calling
            various methods of the AI's body (i.e., the AI object whose turn it is),
            e.g. move, spin. However, it is not up to the AI object
            to decide which of its methods get called - that depends on the implementation of the AI's brain.
        """
        if not self.is_stuck():
            self.brain.move_body()
        self.update_disease_status()


    def calculate_susceptibility(self):
        """
        This function calculates the susceptibility of an AI based on its individual attributes age, gender, lifestyle,
        pre existing conditions and whether the AI is a smoker.
        """
        susceptibility = 1.0

        # Age-based susceptibility
        if self.age < 18:
            susceptibility *= 0.8
        elif self.age > 65:
            susceptibility *= 1.3

        # Gender-based susceptibility
        if self.gender == "male":
            susceptibility *= 1.1
        elif self.gender == "female":
            susceptibility *= 0.9

        # Smoker-based susceptibility
        if self.smoker:
            susceptibility *= 1.5
        else:
            susceptibility *= 0.8

        # Pre-existing condition-based susceptibility
        if self.pre_existing_conditions:
            susceptibility *= 2.0
        else:
            susceptibility *= 1.0

        # Lifestyle-based susceptibility
        if self.lifestyle == "active":
            susceptibility *= 0.7
        elif self.lifestyle == "sedentary":
            susceptibility *= 1.4
        elif self.lifestyle == "moderate":
            susceptibility *= 1.0

        return susceptibility


    def update_disease_status(self):
        """
        This function updates the disease status of the AI by checking its infection and recovery status,
        and managing its interactions with other AI agents based on their health status and the spread type
        (direct contact or within a distance of 2). The function handles incubation, recovery, death, and
        vaccination effects on infection chances.
        """
        if self.is_infected():
            self.incubation_time += 1
            if self.incubation_time > self.incubation_duration:
                self.get_sick()

        if self.is_sick():
            self.recovery_time += 1
            if self.recovery_time > self.recovery_duration:
                if random.random() < self.death_chance:
                    self.die()
                else:
                    self.get_healthy()
                    AI.recovered_count += 1
                self.recovery_time = 0

        if self.is_recovered():
            return False

        if self.spread_type == 0:
            if self.is_susceptible():
                # Check nearby AI:
                for x_offset in range(-1, 2):
                    for y_offset in range(-1, 2):
                        if x_offset == 0 and y_offset == 0:
                            # Skip the AI's own square
                            continue

                        neighbor_x = self.get_location().get_x() + x_offset
                        neighbor_y = self.get_location().get_y() + y_offset
                        neighbor_square = self.world.get_square(Coordinates(neighbor_x, neighbor_y))

                        # Check if there is an AI in the neighbor square and if it is sick
                        if neighbor_square.get_AI() is not None and neighbor_square.get_AI().is_sick():
                            if not self.is_vaccinated():
                                if random.random() < self.infection_chance * self.susceptibility:
                                    self.get_infected()
                                    AI.infected_count += 1
                            if self.is_vaccinated():
                                if random.random() < self.infection_chance * self.vaccination_rate * self.susceptibility:
                                    self.get_infected()
                                    AI.infected_count += 1

        if self.spread_type == 1:
            if self.is_susceptible():
                # Check nearby AI within a distance of 2:
                for x_offset in range(-2, 3):
                    for y_offset in range(-2, 3):
                        if x_offset == 0 and y_offset == 0:
                            # Skip the AI's own square
                            continue

                        neighbor_x = self.get_location().get_x() + x_offset
                        neighbor_y = self.get_location().get_y() + y_offset
                        neighbor_square = self.world.get_square(Coordinates(neighbor_x, neighbor_y))

                        # Check if there is an AI in the neighbor square and if it is sick
                        if neighbor_square.get_AI() is not None and neighbor_square.get_AI().is_sick():
                            if not self.is_vaccinated():
                                if random.random() < self.infection_chance * self.susceptibility:
                                    self.get_infected()
                                    AI.infected_count += 1
                            if self.is_vaccinated():
                                if random.random() < self.infection_chance * self.vaccination_rate * self.susceptibility:
                                    self.get_infected()
                                    AI.infected_count += 1

    def __str__(self):
        return self.get_name() + ' at location ' + str(self.get_location())
