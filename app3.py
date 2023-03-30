from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug. utils import secure_filename
from photo_restorer import predict_image
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug. utils import secure_filename



UPLOAD_FOLDER = '/static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app3 = Flask(__name__)
app3. config ['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app3.config ['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000

@app3.route("/")
def home():
    return render_template("index3.html")

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app3.route('/', methods=['POST'])
def upload_file():
    if request.method == 'POST':

        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']


        if file.filename == '':
            return redirect(request.url)


        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            full_filename = "." + url_for("static", filename ="images/" + filename)
            print(full_filename)
            file.save(full_filename)
            
            predicted_img_url =  predict_image(full_filename)
            return render_template("index3.html", filename =filename, restored_img_url = predicted_img_url)

if __name__ == "__main__":
    app3.run(debug=True)