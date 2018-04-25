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
        return pixels_count > 5000
