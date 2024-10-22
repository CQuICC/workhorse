/*
* Author: Ashutosh Singh
* Description: PID controller for wavelength stabilisation of DFB laser diode. 
*
*/

#include "Wire.h"

#define rth A0
#define pd_Ref A1
#define pd_Etl A2
#define MCP4725_ADDR 0x60// I2C address
#define max_DAC 2400 // Corresponds to Max 3 V on the BJT

#define set_point 1 // Ratio of 1

const int numReadings = 20;   // Change data type if going over 32 readings average
int total =0;
int loop_Index_Reset = 0;
float PID_DAC_Out = 0;
float average = 0;

float rth_Avg = 0;
float pd_Ref_Avg = 0;
float pd_Etl_Avg = 0;


double ratio, output, loop_error, pre_error = 0, set_Point;   //PID Parameters
double Pout, Iout, Dout, PID_Output;
double dspSampleTime = 1; // Sampling time 1 s
const float errormin = 0.02;
double dac_output = 0, dac_Last = 0;

double Kp = 10, Ki = 0.01, Kd =0;   //PID Parameters


float average_ADC( int port); 
void dac_Write(int write_Value);
void PID_Control(int ratio);

void setup() {
delay(2000);
Serial.begin(9600);
Wire.begin();
set_Point = set_point;
}

void loop() {
delay (1000*dspSampleTime);
rth_Avg = average_ADC(rth);
pd_Ref_Avg = average_ADC(pd_Ref);
pd_Etl_Avg = average_ADC(pd_Etl);
ratio = pd_Etl_Avg / pd_Ref_Avg;
Serial.print(rth_Avg);
Serial.print(",");
Serial.print(pd_Ref_Avg);
Serial.print(",");
Serial.print(pd_Etl_Avg);
Serial.print(",");
// Serial.print("Ratio= ");
Serial.print(ratio);
Serial.print(",");
PID_Control(ratio);
}

void PID_Control(double ratio){
  if (isinf(ratio)){
      delay(2000);      // Delay for two seconds to account for laser to be turned ON
      ratio = set_Point;
  }
    

  loop_error = set_Point - ratio;
  if (abs(loop_error)< errormin){
    loop_error = 0;
  }
  // Serial.print("Loop Error =");
  Serial.print(loop_error);
  Serial.print(",");
  Pout = Kp*loop_error;
  Iout+=Ki*(loop_error + pre_error)*0.5*dspSampleTime;
  Dout+=Kd*(loop_error - pre_error)/dspSampleTime;
  PID_Output = Pout + Iout + Dout;
    // Serial.print("POut: ");
  Serial.print(Pout);
  Serial.print(",");
    // Serial.print("IOut: ");
  Serial.print(Iout);
  Serial.print(",");
    // Serial.print("Dout: ");
  Serial.print(Dout);
  Serial.print(",");
  // Serial.print("PID Out: ");
  Serial.print(PID_Output);
  Serial.print(",");

  // if (PID_Output < 0){
    PID_DAC_Out = dac_Last + PID_Output;
    dac_Write(PID_DAC_Out);    
    dac_Last = PID_DAC_Out;

  Serial.print(",");
  // Serial.print("DAC Set: ");
  Serial.println(PID_DAC_Out);
  pre_error = loop_error;
}



float average_ADC(int port){
  total = 0;
  average = 0;
  for (int i = 0; i< numReadings; i++)
  total += analogRead(port);
  average = total / numReadings;
  return average;
}


void dac_Write(int write_Value){
  int output = 0;
  if (write_Value > max_DAC){
    output = max_DAC;
    loop_Index_Reset++;
    if (loop_Index_Reset > 10){
      output = 570;
      delay(10000);
      loop_Index_Reset = 0;
    } 
  }
    
  else if (write_Value >= 0 && write_Value < max_DAC)
    output = write_Value+570; // 0.7 V offset
  
  // Serial.print("DAC Out: ");
  Serial.print(output);
  int MSB = int(output /256)& 0x0F;
  int LSB = int(output & 0xFF);
  Wire.beginTransmission(MCP4725_ADDR);
  Wire.write(MSB);        // the 4 most significant bits.
  Wire.write(LSB);        // the 8 least significant bits.
  Wire.endTransmission();
}