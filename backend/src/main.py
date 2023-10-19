from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine
from .CSVFile import CSVFile
from datetime import datetime, date

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
        date_file = date(year=int(file_published[0]),
                         month=int(file_published[1]),
                         day=int(file_published[2]))
    except Exception as e:
        print(f'Vixeeeee: {e}')

    last_update = crud.get_last_publish_date(db=db)
    if (last_update is not False and date_file <= last_update):

        return {
            'message': 'Os imóveis estão atualizados',
            }

    else:
        inicio = datetime.now()
        qtde = []
        for row in data:
            qtde.append(crud.create_imovel(
                db=db,
                imovel=row,
                published_in=f.get_formated_date()))

        fim = datetime.now()
        return {
            'published in': f.get_formated_date(),
            'message': f'Foram cadastrados {len(qtde)} imóveis',
            'inicio': inicio,
            'fim': fim,
            'tempo-processamento': (fim - inicio).total_seconds()
            }


@app.get("/")
def data():
    f = CSVFile()
    data = f.download()
    return {
        'date_created': f.date_created,
        'data': data
    }
