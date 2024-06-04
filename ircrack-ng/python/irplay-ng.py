import serial
import time
import serial.tools.list_ports
from prettytable import PrettyTable 
import argparse

    
def protocol_to_int(name):
    match name:
        case "PULSE_WIDTH":
            return 1
        case "PULSE_DISTANCE":
            return 2
        case "APPLE":
            return 3
        case "DENON":
            return 4
        case "JVC":
            return 5
        case "LG":
            return 6
        case "LG2":
            return 7
        case "NEC":
            return 8
        case "NEC2":
            return 9
        case "ONKYO":
            return 10
        case "PANASONIC":
            return 11
        case "KASEIKYO":
            return 12
        case "KASEIKYO_DENON":
            return 13
        case "KASEIKYO_SHARP":
            return 14
        case "KASEIKYO_JVC":
            return 15
        case "KASEIKYO_MITSUBISHI":
            return 16
        case "RC5":
            return 17
        case "RC6":
            return 18
        case "SAMSUNG":
            return 19
        case "SAMSUNGLG":
            return 20
        case "SAMSUNG48":
            return 21
        case "SHARP":
            return 22
        case "SONY":
            return 23
        case "BANG_OLUFSEN":
            return 24
        case "BOSEWAVE":
            return 25
        case "LEGO_PF":
            return 26
        case "MAGIQUEST":
            return 27
        case "WHYNTER":
            return 28
        case "FAST":
            return 29
        case _:
            return 0


def clear(string: str) -> str:
    string = string.decode('ascii')
    for i in ["firmware:", "version:", "protocols:"]:
        string = string.replace(i, '').replace('\n', '').replace('\r', '')
    return string

def width(string: str, string1: str = "")-> int:
    return len(string) + len(string1) + 4


class Controler:
    def __init__(self, port = ""):
        self.devices = []
        self.serialPort = self.Port(port) if port else self.Port()
        
    def Port(self, port = ""):
        a = 0
        if port:
            serialPort = serial.Serial(port=port, baudrate=115200, bytesize=8, timeout=0.5)
            self.devices.append(f"ir{a}")
            time.sleep(1.3)
            return serialPort

        ports = serial.tools.list_ports.comports(include_links=False) # auto found
        
        print("-d/--device not specified")
        print("searching automatic...")
        
        for port in ports:
            print(f"found: {port}")
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
    
    
    def SendPacket(self, protocol, address, command, repeats):
        # example: cmd:send protocol: 8 address: 61184 command: 2 repeats: 10 # 
        self.serialPort.readall()
        if "0x" in address or "0X" in address:
            print(f"\n{self.devices[0]}:\n\tprotocol: {protocol}\n\taddress:  {address}\n\tcommand:  {command}\n\trepeats:  {repeats}")
            self.serialPort.write(f"cmd:send protocol: {protocol_to_int(protocol)} address: {int(address, 16)} command: {int(command, 16)} repeats: {repeats}".encode("ascii"))
        else:
            print(f"\n{self.devices[0]}:\n\tprotocol: {protocol}\n\taddress:  0x{hex(int(address)).upper()[2:]}\n\tcommand:  0x{hex(int(command)).upper()[2:]}\n\trepeats:  {repeats}")
            self.serialPort.write(f"cmd:send protocol: {protocol_to_int(protocol)} address: {address} command: {command} repeats: {repeats}".encode("ascii"))
        b = 0
        while b < int(repeats)+10: 
            serialData = self.serialPort.readlines() # save to list 
            time.sleep(0.10)
            b += 1
            if serialData:
                break
        
        print(f"\n{self.devices[0]}: {clear(serialData[0])}")
    
parser = argparse.ArgumentParser(description="Decode type argument example")
parser.add_argument("-p", "--protocol", metavar="", type=str, default='0', required=True, help="Protocol (Name or Value, NEC/8 ...)")
parser.add_argument("-a", "--address", metavar="", type=str, default='0', required=True, help="Address: (HEX or Decimal, 0xEF00/61184 ...)")
parser.add_argument("-c", "--command", metavar="", type=str, default='0', required=True, help="Command: (HEX or Decimal, 0x2/2 ...)")
parser.add_argument("-r", "--repeats", metavar="", type=str, default='1', help="Repeats: (1-4294967295)")
parser.add_argument("-d", "--device", metavar="", type=str, default='', help="Port: (COM10, ttyUSB0, ...)")

args = parser.parse_args()


a = Controler(args.device)  
a.SendPacket(args.protocol, args.address, args.command, args.repeats)    