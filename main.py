
import RPi.GPIO as GPIO
import time
import numpy as np
from car import Car
from motor import Motor
from camera import Camera
from color_detection import ColorDetector

# class GPIO_Mock:
#     BOARD = 'BOARD'
#     OUT = 'OUT'

#     def output(self, pin, is_positive):
#         pass

#     def setup(self, pin, is_positive):
#         pass

#     def cleanup(self):
#         pass

#     def setmode(self, mode):
#         pass

# GPIO = GPIO_Mock()

MOTOR_A_PIN_1 = 11
MOTOR_A_PIN_2 = 13
MOTOR_A_PWM = 15
MOTOR_B_PIN_1 = 29
MOTOR_B_PIN_2 = 31
MOTOR_B_PWM = 33

boundaries_of = {
    'pink': (
        np.array([ 119, 0,103 ], dtype='uint8'),  
        np.array([ 255, 122,237 ], dtype='uint8'), 
    ),
    'blue': (
        np.array([ 0, 59,119 ], dtype='uint8'),
        np.array([ 143, 195,247 ], dtype='uint8'),
    ),
    'orange': (
        np.array([ 150, 77,0 ], dtype='uint8'),
        np.array([ 255, 188,117 ], dtype='uint8'),
    
    ),
    'yellow': (
        np.array([ 100, 100, 0], dtype='uint8'),
        np.array([ 200, 200,186 ], dtype='uint8'),
    ),
    'green': (
        np.array([ 0, 124,0 ], dtype='uint8'),
        np.array([ 142, 255,142 ], dtype='uint8'),
    
    )
}


def is_color_in_range(color, lower, upper):
    return np.all(lower < color) and np.all(upper > color)

class App:
    def __init__(self):
        self.car = None

    def _setup_gpio(self):
        GPIO.setmode(GPIO.BOARD)

        GPIO.setup(MOTOR_A_PIN_1, GPIO.OUT)
        GPIO.setup(MOTOR_A_PIN_2, GPIO.OUT)
        GPIO.setup(MOTOR_A_PWM, GPIO.OUT)
        GPIO.setup(MOTOR_B_PIN_1, GPIO.OUT)
        GPIO.setup(MOTOR_B_PIN_2, GPIO.OUT)
        GPIO.setup(MOTOR_B_PWM, GPIO.OUT)

        GPIO.output(MOTOR_A_PIN_1, False)
        GPIO.output(MOTOR_A_PIN_2, False)
        GPIO.output(MOTOR_B_PIN_1, False)
        GPIO.output(MOTOR_B_PIN_2, False)

        GPIO.output(MOTOR_A_PWM, True)
        GPIO.output(MOTOR_B_PWM, True)

    def setup(self):
        self._setup_gpio()
        motor_1 = Motor(GPIO, MOTOR_A_PIN_2, MOTOR_A_PIN_1)
        motor_2 = Motor(GPIO, MOTOR_B_PIN_1, MOTOR_B_PIN_2)
        self.car = Car(motor_1, motor_2, Camera())
        self.path = ['pink', 'orange', 'blue', 'yellow', 'green']        

    def run(self):
        if len(self.path) == 0:
            return
        image = self.car.camera.capture()
        color_detector = ColorDetector(image)
        colors = boundaries_of.keys()
        color_to_find = self.path[0]
        color_to_find_range = boundaries_of[color_to_find]
        for found_color in color_detector.kmeans.cluster_centers_:
            print ('FOUND COLOR RGB')
            print (found_color)
            is_color_found = is_color_in_range(found_color, color_to_find_range[0], color_to_find_range[1])
            if not is_color_found:
                print('NOT IN RANGE {}'.format(color_to_find))
                self.car.go_forward(0.2)
                self.car.turn_right(0.05)                
                continue
            else:
                print('IN RANGE {}'.format(color_to_find))                
                if color_to_find == 'pink':
                    self.car.go_forward(0.5)
                elif color_to_find == 'blue':
                    self.car.turn_left(0.7)
                elif color_to_find == 'yellow':
                    self.car.turn_right(0.5)
                elif color_to_find == 'green':
                    self.car.turn_right(5)
                elif color_to_find == 'orange':
                    self.car.turn_right(0.7)
                self.path = self.path[1:]


    def stop(self):
        GPIO.cleanup()
        self.car.camera.close()


if __name__ == '__main__':
    app = App()
    app.setup()
    try:    
        while True:
            app.run()
    except KeyboardInterrupt:
        app.stop()
        print("Program stopped by User")
