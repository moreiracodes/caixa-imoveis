
'''
    Keeps utils functions
'''
from .spider import Spider
from fastapi import HTTPException


def format_brl_to_usd(brl: str):
    '''
        Receive a BRL format money string (R$ 3.000.123,32)
        and return a float type in USD format (U$ 3000123.32 )
    '''

    
    try:
        brl = brl.replace('.', '')
        brl = brl.replace(',', '.')


        usd = float(brl)

        # ################3
        # brl = list(brl)

        # if '.' in brl:
        #     while ('.' in brl):
        #         brl.remove(".")

        # if ',' in brl:
        #     brl[brl.index(",")] = "."
        
        # result = ''

        # for i in brl:
        #     result = result + i

        # print (f'Antes: {result}')
        # usd = float(result)

        return usd

    except Exception as e:
        
        return False


def input_cleaner(input: str, title=True):
    '''
        Remove space character before and after content
        and capitalize the first letter of each word
    '''
    if (title):
        return input.lstrip().rstrip().title()
    return input.lstrip().rstrip()


def get_imovel_complemento(imovel_id):
    try:
        imovel_id = input_cleaner(imovel_id, title=False)
        spider = Spider(imovel_id)

        if spider is None:
            raise HTTPException(
                status_code=400,
                detail="Não foi possível recuperar detalhes do imóvel"
            )

        return spider.run()

    except Exception as e:
        print(f'Erro ao fazer web scrapping dos detalhes \
            do imóvel {imovel_id}: {e}')
        return False
