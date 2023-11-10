'''
    crud.py 

    Esse módulo contém as operações de CRU
    
    Autor: moreiracondes <moreiracodes@proton.me>
'''


from sqlalchemy import and_, or_, not_
from sqlalchemy.orm import Session
from . import models, schemas, utils
from datetime import date


def create_imovel(db: Session,
                  imovel: list,
                  publicado_em: str):
    '''
        Receive imovel array and publicado_em and execute a insert query
    '''
    while (not utils.format_brl_to_usd(imovel[5])):

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


def get_last_publish_date(uf: str, db: Session):
    model_imovel = models.Imoveis

    row = db.query(model_imovel).filter(and_(
        model_imovel.uf == uf)).order_by(
            model_imovel.publicado_em).first()

    if (row is None):
        return False

    return row.publicado_em


def get_imovel_detalhes(db: Session, imovel_id: str):
    row = db.query(models.Imoveis).where(
        models.Imoveis.imovel_id == imovel_id).first()

    if (row is None):
        return False

    return row


def get_imoveis(termos_de_busca: list, order_by:int, db: Session):
    
    model_imoveis = models.Imoveis

    order_by_opt = [
        model_imoveis.preco_venda.asc(),
        model_imoveis.preco_venda.desc(),
        model_imoveis.preco_avaliacao.asc(),
        model_imoveis.preco_avaliacao.desc(),
        model_imoveis.desconto.asc(),
        model_imoveis.desconto.desc(),
        model_imoveis.cidade.asc(),
        model_imoveis.cidade.desc(),
        model_imoveis.bairro.asc(),
        model_imoveis.bairro.desc(),
        model_imoveis.uf.asc(),
        model_imoveis.uf.desc(),
    ]
    search_args = []

    for attr in termos_de_busca:
            
        if termos_de_busca[attr] is not None:

            if (type(termos_de_busca[attr]) is float):

                if('_min' in attr):
                    substring_end = attr.rfind("_")
                    search_args.append(getattr(
                            model_imoveis, attr[0:substring_end]) >= termos_de_busca[attr])
                if('_max' in attr):
                    substring_end = attr.rfind("_")
                    search_args.append(getattr(
                            model_imoveis, attr[0:substring_end]) <= termos_de_busca[attr])
            else:
                termos_fracionados = termos_de_busca[attr].split(' ')
                for termos in termos_fracionados:
                    search_args.append(getattr(
                        model_imoveis, attr).ilike(f'%{termos}%'))

    result = db.query(model_imoveis
                      ).filter(and_(*search_args)).order_by(order_by_opt[order_by]).all()

    if (result is None):
        return False

    return result


def arquivamento_de_imoveis(imovel_antigos_mantidos: list, db: Session):

    model_imovel = models.Imoveis

    search_args = [model_imovel.ativo is True]

    for imovel_antigo_id in imovel_antigos_mantidos:

        # Se o imóvel estiver na lista dos matidos ele não deve ser arquivado
        search_args.append(model_imovel.imovel_id(not_(imovel_antigo_id)))

        # Senão ele deve ser arquivado

    row = db.query(model_imovel).filter(or_(
        *search_args)).update({
            model_imovel.ativo: False
        })


    if (row is None):
        return False

    return row
    


