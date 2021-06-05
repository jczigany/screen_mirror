import sys
from PySide2.QtCore import QThread, Qt, Slot, QObject, Signal
from PySide2.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QTabWidget,
    QWidget,
)
from PySide2.QtGui import QImage, QPixmap
import cv2
import imagezmq

imageHub = imagezmq.ImageHub(open_port='tcp://192.168.68.3:5555', REQ_REP=True)


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
            p = convertToQtFormat.scaled(800, 600, Qt.KeepAspectRatio)
            self.changePixmap.emit(p, hostname)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Screen-Mirror")

        tabs = QTabWidget()
        tabs.setTabPosition(QTabWidget.West)
        tabs.setMovable(True)

        self.screen1_label = QLabel(self)
        self.screen1_label.resize(800, 600)
        self.screen2_label = QLabel(self)
        self.screen2_label.resize(800, 600)
        # for n, color in enumerate(["red", "green", "blue", "yellow"]):
        tabs.addTab(self.screen1_label, "Station-1")
        tabs.addTab(self.screen2_label, "Station-2")

        self.setCentralWidget(tabs)

        th = Thread(self)
        th.changePixmap.connect(self.setImage)
        th.start()

    @Slot(QImage, str)
    def setImage(self, image, hostname):
        if hostname == "Board-1":
            self.screen1_label.setPixmap(QPixmap.fromImage(image))
        if hostname == "Station_2":
            self.screen2_label.setPixmap(QPixmap.fromImage(image))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()