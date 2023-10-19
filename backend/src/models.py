from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Numeric, Date
from sqlalchemy.orm import relationship

from .database import Base


class RealEstate(Base):
    __tablename__ = "real_estate"

    real_estate_id = Column(String(30),
                            primary_key=True,
                            unique=True,
                            index=True)
    federation_id = Column(String(2), nullable=False)
    city = Column(String(50), nullable=False)
    neighbor = Column(String(50), nullable=False)
    address = Column(String(200), nullable=False)
    sell_price = Column(Numeric(10, 2), nullable=False)
    evaluation_price = Column(Numeric(10, 2), nullable=False)
    discount = Column(Numeric(10, 2), nullable=False)
    description = Column(String(200), nullable=False)
    sell_type = Column(String(50), nullable=False)
    link = Column(String(150), nullable=False)
    is_active = Column(Boolean, default=True)
    published_in = Column(Date, nullable=False)

    sell_type_relationship = relationship(
        'SellType',
        back_populates='real_estate_relationship')


class SellType(Base):
    __tablename__ = "tipo_pagamento"

    id = Column(Integer, primary_key=True, index=True)
    codigo_imovel = Column(String, ForeignKey('real_estate.real_estate_id'))
    financiamento = Column(Boolean, default=False)
    parcelamento = Column(Boolean, default=False)
    consorcio = Column(Boolean, default=False)

    real_estate_relationship = relationship(
        'RealEstate',
        back_populates='sell_type_relationship')


# class User(Base):
#     __tablename__ = "users"

#     id = Column(Integer, primary_key=True, index=True)
#     email = Column(String, unique=True, index=True)
#     hashed_password = Column(String)
#     is_active = Column(Boolean, default=True)

#     items = relationship("Item", back_populates="owner")


# class Item(Base):
#     __tablename__ = "items"

#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String, index=True)
#     description = Column(String, index=True)
#     owner_id = Column(Integer, ForeignKey("users.id"))

#     owner = relationship("User", back_populates="items")
