from fastapi import APIRouter, Depends, File, UploadFile, status
from fastapi.responses import JSONResponse, StreamingResponse

from src.module.aluno.aluno_controller import AlunoController
from src.module.aluno.aluno_dto import (
    AlunoCreate,
    AlunoFiltro,
    AlunoUpdate,
)

router = APIRouter(prefix="/aluno", tags=["Aluno"])


# ===============================================
# Dependencia - Controller
# ===============================================
def get_controller():
    return AlunoController()


# ===============================================
# Created Aluno
# ===============================================
@router.post("/")
async def aluno_created(
    req: AlunoCreate,
    controller: AlunoController = Depends(get_controller),  # noqa: B008
):

    controller.aluno_created(req)

    return JSONResponse(
        content={"success": True, "detail": "Salvo com sucesso!"},
        status_code=status.HTTP_201_CREATED,
    )


# ===============================================
# Updated Aluno
# ===============================================
@router.patch("/{id}")
async def aluno_updated(
    id: str,
    req: AlunoUpdate,
    controller: AlunoController = Depends(get_controller),  # noqa: B008
):

    controller.aluno_updated(id, req)

    return JSONResponse(
        content={"success": True, "detail": "Aluno Atualizado com sucesso!"},
        status_code=status.HTTP_200_OK,
    )


# ===============================================
# Get All Aluno
# ===============================================
@router.get("/", status_code=status.HTTP_200_OK)
async def aluno_get_all(
    aluno_filtro: AlunoFiltro = Depends(),  # noqa: B008
    controller: AlunoController = Depends(get_controller),  # noqa: B008
):
    alunos = controller.aluno_get_all(aluno_filtro)

    return JSONResponse(
        content=alunos,
        status_code=status.HTTP_200_OK,
    )


# ===============================================
# Delete Aluno
# ===============================================
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def aluno_delete(
    id: str, controller: AlunoController = Depends(get_controller)  # noqa: B008
):

    controller.aluno_delete(id)


# ===============================================
# Import Excel Aluno
# ===============================================
@router.post("/importar-excel/", status_code=status.HTTP_200_OK)
async def aluno_import_xlsx(
    file: UploadFile = File(...),  # noqa: B008
    controller: AlunoController = Depends(get_controller),  # noqa: B008
):

    iterfile = await controller.aluno_import_xlsx(file)

    return StreamingResponse(
        iterfile(),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=aluno_errs.xlsx"},
    )


# ===============================================
# Tamplete Excel Aluno
# ===============================================
@router.get("/export-tamplete-xlsx/", status_code=status.HTTP_200_OK)
async def export_excel_aluno_tamplete(
    controller: AlunoController = Depends(get_controller),  # noqa: B008
):

    iterfile = await controller.export_excel_tamplete()

    return StreamingResponse(
        iterfile(),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=tamplete_aluno.xlsx"},
    )
