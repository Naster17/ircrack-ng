import serial
import time
import serial.tools.list_ports
from prettytable import PrettyTable 
from os import system, name

def cls():
    if name == 'nt':
        system('cls')
    else:
        system('clear')

def clear(string: str) -> str:
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
        a = 0
        ports = serial.tools.list_ports.comports(include_links=False) # auto found
        for port in ports:
            serialPort = serial.Serial(port=port.device, baudrate=115200, bytesize=8, timeout=0.5)
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
                    a += 1
                    return serialPort 
    
    def Listner(self):
        # b'Protocol=NEC Address=0xEF00 Command=0xA Raw-Data=0xF50AEF00 32 bits LSB first\r\n'
        myTable = PrettyTable(["Protocol", "Address", "Command", "Raw Data", "Bits"])
        self.serialPort.write("cmd:start_listner".encode("ascii"))
        cls();
        print("Waiting for packets...")
        while True:
            try:
                serialData = self.serialPort.readline()
                serialData = serialData.decode("ascii")
                if "Repeat" not in serialData and "noise" not in serialData and "packet:" not in serialData and len(serialData) > 5:
                    cls()
                    data = serialData.split()
                    myTable.add_row([clear(data[0]), clear(data[1]), clear(data[2]), clear(data[3]), ' '.join(data[4:])])
                    print(myTable)
                    
            except KeyboardInterrupt:
                self.serialPort.write("stop".encode("ascii"))
                exit(0)
    

    
a = Controler()
a.Listner()
