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

        self.letter_to_chord = {
                'a':'OOXOOO',
                'b':'OXXOOO',
                'c':'OOXXOO',
                'd':'OOXXXO',
                'e':'OOXOXO',
                'f':'OXXXOO',
                'g':'OXXXXO',
                'h':'OXXOXO',
                'i':'OXOXOO',
                'j':'OXOXXO',
                'k':'XOXOOO',
                'l':'XXXOOO',
                'm':'XOXXOO',
                'n':'XOXXXO',
                'o':'XOXOXO',
                'p':'XXXXOO',
                'q':'XXXXXO',
                'r':'XXXOXO',
                's':'XXOXOO',
                't':'XXOXXO',
                'u':'XOXOOX',
                'v':'XXXOOX',
                'w':'OXOXXX',
                'x':'XOXXOX',
                'y':'XOXXXX',
                'z':'XOXOXX'}

    
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
        counter = 0
        for key in self.letter_to_chord[letter]:
            if key == 'X':
                vib = pow(2, counter)
                self._vibrate_key(vib)
                print(vib)
                time.sleep(.05)
                self.ser.reset_input_buffer()  #vibrating causes noise with the input buffer not sure why need to figure this out.
            counter += 1
        
    
