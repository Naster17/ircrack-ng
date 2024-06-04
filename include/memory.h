#ifndef MEMORY_H
#define MEMORY_H

#include <Arduino.h>
#include <EEPROM.h>
#include <IRremote.hpp>

static int Address = 0;

struct IRDataSave
{
    decode_type_t protocol;
    uint16_t address;
    uint16_t command;
};

void info_memory(Print *aSerial)
{
    aSerial->print("EEPROM length: ");
    aSerial->println(EEPROM.length());
};

void save_to_memory(decode_type_t protocol, uint16_t address, uint16_t command)
{
    IRDataSave obj;
    obj.protocol = protocol;
    obj.address = address;
    obj.command = command;

    EEPROM.put(address, obj);
    Address = Address + 6;
};

// void readPacket(int addr)
// {
//   int eeAddress = addr;
//   IRData obj2;

//   EEPROM.get(eeAddress, obj2);

//   Serial.println("Read custom object from EEPROM: ");
//   Serial.println(obj2.protocol);
//   Serial.println(obj2.address);
//   Serial.println(obj2.command);
// }

void read_from_memory() {

};

void clear_memory()
{
    for (uint16_t i = 0; i < EEPROM.length(); i++)
    {
        EEPROM.write(i, 0);
    }
};

#endif