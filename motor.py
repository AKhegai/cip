class Motor:
    def __init__(self, gpio, pwm, back_pin):
        self.gpio = gpio
        self.pwm = pwm
        self.back_pin = back_pin

    def forward(self, dc):
        self.pwm.ChangeDutyCycle(dc)
        self.gpio.output(self.back_pin, False)

    def stop(self):
        self.pwm.ChangeDutyCycle(0)
        self.gpio.output(self.back_pin, False)
