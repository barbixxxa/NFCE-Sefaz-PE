import requests
import argparse
import lxml
from bs4 import BeautifulSoup

requests.packages.urllib3.disable_warnings()
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'

parser = argparse.ArgumentParser()
parser.add_argument("URL", help="URL para realizar o download EX: 'http://nfce.sefaz.pe.gov.br/nfce-web/consultarNFCe?p=00000000000000000000000000000000000000000000|0|0|0|0000000000000000000000000000000000000000'")
args = parser.parse_args()


def limparString(string):
    return string.replace(" ", "_").replace(".", "_").lower()


def main():

    response = requests.get(args.URL, verify=False)
    arquivo_conteudo_raw = response.text

    arquivo_conteudo_xml = BeautifulSoup(arquivo_conteudo_raw, "xml")

    arquivo_conteudo_xml_prettify = arquivo_conteudo_xml.prettify()

    xNome = limparString(arquivo_conteudo_xml.find('xNome').text)

    dhRecbto = limparString(arquivo_conteudo_xml.find(
        'dhRecbto').text.split('T')[0])

    arquivo_nome = 'nfce-' + xNome + '-' + dhRecbto + '.xml'
    arquivo_dir = '/home/theeam/Documents/NFCE-Sefaz-PE-virtualEnv/NFCE-Sefaz-PE/output/'

    try:
        arquivo_output = open(arquivo_dir+arquivo_nome, 'w')
        arquivo_output.write(arquivo_conteudo_xml_prettify)
        print('=> NFCE salva com sucesso!\n==> ARQUIVO: \'' +
              arquivo_nome + '\'\n==> PASTA: \'' + arquivo_dir + '\'')
    except:
        print('Erro ao salvar o arquivo!')


if __name__ == "__main__":
    main()
