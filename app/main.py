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

########## VALIDATIONS ##########

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
        raise HTTPException(status_code=404, detail="Not found")

########## USER ##########

# Get user
@app.get("/api/user/get")
async def get_user(id_check: int, id_user: int, api_key: str = Header(...)):
    await(validate_api_key(api_key))
    grant_access = False
    permissions = [ProfileEnum.STUDENT.value, ProfileEnum.TEACHER.value, ProfileEnum.LABOR.value]
    profile = await(validate_permissions(id_check, permissions))

    # If its a teacher or admin, always grant access
    if profile in [ProfileEnum.TEACHER.value, ProfileEnum.ADMIN.value]:
        grant_access = True
    # If its a student, grant access if its his/her own profile
    elif profile == ProfileEnum.STUDENT.value and id_check == id_user:
        grant_access = True
    # If its a laboral tutor, grant access if its his/her own profile or its his/her student
    elif profile == ProfileEnum.LABOR.value and id_check == id_user or is_student_under_labor_tutor(id_check, id_user):
        grant_access = True

    # Return the user if has granted access
    if grant_access:
        return get_object_from_db(T_USER, ID_NAME_USER, id_user)
    # Raise exception if has NOT granted access
    else:
        raise HTTPException(status_code=401, detail="Permission denied")
    
# Add student
@app.post("/api/user/add-student")
async def add_student(id_check: int, student: UserCreate, api_key: str = Header(...)):
    await(validate_api_key(api_key))
    await(validate_permissions(id_check, [ProfileEnum.TEACHER.value]))
    return insert_user_to_db(student, ProfileEnum.STUDENT)

# Add teacher
@app.post("/api/user/add-teacher")
async def add_teacher(id_check: int, teacher: UserCreate, api_key: str = Header(...)):
    await(validate_api_key(api_key))
    await(validate_permissions(id_check, [ProfileEnum.ADMIN.value]))
    return insert_user_to_db(teacher, ProfileEnum.TEACHER)

# Add laboral tutor
@app.post("/api/user/add-labor")
async def add_labor(id_check: int, labor: UserCreate, api_key: str = Header(...)):
    await(validate_api_key(api_key))
    await(validate_permissions(id_check, [ProfileEnum.TEACHER.value]))
    return insert_user_to_db(labor, ProfileEnum.LABOR)

# Add students set with XML
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
    return delete_object_from_db(T_USER, ID_NAME_USER, id_user)


# EL ADMIN PUEDE EDITAR A CUALQUIERA, EL ALUMNO Y LABORAL A SÍ MISMO.
# PERO EL PROFESOR PUEDE EDITAR A CUALQUIER USUARIO AL IGUAL QUE EL ADMIN? ######################
# Update user
@app.put("/api/user/update")
async def update_user(id_check: int, id_user: int, updated_fields: dict, api_key: str = Header(...)):
    await(validate_api_key(api_key))
    grant_access = False
    permissions = [ProfileEnum.STUDENT.value, ProfileEnum.TEACHER.value, ProfileEnum.LABOR.value]
    profile = await(validate_permissions(id_check, permissions))

    # If is a Student or Laboral tutor, only can update their own data
    if profile in [ProfileEnum.STUDENT.value, ProfileEnum.LABOR.value] and id_check == id_user:
        grant_access = True
    # If is an Admin or Teacher, always grant access
    elif profile in [ProfileEnum.TEACHER.value, ProfileEnum.ADMIN.value]:
        grant_access = True

    # Update the user if has granted access
    if grant_access:
        return update_table_db(T_USER, ID_NAME_USER, id_user, updated_fields)
    # Raise exception if has NOT granted access
    else:
        raise HTTPException(status_code=401, detail="Permission denied")

# Login
@app.post("/api/user/login")
async def get_user(auth: LoginCreate, api_key: str = Header(...)):
    await(validate_api_key(api_key))
    return login_from_db(auth)

# Send email
@app.post("/api/user/send-email")
async def send_email_for_reset(email: EmailCreate, api_key: str = Header(...)):
    await(validate_api_key(api_key))
    return send_email(email.email)

########## COMPANY ##########

# Get company
@app.get("/api/company/get")
async def get_company(id_check: int, id_company: int, api_key: str = Header(...)):
    await(validate_api_key(api_key))
    grant_access = False
    profile = await(validate_permissions(id_check, [ProfileEnum.TEACHER.value, ProfileEnum.STUDENT.value]))
    # If its a teacher or admin, grant access
    if profile in [ProfileEnum.TEACHER.value, ProfileEnum.ADMIN.value]:
        grant_access = True
    # If its an student, check if its his/her company
    ## HAY QUE HACER EL CHECKEOEEOOEOEOEOEOEO AQUÍ
    # PUEDE HABER UN MISMO ALUMNO EN MÁS DE UN CONVENIO A LA VEZ(de otros años),
    # HAY QUE DISTINGIRLO CON ALGO MÁS. (CONVENIO ACTIVO)
    elif profile == ProfileEnum.STUDENT.value and is_student_company(id_check, id_company):
        grant_access = True

    # Return the company if has granted access
    if grant_access:
        return get_object_from_db(T_COMPANY, ID_NAME_COMPANY, id_company)
    # Raise exception if has NOT granted access
    else:
        raise HTTPException(status_code=401, detail="Permission denied")

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
    return delete_object_from_db(T_COMPANY, ID_NAME_COMPANY, id_company)

## Update company
@app.put("/api/company/update")
async def update_company(id_check: int, id_company: int, updated_fields: dict, api_key: str = Header(...)):
    await(validate_api_key(api_key))
    await(validate_permissions(id_check, [ProfileEnum.TEACHER.value]))
    return update_table_db(T_COMPANY, ID_NAME_COMPANY, id_company, updated_fields)

########## MODULE ##########

## Get module
@app.get("/api/module/get")
async def get_module(id_check: int, id_module: int, api_key: str = Header(...)):
    await(validate_api_key(api_key))
    await(validate_permissions(id_check, [ProfileEnum.TEACHER.value, ProfileEnum.LABOR.value]))
    return get_object_from_db(T_MODULE, ID_NAME_MODULE, id_module)

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
    return delete_object_from_db(T_MODULE, ID_NAME_MODULE, id_module)

# Update module
@app.put("/api/module/update")
async def update_module(id_check: int, id_module: int, updated_fields: dict, api_key: str = Header(...)):
    await(validate_api_key(api_key))
    await(validate_permissions(id_check, [ProfileEnum.ADMIN.value]))
    return update_table_db(T_MODULE, ID_NAME_MODULE, id_module, updated_fields)

# Student entries

## HAY QUE CHECKEAR SI ES LABOR QUE SOLO SEAN LAS ENTRADAS DE LOS QUE TUTORIZA,
# Y SI ES ALUMNO SOLO SUS PROPIAS ENTRADAS, SI NO, DENEGAR
@app.get("/api/user/get-all-entries")
async def get_entries(id_check: int, id_user: int, api_key: str = Header(...)):
    await(validate_api_key(api_key))
    grant_acess = False
    permissions = [ProfileEnum.STUDENT.value, ProfileEnum.TEACHER.value, ProfileEnum.LABOR.value]
    profile = await(validate_permissions(id_check, permissions))

    # If its an Admin or Teacher, always grant access
    if profile in [ProfileEnum.ADMIN.value, ProfileEnum.TEACHER.value]:
        grant_acess = True
    # If its a student, grant access if its his/her own entries
    elif profile == ProfileEnum.STUDENT.value and id_check == id_user:
        grant_acess = True
    # If its a labor, grant access if its his/her student entries
    elif profile == ProfileEnum.LABOR.value and is_student_under_labor_tutor(id_check, id_user):
        grant_acess = True

    # Return the entries from the user if has granted access
    if grant_acess:
        return get_entries_from_user(id_user)
    # Raise exception if has NOT granted access
    else:
        raise HTTPException(status_code=401, detail="Permission denied")

########## DATABASE ##########

# Backup database
@app.get("/api/db/backup")
async def backup_database(id_check: int, api_key: str = Header(...)):
    await(validate_api_key(api_key))
    await(validate_permissions(id_check, [ProfileEnum.ADMIN.value]))
    return generate_backup_of_db()

# Drop database
@app.delete("/api/db/drop")
async def drop_database(id_check: int, api_key: str = Header(...)):
    await(validate_api_key(api_key))
    await(validate_permissions(id_check, [ProfileEnum.ADMIN.value]))
    return drop_db()

########## UNIT ##########

## Get unit

@app.get("/api/unit/get")
async def get_unit(id_check: int, id_unit: int, api_key: str = Header(...)):
    await(validate_api_key(api_key))
    await(validate_permissions(id_check, [ProfileEnum.TEACHER.value]))
    return get_object_from_db(T_UNIT, ID_NAME_UNIT, id_unit)

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
    return delete_object_from_db(T_UNIT, ID_NAME_UNIT, id_unit)

## Update unit

@app.put("/api/unit/update")
async def update_unit(id_check: int, id_unit: int, updated_fields: dict, api_key: str = Header(...)):
    await(validate_api_key(api_key))
    await(validate_permissions(id_check, [ProfileEnum.ADMIN.value]))
    return update_table_db(T_UNIT, ID_NAME_UNIT, id_unit, updated_fields)

########## DAY ##########

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
    return update_table_db(T_DAY, ID_NAME_DAY, id_day, updated_fields)

########## AGREEMENT ##########

## Get agreement

## CONTROLAR EN EL GET QUE EL ALUMNO SOLO PUEDA VER SU CONVENIO Y LABORAL SOLO EL DE LOS QUE TUTORIZA
# NO SE SI HACER OTRO END POINT PARA OBTENER EL CONVENIO DE UN ESTUDIANTE
@app.get("/api/agreement/get")
async def get_agreement(id_check: int, id_agreement: int, api_key: str = Header(...)):
    await(validate_api_key(api_key))
    grant_access = False
    permissions = [ProfileEnum.STUDENT.value, ProfileEnum.TEACHER.value, ProfileEnum.LABOR.value]
    profile = await(validate_permissions(id_check, permissions))

    # If its an Admin or Teacher, grant access
    if profile in [ProfileEnum.ADMIN.value, ProfileEnum.TEACHER.value]:
        grant_access = True
    # If its a Student and is requesting for his own agreement, grant access
    elif profile == ProfileEnum.STUDENT.value and is_student_agreement():
        grant_access = True
    # If its a Laboral tutor and is requesting for the agreement of their students, grant access
    elif profile == ProfileEnum.LABOR.value and is_agreement_from_his_students():
        grant_access = True
    
    # Return the agreement if has granted access
    if grant_access:
        return get_object_from_db(T_AGREEMENT, ID_NAME_AGREEMENT, id_agreement)
    # Raise exception if has NOT granted access
    else:
        raise HTTPException(status_code=401, detail="Permission denied")

## Add agreement
@app.post("/api/agreement/add")
async def add_agreement(id_check: int, agreement: AgreementCreate, api_key: str = Header(...)):
    await(validate_api_key(api_key))
    await(validate_permissions(id_check, [ProfileEnum.TEACHER.value]))
    return insert_agreement_to_db(agreement)

## Delete agreement
@app.delete("/api/agreement/delete")
async def delete_agreement(id_check: int, id_agreement: int, api_key: str = Header(...)):
    await(validate_api_key(api_key))
    await(validate_permissions(id_check, [ProfileEnum.TEACHER.value]))
    return delete_object_from_db(T_AGREEMENT, ID_NAME_AGREEMENT, id_agreement)

## Update agreement
@app.put("/api/agreement/update")
async def update_agreement(id_check: int, id_agreement: int, updated_fields: dict, api_key: str = Header(...)):
    await(validate_api_key(api_key))
    await(validate_permissions(id_check, [ProfileEnum.TEACHER.value]))
    return update_table_db(T_AGREEMENT, ID_NAME_AGREEMENT, id_agreement, updated_fields)

########## SETTINGS ##########

# Update grade duration
@app.put("/api/setting/grade_duration")
async def update_grade_duration(id_check: int, start_date: str, end_date: str, api_key: str = Header(...)):
    await(validate_api_key(api_key))
    await(validate_permissions(id_check, [ProfileEnum.ADMIN.value]))
    # Check that date format is valid
    if is_date_format_valid([start_date, end_date], DATE_FORMAT) == False:
        raise HTTPException(status_code=400, detail="Incorrect date format")
    # Check that start date is smaller than end date
    if start_date and end_date and start_date >= end_date:
        raise HTTPException(status_code=400, detail="Start date must be before end date")
    grade_duration = {"startDate": start_date, "endDate": end_date}
    return update_table_db(T_SETTING, ID_NAME_SETTING, 1, grade_duration)

# Update ponderation
@app.put("/api/setting/ponderation")
async def update_ponderation(id_check: int, aptitudes_ponderation: int, subjects_ponderation: int, api_key: str = Header(...)):
    await(validate_api_key(api_key))
    await(validate_permissions(id_check, [ProfileEnum.ADMIN.value]))
    # If ponderation does not equal 100, raise HTTPException
    if aptitudes_ponderation + subjects_ponderation != 100:
        raise HTTPException(status_code=400, detail="Aptitudes and Subjects must sum a total of 100")
    # If ponderation equals 100, update it
    ponderation = {"aptitudesPonderation": aptitudes_ponderation, "subjectsPonderation": subjects_ponderation}
    return update_table_db(T_SETTING, ID_NAME_SETTING, 1, ponderation)

# Update holidays
@app.put("/api/setting/holidays")
async def update_holidays(id_check: int, holidays: dict,api_key: str = Header(...)):
   
    await(validate_api_key(api_key))
    await(validate_permissions(id_check, [ProfileEnum.ADMIN.value]))
    return update_table_db(T_SETTING, ID_NAME_SETTING, 1, holidays)