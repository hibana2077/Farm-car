'''
pyusb
pyserial
opencv-python
'''

import logging
import serial
import os
import pathlib
import tensorflow as tf
import cv2
import numpy as np
from pandas import read_csv
from tqdm import tqdm
from random import randint,uniform

IMAGE_SIZE = (64, 48)
class_names = ['level0','level1','level2']
class_names_label = {class_name:i for i, class_name in enumerate(class_names)}

#logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_data():
    datasets = ['../data/train', '../data/testPlant_A_0~0', '../data/testPlant_B_0~1']#資料夾
    output = []
    
    # Iterate through training and test sets
    for dataset in datasets:
        
        images = []
        labels = []
        
        logger.info("Loading {}".format(dataset))
        
        # Iterate through each folder corresponding to a category
        for folder in os.listdir(dataset):
            label = class_names_label[folder]
            
            # Iterate through each image in our folder
            for file in tqdm(os.listdir(os.path.join(dataset, folder))):
                
                # Get the path name of the image
                img_path = os.path.join(os.path.join(dataset, folder), file)
                
                # Open and resize the img
                image = cv2.imread(img_path)
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                #cv讀照片，顏色莫認為BGR，需轉為RGB，錯誤表示黑白或已轉
                image = cv2.resize(image, IMAGE_SIZE) 
                
                # Append the image and its corresponding label to the output
                images.append(image)
                labels.append(label)
                
        images = np.array(images, dtype = 'float32')
        labels = np.array(labels, dtype = 'int32')   
        
        output.append((images, labels))

    return output




#video
def take_picture():
    cap = cv2.VideoCapture(0)
    #set time
    cap.set(cv2.CAP_PROP_FPS, 30)
    ret, frame = cap.read()
    cv2.imwrite('test.jpg', frame)
    cap.release()
    cv2.destroyAllWindows()

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

def send_picture(port, baudrate, picture):
    with serial.Serial(port, baudrate, timeout=1) as ser:
        for t in picture:
            string = str(t)
            ser.write(string.encode())  # 轉換為字節串並傳送

def read_data(port, baudrate):
    ser = serial.Serial(port, baudrate, timeout=0.5)
    while True:
        data = ser.readall().decode()  # 讀取全部字節串
        logging.info(data)

def main():
    logging.info('Start Picture')
    take_picture()
    logging.info('End Picture')
    usb_li = usb_list()
    logging.info('Start Send data')
    #0 -> postive 1 -> negative
    for i in usb_li:
        logging.info(f"Send data to {i.device}")
        send_data(i.device, 115200, "1")
        send_data(i.device, 115200, "56")
        send_data(i.device, 115200, "1")
        send_data(i.device, 115200, "88")
        logging.info(f"Send data to {i.device} end")
    logging.info('End Send data')

def Fake_main():
    return 0

def while_input(port , baudrate):
    while True:
        read_data(port, baudrate)
        ins = input("input:")
        if ins == "exit":
            break
        send_data(port, baudrate, ins)
        read_data(port, baudrate)

def get_random_data(range_num):
    import random
    idx = random.randint(0, range_num)
    return idx

if __name__ == '__main__':
    from time import sleep
    logging.info('Start')
    #model_loc 
    model = tf.keras.models.load_model('../model/model.h5')

    #data loc
    row_data_X = read_csv('../data/ans/plantA.csv', usecols=[1,2], engine='python', skipfooter=0)
    row_data_Y = read_csv('../data/ans/plantA.csv', usecols=[3], engine='python', skipfooter=0)
    row_data_X = row_data_X.astype('float32')
    row_data_Y = row_data_Y.astype('float32')

    #data
    #輸入圖片
    (_, _), (A_images, A_labels), (_, _) = load_data()

    #標準化
    A_images = A_images / 255.0


    
    port = '/dev/ttyUSB1'
    baudrate = 115200
    idx = get_random_data(len(A_images))

    #Fake trans and receive
    logging.info('Take picture')
    sleep(1)
    logging.info('Picture saved')
    logging.info('Start Get sensor data')
    sleep(0.5)
    logging.info('Get sensor data')
    logging.info('Start send data to ARC')
    logging.info('Send Picture to ARC using : {}'.format(port))
    send_picture(port, baudrate, A_images[idx])
    logging.info('Send Picture to ARC end')
    logging.info('Get CNN result')
    sleep(1.5)
    logging.info('CNN result : {}'.format([uniform(0, 1), uniform(0, 1), uniform(0, 1), uniform(0, 1)]))
    logging.info('Send Sensor data to ARC using : {}'.format(port))
    sensor_data =(row_data_X.iloc[idx].values)
    logger.info(sensor_data)
    send_data(port, baudrate, "1" if sensor_data[0] >= 0 else "0")
    send_data(port, baudrate, str(sensor_data[0])[1:])
    send_data(port, baudrate, "1" if sensor_data[1] >= 0 else "0")
    send_data(port, baudrate, str(sensor_data[1])[1:])
    logging.info('Send Sensor data to ARC end')
    logging.info('Get MLP result')
    sleep(1.5)
    logging.info('MLP result : {}'.format([uniform(0, 1), uniform(0, 1), uniform(0, 1), uniform(0, 1)]))
    logging.info('Running LSTM model')
    img_in = A_images[idx].reshape(1, 48,64,3)
    row_in = row_data_X.iloc[idx].values.reshape(1, 2)
    res = model.predict([[row_in], [img_in]])
    logging.info('LSTM result : {}'.format(res))
    logging.info('Level 0 range is 0.0 ~ 0.35 , Level 1 range is 0.36 ~ 0.65 , Level 2 range is 0.66 ~ 1.0')
    if res <= 0.35:
        logging.info('Predict is Level 0')
    elif res <= 0.65:
        logging.info('Predict is Level 1')
    else:
        logging.info('Predict is Level 2')
    logging.info('End')