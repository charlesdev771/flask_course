import urllib.request, json
url = "https://api.themoviedb.org/3/discover/movie?sort_by=popularity.desc&api_key=bc8727e8414632f708300d82f0facca2"

resposta = urllib.request.urlopen(url)

dados = resposta.read()

jdata = json.loads(dados)

print(jdata['results'])
