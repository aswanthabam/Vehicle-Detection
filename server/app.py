from flask import Flask, jsonify, request 
from response import Response
from uuid import uuid4
import os
import utils
from flask_cors import CORS

app = Flask(__name__, static_url_path='/media/', static_folder='media/') 
UPLOAD_FOLDER = 'media/images/'
RESULT_FOLDER = 'media/results/'
CARS_CASCADE = 'cascades/cars.xml'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app)

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

            img, result = utils.image_detect(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            utils.save_image(img, os.path.join(RESULT_FOLDER, filename))
            return Response("File uploaded successfully", {
                "result": result,
                "result_url": f"{request.url_root}media/results/{filename}",
                "upload_url": f"{request.url_root}media/images/{filename}"
            }).send_success_response(200)
    return Response("Method not allowed", {}).send_failiure_response(405)
  


if __name__ == '__main__': 
  
    app.run(debug = True,host='0.0.0.0') 