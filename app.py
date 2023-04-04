import os
import gc
import io
import time
import base64
import logging

import numpy as np
from PIL import Image

from flask import Flask, request, send_file, jsonify, send_from_directory
from flask_cors import CORS
from utils import preprocessor

import detect


app = Flask(__name__, static_folder='assets',)
CORS(app)

net = detect.load_model(model_name="u2net")

logging.basicConfig(level=logging.INFO)


@app.route("/", methods=["GET"])
def ping():
    return "U^2-Net!"


@app.route("/remove", methods=["POST"])
def remove():
    images = []
    for file in request.files.getlist("files"):
        file_path = 'files/' + file.filename
        file.save(file_path)
        # preprocessor.process(file)
        # os.remove(file_path)
        # data = file.stream.read()

        file_paths = preprocessor.process(file)
        print(file_paths)
        for path in file_paths:
            start = time.time()
            img = Image.open(path).convert("RGBA")
            output = detect.predict(net, np.array(img))
            output = output.resize(
                (img.size), resample=Image.BILINEAR)  # remove resample

            empty_img = Image.new("RGBA", (img.size), 0)
            new_img = Image.composite(
                img, empty_img, output.convert("L")).convert('RGBA')

            file_name, _ = os.path.splitext(path)
            save_path = 'assets/' + file_name + '.png'
            print(save_path)
            new_img.save(save_path)
            images.append(save_path)
            logging.info(f" Predicted in {time.time() - start:.2f} sec")

    return jsonify({'images': images})


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
