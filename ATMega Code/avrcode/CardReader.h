#include <avr/io.h>
#include <string.h>
#include "buttons.h"
#include "MCP4021.h"
#include <avr/eeprom.h>
#include "CD4014.h"
#include "TPIC6B595N.h"

#define NUMIR 11


typedef struct{			// This structure is simply to allow passing wiper value array to functions.
	uint8_t wiperVals[11];
} thresh_Props;
	



typedef struct{			// This structure is simply to allow passing wiper value array to functions.
	uint16_t newRead;
	uint16_t oldRead;
	uint16_t newTime;
	uint16_t oldTime;
	uint16_t elapseTime;
	uint16_t cardNum;
	uint8_t readCount;
} card_Props;
	

ISR(INT0_vect);		//Pin change interrupt vector for the IR sensor 11.  This is to detect card being inserted.

void CardReader_Init(void);	 //sets up interupt 
// enables INT0 pin change interrupt
// enables interupt on change in pin status
// sets pull up resistor on pin change interupt

uint16_t Card_ReadStates(void); //reads current state of 11 IR sensors
// does a fair bit of bit manipulating to put IR sensors in a reasonable order.

void Card_IR(uint16_t);  // turns on IR light corresponding to bits of 16 bit integer passed to function
//DOES NOT PREVENT VIBRATION MOTORS FROM BEING TURNED ON!.


void Card_Next_Thresh(uint8_t j, thresh_Props inThresh); //sets digital potentiometer MCP4021 to threshold value for current IR sensor 
// array of threshold values are passed in to function
// THRESHOLD VALUES MUST BE CALLED IN ASCENDING ORDER, TO SAVE TIME FUNCTION ONLY SETS 0TH VALUE AND THEN CHANGES RESISTANCE UP OR DOWN BASED
// DIFFERENCE BETWEEN Jth AND J-1th VALUE.

uint16_t Card_Read(uint8_t raw, thresh_Props inThresh);
// reads cards by succesivley turning on a single IR LED and calling Card_ReadStates.  Each successive Card_read are OR'd together for final card reading.
// IR LEDs are turned on succesivley to allow so that individual threshold values can be used.  This can probably be sped up by turning multiple LEDS on at the same time 
//if they have the same threshold; however, current draw is as each IR sensor draws approx 40ma. 


card_Props Card_Debounce(card_Props inCard, thresh_Props inThresh);
// This function is called from the main loop when cardFlag is tripped.  Function is recieves, updates and returns card_Props structure from main loop.
//card_Props is updated with newReading, and new elapsed time after each sucessive read.  
//TODO PUT IN NEW VARIABLE SO THAT MAIN LOOP WILL KNOW WHEN A STABLE READING HAS BEEN TAKEN.  


//****************************AUTO-CALIBRATION******************************************************//
//Below are functions that allow the BELLA to calibrate the optimal threshold value for each IR sensor in the card reader. Optimal digital wiper positions are determined for each IR sensor
// by finidng the wiper positions where each ir sensor will read high for a white and black card.  The midpoint between these two values is the ideal threshold value.  
// This is done by succesively raising the wiper position and noting when an IR sensor first turns on in an array. Two arrays are taken, one for a all-white card and one for a all black card.
// The values are then averaged and the optimal thresh valuee is written into EEPROM as the threshold array

thresh_Props Card_Update_Wiper_Array(thresh_Props inThresh, uint8_t wiperPos, uint16_t cardVals); // updates wiper value array during auto Card reader autocalibration, part of determining optimal threshold value for each IR sensor
// called after each change in the digital resistor as resistor value is raised.  IR sensors that change from low to high have wiper value recorded in array.  

thresh_Props Card_Get_Bounds(void); // returns array of smallest wiper value at which sensor reads high for each IR sensor.  Used during Card autocalibration.

thresh_Props Card_Get_Thresh(thresh_Props inNew, thresh_Props inOld, thresh_Props outThresh);  \
//makes an array of midpoints values of two arrays of wiper values, inNew and inOld 
//writes array to EEPROM Memory

void Card_Print_Array(uint8_t cardArray[], uint8_t length); //Prints cardArray[].  For debugging. 
void Card_Read_Stored_Thresh(void); // prints threshold array stored in EEPROM