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
        self.myTable = PrettyTable(["Device", "Firmware", "Driver"]) 
        self.serialPort = self.Port()
    
    def Port(self):
        ports = serial.tools.list_ports.comports(include_links=False) # auto found
        
        for port in ports:
            serialPort = serial.Serial(
                port=port.device, baudrate=115200, bytesize=8, timeout=0.4, stopbits=serial.STOPBITS_ONE
            )
            time.sleep(0.2)
            serialPort.write("info".encode("ascii"))
            serialData = serialPort.readlines() # save to list 
            serialData.append(bytes(port.description, "ascii"))
            
            a = 0
            for data in serialData:
                if "IR Dongle" in data.decode("ascii"):
                    self.devices.append(f"ir{a}")
                    self.myTable.add_row([self.devices[a], clear(serialData[1])+clear(serialData[2]), clear(serialData[4])])
                    a += 1
                else:
                    serialPort.close()
                    
        self.Info(serialData)
        return serialPort
    
    
    def Info(self, info: list):
        print()
        print(self.myTable)
    
    
a = Controler()
