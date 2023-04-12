import os
import time
import logging

import numpy as np

from flask import Flask, request, jsonify
from flask_cors import CORS
from preprocessor import preprocessor

from predict import predict


app = Flask(__name__, static_folder='assets',)
CORS(app)

logging.basicConfig(level=logging.INFO)


@app.route("/", methods=["GET"])
def ping():
    return "Background Remover"


@app.route("/remove", methods=["POST"])
def remove():
    images = []
    for file in request.files.getlist("files"):
        file_path = 'files/' + file.filename
        file.save(file_path)

        file_paths = preprocessor.process(file)
        for path in file_paths:
            start = time.time()

            save_path = predict(path)

            images.append(save_path)

            logging.info(f" Predicted in {time.time() - start:.2f} sec")

    return jsonify({'images': images})


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
