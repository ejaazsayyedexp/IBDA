from flask import Flask, flash, request, redirect, url_for, render_template,jsonify
import urllib.request
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
    # print('display_image filename: ' + filename)
    # carbohydrates, proteins, fats, vitamins, minerals, calories = ibda.predict(url_for('static', filename='uploads/' + filename))
    # Nutrients = {
    #     "Carbohydrates": carbohydrates,
    #     "Proteins": proteins,
    #     "Fats": fats,
    #     "Vitamins": vitamins,
    #     "Minerals": minerals,
    #     "Calories": calories
    # }
    # return redirect(url_for('static', filename='uploads/' + filename), code=301)
    # return jsonify(Nutrients)
    return prediction_of_model
 
if __name__ == "__main__":
    app.run(debug=True)

