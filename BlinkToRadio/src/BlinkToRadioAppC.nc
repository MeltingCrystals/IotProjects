#include <Timer.h>
#include "BlinkToRadio.h"
#define NEW_PRINTF_SEMANTICS
#include "printf.h"
 configuration BlinkToRadioAppC {
 }
 implementation {
 components MainC, LedsC, BlinkToRadioC;
 components PrintfC;
 components SerialStartC;
 components new TimerMilliC() as Timer0;
 components ActiveMessageC;
 components new AMReceiverC(AM_BLINKTORADIO);
 components new AMSenderC(AM_BLINKTORADIO);

 BlinkToRadioC.Boot -> MainC;
 BlinkToRadioC.Leds -> LedsC;
 BlinkToRadioC.Timer0 -> Timer0;
 
 BlinkToRadioC.Packet -> AMSenderC;
 BlinkToRadioC.AMPacket -> AMSenderC;
 BlinkToRadioC.AMSend -> AMSenderC;
 BlinkToRadioC.AMControl -> ActiveMessageC;
 
 BlinkToRadioC.Receive -> AMReceiverC; 
 } 