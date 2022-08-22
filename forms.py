from typing import List, Optional
from fastapi import Request


class ValidationError(Exception):
    def __init__(self, detail):
        self.detail = detail


class SignupForm:
    def __init__(self, request: Request):
        self.request = request
        self.errors = []

    async def load_data(self):
        form = await self.request.form()
        self.fullname = form.get("fullname")
        self.email = form.get("email")
        self.password  = form.get("password")
        return {"fullname": self.fullname,
                "email": self.email,
                "password": self.password}


    def is_valid(self):
        if  len(self.fullname)<4:
            raise ValidationError("Fullname should be > 3 characters")
        elif "@" not in self.email:
            raise ValidationError('Email is required')
        elif not len(self.password)>=4:
            raise ValidationError("Password must be atleast 4 characters")


class LoginForm:
    def __init__(self, request: Request):
        self.request : Request = request
        self.errors = []

    async def data(self):
        form = await self.request.form()
        self.email = form.get("email")
        self.password  = form.get("password")
        return {  "email": self.email,
                "password": self.password}


    def isvalid(self):
        if "@" not in self.email:
            raise ValidationError('Email is required')
        elif not len(self.password)>=4:
            raise ValidationError("Password must be atleast 4 characters")
     