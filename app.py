from flask import Flask, flash, request, redirect, url_for, render_template,jsonify
import urllib.request
import requests
import json
import os
from werkzeug.utils import secure_filename
import pickle
from predictions import makePredictions
from loadModel import loadModel

app = Flask(__name__)
model = loadModel()
#ibda = pickle.load(open('ibda.pkl', 'rb'))
classes = ['bread','Dairy Products','Dessert']
 
UPLOAD_FOLDER = 'static/uploads/'
 
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
 
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'jfif'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
     
 
@app.route('/')
def home():
    return 'home'
    #return render_template('index.html')
 
@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        print("No file part")
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        print("No image selected")
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #print('upload_image filename: ' + filename)
        flash('Image successfully uploaded and displayed below')
       #return render_template('index.html', filename=filename)
    else:
        print("Allowed types")
        flash('Allowed image types are - png, jpg, jpeg, jfif')
        return redirect(request.url)
 
@app.route('/display/<filename>')
def display_image(filename):
    prediction_of_model = makePredictions(model,os.path.join('static/uploads/',filename),classes)
    url = 'https://api.nal.usda.gov/fdc/v1/foods/search'
    parameters = {
        'query':filename[:-4],
        'api_key':'7BPKqVCgXpo0fJbU9SzcUXDketRPN7q1FPAJzord',
        'format':'abridged',
        'nutrients':[203,204,205,206]
    }
    response_food_header = requests.get(url=url,params=parameters)
    output = response_food_header.json()
    #print(output)
    list1 = {}

    for x in output["foods"][0]["foodNutrients"]:
        if(x["value"]!=0):
            list1[x["nutrientName"]] = {"value":x["value"],"unit":x["unitName"]}
    return jsonify(list1)

 
if __name__ == "__main__":
    app.run(debug=True)

