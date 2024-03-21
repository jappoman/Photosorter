import configparser


class ConfigManager:
    def __init__(self, config_file_path="config.cfg"):
        self.config_file_path = config_file_path
        self.config = configparser.ConfigParser()
        self.load_config()

    def load_config(self):
        """Carica le impostazioni dal file di configurazione."""
        try:
            self.config.read_file(open(self.config_file_path))
        except FileNotFoundError:
            print(
                f"Il file di configurazione {self.config_file_path} non è stato trovato."
            )
            # Qui potresti anche creare un file di configurazione di default o gestire l'errore in altro modo.

    def get_setting(self, section, setting):
        """Restituisce il valore di una impostazione specifica."""
        try:
            return self.config.get(section, setting)
        except (configparser.NoSectionError, configparser.NoOptionError) as e:
            print(
                f"Errore nella lettura di {section} {setting} dal file di configurazione: {e}"
            )
            return None

    def update_setting(self, section, setting, value):
        """Aggiorna un'impostazione nel file di configurazione."""
        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config.set(section, setting, value)
        with open(self.config_file_path, "w") as configfile:
            self.config.write(configfile)
