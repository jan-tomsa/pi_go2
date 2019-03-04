from flask import Flask
import pigpio

app = Flask(__name__)

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
    return 'Testing LED (GPIO #21) turned on'

@app.route('/test2/')
def test2():
    pi.write(21, 0) # off
    return 'Testing LED (GPIO #21) turned off'
