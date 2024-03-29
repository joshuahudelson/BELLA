import time
import serial
import serial.tools.list_ports
import struct
import codecs
import pygame


class keyboard:
    """ Communicates between the BELLA
        keyboard and the game programs.
    """

    def __init__(self):
        """
            self.ser: a serial object for transmitting the keyboard state.

            self.raw: a 32-bit number representing the entire state of the
                      keyboard ("1" == key down).

            self.chord: a 6-bit number representing only the state of the main
                        typing keys.

            self.letter: a string representing the letter translation of the
                         chord of keys being pressed.  If no chord, then "None."

            self.cursor_key: the index (0-19) of the cursor key being pressed.
                             If multiple, it returns only the leftmost.

            self.cursor_keys_list: a list of indices of the cursor keys being
                                   depressed.

            self.standard:  a string that is either the letter translation of
                            a chord being typed, or one of a set of additional
                            commands (quit, space, display, newline, backspace)
                            or the index of a cursor key that has been pressed.

            self.card_state: boolean; is card inserted or not?

            self.last_button_state:	DELETE?

            self.last_chord:		DELETE?

            self.last_letter:		DELETE?
        """

        self.ser = None

        self.raw = None
        self.chord = None
        self.letter = None
        self.cursor_key = None
        self.cursor_keys_list = None
        self.standard = None

        self.card_state = None
        self.card_trigger = None
        self.card_str = '                    '
        self.card_ID = None


        self.last_chord = None
        self.last_letter = None
        self.key = None
        self.braille_unicode = None

        self.comport = None

        self.keyboard_flag = None

        self.temp_readline = None

        self.comp_keyboard_counter = 0
        self.COMP_KEYBOARD_COUNTER_ITERATIONS = 3
        self.comp_keyboard_key_list = [];


        self.chord_to_letter = {
            '000001': 'a', '000011': 'b', '001001': 'c', '011001': 'd',
            '010001': 'e', '001011': 'f', '011011': 'g', '010011': 'h',
            '001010': 'i', '011010': 'j', '000101': 'k', '000111': 'l',
            '001101': 'm', '011101': 'n', '010101': 'o', '001111': 'p',
            '011111': 'q', '010111': 'r', '001110': 's', '011110': 't',
            '100101': 'u', '100111': 'v', '111010': 'w', '101101': 'x',
            '111101': 'y', '110101': 'z', '000000': None,
            }

        self.letter_to_chord = {
            'a':'000001', 'b':'000011', 'c':'001001', 'd':'011001',
            'e':'010001', 'f':'001011', 'g':'011011', 'h':'010011',
            'i':'001010', 'j':'011010', 'k':'000101', 'l':'000111',
            'm':'001101', 'n':'011101', 'o':'010101', 'p':'001111',
            'q':'011111', 'r':'010111', 's':'001110', 't':'011110',
            'u':'100101', 'v':'100111', 'w':'111010', 'x':'101101',
            'y':'111101', 'z':'110101', 'space':'000000',
                }

        self.chord_to_key = {
            '000001': 'key1', '000010': 'key2', '000100': 'key3',
            '001000': 'key4', '010000': 'key5', '100000': 'key6',
            }

        self.key_to_chord = {
            'key1':'000001', 'key2':'000010', 'key3':'000100',
            'key4':'001000', 'key5':'010000', 'key6':'100000',
            }

        self.chord_to_unicode = {
            '000000': None, '000001': u'\u2801', '000010': u'\u2802', '000011': u'\u2803',
            '000100': u'\u2804', '000101': u'\u2805', '000110': u'\u2806', '000111': u'\u2807',
            '001000': u'\u2808', '001001': u'\u2809', '001010': u'\u280A', '001011': u'\u280B',
            '001100': u'\u280C', '001101': u'\u280D', '001110': u'\u280E', '001111': u'\u280F',
            '010000': u'\u2810', '010001': u'\u2811', '010010': u'\u2812', '010011': u'\u2813',
            '010100': u'\u2814', '010101': u'\u2815', '010110': u'\u2816', '010111': u'\u2817',
            '011000': u'\u2818', '011001': u'\u2819', '011010': u'\u281A', '011011': u'\u281B',
            '011100': u'\u281C', '011101': u'\u281D', '011110': u'\u281E', '011111': u'\u281F',
            '100000': u'\u2820', '100001': u'\u2821', '100010': u'\u2822', '100011': u'\u2823',
            '100100': u'\u2824', '100101': u'\u2825', '100110': u'\u2826', '100111': u'\u2827',
            '101000': u'\u2828', '101001': u'\u2829', '101010': u'\u282A', '101011': u'\u282B',
            '101100': u'\u282C', '101101': u'\u282D', '101110': u'\u282E', '101111': u'\u282F',
            '110000': u'\u2830', '110001': u'\u2831', '110010': u'\u2832', '110011': u'\u2833',
            '110100': u'\u2834', '110101': u'\u2835', '110110': u'\u2836', '110111': u'\u2837',
            '111000': u'\u2838', '111001': u'\u2839', '111010': u'\u283A', '111011': u'\u283B',
            '111100': u'\u283C', '111101': u'\u283D', '111110': u'\u283E', '111111': u'\u283F'}


        self.unicode_to_chord = {
            u'\u2800': '000000', u'\u2801': '000001', u'\u2802': '000010', u'\u2803': '000011',
            u'\u2804': '000100', u'\u2805': '000101', u'\u2806': '000110', u'\u2807': '000111',
            u'\u2808': '001000', u'\u2809': '001001', u'\u280A': '001010', u'\u280B': '001011',
            u'\u280C': '001100', u'\u280D': '001101', u'\u280E': '001110', u'\u280F': '001111',
            u'\u2810': '010000', u'\u2811': '010001', u'\u2812': '010010', u'\u2813': '010011',
            u'\u2814': '010100', u'\u2815': '010101', u'\u2816': '010110', u'\u2817': '010111',
            u'\u2818': '011000', u'\u2819': '011001', u'\u281A': '011010', u'\u281B': '011011',
            u'\u281C': '011100', u'\u281D': '011101', u'\u281E': '011110', u'\u281F': '011111',
            u'\u2820': '100000', u'\u2821': '100001', u'\u2822': '100010', u'\u2823': '100011',
            u'\u2824': '100100', u'\u2825': '100101', u'\u2826': '100110', u'\u2827': '100111',
            u'\u2828': '101000', u'\u2829': '101001', u'\u282A': '101010', u'\u282B': '101011',
            u'\u282C': '101100', u'\u282D': '101101', u'\u282E': '101110', u'\u282F': '101111',
            u'\u2830': '110000', u'\u2831': '110001', u'\u2832': '110010', u'\u2833': '110011',
            u'\u2834': '110100', u'\u2835': '110101', u'\u2836': '110110', u'\u2837': '110111',
            u'\u2838': '111000', u'\u2839': '111001', u'\u283A': '111010', u'\u283B': '111011',
            u'\u283C': '111100', u'\u283D': '111101', u'\u283E': '111110', u'\u283F': '111111'}


    def list_coms(self):
        """ Returns a list of communication ports available
        """

        comports = list(serial.tools.list_ports.comports())

        port_numbers = []

        for port_no, description, address in comports:
            port_numbers.append(port_no)

        return port_numbers


    def test_coms(self):
        """ Scans through the communication ports to find the one to which
            the BELLA is attached.
        """

        port_numbers = self.list_coms()

        if len(port_numbers) > 0:
            for port in port_numbers:
                print("testing {}".format(port))
                print(port)
                self.ser = serial.Serial(port,baudrate=38400,timeout=0)
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
                    self.keyboard_flag = 1
                    break # does this need to be a return?

                self.keyboard_flag = 1
                print("No BrailleCade found.")
                self.ser.close
        else:
            print("No comports found.")
            print("Using computer keyboard.")
            self.keyboard_flag = 0


    def update_keyboard(self):
        """ The main keyboard function.  Sends keyboard a a 'b' to trigger
            keyboard to return its state.  If state is all 1s, there's a
            card to read from.  If it's all 10s, there's not.
        """
        self.ser.write(b'b')
        time.sleep(.1)

        if self.ser.inWaiting() > 0:
            self.temp_readline = self.ser.readline()
            return self.parse_keys_pressed()


    def parse_keys_pressed(self):
#        print("This is temp_readline: " + str(self.temp_readline))
        self.raw = format(int.from_bytes(self.temp_readline,'little'),'032b')
        self.raw = self.raw[0:32]
#        print("This is self.raw after formatting: " + self.raw)

        self.card_trigger = False

        if self.raw == '11111111111111111111111111111111':

            self.request_card()
            self.card_trigger = True

            self.raw = '00000000000000000000000000000000'
#            print("This is self.raw after 1111...: " + self.raw)

        if self.raw == '10101010101010101010101010101010':
            self.card_state = False
            self.card_str = '                    '
            self.card_ID = None
            print("This is self.raw after 101010: " + self.raw)

            self.raw = '00000000000000000000000000000000'
#            print("This is self.raw after 00000...: " + self.raw)

        self.chord = self.raw[0:6]  # chord = combination of the 6 keys
        self.letter = self.get_letter(self.chord) # its translation to letter
        self.key = self.get_key(self.chord) # if just a single key is pressed

        # See if any cursor keys are pressed (only returns leftmost one)
        try:
            self.cursor_key = self.raw[9:31].index('1')
        except:
            self.cursor_key = None

        # Returns the full list of pressed cursor keys
        self.cursor_keys_list = [(19 - pos) for pos,char in enumerate(self.raw[12:32]) if char == '1']


        if ((self.raw[0] == '1') & (self.raw[1] == '1') & (self.raw[8] == '1')):
            self.standard = 'quit'
#            print("quit tripped")
        elif self.raw[1] == '1':
            self.standard = 'space'
            self.letter = 'space' # is this right? space is higher priority than a letter?
#            print("space tripped")
        elif ((self.raw[0] == '1') & (self.raw[8] == '1')):
            self.standard = 'display'
#            print("display tripped")
        elif (self.raw[8] == '1'):
            self.standard = 'newline'
#            print("newline tripped")
        elif (self.raw[0] == '1'):
            self.standard = 'backspace'
#            print("backspace tripped")
        elif self.letter:
            self.standard = self.letter
#            print("self standard set equal to letter")
        elif self.cursor_key:
            self.standard = self.cursor_key
#            print("self standard set equal to cursor key")
        else:
            self.standard = None
#            print("self standard set equal to none")

        self.braille_unicode = self.chord_to_unicode[self.chord]

#        print("Card Trigger: " + str(self.card_trigger))

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
                'card_ID':self.card_ID,
                'braille_unicode': self.braille_unicode,
                'volume':'whatever'
                }

    def get_letter(self, chord):
        """ Get a letter from a chord.
        """
        return self.chord_to_letter.get(chord, 'error')


    def get_key(self, chord):
        """ Get a key from a chord.
        """
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


if __name__ == "__main__":
    this_keyboard = keyboard()
    this_keyboard.test_coms()
