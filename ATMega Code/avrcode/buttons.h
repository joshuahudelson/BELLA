#include <avr/io.h>
#include <util/delay.h>
#include <avr/power.h>
#include <avr/interrupt.h>
#include <string.h>
#include "pinDefines.h"
#include "USART.h"
#include "MCP4021.h"
#include <avr/eeprom.h>
#include "CD4014.h"


#ifndef BUTTONS_H
#define	BUTTONS_H
#define BTNDDR DDRD
#define BTNPORT PORTD
#define CARDPORT PORTD
#define BTNSER PD5
#define BTNCLK PD6
#define BTNCTRL PD7   
#define CARDSENSE PD2
#define KEYNUM 29

typedef struct{				// structure is used to hold data about button presses
	uint16_t buttTimes[40];	// timing of last time button was unpressed 
	long long buttPressed;	//64 bit number representing buttons that have been debounced
	uint8_t chordF;			// chord flag, used to mark when key has been held long enough to be a chord
	uint8_t holdF;			// hold flag, used to mark a chord has already been pressed.  Button state changes ignored until all buttons are realased.  TO DO: SEE IF THIS MIGHT BLOCK CARD READER.
	long long keyChord;  // variable which houses last chord from debounced buttons
} button_Props;

void Button_InitTimer1(void);	// initiates 16 bit timer to debounce keys and to determine when a chord is pressed	

button_Props Button_Debounce(button_Props);		//function debounces keys and button presses and determines when chord is pressed by user.  

#endif