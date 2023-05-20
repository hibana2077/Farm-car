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
    return ports

def send_data(port, baudrate, data):
    with serial.Serial(port, baudrate, timeout=1) as ser:
        ser.write(data.encode())  # 轉換為字節串並傳送

def main():
    logging.info('Start Picture')
    take_picture()
    logging.info('End Picture')
    logging.info('Start USB list')
    usb_li = usb_list()
    logging.info('End USB list')
    logging.info('Start Send data')
    for i in usb_li:
        print(i.device)
    logging.info('End Send data')

if __name__ == '__main__':
    logging.info('Start main')
    main()
    logging.info('End main')