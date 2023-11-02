from PyQt6 import QtWidgets, QtCore, QtGui
from AI_graphics_item import AIGraphicsItem
from coordinates import Coordinates


class GUI(QtWidgets.QMainWindow):
    """
    The class GUI handles the drawing of a World and allows user to
    interact with it.
    """

    def __init__(self, world, square_size):
        super().__init__()
        self.setCentralWidget(QtWidgets.QWidget())  # QMainWindown must have a centralWidget to be able to add layouts
        self.horizontal = QtWidgets.QHBoxLayout()  # Horizontal main layout
        self.centralWidget().setLayout(self.horizontal)
        self.world = world
        self.square_size = square_size
        self.init_window()
        self.world.gui = self

        self.add_AI_world_grid_items()
        self.add_AI_graphics_items()
        self.update()

        # Set a timer to call the update function periodically
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.world.next_full_turn)
        self.timer.timeout.connect(self.update)
        self.timer.start(100)  # Milliseconds

    def add_AI_world_grid_items(self):
        """
        This function iterates through the world grid and creates a QGraphicsRectItem for each square.
        It sets the position, width, and height of the QGraphicsRectItem based on the square's coordinates and size.
        It also sets the color of the QGraphicsRectItem based on whether the square is a wall or not.
        """
        for x in range(self.world.get_width()):
            for y in range(self.world.get_height()):
                # Create a new QGraphicsRectItem with the correct position, width, and height.
                rect = QtWidgets.QGraphicsRectItem(x * self.square_size, y * self.square_size, self.square_size,
                                                   self.square_size)
                # Add the newly created item to the scene
                self.scene.addItem(rect)
                # Set color based on whether square is a wall or not
                if self.world.get_square(Coordinates(x, y)).is_wall:
                    color = QtGui.QColor(20, 20, 20)
                else:
                    color = QtGui.QColor(211, 211, 211)
                brush = QtGui.QBrush(color)
                rect.setBrush(brush)

    def add_AI_graphics_items(self):
        """
        This function iterates through the AI instances in the world and creates a new AIGraphicsItem for each AI
        that has not been added yet. It sets the graphics_item attribute of the AI to the created AIGraphicsItem
        and adds the AIGraphicsItem to the scene.
        """
        added_AI = []

        for AI in self.world.AI:
            if AI not in added_AI:
                # create new AIGraphicsItem for this AI
                graphics_item = AIGraphicsItem(AI, self.square_size)
                AI.graphics_item = graphics_item  # Set the graphics_item attribute of the AI
                self.scene.addItem(graphics_item)
                added_AI.append(AI)

    def delete_AI_graphics_item(self, ai_graphics_item):
        """
        Remove the AI's graphics item from the scene.
        """
        self.scene.removeItem(ai_graphics_item)

    def get_AI_graphics_items(self):
        """
        Returns all the AIGraphicsItem in the scene.
        """
        items = []
        for item in self.scene.items():
            if type(item) is AIGraphicsItem:
                items.append(item)
        return items

    def update_AI_graphics_items(self):
        """
        Iterates over all AI items and updates their position to match
        their physical representations in the world.
        """
        for AI_item in self.get_AI_graphics_items():
            AI_item.updateAll()

    def update_grid(self):
        for x in range(self.world.get_width()):
            for y in range(self.world.get_height()):
                square = self.world.get_square(Coordinates(x, y))
                rect = self.scene.itemAt(float(x * self.square_size + self.square_size // 2),
                                         float(y * self.square_size + self.square_size // 2), self.view.transform())

                if not isinstance(rect, AIGraphicsItem):  # Add this check
                    if square.is_wall:
                        color = QtGui.QColor(20, 20, 20)
                    else:
                        color = QtGui.QColor(211, 211, 211)
                    brush = QtGui.QBrush(color)
                    rect.setBrush(brush)

    def update(self):
        """
        Updates the AI graphics items to match their current state in the world.
        """
        self.update_AI_graphics_items()
        self.update_grid()
        if all(ai.is_dead() or ai.is_recovered() or ai.is_susceptible() for ai in self.world.AI):
            self.close()

    def init_window(self):
        """
        Sets up the window.
        """
        self.setGeometry(30, 30, 650, 635)
        self.setWindowTitle('World')
        self.show()

        # Add a scene for drawing 2d objects
        self.scene = QtWidgets.QGraphicsScene()
        self.scene.setSceneRect(-20, -25, 820, 630)

        # Add a view for showing the scene
        self.view = QtWidgets.QGraphicsView(self.scene, self)
        self.view.adjustSize()
        self.view.show()
        self.horizontal.addWidget(self.view)
