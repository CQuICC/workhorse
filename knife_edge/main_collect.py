# Author: Ashutosh Singh
# Desc: Collect data from Tiva. The hardware is tied using hardware ID
#	to be used with Linear Stage ELL20K/M	
import numpy as np
import serial.tools.list_ports
import time
import elliptec

list = serial.tools.list_ports.grep("VID:PID=1cbe:00fd", 'hwid')
connected = []
for element in list:
    connected.append(element.device)
print("Tiva board at: ",connected)
baudrate=115200
tiva = serial.Serial(connected[0], baudrate, timeout=2)

another_list = serial.tools.list_ports.grep("VID:PID=0403:6015", 'hwid')
connected2=[]
for element in another_list:
    connected2.append(element.device)
print("Linear stage at: ", connected2)

    
controller = elliptec.Controller(connected2[0])
ls = elliptec.Linear(controller)
ls.home()
time.sleep(1)

#tiva.open()
tiva.flush()
x = np.linspace(50,58,51)
f = open(f"data/run_{time.time()}.txt", "w")

header = "distance"
header_addon = lambda a: f",read_{a}"

for i in range(10):
    header = header+header_addon(i)
f.write(header + '\n')


for distance in x:
    ls.set_distance(distance)
    f.write(str(distance) + ",")
    time.sleep(0.5)
    command = "#"
    tiva.write(command.encode())
    out=""
    flag=""
    while (flag!=b'@'):
        out = tiva.readline().strip(b'\r\n')
        f.write(out.decode()+",")
        print(out.decode())
        flag=out
    f.write("\n")
tiva.close()
f.close()
