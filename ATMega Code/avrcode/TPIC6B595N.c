#include "TPIC6B595N.h"



void TPIC_Init(void){
	TPICDDR |= ((1<<TPICENABLE)|(1<<TPICSERCLK)|(1<<TPICREGCLK)|(1<<TPICSERIN)); //set output pins
	TPICPORT |= (1<<TPICENABLE); //Enable low NO SHAKING!
	printString("TPIC initialized \r\n");
}

void TPIC_ShiftOut(uint8_t inByte){
	TPICPORT &= ~(1<<TPICSERCLK); // serial clck low
	for(uint8_t i= 0; i<8; i++){
		if(inByte & 0b10000000){
			TPICPORT |= (1<<TPICSERIN);  // serial input high
		}
		else{
			TPICPORT &= ~(1<<TPICSERIN);
		}
		TPICPORT |= (1<<TPICSERCLK); // serial clock high
		_delay_ms(1);
		TPICPORT &= ~(1<<TPICSERCLK); // serial clck low
		_delay_ms(1);
		inByte = inByte<<1;//shift inbyte over and repeat
	}
}

void TPIC_Latch(void){
	TPICPORT |=(1<<TPICREGCLK); //register clock high
	_delay_ms(1);	
	TPICPORT &= ~(1<<TPICREGCLK);	// register clock low
}

void TPIC_Activate(void){
	TPIC_Latch();				// latch data from shift register into ouput register
	TPICPORT &= ~(1<<TPICENABLE); //Enable low 
}

void TPIC_Deactivate(void){
	TPICPORT |= (1<<TPICENABLE); //Enable low STOP ALL THAT SHAKING!
}

void TPIC_Pulse(void){
	TPIC_Latch(); // latch data from shift register into ouput register
	TPIC_Activate(); //enable output	
	_delay_ms(PULSE); // do nothing
	TPIC_Deactivate(); // deactivate
}