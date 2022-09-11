from unicodedata import name
from flask import Flask, render_template, request
import urllib.request, json


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


app.run(debug=True, port=777)
