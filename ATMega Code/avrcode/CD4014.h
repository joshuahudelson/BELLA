#include <avr/io.h>
#include <util/delay.h>
#include <avr/power.h>
#include <avr/interrupt.h>
#include "pinDefines.h"
#include "USART.h"




#ifndef SHFTREG_H
#define	SHFTREG_H
#define SHFTREGDDR DDRD
#define SHFTREGPORT PORTD
#define SHFTREGSER PD5
#define SHFTREGCLK PD6
#define SHFTREGCTRL PD7 
#define SENSENUM 40



void CD4014_init(void);
//Sets outputs in DDR
//Sets serial input pin

long long CD4014_ReadStates(void);
//Reads in shift register
//latches (stores) parrallel inputs into shift register
//shifts in and stores data in 64 bit number
#endif