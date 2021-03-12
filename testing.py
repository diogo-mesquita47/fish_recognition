# -*- coding: utf-8 -*-
"""
Created on Mon Mar  8 18:11:18 2021

@author: diogo
"""

from tensorflow import keras
from keras.preprocessing.image import ImageDataGenerator
import numpy as np
from keras.preprocessing import image
from IPython.display import display
from PIL import Image
import tensorflow as tf


#new_model = tf.keras.models.load_model("fish_model.h5")
#print(new_model)

model = keras.models.load_model(r"C:\Users\mrdio\Desktop\super-duper-robot\FINAL PROJECT (ML)")

test_image = image.load_img(r"C:\Users\mrdio\Desktop\super-duper-robot\FINAL PROJECT (ML)\random.jpg",target_size = (64,64))
test_image = image.img_to_array(test_image)
test_image = np.expand_dims(test_image, axis=0)
result = model.predict(test_image)
if result[0][0] >= 0.5:
    prediction = "fish"
else:
    prediction = "no fish"
print(prediction)
print(test_image)