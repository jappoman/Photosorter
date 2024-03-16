from PyQt5.QtWidgets import (
    QMainWindow, QPushButton, QLineEdit, QLabel, QDesktopWidget,
    QFileDialog, QProgressBar, QCheckBox, QApplication,
    QVBoxLayout, QHBoxLayout, QWidget, QScrollArea
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, pyqtSignal
import sys


class App(QMainWindow):

    startSortingSignal = pyqtSignal()

    def __init__(self, config):
        super().__init__()
        self.config = config
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Photosorter v1.1")
        self.setWindowIcon(QIcon(":/icon.ico"))

        # Utilizza QVBoxLayout e QHBoxLayout per organizzare i widget
        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)
        mainLayout = QVBoxLayout(centralWidget)

        # Scroll Area
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scrollContent = QWidget(scroll)

        # Scroll Area Layout
        scrollLayout = QVBoxLayout(scrollContent)
        scrollContent.setLayout(scrollLayout)

        # Source directory
        scrollLayout.addWidget(QLabel("Insert source directory path:"))
        scrollLayout.addWidget(QLineEdit().setPlaceholderText("Source directory path"))
        textbox_sourcedir = QLineEdit()
        textbox_sourcedir.setPlaceholderText("Source directory path")
        scrollLayout.addWidget(textbox_sourcedir)
        button_sourcedir = QPushButton("...")
        scrollLayout.addWidget(button_sourcedir)
        button_sourcedir.clicked.connect(self.on_click_sourcedir_button)

        # Destination directory
        scrollLayout.addWidget(QLabel("Insert destination directory path:"))
        scrollLayout.addWidget(QLineEdit().setPlaceholderText("Destination directory path"))
        textbox_destdir = QLineEdit()
        textbox_destdir.setPlaceholderText("Destination directory path")
        scrollLayout.addWidget(textbox_destdir)
        button_destdir = QPushButton("...")
        scrollLayout.addWidget(button_destdir)
        button_destdir.clicked.connect(self.on_click_destdir_button)

        # Aggiungi altri widget qui...


        




        scroll.setWidget(scrollContent)
        mainLayout.addWidget(scroll)

        # Ridimensionabile e reattivo
        self.setMinimumSize(640, 480)  # Imposta una dimensione minima per la finestra principale

        

    def closeEvent(self, event):
        # when closing, kill the program
        sys.exit()

    @pyqtSlot()
    def on_click_start(self):
        # disable all the buttons and textbox when the app start
        ui_elements = [
            self.textbox_sourcedir, self.button_sourcedir,
            self.textbox_destdir, self.button_destdir,
            self.textbox_placesfilepath, self.button_placesfilepath,
            self.textbox_homelat, self.textbox_homelon,
            self.textbox_xpsace, self.textbox_ypsace, self.textbox_zpsace,
            self.textbox_xtime, self.textbox_ytime, self.textbox_ztime,
            self.button_start, self.check_dictionarymode, self.check_movefile
        ]

        for element in ui_elements:
            element.setEnabled(False)

        self.startSortingSignal.emit()

    def on_click_sourcedir_button(self):
        # set source dir from dialog
        fileName = str(QFileDialog.getExistingDirectory(self, "Select directory"))
        if fileName:
            self.textbox_sourcedir.setText(fileName)

    def on_click_destdir_button(self):
        # set destination dir from dialog
        fileName = str(QFileDialog.getExistingDirectory(self, "Select directory"))
        if fileName:
            self.textbox_destdir.setText(fileName)

    def on_click_placesfilepath_button(self):
        # set destination dir from dialog
        fileName, _ = QFileDialog.getOpenFileName(
            self, "Open places.txt file", "", "Text file (*.txt)"
        )
        if fileName:
            self.textbox_placesfilepath.setText(fileName)
