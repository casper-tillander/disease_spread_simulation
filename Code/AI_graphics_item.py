from PyQt6 import QtWidgets, QtGui, QtCore
from AI import AI
from coordinates import Coordinates
from direction import Direction
import math


class AIGraphicsItem(QtWidgets.QGraphicsPolygonItem):
    """
    The class AIGraphicsItem extends QGraphicsPolygonItem to link it together to the physical
    representation of an AI. The QGraphicsPolygonItem handles the drawing, while the
    AI knows its own location and status.

    Shapes of different AI:
    SmartAI: Circle
    AvoidingAI: Diamond
    Vaccinator: Triangle
    Doctor: Cross
    Builder: Square
    """

    def __init__(self, AI, square_size):
        # Call init of the parent object
        super(AIGraphicsItem, self).__init__()

        self.AI = AI
        self.square_size = square_size
        brush = QtGui.QBrush(1) # 1 for even fill
        self.setBrush(brush)
        self.constructVertices()
        self.updateAll()

    def constructVertices(self):
        if self.AI.is_doctor_instance():
            self.constructCrossVertices()
        elif self.AI.is_vaccinator_instance():
            self.constructTriangleVertices()
        elif self.AI.is_avoiding_instance():
            self.constructDiamondVertices()
        elif self.AI.is_builder_instance():
            self.constructSquareVertices()
        else:
            self.constructCircleVertices()

    def constructCrossVertices(self):
        """
        This method sets the shape of this item into a plus sign (+).
        """
        # Create a new QPolygonF object
        plus = QtGui.QPolygonF()

        # Define the width of the plus sign's arms
        arm_width = self.square_size / 4

        # Add the corners of a plus sign to the polygon object
        plus.append(QtCore.QPointF(self.square_size / 2 - arm_width, 0))  # Top Left
        plus.append(QtCore.QPointF(self.square_size / 2 + arm_width, 0))  # Top Right
        plus.append(
            QtCore.QPointF(self.square_size / 2 + arm_width, self.square_size / 2 - arm_width))  # Middle Top Right
        plus.append(QtCore.QPointF(self.square_size, self.square_size / 2 - arm_width))  # Right Top
        plus.append(QtCore.QPointF(self.square_size, self.square_size / 2 + arm_width))  # Right Bottom
        plus.append(
            QtCore.QPointF(self.square_size / 2 + arm_width, self.square_size / 2 + arm_width))  # Middle Bottom Right
        plus.append(QtCore.QPointF(self.square_size / 2 + arm_width, self.square_size))  # Bottom Right
        plus.append(QtCore.QPointF(self.square_size / 2 - arm_width, self.square_size))  # Bottom Left
        plus.append(
            QtCore.QPointF(self.square_size / 2 - arm_width, self.square_size / 2 + arm_width))  # Middle Bottom Left
        plus.append(QtCore.QPointF(0, self.square_size / 2 + arm_width))  # Left Bottom
        plus.append(QtCore.QPointF(0, self.square_size / 2 - arm_width))  # Left Top
        plus.append(
            QtCore.QPointF(self.square_size / 2 - arm_width, self.square_size / 2 - arm_width))  # Middle Top Left

        # Close the polygon
        plus.append(QtCore.QPointF(self.square_size / 2 - arm_width, 0))  # Top Left

        # Set this newly created polygon as this Item's polygon.
        self.setPolygon(plus)

        # Set the origin of transformations to the center of the plus sign.
        # This makes it easier to rotate this Item.
        self.setTransformOriginPoint(self.square_size / 2, self.square_size / 2)

    def constructDiamondVertices(self):
        """
        This method sets the shape of this item into a diamond.
        """
        # Create a new QPolygonF object
        diamond = QtGui.QPolygonF()

        # Add the corners of a diamond to the the polygon object
        diamond.append(QtCore.QPointF(self.square_size / 2, 0))  # Top
        diamond.append(QtCore.QPointF(self.square_size, self.square_size / 2))  # Right
        diamond.append(QtCore.QPointF(self.square_size / 2, self.square_size))  # Bottom
        diamond.append(QtCore.QPointF(0, self.square_size / 2))  # Left

        # Set this newly created polygon as this Item's polygon.
        self.setPolygon(diamond)

        # Set the origin of transformations to the center of the diamond.
        # This makes it easier to rotate this Item.
        self.setTransformOriginPoint(self.square_size / 2, self.square_size / 2)


    def constructSquareVertices(self):
        """
        This method sets the shape of this item into a square.
        """
        # Create a new QPolygonF object
        square = QtGui.QPolygonF()

        # Add the corners of a square to the the polygon object
        square.append(QtCore.QPointF(0, 0))  # Top-left
        square.append(QtCore.QPointF(self.square_size, 0))  # Top-right
        square.append(QtCore.QPointF(self.square_size, self.square_size))  # Bottom-right
        square.append(QtCore.QPointF(0, self.square_size))  # Bottom-left
        square.append(QtCore.QPointF(0, 0))  # Top-left

        # Set this newly created polygon as this Item's polygon.
        self.setPolygon(square)

        # Set the origin of transformations to the center of the square.
        # This makes it easier to rotate this Item.
        self.setTransformOriginPoint(self.square_size / 2, self.square_size / 2)


    def constructCircleVertices(self):
        """
        This method sets the shape of this item into a circle.
        """
        # Create a new QPolygonF object
        circle = QtGui.QPolygonF()

        # Add points to the polygon to form a circle
        for i in range(0, 360, 10):
            x = self.square_size / 2 * math.cos(math.radians(i)) + self.square_size / 2
            y = self.square_size / 2 * math.sin(math.radians(i)) + self.square_size / 2
            circle.append(QtCore.QPointF(x, y))

        # Set the newly created polygon as the item's polygon
        self.setPolygon(circle)

        # Set the origin of transformations to the center of the circle.
        # This makes it easier to rotate this Item.
        self.setTransformOriginPoint(self.square_size / 2, self.square_size / 2)

    def constructTriangleVertices(self):
        """
        This method sets the shape of this item into a triangle.
        """
        # Create a new QPolygon object
        triangle = QtGui.QPolygonF()

        # Add the corners of a triangle to the the polygon object
        triangle.append(QtCore.QPointF(self.square_size / 2, 0))  # Tip
        triangle.append(QtCore.QPointF(0, self.square_size))  # Bottom-left
        triangle.append(QtCore.QPointF(self.square_size, self.square_size))  # Bottom-right
        triangle.append(QtCore.QPointF(self.square_size / 2, 0))  # Tip

        # Set this newly created polygon as this Item's polygon.
        self.setPolygon(triangle)

        # Set the origin of transformations to the center of the triangle.
        # This makes it easier to rotate this Item.
        self.setTransformOriginPoint(self.square_size / 2, self.square_size / 2)

    def updateAll(self):
        """
        Updates the visual representation to correctly resemble the current
        location, direction and status of the parent AI.
        """
        self.updatePosition()
        self.updateRotation()
        self.updateColor()


    def updatePosition(self):
        """
        Updates the coordinates of this item to match the attached AI.
        """
        location = AI.get_location(self.AI)
        x = Coordinates.get_x(location)
        y = Coordinates.get_y(location)
        self.setX(x*self.square_size)
        self.setY(y * self.square_size)


    def updateRotation(self):
        """
        Rotates this item to match the rotation of parent AI.
        """
        degrees = Direction.get_degrees(self.AI.get_facing())
        self.setRotation(degrees)


    def updateColor(self):
        """
        Draws broken AI in red, infected i pink, stuck in yellow, susceptible in green, recovered in blue.
        """
        if self.AI.is_sick():
            self.setBrush(QtGui.QColor(255, 0, 0))
        if self.AI.is_stuck():
            self.setBrush(QtGui.QColor(255, 255, 0))
        if self.AI.is_recovered():
            self.setBrush(QtGui.QColor(0, 0, 255))
        if self.AI.is_susceptible():
            self.setBrush(QtGui.QColor(0, 255, 0))
        if self.AI.is_infected():
            self.setBrush(QtGui.QColor(255, 20, 147))


    def mousePressEvent(self, *args, **kwargs):
        """
        Remove the AI from the simulation
        """
        self.AI.die()
