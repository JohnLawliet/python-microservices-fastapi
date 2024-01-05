import pathlib, io, uuid
from functools import lru_cache
from fastapi import (
    Depends, FastAPI, Request, File, UploadFile
)
from typing_extensions import Annotated
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from pydantic_settings import BaseSettings

# This is needed to enable debug mmode. Debug mode is picked up based on value in .env
# note that this requires python-dotenv
class Settings(BaseSettings):
    debug: bool = False
    echo_active: bool = False

    class Config:
        env_file = ".env"

@lru_cache
def get_settings():
    return Settings()

settings = get_settings()
DEBUG=settings.debug

BASE_DIR = pathlib.Path(__file__).parent
UPLOAD_DIR = BASE_DIR / "uploads"

app = FastAPI()
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

@app.get("/", response_class=HTMLResponse)
def home_view(request: Request, settings: Annotated[Settings, Depends(get_settings)]):
    return templates.TemplateResponse("home.html", {"request":request, "abc":123})

@app.post("/")
def home_view(request: Request):
    return {"hello":"world"}


# for uploading anything always use async
@app.post("/img-echo", response_class=FileResponse)
async def img_echo_view(file:UploadFile = File(...), settings:Settings = Depends(get_settings)):
    if not settings.echo_active:
        raise Exception(detail="Invalid endpoint", status_code=400)
    UPLOAD_DIR.mkdir(exist_ok=True)
    bytes_str = io.BytesIO(await file.read())
    fname = pathlib.Path(file.filename)
    fext = fname.suffix                             # .jpg, .txt
    dest = UPLOAD_DIR / f"{uuid.uuid1()}{fext}"     # uuid1 comes with a timestamp
    with open(str(dest), 'wb') as out:
        out.write(bytes_str.read())
    return file
