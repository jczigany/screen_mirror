import socket
import threading
import time
import pickle
import cv2
import struct
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


def send_data(conn, payload, data_id=0):
    '''
    @brief: send payload along with data size and data identifier to the connection
    @args[in]:
        conn: socket object for connection to which data is supposed to be sent
        payload: payload to be sent
        data_id: data identifier
    '''
    # serialize payload
    serialized_payload = pickle.dumps(payload)
    # send data size, data identifier and payload
    conn.sendall(struct.pack('>I', len(serialized_payload)))
    conn.sendall(struct.pack('>I', data_id))
    conn.sendall(serialized_payload)


def receive_data(conn):
    '''
    @brief: receive data from the connection assuming that
        first 4 bytes represents data size,
        next 4 bytes represents data identifier and
        successive bytes of the size 'data size'is payload
    @args[in]:
        conn: socket object for conection from which data is supposed to be received
    '''
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


def do_something(conn_name, data):
    '''
    @beief: a sample function to do something with received data
    @args[in]:
        conn_name: connection name from where dat is received
        data: received data
    @args[out]:
        a string response
    '''
    print('Data number {} received from client {}'.format(
        data['data number'], conn_name))
    time.sleep(0.1)
    return 'Data number {} received on server'.format(data['data number'])


# def handle_client(conn, conn_name):
#     changePixmap = Signal(str)
#     while True:
#         data_id, payload = receive_data(conn)
#         if data_id == data_identifiers['image']:
#             print('---Recieved image too ---')
#             self.changePixmap.emit('localhost')
#             # cv2.imwrite('server_data/received_image.png', payload)
#             send_data(conn, 'Image received on server')
#         # elif data_id == data_identifiers['data']:
#         #     response = do_something(conn_name, payload)
#         #     send_data(conn, response)
#
#     conn.close()


# define identifiers for data which could be used to take certain action for data
data_identifiers = {'info': 0, 'data': 1, 'image': 2}
# key to trust a connection
key_message = 'C0nn3c+10n'

def create_socket():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = 12345
    server_socket.bind(('127.0.0.1', port))
    server_socket.listen(5)
    print('[INFO]: Server Started')
    return server_socket


class Thread(QThread):
    def __init__(self, parent):
        super(Thread, self).__init__(parent)
    # changePixmap = Signal(QImage, str)
    # changePixmap = Signal(str)
    # hostname = 'localhost'

    def run(self):
        szerver = create_socket()
        conn, (address, port) = szerver.accept()
        conn_name = '{}|{}'.format(address, port)
        # print("[INFO]: Accepted the connection from {}".format(conn_name))
        # send_data(conn, 'Connection accepted')
        threading.Thread(target=self.parent().handle_client, args=(conn,)).start()
        # self.changePixmap.emit(p, hostname)
        # self.changePixmap.emit('localhost')

        szerver.close()
        # print('[INFO]: Server Closed')


class MainApp(QMainWindow):
    def __init__(self):
        super(MainApp, self).__init__()
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
        # th.changePixmap.connect(self.setImage)
        # self.handle_client.changePixmap.connect(self.setImage)
        th.start()

    def handle_client(self, conn):
        changePixmap = Signal(str)
        while True:
            data_id, payload = receive_data(conn)
            if data_id == data_identifiers['image']:
                print('---Recieved image too ---')
                # self.changePixmap.emit('localhost')
                self.setImage('localhost')
                # cv2.imwrite('server_data/received_image.png', payload)
                send_data(conn, 'Image received on server')
            # elif data_id == data_identifiers['data']:
            #     response = do_something(conn_name, payload)
            #     send_data(conn, response)

        conn.close()

    # @Slot(QImage, str)
    @Slot(str)
    # def setImage(self, image, hostname):
    def setImage(self, hostname):
        print("változás fogadva")
        # self.screen1_label.setPixmap(QPixmap.fromImage(image))
        # if hostname == "Board-1":
        #     self.screen1_label.setPixmap(QPixmap.fromImage(image))
        # if hostname == "Station_2":
        #     self.screen2_label.setPixmap(QPixmap.fromImage(image))

        # szerver = create_socket()
        # conn, (address, port) = szerver.accept()
        # conn_name = '{}|{}'.format(address, port)
        # print("[INFO]: Accepted the connection from {}".format(conn_name))
        # send_data(conn, 'Connection accepted')
        # threading.Thread(target=handle_client, args=(conn, conn_name)).start()
        # print("jött valami")
        #
        # szerver.close()
        # print('[INFO]: Server Closed')

if __name__ == '__main__':
    app = QApplication([])
    win = MainApp()
    win.show()
    app.exec_()
