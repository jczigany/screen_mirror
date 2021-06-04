import socket, threading, time, pickle, cv2, struct, _thread, configparser, os
# from _thread import *
from PySide2.QtCore import QThread, Qt, Slot, QObject, Signal
from PySide2.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton, QTabWidget, QWidget, QDialog
from PySide2.QtGui import QImage, QPixmap

config = configparser.ConfigParser()
IP = ""
PORT = ""
if os.path.exists('server.ini'):
    config.read('server.ini')
    IP = config['DEFAULT'].get('ip')
    PORT = config['DEFAULT'].get('port')
else:
    exit(1111)


class Mainwindow(QMainWindow):
    def __init__(self):
        super(Mainwindow, self).__init__()
        self.resize(1300, 900)
        tabs = QTabWidget()
        tabs.setTabPosition(QTabWidget.West)
        tabs.setMovable(True)

        self.screen1_label = QLabel(self)
        self.screen1_label.resize(1280, 960)
        self.screen2_label = QLabel(self)
        self.screen2_label.resize(1280, 960)
        self.screen3_label = QLabel(self)
        self.screen3_label.resize(1280, 960)
        self.screen4_label = QLabel(self)
        self.screen4_label.resize(1280, 960)
        self.screen5_label = QLabel(self)
        self.screen5_label.resize(1280, 960)
        self.screen6_label = QLabel(self)
        self.screen6_label.resize(1280, 960)
        self.screen7_label = QLabel(self)
        self.screen7_label.resize(1280, 960)


        tabs.addTab(self.screen1_label, "Tábla 1")
        tabs.addTab(self.screen2_label, "Tábla 2")
        tabs.addTab(self.screen3_label, "Tábla 3")
        tabs.addTab(self.screen4_label, "Tábla 4")
        tabs.addTab(self.screen5_label, "Tábla 5")
        tabs.addTab(self.screen6_label, "Tábla 6")
        tabs.addTab(self.screen7_label, "CENTER")

        self.setCentralWidget(tabs)
        self.szerver = self.create_socket()
        # conn, address = self.szerver.accept()
        # _thread.start_new_thread(self.kulon_kliens, (conn,))
        threading.Thread(target=self.hatter_folyamat).start()

    def create_socket(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # port = 12345
        # server_socket.bind(('127.0.0.1', port))
        server_socket.bind((IP, int(PORT)))
        server_socket.listen(10)
        # print('[INFO]: Server Started')
        return server_socket

    def send_data(self, conn, payload, data_id=0):
        # serialize payload
        serialized_payload = pickle.dumps(payload)
        # send data size, data identifier and payload
        conn.sendall(struct.pack('>I', len(serialized_payload)))
        conn.sendall(struct.pack('>I', data_id))
        conn.sendall(serialized_payload)

    def receive_data(self, conn):
        # receive first 4 bytes of data as data size of payload
        data_size = struct.unpack('>I', conn.recv(4))[0]
        # receive next 4 bytes of data as data identifier
        data_id = struct.unpack('>I', conn.recv(4))[0]
        # receive payload till received payload size is equal to data_size received
        received_payload = b""
        reamining_payload_size = data_size
        while reamining_payload_size != 0:
            received_payload += conn.recv(reamining_payload_size)
            reamining_payload_size = data_size - len(received_payload)
            # reamining_payload_size -= len(received_payload)
        payload = pickle.loads(received_payload)
        return (data_id, payload)

    def hatter_folyamat(self):
        threadCount = 0
        while True:
            conn, address = self.szerver.accept()
            _thread.start_new_thread(self.kulon_kliens, (conn,))
            # threadCount += 1
            # print("Thread number: " + str(threadCount))
            # print("Összes szál:---------", threading.active_count())
            # print("Összes szál:*****************", _thread._count())
        conn.close()

    def kulon_kliens(self, conn):
        try:
            while True:
                data_id, payload = self.receive_data(conn)
                rgbImage = cv2.cvtColor(payload, cv2.COLOR_BGR2RGB)
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                p = convertToQtFormat.scaled(1280, 960, Qt.KeepAspectRatio)
                if data_id == 1:
                    self.screen1_label.setPixmap(QPixmap.fromImage(p))
                elif data_id == 2:
                    self.screen2_label.setPixmap(QPixmap.fromImage(p))
                elif data_id == 3:
                    self.screen3_label.setPixmap(QPixmap.fromImage(p))
                elif data_id == 4:
                    self.screen4_label.setPixmap(QPixmap.fromImage(p))
                elif data_id == 5:
                    self.screen5_label.setPixmap(QPixmap.fromImage(p))
                elif data_id == 6:
                    self.screen6_label.setPixmap(QPixmap.fromImage(p))
                elif data_id == 7:
                    self.screen7_label.setPixmap(QPixmap.fromImage(p))
        except:
            conn.close()
            _thread.exit_thread()


if __name__ == '__main__':
    app = QApplication([])
    win = Mainwindow()
    win.show()
    app.exec_()