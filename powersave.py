import argparse

MODE_OFF = 0x0000
MODE_ON = 0x0001

def get_mode_id(mode_name):
    if mode_name.upper() == "ON" :
        return MODE_ON
    elif mode_name.upper() == "OFF":
        return MODE_OFF
    else:
        raise ValueError('Invalid argument value for --mode')

def set_powersave_mode(device, mode):
    device.ctrl_transfer(0xa1, 2, 0x0100, 0x2900, 16)
    device.ctrl_transfer(0xa1, 2, 0x0100, 0x2900, 50)
    device.ctrl_transfer(0x40, 4, mode, 0x0000, None)


class PowersaveCommand:
    def __init__(self, args):
        parser = argparse.ArgumentParser()
        parser.add_argument("-m", "--mode", type=str, help="The monitoring mode to set, either OFF or ON")
        args = parser.parse_args(args)
        
        self.mode = get_mode_id(args.mode)
    
    def execute(self, device):
        set_powersave_mode(device, self.mode)







