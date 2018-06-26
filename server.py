from flask import Flask, render_template
#from forms import FormEnvio, FormJogo, FormLogin

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/jogar')
def login():
    pass

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
