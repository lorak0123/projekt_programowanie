import datetime
import io

from fastapi import FastAPI, Path, UploadFile, Depends, HTTPException
import sympy
from PIL import Image, ImageOps
from fastapi.responses import Response
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status
from starlette.middleware.cors import CORSMiddleware

from app.database_mock import get_user
from app.models import TokenModel
from app.utils import create_access_token, create_refresh_token, verify_password, get_current_user

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/prime/{number}")
async def prime_number(number: int = Path(..., gt=0, le=9223372036854775807)):
    return sympy.isprime(number)


@app.post("/picture/invert")
async def create_upload_file(file: UploadFile):
    content = await file.read()
    image = Image.open(io.BytesIO(content))
    image = ImageOps.invert(image)
    buf = io.BytesIO()
    image.save(buf, format='JPEG')
    return Response(content=buf.getvalue(), media_type="image/jpeg")


@app.get('/time')
async def get_time(user=Depends(get_current_user)):
    return datetime.datetime.now().time()


@app.post('/login', response_model=TokenModel)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user(form_data.username)
    if user is None or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect login or password"
        )

    return {
        "access_token": create_access_token(form_data.username),
        "refresh_token": create_refresh_token(form_data.username),
    }
