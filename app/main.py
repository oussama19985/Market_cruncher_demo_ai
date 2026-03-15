from fastapi import FastAPI
from dotenv import load_dotenv
from app.routes import router

load_dotenv()

app = FastAPI(title="Market Analysis Agent")

app.include_router(router)
