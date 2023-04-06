
#include "CD4014.h"

void CD4014_init(void){
	SHFTREGDDR |= ((1<<SHFTREGCLK)|(1<<SHFTREGCTRL))|(1<<PD4); 
	SHFTREGPORT |= (1<<SHFTREGSER);
	printString("CD4014 Initialized \r\n");
	}

long long CD4014_ReadStates(void){
	long long buttStates = 0;
	SHFTREGPORT |= (1<<SHFTREGCTRL);  // SHFTREGCTRL line HIGH to get parrallel inputs
	SHFTREGPORT &= ~(1<<SHFTREGCLK);  //clock low
	SHFTREGPORT |= (1<<SHFTREGCLK);		//clock high
	SHFTREGPORT &= ~(1<<SHFTREGCLK);	// clock low
	SHFTREGPORT &= ~(1<<SHFTREGCTRL); // turn off control
	for(uint8_t i = 0; i<SENSENUM;i++){ //Shift in data from registers
		buttStates = buttStates << 1; //shift left
		SHFTREGPORT |= (1<<SHFTREGCLK);		//clock high
		if ((PIND & (1<<SHFTREGSER)) == 0){  //check if CD4014 pin was pulled low (key pressed)
		 buttStates++;  	// if so record button on
		 }
		SHFTREGPORT &= ~(1<<SHFTREGCLK); // clock low, prepare for next bit
		}
	return(buttStates);
}