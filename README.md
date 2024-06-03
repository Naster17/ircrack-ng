# ircrack-ng

![11](https://github.com/Naster17/ircrack-ng/assets/62520991/7d0313cb-9eb1-4b3e-9d7d-608136b41cf8)

## Binaries (python, C++)
- ```irmon-ng``` - Search for available connected devices. Checking the firmware version and other useful information about devices
- ```irdump-ng``` - IR signal interception/sniffing mode. Displaying all the necessary information about the intercepted signal
- ```irplay-ng``` - Sending signals. With support for hexadecimal and decimal. See more below
- ```irserial-ng``` - Direct connection via serial port. Useful for debugging and understanding how the device works
- ```irdatabase-ng``` - Using pre-ready IR signals via database
- ```irbrutforce-ng``` - Soon!
- ```irmemory-ng``` - Soon! Reading stored signals in the device memory. Thanks to the no-serial mode
- ```irdos-ng``` - Soon! Simple DoS script. Wait firmware updated for more speed.

## Exaple commands
- ```python irplay-ng.py -a 0xEF00 -c 0x3 -p NEC -d COM10```

## Build Instruction

