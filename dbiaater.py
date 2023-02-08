import urllib3
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
import nltk
import pymysql
import pandas as pd

    
def inserePalavraLocalizacao(idperfil, idpalavra, localizacao):
    conexao = pymysql.connect(host='localhost',user='root',password='ater',db='iaater', autocommit = True)
    cursor = conexao.cursor()
    cursor.execute('insert into palavra_localizacao(idperfil, idpalavra, localizacao) values (%s, %s, %s)', (idperfil, idpalavra, localizacao))
    idpalavraLocalizacao = cursor.lastrowid
    cursor.close()
    return idpalavraLocalizacao

def inserePalavra(palavra):
    conexao = pymysql.connect(host='localhost',user='root',password='ater',db='iaater', autocommit = True, use_unicode = True, charset = 'utf8mb4')
    cursor = conexao.cursor()
    cursor.execute('insert into palavras(palavra) values (%s)', palavra)
    idpalavra = cursor.lastrowid
    cursor.close()
    conexao.close()
    return idpalavra

def palavraIndexada(palavra):
    retorno = -1
    conexao = pymysql.connect(host='localhost',user='root',password='ater',db='iaater', autocommit = True, use_unicode = True, charset = 'utf8mb4')
    cursor = conexao.cursor()
    cursor.execute('select idpalavra from palavras where palavra = %s', palavra)
    if cursor.rowcount > 0:
        # print('Palavra já cadastrada')
        retorno = cursor.fetchone()[0]
    # else:
    #     print('Palavra não cadastrada')
    cursor.close()
    conexao.close()
    return retorno

def inserePerfil(perfil, bio):
    conexao = pymysql.connect(host='localhost',user='root',password='ater',db='iaater', autocommit = True)
    cursor = conexao.cursor()
    cursor.execute('insert into perfis(perfil, bio) values (%s, %s)', (perfil, bio))
    idperfil = cursor.lastrowid  
    cursor.close()
    conexao.close()
    return idperfil

def perfilIndexado(perfil):
    retorno = -1
    conexao = pymysql.connect(host='localhost',user='root',password='ater',db='iaater' )
    cursorUrl = conexao.cursor()
    cursorUrl.execute('select idperfil from perfis where perfil = %s', perfil)
    if cursorUrl.rowcount > 0:
        # print('Url cadastrada')
        idperfil = cursorUrl.fetchone()[0]
        cursorPalavra = conexao.cursor()
        cursorPalavra.execute('select idperfil from palavra_localizacao where idperfil = %s', idperfil)
        if cursorPalavra.rowcount > 0:
            # print('Url com palavras')
            retorno = -2
        else:
            # print('Url sem palavras')
            retorno = idperfil
            
        cursorPalavra.close()
    # else:
    #     print('Url não cadastrada')
    
    cursorUrl.close()
    conexao.close()
    
    return retorno

def separaPalavras(texto):
    stop = nltk.corpus.stopwords.words('portuguese')
    stemmer = nltk.stem.RSLPStemmer()
    splitter = re.compile('\\W')
    lista_palavras = []
    lista = [p for p in splitter.split(texto) if p !='']
    for p in lista:
        if p.lower() not in stop:
            if len(p) > 1:
                lista_palavras.append(stemmer.stem(p).lower())
    return lista_palavras

def indexador(perfil, bio):
    indexado = perfilIndexado(perfil)
    if indexado == -2:
        print('Perfil já indexado')
        return
    elif indexado == -1:
        idnovoperfil = inserePerfil(perfil, bio)
    elif indexado > 0:
        idnovoperfil = indexado
        
    print('Indexando '+ perfil)
    
    palavras = separaPalavras(bio)
    for i in range(len(palavras)):
        palavra = palavras[i]
        idpalavra = palavraIndexada(palavra)
        if idpalavra == -1:
            idpalavra = inserePalavra(palavra)
        inserePalavraLocalizacao(idnovoperfil, idpalavra, i)

        
def crawl():
    df = pd.read_csv("dataset.csv", sep=",", encoding="utf8")
    for x in range(0, len(df['bio'])):
        print(df['user'][x], df['bio'][x])
        indexador(df['user'][x], df['bio'][x])
        
crawl()