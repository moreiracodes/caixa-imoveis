
'''
    Keeps utils functions
'''


def format_brl_to_usd(brl: str):
    '''
        Receive a BRL format money string (R$ 3.000.123,32)
        and return a float type in USD format (U$ 3000123.32 )
    '''
    try:
        brl = list(brl)

        while ('.' in brl):
            brl.remove(".")

        brl[brl.index(",")] = "."
        result = ''
        for i in brl:
            result = result + i

        usd = float(result)

        return usd

    except Exception:
        return False


def input_cleaner(input: str, title=True):
    '''
        Remove space character before and after content
        and capitalize the first letter of each word
    '''
    if (title):
        return input.lstrip().rstrip().title()
    return input.lstrip().rstrip()
