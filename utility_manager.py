import datetime
from PIL import Image
from PIL.ExifTags import TAGS
from PIL.ExifTags import GPSTAGS
from geopy.exc import GeocoderTimedOut
from time import sleep


def get_exif(filename):
    if filename.endswith(".jpg"):
        image = Image.open(filename)
        image.verify()
        return image._getexif()
    else:
        return False


def get_labeled_exif(exif):
    labeled = {}
    for key, val in exif.items():
        labeled[TAGS.get(key)] = val
    return labeled


def get_geotagging(exif):
    if not exif:
        return "No EXIF metadata found"
        # raise ValueError("No EXIF metadata found")

    geotagging = {}
    for idx, tag in TAGS.items():
        if tag == "GPSInfo":
            if idx not in exif:
                return "No EXIF geotagging found"
                # raise ValueError("No EXIF geotagging found")
            try:
                for key, val in GPSTAGS.items():
                    if key in exif[idx]:
                        geotagging[val] = exif[idx][key]
            except GeocoderTimedOut:
                sleep(1)
                get_geotagging(exif)

    return geotagging


def dms_to_dd(gps_coords, gps_coords_ref):
    d, m, s = gps_coords
    dd = d + m / 60 + s / 3600
    if gps_coords_ref.upper() in ("S", "W"):
        return -dd
    elif gps_coords_ref.upper() in ("N", "E"):
        return dd
    else:
        raise RuntimeError("Incorrect gps_coords_ref {}".format(gps_coords_ref))


def hour_between(d1, d2):
    d1 = datetime.datetime.strptime(d1, "%Y-%m-%d-%")
    d2 = datetime.datetime.strptime(d2, "%Y-%m-%d")
    return abs((d2 - d1).hour)


def replace_all(text, dic):
    for i, j in dic.items():
        if j != "":
            text = text.replace(i, j)
    return text


def sort_file_tuples(tuples):
    sorted_tuples = sorted(tuples, key=lambda x: x[1])
    return sorted_tuples
