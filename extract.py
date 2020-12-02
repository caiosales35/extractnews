#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib.request
import AdvancedHTMLParser
import abc

# interface de requisições, obrigatorio implementar um metodo que retorne um html
class Requests(metaclass=abc.ABCMeta):
     @abc.abstractmethod
     def getHTML(self, url):
        return

class WebRequest(Requests):
    def __init__(self, encode="utf-8"):
        self._encode = encode
    # Se quiser alterar a forma de obter HTML da web, deve se alterar a forma de fazer
    # requisições (atualmente com urlib); retornando o HTML da pagina na variavel text
    def getHTML(self, url):
        response = urllib.request.urlopen(url).read()
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



# Se quiser alterar os sites de pesquisas e as classes dos elementos para serem recuperados;
# alterar o preenchimento da variavel dicionario_fontes. Atulmente tratada como um dicionario;
# pode-se fazer a leiura direta do terminar, ou ainda de um arquivo, atualmente é estatico.
# URL: [array com classes de elemtos para recuperar da pagina]
def getFonts():
    dicionario_fontes = {"https://g1.globo.com/": ["feed-post-link"], "https://www.saocarlosagora.com.br/": ["tituloVitrine"] }
    return dicionario_fontes

parser = AdvancedHTMLParser.AdvancedHTMLParser()
urls = getFonts()
html = WebRequest().getHTML("https://g1.globo.com/") # passar url de urls
  
parser.parseStr(html)
itens = parser.getElementsByClassName("feed-post-link")

for item in itens:
    print(item.textContent)
    print(item.getAttribute("href"))
    print("\n")


# criar funcao para armazenar dados em arquivos