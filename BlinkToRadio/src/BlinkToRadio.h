 #ifndef BLINKTORADIO_H
 #define BLINKTORADIO_H
 
 enum {
 AM_BLINKTORADIO = 6,
 TIMER_PERIOD_MILLI = 250
}; 

 typedef nx_struct BlinkToRadioMsg {
 nx_uint16_t nodeid;
 nx_uint16_t counter;
 nx_uint16_t messageid;
} BlinkToRadioMsg;

#endif