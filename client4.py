import socket, pickle, cv2, struct, time,configparser, os
from PIL import ImageGrab
import numpy as np

config = configparser.ConfigParser()
HOSTNAME = ""
SERVER = ""
PORT = ""
if os.path.exists('config.ini'):
    config.read('config.ini')
    HOSTNAME = config['DEFAULT'].get('station')
    SERVER = config['DEFAULT'].get('server')
    PORT = config['DEFAULT'].get('port')
    print(HOSTNAME, SERVER, PORT)
else:
    exit(1111)

def send_data(conn, payload, data_id=int(HOSTNAME)):
    '''
    @brief: send payload along with data size and data identifier to the connection
    @args[in]:
        conn: socket object for connection to which data is supposed to be sent
        payload: payload to be sent
        data_id: data identifier
    '''
    # serialize payload
    serialized_payload = pickle.dumps(payload)
    #send data size, data identifier and payload
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

def main():
    # create client socket object and connect it to server
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect(('127.0.0.1', 12345))
    while True:
        # img_np = "sending DATA"
        img = ImageGrab.grab(bbox=None)  # bbox specifies specific region (bbox= x,y,width,height)
        img_np = np.array(img)
        send_data(conn, img_np)
        time.sleep(1)
        print(receive_data(conn)[1])

    conn.close()
    print('[INFO]: Connection closed')


if __name__ == '__main__':
    main()
