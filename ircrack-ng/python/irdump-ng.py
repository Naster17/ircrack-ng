import serial
import time
import serial.tools.list_ports
from prettytable import PrettyTable 
from os import system, name


def clear(string: str) -> str:
            # b'Protocol=NEC Address=0xEF00 Command=0xA Raw-Data=0xF50AEF00 32 bits LSB first\r\n'
    try:
        string = string.decode('ascii')
    except:
        pass 
    for i in ["firmware:", "version:", "protocols:", "Protocol=", "Address=", "Command=", "Raw-Data="]:
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
                    print("Found dongle")
                    return serialPort
    
    def cls(self):
        if name == 'nt':
            system('cls')
        else:
            system('clear')
        
    def Listner(self):
        # b'Protocol=NEC Address=0xEF00 Command=0xA Raw-Data=0xF50AEF00 32 bits LSB first\r\n'
        myTable = PrettyTable(["Protocol", "Address", "Command", "Raw Data", "Bits"])
        self.serialPort.write("startListner".encode("ascii"))
        self.cls();
        while True:
            try:
                serialData = self.serialPort.readline()
                serialData = serialData.decode("ascii")
                if "Repeat" not in serialData and "noise" not in serialData and "packet:" not in serialData and len(serialData) > 5:
                    self.cls()
                    data = serialData.split()
                    myTable.add_row([clear(data[0]), clear(data[1]), clear(data[2]), clear(data[3]), ' '.join(data[4:])])
                    print(myTable)
                    
            except KeyboardInterrupt:
                self.serialPort.write("stop".encode("ascii"))
                exit(0)
    
a = Controler()
a.Listner()
