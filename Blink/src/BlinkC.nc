#include "Timer.h"
#include "printf.h"
module BlinkC @safe()
{
  uses interface Timer<TMilli> as Timer0;
  uses interface Timer<TMilli> as Timer1;
  uses interface Timer<TMilli> as Timer2;
  
  uses interface Leds;
  uses interface Boot;
}
implementation
{
  event void Boot.booted()
  {
    call Timer0.startPeriodic( 250 );
    call Timer1.startPeriodic( 500 );
    call Timer2.startPeriodic( 1000 );
  }

  event void Timer0.fired()
  {
    printf("Timer 0: %lu.\n", call Timer0.getNow());
    printfflush();
    call Leds.led0Toggle();
  }
  
  event void Timer1.fired()
  {
    printf("Timer 1: %lu.\n", call Timer1.getNow());
    printfflush();
    call Leds.led1Toggle();
  }
  
  event void Timer2.fired()
  {
    printf("Timer 2: %lu.\n", call Timer2.getNow());
    printfflush();
    call Leds.led2Toggle();
  }

}
