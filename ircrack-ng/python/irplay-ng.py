import serial
import time
import serial.tools.list_ports
from prettytable import PrettyTable 


def clear(string: str) -> str:
    string = string.decode('ascii')
    for i in ["firmware:", "version:", "protocols:"]:
        string = string.replace(i, '').replace('\n', '').replace('\r', '')
    return string

def width(string: str, string1: str = "")-> int:
    return len(string) + len(string1) + 4

class Controler:
    def __init__(self):
        self.devices = []
        self.serialPort = self.Port()
        
    def Port(self):
        ports = serial.tools.list_ports.comports(include_links=False) # auto found
        a = 0
        
        for port in ports:
            serialPort = serial.Serial(
                port=port.device, baudrate=115200, bytesize=8, timeout=0.5, stopbits=serial.STOPBITS_ONE
            )
            time.sleep(0.2)
            serialPort.write("info".encode("ascii"))
            serialData = serialPort.readlines() # save to list 
            serialData.append(bytes(port.description, "ascii"))
            
            for data in serialData:
                if "IR Dongle" in data.decode("ascii"):
                    self.devices.append(f"ir{a}")    
                    a += 1
                    return serialPort
                    
        return serialPort
    
    def SendPacket(self):
        ...    

    
    
a = Controler()
