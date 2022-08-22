from pydantic import BaseModel, EmailStr
from werkzeug.security import generate_password_hash, check_password_hash

class User(BaseModel):
    fullname : str 
    email : str
    password : str 
    #  password : str | None = None


    @staticmethod   # used not to pass the self argument
    def get_hashed_password(password):
        return generate_password_hash(
            password,method='sha256')
    @staticmethod
    def verify_password(hashed_password, password):
        return check_password_hash(hashed_password, password)   