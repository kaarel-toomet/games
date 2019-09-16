# uwu977

## What it is

tile based game thingy

## Starting

Command line:

`uwu977.py`

It has various arguments, check `uwu977.py -h`.


## How to play

When starting the game, it asks for the world to load.  Either choose
one of the saved worlds, or press 'cancel' to create a new one.

Keyboard:

* arrow keys to move
* **A**, **S**, **D**, **W** to build left, down, right, up\
* **J**, **K**, **L**, **I** to break left, down, right, up\
* C to break backgrounds
* P to pause
* H to set home
* R to return home
* [ or ] to change build block
* X to toggle home visibility
* T to return to title
* G to change gamemode
* **Z** to save world file.  It opens a dialog to ask for file name to
  save.  Normally you want to save in a '.npz' file (numpy compressed
  matrices).


## Requirements

It is tested with python3 3.6 only but may run with python 2 too:

* python 3
* pygame
* numpy
* gtk 3 (tested with gi 3.26)

## Issues

* Currently the screen scaling does not work: I haven't found a good way
  to get screen DPI.
* There is some support for multiple screens.  As pygame does not
  directly handle it, the game relies on a short shellscript that
  revolves around 'xdotool' (X11-specific).  If xdotool is found and
  reports valid screen size, this is used as the size of the active
  screen.  Otherwise pygam full screen size is used, which may be
  wrong on multiple monitors.
  
