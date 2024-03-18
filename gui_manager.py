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
        groupSourceDirectoryPath = QGroupBox("Source directory path")  # Gruppo con titolo
        horizontalSourceLayout = QHBoxLayout()  # Layout orizzontale per la directory sorgente
        textbox_sourcedir = QLineEdit()
        textbox_sourcedir.setPlaceholderText("Insert source directory path")
        horizontalSourceLayout.addWidget(textbox_sourcedir)  # Aggiunge la casella di testo al layout orizzontale
        button_sourcedir = QPushButton("...")
        button_sourcedir.clicked.connect(self.on_click_sourcedir_button)
        horizontalSourceLayout.addWidget(button_sourcedir)  # Aggiunge il bottone al layout orizzontale
        groupSourceDirectoryPath.setLayout(horizontalSourceLayout)  # Imposta il layout del gruppo
        scrollLayout.addWidget(groupSourceDirectoryPath)  # Aggiungi il gruppo al layout principale

        # Destination directory layout
        groupDestinationDirectoryPath = QGroupBox("Destination directory path")  # Gruppo con titolo
        horizontalDestinationLayout = QHBoxLayout()  # Layout orizzontale per la directory di destinazione
        textbox_destdir = QLineEdit()
        textbox_destdir.setPlaceholderText("Insert destination directory path")
        horizontalDestinationLayout.addWidget(textbox_destdir)  # Aggiunge la casella di testo al layout orizzontale
        button_destdir = QPushButton("...")
        button_destdir.clicked.connect(self.on_click_destdir_button)
        horizontalDestinationLayout.addWidget(button_destdir)  # Aggiunge il bottone al layout orizzontale
        groupDestinationDirectoryPath.setLayout(horizontalDestinationLayout)
        scrollLayout.addWidget(groupDestinationDirectoryPath)  # Aggiunge il layout orizzontale al layout principale

        # Places directory layout
        groupKnownPlacesPath = QGroupBox("Known places file path")  # Gruppo con titolo
        horizontalPlacesLayout = QHBoxLayout()  # Layout orizzontale per il file dei places
        textbox_placespath = QLineEdit()
        textbox_placespath.setPlaceholderText("Insert known places file path")
        horizontalPlacesLayout.addWidget(textbox_placespath)  # Aggiunge la casella di testo al layout orizzontale
        button_placespath = QPushButton("...")
        button_placespath.clicked.connect(self.on_click_placesfilepath_button)
        horizontalPlacesLayout.addWidget(button_placespath)  # Aggiunge il bottone al layout orizzontale
        groupKnownPlacesPath.setLayout(horizontalPlacesLayout)
        scrollLayout.addWidget(groupKnownPlacesPath)  # Aggiunge il layout orizzontale al layout principale

        # Home Location section
        groupBoxHomeLocation = QGroupBox("Home Location")  # Gruppo con titolo
        homeLocationLayout = QVBoxLayout()  # QVBoxLayout per gli elementi interni
        latLayout = QHBoxLayout()
        latLayout.addWidget(QLabel("Latitude:"))
        textbox_homelat = QLineEdit()
        textbox_homelat.setPlaceholderText("Insert home location latitude")
        latLayout.addWidget(textbox_homelat)
        lonLayout = QHBoxLayout()
        lonLayout.addWidget(QLabel("Longitude:"))
        textbox_homelon = QLineEdit()
        textbox_homelon.setPlaceholderText("Insert home location longitude")
        lonLayout.addWidget(textbox_homelon)
        # Aggiungi i layout di latitudine e longitudine al layout del gruppo
        homeLocationLayout.addLayout(latLayout)
        homeLocationLayout.addLayout(lonLayout)
        groupBoxHomeLocation.setLayout(homeLocationLayout)  # Imposta il layout del gruppo
        scrollLayout.addWidget(groupBoxHomeLocation)  # Aggiungi il gruppo al layout principale



        # Space Options section aggiornata
        groupBoxSpaceOptions = QGroupBox("Space Options")
        spaceOptionsLayout = QVBoxLayout()

        # Descrizione dello spazio
        spaceExplanationLabel = QLabel("Pics far away X kms from each others and Y kms away from home are put together.\nZ are the kms away from home where to start the calculation about space.")
        spaceOptionsLayout.addWidget(spaceExplanationLabel)

        # Campi X, Y, Z su una riga
        spaceFieldsLayout = QHBoxLayout()
        spaceFieldsLayout.addWidget(QLabel("(X) kms between pics:"))
        textbox_xspace = QLineEdit()
        textbox_xspace.setPlaceholderText("2")
        spaceFieldsLayout.addWidget(textbox_xspace)
        spaceFieldsLayout.addWidget(QLabel("(Y) kms from home:"))
        textbox_yspace = QLineEdit()
        textbox_yspace.setPlaceholderText("10")
        spaceFieldsLayout.addWidget(textbox_yspace)
        spaceFieldsLayout.addWidget(QLabel("(Z) kms where to start:"))
        textbox_zspace = QLineEdit()
        textbox_zspace.setPlaceholderText("1")
        spaceFieldsLayout.addWidget(textbox_zspace)

        spaceOptionsLayout.addLayout(spaceFieldsLayout)
        groupBoxSpaceOptions.setLayout(spaceOptionsLayout)
        scrollLayout.addWidget(groupBoxSpaceOptions)

        # Time Options section aggiornata
        groupBoxTimeOptions = QGroupBox("Time Options")
        timeOptionsLayout = QVBoxLayout()

        # Descrizione del tempo
        timeExplanationLabel = QLabel("Pics far away X seconds from each others and Y kms away from home are put together.\nZ are the seconds when to start the calculation about time.")
        timeOptionsLayout.addWidget(timeExplanationLabel)

        # Campi X, Y, Z su una riga
        timeFieldsLayout = QHBoxLayout()
        timeFieldsLayout.addWidget(QLabel("(X) sec between pics:"))
        textbox_xtime = QLineEdit()
        textbox_xtime.setPlaceholderText("3600")
        timeFieldsLayout.addWidget(textbox_xtime)
        timeFieldsLayout.addWidget(QLabel("(Y) kms from home:"))
        textbox_ytime = QLineEdit()
        textbox_ytime.setPlaceholderText("10")
        timeFieldsLayout.addWidget(textbox_ytime)
        timeFieldsLayout.addWidget(QLabel("(Z) sec when to start:"))
        textbox_ztime = QLineEdit()
        textbox_ztime.setPlaceholderText("3600")
        timeFieldsLayout.addWidget(textbox_ztime)

        timeOptionsLayout.addLayout(timeFieldsLayout)
        groupBoxTimeOptions.setLayout(timeOptionsLayout)
        scrollLayout.addWidget(groupBoxTimeOptions)





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
