#!/usr/bin/python3

import cv2

from qt_gl_preview import *
from picamera2 import *

# This version creates a lores YUV stream, extracts the Y channel and runs the face
# detector directly on that. We use the supplied OpenGL accelerated preview window
# and delegate the face box drawing to its callback function, thereby running the
# preview at the full rate with face updates as and when they are ready.

face_detector = cv2.CascadeClassifier("/usr/local/lib/python3.9/dist-packages/cv2/data/haarcascade_frontalface_default.xml")

moves = {
  "right": "Move right!",
  "left": "Move left!",
  "up": "Move up!",
  "down": "Move down!",
  "nice": "Nice!"
}

v_deadband = 20
h_deadband = 20

h_ref = 320
v_ref = 100

def draw_faces(request):
    cw = 0
    ch = 0
    instructions = []
    stream = request.picam2.stream_map["main"]
    fb = request.request.buffers[stream]
    with fb.mmap(0) as b:
        im = np.array(b, copy=False, dtype=np.uint8).reshape((h0, w0, 4))
        for f in faces:
            (x, y, w, h) = [c * n // d for c, n, d in zip(f, (w0, h0) * 2, (w1, h1) * 2)]
            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0, 0))
            
            cw = x + w//2
            ch = y + h//2

        font = cv2.FONT_HERSHEY_SIMPLEX

        if (cw < h_ref - h_deadband):
            instructions.append(moves["right"])
        elif (cw > h_ref + h_deadband):
            instructions.append(moves["left"])

        if (ch < v_ref - h_deadband):
            instructions.append(moves["down"])
        elif (ch > v_ref + h_deadband):
            instructions.append(moves["up"])
        
        
        if (len(instructions) == 0):
            instructions.append(moves["nice"])

        if (len(faces) == 1):
          for idx, text in enumerate(instructions):
            cv2.putText(im, text, (50, 340 + idx*50), font, 0.8, (0, 255, 255), 2)
          
        cv2.line(im, (h_ref, 0), (h_ref, 480), (225, 193, 110), 1)  
        cv2.line(im, (0, v_ref), (640, v_ref), (225, 193, 110), 1)   

        del im

picam2 = Picamera2()
preview = QtGlPreview(picam2)
config = picam2.preview_configuration(main={"size": (640, 480)},
                                      lores={"size": (320, 240), "format": "YUV420"})
picam2.configure(config)

(w0, h0) = picam2.stream_configuration("main")["size"]
(w1, h1) = picam2.stream_configuration("lores")["size"]
s1 = picam2.stream_configuration("lores")["stride"]
faces = []

picam2.request_callback = draw_faces

picam2.start()

import json
import display_controls_window
controls_bounds = json.load(open('./controls.json'))
windowName = 'Control Params'
cv2.namedWindow(windowName, cv2.WINDOW_NORMAL) 
display_controls_window.make_trackbars(windowName, controls_bounds, picam2)


while True:
    buffer = picam2.capture_buffer("lores")
    grey = buffer[:s1*h1].reshape((h1, s1))
    faces = face_detector.detectMultiScale(grey, 1.1, 3)

    cv2.imshow("Camera", buffer)
