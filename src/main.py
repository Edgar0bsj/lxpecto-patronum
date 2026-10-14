from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.router.aluno_router import router as aluno_router
from src.router.vinculo_router import router as vinculo_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(vinculo_router)
app.include_router(aluno_router)
