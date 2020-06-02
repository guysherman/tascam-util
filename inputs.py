import argparse

INPUT_IN1 = 0x0000
INPUT_IN2 = 0x0001
INPUT_IN3 = 0x0002
INPUT_IN4 = 0x0003


MODE_OFF = 0x0000
MODE_ON = 0x0001

def get_input_index(input_name):
    if input_name.upper() == "IN1":
        return INPUT_IN1
    elif input_name.upper() == "IN2":
        return INPUT_IN2
    elif input_name.upper() == "IN3":
        return INPUT_IN3
    elif input_name.upper() == "IN4":
        return INPUT_IN4
    else:
        raise ValueError('Invalid argument value for --input')


def get_mode_id(mode_name):
    if mode_name.upper() == "ON" :
        return MODE_ON
    elif mode_name.upper() == "OFF":
        return MODE_OFF
    else:
        raise ValueError('Invalid argument value for --mode')

def set_input_mode(device, input, mode):
    device.ctrl_transfer(0xa1, 2, 0x0100, 0x2900, 16)
    device.ctrl_transfer(0xa1, 2, 0x0100, 0x2900, 50)
    device.ctrl_transfer(0x40, 6, mode, input, None)


class InputCommand:
    def __init__(self, args):
        parser = argparse.ArgumentParser()
        parser.add_argument("-i", "--input", type=str, help="The input pair to set monitoring for, either IN1, IN2, IN3 or IN4")
        parser.add_argument("-m", "--mode", type=str, help="The monitoring mode to set, either OFF or ON")
        args = parser.parse_args(args)
        
        self.input = get_input_index(args.input)
        self.mode = get_mode_id(args.mode)
    
    def execute(self, device):
        set_input_mode(device, self.input, self.mode)







