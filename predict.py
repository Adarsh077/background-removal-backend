from keras.utils import CustomObjectScope
import tensorflow as tf
from glob import glob
import cv2
import numpy as np
import os
from metrics import dice_loss, dice_coef, iou

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"


""" Global parameters """
H = 512
W = 512

""" Creating a directory """


def create_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def predict(path):
    np.random.seed(42)
    tf.random.set_seed(42)

    create_dir("remove_bg")
    with CustomObjectScope({'iou': iou, 'dice_coef': dice_coef, 'dice_loss': dice_loss}):
        model = tf.keras.models.load_model("model.h5")

    """ Extracting name """
    name = path.split("/")[-1].split(".")[0]

    """ Read the image """
    image = cv2.imread(path, cv2.IMREAD_COLOR)
    h, w, _ = image.shape
    x = cv2.resize(image, (W, H))
    x = x/255.0
    x = x.astype(np.float32)
    x = np.expand_dims(x, axis=0)

    """ Prediction """
    y = model.predict(x)[0]
    y = cv2.resize(y, (w, h))
    y = np.expand_dims(y, axis=-1)
    y = y > 0.5

    photo_mask = y
    background_mask = np.abs(1-y)

    masked_photo = image * photo_mask
    background_mask = np.concatenate(
        [background_mask, background_mask, background_mask], axis=-1)
    background_mask = background_mask * [255, 255, 255]
    final_photo = masked_photo + background_mask

    save_path = 'assets/' + name + '.png'

    cv2.imwrite(save_path, final_photo)
    return save_path
