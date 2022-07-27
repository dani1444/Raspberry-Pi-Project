USE_FAKE_GPIO = False # Chage to FALSE if testing in the Raspberry Pi

#if USE_FAKE_GPIO:
    #from .fake_gpio import GPIO  # For running app
#else:
import RPi.GPIO as GPIO  # For testing in Raspberry Pi

import numpy as np
import time

class SensorController:

    def __init__(self):
        self.PIN_TRIGGER = 18  # do not change
        self.PIN_ECHO = 24  # do not change
        self.distance = None
        self.shape_dist = [False, False, False]
        print('Sensor controller initiated')

    def track_rod(self):
        consideration = []
        total_measurements = 10
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.PIN_ECHO, GPIO.IN)
        GPIO.setup(self.PIN_TRIGGER, GPIO.OUT)
        GPIO.output(self.PIN_TRIGGER, GPIO.LOW)
        print('Monitoring is started')
        for i in range(total_measurements):
            GPIO.output(self.PIN_TRIGGER, GPIO.HIGH)
            time.sleep(0.0001)
            GPIO.output(self.PIN_TRIGGER, GPIO.LOW)
            time.sleep(0.0001)
            starting_time = 0
            ending_time = 0
            while GPIO.input(self.PIN_ECHO) == 0:
                starting_time = time.time()
            while GPIO.input(self.PIN_ECHO) == 1:
                ending_time = time.time()
            time_period = None
            time_period = ending_time - starting_time
            d = 17150 * time_period
            calculated_distance = round(d, 2)
            print("Distance(cm): ", calculated_distance)
            consideration.append(calculated_distance)
            print("Considerations:", consideration)
        med = np.median(consideration)
        median1 = round(med, 2)
        print("Calculated values", consideration)
        print("The median distance is:", median1)
        # self.distance = round(median1-1.7,2)
        self.distance = median1
	
        dist = self.distance

        if dist in range(14,20):
            self.shape_dist = [True, False, False]
            print("In circle and square zone")
        elif (dist >= 12.5 and dist <= 15.2):
            self.shape_dist = [True, True, False]
            print("In square and triangle zone")
        elif (dist >= 4 and dist <= 9):
            self.shape_dist = [False, False, True]
            print("In Circle zone")
        elif (dist >= 9 and dist <= 14):
            self.shape_dist = [False, True, False]
            print("In Square zone")
        elif (dist >= 14 and dist <= 19):
            self.shape_dist = [True, False, False]
            print("In Triangle zone")
        else:
            self.shape_dist = [False, False, False]
            print("Out of Zone")

        GPIO.cleanup()
        print('Monitoring')

    def get_distance(self):
        return self.distance

    def get_shape_from_distance(self):
        return self.shape_dist
