'''
pyusb
pyserial
opencv-python
'''

import logging
import serial
# import os
# import pathlib
# import tensorflow as tf
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

'''
ARC
CP2102 -> /dev/USB0
FT232 -> /dev/USB1 
Baudrate -> 115200'''

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

def read_data(port, baudrate):
    ser = serial.Serial(port, baudrate, timeout=0.5)
    while True:
        data = ser.readall().decode()  # 讀取全部字節串
        print(data)



def main():
    logging.info('Start Picture')
    take_picture()
    logging.info('End Picture')
    logging.info('Start USB list')
    usb_li = usb_list()
    logging.info('End USB list')
    logging.info('Start Send data')
    #0 -> neg 1 -> Postive
    for i in usb_li:
        logging.info(f"Send data to {i.device}")
        send_data(i.device, 115200, "0")
        send_data(i.device, 115200, "56")
        send_data(i.device, 115200, "0")
        send_data(i.device, 115200, "88")
        logging.info(f"Send data to {i.device} end")
    logging.info('End Send data')

if __name__ == '__main__':
    logging.info('Start main')
    main()
    logging.info('End main')
    logging.info('Start Read data')
    port = '/dev/ttyUSB1'
    baudrate = 115200
    read_data(port, baudrate)