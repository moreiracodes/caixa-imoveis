from fastapi import Depends, FastAPI, status, HTTPException
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

# Atualiza os imóveis cadastrados
@app.get("/verifica-atualizacoes")
def verifica_atualizacoes(db: Session = Depends(get_db)):

    uf_list = ['AC', 'AL', 'AP', 'AM', 'BA', 'CE', 
               'DF', 'ES', 'GO', 'MA', 'MT', 'MS',
               'MG', 'PA', 'PB', 'PR', 'PE', 'PI',
               'RJ', 'RN', 'RS', 'RO', 'RR', 'SC',
               'SP', 'SE', 'TO']
    message = []
   
    # armazena a quantidade total de imóveis inseridos 
    contador = 0

    inicio = datetime.now()

    # Percorre a lista de estados (UF)
    for uf in uf_list:
        
        # armazena a quantidade de imóveis cadastrados por estado
        imoveis_cadastrados = []

        # Faz o download do arquivo csv da respectiva uf  
        f = CSVFile(uf)

        dados_csv = f.download()
        data_csv = f.get_data_formatada()


        last_update = crud.get_last_publish_date(uf, db=db)

        # Se a data do arquivo for anterior a data da ultima inserção
        if ((last_update is not False) and (data_csv <= last_update)):

             message.append(f'{uf} Imóveis já estão atualizados')

        else:


            imovel_antigos_mantidos = [] 

            # Percorre linha por linha do arquivo baixado 
            for row in dados_csv:

                imovel_id = utils.input_cleaner(row[0], title=False)
                
                try:
                    
                    imovel_atual = crud.get_imovel_detalhes(db=db, imovel_id=imovel_id)

                    # Se o imóvel não existir, cadastra ou mantém, senão arquiva
                    if(not imovel_atual):
                  
                        # Grava o imóvel no banco e returna o objeto da inserção
                        imovel_inserido_obj = crud.create_imovel(
                            db=db,
                            imovel=row,
                            publicado_em=data_csv
                        )

                        imoveis_cadastrados.append(imovel_inserido_obj)
                    
                    else:
                        imovel_antigos_mantidos.append(imovel_id)


                except Exception as e:
                    print(f'Erro ao inserir imóvel {imovel_id}: {e}')
                finally:
                    del(imovel_id)

            
            if (imovel_antigos_mantidos):
                try:
                    # arquiva os imóveis que não estão neste arquivo 
                    crud.arquivamento_de_imoveis(imovel_antigos_mantidos, db=db)
                    raise Exception (f'Erro ao arquivar imóveis de {uf}')
                
                except Exception as e:
                    print(f'Erro no arquivamento: {e}')


            date_obj = date.strftime(data_csv, '%d/%m/%Y')

            contador = contador + len(imoveis_cadastrados)
            message.append(
                f'{uf} - {len(imoveis_cadastrados)}     Imóveis ' + 
                f'cadastrados - Publicados em ' + 
                f'{date_obj}')
             
    fim = datetime.now()
    
    return {
        'message': message,
        'total_novos_imoveis': contador,  
        'inicio': inicio,
        'fim': fim,
        'tempo-processamento': (fim - inicio).total_seconds()
    }

# Retorna detalhes de um único imóvel
@app.get("/imovel-detalhes/{imovel_id}")
def imovel(imovel_id: str, db: Session = Depends(get_db)):
    return crud.get_imovel_detalhes(db=db, imovel_id=imovel_id)

# Web Scrapping
@app.get("/imovel-complemento/{imovel_id}")
def complemento(imovel_id: str):
    return utils.get_imovel_complemento(imovel_id)

# Pesquisa
@app.get("/imoveis/",)
def lista_imoveis(
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
