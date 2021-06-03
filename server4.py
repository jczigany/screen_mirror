import socket, threading, time, pickle, cv2, struct, _thread
from PySide2.QtCore import QThread, Qt, Slot, QObject, Signal
from PySide2.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton, QTabWidget, QWidget, QDialog
from PySide2.QtGui import QImage, QPixmap

class Mainwindow(QMainWindow):
    def __init__(self):
        super(Mainwindow, self).__init__()
        tabs = QTabWidget()
        tabs.setTabPosition(QTabWidget.West)
        tabs.setMovable(True)

        self.screen1_label = QLabel(self)
        self.screen1_label.resize(800, 600)
        self.screen2_label = QLabel(self)
        self.screen2_label.resize(800, 600)
        tabs.addTab(self.screen1_label, "Station-1")
        tabs.addTab(self.screen2_label, "Station-2")

        self.setCentralWidget(tabs)
        self.szerver = self.create_socket()
        threading.Thread(target=self.hatter_folyamat).start()

    def create_socket(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        port = 12345
        server_socket.bind(('127.0.0.1', port))
        server_socket.listen(10)
        print('[INFO]: Server Started')
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
        payload = pickle.loads(received_payload)
        return (data_id, payload)

    def hatter_folyamat(self):
        conn, (address, port) = self.szerver.accept()
        # conn_name = '{}|{}'.format(address, port)
        # print("[INFO]: Accepted the connection from {}".format(conn_name))
        # self.send_data(conn, 'Connection accepted')
        while True:
            data_id, payload = self.receive_data(conn)
            print('---Recieved DATA---')
            rgbImage = cv2.cvtColor(payload, cv2.COLOR_BGR2RGB)
            h, w, ch = rgbImage.shape
            bytesPerLine = ch * w
            convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
            p = convertToQtFormat.scaled(800, 600, Qt.KeepAspectRatio)
            if data_id == 1:
                self.screen1_label.setPixmap(QPixmap.fromImage(p))
            elif data_id == 2:
                self.screen2_label.setPixmap(QPixmap.fromImage(p))
            self.send_data(conn, 'Image received on server:' + str(data_id))
        conn.close()

if __name__ == '__main__':
    app = QApplication([])
    win = Mainwindow()
    win.show()
    app.exec_()