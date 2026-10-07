from functools import wraps
from pydantic import ValidationError
from src.module.modalidade.errs.handle_errs import ModalidadeValidationError

import logging

logger = logging.getLogger(__name__)


def handle_exceptions(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)

        except ValidationError as err:
            logger.error("============================")
            logger.error(">>>>>>>>> Erro <<<<<<<<<<<<<")
            logger.error("============================")
            for erro in err.errors():
                campo = " -> ".join(str(loc) for loc in erro["loc"])
                mensagem = erro["msg"]
                tipo = erro["type"]
                logger.error(f"Error: Campos inválidos")
                logger.error(f"Campo: {campo} | Msg: {mensagem} | Tipo: {tipo}")
            logger.error("============================")
            input()
            return

        except ModalidadeValidationError as err:
            logger.error("============================")
            logger.error(">>>>>>>>> Erro <<<<<<<<<<<<<")
            logger.error("============================")
            logger.error(f"==>> Mensagem: {err.message} | Detalhes: {err.field}")
            logger.error("============================")
            input()
            return

        except Exception as err:
            logger.error("============================")
            logger.error(">>>>>>>>> Erro <<<<<<<<<<<<<")
            logger.error("============================")
            logger.error(f"Error Inesperado meu nobre")
            logger.error("============================")
            logger.exception(">>>>>>>> Erro \n\n")
            input()
            return

    return wrapper
