#!/usr/bin/python3
import cv2
from qt_gl_preview import *
from picamera2 import *

face_detector = cv2.CascadeClassifier("/usr/local/lib/python3.9/dist-packages/cv2/data/haarcascade_frontalface_default.xml")

W = 1440
H = 1080

def draw_faces(request):
    stream = request.picam2.stream_map["main"]
    fb = request.request.buffers[stream]
    
    with fb.mmap(0) as b:
        im = np.array(b, copy=False, dtype=np.uint8).reshape((h0, w0, 4))
        for f in faces:
            (x, y, w, h) = [c * n // d for c, n, d in zip(f, (w0, h0) * 2, (w1, h1) * 2)]
            print(x+w/2, y+w/2)
            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0, 0))
            cv2.rectangle(im, (W/2, 0), (W/2, H), (255, 255, 254, 0))
        del im

    im2 = np.array(b, copy=False, dtype=np.uint8).reshape((H, W, 4))
    cv2.line(im2, (H/2, 0), (H/2, W), (255, 255, 254), 5)
    del im2

picam2 = Picamera2()
preview = QtGlPreview(picam2)
config = picam2.preview_configuration(main={"size": (W, H)},
                                      lores={"size": (W//2, H//2), "format": "YUV420"})
picam2.configure(config)

(w0, h0) = picam2.stream_configuration("main")["size"]
(w1, h1) = picam2.stream_configuration("lores")["size"]
s1 = picam2.stream_configuration("lores")["stride"]
faces = []

picam2.request_callback = draw_faces

picam2.start()

while True:
    buffer = picam2.capture_buffer("lores")
    grey = buffer[:s1*h1].reshape((h1, s1))
    faces = face_detector.detectMultiScale(grey, 1.1, 3)
