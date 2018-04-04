import RPi.GPIO as GPIO
import time
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
    'red': (
        np.array([50, 56, 179], dtype='uint8'), 
        np.array([101, 101, 255], dtype='uint8'),  
    ),
    'blue': (
        np.array([156, 0, 0], dtype='uint8'),
        np.array([255, 101, 101], dtype='uint8'),
    
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

    def run(self):
        self.car.go_forward(0.5)
        image = self.car.camera.capture()
        color_detector = ColorDetector(image)
        colors = direction_when_see.keys()
        for color in colors:
            is_color_in_image = color_detector.is_color_in_image(boundaries_of[color])
            if not is_color_in_image:
                continue
            elif color == 'red':
                self.car.turn_left(0.5)


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
