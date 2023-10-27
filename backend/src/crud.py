'''
    Keeps CRUD operations and utils
'''


from sqlalchemy import and_, or_, not_
from sqlalchemy.orm import Session
from . import models, schemas, utils


def create_imovel(db: Session,
                  imovel: list,
                  publicado_em: str):
    '''
        Receive imovel array and publicado_em and execute a insert query
    '''
    if (not utils.format_brl_to_usd(imovel[5])):

        # some csv rows have an addition field for address complement
        # so this field is added to previus and general field address
        # and deleted

        imovel[4] = f'{utils.input_cleaner(imovel[4])} \
            {utils.input_cleaner(imovel[5])}'
        imovel.pop(5)

    imovel_id = utils.input_cleaner(imovel[0])

    db_imovel = models.Imoveis(
        imovel_id=imovel_id,
        uf=utils.input_cleaner(imovel[1], False),
        cidade=utils.input_cleaner(imovel[2]),
        bairro=utils.input_cleaner(imovel[3]),
        endereco=utils.input_cleaner(imovel[4]),
        preco_venda=utils.format_brl_to_usd(
            utils.input_cleaner(imovel[5], False)),
        preco_avaliacao=utils.format_brl_to_usd(
            utils.input_cleaner(imovel[6], False)),
        desconto=float(utils.input_cleaner(imovel[7], False)),
        descricao=utils.input_cleaner(imovel[8], False),
        modalidade_venda=utils.input_cleaner(imovel[9], False),
        link=utils.input_cleaner(imovel[10], False),
        publicado_em=publicado_em
    )

    db.add(db_imovel)
    db.commit()
    db.refresh(db_imovel)

    return db_imovel


def get_last_publish_date(db: Session):
    row = db.query(models.Imoveis).\
        order_by(models.Imoveis.publicado_em).first()

    if (row is None):
        return False

    return row.publicado_em


def get_imovel_detalhes(db: Session, imovel_id: str):
    row = db.query(models.Imoveis).where(
        models.Imoveis.imovel_id == imovel_id).first()

    if (row is None):
        return False

    return row


def get_imoveis(termos_de_busca: list, db: Session):
    search_args = []

    for attr in termos_de_busca:
        if termos_de_busca[attr] is not None:

            termos_fracionados = termos_de_busca[attr].split(' ')
            for termos in termos_fracionados:
                search_args.append(getattr(
                    models.Imoveis, attr).ilike(f'%{termos}%'))

    result = db.query(models.Imoveis
                      ).filter(and_(*search_args)).all()

    if (result is None):
        return False

    return result
