from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from fastapi.responses import JSONResponse, StreamingResponse

from src.module.aluno.aluno_controller import AlunoController
from src.module.aluno.aluno_dto import (
    AlunoCreate,
    AlunoFiltro,
    AlunoUpdate,
)

router = APIRouter(prefix="/aluno", tags=["Aluno"])


def get_controller():
    return AlunoController()


@router.post("/")
async def aluno_created(
    req: AlunoCreate, controller: AlunoController = Depends(get_controller)
):

    controller.aluno_created(req)

    return JSONResponse(
        content={"success": True, "detail": "Salvo com sucesso!"},
        status_code=status.HTTP_201_CREATED,
    )


#
#
#
#
@router.patch("/{id}")
async def aluno_updated(
    id: str, req: AlunoUpdate, controller: AlunoController = Depends(get_controller)
):

    controller.aluno_updated(id, req)

    return JSONResponse(
        content={"success": True, "detail": "Aluno Atualizado com sucesso!"},
        status_code=status.HTTP_200_OK,
    )


#
#
#
#
@router.get("/", status_code=status.HTTP_200_OK)
async def aluno_get_all(
    aluno_filtro: AlunoFiltro = Depends(),
    controller: AlunoController = Depends(get_controller),
):
    alunos = controller.aluno_get_all(aluno_filtro)

    return JSONResponse(
        content=alunos,
        status_code=status.HTTP_200_OK,
    )


#
#
#
#
@router.delete("/{id}")
async def aluno_delete(id: str, controller: AlunoController = Depends(get_controller)):

    controller.aluno_delete(id)

    return JSONResponse(
        content=None,
        status_code=status.HTTP_204_NO_CONTENT,
    )


#
#
#
#
@router.post("/importar-excel/", status_code=status.HTTP_200_OK)
async def aluno_import_xlsx(
    file: UploadFile = File(...), controller: AlunoController = Depends(get_controller)
):

    iterfile = await controller.aluno_import_xlsx(file)

    return StreamingResponse(
        iterfile(),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=aluno_errs.xlsx"},
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


#
#
#
#
@router.get("/export-lxp-manager/", status_code=status.HTTP_200_OK)
async def export_lxp_manager(
    controller: AlunoController = Depends(get_controller),
):
    try:

        iterfile = await controller.export_lxp_manager()

        return StreamingResponse(
            iterfile(),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": "attachment; filename=person_manager.csv"},
        )

    except ValueError as err:
        raise
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(err),
        )
    except Exception as err:
        raise
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Putz... Error inesperado meu nobre",
        )
