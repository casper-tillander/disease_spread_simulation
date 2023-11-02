class Square():
    """
    The class Square represents a single square in a the world.
    A square can contain either a wall or an AI or it can be empty.
    """

    def __init__(self, is_wall=False):
        """
        Creates a new square. Initially there is nothing in the square.
        """
        self.AI = None     # most-recent holder (None if no AI in square)
        self.is_wall = is_wall  # flag (one-way currently, since walls can not be removed)


    def get_AI(self):
        """
        Returns the AI in the square or None if there is no AI in the square
        """
        return self.AI


    def is_wall_square(self):
        """
        Returns a boolean value stating whether there is a wall in the square or not
        """
        return self.is_wall


    def is_empty(self):
        """
        Returns a boolean value stating whether the square is empty (A square is empty if it does not contain a wall or an AI) or not
        """
        return not self.is_wall_square() and self.AI is None


    def set_AI(self, AI):
        """
        Marks the square as containing an AI, if possible.
        If the square was not empty, the method fails to do anything.

        Parameter AI is the AI to be placed in this square: AI

        Returns a boolean value indicating if the operation succeeded
        """
        if self.is_empty():
            self.AI = AI
            return True
        else:
            return False


    def remove_AI(self):
        """
        Removes the AI in this square.

        Returns the AI removed from the square or None, if there was no AI
        """
        removed_AI = self.get_AI()
        self.AI = None
        return removed_AI


    def set_wall(self):
        """
        Sets a wall in this square, if possible.
        If the square was not empty, the method fails to do anything.

        Returns a boolean value indicating if the operation succeeded
        """
        if self.is_empty():
            self.is_wall = True
            return True
        else:
            return False
