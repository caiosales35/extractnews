#!/usr/bin/env python
# -*- coding: utf-8 -*-
#import urllib.request 
from urllib.request import Request, urlopen
import AdvancedHTMLParser
import abc
import csv
import codecs

# interface para retornar dados, obrigatorio implementar um metodo que retorne um html
class Data(metaclass=abc.ABCMeta):
     @abc.abstractmethod
     def getHTML(self, url):
        return

# classe que retorna dados da web
class WebDados(Data):
    def __init__(self, encode="utf-8", headers={'User-Agent': 'Mozilla/5.0'}):
        self._encode = encode
        self._headers = headers
    # Se quiser alterar a forma de obter HTML da web, deve se alterar a forma de fazer
    # requisições (atualmente com urlib); retornando o HTML da pagina na variavel text
    def getHTML(self, url):
        request = Request(url, headers=self._headers)
        response = urlopen(request).read()
        try :
            text = response.decode(self._encode)
            return text
        except UnicodeDecodeError:
            print("Não foi possivel baixar do site especificado: " + url)
            print("Erro de decodificação!")
    def setEncode(self, encode):
        self._encode = encode
    def getEncode(self):
        return self._encode
    def setHeaders(self, headers):
        self._headers = headers
    def getHeaders(self):
        return self._headers

# interface para extrair noticias de html de portais web, obrigatorio implementar 
# o metodo get (forma de extração) de cada classe de cada portal de noticias
class extractNews(metaclass=abc.ABCMeta):
    def __init__(self, url, classe=None, tag=None):
        self._url = url
        self._classe = classe
        self._tag = tag
        html = WebDados().getHTML(self._url)
        self._parser = AdvancedHTMLParser.AdvancedHTMLParser()
        self._parser.parseStr(html)

    def getUrl(self):
        return self._url
    def setUtl(self, url):
        self._url = url
    def getClasse(self):
        return self._classe
    def setClasse(self, classe):
        self._classe = classe
    def getTag(self):
        return self._tag
    def setTag(self, tag):
        self._tag = tag

    @abc.abstractmethod
    def getNews(self):
        return

class SaoCarlosAgora(extractNews):
    def getNews(self):
        itens = self._parser.getElementsByClassName(self._classe)
        dados = dict([])
        for item in itens:
            dados[item.textContent] = item.getAttribute("href")
        return dados

class SaoCarlosAgoraUltimas(extractNews):
    def getNews(self):
        itens = self._parser.getElementsByTagName(self._tag)
        dados = dict([])
        for item in itens:
            dados[item.textContent] = item.parentNode.getAttribute("href")
        return dados

class G1(extractNews):
    def getNews(self):
        itens = self._parser.getElementsByClassName(self._classe)
        dados = dict([])
        for item in itens:
            dados[item.textContent] = item.getAttribute("href")
        return dados

class Uol(extractNews):
    def getNews(self):
        itens = self._parser.getElementsByClassName(self._classe)
        dados = dict([])
        for item in itens:
            dados[item.textContent.strip()] = item.parentNode.getAttribute("href")
        return dados


# Se quiser alterar os sites de pesquisas, as classes e / ou tags dos elementos para serem recuperados;
# alterar o preenchimento da variavel dicionario_fontes. Atulmente tratada com um array de arrays;
# pode-se fazer a leiura direta do terminar, ou ainda de um arquivo, atualmente é estatico.
# Elemento: [URL, CLASSE, TAG]
def getFonts():
    dicionario_fontes = [
            ["https://g1.globo.com/", "feed-post-link", None], 
            ["https://www.saocarlosagora.com.br/", "tituloVitrine", None],
            ["https://www.saocarlosagora.com.br/ultimas-noticias/", "ultimas-noticias", "h3"],
            ["https://noticias.uol.com.br/", "thumb-caption", None]
    ]
    
    return dicionario_fontes

urls = getFonts()

dados = []
dados_g1 = G1(urls[0][0], urls[0][1], urls[0][2]).getNews()
dados_saoCarlosAgora = SaoCarlosAgora(urls[1][0], urls[1][1], urls[1][2]).getNews()
dados_saoCarlosAgoraUltimas = SaoCarlosAgoraUltimas(urls[2][0], urls[2][1], urls[2][2]).getNews()
dados_uol = Uol(urls[3][0], urls[3][1], urls[3][2]).getNews()

dados.append(dados_g1)
dados.append(dados_saoCarlosAgora)
dados.append(dados_saoCarlosAgoraUltimas)
dados.append(dados_uol)

class writeCSV():
    try:
        with codecs.open('dict.csv', 'w', 'utf-8') as csv_file:  
            writer = csv.writer(csv_file)
            for key, value in dados[0].items():
                writer.writerow([key, value])
        csv_file.close()
    except IOError:           # operação de entrada/saída falhou
        print("I/O error")
