from PIL import ImageGrab
import numpy as np
import cv2, time
import imagezmq, configparser, os

config = configparser.ConfigParser()
HOSTNAME = ""
SERVER = ""
PORT = ""
if os.path.exists('config.ini'):
    config.read('config.ini')
    HOSTNAME = config['DEFAULT'].get('station')
    SERVER = config['DEFAULT'].get('server')
    PORT = config['DEFAULT'].get('port')
else:
    exit(1111)

sender = imagezmq.ImageSender(connect_to=f"tcp://{SERVER}:{PORT}", REQ_REP=True)

while(True):
    img = ImageGrab.grab(bbox=None) #bbox specifies specific region (bbox= x,y,width,height)
    img_np = np.array(img)
    # img_res = cv2.resize(img_np, dsize=(1024, 768), interpolation=cv2.INTER_CUBIC)
    time.sleep(1) # lehet várakozni, mivel nem változik állandóan a kép
    sender.send_image(HOSTNAME, img_np)

