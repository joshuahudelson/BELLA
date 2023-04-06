// buttons.c is a module to handle buttons or the Braillecade Keyboard.  Button states are read by shifting in data from four 
//daisy-chained 8-bit shift registers (CB4014BE).


#include "buttons.h"


//----Global Variables---//
const uint16_t g_debounceTime = 50;
const uint16_t g_keyPressTime = 500;



void Button_InitTimer1(void){
	TCCR1B |= ((1<<CS12)|(1<<CS10)); // set up timer1 with prescaller of 1024.  one period = 1.024 ms
	printString("timer 1 initialized \r\n");
	}


button_Props Button_Debounce(button_Props B_Data){
	uint16_t time = TCNT1;	//get time from 16 bit clock
	long long buttMask = 1;	//initiate button mask to one.  button mask is used to look at each key and button individualy in loop below
	long long currButtStates = CD4014_ReadStates();	// shift in 40 key values from CD4014BE
	long long CSMask =1;
	//currButtStates &= ~(CSMask<<7);  //ignore CS11 card sensor keep it from blocking updated reads when card is inserted. CS11 is the 7th place in curr butt states see better explanation CardReader.c comments
	if(currButtStates == 0){	// if all keys are released reset everything		
		B_Data.chordF = 0;		// clear chord data
		B_Data.holdF = 0;		// clear hold flag, start paying attention to button presses
		B_Data.buttPressed = 0;	// clear memory of what buttons were pressed. 
	}
	for(uint8_t i = 0; i<SENSENUM; i++){
		if((currButtStates & (buttMask)) == 0){
			B_Data.buttTimes[i] = time;		// continually update time of buttons that have not been pressed
		}
		if((time - B_Data.buttTimes[i] ) >= g_debounceTime){
			B_Data.buttPressed |= buttMask;	// buttons with time> debounce time are marked as pressed 
		}
		if((time - B_Data.buttTimes[i] )>= g_keyPressTime){
			B_Data.chordF = 1;	// any button with time > chord time marks that a chord has been pressed.  
		}
		buttMask = (buttMask<< 1);
	}	
	if((B_Data.chordF == 1) && (B_Data.holdF == 0)){
		//printLongNumber(B_Data.buttPressed);
		//printString("\r\n");
		B_Data.keyChord = B_Data.buttPressed;  // all debounced buttons are included in chord
		B_Data.holdF = 1;	//keeps program from coming back and updating the chord until all keys are relaased. 
	}
	return(B_Data);
}


