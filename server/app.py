from flask import Flask, jsonify, request 

app = Flask(__name__) 

@app.route('/process', methods = ['GET', 'POST']) 
def home(): 
    
    if(request.method == 'POST'): 
        data = "hello world"
        return jsonify({'data': data}) 
  

if __name__ == '__main__': 
  
    app.run(debug = True) 