from flask import Flask, jsonify, request 
from response import Response
from uuid import uuid4
import os, sys
import utils
from flask_cors import CORS
import requests

app = Flask(__name__, static_url_path='/media/', static_folder='media/') 
UPLOAD_FOLDER = 'media/images/'
RESULT_FOLDER = 'media/results/'
YOLO_PATH = 'yolo/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app)

model = utils.YOLO()
model.load_yolo()

@app.route('/process', methods = ['GET', 'POST']) 
def home():
    if request.method == 'GET':
        return Response("Welcome to the object detection API", {
            "images":[
                f"{request.url_root}media/images/{x}" for x in os.listdir(UPLOAD_FOLDER)
            ],
            "results":[
                f"{request.url_root}media/results/{x}" for x in os.listdir(RESULT_FOLDER)
            ]
        }).send_success_response(200)
    for file in os.listdir(UPLOAD_FOLDER):
        os.remove(os.path.join(UPLOAD_FOLDER, file))
    for file in os.listdir(RESULT_FOLDER):
        os.remove(os.path.join(RESULT_FOLDER, file))
    if(request.method == 'POST'): 
        if 'file' not in request.files:
            return Response("No file part", {}).send_failiure_response(400)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            return Response("No selected file", {}).send_failiure_response(400)
        if file:
            filename = f"{uuid4()}.{file.filename.split('.')[-1]}"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            img, result = model.image_detect(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            utils.save_image(img, os.path.join(RESULT_FOLDER, filename))
            return Response("File uploaded successfully", {
                "result": result,
                "result_url": f"{request.url_root}media/results/{filename}",
                "upload_url": f"{request.url_root}media/images/{filename}"
            }).send_success_response(200)
    return Response("Method not allowed", {}).send_failiure_response(405)
  
@app.route('/delete', methods = ['GET']) 
def delete_files():
    for file in os.listdir(UPLOAD_FOLDER):
        os.remove(os.path.join(UPLOAD_FOLDER, file))
    for file in os.listdir(RESULT_FOLDER):
        os.remove(os.path.join(RESULT_FOLDER, file))
    return Response("Files deleted successfully", {}).send_success_response(200)


if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    if not os.path.exists(RESULT_FOLDER):
        os.makedirs(RESULT_FOLDER)
    if not os.path.exists(YOLO_PATH):
        os.makedirs(YOLO_PATH)
    if not os.path.exists(f"{YOLO_PATH}yolov3.weights"):
        print("Downloading YOLO V3 weights .... This might taka a while")
        url = "https://github.com/patrick013/Object-Detection---Yolov3/raw/master/model/yolov3.weights"
        utils.download_file(url, f"{YOLO_PATH}yolov3.weights")
    print("Starting the server ...")
    app.run(debug = True,host='0.0.0.0') 