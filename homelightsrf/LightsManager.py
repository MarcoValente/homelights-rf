from pydantic import BaseModel
from typing import List, Dict
import logging as log
from rpi_rf import RFDevice

from RPi import GPIO
GPIO.setwarnings(False)

# Variables to use in commands
_lights_vars = {
    1: {
        'on' : {
            'tx_pulselength' : 190,
            'tx_proto' : 1,
            'repeat' : 100,
            'tx_length' : None,
            'code' : 7208572,
        },
        'off' : {
            'tx_pulselength' : 190,
            'tx_proto' : 1,
            'repeat' : 10,
            'tx_length' : None,
            'code' : 7208564,
        },
    },
    2: {
        'on' : {
            'tx_pulselength' : 190,
            'tx_proto' : 1,
            'repeat' : 10,
            'tx_length' : None,
            'code' : 7208570,
        },
        'off' : {
            'tx_pulselength' : 190,
            'tx_proto' : 1,
            'repeat' : 10,
            'tx_length' : None,
            'code' : 7208562,
        },
    },
    3: {
        'on' : {
            'tx_pulselength' : 190,
            'tx_proto' : 1,
            'repeat' : 10,
            'tx_length' : None,
            'code' : 7208569,
        },
        'off' : {
            'tx_pulselength' : 191,
            'tx_proto' : 1,
            'repeat' : 10,
            'tx_length' : None,
            'code' : 7208561,
        },
    },
    4: {
        'on' : {
            'tx_pulselength' : 192,
            'tx_proto' : 1,
            'repeat' : 10,
            'tx_length' : None,
            'code' : 7208573,
        },
        'off' : {
            'tx_pulselength' : 190,
            'tx_proto' : 1,
            'repeat' : 10,
            'tx_length' : None,
            'code' : 7208565,
        },
    },
    5: {
        'on' : {
            'tx_pulselength' : 192,
            'tx_proto' : 1,
            'repeat' : 10,
            'tx_length' : None,
            'code' : 7208563,
        },
        'off' : {
            'tx_pulselength' : 191,
            'tx_proto' : 1,
            'repeat' : 10,
            'tx_length' : None,
            'code' : 7208571,
        },
    },
}

# These are the GPIOS on the raspberry pi with configured transmitters
_gpios = [17, 22]

class LightsManager(BaseModel):
    lights_vars: dict = _lights_vars
    dry_run: bool = False
    rf_devices: list = [RFDevice(gpio) for gpio in _gpios]

    def turnOn(self, lights : List[int] = [4,3,2,1]):
        return self._turn(True,lights)
    
    def turnOff(self, lights : List[int] = [4,3,2,1]):
        return self._turn(False,lights)

    def _turn(self, on : bool, lights : List[int]):
        on_str = 'on' if on else 'off'
        log.info(f'Turning {on_str} lights {lights}')
        for l in lights:
            self._turnLight(on,l)

    def _enableTx(self):
        for rfd in self.rf_devices: rfd.enable_tx()

    def _turnLight(self, on : bool, light : int):
        on_str = 'on' if on else 'off'
        log.info(f'Turning {on_str} light {light}')

        cmd_vars = dict(self.lights_vars[light][on_str])
        log.debug(f'Command vars = {cmd_vars}')

        if not self.dry_run:
            self._enableTx()
            for rfd in self.rf_devices: 
                rfd.tx_repeat = cmd_vars['repeat']
                tmp_cmd_vars = dict(cmd_vars)
                del tmp_cmd_vars['repeat']
                rfd.tx_code(**tmp_cmd_vars)