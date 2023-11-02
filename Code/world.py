from square import Square

class World():
    """
    The class World describes a two dimensional world made up
    of squares that different kinds of AI can inhabit. The squares are
    identified by unique coordinates which range from 0...width-1 and
    0...height-1. Each square is represented by a Square object.

    AI can be added to the world, and the world
    maintains an AI listing which allows AI to take their turns in
    a round-robin fashion, in the order in which they were added.
    Each AI is represented by an AI object.
    """

    def __init__ (self, width, height):
        """
        Creates a new world with the specified dimensions.
        Initially all the squares of the new world are empty.

        Parameter width is the width of the world in squares

        Parameter height is the height of the world in squares
        """


        self.squares = [None] * width
        for x in range(self.get_width()):      # stepper
            self.squares[x] = [None] * height
            for y in range(self.get_height()):    # stepper
                self.squares[x][y] = Square()    # fixed value
        self.AI = []                        # container
        self.turn = 0                         # kinda like stepper (but not quite) index to AI list
        self.gui = None

    def get_width(self):
        """
        Returns width of the world in squares
        """
        return len(self.squares)


    def get_height(self):
        """
        Returns the height of the world in squares
        """
        return len(self.squares[0])

    def add_AI(self, AI, location, facing):
        """
        Adds a new AI in the world. (Note! This method also
        takes care that the AI is aware if its new position.
        This is done by calling AI's set_world method.)

        Parameter AI is the AI to be added

        Parameter location is the coordinates of the AI

        Parameter facing is the direction the AI is facing initially

        Returns False if the square at the given location is not empty or the given AI is already located in some world (this or some other world), True otherwise
        """
        if AI.set_world(self, location, facing):
            self.AI.append(AI)
            self.get_square(location).set_AI(AI)
            return True
        else:
            return False


    def add_wall(self, location):
        """
        Adds a wall at the given location in the world, if
        possible. If the square is not empty, the method fails to
        do anything.

        Parameter location is the location of the wall

        Returns a boolean value indicating if the operation succeeded
        """
        return self.get_square(location).set_wall()


    def get_square(self, coordinates):
        """
        Parameter coordinates is a location in the world

        Returns the square that is located at the given location. If the given coordinates point outside of the world,
        this method returns a square that contains a wall and is not located in any world
        """
        if self.contains(coordinates):
            return self.squares[coordinates.get_x()][coordinates.get_y()]
        else:
            return Square(True)


    def get_number_of_AI(self):
        """
        Returns the number of AI added to this world
        """
        return len(self.AI)


    def get_AI(self, turn_number):
        """
        Returns the AI which has the given "turn number".
        The turn numbers of the AI in a world are determined by
        the order in which they were added. I.e., the first AI has
        a turn number of 0, the second one's number is 1, etc.

        Parameter turn_number is the turn number of a AI. Must be on the interval [0, (number of AI minus 1)]

        Returns the AI with the given turn number
        """
        if 0 <= turn_number < self.get_number_of_AI():
            return self.AI[turn_number]
        else:
            return None


    def get_next_AI(self):
        """
        Returns the AI to act next in this world's round-robin turn system, or None if there aren't any AI in the world
        """
        if self.get_number_of_AI() < 1:
            return None
        else:
            return self.AI[self.turn]


    def next_AI_turn(self):
        """
        Lets the next AI take its turn. That is, calls the
        take_turn method of the AI whose turn it is,
        and passes the turn to the next AI. The turn is passed
        to the AI with the next highest turn number (i.e. the one
        that was added to the world after the current AI), or wraps
        back to the first AI (turn number 0) if the last turn number
        was reached. That is to say: the AI which was added first,
        moves first, followed by the one that was added second, etc.,
        until all AI have moved and the cycle starts over.
        If there are no AI in the world, the method does nothing.
        """
        current = self.get_next_AI()
        if current is not None:
            self.turn = (self.turn + 1) % self.get_number_of_AI()
            current.take_turn()


    def next_full_turn(self):
        """
        Lets each AI take its next turn. That is, calls the next_AI_turn
        a number of times equal to the number of AI in the world.
        """
        for count in range(self.get_number_of_AI()):      # stepper
            self.next_AI_turn()


    def contains(self, coordinates):
        """
        Determines if this world contains the given coordinates.

        Parameter coordinates is a coordinate pair: Coordinates

        Returns a boolean value indicating if this world contains the given coordinates
        """
        x_coordinate = coordinates.get_x()
        y_coordinate = coordinates.get_y()
        return 0 <= x_coordinate < self.get_width() and 0 <= y_coordinate < self.get_height()


    def get_AI_array(self):
        """
        Returns an array containing all the robots currently located in this world: list
        """
        return self.AI[:]

