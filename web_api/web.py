from flask import Flask, make_response
import pigpio

app = Flask(__name__)

# Access-Control-Allow-Origin *

pi = pigpio.pi() # Connect to local Pi.
pi.set_mode(21, pigpio.INPUT)

@app.route('/')
def index():
    return 'Flaska se hlasi!'

@app.route('/motor/<motor_id>/')
def motor(motor_id):
    return 'Motor {}'.format(motor_id)


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
