import usb.core
import usb.util
import sys
import os
import argparse

from route import RouteCommand

VENDOR_ID=0x0644
PRODUCT_ID = 0x804e

MODE_MONITOR_MIX = 0x0000
MODE_PC_OUT_12 = 0x0001
MODE_PC_OUT_34 = 0x0002

OUTPUT_LINE12 = 0x0000
OUTPUT_LINE34 = 0x0001

# os.environ['PYUSB_DEBUG'] = 'debug'

def get_device():
    device = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)

    if device is None:
        raise ValueError('Device not found')

    return device

def control_device(device, device_config):
    try:
        if device.is_kernel_driver_active(0):
            device.detach_kernel_driver(0)
        if device.is_kernel_driver_active(1):
            device.detach_kernel_driver(1)
        if device.is_kernel_driver_active(2):
            device.detach_kernel_driver(2)
        if device.is_kernel_driver_active(3):
            device.detach_kernel_driver(3)
        if device.is_kernel_driver_active(4):
            device.detach_kernel_driver(4)
        usb.util.claim_interface(device, device_config[(0,0)])
        usb.util.claim_interface(device, device_config[(1,0)])
        usb.util.claim_interface(device, device_config[(2,0)])
        usb.util.claim_interface(device, device_config[(3,0)])
        usb.util.claim_interface(device, device_config[(4,0)])
    except usb.USBError as err:
        print(err)

def release_device(device, device_config):
    try:
        usb.util.release_interface(device, device_config[(0,0)])
        usb.util.release_interface(device, device_config[(1,0)])
        usb.util.release_interface(device, device_config[(2,0)])
        usb.util.release_interface(device, device_config[(3,0)])
        usb.util.release_interface(device, device_config[(4,0)])
        device.attach_kernel_driver(0)
    except usb.USBError as err:
        print(err)


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

def get_command(command, args):
    if command == "route":
        return RouteCommand(args)
    else:
        raise ValueError('Unknown command')

def main(arguments):

    command = get_command(arguments.command, arguments.args)

    device = get_device()
    device_config = device.get_active_configuration()
    control_device(device, device_config)
    print("Got control of device")
     
    command.execute(device)

    release_device(device, device_config)
    print("Gave up device")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("command", type=str, help="The command to execute")
    parser.add_argument('args', nargs=argparse.REMAINDER, help="the args to pass to the command")
    args = parser.parse_args()
    main(args)


