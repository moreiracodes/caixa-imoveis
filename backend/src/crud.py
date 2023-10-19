'''
    Keeps CRUD operations and utils
'''

from sqlalchemy.orm import Session
from . import models, schemas


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


def create_imovel(db: Session, imovel: list, publicado_em: str):
    '''
        Receive imovel array and publicado_em and execute a insert query
    '''
    if (not format_brl_to_usd(imovel[5])):

        # some csv rows have an addition field for address complement
        # so this field is added to previus and general field address
        # and deleted

        imovel[4] = f'{input_cleaner(imovel[4])} {input_cleaner(imovel[5])}'
        imovel.pop(5)

    db_imovel = models.Imovel(
        imovel_id=input_cleaner(imovel[0]),
        uf=input_cleaner(imovel[1], False),
        cidade=input_cleaner(imovel[2]),
        bairro=input_cleaner(imovel[3]),
        endereco=input_cleaner(imovel[4]),
        preco_venda=format_brl_to_usd(input_cleaner(imovel[5], False)),
        preco_avaliacao=format_brl_to_usd(input_cleaner(imovel[6], False)),
        desconto=float(input_cleaner(imovel[7], False)),
        descricao=input_cleaner(imovel[8], False),
        modalidade_venda=input_cleaner(imovel[9], False),
        link=input_cleaner(imovel[10], False),
        publicado_em=publicado_em
    )

    db.add(db_imovel)
    db.commit()
    db.refresh(db_imovel)
    return db_imovel


def get_last_publish_date(db: Session):
    row = db.query(models.Imovel).\
        order_by(models.Imovel.publicado_em).first()

    if (row is None):
        return False

    return row.publicado_em


# def get_users(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.User).offset(skip).limit(limit).all()

# def get_items(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.Item).offset(skip).limit(limit).all()


# def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
#     db_item = models.Item(**item.dict(), owner_id=user_id)
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)
#     return db_item
