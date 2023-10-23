'''
    Spider.py é um módulo de raspagem de dados que
    busca detalhes dos imóveis não fornecidos pelo
    arquivo csv disponibilizado
'''


import requests
from bs4 import BeautifulSoup


class Spider:
    def __init__(self, url):
        self.url = url

        user_agent = 'Mozilla/5.0 \
            (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7)' + \
            'Gecko/2009021910 Firefox/3.0.7'

        headers = {
            'User-Agent': user_agent,
        }

        self.__headers = headers
        try:
            with requests.Session() as s:
                download = s.get(self.url, headers=self.__headers)
                decoded_content = download.content.decode('UTF-8')

            self.__soup = BeautifulSoup(decoded_content, 'html.parser')

        except Exception as e:
            print(f'Erro ao raspar dados: {e}')

    def get_opcoes_de_pagamento(self):
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

    def get_edital_matricula_info(self):
        '''
            return format:

            {'tipo_edital': 'Concorrência Pública 0003/2023 - FARVE/SP',
            'numero_do_item': '54',
            'caminho_do_edital': '/editais/EC00032023FARVESP.PDF',
            'data_publicacao_do_edital': '13/10/2023 12:03:31',
            'caminho_da_matricula': '/editais/matricula/SP/0000240037588.pdf'}
        '''

        span = self.__soup.find(
            'div',
            attrs={'class': 'related-box'}
        ).findChildren('span')

        # tipo_edital
        tipo_edital = str(span[0])
        remover_itens = ['<span>',
                         'Edital: ',
                         '</span>'
                         ]
        tipo_edital = self.__limpar_string(tipo_edital, remover_itens)
        tipo_edital = tipo_edital.replace('\xa0', ' ')
        del remover_itens

        # número do item
        numero_do_item = str(span[1])
        remover_itens = ['<span>',
                         'Número do item: ',
                         '</span>',
                         ]
        numero_do_item = self.__limpar_string(numero_do_item, remover_itens)
        del remover_itens

        # caminho do edital
        caminho_do_edital = str(span[2])
        remover_itens = ['<span>',
                         'Número do item: ',
                         '</span>',
                         '<a class="" href="#" onclick="javascript:ExibeDoc(',
                         "'",
                         ")",
                         '"',
                         ">Baixar edital e anexos</a>"
                         ]

        caminho_do_edital = self.__limpar_string(
            caminho_do_edital, remover_itens)
        del remover_itens

        # data de publicacao do edital
        data_publicacao_do_edital = str(span[3])
        remover_itens = ['<span style="font-size:0.7em;">',
                         'Número do item: ',
                         '</span>',
                         '(Edital publicado em: ',
                         ')'
                         ]

        data_publicacao_do_edital = self.__limpar_string(
            data_publicacao_do_edital, remover_itens)
        del remover_itens

        # caminho da matricula
        caminho_da_matricula = str(span[4])
        remover_itens = ['<span>',
                         'Número do item: ',
                         '</span>',
                         '<a class="" href="#" onclick="javascript:ExibeDoc(',
                         "'",
                         ")",
                         '"',
                         ">Baixar matrícula do imóvel</a>"
                         ]

        caminho_da_matricula = self.__limpar_string(
            caminho_da_matricula, remover_itens)
        del remover_itens

        print()

        return {
            'tipo_edital': f'{tipo_edital}',
            'numero_do_item': f'{numero_do_item}',
            'caminho_do_edital': f'{caminho_do_edital}',
            'data_publicacao_do_edital': f'{data_publicacao_do_edital}',
            'caminho_da_matricula': f'{caminho_da_matricula}',
        }

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

    def __limpar_string(self, texto, remover_itens):
        for remover in remover_itens:
            texto = texto.replace(remover, '')

        return texto.strip()


url = 'https://venda-imoveis.caixa.gov.br/' + \
    'sistema/detalhe-imovel.asp?' + \
    'hdnOrigem=index&hdnimovel=240037588'

page = Spider(url)
print(url)
print()
print(page.get_imagem())
print()
print(page.get_opcoes_de_pagamento())
print()
print(page.get_edital_matricula_info())
