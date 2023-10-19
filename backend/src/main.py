from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine
from .CSVFile import CSVFile
from datetime import datetime

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
    inicio = datetime.now()
    qtde = []
    for row in data:
        qtde.append(crud.create_imovel(db=db, imovel=row))

    fim = datetime.now()
    return {
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
