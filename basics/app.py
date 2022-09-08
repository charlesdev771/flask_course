from unicodedata import name
from flask import Flask, render_template, request

app = Flask(__name__, template_folder='templates')

@app.route('/', methods=['GET', 'POST'])

def index():
    nome = 'Charles'
    age = 21
    f = []
    
    if request.method == 'post':
        if request.form.get('fruits'):
            f.append(request.form.get('f'))
    
    return render_template('index.html', name = name, age = age, f=f)



@app.route('/about')
def about():
    return render_template('about.html')


app.run(debug=True, port=777)