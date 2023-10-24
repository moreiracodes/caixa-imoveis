'''
    models.py defines database table models
'''
from sqlalchemy import Boolean, Column, String, Numeric, Date

from .database import Base


class Imoveis(Base):
    ''' RealEstate set basic fields to each property/real estate/land '''

    __tablename__ = "imoveis"

    imovel_id = Column(String(30),
                       primary_key=True,
                       unique=True,
                       index=True)
    uf = Column(String(2), nullable=False)
    cidade = Column(String(50), nullable=False)
    bairro = Column(String(50), nullable=False)
    endereco = Column(String(200), nullable=False)
    preco_venda = Column(Numeric(10, 2), nullable=False)
    preco_avaliacao = Column(Numeric(10, 2), nullable=False)
    desconto = Column(Numeric(10, 2), nullable=False)
    descricao = Column(String(200), nullable=False)
    modalidade_venda = Column(String(50), nullable=False)
    link = Column(String(150), nullable=False)
    ativo = Column(Boolean, default=True)
    publicado_em = Column(Date, nullable=False)
