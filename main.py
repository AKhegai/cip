import RPi.GPIO as GPIO
import time


MOTOR_A_PIN_1 = 11
MOTOR_A_PIN_2 = 13
MOTOR_A_PWM = 15
MOTOR_B_PIN_1 = 29
MOTOR_B_PIN_2 = 31
MOTOR_B_PWM = 33


class Motor:
    def init(self, forward_pin, back_pin, pwm=None):
        self.forward_pin = forward_pin
        self.back_pin = back_pin
        self.pwm = pwm

    def forward(self):
        GPIO.output(self.forward_pin, True)
        GPIO.output(self.back_pin, False)

    def back(self):
        GPIO.output(self.forward_pin, False)
        GPIO.output(self.back_pin, True)

    def stop(self):
        GPIO.output(self.forward_pin, False)
        GPIO.output(self.back_pin, False)


class Car:
    def init(self, motor_1, motor_2):
        self.motor_1 = motor_1
        self.motor_2 = motor_2

    def go_forward(self, seconds=1):
        self.motor_1.forward()
        self.motor_2.forward()
        time.sleep(seconds)
        self.stop()
        return self

    def go_back(self, seconds=1):
        self.motor_1.back()
        self.motor_2.back()
        time.sleep(seconds)
        self.stop()
        return self

    def turn_right(self, seconds):
        self.motor_1.forward()
        self.motor_2.back()
        time.sleep(seconds)
        self.stop()
        return self

    def turn_left(self, seconds):
        self.motor_2.forward()
        self.motor_1.back()
        time.sleep(seconds)
        self.stop()
        return self

    def stop(self):
        self.motor_1.stop()
        self.motor_2.stop()
        return self


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
        motor_1 = Motor(MOTOR_A_PIN_1, MOTOR_A_PIN_2)
        motor_2 = Motor(MOTOR_B_PIN_1, MOTOR_B_PIN_2)
        self.car = Car(motor_1, motor_2)

    def run(self):
        self.car.go_forward().go_back()


if __name__ == 'main':
    app = App()
    app.setup()
    try:
        app.run()
    except KeyboardInterrupt:
        print("Program stopped by User")
        GPIO.cleanup()
