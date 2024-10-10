from flask import Flask, render_template, Response, send_file, request
import cv2

import base64
import io
import numpy as np
from PIL import Image
import time
import json

app = Flask(__name__)

width: int = 1920
height: int = 1080

timer = time.time()
timer_ = 60*3
timer_run = False

camera: dict = {}
camera_f: dict = {}
a = False
def get_camera(id):
    global camera, a
    diffrent = ''
    dt = time.time()
    while True:
        if camera.get(id) != None:
            img = Image.open(io.BytesIO(base64.b64decode(camera[id].split(',')[1])))
            img = img.convert('RGB')

            img_io = io.BytesIO()
            img.save(img_io, 'JPEG', quality=60)
            img_io.seek(0)
            if camera[id] != diffrent:
                diffrent = camera[id]
                print(f'Change Time: {time.time()-dt}')
                dt = time.time()
            
            yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + img_io.read() + b'\r\n')

@app.route('/setting', methods=['GET', 'POST'])
def setting():
    global width, height, timer, timer_, timer_run
    if request.method == 'POST':
        #width, height = str(request.form['width']).split(' x ')
        #width, height = int(width), int(height)

        timer_ = int(request.form.get('timer',60*3))
        print('!!!!!!',int(request.form.get('reset', 0)))
        if int(request.form.get('reset', 0)) >= 1:
            timer = time.time()
        a = int(request.form.get('run', 0))
        if a == 1:
            timer_run = True
        elif a == 2:
            timer_run = False
        elif a == 3:
            timer_run = not timer_run
            timer_ = timer = time.time()
            

    return render_template('setting.html', width=width, height=height, timer=timer_)

@app.route('/')
def mainmenu():
    return render_template('mainmenu.html', camera_len=(len(camera)), time=time.time, timer=timer)

@app.route('/test_camera/<int:id>')
def test_camera(id):
    return Response(get_camera(id), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/camera')
def camera_page():
    return camera[1]

@app.route('/get')
def get():
    if request.args['type'] == 'size':
        return json.dumps({'width': width, 'height': height})
    elif request.args['type'] == 'time':
        return json.dumps({'time':time.time(), 'timer': timer_, 'dt': timer, 'run': timer_run})

@app.route('/camera/<int:id>', methods=['GET', 'POST'])
def camera_live(id):
    global camera
    if request.method == 'GET':
        return render_template('camera_get.html', id=id, size=(width, height))
    else:
        camera[id] = request.form['camera']
        return '.'

@app.route('/file/<path:path>')
def file(path):
    return send_file(f'./file/{path}')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True,ssl_context=('cert.pem', 'key.pem')) 