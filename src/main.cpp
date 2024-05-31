#include "ir.h"
#include "interface.h"

void setup()
{
  
  beginReceiver();
  beginSender();
  beginSerial();
}

void loop()
{
  serial();
}