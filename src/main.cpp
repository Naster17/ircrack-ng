#include "ir.h"
#include "interface.h"

void setup()
{
  beginReceiver();
  beginSerial();
}

void loop()
{
  serial();
}