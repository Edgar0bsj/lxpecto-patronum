from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from sqlalchemy.exc import IntegrityError

from src.module.vinculo.vinculo_controller import VinculoController
from src.module.vinculo.vinculo_dto import VinculoDto, VinculoFiltro

router = APIRouter(prefix="/vinculo", tags=["Vinculo"])


def get_controller():
    return VinculoController()


#
#
#
#
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_vinculo(
    req: VinculoDto, controller: VinculoController = Depends(get_controller)
):
    try:
        vinculo = controller.create_vinculo(req)

        return vinculo

    except IntegrityError as err:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Registro duplicado ou violação de integridade no banco de dados.",
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
@router.put("/{id}", status_code=status.HTTP_200_OK)
async def update_vinculo(
    id: str,
    req: VinculoDto,
    controller: VinculoController = Depends(get_controller),
):
    try:
        vinculo = controller.update_vinculo(id, req)

        return vinculo

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
async def find_all_vinculo(
    vinculo_filtro: VinculoFiltro = Depends(),
    controller: VinculoController = Depends(get_controller),
):
    try:
        vinculo = controller.find_all_vinculo(vinculo_filtro)

        return vinculo

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
async def delete_vinculo(
    id: str, controller: VinculoController = Depends(get_controller)
):
    try:
        vinculo = controller.delete_vinculo(id)

        if not vinculo:
            return JSONResponse(
                content={"msg": "Vinculo não encontrado"},
                status_code=status.HTTP_404_NOT_FOUND,
            )

        return {"msg": "Vinculo deletado com sucesso!"}

    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Putz... Error inesperado meu nobre",
        )
