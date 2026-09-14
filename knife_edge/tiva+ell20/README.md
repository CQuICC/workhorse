# knife_edge
Knife Edge experiment for beam waist measurement. The setup uses TI Tiva C series TM4C123GXL eval board (PIN PE_3) for ADC (Max voltage 3.3V, 12 bit). 

The linear stage is Thorlabs ELL20K/M. An example for this is shown in ``` https://github.com/CQuICC/equipment_automation ```



Contents: 

* Serial_control : Energia program for TIVA. Prints 10 ADC readings for each command. 
* main_control.py : Controls linear stage, collects ADC data and writes it in a file. 
* analysis.ipynb : Plots the collected ADC data, and fits it to error function, and draws corresponding gaussian waveform. 
