#ifndef INTERFACE_H
#define INTERFACE_H

#include <Arduino.h>
#include "ir.h"
#include "memory.h"


bool stringContains(const char *str, const char *substring)
{
    size_t strLen = strlen(str);
    size_t substringLen = strlen(substring);

    if (substringLen > strLen)
        return false;

    for (size_t i = 0; i < strLen; i++)
    {
        if (strncmp(str + i, substring, substringLen) == 0)
            return true;
    }

    return false;
}

void beginSerial()
{
    Serial.begin(115200);
    // beginInfo(&Serial);
};

void serial()
{

    if (Serial.available())
    {
        String input = Serial.readString();

        if (stringContains(input.c_str(), "cmd:info"))
        {
            beginInfo(&Serial);
        }
        if (stringContains(input.c_str(), "cmd:wewe"))
        {
            Serial.println("wewe boy");
        }
        if (stringContains(input.c_str(), "cmd:start_listner"))
        {
            receiverListner(&Serial, true);
        }
        if (stringContains(input.c_str(), "cmd:send"))
        {
            sendPacket(input, &Serial);
        }
    }
    else
    {
        receiverListner(&Serial, false);
    }
};

#endif