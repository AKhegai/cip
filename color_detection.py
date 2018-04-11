import numpy as np
from sklearn.cluster import KMeans
from sklearn.utils import shuffle
from time import time
import cv2


def is_color_in_range(color, lower, upper):
    return np.all(lower < color) and np.all(upper > color)


def recreate_image(codebook, labels, w, h):
    d = codebook.shape[1]
    image = np.zeros((w, h, d))
    label_idx = 0
    for i in range(w):
        for j in range(h):
            image[i][j] = codebook[labels[label_idx]]
            label_idx += 1
    return image


class ColorDetector:
    def __init__(self, image):
        self.image = image
        self._train_k_means(3)
        self._crop_image(0.25)
        

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

    def _train_k_means(self, n_colors):
        w, h, d = tuple(self.image.shape)
	image_array = np.reshape(self.image, (w * h, d))
        image_array_sample = shuffle(image_array, random_state=0)[:500]
        self.kmeans = KMeans(n_clusters=n_colors, random_state=0).fit(image_array_sample)
	self.labels = self.kmeans.predict(image_array)
	recreated_image = recreate_image(self.kmeans.cluster_centers_, self.labels, w, h)
	cv2.imwrite('1.jpg', cv2.cvtColor(np.uint8(recreated_image), cv2.COLOR_BGR2RGB))


    def is_color_in_image(self, color_range, color_name):
        for cluster_center in self.kmeans.cluster_centers_:
	        print ('Found {}. Looked for {}'.format(cluster_center, color_name))
            if is_color_in_range(
                cluster_center, 
                color_range[0],
                color_range[1],
            ):
                return True
        print ('\n\n')
        return False
