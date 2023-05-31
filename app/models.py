from decimal import Decimal
from typing import Optional
from pydantic import BaseModel
from enum import Enum

########## USER ##########

class StatusEnum(int, Enum):
    DISABLED = 0,
    ENABLED = 1

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
    picture: Optional[str]
    linkedin: Optional[str]
    github: Optional[str]
    twitter: Optional[str]
    profile: Optional[ProfileEnum]
    isActive: Optional[StatusEnum]

class UserCreate(UserBase):
    pass

class User(UserBase):
    idUser: int
    
    class Config:
        orm_mode = True


########## COMPANY ##########

class CompanyBase(BaseModel):
    name: str
    address: Optional[str] = None
    latitude: Optional[Decimal] = None
    longitude: Optional[Decimal] = None
    phone: Optional[str] = None

class CompanyCreate(CompanyBase):
    pass

class Company(CompanyBase):
    idCompany: int
    
    class Config:
        orm_mode = True


########## MODULE ##########

class ModuleBase(BaseModel):
    name: str
    initials: str
    hours: Optional[int] = None
    description: Optional[str] = None
    idUnit: int

class ModuleCreate(ModuleBase):
    pass

class Module(ModuleBase):
    idModule: int
    
    class Config:
        orm_mode = True

########## UNIT ##########

class UnitEnum(str, Enum):
    MORNING = 'morning'
    EVENING = "evening"
    
class UnitBase(BaseModel):
    level: int
    name: str
    initials: str
    charUnit: Optional[str]= None
    unitType: UnitEnum

class UnitCreate(UnitBase):
    pass

class Unit(UnitBase):
    idUnit: int
    
    class Config:
        orm_mode = True

########## ENTRY ##########

class EntryBase(BaseModel):
    startWeek: str
    endWeek: str 
    idAgreement: int

class EntryCreate(EntryBase):
    pass

class Entry(EntryBase):
    idEntry: int
    
    class Config:
        orm_mode = True

########## COMMENT ##########

class CommentBase(BaseModel):
    text: str
    hours: Optional[str] = None
    observations: Optional[str]=None
    idEntry: int
    idModule: Optional[int] = None

class CommentCreate(CommentBase):
    pass

class Comment(CommentBase):
    idComment: int
    
    class Config:
        orm_mode = True

########## EMAIL ##########

class EmailBase(BaseModel):
    email: str

class EmailCreate(EmailBase):
    pass

class Email(EmailBase):
    
    class Config:
        orm_mode = True

########## LOGIN ##########

class LoginBase(BaseModel):
    email: str
    password: str

class LoginCreate(LoginBase):
    pass

class Login(LoginBase):
    
    class Config:
        orm_mode = True

########## AGREEMENT ##########

class AgreementTypeEnum(str, Enum):
    FCT = 'fct',
    DUAL = 'dual'
    FCT_DUAL = 'fct+dual'

class AgreementBase(BaseModel):
    dualStartAt: str
    dualEndAt: str
    fctStartAt: str
    fctEndAt: str
    agreementType: AgreementTypeEnum
    idCompany: int
    idTeacher: int
    idLabor: int

class AgreementCreate(AgreementBase):
    pass

class Agreement(AgreementBase):
    idAgreement: int

    class Config:
        orm_mode = True

########## SCHOLAR YEAR ##########

class ScholarYearBase(BaseModel):
    startDate: str
    endDate: str
    year: str
    aptitudesPonderation: Optional[int]
    subjectsPonderation: Optional[int]
    holidays: Optional[str]

class ScholarYearCreate(ScholarYearBase):
    pass

class ScholarYear(ScholarYearBase):
    idScholarYear: int

    class Config:
        orm_mode = True
