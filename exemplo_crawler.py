import urllib3
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
import nltk 
import pymysql

def pagina_indexada(url):
    conexao = pymysql.connect(host='localhost', user='root', passwd='12345', db='indice')
    cursorUrl = conexao.cursor()
    cursorUrl.execute("select id from urls where url = %s", url)
   
    if(cursorUrl.rowcount()>0):
        print('url cadastrada')
        idUrl = cursorUrl.fetchone()[0]
        cursorPalavra = conexao.cursor()
        cursorPalavra.execute("select id_url from palavra_localizacao where id_url = %s", idUrl)
       
        if(cursorPalavra.rowcount()>0):
            print('url com palavras')
        else:
            print('url sem palavras')
        
        cursorPalavra.close()
    else:
        print('url nao cadastrada')
        
    
    cursorUrl.close()
    conexao.close()

def get_texto(sopa):
    for tags in sopa(['scrip', 'style']):
        tags.decompose
    return ' '.join(sopa.stripped_strings)

def separa_palavras(texto):
    splitter = re.compile('\\W*')
    stemmer = nltk.stem.RSLPStemmer()
    stop = nltk.corpus.stopwords.words('portuguese')
    lista_palavras = []

    lista = [p for p in splitter.split(texto) if p != '']
    
    for p in lista:
        if p.lower() not in stop:
            if len(p) > 1:
                lista_palavras.append(stemmer.stem(p).lower())
    
    return lista_palavras

def crawl(paginas, profundidade):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    for i in range(profundidade):
        novas_paginas = set()
        for pagina in paginas:
            http = urllib3.PoolManager()
            try:
                dados_pagina =  http.request('GET',pagina)
            except:
                print('erro ao abrir pagina: {}'.format(pagina))
            
            sopa = BeautifulSoup(dados_pagina.data,'html5lib')
            links = sopa.find_all('a')
            
            for link in links:
                
              
                if 'href' in link.attrs:
                    url = urljoin(pagina,str(link.get('href')))
                    
                    if url.find("'") != -1:
                        continue
                    
                    url = url.split('#')[0]
                                
                    if url[0:4] == 'http':
                        novas_paginas.add(url)
            paginas = novas_paginas
            print(len(paginas))

#lista_paginas = ['https://pt.wikipedia.org/wiki/Linguagem_de_programa%C3%A7%C3%A3o']

