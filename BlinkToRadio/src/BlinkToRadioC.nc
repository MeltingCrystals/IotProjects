 #include <Timer.h>
 #include "BlinkToRadio.h"
 #include "printf.h"
 
 module BlinkToRadioC @safe() 
 {
 uses interface Boot;
 uses interface Leds;
 uses interface Timer<TMilli> as Timer0;
 
 uses interface Packet;
 uses interface AMPacket;
 uses interface AMSend;
 uses interface SplitControl as AMControl; 
 
 uses interface Receive; 
 }
	 implementation {
	 uint16_t counter = 0;
	 bool busy = FALSE;
	 uint16_t messageid = 420;
	 message_t pkt;
	 
	 event void Boot.booted() {
	 call AMControl.start();
	 call Timer0.startPeriodic(TIMER_PERIOD_MILLI);
	 }
	
	 event void Timer0.fired() {
	 counter++;
	 if (!busy) {
	 	BlinkToRadioMsg* btrpkt = (BlinkToRadioMsg*)(call Packet.getPayload(&pkt, sizeof
			(BlinkToRadioMsg)));
	 	btrpkt->nodeid = TOS_NODE_ID;
	 	btrpkt->counter = counter;
	 	btrpkt->messageid = messageid;
	 	
	 	if (call AMSend.send(AM_BROADCAST_ADDR, &pkt, sizeof(BlinkToRadioMsg)) == SUCCESS) {
	 		busy = TRUE;
	
	 	} 
	  }
	 }
	
	
	 event void AMControl.stopDone(error_t error){
		// TODO Auto-generated method stub
	 }
	
	 event void AMControl.startDone(error_t error){
		// TODO Auto-generated method stub
		if (error == SUCCESS) {
			call Timer0.startPeriodic(TIMER_PERIOD_MILLI);
		}
		else {
			call AMControl.start();
		} 
	 }
	
	 event void AMSend.sendDone(message_t *msg, error_t error){
	 	printf("Counter: %u\n", counter);
	 	printfflush();
	 	// TODO Auto-generated method stub
	 	if (&pkt == msg) {
	 		busy = FALSE;
	 	}
	 }
	
	 event message_t * Receive.receive(message_t *msg, void *payload, uint8_t len){
	 // TODO Auto-generated method stub
		if (len == sizeof(BlinkToRadioMsg)) {
	  		BlinkToRadioMsg* btrpkt = (BlinkToRadioMsg*)payload;
	 		if (btrpkt->messageid == messageid) {
	 			call Leds.set(btrpkt->counter);
	 		}
	 	}
	 return msg;
	 }
}