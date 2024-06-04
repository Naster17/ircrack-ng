#if defined(__AVR__)

// Firmware
#define DONGLE_VERSION "1.1"
#define FIRMWARE "NasterFirmware"
#define DEVICE "IR Dongle"
// Pins
#define IR_RECEIVE_PIN      3
#define IR_SEND_PIN         5
// Etc
#define LED_FEEDBACK false
#endif

#if !defined (FLASHEND)
#define FLASHEND 0xFFFF // Dummy value for platforms where FLASHEND is not defined
#endif

#if !defined(STR_HELPER)
#define STR_HELPER(x) #x
#define STR(x) STR_HELPER(x)
#endif

