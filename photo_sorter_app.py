from PyQt5.QtWidgets import QApplication
from config_manager import ConfigManager
from gui_manager import GUIManager
from file_manager import FileManager

class PhotoSorterApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.config_manager = ConfigManager("config.cfg")
        self.file_manager = FileManager()
        self.gui_manager = GUIManager(self)
        # Setup e inizializzazione dell'applicazione

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = PhotoSorterApp()
    sys.exit(app.exec_())
