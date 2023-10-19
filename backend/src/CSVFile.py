import csv
import requests


class CSVFile:
    def __init__(self):

        self.__uf = 'SP'

        domain = 'https://venda-imoveis.caixa.gov.br/listaweb/'
        file_name = f'Lista_imoveis_{self.__uf}.csv'
        params = '?82358242'

        self.__url = domain + file_name + params

        self.__date_created = ''

    @property
    def date_created(self):
        return self.__date_created

    def download(self):

        user_agent = 'Mozilla/5.0 \
            (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7)' + \
            'Gecko/2009021910 Firefox/3.0.7'

        headers = {
            'User-Agent': user_agent,
                }

        with requests.Session() as s:
            download = s.get(self.__url, headers=headers)
            decoded_content = download.content.decode('ISO-8859-1')

            cr = csv.reader(decoded_content.splitlines(), delimiter=';')
            my_list = list(cr)

            self.__date_created = my_list[1][3]

            i = 0
            while (i < 4):
                my_list.pop(0)
                i += 1

        return my_list
