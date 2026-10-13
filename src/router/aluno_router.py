from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from src.module.aluno.aluno_controller import AlunoController
from src.module.aluno.aluno_dto import AlunoRequest

router = APIRouter(prefix="/aluno", tags=["Aluno"])


def get_controller():
    return AlunoController()


#
#
#
#
@router.post("/")
async def create_aluno(
    req: AlunoRequest, controller: AlunoController = Depends(get_controller)
):
    aluno = controller.create_aluno(req)

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=aluno)
