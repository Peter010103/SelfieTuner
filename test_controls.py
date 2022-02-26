# %%

from picamera2 import *
picam2 = Picamera2()
preview_config = picam2.preview_configuration()
picam2.configure(preview_config)
picam2.set_controls({"AwbEnable": 0, "AeEnable": 0})
controls = picam2.list_controls()
print({k: v[-1] for k,v in controls.items()})