# -*- coding: utf-8 -*-
"""
Created on Mon Mar  8 09:51:05 2021

@author: diogo
"""

from flask import Flask, redirect, url_for, render_template, request, jsonify, flash
from werkzeug.utils import secure_filename
from tensorflow import keras
from keras.preprocessing.image import ImageDataGenerator, img_to_array
import numpy as np
from keras.preprocessing import image
from IPython.display import display
from PIL import Image
import io
import json
import base64
import requests
from keras.applications import inception_v3
import tensorflow as tf
from keras.models import load_model
import os

UPLOAD_FOLDER = r'C:\Users\mrdio\Desktop\super-duper-robot\FINAL PROJECT (ML)\images_to_insert'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app = Flask(__name__)
app.secret_key = "super secret key"

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/upload')
def upload_file():
   return render_template('uploaders.html')

# @app.route("/uploaders", methods=["POST"])
# def upload():
#     uploaded_files = request.files.getlist("file[]")
#     print(uploaded_files)
#     return ""


@app.route('/fish_detector', methods = ['GET', 'POST'])
def uploader():  
    predictions = []
    model = keras.models.load_model(r"C:\Users\mrdio\Desktop\super-duper-robot\FINAL PROJECT (ML)")
    if request.method == 'POST':
        # check if the post request has the file part
        files = request.files.getlist("file[]")
        #if user does not select file, browser also
        #submit a empty part without filename
        if files[0] == '':
            flash('No selected file')
            return redirect(request.url)
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                test_image = image.load_img(r"C:\Users\mrdio\Desktop\super-duper-robot\FINAL PROJECT (ML)\images_to_insert"+"\\"+filename,target_size = (64,64))
                test_image = image.img_to_array(test_image)
                test_image = np.expand_dims(test_image, axis=0)
                result = model.predict(test_image)
                if result[0][0] >= 0.5:
                    predictions.append("fish")
                else:
                    predictions.append("no fish")
    return " ".join([str(elem) for elem in predictions])
            
        



# @app.route('/uploader', methods = ['GET', 'POST'])
# def uploader():
#    model = keras.models.load_model(r"C:\Users\mrdio\Desktop\super-duper-robot\FINAL PROJECT (ML)")
#    if request.method == 'POST':
#       images = request.files['file']
#       images = secure_filename(images.filename)
#       images.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#       images = image.img_to_array(images)
#       images = np.expand_dims(images, axis=0)
#       result = model.predict(images)
#       if result[0][0] >= 0.5:
#          prediction = "fish"
#       else:
#          prediction = "no fish"
#       return images.content_type

if __name__ == "__main__":
    app.run()