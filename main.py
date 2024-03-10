from fastapi import FastAPI
from typing import List
from pydantic import BaseModel


app = FastAPI()

lights_dict = {
    1: 'off',
    2: 'off',
    3: 'off',
    4: 'off',
}

# Pydantic model for the request body
class ProcessRequest(BaseModel):
    status: str
    lights_list: List[int] = [4,3,2,1]

    def updateLightsDict(self):
        if self.status=='on':
            for l in self.lights_list:
                lights_dict[l] = 'on'
        elif self.status=='off':
            for l in self.lights_list:
                lights_dict[l] = 'off'

@app.get("/")
def get_dict():
    return lights_dict

from homelightsrf.LightsManager import LightsManager as lm
_lm = lm()


# Endpoint to receive a list via POST request
@app.post("/lights/")
def turn_lights(data: ProcessRequest):
    if data.status=='on':
        _lm.turnOn(data.lights_list)
        data.updateLightsDict()
    elif data.status=='off':
        _lm.turnOff(data.lights_list)
        data.updateLightsDict()

    return lights_dict

