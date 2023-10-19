from pydantic import BaseModel


class ImovelBase(BaseModel):

    codigo_imovel: str
    uf: str
    cidade: str
    bairro: str
    endereco: str
    preco_venda: float
    preco_avaliacao: float
    desconto: float
    descricao: str
    modalidade_venda: str
    link: str
    ativo: bool


class Imovel(ImovelBase):

    class Config:
        orm_mode = True


class ImovelCreate(ImovelBase):
    pass

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
