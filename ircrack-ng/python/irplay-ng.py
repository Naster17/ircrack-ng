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
        a = 0
        ports = serial.tools.list_ports.comports(include_links=False) # auto found
        for port in ports:
            serialPort = serial.Serial(
                port=port.device, baudrate=115200, bytesize=8, timeout=0.5, stopbits=serial.STOPBITS_ONE
            )
            time.sleep(0.2)
            serialPort.write("cmd:info".encode("ascii"))
            serialData = serialPort.readlines() # save to list 
            
            for data in serialData:
                if "IR Dongle" in data.decode("ascii"):
                    self.devices.append(f"ir{a}")    
                    a += 1
                    return serialPort     
    
    
    def SendPacket(self):
        print(self.devices)
        
        self.serialPort.write("cmd:wewe".encode("ascii"))
        while 1: 
            serialData = self.serialPort.readlines() # save to list 
            if serialData:
                break
        print(serialData)
        
    
a = Controler()
a.SendPacket()