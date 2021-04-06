########################################################
# Author:     Johnson Olusegun
# Course:     Advance CS topics (CSC 121, Spring 2021)
# Assignment: Italy & Covid reporting Assigment in 2020
# Python version: Python 3.8
########################################################

# Develop a user interface that shows region, population, case numbers and percentage
# PyQtWebEngine
# import map kit and folium
import sys
import io
import folium
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QHBoxLayout, QVBoxLayout, QPushButton, QComboBox,
                             QMessageBox, QDialog)
from PyQt5.QtGui import QFont, QPainter
import PyQt5.QtCore as qt
# import web engine widget
from PyQt5.QtWebEngineWidgets import QWebEngineView
# core module
from core import *

from pyqtlet import L, MapWidget


# main window

class MainWindow(QWidget):
    # constructor
    def __init__(self):
        super().__init__()
        # changing the background color to yellow
        # self.setStyleSheet("background-color: #ece2e1;color:#000;")
        # core
        self.core = Core()
        # list of italy regions
        self.italy_regions = self.core.get_region()
        # list of european region
        self.european_countries = self.core.get_european_countries()
        # initialSetup
        self.initialSetup()

    # initialSetup
    def initialSetup(self):
        # set title
        self.setWindowTitle("Italy Covid Report")
        # set window screen
        self.setFixedSize(1000, 400)
        # show content
        self.contentWidget()

        # show the window
        self.show()

    def contentWidget(self):
        # select region v box 1
        select_region_h_box1 = QHBoxLayout()
        # selection one notice
        select_region_h_box1.addSpacing(10)
        # selection label 1
        select_region_label = QLabel("Select Region", self)
        select_region_h_box1.addWidget(select_region_label)
        # drop down button
        self.select_region_combo = QComboBox(self)
        self.select_region_combo.addItems(self.italy_regions)
        select_region_h_box1.addWidget(self.select_region_combo)
        # push button
        select_region_botton = QPushButton("Check Region", self)
        select_region_botton.pressed.connect(self.italyRegionClicked)
        select_region_h_box1.addWidget(select_region_botton)

        # select region v box 2
        select_region_h_box2 = QHBoxLayout()
        select_region_h_box2.addSpacing(10)
        # selection label 1
        select_region_label = QLabel("Italy against", self)
        select_region_h_box2.addWidget(select_region_label)

        # drop down button (combo )
        self.select_euro_combo = QComboBox(self)
        self.select_euro_combo.addItems(self.european_countries)
        select_region_h_box2.addWidget(self.select_euro_combo)
        # push button
        compare_button = QPushButton("Compare", self)
        compare_button.pressed.connect(self.europeanCountriesClicked)
        select_region_h_box2.addWidget(compare_button)

        # selection main V box
        select_region_main_v_box = QVBoxLayout()
        italy_lbl = QLabel("Italy Region Covid Report", self)
        italy_lbl.setStyleSheet("border: 0.5px solid gray")
        select_region_main_v_box.addWidget(italy_lbl)
        select_region_main_v_box.addLayout(select_region_h_box1)
        select_region_main_v_box.setSpacing(15)
        euro_text = QLabel("Italy Covid report against European countries", self)
        euro_text.setStyleSheet("border: 0.5px solid gray")
        select_region_main_v_box.addWidget(euro_text)
        select_region_main_v_box.addLayout(select_region_h_box2)
        select_region_main_v_box.addStretch()

        # for region map and demographic
        region_map_box = QVBoxLayout()
        coordinate = (41.29246,12.5736108)
        m = folium.Map(
            tiles='Stamen Terrain',
            zoom_start=8,
            location=coordinate
        )

        # save map data to data object
        data = io.BytesIO()
        m.save(data, close_file=False)

        webView = QWebEngineView()
        webView.setHtml(data.getvalue().decode())
        region_map_box.addWidget(webView)

        # main box top - bottom
        h_box = QHBoxLayout()
        h_box.addLayout(select_region_main_v_box)
        h_box.addLayout(region_map_box)
        self.setLayout(h_box)

    # this method when clicked get and display region statistics
    # italyRegionClicked
    def italyRegionClicked(self):
        # check if value returned is not None
        if self.select_region_combo.currentText() is not None:
            stats = self.core.getRegionStats(self.select_region_combo.currentText())
            self.italyRegionStatistics(stats)
        else:
            self.errorMessage("Error getting region")

    # on clicked this method display the statistic between italy and euro countries
    # europeanCountriesClicked
    def europeanCountriesClicked(self):
        if self.select_euro_combo.currentText() is not None:
            # get italy stats
            italy_stats = self.core.getItalyStats("Italy")
            euro_stats = self.core.getEuropeanCountryStats(self.select_euro_combo.currentText())
            # display stats dialog
            self.compareStatisticsDialog(italy_stats, euro_stats)

        else:
            self.errorMessage("Error comparing countries")

    # for handling error message
    def errorMessage(self, message):
        QMessageBox().warning(self, "Unexpected Error", message, QMessageBox.Ok, QMessageBox.Ok)

    # display italy region statistics
    def italyRegionStatistics(self, stats):
        # create dialog
        regionDialog = QDialog(self)
        regionDialog.setFixedSize(390, 230)
        # set dialog title
        regionDialog.setWindowTitle(f"{stats['region']} Report".capitalize())
        # show region

        # dialog title
        d_title = QLabel(f"{stats['region']}", self)
        d_title.setFont(QFont('Times', 25, QFont.Light))
        d_title.setAlignment(qt.Qt.AlignCenter)
        # h rows
        r1_box = QHBoxLayout()
        r1_box.addStretch()
        region_label = QLabel('Region :', self)
        region_label.setFont(QFont('Times', 25, QFont.Light))
        region_text = QLabel(f"{stats['region']}", self)
        region_text.setFont(QFont('Times', 25, QFont.Light))
        r1_box.addWidget(region_label)
        r1_box.addWidget(region_text)
        r1_box.addStretch()

        # 2 h rows
        r2_box = QHBoxLayout()
        r2_box.addStretch()
        population_label = QLabel('Population :', self)
        population_label.setFont(QFont('Times', 25, QFont.Light))
        population_text = QLabel(f"{stats['population']}", self)
        population_text.setFont(QFont('Times', 25, QFont.Light))
        r2_box.addWidget(population_label)
        r2_box.addWidget(population_text)
        r2_box.addStretch()

        # 3 h rows
        r3_box = QHBoxLayout()
        r3_box.addStretch()
        region_population_label = QLabel('Region Population :', self)
        region_population_label.setFont(QFont('Times', 25, QFont.Light))
        region_population_text = QLabel(f"{stats['region_population']}", self)
        region_population_text.setFont(QFont('Times', 25, QFont.Light))
        r3_box.addWidget(region_population_label)
        r3_box.addWidget(region_population_text)
        r3_box.addStretch()

        # 4 h rows
        r4_box = QHBoxLayout()
        r4_box.addStretch()
        case_number_label = QLabel('Total Covid Case :', self)
        case_number_label.setFont(QFont('Times', 25, QFont.Light))
        case_number_text = QLabel(f"{stats['case_number']}", self)
        case_number_text.setFont(QFont('Times', 25, QFont.Light))
        r4_box.addWidget(case_number_label)
        r4_box.addWidget(case_number_text)
        r4_box.addStretch()

        # 5 h rows
        r5_box = QHBoxLayout()
        r5_box.addStretch()
        cal_percentage_label = QLabel('Percentage :', self)
        cal_percentage_label.setFont(QFont('Times', 25, QFont.Light))
        cal_percentage_text = QLabel(f"{stats['percentage']}%", self)
        cal_percentage_text.setFont(QFont('Times', 25, QFont.Light))
        r5_box.addWidget(cal_percentage_label)
        r5_box.addWidget(cal_percentage_text)
        r5_box.addStretch()

        # main v box
        main_v_box = QVBoxLayout()
        main_v_box.setSpacing(10)
        # add row 1
        main_v_box.addLayout(r1_box)
        # add row 2
        main_v_box.addLayout(r2_box)
        # add row 3
        main_v_box.addLayout(r3_box)
        # add row 4
        main_v_box.addLayout(r4_box)
        # add row 5
        main_v_box.addLayout(r5_box)
        main_v_box.addStretch()

        regionDialog.setLayout(main_v_box)
        regionDialog.exec_()

    # comparing italy and other european country
    def compareStatisticsDialog(self, italy_stats, euro_stats):
        # create dialog
        regionDialog = QDialog(self)
        regionDialog.setFixedSize(700, 300)
        # set dialog title
        regionDialog.setWindowTitle(f"{euro_stats['country']}")
        # show comparison
        # left and right v box
        left_v_box = QVBoxLayout()
        right_v_box = QVBoxLayout()

        # horizontal box

        # Left H box 1
        left_h_box_1 = QHBoxLayout()
        left_h_box_1.addStretch()
        country_lbl = QLabel("Country: ", self)
        country_lbl.setFont(QFont('Times', 20, QFont.Light))
        left_h_box_1.addWidget(country_lbl)
        country_text = QLabel(italy_stats['country'], self)
        country_text.setFont(QFont('Times', 20, QFont.Light))
        left_h_box_1.addWidget(country_text)
        left_h_box_1.addStretch()
        # add layout
        left_v_box.addLayout(left_h_box_1)

        # Right H box 1
        right_h_box_1 = QHBoxLayout()
        right_h_box_1.addStretch()
        euro_country_lbl = QLabel("Country: ", self)
        euro_country_lbl.setFont(QFont('Times', 20, QFont.Light))
        right_h_box_1.addWidget(euro_country_lbl)
        euro_country_text = QLabel(euro_stats['country'], self)
        euro_country_text.setFont(QFont('Times', 20, QFont.Light))
        right_h_box_1.addWidget(euro_country_text)
        right_h_box_1.addStretch()
        # add layout
        right_v_box.addLayout(right_h_box_1)

        # Left H box 2
        left_h_box_2 = QHBoxLayout()
        left_h_box_2.addStretch()
        population_lbl = QLabel("Total Population: ", self)
        population_lbl.setFont(QFont('Times', 20, QFont.Light))
        left_h_box_2.addWidget(population_lbl)
        population_text = QLabel(str(italy_stats['population']), self)
        population_text.setFont(QFont('Times', 20, QFont.Light))
        left_h_box_2.addWidget(population_text)
        left_h_box_2.addStretch()
        # add layout
        left_v_box.addLayout(left_h_box_2)

        # Right H box 2
        right_h_box_2 = QHBoxLayout()
        right_h_box_2.addStretch()
        euro_population_lbl = QLabel("Total Population: ", self)
        euro_population_lbl.setFont(QFont('Times', 20, QFont.Light))
        right_h_box_2.addWidget(euro_population_lbl)
        euro_population_text = QLabel(str(euro_stats['population']), self)
        euro_population_text.setFont(QFont('Times', 20, QFont.Light))
        right_h_box_2.addWidget(euro_population_text)
        right_h_box_2.addStretch()
        # add layout
        right_v_box.addLayout(right_h_box_2)

        # Left H box 3
        left_h_box_3 = QHBoxLayout()
        left_h_box_3.addStretch()
        case_lbl = QLabel("Total Case: ", self)
        case_lbl.setFont(QFont('Times', 20, QFont.Light))
        left_h_box_3.addWidget(case_lbl)
        case_text = QLabel(str(italy_stats['case']), self)
        case_text.setFont(QFont('Times', 20, QFont.Light))
        left_h_box_3.addWidget(case_text)
        left_h_box_3.addStretch()
        # add layout
        left_v_box.addLayout(left_h_box_3)

        # Right H box 3
        right_h_box_3 = QHBoxLayout()
        right_h_box_3.addStretch()
        euro_case_lbl = QLabel("Total Case: ", self)
        euro_case_lbl.setFont(QFont('Times', 20, QFont.Light))
        right_h_box_3.addWidget(euro_case_lbl)
        euro_case_text = QLabel(str(euro_stats['case']), self)
        euro_case_text.setFont(QFont('Times', 20, QFont.Light))
        right_h_box_3.addWidget(euro_case_text)
        right_h_box_3.addStretch()
        # add layout
        right_v_box.addLayout(right_h_box_3)

        # Left H box 4
        left_h_box_4 = QHBoxLayout()
        left_h_box_4.addStretch()
        rate_lbl = QLabel("Infection Rate: ", self)
        rate_lbl.setFont(QFont('Times', 20, QFont.Light))
        left_h_box_4.addWidget(rate_lbl)
        rate_text = QLabel(str(italy_stats['rate']), self)
        rate_text.setFont(QFont('Times', 20, QFont.Light))
        left_h_box_4.addWidget(rate_text)
        left_h_box_4.addStretch()
        # add layout
        left_v_box.addLayout(left_h_box_4)

        # Right H box 4
        right_h_box_4 = QHBoxLayout()
        right_h_box_4.addStretch()
        euro_rate_lbl = QLabel("Infection Rate: ", self)
        euro_rate_lbl.setFont(QFont('Times', 20, QFont.Light))
        right_h_box_4.addWidget(euro_rate_lbl)
        euro_rate_text = QLabel(str(euro_stats['rate']), self)
        euro_rate_text.setFont(QFont('Times', 20, QFont.Light))
        right_h_box_4.addWidget(euro_rate_text)
        right_h_box_4.addStretch()
        # add layout
        right_v_box.addLayout(right_h_box_4)

        # inner h box
        second_main_h_box = QHBoxLayout()
        # add right and left v box
        second_main_h_box.addLayout(left_v_box)
        second_main_h_box.addLayout(right_v_box)

        # main v box
        main_v_box = QVBoxLayout()
        # set main title
        main_v_title = QLabel(f"Comparison reports between Italy and {euro_stats['country']}", self)
        main_v_title.setFont(QFont('Times', 20, QFont.Bold))
        main_v_title.setAlignment(qt.Qt.AlignCenter)

        main_v_box.addWidget(main_v_title)
        main_v_box.addSpacing(30)

        # add second_main_h_box
        main_v_box.addLayout(second_main_h_box)
        # push everything to the top
        main_v_box.addStretch()
        # set main layout
        regionDialog.setLayout(main_v_box)

        regionDialog.exec_()


if __name__ == "__main__":
    # main application
    app = QApplication(sys.argv)
    app.setStyleSheet('''
            QWidget {
                font-size: 20px;
                font-family:Times;
            }
        ''')
    mw = MainWindow()
    sys.exit(app.exec_())
