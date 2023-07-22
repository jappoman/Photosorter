import os, time, shutil, sys, configparser, datetime
#import resources_qr
from PIL import Image
from PIL.ExifTags import TAGS
from PIL.ExifTags import GPSTAGS
from geopy.exc import GeocoderTimedOut
from geopy import distance
from geopy.geocoders import Nominatim
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLineEdit, QLabel, QDesktopWidget, QFileDialog, QProgressBar, QCheckBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtCore
from time import sleep

class App(QMainWindow):

    def __init__(self):
        super().__init__()

        #manually setting all the size of widget
        default_spacing = 20
        default_padding_center = default_spacing+300
        default_widget_y_size = 20
        default_check_x_size = 200
        dirbox_x_size = 550
        homeloc_x_size = 295
        xyz_x_size = 120
        text_x_size = 150
        text_y_size = 100
        window_xsize = 640
        window_ysize = 580
        startbutton_x_size = 150
        startbutton_y_size = 50
        progressbox_x_size = 600
        progressbox_y_size = 100
        progressbar_x_size = 600
        load_cfg_x_size = 100

        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        self.setFixedSize(window_xsize, window_ysize)
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())
        self.setWindowTitle("Photosorter v1.1")
        self.setWindowIcon(QIcon(":/icon.ico"))

        # Create textbox for source directory
        #label
        self.label_sourcedir = QLabel(self)
        self.label_sourcedir.setText("Insert source directory path:")
        self.label_sourcedir.resize(dirbox_x_size, default_widget_y_size)
        self.label_sourcedir.move(default_spacing, default_spacing)
        #textbox
        self.textbox_sourcedir = QLineEdit(self)
        self.textbox_sourcedir.setPlaceholderText("Source directory path")
        self.textbox_sourcedir.resize(dirbox_x_size, default_widget_y_size)
        self.textbox_sourcedir.move(default_spacing, default_spacing*2)
        #button
        self.button_sourcedir = QPushButton('...', self)
        self.button_sourcedir.resize(50, default_widget_y_size)
        self.button_sourcedir.move(default_spacing+dirbox_x_size, default_spacing*2)
        self.button_sourcedir.clicked.connect(self.on_click_sourcedir_button)

        # Create textbox for destination directory
        #label
        self.label_destdir = QLabel(self)
        self.label_destdir.setText("Insert destination directory path:")
        self.label_destdir.resize(dirbox_x_size, default_widget_y_size)
        self.label_destdir.move(default_spacing, default_spacing*3)
        #textbox
        self.textbox_destdir = QLineEdit(self)
        self.textbox_destdir.setPlaceholderText("Destination directory path")
        self.textbox_destdir.resize(dirbox_x_size, default_widget_y_size)
        self.textbox_destdir.move(default_spacing, default_spacing*4)
        #button
        self.button_destdir = QPushButton('...', self)
        self.button_destdir.resize(50, default_widget_y_size)
        self.button_destdir.move(default_spacing+dirbox_x_size, default_spacing*4)
        self.button_destdir.clicked.connect(self.on_click_destdir_button)

        # Create textbox for places dictiorary file
        #label
        self.label_placesfilepath = QLabel(self)
        self.label_placesfilepath.setText("Insert known places file path:")
        self.label_placesfilepath.resize(dirbox_x_size, default_widget_y_size)
        self.label_placesfilepath.move(default_spacing, default_spacing*5)
        #textbox
        self.textbox_placesfilepath = QLineEdit(self)
        self.textbox_placesfilepath.setPlaceholderText("known places path")
        self.textbox_placesfilepath.resize(dirbox_x_size, default_widget_y_size)
        self.textbox_placesfilepath.move(default_spacing, default_spacing*6)
        #button
        self.button_placesfilepath = QPushButton('...', self)
        self.button_placesfilepath.resize(50, default_widget_y_size)
        self.button_placesfilepath.move(default_spacing+dirbox_x_size, default_spacing*6)
        self.button_placesfilepath.clicked.connect(self.on_click_placesfilepath_button)

        # Create textbox for home location (lat)
        #label
        self.label_homelat = QLabel(self)
        self.label_homelat.setText("Insert home location (latitude):")
        self.label_homelat.resize(homeloc_x_size, default_widget_y_size)
        self.label_homelat.move(default_spacing, default_spacing*7)
        #textbox
        self.textbox_homelat = QLineEdit(self)
        self.textbox_homelat.setPlaceholderText("Home location (latitude)")
        self.textbox_homelat.resize(homeloc_x_size, default_widget_y_size)
        self.textbox_homelat.move(default_spacing, default_spacing*8)

        # Create textbox for home location (lon)
        #label
        self.label_homelon = QLabel(self)
        self.label_homelon.setText("Insert home location (longitude):")
        self.label_homelon.resize(homeloc_x_size, default_widget_y_size)
        self.label_homelon.move(default_padding_center+5, default_spacing*7)
        #textbox
        self.textbox_homelon = QLineEdit(self)
        self.textbox_homelon.setPlaceholderText("Home location (longitude)")
        self.textbox_homelon.resize(homeloc_x_size, default_widget_y_size)
        self.textbox_homelon.move(default_padding_center+5, default_spacing*8)

        # Create textbox for X space
        #label
        self.label_xspace = QLabel(self)
        self.label_xspace.setText("(X) kms between pics:")
        self.label_xspace.resize(xyz_x_size, default_widget_y_size)
        self.label_xspace.move(default_spacing, default_spacing*10)
        #textbox
        self.textbox_xpsace = QLineEdit(self)
        self.textbox_xpsace.setPlaceholderText("X")
        self.textbox_xpsace.setText("2")
        self.textbox_xpsace.resize(xyz_x_size, default_widget_y_size)
        self.textbox_xpsace.move(default_spacing, default_spacing*11)

        # Create textbox for Y space
        #label
        self.label_yspace = QLabel(self)
        self.label_yspace.setText("(Y) kms from home:")
        self.label_yspace.resize(xyz_x_size, default_widget_y_size)
        self.label_yspace.move(default_spacing, default_spacing*12)
        #textbox
        self.textbox_ypsace = QLineEdit(self)
        self.textbox_ypsace.setPlaceholderText("Y")
        self.textbox_ypsace.setText("10")
        self.textbox_ypsace.resize(xyz_x_size, default_widget_y_size)
        self.textbox_ypsace.move(default_spacing, default_spacing*13)

        # Create textbox for Z safe space
        #label
        self.label_zspace = QLabel(self)
        self.label_zspace.setText("(Z) kms where to start:")
        self.label_zspace.resize(xyz_x_size, default_widget_y_size)
        self.label_zspace.move(default_spacing, default_spacing*14)
        #textbox
        self.textbox_zpsace = QLineEdit(self)
        self.textbox_zpsace.setPlaceholderText("Z")
        self.textbox_zpsace.setText("1")
        self.textbox_zpsace.resize(xyz_x_size, default_widget_y_size)
        self.textbox_zpsace.move(default_spacing, default_spacing*15)

        #space explaination
        self.label_spaceexplain = QLabel(self)
        self.label_spaceexplain.setText("Pics far away X kms from each others and Y kms away from home are put together.\n\nZ are the kms away from home where to start the calculation about space.")
        self.label_spaceexplain.setWordWrap(True)
        self.label_spaceexplain.resize(text_x_size, text_y_size)
        self.label_spaceexplain.move(default_spacing+xyz_x_size+10, default_spacing*10)

        # Create textbox for X time
        #label
        self.label_xtime = QLabel(self)
        self.label_xtime.setText("(X) sec between pics:")
        self.label_xtime.resize(xyz_x_size, default_widget_y_size)
        self.label_xtime.move(default_padding_center+5, default_spacing*10)
        #textbox
        self.textbox_xtime = QLineEdit(self)
        self.textbox_xtime.setPlaceholderText("X")
        self.textbox_xtime.setText("3600")
        self.textbox_xtime.resize(xyz_x_size, default_widget_y_size)
        self.textbox_xtime.move(default_padding_center+5, default_spacing*11)

        # Create textbox for Y time
        #label
        self.label_ytime = QLabel(self)
        self.label_ytime.setText("(Y) kms from home:")
        self.label_ytime.resize(xyz_x_size, default_widget_y_size)
        self.label_ytime.move(default_padding_center+5, default_spacing*12)
        #textbox
        self.textbox_ytime = QLineEdit(self)
        self.textbox_ytime.setPlaceholderText("Y")
        self.textbox_ytime.setText("10")
        self.textbox_ytime.resize(xyz_x_size, default_widget_y_size)
        self.textbox_ytime.move(default_padding_center+5, default_spacing*13)

        # Create textbox for Z safe time
        #label
        self.label_ztime = QLabel(self)
        self.label_ztime.setText("(Z) sec when to start:")
        self.label_ztime.resize(xyz_x_size, default_widget_y_size)
        self.label_ztime.move(default_padding_center+5, default_spacing*14)
        #textbox
        self.textbox_ztime = QLineEdit(self)
        self.textbox_ztime.setPlaceholderText("Z")
        self.textbox_ztime.setText("3600")
        self.textbox_ztime.resize(xyz_x_size, default_widget_y_size)
        self.textbox_ztime.move(default_padding_center+5, default_spacing*15)

        #time explaination
        self.label_timeexplain = QLabel(self)
        self.label_timeexplain.setText("Pics far away X seconds from each others and Y kms away from home are put together.\n\nZ are the seconds when to start the calculation about time.")
        self.label_timeexplain.setWordWrap(True)
        self.label_timeexplain.resize(text_x_size, text_y_size)
        self.label_timeexplain.move(default_padding_center+xyz_x_size+10, default_spacing*10)

        # dictionary mode check
        self.check_dictionarymode = QCheckBox("Create known places dictionary only", self)
        self.check_dictionarymode.resize(default_check_x_size, default_widget_y_size)
        self.check_dictionarymode.move(default_spacing, default_spacing*18)

        # move file check
        self.check_movefile = QCheckBox("Move files instead of copy (faster!)", self)
        self.check_movefile.resize(default_check_x_size, default_widget_y_size)
        self.check_movefile.move(default_spacing, default_spacing*20)

        # reload cfg button
        self.button_cfg = QPushButton('Reload config file', self)
        self.button_cfg.resize(load_cfg_x_size, default_widget_y_size)
        self.button_cfg.move(window_xsize-load_cfg_x_size-default_spacing, default_spacing*18)
        self.button_cfg.clicked.connect(self.on_click_reloadcfg)

        # start button
        self.button_start = QPushButton('Start sorting', self)
        self.button_start.resize(startbutton_x_size, startbutton_y_size)
        self.button_start.move(default_padding_center-int(startbutton_x_size/2), default_spacing*18)
        self.button_start.clicked.connect(self.on_click_start)

        #progressbar
        self.progressbar = QProgressBar(self)
        self.progressbar.resize(progressbar_x_size, default_widget_y_size)
        self.progressbar.move(default_padding_center-int(progressbar_x_size/2), default_spacing*22)
        self.progressbar.setValue(0)

        #progressbox
        self.label_progress = QLabel(self)
        self.label_progress.setText('Press "Start sorting" to begin')
        self.label_progress.setWordWrap(True)
        self.label_progress.resize(progressbox_x_size, progressbox_y_size)
        self.label_progress.move(default_padding_center-int(progressbox_x_size/2), default_spacing*23)


        #load config from configuration file
        try:
            config = configparser.ConfigParser()
            config.read_file(open("config.cfg"))
            self.textbox_sourcedir.setText(config.get('Directories', 'source_dir'))
            self.textbox_destdir.setText(config.get('Directories', 'destination_dir'))
            self.textbox_placesfilepath.setText(config.get('Places', 'places_file_path'))
            self.textbox_homelat.setText(config.get('Home', 'home_lat'))
            self.textbox_homelon.setText(config.get('Home', 'home_lon'))
            self.textbox_xpsace.setText(config.get('Space', 'x_space'))
            self.textbox_ypsace.setText(config.get('Space', 'y_space'))
            self.textbox_zpsace.setText(config.get('Space', 'z_space'))
            self.textbox_xtime.setText(config.get('Time', 'x_time'))
            self.textbox_ytime.setText(config.get('Time', 'y_time'))
            self.textbox_ztime.setText(config.get('Time', 'z_time'))
        except:
            config = False


        #END
        self.show()

    def closeEvent(self, event):
        #when closing, kill the program
        sys.exit()

    @pyqtSlot()

    def on_click_start(self):
        #disable all the buttons and textbox when the app start
        self.textbox_sourcedir.setEnabled(False)
        self.button_sourcedir.setEnabled(False)
        self.textbox_destdir.setEnabled(False)
        self.button_destdir.setEnabled(False)
        self.textbox_placesfilepath.setEnabled(False)
        self.button_placesfilepath.setEnabled(False)
        self.textbox_homelat.setEnabled(False)
        self.textbox_homelon.setEnabled(False)
        self.textbox_xpsace.setEnabled(False)
        self.textbox_ypsace.setEnabled(False)
        self.textbox_zpsace.setEnabled(False)
        self.textbox_xtime.setEnabled(False)
        self.textbox_ytime.setEnabled(False)
        self.textbox_ztime.setEnabled(False)
        self.button_start.setEnabled(False)
        self.check_dictionarymode.setEnabled(False)
        self.check_movefile.setEnabled(False)
        self.button_cfg.setEnabled(False)
        main(self)

    def on_click_reloadcfg(self):
        #reload config from configuration file
        config = configparser.ConfigParser()
        config.read_file(open("config.cfg"))
        self.textbox_sourcedir.setText(config.get('Directories', 'source_dir'))
        self.textbox_destdir.setText(config.get('Directories', 'destination_dir'))
        self.textbox_placesfilepath.setText(config.get('Places', 'places_file_path'))
        self.textbox_homelat.setText(config.get('Home', 'home_lat'))
        self.textbox_homelon.setText(config.get('Home', 'home_lon'))
        self.textbox_xpsace.setText(config.get('Space', 'x_space'))
        self.textbox_ypsace.setText(config.get('Space', 'y_space'))
        self.textbox_zpsace.setText(config.get('Space', 'z_space'))
        self.textbox_xtime.setText(config.get('Time', 'x_time'))
        self.textbox_ytime.setText(config.get('Time', 'y_time'))
        self.textbox_ztime.setText(config.get('Time', 'z_time'))

    def on_click_sourcedir_button(self):
        #set source dir from dialog
        fileName = str(QFileDialog.getExistingDirectory(self, "Select directory"))
        if fileName:
            self.textbox_sourcedir.setText(fileName)

    def on_click_destdir_button(self):
        #set destination dir from dialog
        fileName = str(QFileDialog.getExistingDirectory(self, "Select directory"))
        if fileName:
            self.textbox_destdir.setText(fileName)

    def on_click_placesfilepath_button(self):
        #set destination dir from dialog
        fileName, _ = QFileDialog.getOpenFileName(self,"Open places.txt file", "","Text file (*.txt)")
        if fileName:
            self.textbox_placesfilepath.setText(fileName)

#END OF THE CLASS


#functions ---

def get_exif(filename):
    if filename.endswith('.jpg'):
        image = Image.open(filename)
        image.verify()
        return image._getexif()
    else:
        return False

def get_labeled_exif(exif):
    labeled = {}
    for (key, val) in exif.items():
        labeled[TAGS.get(key)] = val
    return labeled

def get_geotagging(exif):
    if not exif:
        return "No EXIF metadata found"
        #raise ValueError("No EXIF metadata found")

    geotagging = {}
    for (idx, tag) in TAGS.items():
        if tag == 'GPSInfo':
            if idx not in exif:
                return "No EXIF geotagging found"
                #raise ValueError("No EXIF geotagging found")
            try:
                for (key, val) in GPSTAGS.items():
                    if key in exif[idx]:
                        geotagging[val] = exif[idx][key]
            except GeocoderTimedOut:
                sleep(1)
                get_geotagging(exif)

    return geotagging

def dms_to_dd(gps_coords, gps_coords_ref):
    d, m, s =  gps_coords
    dd = d + m / 60 + s / 3600
    if gps_coords_ref.upper() in ('S', 'W'):
        return -dd
    elif gps_coords_ref.upper() in ('N', 'E'):
        return dd
    else:
        raise RuntimeError('Incorrect gps_coords_ref {}'.format(gps_coords_ref))

def hour_between(d1, d2):
    d1 = datetime.datetime.strptime(d1, "%Y-%m-%d-%")
    d2 = datetime.datetime.strptime(d2, "%Y-%m-%d")
    return abs((d2 - d1).hour)

def replace_all(text, dic):
    for i, j in dic.items():
        if j!="": text = text.replace(i, j)
    return text

def sort_file_tuples(tuples):
    sorted_tuples = sorted(tuples ,key=lambda x: x[1])
    return sorted_tuples

#main ---
def main(self):

    #getting all variables from boxes (check if there is a value inside)
    source_dir = self.textbox_sourcedir.text()
    destination_dir = self.textbox_destdir.text()
    #home location
    if (self.textbox_homelat.text()!='' and self.textbox_homelon.text()!=''):
        home_location = (self.textbox_homelat.text(), self.textbox_homelon.text())
    else:
        home_location = (0,0)
    #space coefficient
    if (self.textbox_xpsace.text()!='' and self.textbox_ypsace.text()!=''):
        space_coefficient = int(self.textbox_xpsace.text())/int(self.textbox_ypsace.text())
    else:
        space_coefficient = 1
    #space offset
    if(self.textbox_zpsace.text()!=''):
        space_offset = int(self.textbox_zpsace.text())
    else:
        space_offset = 0
    #time coefficient
    if(self.textbox_xtime.text()!='' and self.textbox_ytime.text()!=''):
        time_coefficient = int(self.textbox_xtime.text())/int(self.textbox_ytime.text())
    else:
        time_coefficient = 1
    #time offset
    if(self.textbox_ztime.text()!=''):
        time_offset = int(self.textbox_ztime.text())
    else:
        time_offset = 0
    #places file path
    if (self.textbox_placesfilepath.text()!=''):
        places_file_path = self.textbox_placesfilepath.text()
        places_file = open(places_file_path, 'r')
        place_list = []
        auxiliaryPlacesList = []
        places_to_replace = {}
        for line in places_file:
            k, v = line.strip().split('=')
            places_to_replace[k.strip()] = v.strip()
        places_file.close()
    else:
        places_to_replace = {}
    #dictionary mode
    dictionary_mode = self.check_dictionarymode.isChecked()
    #file move mode
    file_move_mode = self.check_movefile.isChecked()


    if(source_dir!='' and destination_dir!=''):

        #init a bunch of utility
        files = []
        geolocator = Nominatim(user_agent="Photo_manager")
        char_to_replace = {
        "\\": "_",
        "/": "_",
        ":": "_",
        "\"": "_"
        }

        # getting all files in subfolders
        for r, d, f in os.walk(source_dir):
            for file in f:
                files.append(os.path.join(r, file))

        #default variables
        previous_picture_location = home_location
        previous_picture_date = "01/01/1900 00:00:00"
        event_counter = 1
        place = False

        #sort all files by date
        files_tuples = []
        for f in files:
            f=f.replace("\\", "/")
            #tempdate = (time.ctime(os.path.getmtime(f))).split()
            tempdate = (time.ctime(os.path.getmtime(f)))
            timestamp = time.mktime(datetime.datetime.strptime(tempdate, "%a %b %d %H:%M:%S %Y").timetuple())
            files_tuples.append((f, timestamp))
        files = sort_file_tuples(files_tuples)

        #setting percentage of progression based on number of files
        number_of_files = len(files)
        if(number_of_files>0):
            progression_percentage = 100/number_of_files

        #cycling on all files
        file_counter = 0
        for f in files:
            f=f[0] #using just the filename

            #GETTING PICTURE TIME

            tempdate = (time.ctime(os.path.getmtime(f))).split()

            picture_year = tempdate[4]

            if (tempdate[1] == "Jan") : picture_month = "1"
            if (tempdate[1] == "Feb") : picture_month = "2"
            if (tempdate[1] == "Mar") : picture_month = "3"
            if (tempdate[1] == "Apr") : picture_month = "4"
            if (tempdate[1] == "May") : picture_month = "5"
            if (tempdate[1] == "Jun") : picture_month = "6"
            if (tempdate[1] == "Jul") : picture_month = "7"
            if (tempdate[1] == "Aug") : picture_month = "8"
            if (tempdate[1] == "Sep") : picture_month = "9"
            if (tempdate[1] == "Oct") : picture_month = "10"
            if (tempdate[1] == "Nov") : picture_month = "11"
            if (tempdate[1] == "Dec") : picture_month = "12"

            picture_day = tempdate[2]
            picture_hour = tempdate[3].split(":")[0]
            picture_minutes = tempdate[3].split(":")[1]
            picture_seconds = tempdate[3].split(":")[2]

            picture_date = picture_day + "/" + picture_month + "/" + picture_year + " " + picture_hour +":"+ picture_minutes +":"+ picture_seconds

            #calculating the time distance between 2 pictures (in hour)
            date1 = datetime.datetime.strptime(picture_date, "%d/%m/%Y %H:%M:%S")
            date2 = datetime.datetime.strptime(previous_picture_date, "%d/%m/%Y %H:%M:%S")
            diff = abs(date1 - date2)
            diff_in_seconds = diff.total_seconds()

            #updating date of the previous picture
            previous_picture_date = picture_date


            #GETTIN PICTURE SPACE

            #getting exif infos
            exif = get_exif(f)
            geotags = get_geotagging(exif)


            #TAKING DECISION ABOUT FOLDERS

            #Check if the pictures has gps data
            if (('GPSLatitude' in geotags) and ('GPSLongitude' in geotags) and ('GPSLatitudeRef' in geotags) and ('GPSLongitudeRef' in geotags)):
                #image has gps data

                #sorting out all the geotag infos
                gps_latitude = geotags['GPSLatitude']
                gps_longitude = geotags['GPSLongitude']
                gps_latitude_ref = geotags['GPSLatitudeRef']
                gps_longitude_ref = geotags['GPSLongitudeRef']
                #converting them into decimals
                lat_dd = float(dms_to_dd(gps_latitude, gps_latitude_ref))
                lon_dd = float(dms_to_dd(gps_longitude, gps_longitude_ref))
                #picture location
                picture_location = (lat_dd, lon_dd)
                #getting picture place on first run
                if not place:
                    location = geolocator.reverse(picture_location)
                    temp_split = (location.address).split(", ")
                    place = temp_split[0]+" "+temp_split[1]+" "+temp_split[2]
                    place = place.translate(str.maketrans(char_to_replace))
                    if not dictionary_mode:
                        place = replace_all(place, places_to_replace)
                #calculating distance from home and from previous picture
                distance_from_home = abs(distance.distance(home_location, picture_location).km)
                distance_from_previous_picture = abs(distance.distance(previous_picture_location, picture_location).km)
                #updating location and date of the previous picture
                previous_picture_location =  picture_location

                #check if picture are too far (in space)
                if (distance_from_previous_picture > (distance_from_home*space_coefficient+space_offset)) :
                    #pictures are far away

                    #check if picture are far enought (in time)
                    if (diff_in_seconds > (distance_from_home*time_coefficient+time_offset)):
                        #getting picture place
                        location = geolocator.reverse(picture_location)
                        temp_split = (location.address).split(", ")
                        place = temp_split[0]+" "+temp_split[1]+" "+temp_split[2]
                        place = place.translate(str.maketrans(char_to_replace))
                        if not dictionary_mode:
                            place = replace_all(place, places_to_replace)
                        #new folder
                        destination_dir_path = destination_dir +"/Event_"+ str(event_counter).rjust(5, '0')+" "+ place +" "+ picture_year +"-"+ picture_month.rjust(2, "0") +"-"+ picture_day.rjust(2, "0")
                        event_counter += 1

                else:
                    #pictures are near
                    #check if picture are too far (in time)
                    if (diff_in_seconds > (distance_from_home*time_coefficient+time_offset)):
                        #new folder
                        destination_dir_path = destination_dir +"/Event_"+ str(event_counter).rjust(5, '0')+" "+ place +" "+ picture_year +"-"+ picture_month.rjust(2, "0") +"-"+ picture_day.rjust(2, "0")
                        event_counter += 1

            else:
                #image has not gps data
                #setting placeholder values
                distance_from_home = 0
                distance_from_previous_picture = 0
                #check if picture are too far (in time)
                if (diff_in_seconds > time_offset):
                    #new folder
                    destination_dir_path = destination_dir +"/Event_"+ str(event_counter).rjust(5, '0')+" "+ picture_year +"-"+ picture_month.rjust(2, "0") +"-"+ picture_day.rjust(2, "0")
                    event_counter += 1


            #CREATING FOLDERS

            #making the folder (if not in dictionary mode)
            if not dictionary_mode:
                os.makedirs(destination_dir_path, exist_ok=True)

            #adding filename to path for moving file
            destination_path = destination_dir_path + '/' + f.split("/")[-1]

            #updating the text in progressbox area
            self.label_progress.setText("Copying/moving: " +f.split("/")[-1]+
            "\nto " +destination_dir_path+"/\n\n"+
            "Has GPS: "+str(('GPSLatitude' in geotags) and ('GPSLongitude' in geotags) and ('GPSLatitudeRef' in geotags) and ('GPSLongitudeRef' in geotags)) +
            "\tDistance from home (space): " + str(round(distance_from_home, 3)) +
            "\tDistance from previous (space): "+ str(round(distance_from_previous_picture, 3)) + "\n"+
            "Distance to beat (space): "+ str(round(distance_from_home*space_coefficient+space_offset,3)) +
            "\tCreate new folder (space): "+str(distance_from_previous_picture > (distance_from_home*space_coefficient+space_offset))+"\n\n"+
            "Distance from previous (time): "+ str(diff_in_seconds) +
            "\tDistance to beat (time): " + str(round(distance_from_home*time_coefficient+time_offset,3)) +
            "\tCreate new folder (time): " + str(diff_in_seconds > (distance_from_home*time_coefficient+time_offset)))

            #updating percentage of the bar
            int_percentage = int(progression_percentage*file_counter)
            self.progressbar.setValue(int_percentage)
            file_counter = file_counter+1

            #letting the UI updates
            QtCore.QCoreApplication.processEvents()

            #copying/moving the files (if dictionary mode is not selected)
            if not dictionary_mode:
                if file_move_mode:
                    shutil.move(f, destination_path)
                if not file_move_mode:
                    shutil.copyfile(f, destination_path)
            else:
                #building dictionary file (if dictionary mode is selected)
                auxiliaryPlacesList.append(place)
                for word in auxiliaryPlacesList:
                    if word not in place_list:
                        place_list.append(word)

        #at the end, create a file with the list of unique places (if in dictionary mode)
        if dictionary_mode:
            places_file = open('places_to_replace.txt', 'w')
            for place_to_write in place_list:
                places_file.write(str(place_to_write)+" = \n")
            places_file.close()

        #at the end, if the progression is not truly 100%, set it manually
        self.progressbar.setValue(100)
        #re-enabling gui
        self.textbox_sourcedir.setEnabled(True)
        self.button_sourcedir.setEnabled(True)
        self.textbox_destdir.setEnabled(True)
        self.button_destdir.setEnabled(True)
        self.textbox_placesfilepath.setEnabled(True)
        self.button_placesfilepath.setEnabled(True)
        self.textbox_homelat.setEnabled(True)
        self.textbox_homelon.setEnabled(True)
        self.textbox_xpsace.setEnabled(True)
        self.textbox_ypsace.setEnabled(True)
        self.textbox_zpsace.setEnabled(True)
        self.textbox_xtime.setEnabled(True)
        self.textbox_ytime.setEnabled(True)
        self.textbox_ztime.setEnabled(True)
        self.button_start.setEnabled(True)
        self.button_cfg.setEnabled(True)
        self.check_dictionarymode.setEnabled(True)
        self.check_movefile.setEnabled(True)
        #setting a "done" message in the progressbox area
        self.label_progress.setText("Done")

    else:
        self.textbox_sourcedir.setEnabled(True)
        self.button_sourcedir.setEnabled(True)
        self.textbox_destdir.setEnabled(True)
        self.button_destdir.setEnabled(True)
        self.textbox_placesfilepath.setEnabled(True)
        self.button_placesfilepath.setEnabled(True)
        self.textbox_homelat.setEnabled(True)
        self.textbox_homelon.setEnabled(True)
        self.textbox_xpsace.setEnabled(True)
        self.textbox_ypsace.setEnabled(True)
        self.textbox_zpsace.setEnabled(True)
        self.textbox_xtime.setEnabled(True)
        self.textbox_ytime.setEnabled(True)
        self.textbox_ztime.setEnabled(True)
        self.button_start.setEnabled(True)
        self.button_cfg.setEnabled(True)
        self.check_dictionarymode.setEnabled(True)
        self.check_movefile.setEnabled(True)
        self.label_progress.setText("No source or destination directory specified")


#end functions ---

#CALLING MAIN
if __name__ == "__main__":

    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
