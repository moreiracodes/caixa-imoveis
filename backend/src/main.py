from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine
from .CSVFile import CSVFile
from datetime import datetime, date
from .spider import Spider
from . import utils

# starts Base and create db tables
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
    f = CSVFile()
    data = f.download()
    file_published = f.get_formated_date().split('-')

    try:
        # convert str in array in date type to that can be compared later
        date_file = date(year=int(file_published[0]),
                         month=int(file_published[1]),
                         day=int(file_published[2]))
    except Exception as e:
        print(f'Erro de conversão da data de publição do csv: {e}')

    last_update = crud.get_last_publish_date(db=db)

    # check if there is new file to be insert
    if ((last_update is not False) and (date_file <= last_update)):

        return {
            'message': 'Os imóveis estão atualizados',
        }

    else:
        inicio = datetime.now()
        qtde = []
        for row in data:
            try:
                imovel_id = utils.input_cleaner(row[0], title=False)

                imovel_inserido_obj = crud.create_imovel(
                    db=db,
                    imovel=row,
                    publicado_em=f.get_formated_date()
                )

                qtde.append(imovel_inserido_obj)

            except Exception as e:
                print(f'Erro ao inserir imóvel {imovel_id}: {e}')

            # finally:

        fim = datetime.now()
        return {
            'published in': f.get_formated_date(),
            'message': f'Foram cadastrados {len(qtde)} imóveis',
            'inicio': inicio,
            'fim': fim,
            'tempo-processamento': (fim - inicio).total_seconds()
        }


@app.get("/imovel-detalhes/{imovel_id}")
def imovel(imovel_id: str, db: Session = Depends(get_db)):
    return crud.get_imovel(db=db, imovel_id=imovel_id)


@app.get("/imovel-complemento/{imovel_id}")
def observacoes(imovel_id: str):
    imovel_id = utils.input_cleaner(imovel_id, title=False)
    try:
        url = 'https://venda-imoveis.caixa.gov.br/' + \
            'sistema/detalhe-imovel.asp?' + \
            'hdnOrigem=index&hdnimovel=' + \
            imovel_id

        spider = Spider(url)

        if spider is None:
            raise HTTPException(
                status_code=400,
                detail="Não foi possível recuperar detalhes do imóvel"
            )

        return {
            'imovel_id': imovel_id,
            'imagem': spider.get_imagem(),
            'edital': spider.get_edital(),
            'matricula': spider.get_matricula(),
            'observacoes': spider.get_observacoes()
        }

    except Exception as e:
        print(f'Erro ao fazer web scrapping dos detalhes \
            do imóvel {imovel_id}: {e}')


@app.get("/")
def data():
    f = CSVFile()
    data = f.download()
    return {
        'date_created': f.date_created,
        'data': data
    }
