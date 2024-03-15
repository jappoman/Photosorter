# config_manager.py
import configparser
import os

class ConfigManager:
    def __init__(self, config_file_path):
        self.config_file_path = config_file_path
        self.config = configparser.ConfigParser()
        self.load_config()

    def load_config(self):
        """Carica il file di configurazione."""
        if os.path.exists(self.config_file_path):
            self.config.read(self.config_file_path)
        else:
            print(f"File di configurazione non trovato: {self.config_file_path}")
            # Qui puoi decidere di creare un file di configurazione di default
            # o semplicemente lasciare il config vuoto
            # Esempio di creazione di un file di configurazione di default:
            self.create_default_config()
            self.save_config()

    def create_default_config(self):
        """Crea una configurazione di default se il file non esiste."""
        self.config['Directories'] = {'source_dir': '', 'destination_dir': ''}
        self.config['Places'] = {'places_file_path': ''}
        self.config['Home'] = {'home_lat': '0', 'home_lon': '0'}
        self.config['Space'] = {'x_space': '2', 'y_space': '10', 'z_space': '1'}
        self.config['Time'] = {'x_time': '3600', 'y_time': '10', 'z_time': '3600'}
        # Aggiungi altre sezioni di default secondo necessità

    def save_config(self):
        """Salva le modifiche apportate al file di configurazione."""
        with open(self.config_file_path, 'w') as configfile:
            self.config.write(configfile)

    def get(self, section, option, fallback=None):
        """Restituisce il valore della configurazione richiesta, con un valore di fallback opzionale."""
        return self.config.get(section, option, fallback=fallback)

    def set(self, section, option, value):
        """Imposta un valore nella configurazione. Crea la sezione se non esiste."""
        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config.set(section, option, value)
