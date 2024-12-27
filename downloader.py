#!/usr/bin/python3

import requests
import argparse
import os
from bs4 import BeautifulSoup

requests.packages.urllib3.disable_warnings()
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--url", help="URL para realizar o download EX: 'http://nfce.sefaz.pe.gov.br/nfce-web/consultarNFCe?p=00000000000000000000000000000000000000000000|0|0|0|0000000000000000000000000000000000000000'")
parser.add_argument("-f", "--file", help="Arquivo txt contendo URLs para realizar o download")
args = parser.parse_args()

def limparString(string):
    return string.replace(" ", "_").replace(".", "_").replace("/", "_").replace("\\", "_").lower()

def processar_url(url, erros):
    try:
        response = requests.get(url, verify=False)
        arquivo_conteudo_raw = response.text

        arquivo_conteudo_xml = BeautifulSoup(arquivo_conteudo_raw, "xml")

        xNome = limparString(arquivo_conteudo_xml.find('xNome').text)
        dhRecbto = limparString(arquivo_conteudo_xml.find('dhRecbto').text.split('T')[0])
        nProt = limparString(arquivo_conteudo_xml.find('nProt').text)

        arquivo_nome = 'nfce-' + xNome + '-' + dhRecbto + '-' + nProt + '.xml'
        arquivo_dir = 'output'
        arquivo_output_path = os.path.join(arquivo_dir, arquivo_nome)

        if not os.path.exists(arquivo_dir):
            os.mkdir(arquivo_dir)
            print('=> Pasta NÃO encontrada!\n==> Criando o diretório: ' + arquivo_dir + '\n')

        if os.path.exists(arquivo_output_path):
            print('=> Arquivo já existe: ' + arquivo_output_path)
            return

        with open(arquivo_output_path, 'w') as arquivo_output:
            arquivo_output.write(arquivo_conteudo_xml.prettify())
            print('=> NFCE salva com sucesso!\n==> ARQUIVO: \'' + arquivo_nome + '\'\n==> PASTA: \'' + arquivo_dir + '\'')
    except Exception as e:
        print(f'[ERROR] Falha ao processar URL {url}')
        print(e)
        erros.append(url)

def main():
    erros = []
    
    if args.url:
        processar_url(args.url, erros)
    elif args.file:
        try:
            with open(args.file, 'r') as file:
                urls = file.readlines()
                for url in urls:
                    processar_url(url.strip(), erros)
        except Exception as e:
            print(f'[ERROR] Falha ao ler o arquivo {args.file}')
            print(e)
            erros.append(args.file)
    else:
        print("Por favor, forneça uma URL ou um arquivo txt com URLs.")
    
    if erros:
        with open('erros.txt', 'w') as erro_file:
            for url in erros:
                erro_file.write(url + '\n')

if __name__ == "__main__":
    main()
