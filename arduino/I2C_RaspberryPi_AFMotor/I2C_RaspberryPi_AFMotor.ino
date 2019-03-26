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

void setup() {
    Serial.begin(9600);           // set up Serial library at 9600 bps
    Serial.println("Motor test!");
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
    if (newDataReceived) {
        if (receivedBytes[0]==0) {
          motor1.setSpeed(receivedBytes[1]);
          motor1.run(FORWARD);
          Serial.print("M1+ ");
          Serial.print(receivedBytes[1]);
        } else {
          motor1.setSpeed(receivedBytes[1]);
          motor1.run(BACKWARD);
          Serial.print("M1- ");
          Serial.print(receivedBytes[1]);
        }
        if (receivedBytes[2]==0) {
          motor2.setSpeed(receivedBytes[3]);
          motor2.run(FORWARD);
          Serial.print("M2+ ");
          Serial.print(receivedBytes[3]);
        } else {
          motor2.setSpeed(receivedBytes[3]);
          motor2.run(BACKWARD);
          Serial.print("M2- ");
          Serial.print(receivedBytes[3]);
        }
        if (receivedBytes[4]==0) {
          motor3.setSpeed(receivedBytes[5]);
          motor3.run(FORWARD);
          Serial.print("M3+ ");
          Serial.print(receivedBytes[5]);
        } else {
          motor3.setSpeed(receivedBytes[5]);
          motor3.run(BACKWARD);
          Serial.print("M3- ");
          Serial.print(receivedBytes[5]);
        }
        if (receivedBytes[6]==0) {
          motor4.setSpeed(receivedBytes[7]);
          motor4.run(FORWARD);
          Serial.print("M4+ ");
          Serial.print(receivedBytes[7]);
        } else {
          motor4.setSpeed(receivedBytes[7]);
          motor4.run(BACKWARD);
          Serial.print("M4- ");
          Serial.print(receivedBytes[7]);
        }
        Serial.println("");
        newDataReceived = false;
    }
}

// function that executes whenever data is received from master
// this function is registered as an event, see setup()
void receiveEvent(int howMany) {
    Wire.readBytes((uint8_t*)&receivedBytes, 8);
    newDataReceived = true;
    digitalWrite(ledPin, HIGH);
}
