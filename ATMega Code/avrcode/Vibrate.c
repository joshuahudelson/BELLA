// ------- Preamble -------- //
#include "Vibrate.h"


 

void Vibrate_Keys(uint8_t inByte){
	TPIC_ShiftOut(0x00);  // set out blank byte to assure that we don't turn on any IR sensors
	TPIC_ShiftOut(inByte -192); // ignore the last two bits of inbyte.  Again we don't want to turn on any IR sensors
	TPIC_Pulse(); // pulse outputs
	}