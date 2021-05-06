# coding=utf-8
__author__ = 'Qyon'

import json


class SettingsStore(object):
    def __init__(self, settings_file) -> None:
        super().__init__()
        self.settings_file = settings_file
        try:
            with open(self.settings_file, 'r') as f:
                self._settings = json.load(f)
        except:
            self._settings = {}

    def get(self, param_name, default=None):
        return self._settings.get(param_name, default)

    def set(self, param_name, value):
        self._settings[param_name] = value

    def save(self):
        with open(self.settings_file, 'w') as f:
            json.dump(self._settings, f, indent=4)
