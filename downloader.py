#!/usr/bin/python3

import requests
import argparse
import os
from bs4 import BeautifulSoup
import csv
import xml.etree.ElementTree as ET
from datetime import datetime

requests.packages.urllib3.disable_warnings()
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--url", help="URL para realizar o download EX: 'http://nfce.sefaz.pe.gov.br/nfce-web/consultarNFCe?p=00000000000000000000000000000000000000000000|0|0|0|000000000000000000000'")
parser.add_argument("-f", "--file", help="Arquivo txt contendo URLs para realizar o download")
parser.add_argument("--xml", help="Arquivo XML para converter em CSV")
parser.add_argument("--csv", help="Arquivo de saída CSV")
args = parser.parse_args()

def limparString(string):
    return string.replace(" ", "_").replace(".", "_").replace("/", "_").replace("\\", "_").lower()

def remover_espacos(string):
    return ''.join(string.split())

def formatar_data(data_str):
    try:
        data = datetime.strptime(data_str, '%Y-%m-%dT%H:%M:%S%z')
        return data.strftime('%d/%m/%Y')
    except ValueError:
        return data_str

def substituir_pontos_por_virgulas(valor):
    return valor.replace('.', ',')

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

def xml_to_csv(xml_file, csv_file):
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()

        # Find the infNFe node
        infNFe = root.find('.//{http://www.portalfiscal.inf.br/nfe}infNFe')

        if infNFe is None:
            raise ValueError("Tag infNFe não encontrada no arquivo XML.")

        with open(csv_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            
            # Write the headers
            header = ["dhEmi", "cProd", "xProd", "qCom", "vUnCom", "vProd", "uTrib"]
            writer.writerow(header)
            
            # Extract data and write to CSV
            dhEmi_elem = infNFe.find('.//{http://www.portalfiscal.inf.br/nfe}dhEmi')
            dhEmi = formatar_data(remover_espacos(dhEmi_elem.text)) if dhEmi_elem is not None else ''
            for det in infNFe.findall('.//{http://www.portalfiscal.inf.br/nfe}det'):
                prod = det.find('.//{http://www.portalfiscal.inf.br/nfe}prod')
                if prod is not None:
                    cProd_elem = prod.find('.//{http://www.portalfiscal.inf.br/nfe}cProd')
                    xProd_elem = prod.find('.//{http://www.portalfiscal.inf.br/nfe}xProd')
                    qCom_elem = prod.find('.//{http://www.portalfiscal.inf.br/nfe}qCom')
                    vUnCom_elem = prod.find('.//{http://www.portalfiscal.inf.br/nfe}vUnCom')
                    vProd_elem = prod.find('.//{http://www.portalfiscal.inf.br/nfe}vProd')
                    uTrib_elem = prod.find('.//{http://www.portalfiscal.inf.br/nfe}uTrib')
                    cProd = remover_espacos(cProd_elem.text) if cProd_elem is not None else ''
                    xProd = remover_espacos(xProd_elem.text) if xProd_elem is not None else ''
                    qCom = remover_espacos(qCom_elem.text) if qCom_elem is not None else ''
                    vUnCom = substituir_pontos_por_virgulas(remover_espacos(vUnCom_elem.text)) if vUnCom_elem is not None else ''
                    vProd = substituir_pontos_por_virgulas(remover_espacos(vProd_elem.text)) if vProd_elem is not None else ''
                    uTrib = remover_espacos(uTrib_elem.text) if uTrib_elem is not None else ''
                    writer.writerow([dhEmi, cProd, xProd, qCom, vUnCom, vProd, uTrib])

        print(f'=> Dados do XML salvos com sucesso no arquivo CSV: {csv_file}')
    except Exception as e:
        print(f'[ERROR] Falha ao processar o arquivo XML {xml_file}')
        print(e)

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
    elif args.xml and args.csv:
        xml_to_csv(args.xml, args.csv)
    else:
        print("Por favor, forneça uma URL, um arquivo txt com URLs, ou um arquivo XML e um arquivo CSV para saída.")
    
    if erros:
        with open('erros.txt', 'w') as erro_file:
            for url in erros:
                erro_file.write(url + '\n')

if __name__ == "__main__":
    main()
