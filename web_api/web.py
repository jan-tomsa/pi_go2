from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return 'Flaska se hlasi!'

@app.route('/motor/<motor_id>/')
def motor(motor_id):
    return 'Motor {}'.format(motor_id)
