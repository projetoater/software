import pymysql
import nltk
from flask import Flask, jsonify
import jsonpickle
from json import dumps
from json import JSONEncoder

class set_encoder(JSONEncoder):
    def default(self, obj):
        return list(obj)

def frequenciaScore(linhas):
    contagem = dict([linha[0], 0] for linha in linhas)
    for linha in linhas:
        # print(linha)
        contagem[linha[0]] += 1
    return contagem

def pesquisa(consulta):
    linhas, palavrasid = buscaMaisPalavras(consulta)
    
    scores = frequenciaScore(linhas)
    scoresordenado = sorted([(score, perfil) for (perfil, score) in scores.items()], reverse = 1)
    perfisLocalizados = set()
    for(score, idperfil) in scoresordenado:
        perfisLocalizados.add(getPerfil(idperfil))
    return perfisLocalizados
        
        
def getPerfil(idperfil):
    retorno = ''
    conexao = pymysql.connect(host='localhost',user='root',password='ater',db='iaater', autocommit = True)
    cursor = conexao.cursor()
    cursor.execute('select perfil from perfis where idperfil = %s', idperfil)
    if cursor.rowcount > 0:
        retorno = cursor.fetchone()[0]
    
    cursor.close()
    conexao.close()
    return retorno

# getPerfil(3)

def getIdPalavra(palavra):
    retorno = -1
    stemmer = nltk.stem.RSLPStemmer()
    conexao = pymysql.connect(host='localhost',user='root',password='ater',db='iaater', autocommit = True)
    cursor = conexao.cursor()
    cursor.execute('select idpalavra from palavras where palavra = %s', stemmer.stem(palavra))
    if cursor.rowcount > 0:
        retorno = cursor.fetchone()[0]
    cursor.close()
    conexao.close()
    return retorno

# getIdPalavra('programação')

def buscaMaisPalavras(consulta):
    listaCampos = 'p1.idperfil'
    listaTabelas = ''
    listaClausulas = ''
    palavrasid = []
    
    palavras = consulta.split(' ')
    numeroTabela = 1
    for palavra in palavras:
        idpalavra = getIdPalavra(palavra)
        if idpalavra > 0:
            palavrasid.append(idpalavra)
            if numeroTabela > 1:
                listaTabelas +=', '
                listaClausulas += ' and '
                listaClausulas += 'p%d.idperfil = p%d.idperfil and '%(numeroTabela -1, numeroTabela)
            listaCampos += ', p%d.localizacao' % numeroTabela
            listaTabelas += ' palavra_localizacao p%d' % numeroTabela
            listaClausulas += 'p%d.idpalavra = %d' % (numeroTabela, idpalavra)
            numeroTabela += 1
    consultacompleta = 'select %s from %s where %s' % (listaCampos, listaTabelas, listaClausulas)
    conexao = pymysql.connect(host='localhost',user='root',password='ater',db='iaater', autocommit = True)
    cursor = conexao.cursor()
    cursor.execute(consultacompleta)
    linhas = [linha for linha in cursor]
    cursor.close()
    conexao.close()
    return linhas, palavrasid

 # perfis = pesquisa('brasil')


ia = Flask(__name__)

# EXEMPLO: http://localhost:5000/apiPesquisa/brasil
@ia.route('/apiPesquisa/<string:palavra>', methods = ['GET'])
def apiPesquisa(palavra):
    perfis = pesquisa(palavra)
    # jsonperfis = jsonpickle.encode(perfis)
    jsonperfis = set_encoder().encode(perfis)
    return jsonify(jsonperfis)

ia.run(port=5000, host='localhost', debug = True,use_reloader=False)