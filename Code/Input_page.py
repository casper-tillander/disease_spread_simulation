from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox

"""
This class builds the input window for the simulation. The user can input different values that affect the simulation.
"""

class InputWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Simulation Input')
        self.setGeometry(50, 40, 500, 620)
        self.submit_pressed = False
        self.setStyleSheet('''
                   QWidget {
                       font-size: 10px;
                   }
                   QLabel {
                       font-weight: bold;
                   }
                   QLineEdit, QPushButton {
                       min-height: 15px;
                       padding: 5px;
                       border-radius: 5px;
                   }
                   QPushButton {
                       background-color: #5cb85c;
                       color: white;
                       font-weight: bold;
                       border: none;
                   }
                   QPushButton:hover {
                       background-color: #449d44;
                   }
                   QLineEdit:focus {
                       border: 2px solid #5cb85c;
                   }
                   QTextEdit:focus, QPlainTextEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, QComboBox:focus, QLineEdit:focus {
                       border: 2px solid #5cb85c;
                   }
               ''')

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(10, 10, 10, 10)  # Add padding to the layout
        self.setLayout(self.layout)

        # Title
        title_label = QLabel("Disease Simulation")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")  # Set the title style
        self.layout.addWidget(title_label)

        # Intro text
        intro_label = QLabel(
            "Welcome to the Disease Simulation Input Page. Here, you'll configure the simulation to model the spread of a contagious disease within a population. Please provide the following information:\n\n"
            "1. Number of healthy SmartAI and AvoidingAI.\n"
            "2. Number of infected SmartAI and AvoidingAI.\n"
            "3. Number of doctors, vaccinators and builders.\n"
            "4. Spread type (0: contact, 1: distance).\n"
            "5. Infection chance, incubation duration, recovery duration, death chance, and vaccination effectiveness (in percentage).\n\n"
            "Enter valid values for each field within the given ranges. After submitting, you'll be able to view the simulation and track the disease's progress.")

        intro_label.setWordWrap(True)
        self.layout.addWidget(intro_label)

        # add input fields
        inputs_layout = QVBoxLayout()
        inputs_layout.setSpacing(20)

        # add input fields
        self.healthy_smart_input = QLineEdit()
        self.healthy_smart_input.setPlaceholderText('Enter the number of healthy SmartAI (0-50)')
        self.layout.addWidget(self.healthy_smart_input)

        self.healthy_avoiding_input = QLineEdit()
        self.healthy_avoiding_input.setPlaceholderText('Enter the number of healthy AvoidingAI (0-50)')
        self.layout.addWidget(self.healthy_avoiding_input)

        self.sick_smart_input = QLineEdit()
        self.sick_smart_input.setPlaceholderText('Enter the number of sick SmartAI (0-50)')
        self.layout.addWidget(self.sick_smart_input)

        self.sick_avoiding_input = QLineEdit()
        self.sick_avoiding_input.setPlaceholderText('Enter the number of sick AvoidingAI (0-50)')
        self.layout.addWidget(self.sick_avoiding_input)

        self.doctors_input = QLineEdit()
        self.doctors_input.setPlaceholderText('Enter the number of doctors (0-10)')
        self.layout.addWidget(self.doctors_input)

        self.vaccinators_input = QLineEdit()
        self.vaccinators_input.setPlaceholderText('Enter the number of vaccinators (0-10)')
        self.layout.addWidget(self.vaccinators_input)

        self.builders_input = QLineEdit()
        self.builders_input.setPlaceholderText('Would you like a builder in the world (yes: 1, no: 0)')
        self.layout.addWidget(self.builders_input)

        self.spread_type_input = QLineEdit()
        self.spread_type_input.setPlaceholderText('Enter spread type (contact: 0, distance: 1)')
        self.layout.addWidget(self.spread_type_input)

        self.infection_chance_input = QLineEdit()
        self.infection_chance_input.setPlaceholderText('Enter infection chance (0-100)')
        self.layout.addWidget(self.infection_chance_input)

        self.incubation_duration_input = QLineEdit()
        self.incubation_duration_input.setPlaceholderText('Enter incubation duration (0-100 turns)')
        self.layout.addWidget(self.incubation_duration_input)

        self.recovery_duration_input = QLineEdit()
        self.recovery_duration_input.setPlaceholderText('Enter recovery duration (1-100 turns)')
        self.layout.addWidget(self.recovery_duration_input)

        self.death_chance_input = QLineEdit()
        self.death_chance_input.setPlaceholderText('Enter death chance (0-100)')
        self.layout.addWidget(self.death_chance_input)

        self.vaccination_rate_input = QLineEdit()
        self.vaccination_rate_input.setPlaceholderText('Enter vaccination effectiveness (0-100)')
        self.layout.addWidget(self.vaccination_rate_input)

        # add submit button
        self.submit_button = QPushButton('Submit')
        self.layout.addWidget(self.submit_button)

        # connect submit button to function that checks and returns input values or shows error message
        self.submit_button.clicked.connect(self.return_input)

    def return_input(self):
        try:
            num_smart_healthy = int(self.healthy_smart_input.text())
            num_avoiding_healthy = int(self.healthy_avoiding_input.text())
            num_smart_sick = int(self.sick_smart_input.text())
            num_avoiding_sick = int(self.sick_avoiding_input.text())
            num_doctors = int(self.doctors_input.text())
            num_vaccinators = int(self.vaccinators_input.text())
            num_builders = int(self.builders_input.text())
            spread_type = int(self.spread_type_input.text())
            infection_chance = int(self.infection_chance_input.text())
            incubation_duration = int(self.incubation_duration_input.text())
            recovery_duration = int(self.recovery_duration_input.text())
            death_chance = int(self.death_chance_input.text())
            vaccination_rate = int(self.vaccination_rate_input.text())

            if not (0 <= num_smart_healthy <= 50) or not (0 <= num_avoiding_healthy <= 50)\
                    or not (0 <= num_smart_sick <= 50) or not (0 <= num_avoiding_sick <= 50)\
                    or not (0 <= num_doctors <= 10) or not (0 <= num_builders <= 1)\
                    or not (0 <= num_vaccinators <= 10) or not(0 <= spread_type <= 1) \
                    or not (0 <= infection_chance <= 100) or not (0 <= incubation_duration <= 100)\
                    or not (1 <= recovery_duration <= 100) or not (0 <= death_chance <= 100)\
                    or not (0 <= vaccination_rate <= 100):
                raise ValueError

            self.close()
            self.submit_pressed = True
            return num_smart_healthy, num_avoiding_healthy, num_smart_sick, num_avoiding_sick, num_doctors,\
                   num_vaccinators, num_builders, spread_type, infection_chance, death_chance, incubation_duration,\
                   recovery_duration, vaccination_rate

        except ValueError:
            error_dialog = QMessageBox(self)
            error_dialog.setWindowTitle("Input Error")
            error_dialog.setText("Please enter valid values for each field.")
            error_dialog.exec()

    def is_submit_pressed(self):
        return self.submit_pressed