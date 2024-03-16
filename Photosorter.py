import os, time, shutil, sys, datetime

from geopy import distance
from geopy.geocoders import Nominatim
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtCore

from gui_manager import App
from config_manager import ConfigManager
from utility_manager import get_exif, get_geotagging, dms_to_dd, replace_all, sort_file_tuples

def main(app_instance):
    
 #getting all variables from boxes (check if there is a value inside)
    source_dir = app_instance.textbox_sourcedir.text()
    destination_dir = app_instance.textbox_destdir.text()
    #home location
    if (app_instance.textbox_homelat.text()!='' and app_instance.textbox_homelon.text()!=''):
        home_location = (app_instance.textbox_homelat.text(), app_instance.textbox_homelon.text())
    else:
        home_location = (0,0)
    #space coefficient
    if (app_instance.textbox_xpsace.text()!='' and app_instance.textbox_ypsace.text()!=''):
        space_coefficient = int(app_instance.textbox_xpsace.text())/int(app_instance.textbox_ypsace.text())
    else:
        space_coefficient = 1
    #space offset
    if(app_instance.textbox_zpsace.text()!=''):
        space_offset = int(app_instance.textbox_zpsace.text())
    else:
        space_offset = 0
    #time coefficient
    if(app_instance.textbox_xtime.text()!='' and app_instance.textbox_ytime.text()!=''):
        time_coefficient = int(app_instance.textbox_xtime.text())/int(app_instance.textbox_ytime.text())
    else:
        time_coefficient = 1
    #time offset
    if(app_instance.textbox_ztime.text()!=''):
        time_offset = int(app_instance.textbox_ztime.text())
    else:
        time_offset = 0
    #places file path
    if (app_instance.textbox_placesfilepath.text()!=''):
        places_file_path = app_instance.textbox_placesfilepath.text()
        try:
            places_file = open(places_file_path, 'r')
            place_list = []
            auxiliaryPlacesList = []
            places_to_replace = {}
            for line in places_file:
                k, v = line.strip().split('=')
                places_to_replace[k.strip()] = v.strip()
            places_file.close()
        except Exception as e:
            print(f"Errore nell'apertura o nella lettura del file '{places_file_path}': {e}")
    else:
        places_to_replace = {}
    #dictionary mode
    dictionary_mode = app_instance.check_dictionarymode.isChecked()
    #file move mode
    file_move_mode = app_instance.check_movefile.isChecked()


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
            app_instance.label_progress.setText("Copying/moving: " +f.split("/")[-1]+
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
            app_instance.progressbar.setValue(int_percentage)
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
        app_instance.progressbar.setValue(100)
        #re-enabling gui
        app_instance.textbox_sourcedir.setEnabled(True)
        app_instance.button_sourcedir.setEnabled(True)
        app_instance.textbox_destdir.setEnabled(True)
        app_instance.button_destdir.setEnabled(True)
        app_instance.textbox_placesfilepath.setEnabled(True)
        app_instance.button_placesfilepath.setEnabled(True)
        app_instance.textbox_homelat.setEnabled(True)
        app_instance.textbox_homelon.setEnabled(True)
        app_instance.textbox_xpsace.setEnabled(True)
        app_instance.textbox_ypsace.setEnabled(True)
        app_instance.textbox_zpsace.setEnabled(True)
        app_instance.textbox_xtime.setEnabled(True)
        app_instance.textbox_ytime.setEnabled(True)
        app_instance.textbox_ztime.setEnabled(True)
        app_instance.button_start.setEnabled(True)
        app_instance.button_cfg.setEnabled(True)
        app_instance.check_dictionarymode.setEnabled(True)
        app_instance.check_movefile.setEnabled(True)
        #setting a "done" message in the progressbox area
        app_instance.label_progress.setText("Done")

    else:
        app_instance.textbox_sourcedir.setEnabled(True)
        app_instance.button_sourcedir.setEnabled(True)
        app_instance.textbox_destdir.setEnabled(True)
        app_instance.button_destdir.setEnabled(True)
        app_instance.textbox_placesfilepath.setEnabled(True)
        app_instance.button_placesfilepath.setEnabled(True)
        app_instance.textbox_homelat.setEnabled(True)
        app_instance.textbox_homelon.setEnabled(True)
        app_instance.textbox_xpsace.setEnabled(True)
        app_instance.textbox_ypsace.setEnabled(True)
        app_instance.textbox_zpsace.setEnabled(True)
        app_instance.textbox_xtime.setEnabled(True)
        app_instance.textbox_ytime.setEnabled(True)
        app_instance.textbox_ztime.setEnabled(True)
        app_instance.button_start.setEnabled(True)
        app_instance.button_cfg.setEnabled(True)
        app_instance.check_dictionarymode.setEnabled(True)
        app_instance.check_movefile.setEnabled(True)
        app_instance.label_progress.setText("No source or destination directory specified")



    pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Carica la configurazione
    config = ConfigManager().config
    
    # Crea l'istanza dell'applicazione e passa la configurazione
    ex = App(config)

    # Connetti il segnale alla funzione principale
    ex.startSortingSignal.connect(lambda: main(ex))
    
    sys.exit(app.exec_())
