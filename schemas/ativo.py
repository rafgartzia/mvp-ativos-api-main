from pydantic import BaseModel
from typing import Optional, List
from model.ativo import Ativo


class AtivoSchema(BaseModel):
    """ Define como um novo Ativo a ser inserido deve ser representado
    """
    simbolo: str = "PETR4"
    nome: str = "Petrobras PN"
    quantidade: int = 100
    preco_medio: float = 50.00
    """cotacao: float = 55.00
    valor_total: float = 5500.00
    data_cotacao: str = "2025-01-01 00:00:00.000"
    """


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
            "quantidade": ativo.quantidade,
            "preco_medio": ativo.preco_medio,
            "cotacao": ativo.cotacao,
            "data_cotacao": ativo.data_cotacao
        })

    return {"ativos": result}


class AtivoViewSchema(BaseModel):
    """ Define como uma ativo será retornado.
    """
    simbolo: str = "PETR4"
    nome: str = "Petrobras PN"
    quantidade: int = 100
    preco_medio: float = 50.00
    cotacao: float = 55.00
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
        "quantidade": ativo.quantidade,
        "preco_medio": ativo.preco_medio,
        "cotacao": ativo.cotacao,
        "data_cotacao": ativo.data_cotacao

    }


class CotacaoBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no codigo do ativo.
    """
    simbolo: str = "PETR4"


class CotacaoViewSchema(BaseModel):
    """ Define como uma cotação será retornado.
    """
    simbolo: str = "PETR4"
    valor: float = 100.00
    data: str = "2021-01-01"
