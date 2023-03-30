from flask import Flask, render_template, request
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import os
from io import BytesIO
import traceback

app1 = Flask(__name__)
model = load_model('model.h5')

@app1.route('/')
def home():
    return render_template('index1.html')

# set maximum allowed file size to 10 megabytes
app1.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024

# specify allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# define function to check if file extension is allowed
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app1.route('/predict', methods=['POST'])
def predict():

    # check if image file was uploaded
    if 'image' not in request.files:
        return 'No image file found'

    # Get the file from the POST request
    file = request.files['image']

    try:
        # Read the image
        img = image.load_img(BytesIO(file.read()), target_size=(256, 256))

        if len(file.read()) > app1.config['MAX_CONTENT_LENGTH']:
            return 'File size exceeds limit'

        # convert image to numpy array
        img_array = image.img_to_array(img)

        # normalize pixel values to range [0, 1]
        img_array = img_array / 255.0

        # add batch dimension to input array
        img_array = np.expand_dims(img_array, axis=0)

        # Make the prediction
        preds = model.predict(img_array)

        return str(preds[0])

    except Exception as e:
        traceback.print_exc()
        return f'Error predicting image: {e}'

if __name__ == '__main__':
    app1.run(debug=True)
