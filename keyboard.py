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

    ##    letter2vib = {
    ##                'a': 1, 
    ##                'b': 3, 
    ##                'c': 9,
    ##                'd': 25,
    ##                'e': 17,
    ##                'f': 11,
    ##                'g': 27,
    ##                'h': 19,
    ##                'i': 10,
    ##                'j': 26,
    ##                'k': 5,
    ##                'l': 7,
    ##                'm': 13,
    ##                'n': 29,
    ##                'o': 21,
    ##                'p': 15,
    ##                'q': 31,
    ##                'r': 23,
    ##                's': 14,
    ##                't': 30,
    ##                'u': 37,
    ##                'v': 39,
    ##                'w': 58,
    ##                'x': 45,
    ##                'y': 61,
    ##                'z': 53
    ##                }

        vib1 = 1
        vib2 = 2
        vib3 = 4
        vib4 = 8
        vib5 = 16
        vib6 = 32

        self.letter2vib = {
                'a':[vib1],
                'b':[vib1,vib2],
                'c':[vib1,vib4],
                'd':[vib1,vib4,vib5],
                'e':[vib1,vib5],
                'f':[vib1,vib2,vib4],
                'g':[vib1,vib2,vib4,vib5],
                'h':[vib1,vib2,vib5],
                'i':[vib2,vib4],
                'j':[vib2,vib4,vib5],
                'k':[vib1,vib3],
                'l':[vib1,vib2,vib3],
                'm':[vib1,vib3,vib4],
                'n':[vib1,vib3,vib4,vib5],
                'o':[vib1,vib3,vib5],
                'p':[vib1,vib2,vib3,vib4],
                'q':[vib1,vib2,vib3,vib4,vib5],
                'r':[vib1,vib2,vib3,vib5],
                's':[vib2,vib3,vib4],
                't':[vib2,vib3,vib4,vib5],
                'u':[vib1,vib3,vib6],
                'v':[vib1,vib2,vib3,vib6],
                'w':[vib2,vib4,vib5,vib6],
                'x':[vib1,vib3,vib4,vib6],
                'y':[vib1,vib3,vib4,vib5,vib6],
                'z':[vib1,vib3,vib5,vib6],
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
        return self.last_button_state , self.last_button
        
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

    def vibrate_letter(self,letter):
        for vib in self.letter2vib.get(letter):
            self._vibrate_key(vib)
            print(vib)
            time.sleep(.05)
            self.ser.reset_input_buffer()  #vibrating causes noise with the input buffer not sure why need to figure this out.
            
        
    
