# coding=utf-8
__author__ = 'Qyon'

try:
    import Hamlib
except:
    Hamlib = None

if Hamlib:
    MODE_MAP = {
        'FM': Hamlib.RIG_MODE_FM,
        'AM': Hamlib.RIG_MODE_AM,
        'USB': Hamlib.RIG_MODE_USB,
        'LSB': Hamlib.RIG_MODE_LSB,
        'CW': Hamlib.RIG_MODE_CW,
        'CWR': Hamlib.RIG_MODE_CWR,
    }


class RigController(object):
    def __init__(self, serial_device, serial_speed, rig_id) -> None:
        super().__init__()
        self.rig_id = rig_id
        self.serial_speed = serial_speed
        self.serial_device = serial_device
        self.rig = None
        if Hamlib:
            Hamlib.rig_set_debug(Hamlib.RIG_DEBUG_NONE)
            #            Hamlib.rig_set_debug(Hamlib.RIG_DEBUG_TRACE)
            rig = Hamlib.Rig(120)
            rig.state.rigport.pathname = '/dev/ttyAMA0'
            rig.state.rigport.parm.serial.rate = 9600
            rig.open()
            self.rig = rig

    def set_frequency(self, freqency):
        if self.rig:
            freq = freqency * 1e6
            self.rig.set_freq(Hamlib.RIG_VFO_CURR, int(freq))

    def get_frequency(self):
        if self.rig:
            freq = self.rig.get_freq() / 1e6
        else:
            freq = 0
        return freq

    def set_mode(self, mode_name):
        if self.rig:
            response = self.rig.set_mode(MODE_MAP.get(mode_name, Hamlib.RIG_MODE_USB))
