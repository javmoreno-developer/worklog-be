from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Header, Request
from fastapi.exceptions import HTTPException
from fastapi.security import APIKeyHeader
from typing import List
from database import *
from models import *
from utils import *
import os

app = FastAPI()

api_key_header = APIKeyHeader(name="X-API-Key")

origins = [
    "http://localhost",
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

## Validations

async def validate_api_key(api_key: str = Header(...)):
    if api_key != os.environ["API_KEY"]:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
async def validate_permissions(idUser: int, permissions: List[str]):
    try:
        profile = get_profile_from_user(idUser)
        if(str(profile) not in permissions or str(profile)!= ProfileEnum.ADMIN):
            raise HTTPException(status_code=401, detail="Permission denied")
    except GetUserException as e:
        raise HTTPException(status_code=404, detail=f"{str(e)}")

## Company

@app.post("/api/company/add")
async def add_company(company: CompanyCreate,profileUser: int,api_key: str = Header(...)):
    await(validate_api_key(api_key))
    msg = insert_company_to_db(company,profileUser)
    return msg

@app.delete("/api/company/delete")
async def delete_company(idCompany: str,profileUser: str,api_key: str = Header(...)):
    await(validate_api_key(api_key))
    msg = delete_company_from_db(int(idCompany),int(profileUser))
    return msg

@app.put("/api/company/update")
async def update_company(company: CompanyCreate,idCompany: int,profileUser: int,api_key: str = Header(...)):
    await(validate_api_key(api_key))
    msg = update_company_from_db(company,int(idCompany),int(profileUser))
    return msg

## Module

@app.post("/api/module/add")
async def add_module(module: ModuleCreate,profileUser: int,api_key: str = Header(...)):
    await(validate_api_key(api_key))
    msg = insert_module_to_db(module,profileUser)
    return msg

@app.delete("/api/module/delete")
async def delete_module(idModule: int,profileUser: int,api_key: str = Header(...)):
    await(validate_api_key(api_key))
    msg = delete_module_from_db(idModule,profileUser)
    return msg

@app.put("/api/module/update")
async def update_module(module: ModuleCreate,idModule: int,profileUser: int,api_key: str = Header(...)):
    await(validate_api_key(api_key))
    msg = update_module_from_db(module,idModule,profileUser)
    return msg

## Add user

@app.post("/api/user/add-student")
async def add_student(idUser: int, student: UserCreate, api_key: str = Header(...)):
    await(validate_api_key(api_key))
    await(validate_permissions(idUser, [ProfileEnum.TEACHER.value]))
    return insert_student_to_db(student)

@app.post("/api/user/add-teacher")
async def add_teacher(idUser: int, teacher: UserCreate, api_key: str = Header(...)):
    await(validate_api_key(api_key))
    await(validate_permissions(idUser, [ProfileEnum.ADMIN.value]))
    return insert_teacher_to_db(teacher)

@app.post("/api/user/add-labor")
async def add_labor(idUser: int, labor: UserCreate, api_key: str = Header(...)):
    await(validate_api_key(api_key))
    await(validate_permissions(idUser, [ProfileEnum.TEACHER.value]))
    return insert_labor_to_db(labor)

@app.post("/api/user/add-students-set")
async def add_students_set(idUser: int, request: Request, api_key: str = Header(...)):
    await(validate_api_key(api_key))
    await(validate_permissions(idUser, [ProfileEnum.TEACHER.value]))
    students_xml = await request.body()
    return insert_students_to_db_xml(idUser, students_xml)

# Delete user

@app.delete("/api/user/delete")
async def delete_alumn(idAlumn: int,profileUser: int, api_key: str = Header(...)):
    await(validate_api_key(api_key))
    msg = delete_alumn_from_db(idAlumn,profileUser)
    return msg

# Update user

@app.put("/api/user/update")
async def update_user(idUser: int, idUserToUpdate: int, updated_fields: dict, api_key: str = Header(...)):
    await(validate_api_key(api_key))
    await(validate_permissions(idUser, [ProfileEnum.STUDENT]))
    return update_user_in_db(idUserToUpdate, updated_fields)

#

@app.get("/api/user/get-all-entries")
async def get_entries(idAlumn: int,profileUser: int, api_key: str = Header(...)):
    await(validate_api_key(api_key))
    msg = get_entries_from_user(idAlumn,profileUser)
    return msg

@app.get("/api/user/get-profile")
async def get_profile(idAlumn: int,profileUser: int, api_key: str = Header(...)):
    await(validate_api_key(api_key))
    msg = get_data_from_user(idAlumn,profileUser)
    return msg

## Database

@app.post("/api/user/send-email")
async def send_email_for_reset(email: EmailCreate, api_key: str = Header(...)):
    await(validate_api_key(api_key))
    msg = send_email(email.email)
    return msg

@app.post("/api/db/import/{profileUser}")
async def import_db(profileUser: int, api_key: str = Header(...)):
    await(validate_api_key(api_key))
    msg = import_mysql_database(profileUser)
    return msg

@app.get("/api/db/backup/{idUser}")
async def backup_database(idUser: int, api_key: str = Header(...)):
    await(validate_api_key(api_key))
    return generate_backup_of_db()


@app.delete("/api/db/drop")
async def drop_database(idUser: int, api_key: str = Header(...)):
    await(validate_api_key(api_key))
    await(validate_permissions(idUser, [ProfileEnum.ADMIN.value]))
    return drop_db()

## Unit

@app.post("/api/unit/add/{profileUser}")
async def add_unit(unit: UnitCreate,profileUser: int,api_key: str = Header(...)):
    await(validate_api_key(api_key))
    msg = insert_unit_to_db(unit,profileUser)
    return msg

@app.delete("/api/unit/delete/")
async def delete_unit(idUnit: int,profileUser: int,api_key: str = Header(...)):
    await(validate_api_key(api_key))
    msg = delete_unit_from_db(idUnit,profileUser)
    return msg

@app.put("/api/unit/update/")
async def update_unit(unit: UnitCreate,idUnit: int,profileUser: int,api_key: str = Header(...)):
    await(validate_api_key(api_key))
    msg = update_unit_from_db(unit,idUnit,profileUser)
    return msg

## Day

@app.get("/api/day/")
async def get_day(idDay: int,profileUser: int,api_key: str = Header(...)):
    await(validate_api_key(api_key))
    msg = get_day_from_db(idDay,profileUser)
    return msg

@app.put("/api/day/update/")
async def update_day(day: DayCreate,idDay: int,profileUser: int,api_key: str = Header(...)):
    await(validate_api_key(api_key))
    msg = update_day_from_db(day,idDay,profileUser)
    return msg

## Login

@app.get("/api/user")
async def get_user(idUser: int,profileUser: int,api_key: str = Header(...)):
    await(validate_api_key(api_key))
    msg = get_user_from_db(idUser, profileUser)
    return msg

@app.post("/api/user/login")
async def get_user(auth: LoginCreate,profileUser: int,api_key: str = Header(...)):
    await(validate_api_key(api_key))
    msg = login_from_db(auth,profileUser)
    return msg

## Agreement

@app.get("/api/agreement/get")
async def get_agreement(idAgreement: int, userProfile: int, api_key: str = Header(...)):
    await(validate_api_key(api_key))
    return get_agreement_from_db(idAgreement, userProfile)

@app.delete("/api/agreement/delete")
async def delete_agreement(idUser: int, idAgreement: int, api_key: str = Header(...)):
    await(validate_api_key(api_key))
    await(validate_permissions(idUser))
    return delete_agreement_from_db(idAgreement)

@app.put("/api/agreement/update")
async def delete_agreement(idAgreement: int, userProfile: int, api_key: str = Header(...)):
    await(validate_api_key(api_key))
    return update_agreement_from_db(idAgreement, userProfile)