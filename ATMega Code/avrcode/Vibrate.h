// ------- Preamble -------- //
#include <avr/io.h>
#include <util/delay.h>
#include "pinDefines.h"
#include "USART.h"
#include "TPIC6B595N.h"


void Vibrate_Keys(uint8_t);
// Vibrates keys 1-6 corresponding to bit value 1-6 of number
// ignores all other bit values in number
// pulses vibration motor for time "PUSE" set in TPIC6b595.h 
	
