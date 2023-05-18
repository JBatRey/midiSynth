from PyQt5.QtWidgets import *

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

        echo_delay_label = QLabel("delay [ms]: ", self)
        self.echo_layout.addWidget(echo_delay_label) 
        self.echo_delay_spinbox = QSpinBox()
        self.echo_layout.addWidget(self.echo_delay_spinbox) 
        self.echo_delay_spinbox.setRange(100, 5000)    # f flanger (~ 1Hz)
        self.echo_delay_spinbox.setValue(500)

        echo_decay_label = QLabel("decay: ", self)
        self.echo_layout.addWidget(echo_decay_label) 
        self.echo_decay_spinbox = QDoubleSpinBox()
        self.echo_layout.addWidget(self.echo_decay_spinbox) 
        self.echo_decay_spinbox.setRange(0.1, 0.99)
        self.echo_decay_spinbox.setValue(0.5)
        # maxdelay (< 15ms)

        self.flanger_layout = QHBoxLayout()
        
        flanger_label = QLabel("FLANGER EFFECT: ", self)
        self.flanger_layout.addWidget(flanger_label)
        self.flanger_toggleon = QCheckBox("ON", self)
        self.flanger_layout.addWidget(self.flanger_toggleon)

        flanger_delay_label = QLabel("max delay [ms]: ", self)
        self.flanger_layout.addWidget(flanger_delay_label) 
        self.flanger_delay_spinbox = QSpinBox()
        self.flanger_layout.addWidget(self.flanger_delay_spinbox) 
        self.flanger_delay_spinbox.setRange(1, 14)
        self.flanger_delay_spinbox.setValue(10)
        # maxdelay (< 15ms)

        flanger_fflanger_label = QLabel("f flanger [Hz]: ", self)
        self.flanger_layout.addWidget(flanger_fflanger_label) 
        self.flanger_fflanger_spinbox = QDoubleSpinBox()
        self.flanger_layout.addWidget(self.flanger_fflanger_spinbox) 
        self.flanger_fflanger_spinbox.setRange(0.25, 2.0)     # f flanger (~ 1Hz)
        self.flanger_fflanger_spinbox.setValue(1.0)

        self.wahwah_layout = QHBoxLayout()
        
        wahwah_label = QLabel("WAHWAH EFFECT: ", self)
        self.wahwah_layout.addWidget(wahwah_label)
        self.wahwah_toggleon = QCheckBox("ON", self)
        self.wahwah_layout.addWidget(self.wahwah_toggleon)

        
        wah_freq_label = QLabel("wah freq [Hz]: ", self)
        self.wahwah_layout.addWidget(wah_freq_label) 
        self.wah_freq_spinbox = QSpinBox()
        self.wahwah_layout.addWidget(self.wah_freq_spinbox) 
        self.wah_freq_spinbox.setRange(1000, 5000)
        self.wah_freq_spinbox.setValue(2000)


        wah_damping_label = QLabel("damping factor: ", self)
        self.wahwah_layout.addWidget(wah_damping_label) 
        self.wah_damping_spinbox = QDoubleSpinBox()
        self.wahwah_layout.addWidget(self.wah_damping_spinbox) 
        self.wah_damping_spinbox.setRange(0.01, 0.99)    
        self.wah_damping_spinbox.setValue(0.2)

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

    def get_echo_delay(self):
        return self.echo_delay_spinbox.value()  
    def get_echo_decay(self):
        return self.echo_decay_spinbox.value()  
    def get_flanger_maxdelay(self):
        return self.flanger_delay_spinbox.value()
    def get_flanger_freq(self):
        return self.flanger_fflanger_spinbox.value()
    def get_wahwah_freq(self):
        return self.wah_freq_spinbox.value()
    def get_wahwah_damp(self):
        return self.wah_damping_spinbox.value()

    def get_track_specs(self):

        label = self.get_track_label_text()
        combo = self.get_instrument_combo_value()
        vol = self.get_volume_slider_value()
        echo = self.get_echo_on()
        echoval = self.get_echo_number()
        flanger = self.get_flanger_on()
        wahwah = self.get_wahwah_on()
        echodelay = self.get_echo_delay()
        echodecay = self.get_echo_decay()
        flangermaxdelay = self.get_flanger_maxdelay()
        flangerfreq = self.get_flanger_freq()
        wahfreq = self.get_wahwah_freq()
        wahdamp = self.get_wahwah_damp()

        if label[13:15].isnumeric():
            ind = int(label[13:15])
        else:
            ind = int(label[13])

        trackSpecs = {
            'volume':vol, 
            'instrument':combo, 
            'index':ind, 
            'echo':echo,
            'echodelay':echodelay,
            'echodecay':echodecay,
            'echoval':echoval, 
            'flanger':flanger,
            'flangermaxdelay':flangermaxdelay,
            'flangerfreq': flangerfreq,
            'wahwah':wahwah,
            'wahfreq':wahfreq,
            'wahdamp':wahdamp
            }

        return trackSpecs