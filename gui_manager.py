# gui_manager.py
from PyQt5.QtWidgets import QMainWindow, QLabel, QLineEdit, QPushButton, QProgressBar, QCheckBox, QFileDialog, QApplication, QDesktopWidget
from PyQt5.QtCore import pyqtSlot

class GUIManager:
    def __init__(self, main_window):
        self.main_window = main_window

    def setup_ui(self, main_window):
        main_window.setWindowTitle("Photosorter")
        main_window.setFixedSize(800, 600)

        # Centra la finestra sullo schermo
        qtRectangle = main_window.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        main_window.move(qtRectangle.topLeft())

        # Aggiungi qui la creazione e la disposizione dei widget

        # Esempio: Bottone per selezionare la directory sorgente
        self.button_sourcedir = QPushButton('Select Source Directory', main_window)
        self.button_sourcedir.move(50, 50)
        self.button_sourcedir.clicked.connect(self.on_click_sourcedir)

        # Continua ad aggiungere widget come necessario

    @pyqtSlot()
    def on_click_sourcedir(self):
        dir_path = QFileDialog.getExistingDirectory(self.main_window, "Select Directory")
        if dir_path:
            # Aggiorna il percorso della directory sorgente
            print("Selected directory:", dir_path)
            # Aggiorna un QLineEdit o un QLabel con il percorso selezionato
            # self.lineedit_sourcedir.setText(dir_path)
    
    # Aggiungi altri slot per gestire eventi dai widget della GUI
    
    def load_config(self, config):
        """Carica i valori della configurazione nei widget della GUI."""
        # Qui potresti voler impostare i valori dei widget della GUI
        # basandoti sulla configurazione caricata, ad esempio:
        # self.lineedit_sourcedir.setText(config.get('Directories', 'source_dir'))
        pass
    
    def disable_ui(self):
        """Disabilita l'interfaccia utente durante l'esecuzione di operazioni lunghe."""
        pass
    
    def enable_ui(self):
        """Riabilita l'interfaccia utente al termine delle operazioni."""
        pass

    def signal_connect(self, handler_function):
        """Connette i segnali dei widget della GUI alle funzioni handler."""
        # Ad esempio, connettere un bottone a una funzione specifica:
        # self.button_start.clicked.connect(handler_function)
        pass
