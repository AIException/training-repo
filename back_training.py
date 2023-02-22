from PIL import Image
import json
import os
import accelerate
import base64
from flask import Flask, jsonify, request
import glob




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
    # inputs = {'pic0':,'pic1':,...}
    inputs = request.json
    keys = inputs.keys()
    print(keys)
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

    
    ## Call the shell script for training
    os.system("""accelerate launch textual_inversion_single_aut.py \
        --pretrained_model_name_or_path="stabilityai/stable-diffusion-2" \
        --train_data_dir="dontchange" \
        --learnable_property="object" \
        --placeholder_token="dontchange" --initializer_token="dontchange"\
        --resolution=768 \
        --train_batch_size=1 \
        --gradient_accumulation_steps=1 \
        --max_train_steps=2000\
        --learning_rate=5.0e-04 --scale_lr \
        --lr_scheduler="constant" \
        --lr_warmup_steps=0 \
        --output_dir="dontchange" \
        --push_to_hub \
        --hub_token='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'"""
    )

    ## Empty training pictures' folder for future training
    files = glob.glob('training_data/*')
    for f in files:
        os.remove(f)

    return({'out':'Training Done!'})



    
    



