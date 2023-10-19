from sqlalchemy.orm import Session
from . import models, schemas


def format_brl_to_usd(brl: str):
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
    if (title):
        return input.lstrip().rstrip().title()
    return input.lstrip().rstrip()


def create_imovel(db: Session, imovel: list):

    if (not format_brl_to_usd(imovel[5])):

        imovel[4] = f'{input_cleaner(imovel[4])} {input_cleaner(imovel[5])}'
        imovel.pop(5)

    db_imovel = models.Imoveis(
        codigo_imovel=input_cleaner(imovel[0]),
        uf=input_cleaner(imovel[1], False),
        cidade=input_cleaner(imovel[2]),
        bairro=input_cleaner(imovel[3]),
        endereco=input_cleaner(imovel[4]),
        preco_venda=format_brl_to_usd(input_cleaner(imovel[5], False)),
        preco_avaliacao=format_brl_to_usd(input_cleaner(imovel[6], False)),
        desconto=float(input_cleaner(imovel[7], False)),
        descricao=input_cleaner(imovel[8], False),
        modalidade_venda=input_cleaner(imovel[9], False),
        link=input_cleaner(imovel[10], False)
    )

    db.add(db_imovel)
    db.commit()
    db.refresh(db_imovel)
    return db_imovel


# def get_user(db: Session, user_id: int):
#     return db.query(models.User).filter(models.User.id == user_id).first()


# def get_user_by_email(db: Session, email: str):
#     return db.query(models.User).filter(models.User.email == email).first()


# def get_users(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.User).offset(skip).limit(limit).all()


# def create_user(db: Session, user: schemas.UserCreate):
#     fake_hashed_password = user.password + "notreallyhashed"
#     db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user


# def get_items(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.Item).offset(skip).limit(limit).all()


# def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
#     db_item = models.Item(**item.dict(), owner_id=user_id)
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)
#     return db_item
