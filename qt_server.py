from PySide2.QtNetwork import QTcpSocket, QTcpServer, QHostAddress, QAbstractSocket
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

        label = QLabel("Szerver Port:")
        self.lineEdit_Port = QLineEdit("8765")
        self.pushButton_Listen = QPushButton("Listen")
        self.pushButton_Send = QPushButton("Send")
        self.pushButton_Send.setEnabled(False)

        hatter_gombok.addWidget(label)
        hatter_gombok.addWidget(self.lineEdit_Port)
        hatter_gombok.addWidget(self.pushButton_Listen)

        self.textEdit_Recv = QTextEdit()
        self.textEdit_Send = QTextEdit()

        hatter_szovegek.addWidget(self.textEdit_Recv)
        hatter_szovegek.addWidget(self.textEdit_Send)
        hatter_szovegek.addWidget(self.pushButton_Send)

        # self.socket = QTcpSocket()
        self.server = QTcpServer()
        self.socket = QTcpSocket()
        # port = 8765
        # self.server.listen(QHostAddress.Any, port)
        print(self.server)
        self.pushButton_Listen.clicked.connect(self.on_pushButton_Listen_clicked)
        self.pushButton_Send.clicked.connect(self.on_pushButton_Send_clicked)
        self.server.newConnection.connect(self.server_New_Connect)


    def on_pushButton_Listen_clicked(self):
        print(self.pushButton_Listen.text())
        if self.pushButton_Listen.text() == "Listen":
            port = int(self.lineEdit_Port.text())
            print(port)
            if not self.server.listen(QHostAddress.Any, port):
                qDebug(self.server.errorString())
                return

            self.pushButton_Listen.setText("Cancel Listen")
            qDebug("Listen successfully!")
        else:
            if self.socket.state() == QAbstractSocket.ConnectedState:
                self.socket.disconnectFromHost()
            self.server.close()
            self.pushButton_Listen.setText("Listen")
            self.pushButton_Send.setEnabled(False)

    def on_pushButton_Send_clicked(self):
        qDebug("Send:" + self.textEdit_Send.toPlainText())
        self.socket.write(self.textEdit_Send.toPlainText())
        self.socket.flush()

    def server_New_Connect(self):

        self.socket = self.server.nextPendingConnection()
        #
        #
        self.socket.readyRead.connect(self.socket_Read_Data)
        self.socket.disconnected.connect(self.socket_Disconnected)
        self.pushButton_Send.setEnabled(True)
        qDebug("A client connect!")

    def socket_Read_Data(self):
        buffer = QByteArray()
        buffer = self.socket.readAll()
        print(buffer)
        if not buffer.isEmpty():
            st = self.textEdit_Recv.toPlainText()
            st += str(buffer.data())
            self.textEdit_Recv.setText(st)

    def socket_Disconnected(self):
        self.pushButton_Send.setEnabled(False)
        qDebug("Disconnected!")

if __name__ == '__main__':
    app = QApplication([])
    win = MainWindow()
    win.show()
    app.exec_()