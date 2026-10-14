from fastapi import APIRouter, Depends, HTTPException, status
from src.module.aluno.aluno_controller import AlunoController
from src.module.aluno.aluno_dto import AlunoRequest

from sqlalchemy.exc import IntegrityError
from fastapi.responses import JSONResponse
from src.module.aluno.aluno_dto import AlunoFiltro

router = APIRouter(prefix="/aluno", tags=["Aluno"])


def get_controller():
    return AlunoController()


#
#
#
#
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_aluno(
    req: AlunoRequest, controller: AlunoController = Depends(get_controller)
):
    try:
        aluno = controller.create_aluno(req)

        return aluno

    except IntegrityError as err:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Registro duplicado ou violação de integridade no banco de dados.",
        )

    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Putz... Error inesperado meu nobre",
        )


#
#
#
#
@router.put("/{id}", status_code=status.HTTP_200_OK)
async def update_aluno(
    id: str, req: AlunoRequest, controller: AlunoController = Depends(get_controller)
):
    try:
        aluno = controller.update_aluno(id, req)

        return aluno

    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Putz... Error inesperado meu nobre",
        )


#
#
#
#
@router.get("/", status_code=status.HTTP_200_OK)
async def find_all_aluno(
    aluno_filtro: AlunoFiltro = Depends(),
    controller: AlunoController = Depends(get_controller),
):
    try:
        alunos = controller.find_all_aluno(aluno_filtro)

        return alunos

    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Putz... Error inesperado meu nobre",
        )


#
#
#
#
@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_aluno(id: str, controller: AlunoController = Depends(get_controller)):
    try:
        alunos = controller.delete_aluno(id)

        if not alunos:
            return JSONResponse(
                content={"msg": "Aluno não encontrado"},
                status_code=status.HTTP_404_NOT_FOUND,
            )

        return {"msg": "Aluno deletado com sucesso!"}

    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Putz... Error inesperado meu nobre",
        )
