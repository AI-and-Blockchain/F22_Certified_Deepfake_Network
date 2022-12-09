import numpy as np
import base64

from PIL import Image
from io import BytesIO
from flask import Flask, request, jsonify
from model.model import load_model

app = Flask(__name__)

@app.route("/predict", methods=['GET', 'POST'])
def predict():
    
    image = request.args.get('image')

    if image is None:
        return jsonify({
            'confidence_score': 0.0,
            'status': 'You gotta give me an image string bro. Example: /predict?image=<YOUR IMAGE AS A BASE64 string>'
        })

    print(f"-----------TEST----------------: {image}")

    try:

        # Read in base64 string and extract the relevant bytes
        image = image.split(",")[1].replace(' ', '+').encode()
        image = np.array(Image.open(BytesIO(base64.b64decode(image))).resize((256, 256), resample=Image.Resampling.BOX))

        # Load model for inference
        model = load_model()
        pred = model.predict(np.array([image]))
        print(f"\ntest\n{pred}\ntest\n")
        print(image)
        print("\n\n\n")
        return jsonify({
            'confidence_score': float(round(pred[0][0], 3)),
            'status': 'Successfully made a prediction.'
        })

    except Exception as err:

        print(image)
        return jsonify({
            'confidence_score': 0.0,
            'status': f'Make sure your input is correctly formatted (base64 image format). Error: {err}'
        })

@app.route("/", methods=['GET'])
def hello():

    return jsonify({
        'confidence_score': 0.5134212,
        'status': "This is a static call to check that the api's alive"
    })

if __name__ == "__main__":

    app.run(debug=True, port=8000)