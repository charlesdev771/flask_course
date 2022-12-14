from unicodedata import name
from flask import Flask, render_template, request, redirect, url_for, flash
import urllib.request, json
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cursos.sqlite3'
app.config['SECRET_KEY'] = 'key'
db = SQLAlchemy(app)

class cursos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.Integer)
    desc = db.Column(db.String(100))
    ch = db.Column(db.Integer)

    def __init__(self, nome, desc, ch):
        self.nome = nome
        self.desc = desc
        self.ch = ch

@app.route('/', methods=['GET', 'POST'])

def index():
    nome = 'Charles'
    age = 21
    f = []

    if request.method == 'post':
        if request.form.get('fruits'):
            f.append(request.form.get('f'))

    return render_template('index.html', name = name, age = age, f=f)

@app.route('/filmes/<propriedade>')

def filmes(propriedade):
    ''''
    What are the most popular movies?

    URL: /discover/movie?sort_by=popularity.desc

    What are the highest rated movies rated R?

    URL: /discover/movie/?certification_country=US&certification=R&sort_by=vote_average.desc


    What are the most popular kids movies?

    URL: /discover/movie?certification_country=US&certification.lte=G&sort_by=popularity.desc

    What is are the best movies from 2010?

    URL: /discover/movie?primary_release_year=2010&sort_by=vote_average.desc


    url = "https://api.themoviedb.org/3/discover/movie?sort_by=popularity.desc&api_key=bc8727e8414632f708300d82f0facca2"
    url = "https://api.themoviedb.org/3/discover/movie/?certification_country=US&certification=R&sort_by=vote_average.desc&api_key=bc8727e8414632f708300d82f0facca2"
    url = "https://api.themoviedb.org/3/discover/movie?certification_country=US&certification.lte=G&sort_by=popularity.desc&api_key=bc8727e8414632f708300d82f0facca2"
    url = "https://api.themoviedb.org/3/discover/movie?primary_release_year=2010&sort_by=vote_average.desc&api_key=bc8727e8414632f708300d82f0facca2"

    '''

    url = ''

    if propriedade == 'main':
        url = "https://api.themoviedb.org/3/discover/movie?sort_by=popularity.desc&api_key=bc8727e8414632f708300d82f0facca2"
    elif propriedade == 'kids':
        url = "https://api.themoviedb.org/3/discover/movie/?certification_country=US&certification=R&sort_by=vote_average.desc&api_key=bc8727e8414632f708300d82f0facca2"
    elif propriedade == '2010':
        url = 'https://api.themoviedb.org/3/discover/movie?certification_country=US&certification.lte=G&sort_by=popularity.desc&api_key=bc8727e8414632f708300d82f0facca2'
    elif propriedade == 'drama':
        url = 'https://api.themoviedb.org/3/discover/movie?with_genres=18&primary_release_year=2014&api_key=bc8727e8414632f708300d82f0facca2'
    elif propriedade == 'liam':
        url = 'https://api.themoviedb.org/3/discover/movie?certification_country=US&certification=R&sort_by=revenue.desc&with_cast=3896&api_key=bc8727e8414632f708300d82f0facca2'

    resposta = urllib.request.urlopen(url)

    dados = resposta.read()

    jdata = json.loads(dados)

    return render_template('filmes.html', filmes=jdata['results'])





@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/cursos')
def lista_cursos():
    page = request.args.get('page', 1, type=int)
    per_page = 4
    todos_cursos = cursos.query.paginate(page, per_page)
    return render_template('cursos.html', cursos=todos_cursos)

@app.route('/cria_curso', methods=['GET', 'POST'])
def cria_curso():
    nome = request.form.get('nome')
    desc = request.form.get('desc')
    ch = request.form.get('ch')

    if request.method == 'POST':
        if not nome or not desc or not ch:
            flash("Preencha os campos", "error")
        else:
            curso = cursos(nome, desc, ch)
            db.session.add(curso)
            db.session.commit()
            return redirect(url_for('lista_cursos'))

    return render_template('novo_curso.html', methods=['GET', 'POST'])


@app.route('/<int:id>/atualizar', methods=['GET', 'POST'])
def atualizar(id):
    curso = cursos.query.filter_by(id=id).first()
    if request.method == 'POST':
        nome = request.form['nome']
        desc = request.form['desc']
        ch = request.form['ch']

        cursos.query.filter_by(id=id).update({'nome':nome, 'desc':desc, 'ch':ch})
        db.session.commit()
        return redirect(url_for('lista_cursos'))
    return render_template('atualizar.html', curso=curso)

@app.route('/<int:id>/excluir')
def excluir(id):
    curso = cursos.query.filter_by(id=id).first()
    db.session.delete(curso)
    db.session.commit()
    return redirect(url_for('lista_cursos'))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True, port=777)
