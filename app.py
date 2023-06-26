import openai

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from pydantic import BaseSettings

class Settings(BaseSettings):
    OPENAI_API_KEY: str = "OPENAI_API_KEY"
    
    class Config:
        env_file = '.env'
        
settings = Settings()
openai.api_key = settings.OPENAI_API_KEY

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request" : request})

