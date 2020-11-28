#!/usr/bin/env python
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

    itens = parser.getElementsByClassName("feed-post-link")
    for item in itens:
        print(item.textContent)
        print(item.getAttribute("href"))
        print("\n")
    

except UnicodeDecodeError:
    print("Não foi possivel baixar do site especificado: " + url)
    print("Erro de decodificação!")