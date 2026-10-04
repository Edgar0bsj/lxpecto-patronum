from functools import wraps
import logging

from pydantic import ValidationError

logger = logging.getLogger(__name__)


def handle_exceptions(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)

        except ValidationError as err:
            for erro in err.errors():
                campo = " -> ".join(str(loc) for loc in erro["loc"])
                mensagem = erro["msg"]
                tipo = erro["type"]
                logger.error(f"Error: Campos inválidos")
                logger.error(f"Campo: {campo} | Msg: {mensagem} | Tipo: {tipo}")
            input()
            return

        except Exception as err:
            logger.exception(">>>>>>>> Erro inesperado \n\n")
            input()
            return

    return wrapper
