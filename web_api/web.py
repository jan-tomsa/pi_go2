#/usr/bin/python3
from flask import Flask, make_response, request
import pigpio
import piconzero as pz, time
from smbus import SMBus
import serial
import os
import threading

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


class AFMotorSet():
    bus = None
    comm_array = [0,0,0,0,0,0,0,0]
    def __init__(self, bus_):
        self.bus = bus_

    def setSpeed(self, mot_id, direction, speed):
        dir_i = 0
        if direction == 'STOP':
            dir_i = 0
        if direction == 'FORWARD':
            dir_i = 1
        if direction == 'BACKWARD':
            dir_i = 2
        self.comm_array[mot_id*2] = dir_i
        self.comm_array[mot_id*2+1] = speed
        self.bus.write_i2c_block_data(addr,self.comm_array[0],self.comm_array[1:])

class AFMotor():
    direction = '.'
    speed = 0
    def setSpeed(self, direction_, speed_):
        self.direction = direction_
        self.speed = speed_
    def getCommStr(self):
        return '{}{:03}'.format(self.direction, self.speed)

class AFMotorSetSerial():
    ser = None
    motors = []
    def __init__(self, serial_port_path):
        self.ser = serial.Serial(serial_port_path, 9600) # Establish the connection on a specific port
        self.motors = [AFMotor(),  AFMotor(),   AFMotor(),  AFMotor()]

    def setSpeed(self, mot_id, direction, speed):
        dir_i = '.'
        if direction == 'STOP':
            dir_i = '.'
        if direction == 'FORWARD':
            dir_i = '+'
        if direction == 'BACKWARD':
            dir_i = '-'
        output_str = ""
        self.motors[mot_id].setSpeed(dir_i,speed)
        for m in self.motors:
            output_str += m.getCommStr()
        output_str += '\n'
        self.ser.write(output_str.encode())
        return output_str

app = Flask(__name__)

# Access-Control-Allow-Origin *

pi = pigpio.pi() # Connect to local Pi.
pz.init()  # maybe put into web api function?

motor1 = MMotor( pz, 1 )
motor2 = MMotor( pz, 0 )
motor3 = PMotor( pz, 5, 4 )
motor4 = PMotor( pz, 3, 2 )
motor5 = PMotor( pz, 1, 0 )

motors = [motor1,motor2,motor3,motor4,motor5]

addr = 0x8 # bus address
bus = SMBus(1) # indicates /dev/ic2-1

USB_PATH1 = '/dev/ttyUSB0'
USB_PATH2 = '/dev/ttyUSB1'
usb1_exists = os.path.exists(USB_PATH1)
usb2_exists = os.path.exists(USB_PATH2)
if usb1_exists:
    af_motor_set = AFMotorSetSerial(USB_PATH1)
if usb2_exists:
    af_motor_set = AFMotorSetSerial(USB_PATH2)

if (not usb1_exists and not usb2_exists):
    af_motor_set = AFMotorSet(bus)

@app.route('/')
def index():
    resp = make_response('PiGO 2 web module testing message!')
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route('/afmotor/<int:motor_id>/')
def afmotor(motor_id):
    direction = request.args.get('dir')
    speedArg = request.args.get('speed')
    if speedArg is None:
        speed = 255
    else:
        speed = int(speedArg)
    timerArg = request.args.get('timer')  # in seconds
    if timerArg is not None:
        timer = int(timerArg)
        t = threading.Timer(timer, lambda : af_motor_set.setSpeed(motor_id-1,'STOP',0))
        t.start()
    else:
        timer = 0
    motor_response = af_motor_set.setSpeed(motor_id-1,direction,speed)
    resp = make_response('AFMotor {} - direction: {} speed: {}, comm: "{}", timer: {}'.format(motor_id,direction,speed,motor_response,timer))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route('/piconzero/<int:motor_id>/')
def piconzero(motor_id):
    speed = int(request.args.get('speed'))
    motors[motor_id-1].setSpeed(speed)
    resp = make_response('Motor {} - speed: {}'.format(motor_id,speed))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.route('/set_mode/<int:pin_no>/')
def set_mode(pin_no):
    mode = request.args.get('mode')
    if (mode == 'INPUT'):
        pi.set_mode(pin_no, pigpio.INPUT)
        pi.set_pull_up_down(pin_no, pigpio.PUD_UP)
    else:
        pi.set_mode(pin_no, pigpio.OUTPUT)
    resp = make_response('set_mode({},{})'.format(pin_no,mode))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route('/get_mode/<int:pin_no>/')
def get_mode(pin_no):
    mode = pi.get_mode(pin_no)
    resp = make_response('{}'.format(mode))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.route('/read/<int:pin_no>/')
def pin_read(pin_no):
    val = pi.read(pin_no)
    resp = make_response('{}'.format(val))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route('/write/<int:pin_no>/')
def pin_write(pin_no):
    val = int(request.args.get('val'))
    pi.write(pin_no, val)
    resp = make_response('Pin {} set to {}'.format(pin_no,val))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.route('/pwm/<int:gpio>/')
def pwm(gpio):
    val = int(request.args.get('val'))
    pi.set_PWM_dutycycle(gpio,val)
    resp = make_response('PWM {} set to {}'.format(gpio,val))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

