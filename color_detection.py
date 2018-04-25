import numpy as np
from sklearn.cluster import KMeans
from sklearn.utils import shuffle
from time import time
import cv2


class ColorDetector:
    def __init__(self, image):
        self.image = image

    def _crop_image(self, w_crop_size, h_crop_size=None):
        if h_crop_size is None:
            h_crop_size = w_crop_size

        w, h, d = tuple(self.image.shape)
        w_lower_bound = int(w * w_crop_size)
        w_upper_bound = int(w * (1 - w_crop_size))
        h_lower_bound = int(h * h_crop_size)
        h_upper_bound = int(h * (1 - h_crop_size))

        self.image = self.image[
            w_lower_bound: w_upper_bound,
            h_lower_bound: h_upper_bound,
            :
        ]

    def is_color_in_range(self, range_):
        hsv = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, range_[0], range_[1])
        pixels_count = cv2.countNonZero(mask)
        if pixels_count < 500:
            return False, None
        else:
            left, center, right = self._divide_image(mask)
            pixels_count_arr = [
                cv2.countNonZero(left),
                cv2.countNonZero(center),
                cv2.countNonZero(right),
            ]
            return True, pixels_count_arr.index(max(pixels_count_arr))

    def _divide_image(self, image):
        height, width = image.shape[:2]
        start_row, start_col = 0, 0
        col = int(width / 3)
        left = image[start_row:col, :]
        center = image[col:col * 2, :]
        right = image[col * 2:col * 3, :]
        return left, center, right
