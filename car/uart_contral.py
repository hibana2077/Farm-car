'''
Author: hibana2077 hibana2077@gmaill.com
Date: 2023-05-20 19:49:22
LastEditors: hibana2077 hibana2077@gmaill.com
LastEditTime: 2023-05-21 20:08:28
FilePath: /Farm-car/car/uart_contral.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import serial
import serial.tools.list_ports
import os
import time
import logging

#logging setting
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
logging.info('Start print log')

#forword function
def forword(step,port,boudrate):
    with serial.Serial(port,boudrate,timeout=1) as ser:
        ser.write(f"forword {step}".encode())
    logging.info(f"forword {step}")


# ports = serial.tools.list_ports.main()
# for t in ports:logging.info(t.device)
# if len(ports) == 0:
#     logging.info("No USB device")
#     print(ports)
print(serial.tools.list_ports.main())
print(serial.tools.list_ports.comports())
print(serial.tools.list_ports.grep())