import serial
import time
import serial.tools.list_ports
from prettytable import PrettyTable 
import argparse
from enum import Enum


class Protocol(Enum):
    UNKNOWN = 0
    PULSE_WIDTH = 1
    PULSE_DISTANCE = 2
    APPLE = 3
    DENON = 4
    JVC = 5
    LG = 6
    LG2 = 7
    NEC = 8
    NEC2 = 9  # NEC with full frame as repeat
    ONKYO = 10
    PANASONIC = 11
    KASEIKYO = 12
    KASEIKYO_DENON = 13
    KASEIKYO_SHARP = 14
    KASEIKYO_JVC = 15
    KASEIKYO_MITSUBISHI = 16
    RC5 = 17
    RC6 = 18
    SAMSUNG = 19
    SAMSUNGLG = 20
    SAMSUNG48 = 21
    SHARP = 22
    SONY = 23
    # Now the exotic protocols
    BANG_OLUFSEN = 24
    BOSEWAVE = 25
    LEGO_PF = 26
    MAGIQUEST = 27
    WHYNTER = 28
    FAST = 29
    

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
    
    
    def SendPacket(self, protocol, address, command):
        # example: cmd:send protocol: 8 address: 61184 command: 2 Repeats: 10 # 
        self.serialPort.readall()
        if "0x" in address or "0X" in address:
            print(f"{self.devices[0]}:\n\tprotocol: {protocol}\n\taddress:  {address}\n\tcommand:  {command}")
            self.serialPort.write(f"cmd:send protocol: {protocol} address: {int(address, 16)} command: {int(command, 16)}".encode("ascii"))
        else:
            print(f"{self.devices[0]}:\n\tprotocol: {protocol}\n\taddress:  0x{hex(int(address)).upper()[2:]}\n\tcommand:  0x{hex(int(command)).upper()[2:]}")
            self.serialPort.write(f"cmd:send protocol: {protocol} address: {address} command: {command}".encode("ascii"))
    
    
parser = argparse.ArgumentParser(description="Decode type argument example")
parser.add_argument("-a", "--address", metavar="", type=str, default='0', required=True, help="Address: (HEX or Decimal, 0xEF00/61184 ...)")
parser.add_argument("-c", "--command", metavar="", type=str, default='0', required=True, help="Command: (HEX or Decimal, 0x2/2 ...)")
parser.add_argument("-p", "--protocol", metavar="", type=int, default=8, required=True, help="Protocol (Name or Value, NEC/8 ...)")

args = parser.parse_args()

a = Controler()
a.SendPacket(args.protocol, args.address, args.command)