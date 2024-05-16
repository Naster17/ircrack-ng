#ifndef IR_DRIVER
#define IR_DRIVER

#include <Arduino.h>
#include <IRremote.hpp>
#include "definitions.h"

IRData IrCustomData;
struct IrRawStruct
{
  uint8_t rawCode[RAW_BUFFER_LENGTH]; // The durations if raw
  uint8_t rawCodeLength;              // The length of the code
} IrRawData;

void beginInfo(Print *aSerial)
{
  aSerial->println(F("device: " DEVICE "\nfirmware: " FIRMWARE "\nversion: " DONGLE_VERSION));
  aSerial->print(F("protocols: "));
  printActiveIRProtocols(aSerial);
};

void beginReceiver()
{
  IrReceiver.begin(IR_RECEIVE_PIN, LED_FEEDBACK);
};

void beginSender()
{
  IrSender.begin(IR_SEND_PIN);
};

// Packets
void capturePacket(IRData *IrStructd, Print *aSerial)
{
  if (IrReceiver.decode())
  {
    if (IrReceiver.decodedIRData.protocol == UNKNOWN)
    {
      aSerial->println(F("Received noise or an unknown protocol"));
      aSerial->print(F("\nRaw: len: "));
      aSerial->print((int)IrReceiver.decodedIRData.rawDataPtr->rawlen - 1);
      aSerial->print(F(" packet: "));
      IrReceiver.compensateAndStoreIRResultInArray(IrRawData.rawCode);
      for (int i = 0; i < RAW_BUFFER_LENGTH; i++)
      {
        aSerial->print(IrRawData.rawCode[i]);
        aSerial->print(F(","));
      }
      aSerial->println();
      IrReceiver.resume();
    }
    else
    {
      IrReceiver.resume();
      IrReceiver.printIRResultShort(aSerial);
    }
    aSerial->println();
  }
};

void sendPacket(IRData *IrStructd)
{
  // customCode(&IrData, NEC, 0xEF00, 0x2);
  IrSender.write(IrStructd);
  printIRResultShort(&Serial, IrStructd, false);
};

void craftPacket(IRData *IrStructd, decode_type_t protocol, uint16_t address, uint16_t command)
{
  IrStructd->protocol = protocol;
  IrStructd->address = address;
  IrStructd->address = command;
};

void savePacket();

// Listners
void receiverListner(Print *aSerial)
{
  
  while (1)
  {
    capturePacket(&IrCustomData, aSerial);
    delay(100);
  }
};
// Attacks
void brutforce();
void database();

#endif