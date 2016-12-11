import time
import serial
import serial.tools.list_ports
import struct

class keyboard:
    """
    self.ser:

    self.com_port:
    
    self.last_button_state:
    
    self.card_str:
    
    
    
    


    """
    def __init__(self):
    
        self.card_str = '                    '
        
        self.alphabet = {
                '000001': 'a',
                '000011': 'b',
                '001001': 'c',
                '011001': 'd',
                '010001': 'e',
                '001011': 'f',
                '011011': 'g',
                '010011': 'h',
                '001010': 'i',
                '011010': 'j',
                '000101': 'k',
                '000111': 'l', 
                '001101': 'm',
                '011101': 'n',
                '010101': 'o',
                '001111': 'p',
                '011111': 'q',
                '010111': 'r',
                '001110': 's',
                '011110': 't',
                '100101': 'u',
                '100111': 'v',
                '111010': 'w',
                '101101': 'x',
                '111101': 'y',
                '110101': 'z',
                '000000': None,
                }

    #previous dictionary mapped keys visually but key one is in the LSB position
        self.letter_to_chord = {
                'a':'000001',
                'b':'000011', 
                'c':'001001',
                'd':'011001',
                'e':'010001',
                'f':'001011',
                'g':'011011',
                'h':'010011',
                'i':'001010',
                'j':'011010',
                'k':'000101',
                'l':'000111',
                'm':'001101',
                'n':'011101',
                'o':'010101',
                'p':'001111',
                'q':'011111',
                'r':'010111',
                's':'001110',
                't':'011110',
                'u':'100101',
                'v':'100111',
                'w':'111010',
                'x':'101101',
                'y':'111101',
                'z':'110101',
                'space':'000000',
                }

    
    def list_coms(self):
        """creates list of com ports available in os used by test_coms
        to locate brailleCade keyboard"""
        coms = list(serial.tools.list_ports.comports())
        #print(coms)
        COMList = []
        # return the port if 'USB' is in the description 
        for port_no, description, address in coms:
            COMList.append(port_no)
        return COMList

    def test_coms(self):
        coms = self.list_coms()
        if len(coms) > 0:
            for i in coms:
                print("testing {}".format(i)) 
                self.ser = serial.Serial(i,baudrate=9600,timeout=0)
                time.sleep(.5)
                self.ser.write(b"i")
                time.sleep(.5)
                out = ''
                while self.ser.inWaiting() > 0:
                    out += self.ser.read(1).decode('utf-8')
                if out != '':
                    print(">>{}".format(out))
                if out == 'BrailleCade':
                    print('Braillecade Found')
                    self.com_port = i
                    break
                self.ser.close
                print("Braillecade not found")

    def request_buttons(self):
        self.ser.write(b'b')
        # let's wait one second before reading output (let's give device time to answer)
        time.sleep(.1)
        if self.ser.inWaiting() > 0:
            self.last_button_state = format(int.from_bytes(self.ser.readline(),'little'),'032b')
            self.last_chord = self.last_button_state[2:8]
            print("button state = {}".format(self.last_button_state))
            self.last_letter = self.alphabet.get(self.last_chord,'X')
            if self.last_button_state[8] == '1':
                self.last_letter = 'space'
            try:
                self.last_button = 19 - self.last_button_state[12:32].index('1')
            except:
                self.last_button = None
       # return self.last_button_state , self.last_button
        
    def request_card(self):
        self.ser.write(b'c')
        time.sleep(.1)
        self.card_str = self.ser.readline().decode('ascii')[:-2]
        return(self.card_str)

    def _vibrate_key(self,vib):
        self.ser.write(b'v')
        #time.sleep(.1)
        self.ser.write(str(vib).encode('ascii'))
        self.ser.write(b'\r')
        time.sleep(.2)
        self.ser.write(b'v')
        #time.sleep(.1)
        self.ser.write(b'0')
        self.ser.write(b'\r')

    def vibrate_letter(self, letter, sim=False):
        counter = 0
        if sim:
            value = 0 
            for key in self.letter_to_chord[letter][::-1]: # switch order of string since MSB ans LSB are switching when reading left to right.
                if key == '1':
                    vib = pow(2, counter)
                    value = value + vib
                counter += 1
            self._vibrate_key(value)
        else:
            for key in self.letter_to_chord[letter][::-1]: # switch order of string since MSB ans LSB are switching when reading left to right.
                if key == '1':
                    vib = pow(2, counter)
                    self._vibrate_key(vib)
                    print(vib)
                    time.sleep(.05)
                    self.ser.reset_input_buffer() 
                counter += 1
        
    

