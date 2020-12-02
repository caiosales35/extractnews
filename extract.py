#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib.request
import AdvancedHTMLParser

parser = AdvancedHTMLParser.AdvancedHTMLParser()

# se quiser alterar a forma de obter HTML da web, deve se alterar a forma de fazer
# requisições (atualmente com urlib); retornando o HTML da pagina na variavel text
def getHTML(url):
    response = urllib.request.urlopen(url)
    data = response.read() # a `bytes` object
    try :
        text = data.decode("utf-8")
        return text
    except UnicodeDecodeError:
        print("Não foi possivel baixar do site especificado: " + url)
        print("Erro de decodificação!")


# Se quiser alterar os sites de pesquisas e as classes para serem recuperadas;
# alterar o preenchimento da variavel URL. Atulmente tratada como um dicionario;
# pode-se fazer a leiura direta do terminar, ou ainda de um arquivo, atualmente é estatico.
# URL_PAGINA: [array com classes de elemtos para recuperar da pagina]
def getFonts():
    dicionario_fontes = {"https://g1.globo.com/": ["feed-post-link"], "https://www.saocarlosagora.com.br/": ["tituloVitrine"] }
    return dicionario_fontes

urls = getFonts()
html = getHTML("https://g1.globo.com/") # passar url de urls
  
parser.parseStr(html)
itens = parser.getElementsByClassName("feed-post-link")

for item in itens:
    print(item.textContent)
    print(item.getAttribute("href"))
    print("\n")