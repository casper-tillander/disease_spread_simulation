from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPainter
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout
from PyQt6.QtCharts import QChart, QChartView, QPieSeries
from PyQt6.QtCharts import QBarSet, QBarSeries, QBarCategoryAxis, QValueAxis

"""
This class builds the Statistics window that is shown after the simulation has run.
"""

class StatsWindow(QWidget):
    def __init__(self, gender_count, smoker_count, pre_existing_conditions_count, lifestyle_count,
                 mortality_rate, infection_rate, recovery_rate, vaccination_rate, cured_rate):
        super().__init__()
        self.setWindowTitle("Simulation Statistics")
        self.setGeometry(50, 50, 800, 620)

        layout = QVBoxLayout()
        self.setLayout(layout)

        title_label = QLabel("Disease Simulation Statistics")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        grid_layout = QGridLayout()
        layout.addLayout(grid_layout)

        label_font = QFont()
        label_font.setPointSize(10)

        def create_rates_chart(title, data):
            bar_set = QBarSet(title)

            categories = []
            for key, value in data.items():
                bar_set.append(value * 100)  # Convert to percentages
                categories.append(f"{key} ({value * 100:.2f}%)")

            bar_series = QBarSeries()
            bar_series.append(bar_set)

            chart = QChart()
            chart.addSeries(bar_series)
            chart.setTitle(title)

            axis_x = QBarCategoryAxis()
            axis_x.append(categories)
            chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
            bar_series.attachAxis(axis_x)

            axis_y = QValueAxis()
            axis_y.setRange(0, 100)  # Set Y-axis range to 0-100 for percentages
            axis_y.setLabelFormat("%.2f%%")
            chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)
            bar_series.attachAxis(axis_y)

            chart.legend().setVisible(False)

            chart_view = QChartView(chart)
            chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
            chart_view.setFixedSize(800, 200)

            return chart_view

        def create_pie_chart(title, data):
            series = QPieSeries()
            for key, value in data.items():
                series.append(f"{key} ({value})", value)

            chart = QChart()
            chart.addSeries(series)
            chart.setTitle(title)
            chart.legend().setVisible(True)
            chart.legend().setAlignment(Qt.AlignmentFlag.AlignBottom)

            chart_view = QChartView(chart)
            chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
            chart_view.setFixedSize(390, 150)

            return chart_view

        rates_data = {
            "Mortality": mortality_rate,
            "Infection": infection_rate,
            "Recovery": recovery_rate,
            "Vaccination": vaccination_rate,
            "Cured": cured_rate
        }
        grid_layout.addWidget(create_rates_chart("Disease statistics", rates_data), 0, 0, 1, 2)

        gender_data = {"Male": gender_count["male"], "Female": gender_count["female"]}
        grid_layout.addWidget(create_pie_chart("Gender", gender_data), 1, 0)

        smoker_data = {"Smoker": smoker_count["smoker"], "Non-Smoker": smoker_count["non-smoker"]}
        grid_layout.addWidget(create_pie_chart("Smoking Status", smoker_data), 1, 1)

        pre_existing_conditions_data = pre_existing_conditions_count
        grid_layout.addWidget(create_pie_chart("Pre-existing Conditions", pre_existing_conditions_data), 2, 0)

        lifestyle_data = lifestyle_count
        grid_layout.addWidget(create_pie_chart("Lifestyles", lifestyle_data), 2, 1)

        self.setStyleSheet('''
                                  QWidget {
                                      font-size: 15px;
                                  }
                                  QLabel {
                                      font-weight: bold;
                                  }
                                  QChartView {
                                      border: 2px solid #606060;
                                      border-radius: 10px;
                                      background-color: #f0f0f0;
                                  }
                                   ''')




