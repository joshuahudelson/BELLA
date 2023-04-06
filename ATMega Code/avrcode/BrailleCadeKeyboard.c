// ------- Preamble -------- //
#include <avr/io.h>
#include <util/delay.h>
#include <avr/power.h>
#include <avr/interrupt.h>
#include <string.h>
#include "pinDefines.h"
#include "USART.h"
#include "buttons.h"
#include "Vibrate.h"
#include "MCP4021.h"
#include "CD4014.h" 
#include "CardReader.h"


#define CARD_SENSOR PD3

//----Global Variables---//
uint8_t cardFlag = 0;  // flag is triped by extenal pin PD2 interrupt when IR sensor 11 is tripped



void printKeyVals(long long longNum){
	//Prints 40 key values from bella
	for(uint8_t i = 1;i<5;i++){			//loop over shift each byte of shift register data
		transmitByte(((longNum>>(i*8)) & 0xff));	//transmit byte out
	}
}
	

int main(void) {


  // -------- Inits --------- // 
	clock_prescale_set(clock_div_1);                            /* 8 MHz */
	initUSART();        
	init_MCP4021(); 	// MCP4021 is digital potentiometer IC, used as to set comparator thresholds for IR sensors
	Button_InitTimer1(); // Init timer used to debounce button presses and keys
	CD4014_init();		// init pins (output and input) used for input shift bit registers (buttons and IR sensors)
	TPIC_Init();		// init pins (output and input) used for output shift bit registers (vibrating keys and IR Leds)
//	CardReader_Init();  // sets pin change interrupt used in card reader. 
	

	
	//printString("starting delay\r\n");
	_delay_ms(100);
	//printString("done with delay \r\n");
	
	//PORTD |= (1<<CARD_SENSOR);
	
	//uint8_t data = 0;
	uint8_t RXByte = 0;
	//uint8_t cardCodeStat = 0;
	uint8_t cardCodeReady = 0;
	uint8_t calFlag = 0;
	//uint16_t oldCard =0;
	//uint16_t newCard = 0;
	//uint16_t oldTime =0;
	//uint16_t newTime =0;
	//uint16_t elapseTime = 0;
	card_Props Card;
	printString("hey ya'll \r\n");
	button_Props B_Stuff;
	thresh_Props ramThresh = {{32,33,31,26,41,32,32,31,30,32,32}};
	thresh_Props oldThresh;
	thresh_Props newThresh;
	
	
  // ------ Event loop ------ //
  while (1) {  
	if(cardCodeReady == 0){					// if no card code is ready to report
		B_Stuff = Button_Debounce(B_Stuff);  			 // check on key presses
	}
	
//	if(cardFlag != 0){						// if card is not present
//		Card = Card_Debounce(Card,ramThresh);	//get card information
//		//printString("card sensed \r\n");
//		if(cardFlag == 0){						//cardFlag is set to zero when a card is debounced
//			printString("got barcode");
//			if(Card.cardNum != 0){
//			B_Stuff.keyChord = 0xffffffffff;		//setting B_stuff to all ones lets the computer know a card has been debounced.  It can then read the card number whenever it wants.
//			printWord(Card.cardNum);
//			}
//			else{
//				printString("got nothing");
//				}
//		}
//	}
	
	if((UCSR0A & (1 << RXC0)) != 0)
		RXByte = UDR0;
	
	switch(RXByte){
		case 'i':	printString("BrailleCade");
					RXByte = 0;
					break;
		case 'b':	printKeyVals(B_Stuff.keyChord);
					//printString("\r\n");
					RXByte = 0;
					B_Stuff.keyChord = 0x00000000;
					cardCodeReady = 0;
					break;
		case 'v':	Vibrate_Keys(getNumber());
					RXByte = 0;
					break;
		case 'c':	printWord(Card.cardNum);
					RXByte = 0;
					break;
		case 'r':	cli();
					printWord(Card_Read(0, ramThresh));
					printString("\r\n");
					RXByte = 0;
					EIFR = (1<<INTF0); //reading the card will trip card sensor so we must clear interrupt flag by writting 1 to EIFR Register.
					sei();
					break;
		case 'o':	switch(calFlag){
						case 0:		printString("Calibrate Card Sensor \r\n Insert white card and press 'o' \r\n");
									calFlag++;
									break;
						case 1:		newThresh = Card_Get_Bounds();
									memcpy(oldThresh.wiperVals, newThresh.wiperVals, sizeof(newThresh.wiperVals));
									printString("lower bounds: \r\n");
									Card_Print_Array(newThresh.wiperVals, sizeof(newThresh.wiperVals));
									printString("Insert black card and press 'o' \r\n");
									calFlag++;
									break;
						case 2:		newThresh = Card_Get_Bounds();
									printString("upper bounds: \r\n");
									Card_Print_Array(newThresh.wiperVals, sizeof(newThresh.wiperVals));
									ramThresh = Card_Get_Thresh(newThresh, oldThresh, ramThresh);
									printString("threshold:\r\n"); 
									Card_Print_Array(ramThresh.wiperVals, sizeof(ramThresh.wiperVals));
									calFlag = 0;
									break;
					}				
					RXByte = 0;
					break;
					
		case 't':	Card_IR((uint16_t)65472);
					printWord(Card_ReadStates());
					RXByte = 0;
					break;
		case 'p':	Card_Read_Stored_Thresh();
					RXByte = 0;
					break;
	}
	
	}
	

  return (0);                           
}
 
	
