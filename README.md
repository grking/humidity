# Environmental Control

A quick hack to provide environmental control using a Raspberry Pi using an AM2302 temperature/humidity sensor.  The idea being a humidifier is hooked up to the output pin and the software will keep humidity within the given range.

Monitors the sensor, turns an output on/off at given humidity ranges and produces graphs for 1 hour, 24 hours and 7 days.

Run with:
```bash
sudo python control.py <GPIO input pin> <GPIO output pin>
```

For example:
```bash
sudo python control.py 17 18
```

Install dependencies with:
```bash
sudo ./setup
```

```
age: control.py [-h] [--humiditymin HUMIDITYMIN] [--humiditymax HUMIDITYMAX]
                  [--graphupdate GRAPHUPDATE] [--graphdir GRAPHDIR]
                  [--cycle CYCLE]
                  sensor_pin output_pin

Environment control

positional arguments:
  sensor_pin            The GPIO pin number which the AM2302 data line is
                        connected to
  output_pin            The GPIO pin number which the output is connected to

optional arguments:
  -h, --help            show this help message and exit
  --humiditymin HUMIDITYMIN
                        Minimum humidity in percent. Output goes high when
                        humidity falls to this level. (default: 95)
  --humiditymax HUMIDITYMAX
                        Maximum humidity in percent. Output goes low when
                        humidity rises to this level. (default: 95)
  --graphupdate GRAPHUPDATE
                        How often we generate graphs in seconds. (default: 60)
  --graphdir GRAPHDIR   Full pathname of directory into which graphs are
                        generated. (default: /var/www)
  --cycle CYCLE         Specifiy a humidity cycle:
                        minutes,min_humidity,max_humidity,[minutes,min,max]...
```

