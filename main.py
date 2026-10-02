from fastapi import FastAPI

from routes.clientes import router as clientes_router
from routes.reservas import router as reservas_router
from routes.restaurantes import router as restaurantes_router

app = FastAPI(
    title="API de Reservas de Restaurantes",
    description="CRUD simples para restaurantes, clientes e reservas.",
    version="1.0.0",
)

app.include_router(restaurantes_router)
app.include_router(clientes_router)
app.include_router(reservas_router)
