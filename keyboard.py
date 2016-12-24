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

        self.last_button_state = None

        self.last_chord = None

        self.last_letter = None

        self.comport = None
    
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


    def request_buttons(self):
        """ Sends request for button states to keyboard and waits
            for response.  Formats response into a 32-bit string.  Uses
            that string to generate a 6-bit chord.  Translates the
            chord into a character.  Then checks to see if one of the
            cursor buttons has been pressed.
        """
        
        self.ser.write(b'b')
        time.sleep(.1)
        
        if self.ser.inWaiting() > 0:
            
            self.last_button_state = format(int.from_bytes(self.ser.readline(),'little'),'032b')
            self.last_chord = self.last_button_state[2:8]
            self.last_letter = self.alphabet.get(self.last_chord,'X')
            
            if self.last_button_state[0] == '1':
                self.last_letter = 'newline'
            if self.last_button_state[1] == '1':
                self.last_letter = 'backspace'
            if self.last_button_state[8] == '1':
                self.last_letter = 'space'
            try:
                self.last_button = 19 - self.last_button_state[12:32].index('1')
            except:
                self.last_button = None



    def request_card(self):
        """ Sends a request to the keyboard for the data on the card.
            Returns this data in the form of an string.
        """
        
        self.ser.write(b'c')
        time.sleep(.1)
        
        self.card_str = self.ser.readline().decode('ascii')[:-2]  # not sure why the last two aren't included; test to find out.
        
        return(self.card_str)


    def _vibrate_key(self, vib, time=0.2):
        """ 
        """
        
        self.ser.write(b'v')
        self.ser.write(str(vib).encode('ascii'))
        self.ser.write(b'\r')
        
        time.sleep(time)

        self.ser.write(b'v')
        self.ser.write(b'0')
        self.ser.write(b'\r')


    def vibrate_letter(self, letter, sim=False):  # What the fuck does "sim" mean?
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
        
    

