import serial.tools.list_ports
import csv

list = serial.tools.list_ports.grep('VID:PID=2341:0043','hwid')
connected=[]
for elements in list:
    connected.append(elements.device)
baud = 9600

arduino = serial.Serial(connected[0], baudrate=baud, timeout = 1)
arduino.close()
arduino.open()

filename = "data/deployed/30mA.csv"

with open (filename,'w') as f:
    f.write("rth,pd_Ref,pd_Etl,Ratio, loop_Error,Pout,Iout,Dout, PID_Out,DAC_Out, DAC_set\n")
    f.close()

while True:
    with open (filename,'a') as f:
        try:
            line = arduino.readline().decode("utf-8")
            print(line.rstrip('\n'))
            f.write(line.rstrip("\n"))

        except:
            print("ehh, error!!!")
        