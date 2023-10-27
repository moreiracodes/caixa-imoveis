'''
    Spider.py é um módulo de raspagem de dados que
    busca detalhes dos imóveis não fornecidos pelo
    arquivo csv disponibilizado
'''


import requests
from bs4 import BeautifulSoup


class Spider:
    def __init__(self, imovel_id):
        self.imovel_id = imovel_id

        self.__url = 'https://venda-imoveis.caixa.gov.br/' + \
            'sistema/detalhe-imovel.asp?' + \
            'hdnOrigem=index&hdnimovel=' + \
            self.imovel_id

        user_agent = 'Mozilla/5.0 \
            (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7)' + \
            'Gecko/2009021910 Firefox/3.0.7'

        headers = {
            'User-Agent': user_agent,
        }

        self.__headers = headers
        try:
            with requests.Session() as s:
                download = s.get(self.__url, headers=self.__headers)
                decoded_content = download.content.decode('UTF-8')

            self.__soup = BeautifulSoup(decoded_content, 'html.parser')

        except Exception as e:
            print(f'Erro ao raspar dados: {e}')

    def run(self):
        return {
            'imovel_id': self.imovel_id,
            'imagem': self.get_imagem(),
            'edital': self.get_edital(),
            'matricula': self.get_matricula(),
            'observacoes': self.get_observacoes()
        }

    def get_observacoes(self):
        '''
            return format:
            ['Imóvel NÃO aceita utilização de FGTS',
            'Imóvel NÃO aceita financiamento habitacional',
            'Imóvel NÃO aceita parcelamento',
            'Imóvel NÃO aceita consórcio']
        '''

        content = self.__soup.find(
            'i',
            attrs={'class': 'fa fa-info-circle'}
        ).parent
        content = content.get_text()

        content = content.split('.')

        new_list = []
        for item in content:
            new_item = item.replace('\xa0', '').strip()
            if new_item != '':
                new_list.append(new_item)

        return new_list

    def get_imagem(self):
        '''
            return a path string from image as:
            /fotos/F000024003758821.jpg
        '''
        content = self.__soup.find(
            'img',
            attrs={'id': 'preview'}
        ).attrs['src']
        return content

    def get_edital(self):
        try:
            content = self.__soup.find(
                'a',
                string='Baixar edital e anexos'
            ).attrs['onclick']

            content = str(content).split("'")

            return content[1]
        except Exception:
            return ''

    def get_matricula(self):

        try:
            content = self.__soup.find(
                'a',
                string='Baixar matrícula do imóvel'
            ).attrs['onclick']

            content = str(content).split("'")

            return content[1]
        except Exception:
            return ''

    def __limpar_string(self, texto, remover_itens):
        for remover in remover_itens:
            texto = texto.replace(remover, '')

        return texto.strip()
