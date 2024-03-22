from flask import Flask, jsonify, request 
from response import Response
from uuid import uuid4
import os
import cv2

app = Flask(__name__) 
UPLOAD_FOLDER = 'media/images/'
RESULT_FOLDER = 'media/results/'
CARS_CASCADE = 'cascades/cars.xml'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/process', methods = ['GET', 'POST']) 
def home(): 
    
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

            car_cascade = cv2.CascadeClassifier(CARS_CASCADE)
            img = cv2.imread(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            cars = car_cascade.detectMultiScale(gray, 1.1, 1)
            no_of_cars = len(cars)
            for (x,y,w,h) in cars:
                cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)      
            cv2.imwrite(os.path.join(RESULT_FOLDER, filename), img)
            return Response("File uploaded successfully", {}).send_success_response(200)
    return Response("Method not allowed", {}).send_failiure_response(405)
  


if __name__ == '__main__': 
  
    app.run(debug = True) 