class Router:
    def __init__(self, car, path):
        self.car = car
        self._path = path
        self._color_to_find_index = 0

    def handle(self, found_color):
        if not found_color or _color_to_find_index == len(self._path) or found_color != self._path[_color_to_find_index]:
            return
        else:
            self._color_to_find_index += 1
            if found_color == 'pink':
                self.car.turn_left(0.5)
            elif found_color == 'blue':
                self.car.turn_right(0.5)
            elif found_color == 'yellow':
                self.car.go_forward(0.5)
            elif found_color == 'green':
                self.car.go_forward(0.5)
            elif found_color == 'orange':
                self.car.turn_left(1.5)