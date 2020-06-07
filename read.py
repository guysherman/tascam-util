"""
This module contains a command to read parameters from the device
"""
import argparse


COMMAND_POWERSAVE = 0x03
COMMAND_INPUT_ENABLE = 0x05
COMMAND_MONITORING_MODE = 0x07
COMMAND_ROUTING = 0x09

INDICES_POWERSAVE = [0]
INDICES_INPUT_ENABLE = [0, 1, 2, 3]
INDICES_MONITORING_MODE = [0, 1]
INDICES_ROUTING = [0, 1]

CONVERT_POWERSAVE = ["Off", "On"]
CONVERT_INPUT_ENABLE = ["Off", "On"]
CONVERT_MONITORING_MODE = ["Mono", "Stereo"]
CONVERT_ROUTING = ["Monitor Mix", "PC 1 & 2", "PC 3 & 4"]

OUTPUT_POWERSAVE = "Auto-powersave {} is {}"
OUTPUT_INPUT_ENABLE = "Input {} is {}"
OUTPUT_MONITORING_MODE = "Channel Pair {} is monitored in {}"
OUTPUT_ROUTING = "Channel Pair {} is playing back {}"

def get_read_command(command_name):
    """
        Returns the value for bRequest
    """
    if command_name.upper() == "POWERSAVE":
        return COMMAND_POWERSAVE
    elif command_name.upper() == "INPUT":
        return COMMAND_INPUT_ENABLE
    elif command_name.upper() == "MONITOR":
        return COMMAND_MONITORING_MODE
    elif command_name.upper() == "ROUTE":
        return COMMAND_ROUTING
    else:
        raise ValueError('Invlaid argument for --command')

def get_indices(command_name):
    """
        Returns the set of indices to iterate through
    """
    if command_name.upper() == "POWERSAVE":
        return INDICES_POWERSAVE
    elif command_name.upper() == "INPUT":
        return INDICES_INPUT_ENABLE
    elif command_name.upper() == "MONITOR":
        return INDICES_MONITORING_MODE
    elif command_name.upper() == "ROUTE":
        return INDICES_ROUTING
    else:
        raise ValueError('Invlaid argument for --command')

def get_output_conversion(command_name):
    """
        Returns a lookup to turn the response values back into
        strings
    """
    if command_name.upper() == "POWERSAVE":
        return CONVERT_POWERSAVE
    elif command_name.upper() == "INPUT":
        return CONVERT_INPUT_ENABLE
    elif command_name.upper() == "MONITOR":
        return CONVERT_MONITORING_MODE
    elif command_name.upper() == "ROUTE":
        return CONVERT_ROUTING
    else:
        raise ValueError('Invalid argument for --command')

def get_message(command_name):
    """
        Returns the output string for the given command
    """
    if command_name.upper() == "POWERSAVE":
        return OUTPUT_POWERSAVE
    elif command_name.upper() == "INPUT":
        return OUTPUT_INPUT_ENABLE
    elif command_name.upper() == "MONITOR":
        return OUTPUT_MONITORING_MODE
    elif command_name.upper() == "ROUTE":
        return OUTPUT_ROUTING
    else:
        raise ValueError('Invalid argument for --command')

def read_data(device, command, indices, output_conversion, message):
    """
        Reads data from the usb device
    """
    for index in indices:
        device.ctrl_transfer(0xa1, 2, 0x0100, 0x2900, 16)
        device.ctrl_transfer(0xa1, 2, 0x0100, 0x2900, 50)
        result = device.ctrl_transfer(0xc0, command, 0, index, 1, None)
        print(message.format(index, output_conversion[result[0]]))


class ReadCommand:
    """
    A command which affects the internal signal routing of the US4x4
    """
    def __init__(self, args):
        """
        Constructor. Parses the command-line arguments passed to the command, extracts the necessary data, 
        converts it to the appropriate integers, and stores for use later
        """
        parser = argparse.ArgumentParser()
        parser.add_argument("-c", "--command", type=str, help="The line output device to route to, either POWERSAVE, INPUT, MONITOR, ROUTE")
        args = parser.parse_args(args)
        
        self.command = get_read_command(args.command)
        self.indices = get_indices(args.command)
        self.output_conversion = get_output_conversion(args.command)
        self.message = get_message(args.command)
    
    def execute(self, device):
        """
        Executes the task of altering the internal signal routing of the device
        """
        read_data(device, self.command, self.indices, self.output_conversion, self.message)







