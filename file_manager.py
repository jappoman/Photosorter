# file_manager.py
import os
import shutil
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from geopy.distance import distance
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from time import sleep

class FileManager:
    def __init__(self, config_manager):
        self.config_manager = config_manager
        self.geolocator = Nominatim(user_agent="photo_sorter")
        self.char_to_replace = {"\\": "_", "/": "_", ":": "_", "\"": "_"}
        
    def get_exif(self, filename):
        """Estrae i metadati EXIF da un file immagine."""
        if filename.lower().endswith('.jpg') or filename.lower().endswith('.jpeg'):
            image = Image.open(filename)
            image.verify()
            return image._getexif()
        else:
            return None

    def get_geotagging(self, exif):
        """Estrae i dati geografici dai metadati EXIF."""
        if not exif:
            return None

        geotagging = {}
        for (idx, tag) in TAGS.items():
            if tag == 'GPSInfo':
                if idx not in exif:
                    return None
                for (key, val) in GPSTAGS.items():
                    if key in exif[idx]:
                        geotagging[val] = exif[idx][key]
        return geotagging

    def dms_to_dd(self, gps_coords, gps_coords_ref):
        """Converte coordinate GPS da gradi, minuti, secondi a gradi decimali."""
        d, m, s = gps_coords
        dd = d + (m / 60.0) + (s / 3600.0)
        if gps_coords_ref.upper() in ['S', 'W']:
            dd *= -1
        return dd

    # Aggiungi qui altre funzioni necessarie, come il metodo per ordinare le foto
    
    def sort_photos(self, source_dir, destination_dir):
        """Organizza le foto nel directory di destinazione."""
        # Implementa qui la logica per ordinare le foto basandoti sui metadati EXIF e sulle preferenze dell'utente.
        pass
