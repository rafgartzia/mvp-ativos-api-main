from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from model import Base


class Ativo(Base):
    __tablename__ = 'ativo'

    id = Column("pk_ativo", Integer, primary_key=True)
    simbolo = Column(String(10), unique=True, nullable=False)
    nome = Column(String(50), nullable=False)
    preco_medio = Column(Float, nullable=False)
    quantidade = Column(Integer, nullable=False)
    cotacao = Column(Float, nullable=True)
    valor_total = Column(Float, nullable=False)
    data_cotacao = Column(DateTime, nullable=True)
    data_insercao = Column(DateTime, default=datetime.now())

    def __init__(self, simbolo: str, nome: str, preco_medio: float,
                 quantidade: int, cotacao: float, valor_total: float,
                 data_cotacao: Union[DateTime, None] = None,
                 data_insercao: Union[DateTime, None] = None):
        """
        Cria um Ativo

        Argumentos:
            simbolo: str - código do ativo - ex: PETR4
            nome: str - nome do ativo - ex: Petrobras PN
            preco_medio: float - preço médio de compra, considerando todas as 
                                 compras de um mesmo ativo
            quantidade: int - quantidade de ativos em custódia
            cotacao: float - preço atualizado do ativo
            valor_total: float  - valor total atualizado - quantidade * cotacao
            data_cotacao: datetime - data da última cotação
            data_insercao: datetime - data de inserção no banco    
        """
        self.simbolo = simbolo
        self.nome = nome
        self.preco_medio = preco_medio
        self.quantidade = quantidade
        self.cotacao = cotacao
        self.valor_total = valor_total
        self.data_cotacao = data_cotacao

        # se não for informada, será o data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao
