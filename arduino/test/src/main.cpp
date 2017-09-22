
#include "Arduino.h"

#define DIR1 2
#define DIR2 3
#define PWM_PIN 5



class Motor{
};

struct RobotIo {
  // switchs
  int sw1, sw2, sw3, sw4;
  int sw1_pin, sw2_pin, sw3_pin, sw4_pin;
  
  // ir
  int ir_lis[4];
  int ir_pin_lis[] = {};
  
  // line
  // motor_pwms
  // serial
};

int val = 0;
int now = 0;




void setup() {
  // initialize digital pin LED_BUILTIN as an output.

  pinMode(17, INPUT);

  Serial.begin(9600);

}

void loop() {
  
  now = digitalRead(17);  
  val = analogRead(16);

  Serial.print("analog:" + String(val) + "  digital:"+String(now) + "\n");


  delay(300);               
}




/*
  val = 256*sin(now*0.01);
  
  analogWrite(PWM_PIN, abs(val));

  if (val<0){
    digitalWrite(DIR1, 0);
    digitalWrite(DIR2, 1);
  }else if (val>0){
    digitalWrite(DIR1, 1);
    digitalWrite(DIR2, 0);
  }
  Serial.print("val:" + String(val) + "\n");

  now++;
*/





