from pathlib import Path

from pydantic import BaseModel
import pandas as pd


def import_csv_entity[T: BaseModel](
    CACHE: dict[str, T],
    entity: T,
    arquivo_name: dict = {"Modalidades": "manager/teaching-modality.unig_producao.csv"},
):
    path_output = Path.cwd() / "manager"
    path_output.mkdir(exist_ok=True, parents=True)

    entitys = CACHE[entity.__name__]

    list_entity = [e.to_manager() for e in entitys]

    df = pd.DataFrame(list_entity)

    for k, v in arquivo_name.items():

        if str(k) == entity.__name__:
            df.to_csv(v, index=False, sep=";", encoding="utf-8")
