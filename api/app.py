from flask import Flask, request
from model.model import load_model

app = Flask(__name__)

@app.route("/", methods=['POST'])
def predict():

    data = request.get_data()
    print(data)
    return "Success"

if __name__ == "__main__":

    app.run(debug=True, port=8000)