from PyQt5.QtWidgets import QWidget, QLabel, QComboBox, QSlider, QVBoxLayout,QHBoxLayout, QFrame,QCheckBox,QRadioButton,QPushButton

class TrackWidget(QFrame):
    def __init__(self, track_name, track_number ):
        self.name = track_name
        self.num = track_number
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        
        self.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        self.setLineWidth(1)

        labeltext = 'track number '+ str(self.num) + ' - ' + str(self.name)
        self.track_label = QLabel(labeltext, self)
        layout.addWidget(self.track_label)

        self.instrument_combo = QComboBox(self)

        self.instrument_combo.addItems([
            "acoustic guitar",
            "clarinet", 
            "tom", 
            "snare drum", 
            "flute", 
            "saxo", 
            "piano", 
            "electric piano",
            "violin", 
            "viola",
            "cello",
            "hotbath",
            "string ensemble"
            ])

        layout.addWidget(self.instrument_combo)

        volume_layout = QHBoxLayout()
        layout.addLayout(volume_layout)

        volume_label = QLabel("VOLUME = 0", self)
        volume_layout.addWidget(volume_label)

        self.volume_slider = QSlider(self)
        self.volume_slider.setOrientation(1)  # Vertical orientation
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(50)
        volume_layout.addWidget(self.volume_slider)

        volume_label2 = QLabel(" 100", self)
        volume_layout.addWidget(volume_label2)

        
        # Create button
        self.button = QPushButton('Show/Hide Track Effects')
        self.button.clicked.connect(self.toggleLayout)

        # Add button to the layout
        layout.addWidget(self.button)


        self.echo_layout = QHBoxLayout()
        
        echo_label = QLabel("ECHO EFFECT: ", self)
        self.echo_layout.addWidget(echo_label)
        self.echo_toggleon = QCheckBox("ON", self)
        self.echo_layout.addWidget(self.echo_toggleon)
        echo_number_label = QLabel("ECHO NUMBER: ", self)
        self.echo_layout.addWidget(echo_number_label)

        self.radio_button1 = QRadioButton("1", self)
        self.radio_button1.setChecked(True)
        self.radio_button2 = QRadioButton("2", self)
        self.echo_layout.addWidget(self.radio_button1)
        self.echo_layout.addWidget(self.radio_button2)

        self.flanger_layout = QHBoxLayout()
        
        flanger_label = QLabel("FLANGER EFFECT: ", self)
        self.flanger_layout.addWidget(flanger_label)
        self.flanger_toggleon = QCheckBox("ON", self)
        self.flanger_layout.addWidget(self.flanger_toggleon)

        self.wahwah_layout = QHBoxLayout()
        
        wahwah_label = QLabel("WAHWAH EFFECT: ", self)
        self.wahwah_layout.addWidget(wahwah_label)
        self.wahwah_toggleon = QCheckBox("ON", self)
        self.wahwah_layout.addWidget(self.wahwah_toggleon)

        self.effectswidget = QFrame()
        widgetlayout = QVBoxLayout()
        self.effectswidget.setLayout(widgetlayout)
        widgetlayout.addLayout(self.flanger_layout)
        widgetlayout.addLayout(self.wahwah_layout)
        widgetlayout.addLayout(self.echo_layout)
        self.effectswidget.setVisible(False)

        layout.addWidget(self.effectswidget)
        

    def toggleLayout(self):
        if self.effectswidget.isVisible():
            self.effectswidget.setVisible(False)
        else:
            self.effectswidget.setVisible(True)

    def get_track_label_text(self):
        return self.track_label.text()

    def get_instrument_combo_value(self):
        return self.instrument_combo.currentText()

    def get_volume_slider_value(self):
        return self.volume_slider.value()
    
    def get_echo_on(self):
        return self.echo_toggleon.isChecked()

    def get_echo_number(self):
        if self.radio_button1.isChecked():
            retval = 1
        else:
            retval=2
        return retval

    def get_flanger_on(self):
        return self.flanger_toggleon.isChecked()
    
    def get_wahwah_on(self):
        return self.wahwah_toggleon.isChecked()