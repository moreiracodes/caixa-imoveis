from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from typing import Union
from . import crud, models, schemas
from .database import SessionLocal, engine
from .CSVFile import CSVFile
from datetime import datetime, date
from . import utils

# starts Base and create db models
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/data")
def CreateImovel(db: Session = Depends(get_db)):

    uf_list = ['AC', 'AL', 'AP', 'AM', 'BA', 'CE', 
               'DF', 'ES', 'GO', 'MA', 'MT', 'MS',
               'MG', 'PA', 'PB', 'PR', 'PE', 'PI',
               'RJ', 'RN', 'RS', 'RO', 'RR', 'SC',
               'SP', 'SE', 'TO']
    message = []
    inicio = datetime.now()
    imoveis_cadastrados_por_uf = []
    for uf in uf_list:

        f = CSVFile(uf)
        data = f.download()
        file_published = f.get_formated_date().split('-')
        try:
            # convert str in array in date type to that can be compared later
            date_file = date(year=int(file_published[0]),
                            month=int(file_published[1]),
                                day=int(file_published[2]))
        except Exception as e:
            print(f'Erro de conversão da data de publição do csv de {uf}: {e}')

        last_update = crud.get_last_publish_date(uf, db=db)

        # check if there is new file to be insert
        if ((last_update is not False) and (date_file <= last_update)):

             message.append(f'Os imóveis de {uf} já estão atualizados')

        else:
            imoveis_cadastrados = []
            for row in data:
                
                imovel_id = utils.input_cleaner(row[0], title=False)
               
                try:
                
                    imovel_inserido_obj = crud.create_imovel(
                        db=db,
                        imovel=row,
                        publicado_em=f.get_formated_date()
                    )

                    imoveis_cadastrados.append(imovel_inserido_obj)

                except Exception as e:
                    print(f'Erro ao inserir imóvel {imovel_id}: {e}')
                finally:
                    del(imovel_id)
            imoveis_cadastrados_por_uf.append(len(imoveis_cadastrados))
            message.append(f'Foram cadastrados {len(imoveis_cadastrados)} imóveis de {uf}')
    
    fim = datetime.now()
    return {
        'published in': f.get_formated_date(),
        'message': message,
        'total_novos_imoveis': '',  
        'inicio': inicio,
        'fim': fim,
        'tempo-processamento': (fim - inicio).total_seconds()
    }


@app.get("/imovel-detalhes/{imovel_id}")
def imovel(imovel_id: str, db: Session = Depends(get_db)):
    return crud.get_imovel_detalhes(db=db, imovel_id=imovel_id)


@app.get("/imovel-complemento/{imovel_id}")
def observacoes(imovel_id: str):
    return utils.get_imovel_complemento(imovel_id)


@app.get("/imoveis/",)
def read_imoveis(
    imovel_id: Union[str, None] = None,
    uf: Union[str, None] = None,
    cidade: Union[str, None] = None,
    bairro: Union[str, None] = None,
    endereco: Union[str, None] = None,
    preco_venda_min: Union[float, None] = None,
    preco_venda_max: Union[float, None] = None,
    preco_avaliacao_min: Union[float, None] = None,
    preco_avaliacao_max: Union[float, None] = None,
    desconto_min: Union[float, None] = None,
    desconto_max: Union[float, None] = None,
    descricao: Union[str, None] = None,
    modalidade_venda: Union[str, None] = None,
    order_by: Union[int, None] = 0,
    db: Session = Depends(get_db),
):

    termos_de_busca = {
        'imovel_id': imovel_id,
        'uf': uf,
        'cidade': cidade,
        'bairro': bairro,
        'endereco': endereco,
        'preco_venda_min': preco_venda_min,
        'preco_venda_max': preco_venda_max,
        'preco_avaliacao_min': preco_avaliacao_min,
        'preco_avaliacao_max': preco_avaliacao_max,
        'desconto_min': desconto_min,
        'desconto_max': desconto_max,
        'descricao': descricao,
        'modalidade_venda': modalidade_venda,
    }
    
    return crud.get_imoveis(termos_de_busca, order_by, db=db)
