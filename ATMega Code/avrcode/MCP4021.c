// ------- Preamble -------- //
#include <avr/io.h>
#include <util/delay.h>
#include <avr/power.h>
#include "pinDefines.h"
#include "USART.h"
#include <util/delay.h>                     /* Functions to waste time */
#include "MCP4021.h"


void init_MCP4021(void){
	DPOTDDR |= ((1<<CS)|(1<<UD));
	resistanceDown(SPAN);
	_delay_ms(5);
	resistanceUp(SPAN/2);
	}
	

void resistanceUp(uint8_t incmnts){
	//Set direction up
	DPTPORT |= (1<<UD);	//set UD high to (increment up direction)
	DPTPORT &= ~(1<<CS); // set CS low while UD is hight send UP direction info
	for(uint8_t i = 0; i<incmnts; i++){
		DPTPORT &= ~(1<<UD); //set UD Low.  Falling edge does nothing
		DPTPORT |= (1<<UD); //set UD High. Rising edge increments
	}
	DPTPORT |= (1<<CS); // Set Chip select high while UD is high.  Avoid saving wiper location to MCP4021 Memory
}


void resistanceDown(uint8_t incmnts){
	//Set direction up
	DPTPORT &= ~(1<<UD); //set UD low to (increment down direction)
	DPTPORT &= ~(1<<CS); // set CS low while UD is low send down direction info
	for(uint8_t i = 0; i<incmnts; i++){
		DPTPORT &= ~(1<<UD); //set UD Low.  Falling edge does nothing
		DPTPORT |= (1<<UD); //set UD High. Rising edge increments
	}
	DPTPORT |= (1<<CS); // Set Chip select high while UD is high.  Avoid saving wiper location to MCP4021 Memory
}

void saveState(void){  // TODO; FIGURE OUT BETTER TIMING
	DPTPORT |= (1<<CS); // Set CS high just to make sure
	DPTPORT |= (1<<UD);	//set UD high to 
	_delay_ms(1);
	DPTPORT &= ~(1<<CS); // set CS low while UD is high
	_delay_ms(1);
	DPTPORT &= ~(1<<UD);	//set UD low
	_delay_ms(1);
	DPTPORT |= (1<<CS); // Set CS high to lock in write
	_delay_ms(10); 		// 10 ms is max EEPROM writing time in datasheet
}
	
	
void upDown(){
	const uint8_t delayTime = 10;
	resistanceDown(SPAN);
	for (uint8_t i=0; i <SPAN; i++){
		resistanceUp(1);
		_delay_ms(delayTime);
	}
	for (uint8_t i=0; i <SPAN; i++){
		resistanceDown(1);
		_delay_ms(delayTime);
	}
	resistanceUp(SPAN/2);
}
