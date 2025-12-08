# Python KlikAanKlikUit ICS-2000 library
This library gives methods to control a ICS-2000 from KlikAanKlikUit. It is made to add support for this device within Home assistant, which implementation is available in [this](https://github.com/zefanjajobse/ics-2000-home-assistant) repository.

## Usage example:
```py
from ics_2000.entities.dim_device import DimDevice
from ics_2000.entities.switch_device import SwitchDevice
from ics_2000.hub import Hub

hub = Hub("example@email.com", "password")
homes = hub.login()  # Authenticate
print(homes) # returns a dictionary of homes, ex: {"0": "test home}
hub.select_home("132829") # Select the right home by id
hub.get_devices() # request devices
for device in hub.devices:
    if type(device) is SwitchDevice or type(device) is DimDevice:
        print(device.name)
        if device.get_on_status(): # returns bool
            device.turn_off(False) # turn a device off
```