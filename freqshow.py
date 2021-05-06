# FreqShow main application and configuration.
# Author: Tony DiCola (tony@tonydicola.com)
#
# The MIT License (MIT)
#
# Copyright (c) 2014 Adafruit Industries
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import os
import time
from typing import Any, Union

import pygame

import controller
import model
import ui
from rig_controller import RigController
from platform import system
import signal

# Application configuration.
from settings import SettingsStore

CLICK_DEBOUNCE = 0.4  # Number of seconds to wait between clicks events. Set
# to a few hunded milliseconds to prevent accidental
# double clicks from hard screen presses.

# Font size configuration.
MAIN_FONT = 25
NUM_FONT = 50

# Color configuration (RGB tuples, 0 to 255).
MAIN_BG = (0, 0, 0)  # Black
INPUT_BG = (60, 255, 255)  # Cyan-ish
INPUT_FG = (0, 0, 0)  # Black
CANCEL_BG = (128, 45, 45)  # Dark red
ACCEPT_BG = (45, 128, 45)  # Dark green
BUTTON_BG = (60, 60, 60)  # Dark gray
BUTTON_FG = (255, 255, 255)  # White
BUTTON_BORDER = (200, 200, 200)  # White/light gray
INSTANT_LINE = (0, 255, 128)  # Bright yellow green.

# Define gradient of colors for the waterfall graph.  Gradient goes from blue to
# yellow to cyan to red.
WATERFALL_GRAD = [(0, 0, 255), (0, 255, 255), (255, 255, 0), (255, 0, 0)]

# Configure default UI and button values.
ui.MAIN_FONT = MAIN_FONT
ui.Button.fg_color = BUTTON_FG
ui.Button.bg_color = BUTTON_BG
ui.Button.border_color = BUTTON_BORDER
ui.Button.padding_px = 2
ui.Button.border_px = 2

LABEL_ALPHA_FG = (255, 255, 255, 128)
LABEL_ALPHA_BG = (0, 0, 0, 128)


def handler(signum, frame):
    pass


try:
    signal.signal(signal.SIGHUP, handler)
except:
    pass

if __name__ == '__main__':
    settings_store = SettingsStore('settings.json')
    rig_controller = None
    # Initialize pygame and SDL to use the PiTFT display and touchscreen.
    if system() != "Windows":
        os.putenv('SDL_VIDEODRIVER', 'fbcon')
        os.putenv('SDL_FBDEV', '/dev/fb0')
        os.putenv('SDL_MOUSEDRV', 'TSLIB')
        os.putenv('SDL_MOUSEDEV', '/dev/input/event0')
    rig_controller = RigController('/dev/ttyAMA0', 9600, 120)

    pygame.display.init()
    pygame.font.init()
    pygame.mouse.set_visible(True)
    # Get size of screen and create main rendering surface.
    if system() == "Windows":
        size = (800, 480)
        screen = pygame.display.set_mode(size)
    else:
        size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        screen = pygame.display.set_mode(size, pygame.FULLSCREEN)

    # Display splash screen.
    splash = pygame.image.load('freqshow_splash.png')
    screen.fill(MAIN_BG)
    screen.blit(splash, ui.align(splash.get_rect(), (0, 0, size[0], size[1])))
    pygame.display.update()
    splash_start = time.time()
    # Create model and controller.
    fsmodel = model.FreqShowModel(size[0], size[1], settings_store)
    fscontroller = controller.FreqShowController(fsmodel, rig_controller=rig_controller)
    # Main loop to process events and render current view.
    lastclick = 0

    last_render = time.time()
    freq = 68.3285
    fsmodel.set_center_freq(freq)
    fsmodel.set_center_freq_display(freq)
    last_freq_change = time.time()
    while True:
        # Process any events (only mouse events for now).
        for event in pygame.event.get():
            if event.type is pygame.MOUSEBUTTONDOWN \
                    and (time.time() - lastclick) >= CLICK_DEBOUNCE:
                lastclick = time.time()
                fscontroller.current().click(pygame.mouse.get_pos())
            elif event.type is pygame.QUIT:
                fscontroller.current().quit_accept()
        # Update and render the current view.
        if time.time() - last_render > 1 / 20:
            fscontroller.current().render(screen)
            pygame.display.update()
            last_render = time.time()
    # if rig_controller and time.time() - last_freq_change > 0.5:
    # 	fscontroller.update_display_freqency()
    # 	last_freq_change = time.time()
