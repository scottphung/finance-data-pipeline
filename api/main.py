from fastapi import FastAPI
from api.routes import portfolio

app = FastAPI(title="Quant Hedge Fund API")

app.include_router(portfolio.router)