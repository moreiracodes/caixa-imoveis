'''
    models.py defines database table models
'''
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Numeric, Date
from sqlalchemy.orm import relationship

from .database import Base


class Imovel(Base):
    ''' RealEstate set basic fields to each property/real estate/land '''

    __tablename__ = "imovel"

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

    # Define a relationship between real_estate and sell_type
    tipo_venda_relacionamento = relationship(
        'TipoVenda',
        back_populates='imovel_relacionamento')


class TipoVenda(Base):
    __tablename__ = "tipo_venda"

    id = Column(Integer, primary_key=True, index=True)
    imovel_id = Column(String, ForeignKey('imovel.imovel_id'))
    financiamento = Column(Boolean, default=False)
    parcelamento = Column(Boolean, default=False)
    consorcio = Column(Boolean, default=False)

    # Define a relationship between sell_type and real_estate 
    imovel_relacionamento = relationship(
        'Imovel',
        back_populates='tipo_venda_relacionamento')
