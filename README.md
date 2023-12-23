# Agent-based Modeling of the Spread of a Disease

This project is an educational tool designed for an exercise in agent-based modeling and AI behavior within a simulated environment. It aims to provide a graphical representation of the spread of a disease within a confined population, demonstrating the impact of infection rates, vaccination rates, and individual behavior. This simulation is intentionally abstract and should not be considered a realistic model of disease spread. Rather, it serves as a platform for exploring the fundamentals of artificial intelligence in a controlled setting.

Each individual in the simulation is an AI agent with randomly generated attributes such as age, gender, and pre-existing health conditions. Users can customize input parameters, including the number of healthy and sick individuals, the behavior of the individuals (SmartAI or AvoidingAI), and the number of Doctors, Vaccinators, and Builders. Disease parameters such as infection chance, death chance, incubation duration, recovery duration, and vaccination rate are also adjustable.

Upon completion of the simulation, a comprehensive set of statistics is provided, which includes counts of the dead, infected, recovered, vaccinated, and cured, as well as various rates like mortality, infection, recovery, vaccination, and cured rates. The simulation data is automatically saved to an external file that is updated with each simulation run.

## Directory Structure
- The repository is divided into a directory containing the program's code and a directory containing the project documents. The technical document, in particular, can be consulted for a better understanding of the simulation's mechanics.

## Properties of the Simulation
- Customizable input parameters for simulating various population and disease scenarios.
- Adjustable disease parameters to explore different outcomes and strategies.
- AI agents with individual attributes providing diverse agent behavior within the simulation.
- A grid-based simulation environment that visualizes the movement and interactions of individuals.
- Real-time updates on the health status of individuals.
- Detailed statistics on the simulation results, offering insights into the dynamics of the disease spread.
- Automated data saving for analysis and review.
- Testing of all AI types, the disease logic, and the CSV file writing process.

## User Instructions
1. Clone the repository or download the source code.
2. Install the necessary dependencies (e.g., PyQt6).
3. Execute the `main.py` script to launch the simulation.
4. Enter the desired parameters and click the "Submit" button to start the simulation.
5. Watch the simulation unfold in the grid-based environment and track the real-time status updates of the individuals.
6. Review the post-simulation statistics to gain insights into the impact of the disease on the simulated population.

## Acknowledgments

This project is developed as the final project in the cource CS-A1121 Basics in Programming Y2 at Aalto University in 2023. The responsible teacher for the course was Sanna Suoranta, and the project advisor was Mondal Shubham.

## Licence
This project is licensed under the terms of the MIT license. It can be found in the file LICENSE.txt.
