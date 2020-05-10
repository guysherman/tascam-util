# Tascam Util

This repository contains (a) tool(s) for controlling the software  mixer and routing of the Tascam USB 4x4 audio interface, on Linux.

On Windows or Mac, you can just use Tascam's utilities.

## Getting up and running

### Dependencies

* Python 3
* virtualenv
* LibUSB
* PyUSB - we'll install this one slightly differently

On Ubuntu 20.04 you'd do the following to get these:

```
$> sudo apt install python3 python3-pip python3-virtualenv
$> sudo apt install libusb-1.0-0
```

### Get the code

Then, clone this code, with something like:

```
$> git clone git@github.com:guysherman/tascam-util.git
$> cd tascam-util
$> ./setup.sh
```

Or download it as a zip file, whatever.

Note, your distribution might call python3 `python` and pip3 `pip`, in which case you'll need to 
tweak `setup.sh` to use the correct name. And do the same thing in your mind when reading further in this doc

## Set some settings

I mainly wrote this because I wanted to set Line Outs 3 and 4 to be directly mapped to PC Outs 3 and 4, rather than feeding from the internal mixer.

Here's the help text:

```
usage: tascam-util.py [-h] [-o OUTPUT] [-m MODE]

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        The line output device to modify, either LINE12 or LINE34
  -m MODE, --mode MODE  The mode to set the output to, MIX, OUT12 or OUT34
  ```

Essentially, you have two output groups to play with:
* Line Outs 1-2
* Line Outs 3-4

They can be set to one of:
* MIX - All the PC outs, and the physical inputs on the interface are mixed, according to the 'Monitor Balance' knob on the inteface, and then sent out the output group
* OUT12 - The output group receives a direct feed from PC Outs 1 and 2
* OUT34 - The output group receives a direct feed from PC Outs 3 and 4

**Really Important Note**: Line Outs 3-4 do not have a physical volume control on the interface, so they are really loud! I might eventually reverse engineer Tascam's "Software Mixer" application, rather than just this little bit of their settings panel, in which case I might find a way to control that line out via software.

I have my setup as follows:

Line Out 1-2 : Monitor Mix
Line Out 3-4 : PC Out 3-4

I have my monitors running from Line Out 3-4, and then I send the master out of my DAW to Channels 3 and 4. Usually I'll send it to Channels 1 and 2, but if I want to send a particular mix to the headphones I can set up a separate bus to go to Channels 1 and 2.

So to kick my interface into gear I do the following, from within the root folder of where the code is:

```
$> python3 tascam-util.py -o LINE12 -m MIX
$> python3 tascam-util.py -o LINE34 -m OUT34

```

