import csv
import os

"""
This class handles the writing of the simulation data to the csv file "simulation_data.csv"
"""

class SimulationDataStorage:
    def save_simulation_data(self, turn, dead_count, infected_count, recovered_count, vaccinated_count,
                             cured_count, total_population, gender_count, smoker_count,
                             pre_existing_conditions_count, lifestyle_count):
        mortality_rate = (dead_count / total_population)
        infection_rate = (infected_count / total_population)
        recovery_rate = (recovered_count / total_population)
        vaccination_rate = (vaccinated_count / total_population)
        cured_rate = (cured_count / total_population)

        simulation_data = {
            "turn": turn,
            "dead_count": dead_count,
            "infected_count": infected_count,
            "recovered_count": recovered_count,
            "vaccinated_count": vaccinated_count,
            "cured_count": cured_count,
            "total_population": total_population,
            "rates": {
                "mortality_rate": mortality_rate,
                "infection_rate": infection_rate,
                "recovery_rate": recovery_rate,
                "vaccination_rate": vaccination_rate,
                "cured_rate": cured_rate
            },
            "gender_count": gender_count,
            "smoker_count": smoker_count,
            "pre_existing_conditions_count": pre_existing_conditions_count,
            "lifestyle_count": lifestyle_count
        }

        self.write_simulation_data(simulation_data)

    def write_simulation_data(self, simulation_data, file_name='simulation_data.csv'):
        headers = [
            'Turn', 'Dead', 'Infected', 'Recovered', 'Vaccinated', 'Cured', 'Total_Population',
            'Mortality Rate', 'Infection Rate', 'Recovery Rate', 'Vaccination Rate', 'Cured Rate',
            'Male', 'Female', 'Smoker', 'Non-Smoker', 'Pre-Existing Conditions', 'No Pre-Existing Conditions',
            'Active', 'Sedentary', 'Moderate'
        ]

        if not os.path.exists(file_name):
            with open(file_name, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(headers)

        with open(file_name, mode='a', newline='') as file:
            writer = csv.writer(file)
            row = [
                simulation_data['turn'],
                simulation_data['dead_count'],
                simulation_data['infected_count'],
                simulation_data['recovered_count'],
                simulation_data['vaccinated_count'],
                simulation_data['cured_count'],
                simulation_data['total_population'],
                simulation_data['rates']['mortality_rate'],
                simulation_data['rates']['infection_rate'],
                simulation_data['rates']['recovery_rate'],
                simulation_data['rates']['vaccination_rate'],
                simulation_data['rates']['cured_rate'],
                simulation_data['gender_count']['male'],
                simulation_data['gender_count']['female'],
                simulation_data['smoker_count']['smoker'],
                simulation_data['smoker_count']['non-smoker'],
                simulation_data['pre_existing_conditions_count']['yes'],
                simulation_data['pre_existing_conditions_count']['no'],
                simulation_data['lifestyle_count']['active'],
                simulation_data['lifestyle_count']['sedentary'],
                simulation_data['lifestyle_count']['moderate']
            ]
            writer.writerow(row)

    """
    This function returns the last turn and is used in the main function. It is needed to keep track of how many
    times the simulation has been run.
    """
    @classmethod
    def get_last_turn(cls, file_name='simulation_data.csv'):
        if not os.path.exists(file_name):
            return 0
        with open(file_name, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                pass
            last_row = row
        last_turn = int(last_row[0]) if last_row else 0
        return last_turn
