"""
This module contains a command to handle the powersave mode of 
the US4x4 interface
"""
import argparse

MODE_OFF = 0x0000
MODE_ON = 0x0001

def get_mode_id(mode_name):
    """
    Take a mode name and return the correct integer value to represent 
    it in the USB control transfer command
    """
    if mode_name.upper() == "ON" :
        return MODE_ON
    elif mode_name.upper() == "OFF":
        return MODE_OFF
    else:
        raise ValueError('Invalid argument value for --mode')

def set_powersave_mode(device, mode):
    """
    Executes the USB control transfer command to set the powersave
    mode for the given input pair
    """
    device.ctrl_transfer(0xa1, 2, 0x0100, 0x2900, 16)
    device.ctrl_transfer(0xa1, 2, 0x0100, 0x2900, 50)
    device.ctrl_transfer(0x40, 4, mode, 0x0000, None)


class PowersaveCommand:
    """
    Command to affect the powersave mode for the US4x4 interface
    """
    def __init__(self, args):
        """
        Constructor, takes the command-line arguments and parses them into useful inputs to 
        the control transfer command
        """
        parser = argparse.ArgumentParser()
        parser.add_argument("-m", "--mode", type=str, help="The monitoring mode to set, either OFF or ON")
        args = parser.parse_args(args)
        
        self.mode = get_mode_id(args.mode)
    
    def execute(self, device):
        """
        Invokes the control transfer instruction to set the powersave mode
        """
        set_powersave_mode(device, self.mode)







