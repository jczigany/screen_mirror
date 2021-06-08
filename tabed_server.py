import sys, configparser, os
from PySide2.QtCore import QThread, Qt, Slot, QObject, Signal
from PySide2.QtWidgets import QApplication, QLabel, QMainWindow, QTabWidget
from PySide2.QtGui import QImage, QPixmap
import cv2
import imagezmq

config = configparser.ConfigParser()
IP = ""
PORT = ""
if os.path.exists('server.ini'):
    config.read('server.ini')
    IP = config['DEFAULT'].get('ip')
    PORT = config['DEFAULT'].get('port')
else:
    exit(1111)

imageHub = imagezmq.ImageHub(open_port=f"tcp://{IP}:{PORT}", REQ_REP=True)


class Thread(QThread):
    changePixmap = Signal(QImage, str)

    def run(self):
        while True:
            (hostname, frame) = imageHub.recv_image()
            imageHub.send_reply(b'OK')
            rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgbImage.shape
            bytesPerLine = ch * w
            convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
            # p = convertToQtFormat.scaled(1280, 1024, Qt.KeepAspectRatio)
            self.changePixmap.emit(convertToQtFormat, hostname)
            # self.changePixmap.emit(p, hostname)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Screen-Mirror")
        self.resize(1340, 1060)
        tabs = QTabWidget()
        tabs.setTabPosition(QTabWidget.West)
        tabs.setMovable(True)

        self.screen1_label = QLabel(self)
        self.screen1_label.resize(1280, 1024)
        self.screen2_label = QLabel(self)
        self.screen2_label.resize(1280, 1024)
        self.screen3_label = QLabel(self)
        self.screen3_label.resize(1280, 1024)
        self.screen4_label = QLabel(self)
        self.screen4_label.resize(1280, 1024)
        self.screen5_label = QLabel(self)
        self.screen5_label.resize(1280, 1024)
        self.screen6_label = QLabel(self)
        self.screen6_label.resize(1280, 1024)
        self.screen7_label = QLabel(self)
        self.screen7_label.resize(1280, 1024)

        tabs.addTab(self.screen1_label, "Tábla 1")
        tabs.addTab(self.screen2_label, "Tábla 2")
        tabs.addTab(self.screen3_label, "Tábla 3")
        tabs.addTab(self.screen4_label, "Tábla 4")
        tabs.addTab(self.screen5_label, "Tábla 5")
        tabs.addTab(self.screen6_label, "Tábla 6")
        tabs.addTab(self.screen7_label, "CENTER")

        self.setCentralWidget(tabs)

        th = Thread(self)
        th.changePixmap.connect(self.setImage)
        th.start()

    @Slot(QImage, str)
    def setImage(self, image, hostname):
        if hostname == "Station_1":
            self.screen1_label.setPixmap(QPixmap.fromImage(image))
        if hostname == "Station_2":
            self.screen2_label.setPixmap(QPixmap.fromImage(image))
        if hostname == "Station_3":
            self.screen3_label.setPixmap(QPixmap.fromImage(image))
        if hostname == "Station_4":
            self.screen4_label.setPixmap(QPixmap.fromImage(image))
        if hostname == "Station_5":
            self.screen5_label.setPixmap(QPixmap.fromImage(image))
        if hostname == "Station_6":
            self.screen6_label.setPixmap(QPixmap.fromImage(image))
        if hostname == "Center":
            self.screen7_label.setPixmap(QPixmap.fromImage(image))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()