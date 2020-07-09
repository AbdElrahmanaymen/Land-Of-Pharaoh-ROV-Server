from flask import Flask, request, Response, session, stream_with_context
import cv2
import sys
import numpy
import requests
import serial

app = Flask(__name__)
app.secret_key = '2019'

#ser = serial.Serial('/dev/ttyUSB0', 9600)

@app.route('/')
def index():
    return "Hi this is the ROV winner's server :) just have fun"

def get_frame():
    camera_port=0
    camera=cv2.VideoCapture(camera_port) #this makes a web cam object

    while True:
        retval, im = camera.read()
        imgencode=cv2.imencode('.jpg',im)[1]
        stringData=imgencode.tostring()
        yield (b'--frame\r\n'
            b'Content-Type: text/plain\r\n\r\n'+stringData+b'\r\n')

    del(camera)

@app.route('/camera1')
def camera1():
     return Response(get_frame(),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/joystick')
def joystick():
    pass

@app.route('/joy', methods=["GET", "POST"])
def joy():  
    global joystick
    if request.method == 'POST':
        joystick = request.args.get("joystick")
        print(joystick)
        return '1'
    else:
        return joystick

def sendToArduino(data):
    #ser.write(data)
    pass

if __name__ == '__main__':
    app.run(threaded=True)
