import openai

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
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

@app.post("/", response_class=HTMLResponse)
async def index(request: Request, animal: str= Form(...)):
    response = openai.Completion.create(
        model= "text-davinci-003",
        prompt= generate_prompt(animal),
        temperature= 0.6
    )
    result = response.choices[0].text
    return templates.TemplateResponse("index.html", {"request": request, "result": result})
 
def generate_prompt(animal: str):
    return """Sugiere tres nombres para un animal como si fuera un super heroe.

Animal: Gato
Names: Capitan MichiBionico, Agente Uñas Afiladas, El felino increible
Animal: Perro
Names: Cody La protectora, El canino maravilloso, Super Pachoncito
Animal: {}
Names:""".format(animal.capitalize())