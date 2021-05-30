from PIL import ImageGrab
import numpy as np
import cv2
import imagezmq, configparser, os
# from zlib import compress

config = configparser.ConfigParser()
sender = imagezmq.ImageSender(connect_to='tcp://192.168.68.3:5555', REQ_REP=True)
hostname = "Station_2"

while(True):
    img = ImageGrab.grab(bbox=None) #bbox specifies specific region (bbox= x,y,width,height)
    img_np = np.array(img)
    img_res = cv2.resize(img_np, dsize=(1024, 768), interpolation=cv2.INTER_CUBIC)


    # Itt van az a forrás, amit át kell küldeni, és a szerveren megjeleníteni!!!!
    # cv2.imshow("test", res)
    # time.sleep(1) # lehet várakozni, mivel nem változik állandóan a kép
    sender.send_image(hostname, img_res)

    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break

cv2.destroyAllWindows()