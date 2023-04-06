
#include "CardReader.h"

//----Global Variables---//
//const uint8_t g_numIRSense = 11;
uint8_t g_eepromWiperVal[11] EEMEM = {32,32,32,32,32,32,32,32,32,32,32};  // TODO change to EEPROM_Threshold_Array to match comments.
extern uint8_t cardFlag;


ISR(INT0_vect){
//for the card reader
	cardFlag = 1;
	}

void CardReader_Init(void){
	EIMSK |= (1<<INT0);  /* enable INT0 */
	EICRA |= (1<<ISC00);  /* Trigger on any change */
	CARDPORT |= (1<<CARDSENSE); // pull up on card sensor
	EIFR = (1<<INTF0); //clear interrupt flag so that we don't trip interrupt just because we turned on the sensor.
	sei(); //enable interrupts
}




uint16_t Card_ReadStates(void){
uint16_t cardStates = 0;
long long sensor_states = CD4014_ReadStates();  // take in all of the button states from the shift bit registers
cardStates = (sensor_states & 0x7ff);  // reduce huge number to last 11 bits we care about.
return(cardStates);
}


 void Card_IR(uint16_t inWord){
	uint8_t sendByte1 = inWord & 0xFF;
	uint8_t sendByte2 = inWord>>8;
	TPIC_ShiftOut(sendByte2); 
	TPIC_ShiftOut(sendByte1);
	TPIC_Activate();
}

 
 void Card_Next_Thresh(uint8_t j, thresh_Props inThresh){
	uint8_t curr_thresh = 0;
	if(j == 0){
	resistanceDown(SPAN); //lower resistance all the way down.
	_delay_ms(5);
	resistanceUp(inThresh.wiperVals[j]); // raise resistance to first thresh value
	//printByte(curr_thresh);
	}
	else{
		if(inThresh.wiperVals[j] > inThresh.wiperVals[(j-1)]){
			resistanceUp((inThresh.wiperVals[j] - inThresh.wiperVals[(j-1)]));
			//printString("UP \r\n");
		}
		else if(inThresh.wiperVals[j] < inThresh.wiperVals[(j-1)]){
			resistanceDown((inThresh.wiperVals[(j-1)] - inThresh.wiperVals[j]));
			//printString("DOWN \r\n");
		}
		else{
			//printString("SAME \r\n");
		}
	}
}


uint16_t Card_Read(uint8_t raw, thresh_Props inThresh){
	uint16_t cardRead = 0;
	uint16_t newRead = 0;
	uint8_t sensor_ix = 1;
	for(uint8_t i = 6; i<16; i++){
		if(raw == 1){
		}
		else{
		Card_Next_Thresh(i-6, inThresh);
		}
		Card_IR(sensor_ix<<i);
		_delay_ms(1);
		newRead = Card_ReadStates();
		//vibPort |= (1<<vibEnable); //Enable low TURN OFF LIGHT!
		cardRead |= newRead;
	}
	//cardRead >>=1;
return(cardRead);
}


card_Props Card_Debounce(card_Props inCard, thresh_Props inThresh){
	inCard.newRead = Card_Read(0, inThresh);			//read card sensors store data in newRead
	//printWord(inCard.newRead);
	//printString("\r\n");
	inCard.newTime = TCNT1;								//get time of reading for debouncing
	if((inCard.readCount != 0) && (inCard.newRead == inCard.oldRead)){  //if card read count is not zero and previous reading is the same as current reading
		inCard.elapseTime += (inCard.newTime-inCard.oldTime);	// calculate elapsed time since initial reading of same value
		//printWord(inCard.elapseTime);
		//printString("\r\n");
		if(inCard.elapseTime> 1000){							// if elapsed time since initial reading of same value > 1000 
			printString("card debounced\r\n");
			inCard.readCount = 0;								// reset card reading flag doing so tells main loop a card has been debounced.  Also stops card reading each cycle
			inCard.cardNum = inCard.newRead;					// set card.Num 
			cardFlag = 0;
		}
	}
	else{
	inCard.readCount++;
	inCard.oldRead = inCard.newRead;
	inCard.oldTime = inCard.newTime;
	inCard.elapseTime = 0;
	//printWord(inCard.elapseTime);
	//printString("\r\n");
	}
	return(inCard);

}


thresh_Props Card_Update_Wiper_Array(thresh_Props inThresh, uint8_t wiperPos, uint16_t cardVals){
	for(uint8_t i=0; i<NUMIR; i++){
		//printString("CS ");
		//printByte(i);
		if((cardVals & (1<<i))== 0){
			if(inThresh.wiperVals[i] == 0){
				inThresh.wiperVals[i] = wiperPos;
				//printString(" wiper val set to");
				//printByte(wiperPos);
			}
			else{
				//printString(" wiper val =");
				//printByte(newThresh.wiper[i]);
			}
		}
		else{
			//printString(" not set");
		}
		//printString("\r\n");
	}
	//printString("\r\n");
return(inThresh);
}


//TODO putt currWiperVal in program memory, put error checking in the Card_Get_Thresh

thresh_Props Card_Get_Bounds(void){
	thresh_Props tempThresh;
	memset(tempThresh.wiperVals,0,sizeof(tempThresh.wiperVals));
	resistanceDown(SPAN); 
	_delay_ms(5);		// let MCP4021 chatch up
	uint8_t wiperVal = 0;
	uint16_t cardVal =  Card_Read(1, tempThresh);
	printWord(cardVal);
	printString("\r\n");
	while((cardVal !=00)&& (wiperVal < SPAN)){  //while any sensors are on
		resistanceUp(1);	// raise threshold voltage with digital pot
		wiperVal++;			// increment pot wiper value
		cardVal =  Card_Read(1,tempThresh);	// read card
		tempThresh = Card_Update_Wiper_Array(tempThresh, wiperVal, cardVal);  // update any new values in wiper array. 
    }
	return(tempThresh);
}
		
	
thresh_Props Card_Get_Thresh(thresh_Props inNew, thresh_Props inOld, thresh_Props outThresh){
	for(uint8_t i=0; i<NUMIR; i++){
		outThresh.wiperVals[i] = ((inOld.wiperVals[i]-inNew.wiperVals[i])+1)/2;
	}
	eeprom_update_block(outThresh.wiperVals, g_eepromWiperVal, NUMIR);
	return(outThresh);
}
	
void Card_Print_Array(uint8_t cardArray[], uint8_t length){
	for(uint8_t i=0; i<length; i++){
		printString("CS ");
		printByte(i);
		printString(" = ");
		printByte(cardArray[i]);
		printString("\r\n");
	}
}

void Card_Read_Stored_Thresh(void){
	uint8_t newArray[NUMIR];
	eeprom_read_block(newArray, g_eepromWiperVal, NUMIR);
	printString("Stored Threshold Values:\r\n");
	Card_Print_Array(newArray, sizeof(newArray));
}
