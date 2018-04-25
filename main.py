
import RPi.GPIO as GPIO
import time
import numpy as np
from car import Car
from motor import Motor
from camera import Camera
from color_detection import ColorDetector

MOTOR_A_PIN_1 = 11
MOTOR_A_PIN_2 = 13
MOTOR_A_PWM = 15
MOTOR_B_PIN_1 = 29
MOTOR_B_PIN_2 = 31
MOTOR_B_PWM = 33

boundaries_of = {
    'orange': (
        np.array([5, 50, 50], dtype=np.uint8),
        np.array([15, 255, 255], dtype=np.uint8)
    ),
    'green': (
        np.array([40, 100, 50], dtype='uint8'),
        np.array([80, 255, 255], dtype='uint8'),
    )
}


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
        self.path = ['green', 'green', 'orange', 'green']

    def run(self):
        for image in self.car.camera.start_capturing():
            if len(self.path) == 0:
                return
            color_detector = ColorDetector(image)
            color_to_find = self.path[0]
            color_to_find_range = boundaries_of[color_to_find]
            is_color_found, where_to_go = color_detector.is_color_in_range(
                color_to_find_range
            )
            if is_color_found:
                print('IN RANGE {}'.format(color_to_find))
                if where_to_go == 0:
                    self.car.turn_left(0.1)
                elif where_to_go == 1:
                    self.car.go_forward(0.2)
                    self.car.turn_right(0.1)                    
                else:
                    self.car.turn_right(0.1)
            else:
                print('NOT IN RANGE {}'.format(color_to_find))

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
        print("Program stopped by user")
