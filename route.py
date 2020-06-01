import argparse

MODE_MONITOR_MIX = 0x0000
MODE_PC_OUT_12 = 0x0001
MODE_PC_OUT_34 = 0x0002

OUTPUT_LINE12 = 0x0000
OUTPUT_LINE34 = 0x0001

def get_output_index(output_name):
    if output_name == "LINE12":
        return OUTPUT_LINE12
    elif output_name == "LINE34":
        return OUTPUT_LINE34
    else:
        raise ValueError('Invalid argument value for --device')


def get_mode_id(mode_name):
    if mode_name == "MIX":
        return MODE_MONITOR_MIX
    elif mode_name == "OUT12":
        return MODE_PC_OUT_12
    elif mode_name == "OUT34":
        return MODE_PC_OUT_34
    else:
        raise ValueError('Invalid argument value for --mode')

def set_output_mode(device, output, mode):
    device.ctrl_transfer(0xa1, 2, 0x0100, 0x2900, 16)
    device.ctrl_transfer(0xa1, 2, 0x0100, 0x2900, 50)
    device.ctrl_transfer(0x40, 10, mode, output, None)


class RouteCommand:
    def __init__(self, args):
        parser = argparse.ArgumentParser()
        parser.add_argument("-d", "--dest", type=str, help="The line output device to route to, either LINE12 or LINE34")
        parser.add_argument("-s", "--source", type=str, help="The audio source to route from, MIX, OUT12 or OUT34")
        args = parser.parse_args(args)
        
        self.source = get_mode_id(args.source)
        self.dest = get_output_index(args.dest)
    
    def execute(self, device):
        set_output_mode(device, self.dest, self.source)







