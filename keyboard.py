import time
import serial
import serial.tools.list_ports
import struct

class keyboard:
    """ Object that communicates between the
        braillecade keyboard and the computer.
    """

    def __init__(self):
        """
            self.Ser: serial object?

            self.last_button_state:

            self.last_chord:

            self.last_letter:
        """

        self.ser = None


        self.standard = None
        self.raw = None
        self.chord = None
        self.letter = None
        self.cursor_key = None
        self.cursor_key_list = None
        self.card_state = None
        self.card_trigger = None
        self.card_str = '                    '
        self.card_ID = None
        

        self.last_chord = None

        self.last_letter = None

        self.comport = None
    
        
        self.chord_to_letter = {
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

        self.chord_to_key = {
            '000001': 'key1',
            '000010': 'key2',
            '000100': 'key3',
            '001000': 'key4',
            '010000': 'key5',
            '100000': 'key6',
            }

        self.key_to_chord = {
            'key1':'000001',
            'key2':'000010',
            'key3':'000100',
            'key4':'001000',
            'key5':'010000',
            'key6':'100000',
            }

    
    def list_coms(self):
        """ Returns a list of communication ports available
        """
        
        comports = list(serial.tools.list_ports.comports())

        port_numbers = []

        for port_no, description, address in comports:
            port_numbers.append(port_no)
            
        return port_numbers


    def test_coms(self):
        """
        """

        port_numbers = self.list_coms()

        if len(port_numbers) > 0:
            for port in port_numbers: # don't use i
                print("testing {}".format(port)) 
                self.ser = serial.Serial(port,baudrate=9600,timeout=0)
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
                    self.com_port = port
                    break # does this need to be a return

                self.ser.close

        print("No comports found")


    def update_keyboard(self):
        """
        """

        self.ser.write(b'b')
        time.sleep(.1)

        if self.ser.inWaiting() > 0:

            self.raw = format(int.from_bytes(self.ser.readline(),'little'),'032b')

            self.card_trigger = False

            if self.raw == '11111111111111111111111111111111':

                self.request_card()
                self.card_trigger = True
                
                self.raw = '00000000000000000000000000000000'

            if self.raw == '10101010101010101010101010101010':
                self.card_state = False
                self.card_str = '                    '
                self.card_ID = None

                self.raw = '00000000000000000000000000000000'


            self.chord = self.raw[2:8]
            self.letter = self.get_letter(self.chord)
            self.key = self.get_key(self.chord)

            try:
                self.cursor_key = 19 - self.raw[12:32].index('1')
            except:
                self.cursor_key = None

            self.cursor_keys_list = [(19 - pos) for pos,char in enumerate(self.raw[12:32]) if char == '1']


            if ((self.raw[0] == '1') & (self.raw[1] == '1') & (self.raw[8] == '1')):
                self.standard = 'quit'
            elif self.raw[8] == '1':
                self.standard = 'space'
                self.letter = 'space' # is this right? space is higher priority than a letter?
            elif ((self.raw[0] == '1') & (self.raw[1] == '1')):
                self.standard = 'display'
            elif (self.raw[0] == '1'):
                self.standard = 'newline'
            elif (self.raw[1] == '1'):
                self.standard = 'backspace'
            elif self.letter:
                self.standard = self.letter
            elif self.cursor_key:
                self.standard = self.cursor_key
            else:
                self.standard = None

        return {
                'raw':self.raw,
                'card_trigger':self.card_trigger,
                'chord':self.chord,
                'letter':self.letter,
                'cursor_key':self.cursor_key,
                'cursor_keys_list':self.cursor_keys_list,
                'standard':self.standard,
                'card_state':self.card_state,
                'card_str':self.card_str,
                'key':self.key,
                'card_ID':self.card_ID
                }


    def get_letter(self, chord):
        
        return self.chord_to_letter.get(chord, 'error')

    def get_key(self, chord):

        return self.chord_to_key.get(chord, None)


    def request_card(self):
        """ Sends a request to the keyboard for the data on the card.
            Returns this data in the form of an string.
        """
        
        self.ser.write(b'c')
        time.sleep(.1)
        
        temp_string = self.ser.readline().decode('ascii')
        self.card_str = temp_string[1:-2]
        self.card_ID = temp_string[0]

        print(self.card_str)

        self.card_state = True
        
        return(self.card_str)


    def vibrate_single_key(self, vib):

        counter = 0

        for digit in self.key_to_chord[vib][::-1]: # switch order of string since MSB ans LSB are switching when reading left to right.
            if digit == '1':
                vib = pow(2, counter)
                self._vibrate_key(vib)
                print(vib)
                time.sleep(.01)
                self.ser.reset_input_buffer() 
            counter += 1


    def _vibrate_key(self, vib, sleep_time=0.05):
        """ 
        """
        
        self.ser.write(b'v')
        self.ser.write(str(vib).encode('ascii'))
        self.ser.write(b'\r')
        
        time.sleep(sleep_time)

        self.ser.write(b'v')
        self.ser.write(b'0')
        self.ser.write(b'\r')


    def vibrate_letter(self, letter, sim=False):
        """
        """
        
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
        

    def vibrate_chord(self, chord, sim=False):
        """
        """
        
        counter = 0

        if sim:
            value = 0 
            for key in chord[::-1]: # switch order of string since MSB ans LSB are switching when reading left to right.
                if key == '1':
                    vib = pow(2, counter)
                    value = value + vib
                counter += 1
                
            self._vibrate_key(value)

        else:
            for key in chord[::-1]: # switch order of string since MSB ans LSB are switching when reading left to right.
                if key == '1':
                    vib = pow(2, counter)
                    self._vibrate_key(vib)
                    print(vib)
                    time.sleep(.05)
                    self.ser.reset_input_buffer() 
                counter += 1

