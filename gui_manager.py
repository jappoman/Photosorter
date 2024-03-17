from PyQt5.QtWidgets import (
    QMainWindow, QPushButton, QLineEdit, QLabel, QDesktopWidget,
    QFileDialog, QProgressBar, QCheckBox, QApplication,
    QVBoxLayout, QHBoxLayout, QWidget, QScrollArea, QGroupBox
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
        self.setWindowTitle("Photosorter v2.0")
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

        # Source directory layout
        scrollLayout.addWidget(QLabel("Insert source directory path:"))
        sourceLayout = QHBoxLayout()  # Layout orizzontale per la directory sorgente
        textbox_sourcedir = QLineEdit()
        textbox_sourcedir.setPlaceholderText("Source directory path")
        sourceLayout.addWidget(textbox_sourcedir)  # Aggiunge la casella di testo al layout orizzontale
        button_sourcedir = QPushButton("...")
        sourceLayout.addWidget(button_sourcedir)  # Aggiunge il bottone al layout orizzontale
        scrollLayout.addLayout(sourceLayout)  # Aggiunge il layout orizzontale al layout principale
        button_sourcedir.clicked.connect(self.on_click_sourcedir_button)

        # Destination directory layout
        scrollLayout.addWidget(QLabel("Insert destination directory path:"))
        destLayout = QHBoxLayout()  # Layout orizzontale per la directory di destinazione
        textbox_destdir = QLineEdit()
        textbox_destdir.setPlaceholderText("Destination directory path")
        destLayout.addWidget(textbox_destdir)  # Aggiunge la casella di testo al layout orizzontale
        button_destdir = QPushButton("...")
        destLayout.addWidget(button_destdir)  # Aggiunge il bottone al layout orizzontale
        scrollLayout.addLayout(destLayout)  # Aggiunge il layout orizzontale al layout principale
        button_destdir.clicked.connect(self.on_click_destdir_button)

        # Places directory layout
        scrollLayout.addWidget(QLabel("Insert known places file path:"))
        placesLayout = QHBoxLayout()  # Layout orizzontale per il file dei places
        textbox_placespath = QLineEdit()
        textbox_placespath.setPlaceholderText("Known places file path")
        placesLayout.addWidget(textbox_placespath)  # Aggiunge la casella di testo al layout orizzontale
        button_placespath = QPushButton("...")
        placesLayout.addWidget(button_placespath)  # Aggiunge il bottone al layout orizzontale
        scrollLayout.addLayout(placesLayout)  # Aggiunge il layout orizzontale al layout principale
        button_placespath.clicked.connect(self.on_click_placesfilepath_button)

        # Home Location section
        groupBoxHomeLocation = QGroupBox("Home Location")  # Gruppo con titolo
        homeLocationLayout = QVBoxLayout()  # QVBoxLayout per gli elementi interni
        latLayout = QHBoxLayout()
        latLayout.addWidget(QLabel("Latitude:"))
        textbox_homelat = QLineEdit()
        textbox_homelat.setPlaceholderText("Home location (latitude)")
        latLayout.addWidget(textbox_homelat)
        lonLayout = QHBoxLayout()
        lonLayout.addWidget(QLabel("Longitude:"))
        textbox_homelon = QLineEdit()
        textbox_homelon.setPlaceholderText("Home location (longitude)")
        lonLayout.addWidget(textbox_homelon)
        # Aggiungi i layout di latitudine e longitudine al layout del gruppo
        homeLocationLayout.addLayout(latLayout)
        homeLocationLayout.addLayout(lonLayout)
        groupBoxHomeLocation.setLayout(homeLocationLayout)  # Imposta il layout del gruppo
        scrollLayout.addWidget(groupBoxHomeLocation)  # Aggiungi il gruppo al layout principale

        # Space explaination
        scrollLayout.addWidget(QLabel("Pics far away X kms from each others and Y kms away from home are put together.\nZ are the kms away from home where to start the calculation about space."))

        # Space layout
        spaceLayout = QHBoxLayout()
        spaceLayout.addWidget(QLabel("(X) kms between pics:"))
        textbox_xpsace = QLineEdit()
        textbox_xpsace.setPlaceholderText("2")
        spaceLayout.addWidget(textbox_xpsace)
        spaceLayout.addWidget(QLabel("(Y) kms from home:"))
        textbox_ypsace = QLineEdit()
        textbox_ypsace.setPlaceholderText("10")
        spaceLayout.addWidget(textbox_ypsace)
        spaceLayout.addWidget(QLabel("(Z) kms where to start:"))
        textbox_zpsace = QLineEdit()
        textbox_zpsace.setPlaceholderText("1")
        spaceLayout.addWidget(textbox_zpsace)
        scrollLayout.addLayout(spaceLayout)

        # Time explaination
        scrollLayout.addWidget(QLabel("Pics far away X seconds from each others and Y kms away from home are put together.\nZ are the seconds when to start the calculation about time."))

        # Time layout
        timeLayout = QHBoxLayout()
        timeLayout.addWidget(QLabel("(X) sec between pics:"))
        textbox_xtime = QLineEdit()
        textbox_xtime.setPlaceholderText("3600")
        timeLayout.addWidget(textbox_xtime)
        timeLayout.addWidget(QLabel("(Y) kms from home:"))
        textbox_ytime = QLineEdit()
        textbox_ytime.setPlaceholderText("10")
        timeLayout.addWidget(textbox_ytime)
        timeLayout.addWidget(QLabel("(Z) sec when to start:"))
        textbox_ztime = QLineEdit()
        textbox_ztime.setPlaceholderText("3600")
        timeLayout.addWidget(textbox_ztime)
        scrollLayout.addLayout(timeLayout)




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
