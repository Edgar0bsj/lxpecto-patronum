from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from src.module.aluno.aluno_controller import AlunoController
from src.module.aluno.aluno_dto import AlunoRequest

from sqlalchemy.exc import IntegrityError
from fastapi.responses import JSONResponse, StreamingResponse
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


#
#
#
#
@router.post("/importar-excel/", status_code=status.HTTP_200_OK)
async def importar_excel_aluno(
    file: UploadFile = File(...), controller: AlunoController = Depends(get_controller)
):

    try:

        iterfile = await controller.import_excel_aluno(file)

        return StreamingResponse(
            iterfile(),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": "attachment; filename=aluno_errs.xlsx"},
        )

    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(err),
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
@router.get("/export-tamplete-xlsx/", status_code=status.HTTP_200_OK)
async def export_excel_aluno_tamplete(
    controller: AlunoController = Depends(get_controller),
):

    try:

        iterfile = await controller.export_excel_tamplete()

        return StreamingResponse(
            iterfile(),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": "attachment; filename=tamplete_aluno.xlsx"},
        )

    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(err),
        )
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Putz... Error inesperado meu nobre",
        )
