import argparse

INPUT_IN12 = 0x0000
INPUT_IN34 = 0x0001

MODE_MONO = 0x0000
MODE_STEREO = 0x0001

def get_input_index(input_name):
    if input_name.upper() == "IN12":
        return INPUT_IN12
    elif input_name.upper() == "IN34":
        return INPUT_IN34
    else:
        raise ValueError('Invalid argument value for --input')


def get_mode_id(mode_name):
    if mode_name.upper() == "MONO" :
        return MODE_MONO
    elif mode_name.upper() == "STEREO":
        return MODE_STEREO
    else:
        raise ValueError('Invalid argument value for --mode')

def set_monitor_mode(device, input, mode):
    device.ctrl_transfer(0xa1, 2, 0x0100, 0x2900, 16)
    device.ctrl_transfer(0xa1, 2, 0x0100, 0x2900, 50)
    device.ctrl_transfer(0x40, 8, mode, input, None)


class MonitorCommand:
    def __init__(self, args):
        parser = argparse.ArgumentParser()
        parser.add_argument("-i", "--input", type=str, help="The input pair to set monitoring for, either IN12 or IN34")
        parser.add_argument("-m", "--mode", type=str, help="The monitoring mode to set, either MONO or STEREO")
        args = parser.parse_args(args)
        
        self.input = get_input_index(args.input)
        self.mode = get_mode_id(args.mode)
    
    def execute(self, device):
        set_monitor_mode(device, self.input, self.mode)







