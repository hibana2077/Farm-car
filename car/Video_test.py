'''
Author: hibana2077 hibana2077@gmaill.com
Date: 2023-05-20 19:49:38
LastEditors: hibana2077 hibana2077@gmaill.com
LastEditTime: 2023-05-20 19:52:27
FilePath: /Farm-car/car/Video_test.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import logging
import os
import cv2 as cv

#logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

#video
def take_picture():
    cap = cv.VideoCapture(0)
    ret, frame = cap.read()
    cv.imwrite('test.jpg', frame)
    cap.release()
    cv.destroyAllWindows()

def main():
    logging.info('Start')
    take_picture()
    logging.info('End')

if __name__ == '__main__':
    logging.info('Start main')
    main()