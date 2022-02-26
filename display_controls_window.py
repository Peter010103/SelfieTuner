from curses import window
import cv2
import json

# from picamera2 import *
# from null_preview import *
from functools import partial

# picam2 = Picamera2()
# preview = NullPreview(picam2)
# picam2.configure(picam2.preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)}))
# picam2.start()

# controls = picam2.list_controls()
# controls = {k: v[-1] for k,v in controls.items()}
controls_bounds = json.load(open('./controls.json'))

# def on_change_sharpness(value):
#   param = "Sharpness"
#   controlVal = trackbarVal_to_controlVal(*controls_bounds[param][:2], value)
#   picam2.set_controls({
#     param: controlVal
#   })
#   print(value)

def controlVal_to_trackbarVal(min, max, controlVal):
  """Return number between 0 and 100"""
  # NOTE: this assumes we are working with ints
  return int(100 * (controlVal - min) / (max - min))

def trackbarVal_to_controlVal(min_val, max_val, trackbarVal):
  """Convert trackbar value to data within bounds of controlVal"""
  print(min_val, max_val, trackbarVal)
  control_val_type = type(min_val)
  
  if control_val_type == int:
    if max_val < 100:
      val = trackbarVal
    else:
      val = min_val + (max_val - min_val) * trackbarVal / 100

  elif control_val_type == float:
    if (max_val - min_val) < 10 or (max_val - min_val) > 100:
      val = min_val + (max_val - min_val) * trackbarVal / 100
    else:
      val = trackbarVal
  
  print(val)
  return control_val_type(val)

def on_change(value, controlParam, picam2):
  # print(controlParam)
  controlVal = trackbarVal_to_controlVal(*controls_bounds[controlParam][:2], value)
  picam2.set_controls({controlParam: controlVal})
  print(value)

def make_trackbars(windowName, control_bounds, cam):
  """Routine to make trackbars from a dictionary of controls"""
  # print(control_bounds)
  for control_param,v in control_bounds.items():
    min_val, max_val, default_val = v
    # INT or FLOAT trackbar
    if type(min_val) == int:
      cv2.createTrackbar(control_param, windowName, \
        controlVal_to_trackbarVal(*control_bounds[control_param]), \
        # min(max_val, 100), lambda x: on_change(x, control_param))
        min(max_val, 100), partial(on_change, controlParam=control_param, picam2=cam))
    
    # float
    if type(min_val) == float:
      track_bar_upper_bound = max_val
      if (max_val - min_val) < 10 or (max_val - min_val) > 100:
        track_bar_upper_bound = 100
      cv2.createTrackbar(control_param, windowName, \
        controlVal_to_trackbarVal(*control_bounds[control_param]), \
        # int(max_val), lambda x: on_change(x, control_param))
        int(track_bar_upper_bound), partial(on_change, controlParam=control_param, picam2=cam))

# windowName = 'Control Params'
# cv2.namedWindow(windowName, cv2.WINDOW_NORMAL)
# cv2.createTrackbar('Sharpness', windowName, \
#   controlVal_to_trackbarVal(*controls_bounds["Sharpness"]), 100, \
#   lambda x: on_change(x, 'Sharpness'))

# control_param = "NoiseReductionMode"
# cv2.createTrackbar(control_param, windowName, \
#   controlVal_to_trackbarVal(*controls_bounds[control_param]), 100, \
#   lambda x: on_change(x, control_param))

# make_trackbars(controls_bounds)

# while True:
#   im = picam2.capture_array()

#   # grey = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
#   # faces = face_detector.detectMultiScale(grey, 1.1, 5)

#   # for (x, y, w, h) in faces:
#   #     cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0))

#   cv2.imshow("Vid", im)
  # if cv2.waitKey(30) == ord('q'):
  #   break


# cv2.waitKey(0)
cv2.destroyAllWindows()

# img = cv2.imread('./screenshot.png')
# img = cv2.resize(img, (960, 540))
 

# # cv2.namedWindow(windowName, cv2.WINDOW_NORMAL)
# cv2.imshow(windowName, img)

 
# cv2.waitKey(0)
