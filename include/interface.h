#ifndef INTERFACE_H
#define INTERFACE_H

#include <Arduino.h>
#include "ir.h"

void beginSerial()
{
    Serial.begin(115200);
    beginInfo(&Serial);
};

void serial()
{
    if (Serial.available())
    {
        String input = Serial.readString();
        if (input == "info")
        {
            beginInfo(&Serial);
        }
        if (input == "startListner") {
            receiverListner(&Serial);
        }
    }
};

#endif