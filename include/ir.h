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

template <typename T>
T getValue(String input, const char *find_from)
{
  int protocolIndex = input.indexOf(find_from);

  int startIndex = protocolIndex + strlen(find_from);
  int endIndex = input.indexOf(' ', startIndex);

  String value = input.substring(startIndex, endIndex);

  return static_cast<T>(value.toInt());
}

void sendPacket(String input)
{
  // cmd:send protocol: 8 address: 61184 command: 2
  // uint16_t protocol = NEC;
  // uint16_t address = 0xEF00;
  // uint16_t command = 0x2;
  IrSender.write(getValue<decode_type_t>(input, "protocol: "), getValue<uint16_t>(input, "address: "), getValue<uint16_t>(input, "command: "));
  delay(50);
};

void savePacket();

// Listners
void receiverListner(Print *aSerial)
{

  while (1)
  {
    capturePacket(&IrCustomData, aSerial);
    delay(50);
  }
};
// Attacks
void brutforce();
void database();

#endif