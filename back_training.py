from PIL import Image
import json
import os

import base64
from flask import Flask, jsonify, request


app = Flask(__name__)


def open_pic(img_str, key):

    filename = 'training_data/train{}.jpg'.format(key)
    key += 1

    img = base64.b64decode(img_str)
    with open(filename, 'wb') as file:
        file.write(img)
        return({'out':'Image Saved!'})
    
    return({'out':'Image not Saved.'})



@app.route('/endpoint_pic', methods=['POST'])
def endpoint_pic():
    inputs = request.json
    keys = inputs.keys()
    print(len(keys))
    save_key = 0
    for k in keys:
        saved = open_pic(inputs[k], save_key)
        save_key += 1

    return saved


@app.route('/endpoint_info', methods=['POST'])
def endpoint_info():
    # inputs = {'link':, 'color':, 'placeholder':, 'init_tok':}
    inputs = request.json
    with open('json_data.json', 'w') as outfile:
        json.dump(inputs, outfile)
        return({'out':'Information Retrieved.'})

    
    



