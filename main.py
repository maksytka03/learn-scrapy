import os.path
from os import walk
import sys
from subprocess import call

from PyQt6.QtCore import Qt, QThread
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QMainWindow,
    QLabel,
    QPushButton,
    QGridLayout,
    QFileDialog,
    QComboBox,
    QScrollArea,
    QVBoxLayout,
    QLineEdit,
)
from PyQt6.QtGui import QFont, QFontDatabase

class Scraper(QThread):
    def __init__(self, directory, command):
        super().__init__()
        self._directory = directory
        self._command = command

    def run(self):
        os.chdir(self._directory)
        os.system(self._command)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Scraper")
        self.setFixedSize(700, 500)

        font_id = QFontDatabase.addApplicationFont(
            os.path.abspath("GabaritoFont/Gabarito-VariableFont_wght.ttf")
        )
        self.font_family = QFontDatabase.applicationFontFamilies(font_id)

        layout = QGridLayout()
        central_widget = QWidget()

        greet_label = QLabel("Welcome to the Web Scraper command center!")
        greet_label.setFont(QFont(self.font_family[0], 24))
        greet_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        info_label = QLabel("Here you can control your Scrapy spiders.")
        info_label.setFont(QFont(self.font_family[0], 14))
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        start_scraping_button = QPushButton("Start Scraping")
        start_scraping_button.setFont(QFont(self.font_family[0], 16))
        start_scraping_button.clicked.connect(self.start_scraping)

        stop_scraping_button = QPushButton("Stop Scraping")
        stop_scraping_button.setFont(QFont(self.font_family[0], 16))
        stop_scraping_button.clicked.connect(self.stop_scraping)

        self.scraping_status_label = QLabel("")
        self.scraping_status_label.setFont(QFont(self.font_family[0], 16))
        self.scraping_status_label.setVisible(False)

        self.command_line_edit = QLineEdit()
        self.command_line_edit.setPlaceholderText("Enter spider's name to "
                                                  "crawl...")

        layout.addWidget(greet_label, 0, 0)
        layout.addWidget(info_label, 1, 0)
        layout.addWidget(self.scraping_status_label, 2, 0)
        layout.addWidget(self.command_line_edit, 3, 0, 2, 0)
        layout.addWidget(start_scraping_button, 4, 0)
        layout.addWidget(stop_scraping_button, 5, 0)

        self.setCentralWidget(central_widget)
        self.centralWidget().setLayout(layout)

    # TODO: SCRAPE BRICKSET.COM

    def start_scraping(self):
        current_dir = (
            "C:\\Users\\Pavlo\\PycharmProjects\\learnScrapyTutorial"
            "\\tutorial\\tutorial")
        command_input = self.command_line_edit.text()
        if command_input:
            command = f"scrapy crawl {self.command_line_edit.text().strip().lower()}"
            self.scraper = Scraper(current_dir, command)
            self.scraper.finished.connect(self.scraping_finished)
            self.scraper.start()

    def stop_scraping(self):
        self.scraping_status_label.setText("Scraping Stopped")
        self.scraper.terminate()
        self.scraping_status_label.setVisible(True)

    def scraping_finished(self):
        self.scraping_status_label.setText("Scraping Finished")
        del self.scraper
        self.scraping_status_label.setVisible(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
