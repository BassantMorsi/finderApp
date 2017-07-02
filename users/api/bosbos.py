
import os
import cv2
from PIL import Image
import numpy as np
from users.models import User, FindRequest, MissRequest



MISS_FACES_PATH = "{base_path}/faces/miss/".format(
    base_path=os.path.abspath(os.path.dirname(__file__)))


FIND_FACES_PATH = "{base_path}/faces/find/".format(
   base_path=os.path.abspath(os.path.dirname(__file__)))


def get_images_and_labels(path, extension):
    # images will contains face images
    images = []
    # labels will contains the label that is assigned to the image
    labels = []
    # Append all the absolute image paths in a list image_paths
    image_paths = [os.path.join(path, f) for f in os.listdir(path) if f.endswith(extension)]
    for image_path in image_paths:
        image_pil = Image.open(image_path).convert('L')
        image = np.array(image_pil, 'uint8')
        images.append(image)
        labels.append(int(os.path.split(image_path)[1].split(".")[0]))
    return images, labels

requestid= 1
userid = 1
e = '.' + str(requestid) + '.' + str(userid) + '.jpg'
images, labels = get_images_and_labels(FIND_FACES_PATH, e)

for label in labels:
    print label