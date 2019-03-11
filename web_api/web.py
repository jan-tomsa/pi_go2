from flask import Flask, make_response, request
import pigpio

app = Flask(__name__)

# Access-Control-Allow-Origin *

pi = pigpio.pi() # Connect to local Pi.
#pi.set_mode(21, pigpio.INPUT)

@app.route('/')
def index():
    return 'Flaska se hlasi!'

@app.route('/motor/<motor_id>/')
def motor(motor_id):
    return 'Motor {}'.format(motor_id)


@app.route('/set_mode/<int:pin_no>/')
def set_mode(pin_no):
    mode = request.args.get('mode')
    if (mode == 'INPUT'):
        pi.set_mode(pin_no, pigpio.INPUT)
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



@app.route('/test/')
def test():
    pi.write(21, 1) # on
    resp = make_response("Testing LED (GPIO #21) turned on")
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route('/test2/')
def test2():
    pi.write(21, 0) # off
    resp = make_response("Testing LED (GPIO #21) turned off")
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp
