from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QFileDialog, QWidget, QVBoxLayout, QLabel, QPushButton,QMessageBox
from PyQt5.QtGui import QPixmap
import qdarktheme
import sys
import mainwin
from track_widget import *
import backend


class myApp(QtWidgets.QMainWindow, mainwin.Ui_MainWindow):
    def __init__(self, parent=None):
        super(myApp, self).__init__(parent)
        self.setupUi(self)
        self.resize(1000,1000)
        self.scrollArea.setWidgetResizable(True)
        self.scroll_layout = QVBoxLayout(self.scrollAreaWidgetContents)
        self.pushButton.clicked.connect(self.openFileDialog)
        self.synth_button.clicked.connect(self.synthSong)
        backend.initFunc()


        
    def openFileDialog(self):
        options = QFileDialog.Options()
        file_dialog = QFileDialog()
        file_dialog.setOptions(options)
        file_dialog.setNameFilter("MIDI Files (*.mid *.midi)")
        file_dialog.setWindowTitle("Open MIDI File")
        file_dialog.setFileMode(QFileDialog.ExistingFile)

        if file_dialog.exec_() == QFileDialog.Accepted:
            selected_files = file_dialog.selectedFiles()
            if len(selected_files) > 0:
                midi_path = selected_files[0]
                self.filename_label.setText("Selected MIDI File: " + midi_path)


            self.tracklist = backend.pickUpTrackInfo(midi_path)
            self.addTrack()

    def errorWindowPopUp(error_message = "An error occurred!"):  
        message_box = QMessageBox()
        message_box.setIcon(QMessageBox.Critical)
        message_box.setWindowTitle("Error")
        message_box.setText(error_message)
        message_box.exec_()

              
    def addTrack(self):
        self.clear_layout(self.scroll_layout)
        for element in self.tracklist:
            if element[2] != []:
                track_widget = TrackWidget(element[1], element[0])
                track_widget.setMinimumHeight(300) 
                track_widget.setMaximumHeight(300) 
                self.scroll_layout.addWidget(track_widget)

    def clear_layout(self,layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
            else:
                self.clear_layout(item.layout())

    def synthSong(self):
                # Access and print the widgets in the layout
        trackinfo = []
        
        for i in range(self.scroll_layout.count()):

            if (self.scroll_layout.itemAt(i).widget()):

                widget = self.scroll_layout.itemAt(i).widget()
                label = widget.get_track_label_text()
                combo = widget.get_instrument_combo_value()
                vol = widget.get_volume_slider_value()
                echo = widget.get_echo_on()
                echoval = widget.get_echo_number()
                flanger = widget.get_flanger_on()
                wahwah = widget.get_wahwah_on()

                if label[13:15].isnumeric():
                    ind = int(label[13:15])
                else:
                    ind = int(label[13])
                                
            trackSpecs = {
            'volume':vol, 
            'instrument':combo, 
            'index':ind, 
            'echo':echo, 
            'echoval':echoval, 
            'flanger':flanger,
            'wahwah':wahwah
            }

            trackinfo.append(trackSpecs)
        try:
            backend.synthesizeSong(self.tracklist, trackinfo, self.lineEdit.text())
        except:
            self.errorWindowPopUp("Error while processing!")

def main():
    app = QApplication(sys.argv)
    qdarktheme.setup_theme()

    form = myApp()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()
