import sys 
import serial
import time
import threading
import serial.tools.list_ports
from prettytable import PrettyTable 


def clear(string: str) -> str:
    string = string.decode('ascii')
    for i in ["firmware:", "version:", "protocols:"]:
        string = string.replace(i, '').replace('\n', '').replace('\r', '')
    return string

def width(string: str, string1: str = "")-> int:
    return len(string) + len(string1) + 4


class TimeoutException(Exception):
    pass

def write_with_timeout(serialPort, data, timeout=0.5):
    """
    Write data to the serial port with a timeout.

    Args:
        serialPort: The serial port to write to.
        data: The data to write.
        timeout: The timeout in seconds.

    Raises:
        TimeoutException: If the write operation times out.
    """
    def write_thread():
        try:
            serialPort.write(data)
        except Exception as e:
            raise TimeoutException(e)

    thread = threading.Thread(target=write_thread)
    thread.start()
    thread.join(timeout)
    
    if thread.is_alive():
        raise TimeoutException("Write operation timed out.")


class Controler:
    def __init__(self):
        self.devices = []
        self.myTable = PrettyTable(["Device", "Port", "Firmware", "Driver"]) 
        self.serialPort = self.Port()
    
    def Port(self):
        ports = serial.tools.list_ports.comports(include_links=False) # auto found
        a = 0

        for port in ports:
            serialPort = serial.Serial(
                port=port.device, baudrate=115200, bytesize=8, timeout=0.4, stopbits=serial.STOPBITS_ONE
            )
            time.sleep(2)
            serialPort.write("cmd:info".encode("ascii"))
            b = 0
            while b < 10: 
                serialData = serialPort.readlines() # save to list 
                time.sleep(0.10)
                b += 1
                if serialData:
                    break
            
            
            for data in serialData:
                if "IR Dongle" in data.decode("ascii"):
                    self.devices.append(f"ir{a}")
                    self.myTable.add_row([self.devices[a], port.device, clear(serialData[1])+clear(serialData[2]), port.description])
                    a += 1
                    
        self.Info()
        
        return serialPort
    
    
    def Info(self):
        print()
        print(self.myTable)
        print()
        

a = Controler()
