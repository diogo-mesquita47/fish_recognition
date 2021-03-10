# -*- coding: utf-8 -*-
"""
Created on Fri Mar  5 14:52:38 2021

@author: diogo
"""

from keras.models import Sequential
from keras.layers import Convolution2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense

classifier = Sequential()

classifier.add(Convolution2D(32, 3, 3, input_shape = (64,64,3), activation = "relu"))

classifier.add(MaxPooling2D(pool_size = (2,2)))

classifier.add(Flatten())

classifier.add(Dense(128, activation = "relu"))
classifier.add(Dense(1, activation = "sigmoid"))
classifier.compile(optimizer = "adam", loss = "binary_crossentropy",metrics = ["accuracy"])

from keras.preprocessing.image import ImageDataGenerator

train_datagen = ImageDataGenerator(
    rescale=1./255,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True)

test_datagen = ImageDataGenerator(rescale=1./255)

training_set1 = train_datagen.flow_from_directory(
    r"C:\Users\mrdio\Desktop\super-duper-robot\FINAL PROJECT (ML)\dataset_alot\training_set",
    target_size=(64, 64),
    batch_size=32,
    class_mode="binary")

test_set1 = test_datagen.flow_from_directory(
    r"C:\Users\mrdio\Desktop\super-duper-robot\FINAL PROJECT (ML)\dataset_alot\test_set",
    target_size=(64, 64),
    batch_size=32,
    class_mode="binary")

from IPython.display import display
from PIL import Image

classifier.save("fish_model.h5")


#classifier.fit_generator(
    #training_set1,
    #steps_per_epoch=80,
    #epochs=10,
    #validation_data=test_set1,
    #validation_steps=400)
    
#classifier.save("C:/Users/mrdio/Desktop/super-duper-robot/FINAL PROJECT (ML)")

#import numpy as np
#from keras.preprocessing import image
#test_image = image.load_img(r"C:\Users\mrdio\Desktop\super-duper-robot\FINAL PROJECT (ML)\random.jpg",target_size = (64,64))
#test_image = image.img_to_array(test_image)
#test_image = np.expand_dims(test_image, axis=0)
#result = classifier.predict(test_image)
#training_set1.class_indices
#if result[0][0] >= 0.5:
    #prediction = "fish"
#else:
    #prediction = "no fish"
#print(prediction)
