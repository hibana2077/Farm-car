'''
pyusb
pyserial
opencv-python
'''

import logging
import serial
import os
import cv2 as cv

#logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

#video
def take_picture():
    cap = cv.VideoCapture(0)
    #set time
    cap.set(cv.CAP_PROP_FPS, 30)
    ret, frame = cap.read()
    cv.imwrite('test.jpg', frame)
    cap.release()
    cv.destroyAllWindows()

#usb device list
def usb_list():
    import serial.tools.list_ports

    ports = serial.tools.list_ports.comports()

    for port in ports:
        logging.info(port)

def main():
    logging.info('Start Picture')
    take_picture()
    logging.info('End Picture')
    logging.info('Start USB list')
    usb_list()
    logging.info('End USB list')

if __name__ == '__main__':
    logging.info('Start main')
    main()