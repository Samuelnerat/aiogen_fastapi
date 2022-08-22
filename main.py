# from urllib import response
import uvicorn
from sqlalchemy.orm import Session
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Request, Form, HTTPException, Depends, Response
from fastapi.responses import HTMLResponse
from database import engine, get_db
from models import Base
from sqlalchemy.exc import SQLAlchemyError
import schemas, models
from forms import SignupForm, ValidationError, LoginForm
import jwt
from config import Config



app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


Base.metadata.create_all(bind=engine)

@app.get("/", response_class =HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.get("/signup", response_class =HTMLResponse)
def signup(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/signup", response_class =HTMLResponse)
async def signup(request: Request, db: Session = Depends(get_db)):
    form = SignupForm(request)
    specific = await form.load_data()
    email = specific["email"]
    name = specific["fullname"]
    passwd = specific["password"]
    # if form.is_valid():
    try:
        form.is_valid()
        existing_user = db.query(models.User).filter(models.User.email == email).first()
        if not existing_user:            
            user = schemas.User(email=email, fullname=name, password=passwd)
            user.password = schemas.User.get_hashed_password(passwd)
            db_user = models.User(email= user.email, hashed_password= user.password, fullname= user.fullname)
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            return templates.TemplateResponse ("login.html", {"request": request, "message": "User Successfully Registered"})
        else:
            return templates.TemplateResponse ("index.html", {"request": request, "error": "User Already Registered"})
    except SQLAlchemyError as ex:
        sqlstate = ex.args[0]
        print(sqlstate)
    except ValidationError as error:
        return templates.TemplateResponse ("index.html", {"request": request, "error": error.detail})


@app.get("/login", response_class =HTMLResponse)
def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login", response_class =HTMLResponse)
async def login(request: Request, response: Response, db: Session = Depends(get_db)):
    form = LoginForm(request)
    specific = await form.data()
    email = specific["email"]
    passwd = specific["password"]

    # if form.isvalid():
    try:
        form.isvalid()
        existing_user = db.query(models.User).filter(models.User.email == email).first()
        if existing_user is None:
            return templates.TemplateResponse ("login.html", {"request": request, "error": "User Does Not Exsit"})
        else:
            if schemas.User.verify_password(existing_user.hashed_password, passwd):
                data = {"username":email}                    
                # print(data)
                jwt_token = jwt.encode(data, Config.SECRET_KEY, algorithm=Config.ALGORITHM)
                # print(jwt_token)
                response = templates.TemplateResponse("dashboard.html", {"request": request, "message": "Login Successful"})                    
                response.set_cookie(key="access_token", value=f"Bearer{jwt_token}", httponly=True)
                db.commit()
                return response
            else:
                return templates.TemplateResponse ("login.html", {"request": request, "error": "Invalid Password"})
    except SQLAlchemyError as ex:
        sqlstate = ex.args[0]
        print(sqlstate)
    except ValidationError as error:
        return templates.TemplateResponse ("login.html", {"request": request, "error": error.detail})


@app.get("/dashboard", response_class =HTMLResponse)
def daashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})


@app.get("/task", response_class =HTMLResponse)
def task(request: Request):
    return templates.TemplateResponse("task.html", {"request": request})


@app.get("/settings", response_class =HTMLResponse)
def settings(request: Request):
    return templates.TemplateResponse("settings.html", {"request": request})



@app.get("/logout")
async def Logout(request: Request):
    response = templates.TemplateResponse("home.html", {"request": request, "message": "Logout Successful"})
    response.delete_cookie(Config.SECRET_KEY)
    return response

if __name__ == "__main__":
    uvicorn.run(app)