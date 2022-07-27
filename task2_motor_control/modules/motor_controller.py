import random

try:
    from .fake_gpio import GPIO  # For running app
except ImportError:
    from fake_gpio import GPIO  # For running main
from time import sleep


import RPi.GPIO as GPIO # For testing in Raspberry Pi
class MotorController(object):
    def __init__(self):
        self.working = False
        self.stopped = True
        self.position = ''

    def start_motor(self):
        self.working = True
        self.stopped = False
        self.PIN_STEP = 25  # do not change
        self.PIN_DIR = 8  # do not change
        self.clockwise_direction = 0
        # GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        self.counter_clockwise_direction = 1
        self.motor_rotation_per_step = 0.225  # given in raspberry pi guideline
        self.SPR_at_180 = int(180 / self.motor_rotation_per_step)  # 800 steps per resolution
        self.SPR_at_360 = int(360 / self.motor_rotation_per_step)  # 1600 steps per resolution
       
        GPIO.setup(self.PIN_DIR, GPIO.OUT)
        GPIO.setup(self.PIN_STEP, GPIO.OUT)
        print('Motor started')

        #### 180 clockwise
        self.anglemode = [self.SPR_at_180, self.SPR_at_360]
        self.angle_mode = random.choice(self.anglemode)
        self.dirmode = [self.clockwise_direction, self.counter_clockwise_direction]
        self.dir_mode = random.choice(self.dirmode)
        
        if self.angle_mode == self.SPR_at_180 and self.dir_mode == self.clockwise_direction:
            self.position = '180 degree in clockwise direction'
        elif self.angle_mode == self.SPR_at_180 and self.dir_mode == self.counter_clockwise_direction:
            self.position = '180 degree in counter-clockwise direction'
        elif self.angle_mode == self.SPR_at_360 and self.dir_mode == self.clockwise_direction:
            self.position = '360 degree in clockwise direction'
        elif self.angle_mode == self.SPR_at_360 and self.dir_mode == self.counter_clockwise_direction:
            self.position = '360 degree in counter-clockwise direction'

        GPIO.output(self.PIN_DIR, self.dir_mode)
        for x in range(self.angle_mode):
            GPIO.output(self.PIN_STEP, GPIO.HIGH)  # these two pins GPIO.HIGH AND GPIO.LOW will provide a pulse
            sleep(0.002)  # sleep time will be calculated by this formula f=1/t
            GPIO.output(self.PIN_STEP, GPIO.LOW)  # now we have to find the frequency i.e f=1600/60=26.666
            print (self.angle_mode-x)
            if self.stopped == True:
                break
        self.working = False
        print("Motor is stopped")

    def stop_motor(self):
        self.stopped = True
        self.working = False

    def what_position(self):
        return self.position

    def is_working(self):
        return self.working
