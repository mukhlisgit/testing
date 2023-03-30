from flask import Flask, request, render_template, send_file
import numpy as np
import cv2

# Initialize Flask app
app2 = Flask(__name__)

# Paths to load the model
DIR = r"C:Users/mukhlis/colorize"
MODEL = 'models/colorization_release_v2.caffemodel'
PROTOTXT = 'models/colorization_deploy_v2.prototxt'
POINTS = 'models/pts_in_hull.npy'

# Load the model
net = cv2.dnn.readNetFromCaffe(PROTOTXT, MODEL)
pts = np.load(POINTS)

# Load centers for ab channel quantization used for rebalancing.
class8 = net.getLayerId("class8_ab")
conv8 = net.getLayerId("conv8_313_rh")
pts = pts.transpose().reshape(2, 313, 1, 1)
net.getLayer(class8).blobs = [pts.astype("float32")]
net.getLayer(conv8).blobs = [np.full([1, 313], 2.606, dtype="float32")]

@app2.route('/')
def index():
    return render_template('index2.html')

@app2.route('/', methods=['POST'])
def upload_image():
    # Get the uploaded file
    img = request.files['image']

    # Save the image to a temporary directory
    img_path = 'static/' + img.filename
    img.save(img_path)

    # Load the input image
    image = cv2.imread(img_path)
    scaled = image.astype("float32") / 255.0
    lab = cv2.cvtColor(scaled, cv2.COLOR_BGR2LAB)

    resized = cv2.resize(lab, (224, 224))
    L = cv2.split(resized)[0]
    L -= 50

    # Colorize the image
    net.setInput(cv2.dnn.blobFromImage(L))
    ab = net.forward()[0, :, :, :].transpose((1, 2, 0))

    ab = cv2.resize(ab, (image.shape[1], image.shape[0]))

    L = cv2.split(lab)[0]
    colorized = np.concatenate((L[:, :, np.newaxis], ab), axis=2)

    colorized = cv2.cvtColor(colorized, cv2.COLOR_LAB2BGR)
    colorized = np.clip(colorized, 0, 1)

    colorized = (255 * colorized).astype("uint8")

    # Save the colorized image to a new file
    colorized_path = 'static/colorized_' + img.filename
    cv2.imwrite(colorized_path, colorized)

    # Return the colorized image to the user
    return send_file(colorized_path, mimetype='image/jpeg')

if __name__ == '__main__':
    app2.run(debug=True)
