# Picon Zero All Motors Test
# Press Ctrl-C to stop
#
# To check wiring is correct ensure the order of movement is correct

import piconzero as pz, time

#======================================================================
# Reading single character by forcing stdin to raw mode
import sys
import tty
import termios

def readchar():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    if ch == '0x03':
        raise KeyboardInterrupt
    return ch

def readkey(getchar_fn=None):
    getchar = getchar_fn or readchar
    c1 = getchar()
    if ord(c1) != 0x1b:
        return c1
    c2 = getchar()
    if ord(c2) != 0x5b:
        return c1
    c3 = getchar()
    return chr(0x10 + ord(c3) - 65)  # 16=Up, 17=Down, 18=Right, 19=Left arrows

# End of single character reading
#======================================================================

class PiconZeroMotor:
    #pico = null
    current_speed = 0
    def setPico(self,pico_):
        self.pico = pico_

    def getPico(self):
        return self.pico

    def incSpeed(self,delta):
        self.current_speed = max( min( self.current_speed+delta, 127), -127)
        self.setSpeed(self.current_speed)

    def getSpeed(self):
        return self.current_speed

    def forward(self):
        self.current_speed = abs(self.current_speed)
        self.setSpeed(self.current_speed)

    def reverse(self):
        self.current_speed = -abs(self.current_speed)
        self.setSpeed(self.current_speed)

# Motor driven by "standard" Picon Zero motor controls
class MMotor(PiconZeroMotor):
    mot_no = 0
    def __init__(self, pico_, mot_no_):
        self.setPico(pico_)
        self.mot_no = mot_no_

    def stop(self):
        #print("stop")
        self.getPico().setMotor(self.mot_no,0)

    def setSpeed(self,speed):
        #print("setSpeed()")
        self.getPico().setMotor(self.mot_no,speed)


OUTPUT_PWM = 1

# Motor driven by Picon Zero PWM (servo) controls
class PMotor(PiconZeroMotor):
    pin1 = 0
    pin2 = 0
    def __init__(self, pico_, pin1_, pin2_):
        self.setPico(pico_)
        self.pin1 = pin1_
        self.pin2 = pin2_
        self.getPico().setOutputConfig(self.pin1, OUTPUT_PWM)
        self.getPico().setOutputConfig(self.pin2, OUTPUT_PWM)

    def stop(self):
        #print("stop")
        self.getPico().setOutput(self.pin1, 0)
        self.getPico().setOutput(self.pin2, 0)

    def setSpeed(self,speed):
        if (speed>=0):
            pin1val = speed*2
            pin2val = 0
        if (speed<0):
            pin1val = 0
            pin2val = -speed*2
        print("P.setSpeed( {} <= {}, {} <= {} )".format( self.pin1, pin1val, self.pin2, pin2val ))
        self.getPico().setOutput(self.pin1, pin1val)
        self.getPico().setOutput(self.pin2, pin2val)

speed = 60

print "Tests the motors by using the keys to control"
print "Use following keys to control various motors"
print
print "Motor # | backwards | forward | speed up  | slow down |"
print "--------+-----------+---------+-----------+-----------+"
print "    1   |    q      |  w      |    a      |    z      |"
print "    2   |     e     |   r     |     d     |     c     |"
print "    3   |      t    |    y    |      g    |      b    |"
print "    4   |       u   |     i   |       j   |       m   |"
print "    5   |        o  |      p  |        l  |        .  |"
print
print "Press Ctrl-C to end"
print

pz.init()

motor1 = MMotor( pz, 1 )
motor2 = MMotor( pz, 0 )
motor3 = PMotor( pz, 5, 4 )
motor4 = PMotor( pz, 3, 2 )
motor5 = PMotor( pz, 1, 0 )

# main loop
try:
    while True:
        keyp = readkey()
        print "Key pressed: '{}'".format(keyp)
        # motor1
        if keyp == 'q':
            motor1.reverse()
            print 'M1 reverse ', motor1.getSpeed()
        elif keyp == 'w':
            motor1.forward()
            print 'M1 forward ', motor1.getSpeed()
        elif keyp == 'a':
            motor1.incSpeed(10)
            print 'M1 +speed: ', motor1.getSpeed()
        elif keyp == 'z':
            motor1.incSpeed(-10)
            print 'M1 -speed: ', motor1.getSpeed()
        # motor2
        if keyp == 'e':
            motor2.reverse()
            print 'M2 reverse ', motor2.getSpeed()
        elif keyp == 'r':
            motor2.forward()
            print 'M2 forward ', motor2.getSpeed()
        elif keyp == 'd':
            motor2.incSpeed(10)
            print 'M2 +speed: ', motor2.getSpeed()
        elif keyp == 'c':
            motor2.incSpeed(-10)
            print 'M2 -speed: ', motor2.getSpeed()
        # motor3
        if keyp == 't':
            motor3.reverse()
            print 'M3 reverse ', motor3.getSpeed()
        elif keyp == 'y':
            motor3.forward()
            print 'M3 forward ', motor3.getSpeed()
        elif keyp == 'g':
            motor3.incSpeed(10)
            print 'M3 +speed: ', motor3.getSpeed()
        elif keyp == 'b':
            motor3.incSpeed(-10)
            print 'M3 -speed: ', motor3.getSpeed()
        # motor4
        if keyp == 'u':
            motor4.reverse()
            print 'M4 reverse ', motor4.getSpeed()
        elif keyp == 'i':
            motor4.forward()
            print 'M4 forward ', motor4.getSpeed()
        elif keyp == 'j':
            motor4.incSpeed(10)
            print 'M4 +speed: ', motor4.getSpeed()
        elif keyp == 'm':
            motor4.incSpeed(-10)
            print 'M4 -speed: ', motor4.getSpeed()
        # motor5
        if keyp == 'o':
            motor5.reverse()
            print 'M5 reverse ', motor5.getSpeed()
        elif keyp == 'p':
            motor5.forward()
            print 'M5 forward ', motor5.getSpeed()
        elif keyp == 'l':
            motor5.incSpeed(10)
            print 'M5 +speed: ', motor5.getSpeed()
        elif keyp == '.':
            motor5.incSpeed(-10)
            print 'M5 -speed: ', motor5.getSpeed()
        # all motors
        elif keyp == ' ':
            motor1.stop()
            motor2.stop()
            motor3.stop()
            motor4.stop()
            motor5.stop()
            print 'Stop'
        elif ord(keyp) == 3:
            break

except KeyboardInterrupt:
    print

finally:
    pz.cleanup()
    
