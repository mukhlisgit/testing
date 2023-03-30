from flask import Flask, render_template
from app1 import app1 as app1
from app2 import app2 as app2
from app3 import app3 as app3

app = Flask(__name__)

# Add routes for the three existing Flask applications
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/app1')
def serve_app1():
    return app1.home()

@app.route('/app2')
def serve_app2():
    return app2.index()

@app.route('/app3')
def serve_app3():
    return app3.index()

if __name__ == '__main__':
    app.run(debug=True)
