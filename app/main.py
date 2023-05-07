from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Header, Request
from fastapi.exceptions import HTTPException
from fastapi.security import APIKeyHeader
from typing import List
from constants import *
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
    
async def validate_permissions(id_check: int, permissions: List[str]):
    try:
        profile = get_profile_from_user(id_check)
        if(str(profile) not in permissions and str(profile)!= ProfileEnum.ADMIN.value):
            raise HTTPException(status_code=401, detail="Permission denied")
        else:
            return profile
    except GetUserException as e:
        raise HTTPException(status_code=404, detail=f"{str(e)}")

## Add user

@app.post("/api/user/add-student")
async def add_student(id_check: int, student: UserCreate, api_key: str = Header(...)):
    await(validate_api_key(api_key))
    await(validate_permissions(id_check, [ProfileEnum.TEACHER.value]))
    return insert_student_to_db(student)

@app.post("/api/user/add-teacher")
async def add_teacher(id_check: int, teacher: UserCreate, api_key: str = Header(...)):
    await(validate_api_key(api_key))
    await(validate_permissions(id_check, [ProfileEnum.ADMIN.value]))
    return insert_teacher_to_db(teacher)

@app.post("/api/user/add-labor")
async def add_labor(id_check: int, labor: UserCreate, api_key: str = Header(...)):
    await(validate_api_key(api_key))
    await(validate_permissions(id_check, [ProfileEnum.TEACHER.value]))
    return insert_labor_to_db(labor)

@app.post("/api/user/add-students-set")
async def add_students_set(id_check: int, request: Request, api_key: str = Header(...)):
    await(validate_api_key(api_key))
    await(validate_permissions(id_check, [ProfileEnum.TEACHER.value]))
    students_xml = await request.body()
    return insert_students_to_db_xml(students_xml)

# Delete user

@app.delete("/api/user/delete")
async def delete_user(id_check: int, id_user: int, api_key: str = Header(...)):
    await(validate_api_key(api_key))
    await(validate_permissions(id_check, [ProfileEnum.TEACHER.value]))
    return delete_alumn_from_db(id_user)

# Update user

@app.put("/api/user/update")
async def update_user(id_check: int, id_user: int, updated_fields: dict, api_key: str = Header(...)):
    await(validate_api_key(api_key))
    await(validate_permissions(id_check, [ProfileEnum.STUDENT]))
    return update_user_in_db(id_user, updated_fields)

## Add company

@app.post("/api/company/add")
async def add_company(id_check: int, company: CompanyCreate, api_key: str = Header(...)):
    await(validate_api_key(api_key))
    await(validate_permissions(id_check, [ProfileEnum.TEACHER.value]))
    return insert_company_to_db(company)

## Delete company

@app.delete("/api/company/delete")
async def delete_company(id_check: int, id_company: int, api_key: str = Header(...)):
    await(validate_api_key(api_key))
    await(validate_permissions(id_check, [ProfileEnum.TEACHER.value]))
    return delete_company_from_db(id_company)

## Update company

@app.put("/api/company/update")
async def update_company(id_check: int, id_company: int, updated_fields: dict, api_key: str = Header(...)):
    await(validate_api_key(api_key))
    await(validate_permissions(id_check, [ProfileEnum.TEACHER.value]))
    return update_company_from_db(id_company, updated_fields)

## Add module

@app.post("/api/module/add")
async def add_module(id_check: int, module: ModuleCreate, api_key: str = Header(...)):
    await(validate_api_key(api_key))
    await(validate_permissions(id_check, [ProfileEnum.ADMIN.value]))
    return insert_module_to_db(module)

## Delete module

@app.delete("/api/module/delete")
async def delete_module(id_check: int, id_module: int, api_key: str = Header(...)):
    await(validate_api_key(api_key))
    await(validate_permissions(id_check, [ProfileEnum.ADMIN.value]))
    return delete_module_from_db(id_module)

## Update module

@app.put("/api/module/update")
async def update_module(id_check: int, id_module: int, updated_fields: dict, api_key: str = Header(...)):
    await(validate_api_key(api_key))
    await(validate_permissions(id_check, [ProfileEnum.ADMIN.value]))
    return update_module_from_db(id_module, updated_fields)

#

## HAY QUE CHECKEAR SI ES LABOR QUE SOLO SEAN LAS ENTRADAS DE LOS QUE TUTORIZA, Y SI ES ALUMNO SOLO SUS PROPIAS ENTRADAS, SI NO, DENEGAR
@app.get("/api/user/get-all-entries")
async def get_entries(id_check: int, id_user: int, api_key: str = Header(...)):
    await(validate_api_key(api_key))
    await(validate_permissions(id_check, [ProfileEnum.STUDENT.value, ProfileEnum.TEACHER.value, ProfileEnum.LABOR.value]))
    return get_entries_from_user(id_user)

## LO MISMO QUE ARRIBA
@app.get("/api/user/get-profile")
async def get_profile(id_check: int, id_user: int, api_key: str = Header(...)):
    await(validate_api_key(api_key))
    await(validate_permissions(id_check, [ProfileEnum.STUDENT.value, ProfileEnum.TEACHER.value, ProfileEnum.LABOR.value]))
    return get_data_from_user(id_user)

## Database

@app.post("/api/user/send-email")
async def send_email_for_reset(email: EmailCreate, api_key: str = Header(...)):
    await(validate_api_key(api_key))
    return send_email(email.email)

@app.post("/api/db/import")
async def import_db(id_check: int, api_key: str = Header(...)):
    await(validate_api_key(api_key))
    await(validate_permissions(id_check, [ProfileEnum.ADMIN.value]))
    return import_mysql_database()

@app.get("/api/db/backup")
async def backup_database(id_check: int, api_key: str = Header(...)):
    await(validate_api_key(api_key))
    await(validate_permissions(id_check, [ProfileEnum.ADMIN.value]))
    return generate_backup_of_db()


@app.delete("/api/db/drop")
async def drop_database(id_check: int, api_key: str = Header(...)):
    await(validate_api_key(api_key))
    await(validate_permissions(id_check, [ProfileEnum.ADMIN.value]))
    return drop_db()

## Add unit

@app.post("/api/unit/add")
async def add_unit(id_check: int, unit: UnitCreate, api_key: str = Header(...)):
    await(validate_api_key(api_key))
    await(validate_permissions(id_check, [ProfileEnum.ADMIN.value]))
    return insert_unit_to_db(unit)

## Delete unit

@app.delete("/api/unit/delete")
async def delete_unit(id_check: int, id_unit: int, api_key: str = Header(...)):
    await(validate_api_key(api_key))
    await(validate_permissions(id_check, [ProfileEnum.ADMIN.value]))
    return delete_unit_from_db(id_unit)

## Update unit

@app.put("/api/unit/update")
async def update_unit(id_check: int, id_unit: int, updated_fields: dict, api_key: str = Header(...)):
    await(validate_api_key(api_key))
    await(validate_permissions(id_check, [ProfileEnum.ADMIN.value]))
    return update_unit_from_db(id_unit, updated_fields)

## Get day

@app.get("/api/day")
async def get_day(id_check: int, id_day: int, api_key: str = Header(...)):
    await(validate_api_key(api_key))
    await(validate_permissions(id_check, [ProfileEnum.STUDENT.value, ProfileEnum.TEACHER.value, ProfileEnum.LABOR.value]))
    return get_day_from_db(id_day)

## Update day

@app.put("/api/day/update")
async def update_day(id_check: int, id_day: int, updated_fields: dict, api_key: str = Header(...)):
    await(validate_api_key(api_key))
    await(validate_permissions(id_check, [ProfileEnum.STUDENT.value]))
    return update_day_from_db(id_day, updated_fields)

## Login

@app.get("/api/user")
async def get_user(idUser: int,profileUser: int,api_key: str = Header(...)):
    await(validate_api_key(api_key))
    msg = get_user_from_db(idUser, profileUser)
    return msg

#### AQUI SE NECESITA EL PROFILE?
@app.post("/api/user/login")
async def get_user(auth: LoginCreate,profileUser: int,api_key: str = Header(...)):
    await(validate_api_key(api_key))
    msg = login_from_db(auth,profileUser)
    return msg

## Get agreement

## CONTROLAR EN EL GET QUE EL ALUMNO SOLO VEA SU CONVENIO Y LABORAL EL DE LOS QUE TUTORIZA
@app.get("/api/agreement/get")
async def get_agreement(id_check: int, id_agreement: int, api_key: str = Header(...)):
    await(validate_api_key(api_key))
    profile = await(validate_permissions(id_check, [ProfileEnum.STUDENT.value, ProfileEnum.TEACHER.value, ProfileEnum.LABOR.value]))
    return get_agreement_from_db(id_agreement, profile)

## Add agreement

@app.post("/api/agreement/add")
async def get_agreement(id_check: int, id_agreement: int, userProfile: int, api_key: str = Header(...)):
    await(validate_api_key(api_key))
    await(validate_permissions(id_check, [ProfileEnum.TEACHER.value]))
    return add_agreement_to_db(id_agreement, userProfile)

## Delete agreement

@app.delete("/api/agreement/delete")
async def delete_agreement(id_check: int, id_agreement: int, api_key: str = Header(...)):
    await(validate_api_key(api_key))
    await(validate_permissions(id_check, [ProfileEnum.TEACHER.value]))
    ## TMBN PODEMOS HACER UN MÉTODO PARA BORRAR QUE BORRE DE CUALQUIER TABLA Y GLOBALIZAMOS ESO
    return delete_agreement_from_db(id_agreement)

## Update agreement

@app.put("/api/agreement/update")
async def update_agreement(id_check: int, id_agreement: int, updated_fields: dict,  api_key: str = Header(...)):
    await(validate_api_key(api_key))
    await(validate_permissions(id_check, [ProfileEnum.TEACHER.value]))
    ## COMPRUEBA QUE ESTE MÉTODO FUNCIONA EN TODAS LAS TABLAS,
    # METE TODAS LAS TABLAS Y NOMBRES DE IDS EN EL ARCHIVO DE CONSTANTES
    # Y MIRA TMBN EL MÉTODO QUE VA POR DENTRO DE GET_OBJECT_FROM_DB
    # CON ESTOS DOS MÉTODOS NOS GLOBALIZAMOS TODOS LOS UPDATE
    return update_table_db(TABLE_AGRE, ID_NAME_AGRE, id_agreement, updated_fields)