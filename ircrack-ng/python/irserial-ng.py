import serial
import time
import serial.tools.list_ports
from prettytable import PrettyTable 


serialPort = serial.Serial(
    port="COM10", baudrate=115200, bytesize=8, timeout=0.5
)

while 1:
    inp = input("> ")
    if inp == "exit": exit()
    
    serialPort.write(inp.encode("ascii"))

    while 1: 
        serialData = serialPort.readlines() # save to list 
        if serialData:
            break
        
    for data in serialData:
        print(data)
    
    
