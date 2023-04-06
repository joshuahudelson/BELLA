#include <avr/io.h>
#include <util/delay.h>
#include <avr/power.h>
#include "pinDefines.h"
#include "USART.h"
#include <util/delay.h>                     /* Functions to waste time */


#ifndef MCP4021
#define DPTPORT PORTD
#define DPOTDDR DDRD
#define CS PD4
#define UD PD3
#define SPAN 64
#endif

void init_MCP4021(void);

void resistanceUp(uint8_t incmnts);

void resistanceDown(uint8_t incmnts);

void saveState(void);

void upDown(void);