import urllib3
from bs4 import BeautifulSoup


http = urllib3.PoolManager()
pagina =  http.request('GET','https://pt.wikipedia.org/wiki/Linguagem_de_programa%C3%A7%C3%A3o''')
sopa = BeautifulSoup(pagina.data,'html5lib')

for tags in sopa(['scrip', 'style']):
    tags.decompose
conteudo = ' '.join(sopa.stripped_strings)