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

Other options:
```bash
--humiditymin <min>     - Minimum humidity in percent (output pin goes high when lower than this)
--humiditymax <max>     - Maximum humidity in percent (output pin goes low when higher than this)
```

