#include <avr/io.h>
#include <util/delay.h>
#include "pinDefines.h"
#include "USART.h"


#ifndef TPICRATE_H
#define TPICrate_H


#define PULSE 100 //pulse time interval in miliseconds
#define	TPICDDR	DDRC
#define TPICPORT PORTC
#define TPICENABLE PC2  //Enables output of TPIC6B595 (sink output) of data in output register
#define TPICSERCLK PC3  // Serial clock of TPIC6B595
#define TPICREGCLK PC4  // Latch pin, moves data from serial register to ouput register
#define TPICSERIN PC5 	// data feed into serial register

void TPIC_Init(void);
	//Sets pins for TPIC.
	//Sets TPICENABLE pin hight to disable output

void TPIC_ShiftOut(uint8_t inByte);
	//Shifts out byte of to TPIC shift registers
	//Does not latch data into output registers (data in shift registers not visible to output registers).

void TPIC_Latch(void);
	// latches data into output registers

void TPIC_Activate(void);
	//Latches data into output registers (TPIC_Latch) then enable outputs.  

void TPIC_Deactivate(void);
	//Disable outputs

void TPIC_Pulse(void);
	//Latches data into output registers (TPIC_Latch), 
	//enables outputs(TPIC_ACTIVATE)
	//waits for PULSE interval
	//Disables outputs (TPIC_Deactivate
#endif
