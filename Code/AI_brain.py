from AI import AI


class AIbrain(AI):
    """
    The class `AIbrain` represents the "brains" (or artificial intelligence, AI) of
    virtual AI that inhabit two dimensional grid worlds. An AI brain is equipped
    with an algorithm for determining what a AI should do during its turn in an AI
    simulation. In other words, an AI brain is capable of controlling the actions of a AI body.

    Concrete class that extend this class need to provide implementations for the abstract
    `move_body` method; each such concrete class can represent a new kind of AI behavior.

    The given parameter body is the AI that the brain controls.
    """

    def __init__(self, body):
        self.body = body


    def move_body(self):
        pass
