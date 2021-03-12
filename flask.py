# -*- coding: utf-8 -*-
"""
Created on Mon Mar  8 09:51:05 2021

@author: diogo
"""

from flask import Flask, redirect, url_for, render_template, request, jsonify, flash, send_from_directory
from werkzeug.utils import secure_filename
from tensorflow import keras
from keras.preprocessing.image import ImageDataGenerator, img_to_array
import numpy as np
from keras.preprocessing import image
import os

UPLOAD_FOLDER = r'C:\Users\mrdio\Desktop\super-duper-robot\fish_recognition\images_to_insert'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
UPLOAD_FOLDER1 = r"C:\Users\mrdio\Desktop\super-duper-robot\fish_recognition\fish"
UPLOAD_FOLDER2 = r"C:\Users\mrdio\Desktop\super-duper-robot\fish_recognition\no_fish"


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app = Flask(__name__)
app.secret_key = "super secret key"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/upload')
def upload_file():
   return render_template('uploaders.html')


@app.route('/fish_detector', methods = ['GET', 'POST'])
def uploader():  
    predictions = []
    model = keras.models.load_model(r"C:\Users\mrdio\Desktop\super-duper-robot\fish_recognition")
    os.makedirs(r"C:\Users\mrdio\Desktop\super-duper-robot\fish_recognition\fish")
    os.makedirs(r"C:\Users\mrdio\Desktop\super-duper-robot\fish_recognition\no_fish")
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
                app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                test_image = image.load_img(r"C:\Users\mrdio\Desktop\super-duper-robot\fish_recognition\images_to_insert"+"\\"+filename,target_size = (64,64))
                test_image = image.img_to_array(test_image)
                test_image = np.expand_dims(test_image, axis=0)
                result = model.predict(test_image)
                if result[0][0] >= 0.5:
                    predictions.append("fish")
                    app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER1
                    t = image.load_img(r"C:\Users\mrdio\Desktop\super-duper-robot\fish_recognition\images_to_insert"+"\\"+filename)
                    t.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
                else:
                    predictions.append("no fish")
                    app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER2
                    t2 = image.load_img(r"C:\Users\mrdio\Desktop\super-duper-robot\fish_recognition\images_to_insert"+"\\"+filename)
                    t2.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
    image_names = os.listdir(r'C:\Users\mrdio\Desktop\super-duper-robot\fish_recognition\images_to_insert')
    return render_template("gallery.html", text="There are "+str(predictions.count("fish"))+" photos that contain fish and "+str(predictions.count("no fish"))+" that don't:", image_names=image_names)

@app.route('/upload/<filename>')
def send_image(filename):
    return send_from_directory("images_to_insert", filename)

if __name__ == "__main__":
    app.run()