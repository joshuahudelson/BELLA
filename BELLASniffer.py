from keyboard import keyboard

braille_keyboard = keyboard()
braille_keyboard.test_coms()

while(1):
    input_dict = braille_keyboard.update_keyboard()
    if (input_dict['raw'] != '00000000000000000000000000000000'):
        print(input_dict['raw'])
        print(input_dict['chord'])
        print(input_dict['cursor_key'])
