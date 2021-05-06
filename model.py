# FreqShow main application model/state.
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
import time
from glob import glob

import numpy as np
from rtlsdr import *

import pyfftw

from scipy import signal

from settings import SettingsStore

START_FREQ = 145  # Default startup Frequency in mhz
MAX_ZOOM_LEVEL = 4
SDR_SAMPLE_SIZE = 800 * 2 ** MAX_ZOOM_LEVEL  # Number of samples to grab from the radio.  Should be


# larger than the maximum display width.


class FreqShowModel(object):
    settings_store: SettingsStore
    TRV_MODE_LIST = [
        ('NORMAL', 0, 'Normal'),
        ('TRV1', 10386.0 - 430.0, '3cm'),
        ('TRV2', 10489.0 - 430.0, 'QO100'),
    ]

    def __init__(self, width, height, settings_store):
        """Create main FreqShow application model.  Must provide the width and
        height of the screen in pixels.
        """
        # Set properties that will be used by views.
        self.settings_store = settings_store
        self.window = signal.blackmanharris(SDR_SAMPLE_SIZE + 4, False, )
        self.file_data = None
        self.zoom_level = 1
        self.center_freq_display = None
        self.width = width
        self.height = height
        # Initialize auto scaling both min and max intensity (Y axis of plots).
        self.min_auto_scale = True
        self.max_auto_scale = True
        self.set_min_intensity('AUTO')
        self.set_max_intensity('AUTO')
        # Initialize RTL-SDR library.
        self.sdr = RtlSdr()
        # center freq
        self.set_center_freq(START_FREQ)
        self.set_sample_rate(0.25)
        self.set_offset_tuning(0)
        self.set_gain('AUTO')

        self.raw_data = []
        self._current_trv_mode_pos = self.settings_store.get('trv_mode_current', 0)
        trv_modes = self.settings_store.get('trv_modes')
        if trv_modes:
            self.TRV_MODE_LIST = self.TRV_MODE_LIST[:1]
            self.TRV_MODE_LIST.extend(trv_modes[1:])
        self.settings_store.set('trv_modes', self.TRV_MODE_LIST)
        if self._current_trv_mode_pos > len(self.TRV_MODE_LIST):
            self._current_trv_mode_pos = 0
        self.settings_store.set('trv_mode_current', self._current_trv_mode_pos)

        pyfftw.interfaces.cache.enable()

    # self.print_time()

    def _clear_intensity(self):
        if self.min_auto_scale:
            self.min_intensity = None
        if self.max_auto_scale:
            self.max_intensity = None
        self.range = None

    def get_current_trv_mode(self):
        return self.TRV_MODE_LIST[self._current_trv_mode_pos]

    def toggle_current_trv_mode(self):
        self._current_trv_mode_pos += 1
        if self._current_trv_mode_pos >= len(self.TRV_MODE_LIST):
            self._current_trv_mode_pos = 0
        self.settings_store.set('trv_mode_current', self._current_trv_mode_pos)

    def get_center_freq(self):
        """Return center frequency of tuner in megahertz."""
        return self.sdr.get_center_freq() / 1000000.0

    def set_center_freq(self, freq_mhz):
        """Set tuner center frequency to provided megahertz value."""
        try:
            self.sdr.set_center_freq(freq_mhz * 1000000.0)
            self._clear_intensity()
        except IOError:
            # Error setting value, ignore it for now but in the future consider
            # adding an error message dialog.
            pass

    def get_zoom_level(self):
        return self.zoom_level

    def get_center_freq_display(self):
        """Return center frequency of tuner in megahertz."""
        name, offset, display_name = self.get_current_trv_mode()
        return self.center_freq_display + offset

    def set_center_freq_display(self, freq_mhz):
        self.center_freq_display = freq_mhz

    def get_sample_rate(self):
        """Return sample rate of tuner in megahertz."""
        return self.sdr.get_sample_rate() / 1000000.0

    def set_sample_rate(self, sample_rate_mhz):
        """Set tuner sample rate to provided frequency in megahertz."""
        try:
            self.sdr.set_sample_rate(sample_rate_mhz * 1000000.0)
        except IOError:
            # Error setting value, ignore it for now but in the future consider
            # adding an error message dialog.
            pass

    def set_offset_tuning(self, enabled):
        """Set tuner sample rate to provided frequency in megahertz."""
        try:
            librtlsdr.rtlsdr_set_offset_tuning(self.sdr.dev_p, int(enabled))
        except IOError as e:
            print(e)
            # Error setting value, ignore it for now but in the future consider
            # adding an error message dialog.
            pass

    def get_gain(self):
        """Return gain of tuner.  Can be either the string 'AUTO' or a numeric
        value that is the gain in decibels.
        """
        if self.auto_gain:
            return 'AUTO'
        else:
            return '{0:0.1f}'.format(self.sdr.get_gain())

    def set_gain(self, gain_db):
        """Set gain of tuner.  Can be the string 'AUTO' for automatic gain
        or a numeric value in decibels for fixed gain.
        """
        if gain_db == 'AUTO':
            self.sdr.set_manual_gain_enabled(False)
            self.auto_gain = True
            self._clear_intensity()
        else:
            try:
                self.sdr.set_gain(float(gain_db))
                self.auto_gain = False
                self._clear_intensity()
            except IOError:
                # Error setting value, ignore it for now but in the future consider
                # adding an error message dialog.
                pass

    def get_min_string(self):
        """Return string with the appropriate minimum intensity value, either
        'AUTO' or the min intensity in decibels (rounded to no decimals).
        """
        if self.min_auto_scale:
            return 'AUTO'
        else:
            return '{0:0.0f}'.format(self.min_intensity)

    def set_min_intensity(self, intensity):
        """Set Y axis minimum intensity in decibels (i.e. dB value at bottom of
        spectrograms).  Can also pass 'AUTO' to enable auto scaling of value.
        """
        if intensity == 'AUTO':
            self.min_auto_scale = True
        else:
            self.min_auto_scale = False
            self.min_intensity = float(intensity)
        self._clear_intensity()

    def get_max_string(self):
        """Return string with the appropriate maximum intensity value, either
        'AUTO' or the min intensity in decibels (rounded to no decimals).
        """
        if self.max_auto_scale:
            return 'AUTO'
        else:
            return '{0:0.0f}'.format(self.max_intensity)

    def set_max_intensity(self, intensity):
        """Set Y axis maximum intensity in decibels (i.e. dB value at top of
        spectrograms).  Can also pass 'AUTO' to enable auto scaling of value.
        """
        if intensity == 'AUTO':
            self.max_auto_scale = True
        else:
            self.max_auto_scale = False
            self.max_intensity = float(intensity)
        self._clear_intensity()

    # Added from https://stackoverflow.com/questions/20618804/how-to-smooth-a-curve-in-the-right-way
    def smooth(self, y, box_pts):
        box = np.ones(box_pts) / box_pts
        y_smooth = np.convolve(y, box, mode='same')
        return y_smooth

    def get_data(self, smooth=False):
        """Get spectrogram data from the tuner.  Will return width number of
        values which are the intensities of each frequency bucket (i.e. FFT of
        radio samples).
        """
        self.raw_data.append(self.get_fft())
        avg_factor = 4
        if smooth:
            avg_factor = 8
        while len(self.raw_data) > avg_factor:
            self.raw_data.pop(0)
        freqs = np.mean(np.array(self.raw_data), axis=0)

        # Update model's min and max intensities when auto scaling each value.
        if self.min_auto_scale:
            # Lower the display to near bottom of screen
            min_intensity = np.min(freqs)
            # min_intensity = int(np.average(freqs))
            if self.min_intensity is None:
                self.min_intensity = min_intensity
            elif self.min_intensity > min_intensity:
                self.min_intensity -= 0.1
            elif self.min_intensity < min_intensity:
                self.min_intensity += 0.1

        if self.max_auto_scale:
            max_intensity = np.max(freqs)
            if self.max_intensity is None:
                self.max_intensity = max_intensity
            elif self.max_intensity > max_intensity:
                self.max_intensity -= 0.1
            elif self.max_intensity < max_intensity:
                self.max_intensity += 0.1
        # Update intensity range (length between min and max intensity).
        self.range = self.max_intensity - self.min_intensity
        # Return frequency intensities.
        freqs = self.smooth(freqs, 2)
        return freqs

    def get_fft(self):
        # Get width number of raw samples so the number of frequency bins is
        # the same as the display width.  Add two because there will be mean/DC
        # values in the results which are ignored.
        # Added changes from
        freqbins = self.sdr.read_samples(SDR_SAMPLE_SIZE + 4)
        samples = freqbins * self.window
        a = pyfftw.empty_aligned(samples.shape, dtype='complex128', n=16)
        a[:] = samples
        # Run an FFT and take the absolute value to get frequency magnitudes.
        # freqs = np.absolute(np.fft.fft(samples))
        freqs = np.absolute(pyfftw.interfaces.numpy_fft.fft(a))
        # Ignore the mean/DC values at the ends.
        freqs = freqs[2:-2]
        # Shift FFT result positions to put center frequency in center.
        freqs = np.fft.fftshift(freqs)
        # Convert to decibels.
        freqs = 20.0 * np.log10(freqs)
        freqs = np.flip(freqs)

        # freqs = freqs.reshape(-1, 10).max(axis=1)
        if self.zoom_level < MAX_ZOOM_LEVEL:
            freqs = freqs.reshape(-1, 2 ** ((MAX_ZOOM_LEVEL) - self.zoom_level)).max(axis=1)

        middle = np.floor(len(freqs) / 2)
        start_element = int(middle - np.floor(self.width / 2))
        end_element = start_element + self.width
        freqs = freqs[start_element:end_element]
        # # Smooth Curve Display
        # freqs = self.smooth(freqs, 5)
        # self.print_time("get_fft")
        # self.print_time()
        return freqs

    def get_fft_from_file(self):
        if not self.file_data:
            self.file_data = self.load_file_data()
            self.file_data_idx = -1

        self.file_data_idx += 1
        if self.file_data_idx >= len(self.file_data):
            self.file_data_idx = 0

        return self.file_data[self.file_data_idx]

    def load_file_data(self):
        out = []
        for file_name in glob('data/fft-*'):
            out.append(np.load(file_name))

        return out

    def print_time(self, name=None):
        if name is not None:
            td = time.time() - self.last_time
            print("Time for %s is %s" % (name, td))
        else:
            print("-----------------------------------------------------")
        self.last_time = time.time()
