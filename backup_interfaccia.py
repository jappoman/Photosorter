# Ottieni le dimensioni dello schermo
        screen = QDesktopWidget().screenGeometry()

        # Calcola le dimensioni della finestra come percentuale delle dimensioni dello schermo
        window_xsize = int(screen.width() * 0.6)  # 60% della larghezza dello schermo
        window_ysize = int(screen.height() * 0.7)  # 70% dell'altezza dello schermo

        # manually setting all the size of widget
        default_spacing = 20
        default_padding_center = default_spacing + 300
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

        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        self.setFixedSize(window_xsize, window_ysize)
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())
        self.setWindowTitle("Photosorter v1.1")
        self.setWindowIcon(QIcon(":/icon.ico"))

                # Utilizza QVBoxLayout e QHBoxLayout per organizzare i widget
        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)
        mainLayout = QVBoxLayout(centralWidget)

        # Create textbox for source directory
        # label
        self.label_sourcedir = QLabel(self)
        self.label_sourcedir.setText("Insert source directory path:")
        self.label_sourcedir.resize(dirbox_x_size, default_widget_y_size)
        self.label_sourcedir.move(default_spacing, default_spacing)
        # textbox
        self.textbox_sourcedir = QLineEdit(self)
        self.textbox_sourcedir.setPlaceholderText("Source directory path")
        self.textbox_sourcedir.resize(dirbox_x_size, default_widget_y_size)
        self.textbox_sourcedir.move(default_spacing, default_spacing * 2)
        # button
        self.button_sourcedir = QPushButton("...", self)
        self.button_sourcedir.resize(50, default_widget_y_size)
        self.button_sourcedir.move(default_spacing + dirbox_x_size, default_spacing * 2)
        self.button_sourcedir.clicked.connect(self.on_click_sourcedir_button)

        # Create textbox for destination directory
        # label
        self.label_destdir = QLabel(self)
        self.label_destdir.setText("Insert destination directory path:")
        self.label_destdir.resize(dirbox_x_size, default_widget_y_size)
        self.label_destdir.move(default_spacing, default_spacing * 3)
        # textbox
        self.textbox_destdir = QLineEdit(self)
        self.textbox_destdir.setPlaceholderText("Destination directory path")
        self.textbox_destdir.resize(dirbox_x_size, default_widget_y_size)
        self.textbox_destdir.move(default_spacing, default_spacing * 4)
        # button
        self.button_destdir = QPushButton("...", self)
        self.button_destdir.resize(50, default_widget_y_size)
        self.button_destdir.move(default_spacing + dirbox_x_size, default_spacing * 4)
        self.button_destdir.clicked.connect(self.on_click_destdir_button)







        # Create textbox for places dictiorary file
        # label
        self.label_placesfilepath = QLabel(self)
        self.label_placesfilepath.setText("Insert known places file path:")
        self.label_placesfilepath.resize(dirbox_x_size, default_widget_y_size)
        self.label_placesfilepath.move(default_spacing, default_spacing * 5)
        # textbox
        self.textbox_placesfilepath = QLineEdit(self)
        self.textbox_placesfilepath.setPlaceholderText("known places path")
        self.textbox_placesfilepath.resize(dirbox_x_size, default_widget_y_size)
        self.textbox_placesfilepath.move(default_spacing, default_spacing * 6)
        # button
        self.button_placesfilepath = QPushButton("...", self)
        self.button_placesfilepath.resize(50, default_widget_y_size)
        self.button_placesfilepath.move(
            default_spacing + dirbox_x_size, default_spacing * 6
        )
        self.button_placesfilepath.clicked.connect(self.on_click_placesfilepath_button)

        # Create textbox for home location (lat)
        # label
        self.label_homelat = QLabel(self)
        self.label_homelat.setText("Insert home location (latitude):")
        self.label_homelat.resize(homeloc_x_size, default_widget_y_size)
        self.label_homelat.move(default_spacing, default_spacing * 7)
        # textbox
        self.textbox_homelat = QLineEdit(self)
        self.textbox_homelat.setPlaceholderText("Home location (latitude)")
        self.textbox_homelat.resize(homeloc_x_size, default_widget_y_size)
        self.textbox_homelat.move(default_spacing, default_spacing * 8)

        # Create textbox for home location (lon)
        # label
        self.label_homelon = QLabel(self)
        self.label_homelon.setText("Insert home location (longitude):")
        self.label_homelon.resize(homeloc_x_size, default_widget_y_size)
        self.label_homelon.move(default_padding_center + 5, default_spacing * 7)
        # textbox
        self.textbox_homelon = QLineEdit(self)
        self.textbox_homelon.setPlaceholderText("Home location (longitude)")
        self.textbox_homelon.resize(homeloc_x_size, default_widget_y_size)
        self.textbox_homelon.move(default_padding_center + 5, default_spacing * 8)

        # Create textbox for X space
        # label
        self.label_xspace = QLabel(self)
        self.label_xspace.setText("(X) kms between pics:")
        self.label_xspace.resize(xyz_x_size, default_widget_y_size)
        self.label_xspace.move(default_spacing, default_spacing * 10)
        # textbox
        self.textbox_xpsace = QLineEdit(self)
        self.textbox_xpsace.setPlaceholderText("X")
        self.textbox_xpsace.setText("2")
        self.textbox_xpsace.resize(xyz_x_size, default_widget_y_size)
        self.textbox_xpsace.move(default_spacing, default_spacing * 11)

        # Create textbox for Y space
        # label
        self.label_yspace = QLabel(self)
        self.label_yspace.setText("(Y) kms from home:")
        self.label_yspace.resize(xyz_x_size, default_widget_y_size)
        self.label_yspace.move(default_spacing, default_spacing * 12)
        # textbox
        self.textbox_ypsace = QLineEdit(self)
        self.textbox_ypsace.setPlaceholderText("Y")
        self.textbox_ypsace.setText("10")
        self.textbox_ypsace.resize(xyz_x_size, default_widget_y_size)
        self.textbox_ypsace.move(default_spacing, default_spacing * 13)

        # Create textbox for Z safe space
        # label
        self.label_zspace = QLabel(self)
        self.label_zspace.setText("(Z) kms where to start:")
        self.label_zspace.resize(xyz_x_size, default_widget_y_size)
        self.label_zspace.move(default_spacing, default_spacing * 14)
        # textbox
        self.textbox_zpsace = QLineEdit(self)
        self.textbox_zpsace.setPlaceholderText("Z")
        self.textbox_zpsace.setText("1")
        self.textbox_zpsace.resize(xyz_x_size, default_widget_y_size)
        self.textbox_zpsace.move(default_spacing, default_spacing * 15)

        # space explaination
        self.label_spaceexplain = QLabel(self)
        self.label_spaceexplain.setText(
            "Pics far away X kms from each others and Y kms away from home are put together.\n\nZ are the kms away from home where to start the calculation about space."
        )
        self.label_spaceexplain.setWordWrap(True)
        self.label_spaceexplain.resize(text_x_size, text_y_size)
        self.label_spaceexplain.move(
            default_spacing + xyz_x_size + 10, default_spacing * 10
        )

        # Create textbox for X time
        # label
        self.label_xtime = QLabel(self)
        self.label_xtime.setText("(X) sec between pics:")
        self.label_xtime.resize(xyz_x_size, default_widget_y_size)
        self.label_xtime.move(default_padding_center + 5, default_spacing * 10)
        # textbox
        self.textbox_xtime = QLineEdit(self)
        self.textbox_xtime.setPlaceholderText("X")
        self.textbox_xtime.setText("3600")
        self.textbox_xtime.resize(xyz_x_size, default_widget_y_size)
        self.textbox_xtime.move(default_padding_center + 5, default_spacing * 11)

        # Create textbox for Y time
        # label
        self.label_ytime = QLabel(self)
        self.label_ytime.setText("(Y) kms from home:")
        self.label_ytime.resize(xyz_x_size, default_widget_y_size)
        self.label_ytime.move(default_padding_center + 5, default_spacing * 12)
        # textbox
        self.textbox_ytime = QLineEdit(self)
        self.textbox_ytime.setPlaceholderText("Y")
        self.textbox_ytime.setText("10")
        self.textbox_ytime.resize(xyz_x_size, default_widget_y_size)
        self.textbox_ytime.move(default_padding_center + 5, default_spacing * 13)

        # Create textbox for Z safe time
        # label
        self.label_ztime = QLabel(self)
        self.label_ztime.setText("(Z) sec when to start:")
        self.label_ztime.resize(xyz_x_size, default_widget_y_size)
        self.label_ztime.move(default_padding_center + 5, default_spacing * 14)
        # textbox
        self.textbox_ztime = QLineEdit(self)
        self.textbox_ztime.setPlaceholderText("Z")
        self.textbox_ztime.setText("3600")
        self.textbox_ztime.resize(xyz_x_size, default_widget_y_size)
        self.textbox_ztime.move(default_padding_center + 5, default_spacing * 15)

        # time explaination
        self.label_timeexplain = QLabel(self)
        self.label_timeexplain.setText(
            "Pics far away X seconds from each others and Y kms away from home are put together.\n\nZ are the seconds when to start the calculation about time."
        )
        self.label_timeexplain.setWordWrap(True)
        self.label_timeexplain.resize(text_x_size, text_y_size)
        self.label_timeexplain.move(
            default_padding_center + xyz_x_size + 10, default_spacing * 10
        )

        # dictionary mode check
        self.check_dictionarymode = QCheckBox(
            "Create known places dictionary only", self
        )
        self.check_dictionarymode.resize(default_check_x_size, default_widget_y_size)
        self.check_dictionarymode.move(default_spacing, default_spacing * 18)

        # move file check
        self.check_movefile = QCheckBox("Move files instead of copy (faster!)", self)
        self.check_movefile.resize(default_check_x_size, default_widget_y_size)
        self.check_movefile.move(default_spacing, default_spacing * 20)

        # start button
        self.button_start = QPushButton("Start sorting", self)
        self.button_start.resize(startbutton_x_size, startbutton_y_size)
        self.button_start.move(
            default_padding_center - int(startbutton_x_size / 2), default_spacing * 18
        )
        self.button_start.clicked.connect(self.on_click_start)

        # progressbar
        self.progressbar = QProgressBar(self)
        self.progressbar.resize(progressbar_x_size, default_widget_y_size)
        self.progressbar.move(
            default_padding_center - int(progressbar_x_size / 2), default_spacing * 22
        )
        self.progressbar.setValue(0)

        # progressbox
        self.label_progress = QLabel(self)
        self.label_progress.setText('Press "Start sorting" to begin')
        self.label_progress.setWordWrap(True)
        self.label_progress.resize(progressbox_x_size, progressbox_y_size)
        self.label_progress.move(
            default_padding_center - int(progressbox_x_size / 2), default_spacing * 23
        )

        # load config from configuration file
        try:
            self.textbox_sourcedir.setText(self.config.get("Directories", "source_dir"))
            self.textbox_destdir.setText(
                self.config.get("Directories", "destination_dir")
            )
            self.textbox_placesfilepath.setText(
                self.config.get("Places", "places_file_path")
            )
            self.textbox_homelat.setText(self.config.get("Home", "home_lat"))
            self.textbox_homelon.setText(self.config.get("Home", "home_lon"))
            self.textbox_xpsace.setText(self.config.get("Space", "x_space"))
            self.textbox_ypsace.setText(self.config.get("Space", "y_space"))
            self.textbox_zpsace.setText(self.config.get("Space", "z_space"))
            self.textbox_xtime.setText(self.config.get("Time", "x_time"))
            self.textbox_ytime.setText(self.config.get("Time", "y_time"))
            self.textbox_ztime.setText(self.config.get("Time", "z_time"))
        except:
            config = False

        # END
        self.show()