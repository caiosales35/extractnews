#!/usr/bin/env python
# -*- coding: utf-8 -*-
#import urllib.request 
from urllib.request import Request, urlopen
import AdvancedHTMLParser
import abc
import csv
import codecs
import sys

#Essa classe administra os argumentos de entrada e os disponibiliza futuramente
class ManagerArgs():
    def __init__(self, args):
        self._args = args

    def get_url_arg(self):
        return self._args[0]
    def get_class_arg(self):
        return self._args[1]
    def get_tag_arg(self):
        return self._args[2]
    def get_outputfile_arg(self):
        return self._args[3]

    def parsedArgs(self,args):
        if(len(args) != 4):
            print('Argumentos insuficientes')
            print('Use: extract.py <url> <classe> <tag> <arquivodesaida.csv>')
            return
        else:
            return ManagerArgs(args)

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
        self._classe = classe
        self._url = url
        html = WebDados().getHTML(self._url)
        self._parser = AdvancedHTMLParser.AdvancedHTMLParser()
        self._parser.parseStr(html)

    @abc.abstractmethod
    def getNews(self):
        return

class PortalDeNoticias(extractNews):
    def getNews(self):
        itens = self._parser.getElementsByClassName(self._classe)
        dados = dict([])
        for item in itens:
            dados[item.textContent] = item.getAttribute("href")
        return dados

'''
# Agora este dicionario serve somente para consulta.
# Para pesquisar diferentes urls, classes, tags e nome do arquivo csv não é preciso fazer alterações aqui,
# basta informar os novos parametros na linha de comando (:
# Elemento: [URL, CLASSE, TAG]
def getFonts():
    dicionario_fontes = [
            ["https://g1.globo.com/", "feed-post-link", None], 
            ["https://www.saocarlosagora.com.br/", "tituloVitrine", None],
            ["https://www.saocarlosagora.com.br/ultimas-noticias/", "ultimas-noticias", "h3"],
            ["https://noticias.uol.com.br/", "thumb-caption", None]
    ]
    
    return dicionario_fontes
'''
class WriteCSV():
    def __init__(self, outputfile, queryResult):
        #trata o caso em que o usuário digita sem indicar a extensão
        nameFile = outputfile if(".csv" in outputfile) else outputfile + '.csv' 
        try:
            with codecs.open(nameFile, 'w', 'utf-8') as csv_file:  
                writer = csv.writer(csv_file)
                for key, value in queryResult.items():
                    writer.writerow([key, value])
            print('Arquivo ' + nameFile + ' gerado com sucesso.')
            csv_file.close()
        except IOError:         
            print("Operação de saída falhou. Não foi possível gerar o arquivo.")

def main(argv):
   parsedArgs = ManagerArgs(None).parsedArgs(argv)
   if(parsedArgs is None):
        return

   #recebe os dados da consulta 
   dados = PortalDeNoticias(parsedArgs.get_url_arg(), parsedArgs.get_class_arg(), parsedArgs.get_tag_arg()).getNews()
   
   #escreve os resultados em um arquivo csv 
   WriteCSV(parsedArgs.get_outputfile_arg(), dados)

if __name__ == "__main__":
    main(sys.argv[1:])