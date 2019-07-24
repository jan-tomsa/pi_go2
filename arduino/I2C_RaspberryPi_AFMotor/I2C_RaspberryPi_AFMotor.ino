// Wire Slave Receiver
// by Nicholas Zambetti <http://www.zambetti.com>

// Demonstrates use of the Wire library
// Receives data as an I2C/TWI slave device
// Refer to the "Wire Master Writer" example for use with this

// Created 29 March 2006

// This example code is in the public domain.

// 04-Feb-2018 mcarter adapted
#include <Wire.h>
#include <AFMotor.h>

AF_DCMotor motor1(1);
AF_DCMotor motor2(2);
AF_DCMotor motor3(3);
AF_DCMotor motor4(4);

volatile byte receivedBytes[8];
volatile boolean newDataReceived = false;

const int ledPin = 13; // onboard LED
static_assert(LOW == 0, "Expecting LOW to be 0");


String inputString = "";         // a String to hold incoming data
bool stringComplete = false;  // whether the string is complete


void setup() {
    Serial.begin(9600);           // set up Serial library at 9600 bps
    Serial.println("Motor test!");
    // reserve 200 bytes for the inputString:
    inputString.reserve(200);
    Wire.begin(0x8);                // join i2c bus with address #8
    Wire.onReceive(receiveEvent); // register event
    pinMode(ledPin, OUTPUT);
    digitalWrite(ledPin, LOW); // turn it off
    motor1.run(RELEASE);
    motor2.run(RELEASE);
    motor3.run(RELEASE);
    motor4.run(RELEASE);
}

void loop() {
    delay(100);
    // print the string when a newline arrives:
    if (stringComplete) {
      Serial.println(inputString);

      // .000.000.000.000
      // .000.000+255.000
      ////////////////////////////////////////////////////////////////////////////////////////////////////////
      newDataReceived = true;
      digitalWrite(ledPin, HIGH);
      byte recPos = 0;
      byte inPos=0;
      while (inPos<15) {
        char dir = inputString[inPos];
        //Serial.println(dir);
        receivedBytes[recPos] = (dir == '.' ? 0
                                            : (dir == '+' ? 1 : 2)
                                );
        recPos++;
        inPos++;
        //String num = ""+(char)inputString[inPos]+(char)inputString[inPos+1]+(char)inputString[inPos+2];
        int num = (((byte)inputString[inPos])-48)*100
                 +(((byte)inputString[inPos+1])-48)*10
                 +((byte)inputString[inPos+2])-48;
        //Serial.print("||");
        //Serial.print((char)inputString[inPos]);
        //Serial.print((byte)inputString[inPos]);
        //Serial.print(num);
        //Serial.println("||");
        receivedBytes[recPos] = num;//.toInt();
        inPos += 3;
        recPos++;
      }
      //for (byte i=0;i<8;i++) {
      //  Serial.println(receivedBytes[i]);
      //}

      // clear the string:
      inputString = "";
      stringComplete = false;
    }
    if (newDataReceived) {
        ///////////// Motor 1 //////////////
        byte dir1 = receivedBytes[0];
        byte speed1 = receivedBytes[1];
        motor1.setSpeed(speed1);
        if (dir1==0) {
          motor1.run(RELEASE);
          Serial.print("M1* ");
        } else {
            if (dir1==1) {
                motor1.run(FORWARD);
                Serial.print("M1+ ");
            } else {
                motor1.run(BACKWARD);
                Serial.print("M1- ");
            }
        }
        Serial.print(speed1);
        ///////////// Motor 2 //////////////
        byte dir2 = receivedBytes[2];
        byte speed2 = receivedBytes[3];
        motor2.setSpeed(speed2);
        if (dir2==0) {
          motor2.run(RELEASE);
          Serial.print("M2* ");
        } else {
            if (dir2==1) {
                motor2.run(FORWARD);
                Serial.print("M2+ ");
            } else {
                motor2.run(BACKWARD);
                Serial.print("M2- ");
            }
        }
        Serial.print(speed2);
        ///////////// Motor 3 //////////////
        byte dir3 = receivedBytes[4];
        byte speed3 = receivedBytes[5];
        motor3.setSpeed(speed3);
        if (dir3==0) {
          motor3.run(RELEASE);
          Serial.print("M3* ");
        } else {
            if (dir3==1) {
                motor3.run(FORWARD);
                Serial.print("M3+ ");
            } else {
                motor3.run(BACKWARD);
                Serial.print("M3- ");
            }
        }
        Serial.print(speed3);
        ///////////// Motor 4 //////////////
        byte dir4 = receivedBytes[6];
        byte speed4 = receivedBytes[7];
        motor4.setSpeed(speed4);
        if (dir4==0) {
          motor4.run(RELEASE);
          Serial.print("M4* ");
        } else {
            if (dir4==1) {
                motor4.run(FORWARD);
                Serial.print("M4+ ");
            } else {
                motor4.run(BACKWARD);
                Serial.print("M4- ");
            }
        }
        Serial.print(speed4);
        Serial.println("");
        newDataReceived = false;
        digitalWrite(ledPin, LOW); // turn it off
    }
}

// function that executes whenever data is received from master
// this function is registered as an event, see setup()
void receiveEvent(int howMany) {
    Wire.readBytes((uint8_t*)&receivedBytes, 8);
    newDataReceived = true;
    digitalWrite(ledPin, HIGH);
}



void serialEvent() {
  while (Serial.available()) {
    // get the new byte:
    char inChar = (char)Serial.read();
    // add it to the inputString:
    inputString += inChar;
    // if the incoming character is a newline, set a flag so the main loop can
    // do something about it:
    if (inChar == '\n') {
      stringComplete = true;
    }
  }
}











void serialEventXX() {
    char inputString[16];
    byte inputPos = 0;
    while (Serial.available()) {
      // get the new byte:
      char inChar = (char)Serial.read();
      // add it to the inputString:
      if (inputPos < 16) {
        inputString[inputPos] = inChar;
        inputPos++;
      }
    }
    byte recPos = 0;
    byte inPos=0;
    while (inPos<15) {
      char dir = inputString[inPos];
      receivedBytes[recPos] = (dir == '.' ? 0
                                          : (dir == '+' ? 1 : 2)
                              );
      recPos++;
      inPos++;
      String num = ""+(char)inputString[inPos]+(char)inputString[inPos+1]+(char)inputString[inPos+2];
      receivedBytes[recPos] = num.toInt();
      inPos += 3;
      recPos++;
    }
    newDataReceived = true;
    digitalWrite(ledPin, HIGH);
}
