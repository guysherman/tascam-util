"""
This module contains a command to control the signal routing for the US4x4
"""
import argparse

MODE_MONITOR_MIX = 0x0000
MODE_PC_OUT_12 = 0x0001
MODE_PC_OUT_34 = 0x0002

OUTPUT_LINE12 = 0x0000
OUTPUT_LINE34 = 0x0001

def get_output_index(output_name):
    """
    Converts a string from the command-line arguments into an integer value,
    which we can use in the control transfer command to the device

    output_name - a string indentifying which pair of LINE outputs we wish to 
    modify
    """
    if output_name == "LINE12":
        return OUTPUT_LINE12
    elif output_name == "LINE34":
        return OUTPUT_LINE34
    else:
        raise ValueError('Invalid argument value for --device')


def get_mode_id(mode_name):
    """
    Converts a string from the command-line arguments into an integer value,
    which we can use in the control transfer command to the device

    mode_name - a string indentifying which sound source we wish to route from
    """
    if mode_name == "MIX":
        return MODE_MONITOR_MIX
    elif mode_name == "OUT12":
        return MODE_PC_OUT_12
    elif mode_name == "OUT34":
        return MODE_PC_OUT_34
    else:
        raise ValueError('Invalid argument value for --mode')

def set_output_mode(device, output, mode):
    """
    Sends the appropriate control-transfer commands over USB to the device

    device - the pyusb device object we wish to communicate with
    output - the index of the Line Out pair we wish to modify
    mode - the index of the sound source we wish to route from
    """
    device.ctrl_transfer(0xa1, 2, 0x0100, 0x2900, 16)
    device.ctrl_transfer(0xa1, 2, 0x0100, 0x2900, 50)
    device.ctrl_transfer(0x40, 10, mode, output, None)


class RouteCommand:
    """
    A command which affects the internal signal routing of the US4x4
    """
    def __init__(self, args):
        """
        Constructor. Parses the command-line arguments passed to the command, extracts the necessary data, 
        converts it to the appropriate integers, and stores for use later
        """
        parser = argparse.ArgumentParser()
        parser.add_argument("-d", "--dest", type=str, help="The line output device to route to, either LINE12 or LINE34")
        parser.add_argument("-s", "--source", type=str, help="The audio source to route from, MIX, OUT12 or OUT34")
        args = parser.parse_args(args)
        
        self.source = get_mode_id(args.source)
        self.dest = get_output_index(args.dest)
    
    def execute(self, device):
        """
        Executes the task of altering the internal signal routing of the device
        """
        set_output_mode(device, self.dest, self.source)







