import cv2
import numpy as np

from flask import Flask, request
from model.model import load_model

app = Flask(__name__)

@app.route("/", methods=['POST'])
def predict():

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
    
    return "Success"

if __name__ == "__main__":

    app.run(debug=True, port=8000)