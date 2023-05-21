'''
Author: hibana2077 hibana2077@gmaill.com
Date: 2023-05-21 20:15:20
LastEditors: hibana2077 hibana2077@gmaill.com
LastEditTime: 2023-05-21 20:18:48
FilePath: /Farm-car/car/temp_uart.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE

'''
import serial

# while True:
#     uart.write(b'Hello from Jetson Nano!\n')
#     time.sleep(1)

#/dev/ttyTHS1  /dev/ttyTHS2
THS_list = ['/dev/ttyTHS1','/dev/ttyTHS2']
#/dev/ttyS0  /dev/ttyS1  /dev/ttyS2  /dev/ttyS3
S_list = ['/dev/ttyS0','/dev/ttyS1','/dev/ttyS2','/dev/ttyS3']

for i in THS_list:
    try:
        print(f"Try {i}")
        uart = serial.Serial(
            port=i, 
            baudrate=9600,
            timeout=1
        )
        uart.write(b'Forwd 1000\r\n')
        print(f"Try {i} done")
    except Exception as e:print(e)