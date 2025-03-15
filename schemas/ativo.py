from pydantic import BaseModel
from typing import Optional, List
from model.ativo import Ativo


class AtivoSchema(BaseModel):
    """ Define como um novo Ativo a ser inserido deve ser representado
    """
    simbolo: str = "PETR4"
    nome: str = "Petrobras PN"
    preco_medio: float = 50.00
    quantidade: int = 100
    cotacao: float = 55.00
    valor_total: float = 5500.00
    data_cotacao: str = "2025-01-01 00:00:00.000"


class AtivoBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no codigo do mapa da ativo.
    """
    simbolo: str = "PETR4"


class ListagemAtivosSchema(BaseModel):
    """ Define como uma listagem de progressões será retornada.
    """
    ativos: List[AtivoSchema]


def apresenta_ativos(ativos: List[AtivoSchema]):
    """ Retorna uma representação da ativo seguindo o schema definido em
        AtivoViewSchema.
    """
    result = []
    for ativo in ativos:
        result.append({
            "simbolo": ativo.simbolo,
            "nome": ativo.nome,
            "preco_medio": ativo.preco_medio,
            "quantidade": ativo.quantidade
        })

    return {"ativos": result}


class AtivoViewSchema(BaseModel):
    """ Define como uma ativo será retornado.
    """
    simbolo: str = "PETR4"
    nome: str = "Petrobras PN"
    preco_medio: float = 50.00
    quantidade: int = 100
    cotacao: float = 55.00
    valor_total: float = 5500.00
    data_cotacao: str = "2025-01-01 00:00:00.000"


class AtivoDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    simbolo: str
    nome: str


def apresenta_ativo(ativo: Ativo):
    """ Retorna uma representação da ativo seguindo o schema definido em
        AtivoViewSchema.
    """
    return {
        "simbolo": ativo.simbolo,
        "nome": ativo.nome,
        "preco_medio": ativo.preco_medio,
        "quantidade": ativo.quantidade
    }
