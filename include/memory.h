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

void read_from_memory(Print *aSerial)
{
    IRDataSave obj;
    EEPROM.get(Address, obj);

    aSerial->print("EEPROM:");
    aSerial->print(obj.protocol);
    aSerial->print(obj.address);
    aSerial->print(obj.command);
    aSerial->println();
};

void clear_memory()
{
    for (uint16_t i = 0; i < EEPROM.length(); i++)
    {
        EEPROM.write(i, 0);
    }
};

#endif