class Motor:
    def __init__(self, gpio, forward_pin, back_pin, pwm=None):
        self.gpio = gpio
        self.forward_pin = forward_pin
        self.back_pin = back_pin
        self.pwm = pwm

    def forward(self):
        self.gpio.output(self.forward_pin, True)
        self.gpio.output(self.back_pin, False)

    def back(self):
        self.gpio.output(self.forward_pin, False)
        self.gpio.output(self.back_pin, True)

    def stop(self):
        self.gpio.output(self.forward_pin, False)
        self.gpio.output(self.back_pin, False)
