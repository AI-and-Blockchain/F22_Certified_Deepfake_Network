import cv2
import numpy as np
import flask

from flask_cors import CORS
from flask import Flask, request
from model.model import load_model

app = Flask(__name__)
CORS(
    app,
    origins="*"
)

@app.route("/", methods=['POST', 'GET'])
def predict():
    # print(request.args.get('path'))

    # Read in image
    image = request.files['image'].read()
    bytes = np.frombuffer(image, np.uint8)
    img = np.array([cv2.imdecode(bytes, cv2.IMREAD_COLOR)])
    # print(image[:100])
    # print(bytes, len(bytes))
    # print(img)

    # Perform model inference
    model = load_model()
    score = model.predict(img)
    prediction = round(score)
    
    response = flask.jsonify({'test': ''})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == "__main__":

    app.run(debug=True, port=8000)