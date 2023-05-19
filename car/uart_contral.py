import serial
import serial.tools.list_ports
import os
import time
import logging

#logging setting
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
logging.info('Start print log')

#list all port
def list_all_port():
    port_list = list(serial.tools.list_ports.comports())
    if len(port_list) == 0:
        logging.info('No port found')
        return None
    else:
        for i in range(0,len(port_list)):
            logging.info(port_list[i])
        return port_list


# ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1) #name,baudrate,timeout

# ser.write(b'hello') #send data

# data = ser.readline() #read data

# print(data)

# ser.close() #close port

def send_data(data:str):
    ser = serial.Serial('COM3', 9600, timeout=1) #name,baudrate,timeout
    ser.write(data.encode('utf-8')) #send data
    ser.close() #close port

if __name__ == '__main__':
    while True:
        try:
            list_result = list_all_port()
            if list_result is not None:
                send_data('hello')
            time.sleep(1)
        except KeyboardInterrupt:
            logging.info('KeyboardInterrupt detected')
            break
        except Exception as e:
            logging.error(e)
            break
        finally:
            logging.info('Run finally')