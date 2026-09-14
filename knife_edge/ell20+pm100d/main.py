# Author: Ashutosh Singh
# Description: Uses the Thorlabs PM100D as a measurement sensor.
# This differs from the knife-edge setup, which uses a home-built TIA.
# The power meter communicates over SCPI. The linear-stage code is unchanged.


import csv
import time
from datetime import datetime
import elliptec
import numpy as np
import pyvisa
import serial.tools.list_ports


serial_port_list = serial.tools.list_ports.grep("VID:PID=0403:6015", "hwid")
connected1 = [element.device for element in serial_port_list]
print("Linear stage at: ", connected1)
controller = elliptec.Controller(connected1[0])


rm = pyvisa.ResourceManager('@py')
print(rm.list_resources())
instr = rm.open_resource(
    "USB0::4883::32888::P0044264::INSTR",
    timeout=10000,
)
print(instr.query("SYST:SENS:IDN?"))
instr.write("SENSE:POWER:UNIT W")
instr.write("SENSE:AVERAGE:COUNT 100")
print(instr.query("SENSE:AVERAGE:COUNT?"))
instr.write("SENSE:POWER:RANGE:AUTO ON")
print(instr.query("MEAS:POW?"))

ls = elliptec.Linear(controller)
ls.home()
time.sleep(1)

output_path = f"data/run_{datetime.now().strftime('%Y_%m_%d-%H_%M_%S')}.txt"

with open(output_path, "w", newline="") as output_file:
    writer = csv.writer(output_file)
    start = 0.0
    stop = 1.1
    num = 11
    avg_number = 50

    writer.writerow(["distance", *[f"read_{index}" for index in range(avg_number)]])

    distances = np.linspace(start, stop, num)

    for distance in distances:
        ls.set_distance(distance)
        time.sleep(0.5)

        readings = []
        for _ in range(avg_number):
            power = instr.query("MEAS:POW?").strip()
            readings.append(power)
            print(power)

        writer.writerow([distance, *readings])

instr.close()