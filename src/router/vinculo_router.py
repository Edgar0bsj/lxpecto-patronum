from fastapi import APIRouter, Depends, status

from src.module.vinculo.vinculo_controller import VinculoController
from src.module.vinculo.vinculo_dto import VinculoCreatedDto

router = APIRouter(prefix="/vinculo", tags=["Vinculo"])


def get_controller():
    return VinculoController()


# ===============================================
# Created Vinculo
# ===============================================
@router.post("/", status_code=status.HTTP_201_CREATED)
async def vinculo_created(
    req: VinculoCreatedDto,
    controller: VinculoController = Depends(get_controller),  # noqa: B008
):

    controller.vinculo_created(req)

    return {"success": True, "detail": "Salvo com sucesso!"}
