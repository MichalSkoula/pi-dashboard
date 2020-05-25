mysql = dict(
    user = 'user',
    password = 'pass',
    db = 'mydb',
    host = 'localhost'
)

ssh = dict(
    user = 'sshuser',
    host = '1.2.3.4',
    password = 'sshpass',
    remote_path = '/var/www/clients/client0/web116/web/data/',
    local_path = '/home/pi/cron/data/'
)

android_devices = dict(
    indoor_dev = '/dev/serial/by-id/usb-Arduino__www.arduino.cc__0043_75735303431351305180-if00',
    outdoor_dev = '/dev/serial/by-id/usb-Arduino_LLC_Arduino_Leonardo-if00',
)

cameras = dict(
    indoor_cam = '/dev/v4l/by-id/usb-0c45_USB_camera-video-index0',
    outdoor_cam = '/dev/v4l/by-id/usb-Generic_USB2.0_PC_CAMERA-video-index0',
)

