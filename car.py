import time

class Car:
    def __init__(self, motor_1, motor_2, camera):
        self.motor_1 = motor_1
        self.motor_2 = motor_2
        self.camera = camera

    def go_forward(self, seconds=1):
        self.motor_1.forward()
        time.sleep(seconds / 3)        
        self.stop()        
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