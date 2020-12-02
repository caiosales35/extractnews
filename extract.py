#!/usr/bin/env python
# -*- coding: utf-8 -*-
#import urllib.request 
from urllib.request import Request, urlopen
import AdvancedHTMLParser
import abc

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


# Se quiser alterar os sites de pesquisas e as classes dos elementos para serem recuperados;
# alterar o preenchimento da variavel dicionario_fontes. Atulmente tratada como um dicionario;
# pode-se fazer a leiura direta do terminar, ou ainda de um arquivo, atualmente é estatico.
# URL: [array com classes de elemtos para recuperar da pagina]
def getFonts():
    dicionario_fontes = {"https://g1.globo.com/": ["feed-post-link"], "https://www.saocarlosagora.com.br/": ["tituloVitrine"] }
    return dicionario_fontes

urls = getFonts()
parser = AdvancedHTMLParser.AdvancedHTMLParser()

for url, values in urls.items():
    print(url)
    html = WebDados().getHTML(url) # passar url de urls
    parser.parseStr(html)
    
    itens = parser.getElementsByClassName(values[0]) # passar classe do elemtno a ser recuperado
    # posteriormente fazer um foreach para cada classe

    for item in itens:
        print(item.textContent)
        print(item.getAttribute("href"))
        print("\n")


# criar classe para armazenar dados em arquivos