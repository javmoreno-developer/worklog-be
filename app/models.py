from decimal import Decimal
from typing import Optional
from pydantic import BaseModel
from enum import Enum

## Company
class CompanyBase(BaseModel):
    name: str
    direction: Optional[str] = None
    latitude: Optional[Decimal] = None
    longitude: Optional[Decimal] = None
    phone: Optional[str] = None

class CompanyCreate(CompanyBase):
    pass

class Company(CompanyBase):
    idCompany: int
    
    class Config:
        orm_mode = True


## Module
class ModuleBase(BaseModel):
    name: str
    initials: str
    hours: Optional[int] = None
    idUnit: int

class ModuleCreate(ModuleBase):
    pass

class Module(ModuleBase):
    idModule: int
    
    class Config:
        orm_mode = True

## User

class ProfileEnum(str, Enum):
    ADMIN = '1'
    STUDENT = '2'
    TEACHER = '3'
    LABOR = '4'

class UserBase(BaseModel):
    name: str
    surname: str
    email: str
    password: str
    picture: str
    linkedin: str
    github: str
    twitter: str
    profile: ProfileEnum

class UserCreate(UserBase):
    pass

class User(UserBase):
    idUser: int
    
    class Config:
        orm_mode = True

## Unit
class UnitEnum(str, Enum):
    MORNING = 'm'
    EVENING = "e"
    

class UnitBase(BaseModel):
    level: int
    name: str
    initials: str
    charUnit: Optional[str]=None
    unitType: Optional[UnitEnum]=None

class UnitCreate(UnitBase):
    pass

class Unit(UnitBase):
    idUnit: int
    
    class Config:
        orm_mode = True

## Day

class DayBase(BaseModel):
    text: str
    hours: str
    observations: Optional[str]=None
    idEntry: int

class DayCreate(DayBase):
    pass

class Day(DayBase):
    idDay: int
    
    class Config:
        orm_mode = True

class EmailBase(BaseModel):
    email: str

class EmailCreate(EmailBase):
    pass

class Email(EmailBase):
    
    class Config:
        orm_mode = True

class LoginBase(BaseModel):
    email: str
    password: str

class LoginCreate(LoginBase):
    pass

class Login(LoginBase):
    
    class Config:
        orm_mode = True