from flask import Flask, make_response, request
import pigpio
import piconzero as pz, time

app = Flask(__name__)

# Access-Control-Allow-Origin *

pi = pigpio.pi() # Connect to local Pi.
pz.init()

motor1 = MMotor( pz, 1 )
motor2 = MMotor( pz, 0 )
motor3 = PMotor( pz, 5, 4 )
motor4 = PMotor( pz, 3, 2 )
motor5 = PMotor( pz, 1, 0 )

@app.route('/')
def index():
    return 'Flaska se hlasi!'

@app.route('/piconzero/<int:motor_id>/')
def motor(motor_id):
    direction = request.args.get('dir')
    speed = request.args.get('speed')
    return 'Motor {} - {} - speed: {}'.format(motor_id,direction,speed)


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

