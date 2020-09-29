mysql = dict(
    user = 'user',
    password = 'pass',
    db = 'mydb',
    host = 'localhost'
)

android_devices = dict(
    indoor_dev = '/dev/serial/by-id/usb-Arduino__www.arduino.cc__0043_75735303431351305180-if00',
    outdoor_dev = '/dev/serial/by-id/usb-Arduino_LLC_Arduino_Leonardo-if00',
)

cameras = dict(
    indoor_cam_1 = '/dev/v4l/by-id/usb-0c45_USB_camera-video-index0',
    indoor_cam_2 = '/dev/v4l/by-id/usb-USB_2.0_Camera_USB_2.0_Camera_SN0001-video-index0',
    outdoor_cam = '/dev/v4l/by-id/usb-Generic_USB2.0_PC_CAMERA-video-index0',
)

webserver = '/var/www/html/data'
