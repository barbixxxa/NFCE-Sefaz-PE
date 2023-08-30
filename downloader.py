#!/usr/bin/python3

import requests
import argparse
import os
from bs4 import BeautifulSoup

requests.packages.urllib3.disable_warnings()
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'

parser = argparse.ArgumentParser()
parser.add_argument("URL", help="URL para realizar o download EX: 'http://nfce.sefaz.pe.gov.br/nfce-web/consultarNFCe?p=00000000000000000000000000000000000000000000|0|0|0|0000000000000000000000000000000000000000'")
args = parser.parse_args()


def limparString(string):
    return string.replace(" ", "_").replace(".", "_").replace("/", "_").replace("\\", "_").lower()


def main():

    response = requests.get(args.URL, verify=False)
    arquivo_conteudo_raw = response.text

    arquivo_conteudo_xml = BeautifulSoup(arquivo_conteudo_raw, "xml")

    arquivo_conteudo_xml_prettify = arquivo_conteudo_xml.prettify()

    xNome = limparString(arquivo_conteudo_xml.find('xNome').text)

    dhRecbto = limparString(arquivo_conteudo_xml.find(
        'dhRecbto').text.split('T')[0])
    
    nProt = limparString(arquivo_conteudo_xml.find('nProt').text)

    arquivo_nome = 'nfce-' + xNome + '-' + dhRecbto + '-' + nProt +'.xml'
    arquivo_dir = 'output'
    arquivo_output_path = arquivo_dir + '/' + arquivo_nome

    if not os.path.exists(arquivo_dir):
        os.mkdir(arquivo_dir)
        print('=> Pasta NÃO encontrada!\n==> Criando o diretório: ' + arquivo_dir + '\n')

    try:
        arquivo_output = open(arquivo_output_path, 'w')
        arquivo_output.write(arquivo_conteudo_xml_prettify)
        print('=> NFCE salva com sucesso!\n==> ARQUIVO: \'' +
              arquivo_nome + '\'\n==> PASTA: \'' + arquivo_dir + '\'')
    except Exception as e:
        print('[ERROR] Arquivo NÃO foi salvo!')
        print(e)


if __name__ == "__main__":
    main()
