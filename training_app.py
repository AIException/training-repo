import streamlit as st
from PIL import Image
import requests
import io
import base64


def encode_image(image, format = "JPEG"):
       # encode image as base 64
        # postprocess the prediction
        #return {"image": img_str.decode()}
    image.save('send.png')
    with open('send.png', mode='rb') as file:
        img = file.read()
    img_str = base64.b64encode(img)

    return img_str.decode('utf-8')



def request_handler_info(payload, url = 'http://35.188.157.28:5000/endpoint_info'):
    # Send payload
    response = requests.post(url, json=payload)
    out = response.json()['out']

    return out


def request_handler_pic(pics, url = 'http://35.188.157.28:5000/endpoint_pic'):
    # Send payload 
    response = requests.post(url, json=pics)
    out = response.json()

    return out['out']

def request_handler_train(go, url = 'http://35.188.157.28:5000/endpoint_train'):
    # Send payload 
    response = requests.post(url, json=go)
    out = response.json()

    return out['out']


def send_train_pic(train_pics):

    key = 0
    payload = {}

    for train_pic in train_pics:
    #pic = pic.getvalue()
    #stream = io.BytesIO(pic)
        pic = Image.open(train_pic)
        img_str = encode_image(pic)     
        payload["pic{}".format(key)] = img_str
        key += 1
    
    print(payload.keys())
    out = request_handler_pic(payload)
    
    return out




header = st.container()
showcase = st.container()

with header:
    st.title('NeoLocus Training')
    st.write('A generative AI powered tool that helps Companies place their products in Custom Environments.') 
    st.write('Train your items here!')

    
    placeholder = st.text_input("Placeholder Token")
    init_tok = st.text_input("Initializer Token (closest word to the item)")


    info = st.button("Send Info!")
    if info:
        st.session_state = {}

        info_payload = {'placeholder':placeholder, 'init_tok':init_tok}
        result_info = request_handler_info(info_payload)
        st.write(result_info)
        st.session_state['info'] = True

    if 'info' in st.session_state.keys():

        train_pics = st.file_uploader('Upload pictures of your item', accept_multiple_files = True)
        pictures = st.button("Send Pictures!")
        if pictures:
            st.session_state['pictures'] = True
            for train_pic in train_pics:
                print(type(train_pic))
                result_upload = send_train_pic(train_pics)
                st.write(result_upload)
    
    if 'pictures' in st.session_state.keys():
        generate = st.button("Train!")
        if generate:
            result_train = request_handler_train({"":""})
            st.write(result_train)
