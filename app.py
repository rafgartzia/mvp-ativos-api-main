from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote
from sqlalchemy.exc import IntegrityError
from model import Session, Ativo
from logger import logger
from schemas import *
from flask_cors import CORS
from datetime import datetime
import requests


info = Info(title="API Ativos", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação",
               description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
ativo_tag = Tag(name="Ativo",
                description="Adição, visualização e remoção de ativos à base")
cotacao_tag = Tag(name="Cotação",
                  description="Busca a última cotação de um ativo")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, swagger.
    """
    return redirect('/openapi')


@app.post('/ativo', tags=[ativo_tag],
          responses={"200": AtivoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_ativo(form: AtivoSchema):
    """Adiciona um novo ativo à base de dados

    Retorna um representação das ativos
    """
    ativo = Ativo(
        simbolo=form.simbolo,
        nome=form.nome,
        preco_medio=form.preco_medio,
        quantidade=form.quantidade
    )
    logger.debug(f"Adicionando ativo: {ativo.simbolo} - {ativo.nome}")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando ativo
        session.add(ativo)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionada ativo: {ativo.simbolo} - {ativo.nome}")
        return apresenta_ativo(ativo), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Ativo já existente na base :/"
        logger.warning(
            f"Erro ao adicionar ativo {ativo.simbolo} - {ativo.nome}, {error_msg}")
        return {"message": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(
            f"Erro ao adicionar ativo {ativo.simbolo} - {ativo.nome}, {error_msg}")
        return {"message": error_msg}, 400


@app.get('/ativos', tags=[ativo_tag],
         responses={"200": ListagemAtivosSchema, "404": ErrorSchema})
def get_ativos():
    """
        Retorna a lista com todas as ativos cadastradas no BD.
    """
    logger.debug(f"Coletando ativos ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    ativos = session.query(Ativo).all()

    if not ativos:
        # se não há ativos cadastradas
        return {"ativos": []}, 200
    else:
        logger.debug(f"%d Ativos encontrados" % len(ativos))
        # retorna a representação da ativo
        print(ativos)
        return apresenta_ativos(ativos), 200


@app.get('/ativo', tags=[ativo_tag],
         responses={"200": AtivoViewSchema, "404": ErrorSchema})
def get_ativo(query: AtivoBuscaSchema):
    """Faz a busca por um ativo.

    Retorna um representação das ativos.
    """
    ativo_simbolo = query.simbolo
    logger.debug(f"Coletando dados sobre a ativo #{ativo_simbolo}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    ativo = session.query(Ativo).filter(
        Ativo.simbolo == ativo_simbolo).first()

    if not ativo:
        # se a ativo não foi encontrada
        error_msg = "Ativo não encontrado na base :/"
        logger.warning(f"Erro ao buscar ativo {ativo_simbolo}, {error_msg}")
        return {"message": error_msg}, 404
    else:
        logger.debug(f"Ativo encontrado: {ativo_simbolo}")
        # retorna a representação da ativo
        return apresenta_ativo(ativo), 200


@app.delete('/ativo', tags=[ativo_tag],
            responses={"200": AtivoDelSchema, "404": ErrorSchema})
def del_ativo(query: AtivoBuscaSchema):
    """Deleta um Ativo a partir do descrição da ativo informada.

    Retorna um mensagem de confirmação da remoção.
    """
    ativo_simbolo = query.simbolo
    print(ativo_simbolo)
    logger.debug(f"Deletando dados sobre ativo #{ativo_simbolo}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Ativo).filter(
        Ativo.simbolo == ativo_simbolo).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado ativo #{ativo_simbolo}")
        return {"message": "Ativo removido", "id": ativo_simbolo}
    else:
        # se a ativo não foi encontrada
        error_msg = "Ativo não encontrado na base :/"
        logger.warning(
            f"Erro ao deletar ativo {ativo_simbolo}, {error_msg}")
        return {"mesage": error_msg}, 404


@app.get('/cotacao', tags=[cotacao_tag],
         responses={"200": CotacaoViewSchema, "404": ErrorSchema})
def cotacao(query: CotacaoBuscaSchema):
    """Retorna a cotação de um ativo.
    """
    simbolo = query.simbolo
    token = query.token

    logger.debug(f"Buscando cotação do ativo {ativo}")
    cotacao, status = get_cotacao(simbolo, token)

    return cotacao, status


@app.patch('/atualizacotacao', tags=[cotacao_tag],
           responses={"200": AtivoViewSchema, "404": ErrorSchema})
def update_ativo(query: CotacaoBuscaSchema):
    """
    Atualiza a cotação de um ativo.
    """
    ativo = query.simbolo
    token = query.token

    cotacao, status = get_cotacao(ativo, token)

    if status == 200:
        # criando conexão com a base
        session = Session()
        # fazendo a busca
        ativo = session.query(Ativo).filter(
            Ativo.simbolo == ativo).first()

        if not ativo:
            # se a ativo não foi encontrado
            error_msg = "Ativo não encontrado na base :/"
            logger.warning(
                f"Erro ao buscar ativo {ativo_simbolo} , {error_msg}")
            return {"message": error_msg}, 404

        else:
            ativo.cotacao = cotacao['valor']
            ativo.data_cotacao = cotacao['datahora']
            session.commit()
            return apresenta_ativo(ativo), 200
    else:
        return cotacao, status


def get_cotacao(simbolo, token):

    urlBase = "https://brapi.dev/api/quote/"
    url = urlBase + simbolo + "?range=1d&token=" + token
    response = requests.get(url)

    if response.status_code == 200:

        respJson = response.json()['results'][0]

        data_hora_iso = respJson['regularMarketTime']
        data_hora_python = datetime.strptime(
            data_hora_iso, "%Y-%m-%dT%H:%M:%S.%fZ")

        cotacao = {
            "ativo": respJson['symbol'],
            "valor": respJson['regularMarketPrice'],
            "datahora": data_hora_python
        }

        logger.debug(f"Cotacao encontrada {ativo}")
        return cotacao, 200

    else:
        erro_cotacao = {
            "ativo": "Ativo não encontrado ou token incorreto",
            "valor": None,
            "datahora": None
        }

        logger.warning("ERRO - Cotacao não encontrada")
        return erro_cotacao, 404
