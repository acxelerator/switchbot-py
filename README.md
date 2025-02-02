# switchbot-py
SwitchBot client for Python

# install

```shell
$ rye add switchbot_py --git=https://github.com/acxelerator/switchbot-py 
```

# usage


## initialize instance

```python
from switchbot_py import SwitchBot

token = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
secret = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

switchbot = SwitchBot(token=token, secret=secret)
```

## list devices and infrared remote devices

```python

for d in switchbot.devices():
    print(d)

Device(type=Motion Sensor, name=xx, device_id=XXXXXXXXXXXX)
Device(type=MeterPro(CO2), name=xx, device_id=XXXXXXXXXXXX)
Device(type=Meter, name=xx, device_id=XXXXXXXXXXXX)

for r in switchbot.infrared_remotes():
    print(r)

Remote(type=Air Conditioner, name=xxxx, device_id=xx-xxxxxxxxxxxx-xxxxxxxx)
Remote(type=Light, name=xxxx, device_id=xx-xxxxxxxxxxxx-xxxxxxxx)
```
