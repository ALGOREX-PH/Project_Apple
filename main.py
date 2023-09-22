import keras
from flask import Flask, render_template, request
import os
import cv2
import numpy as np
import tensorflow as tf


app = Flask(__name__)
upload_folder = "\\Users\\danielle meer\\Documents\\Programming_Projects\\html\\Example\\Flask Flower\\templates"

def size_regulator(path, target_size=(100, 100)):
    images = []
    image = cv2.imread(path, cv2.IMREAD_GRAYSCALE) 
    image = cv2.resize(image, target_size)
    img = image.reshape(100, 100, 1)
    #img = img / 225
    images.append(img)
    return np.array(images)

def predict(image_file):
    bo = "None"
    model = keras.models.load_model("\\Users\\danielle meer\\Documents\\Programming_Projects\\html\\Example\\Flask Flower\\proj_apple.h5")
    img = size_regulator(image_file)
    pre = np.argmax(model.predict(img))
    if pre == 0 : bo = "Healthy"
    elif pre == 1 : bo = "Apple Scab"
    elif pre == 2 : bo = "Black Rot"
    else : bo = "Cedar Apple Rust"
    return bo

@app.route('/', methods=["GET", "POST"])
@app.route('/home', methods=["GET", "POST"])
def upload_predict():
    if request.method == "POST":
      image_file = request.files["image"]
      if image_file:
          image_location = os.path.join(
              upload_folder,
              image_file.filename
          )
          image_file.save(image_location)
          bo = predict( image_location)

          return render_template("home.html", pre = predict( image_location))
    return render_template("home.html", pre = 0)

if __name__ =="__main__":
    app.run(port=12000, debug=True)


