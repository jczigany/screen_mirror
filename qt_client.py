from PySide2.QtNetwork import QTcpSocket
from PySide2.QtWidgets import *
from PySide2.QtCore import *
import sys


class MainWindow(QDialog):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent=None)
        hatter = QVBoxLayout()
        self.setLayout(hatter)
        hatter_gombok = QHBoxLayout()
        hatter_szovegek = QVBoxLayout()
        hatter.addLayout(hatter_gombok)
        hatter.addLayout(hatter_szovegek)

        label = QLabel("Szerver IP:")
        label_2 = QLabel("Szerver Port:")
        self.lineEidt_IP = QLineEdit("127.0.0.1")
        self.lineEdit_Port = QLineEdit("8765")
        self.pushButton_Connect = QPushButton("Connect")
        self.pushButton_Send = QPushButton("Send")
        self.pushButton_Send.setEnabled(False)

        hatter_gombok.addWidget(label)
        hatter_gombok.addWidget(self.lineEidt_IP)
        hatter_gombok.addWidget(label_2)
        hatter_gombok.addWidget(self.lineEdit_Port)
        hatter_gombok.addWidget(self.pushButton_Connect)

        self.textEdit_Recv = QTextEdit()
        self.textEdit_Send = QTextEdit()

        hatter_szovegek.addWidget(self.textEdit_Recv)
        hatter_szovegek.addWidget(self.textEdit_Send)
        hatter_szovegek.addWidget(self.pushButton_Send)

        self.socket = QTcpSocket()

        self.pushButton_Connect.clicked.connect(self.on_pushButton_Connect_clicked)
        self.pushButton_Send.clicked.connect(self.on_pushButton_Send_clicked)
        self.socket.readyRead.connect(self.socket_Read_Data)
        self.socket.disconnected.connect(self.socket_Disconnected)

    def on_pushButton_Connect_clicked(self):
        if self.pushButton_Connect.text() == "Connect":
            IP = self.lineEidt_IP.text()
            port = int(self.lineEdit_Port.text())
            self.socket.abort()
            self.socket.connectToHost(IP, port)
            if not self.socket.waitForConnected(30000):
                qDebug("Connection failed!")
                return
            qDebug("Connect successfully!")
            self.pushButton_Send.setEnabled(True)
            self.pushButton_Connect.setText("Disconnect")
        else:
            self.socket.disconnectFromHost()
            self.pushButton_Connect.setText("Connect")
            self.pushButton_Send.setEnabled(False)

    def on_pushButton_Send_clicked(self):
        qDebug("Send:" + self.textEdit_Send.toPlainText())
        en_szov = self.textEdit_Send.toPlainText().encode()
        ba_szov = bytearray(en_szov)
        self.socket.write(ba_szov)
        self.socket.flush()

    def socket_Read_Data(self):
        buffer = QByteArray()
        buffer = self.socket.readAll()
        if not buffer.isEmpty():
            str = self.textEdit_Recv.toPlainText()
            str += buffer
            self.textEdit_Recv.setText(st)

    def socket_Disconnected(self):
        self.pushButton_Send.setEnabled(False)
        self.pushButton_Connect.setText("Connect")
        qDebug("Disconnected!")

if __name__ == '__main__':
    app = QApplication([])
    win = MainWindow()
    win.show()
    app.exec_()