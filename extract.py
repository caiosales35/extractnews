# -*- coding: utf-8 -*-
import urllib.request
import AdvancedHTMLParser

parser = AdvancedHTMLParser.AdvancedHTMLParser()

url = "https://g1.globo.com/"
response = urllib.request.urlopen(url)
data = response.read()      # a `bytes` object
try :
    text = data.decode("utf-8") 
    parser.parseStr(text)

    items = parser.getElementsByName("items")
    items = parser.getElementsByClassName("pirulito__text-subtitle--default")
    print(items)

except UnicodeDecodeError:
    print("Não foi possivel baixar do site especificado: " + url)
    print("Erro de decodificação!")