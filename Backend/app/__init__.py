from fastapi import FastAPI
from .config import Config


config = Config()

def create_app():
    app = FastAPI()
    return app
