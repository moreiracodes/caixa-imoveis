from pydantic import BaseModel
# import pydantic
from typing import Union


class Imovel(BaseModel):

    imovel_id: Union[str, None] = None
    uf: Union[str, None] = None
    cidade: Union[str, None] = None
    bairro: Union[str, None] = None
    endereco: Union[str, None] = None
    preco_venda: Union[float, None] = None
    preco_avaliacao: Union[float, None] = None
    desconto: Union[float, None] = None
    descricao: Union[str, None] = None
    modalidade_venda: Union[str, None] = None
    link: Union[str, None] = None
    ativo: Union[bool, None] = None

    class Config:
        orm_mode = True


class ObservacoesBase(BaseModel):

    imovel_id: str
    imagem: str
    edital: str
    matricula: str
    observacoes: list

    class Config:
        orm_mode = True


# class AllOptional(pydantic.main.ModelMetaclass):
#     def __new__(self, name, bases, namespaces, **kwargs):
#         annotations = namespaces.get('__annotations__', {})
#         for base in bases:
#             annotations.update(base.__annotations__)
#         for field in annotations:
#             if not field.startswith('__'):
#                 annotations[field] = Optional[annotations[field]]
#         namespaces['__annotations__'] = annotations
#         return super().__new__(self, name, bases, namespaces, **kwargs)


# class ItemBase(BaseModel):
#     title: str
#     description: str | None = None


# class ItemCreate(ItemBase):
#     pass


# class Item(ItemBase):
#     id: int
#     owner_id: int

#     class Config:
#         orm_mode = True


# class UserBase(BaseModel):
#     email: str


# class UserCreate(UserBase):
#     password: str


# class User(UserBase):
#     id: int
#     is_active: bool
#     items: list[Item] = []

#     class Config:
#         orm_mode = True
