# NFCE-Sefaz-PE
Realiza download das informações da Nota Fiscal Eletronica (NFCe) no site da Secretária da Fazenda (SEFAZ) de Pernambuco http://nfce.sefaz.pe.gov.br/nfce-web/consultarNFCe

# How To
## QRCode
1. Leia o QRCode para obter a URL de acesso;
2. Execute o seguinte comando, substituindo o paramêtro URL pelo valor obtido no passo anterior `python3 downloader.py URL`;
3. Verifique que o arquivo XML foi salvo na pasta output;

## Chave de Acesso
Caso não seja possível ler o QRCode, obtenha a URL via a chave de acesso seguindo os passos a seguir:
1. Acessar a URL `http://nfce.sefaz.pe.gov.br/nfce-web/consultarNFCe`
2. Insira a chave de acesso, valor de 44 digitos, existente na sua nota fiscal impressa próximo ao QRCode e realize a busca;
3. Procure pela URL do QRCode existente na tag (objeto) `<qrCode>`;
4. Utilize a URL obtida no passo anterior como valor de entrada, seguindo os passos em How To > QRCode;

# TODO
## Downloader.py
- [ ] Integrar com leitura de QRCode
- [ ] Receber lista de URL como entrada

## Dados
- [ ] Criar informações de compras, preços através dos dados em XML

## Interface
- [ ] Criar uma interface para visualização
