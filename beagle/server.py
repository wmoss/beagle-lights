#!/usr/bin/env python

from flask import Flask, request
from subprocess import call
from time import sleep
from threading import Lock


app = Flask("lights-and-fan-listener")

@app.route("/batch")
def batch():
    if 'fan' in request.args:
        fan()

    if 'lights' in request.args:
        lights()

    return "", 201

@app.route("/lights")
def lights():
    cycle_gpio(67)
    return "", 201

fan_pin_mapping = {
    0: 68,
    1: 44,
    2: 26,
    3: 46,
    4: 65
}
@app.route("/fan")
def fan():
    value = int(request.args['level'])
    assert 0 <= value and value <= 4, "value must be between 0 and 4"
    cycle_gpio(fan_pin_mapping[value])

    return "", 201

lock = Lock()
def cycle_gpio(pin):
    with lock:
        gpio_file = "/sys/class/gpio/gpio%s/value" % pin

        with open(gpio_file, "w") as fp:
            fp.write("1\n")
        sleep(1)

        with open(gpio_file, "w") as fp:
            fp.write("0\n")
        sleep(1)

def export_gpio_output(pin):
    with open("/sys/class/gpio/gpio%s/direction" % pin, "w") as fp:
        fp.write("out\n")

if __name__ == "__main__":
    for pin in (67, 68, 44, 26, 46, 65):
        export_gpio_output(pin)
    app.run(host="0.0.0.0")
