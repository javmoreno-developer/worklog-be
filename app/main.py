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

# Validate API KEY
async def validate_api_key(api_key: str = Header(...)):
    if api_key != os.environ["API_KEY"]:
        raise HTTPException(status_code=401, detail="Invalid API key")

# Validate permissions
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
    permissions = [ProfileEnum.STUDENT.value, ProfileEnum.TEACHER.value, ProfileEnum.LABOR.value]
    profile = await(validate_permissions(id_check, permissions))
    return get_user_from_db(id_check, id_user, profile)

# Get students
@app.get("/api/user/get/students")
async def get_students(id_check: int, api_key: str = Header(...)):
    await(validate_api_key(api_key))
    await(validate_permissions(id_check, [ProfileEnum.TEACHER.value]))
    return get_students_from_db()

# Get teachers
@app.get("/api/user/get/teachers")
async def get_teachers(id_check: int, api_key: str = Header(...)):
    await(validate_api_key(api_key))
    await(validate_permissions(id_check, [ProfileEnum.TEACHER.value]))
    return get_teachers_from_db()

# Get laborals
@app.get("/api/user/get/laborals")
async def get_laborals(id_check: int, api_key: str = Header(...)):
    await(validate_api_key(api_key))
    await(validate_permissions(id_check, [ProfileEnum.TEACHER.value]))
    return get_laborals_from_db()

# Get disabled users
@app.get("/api/user/get/disabled")
async def get_disabled_users(id_check: int, api_key: str = Header(...)):
    await(validate_api_key(api_key))
    await(validate_permissions(id_check, [ProfileEnum.TEACHER.value]))
    return get_disabled_users_from_db()

# Add student
@app.post("/api/user/add-student")
async def add_student(id_check: int, student: UserCreate, api_key: str = Header(...)):
    await(validate_api_key(api_key))
    await(validate_permissions(id_check, [ProfileEnum.TEACHER.value]))
    return insert_user_to_db(student, ProfileEnum.STUDENT, StatusEnum.DISABLED)

# Add teacher
@app.post("/api/user/add-teacher")
async def add_teacher(id_check: int, teacher: UserCreate, api_key: str = Header(...)):
    await(validate_api_key(api_key))
    await(validate_permissions(id_check, [ProfileEnum.ADMIN.value]))
    return insert_user_to_db(teacher, ProfileEnum.TEACHER, StatusEnum.ENABLED)

# Add laboral tutor
@app.post("/api/user/add-labor")
async def add_labor(id_check: int, labor: UserCreate, api_key: str = Header(...)):
    await(validate_api_key(api_key))
    await(validate_permissions(id_check, [ProfileEnum.TEACHER.value]))
    return insert_user_to_db(labor, ProfileEnum.LABOR, StatusEnum.ENABLED)

# Add students set by XML
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
    return delete_user_from_db(id_user)

# Update user
@app.put("/api/user/update")
async def update_user(id_check: int, id_user: int, updated_fields: dict, api_key: str = Header(...)):
    await(validate_api_key(api_key))
    permissions = [ProfileEnum.STUDENT.value, ProfileEnum.TEACHER.value, ProfileEnum.LABOR.value]
    profile = await(validate_permissions(id_check, permissions))
    return update_user_from_db(id_check, id_user, updated_fields, profile)

# Change status
@app.put("/api/user/change-status")
async def update_user_status(id_check: int, id_user: int, new_status: int, api_key: str = Header(...)):
    await(validate_api_key(api_key))
    await(validate_permissions(id_check, [ProfileEnum.TEACHER.value]))
    return update_user_status_from_db(id_user, new_status)

# Login
@app.post("/api/user/login")
async def login(auth: LoginCreate, api_key: str = Header(...)):
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
    profile = await(validate_permissions(id_check, [ProfileEnum.TEACHER.value, ProfileEnum.STUDENT.value]))
    return get_company_from_db(id_check, id_company, profile)

# Get all companies
@app.get("/api/company/get/all")
async def get_all_companies(id_check: int, api_key: str = Header(...)):
    await(validate_api_key(api_key))
    await(validate_permissions(id_check, [ProfileEnum.TEACHER.value]))
    return get_all_companies_from_db()

# Add company
@app.post("/api/company/add")
async def add_company(id_check: int, company: CompanyCreate, api_key: str = Header(...)):
    await(validate_api_key(api_key))
    await(validate_permissions(id_check, [ProfileEnum.TEACHER.value]))
    return insert_company_to_db(company)

# Delete company
@app.delete("/api/company/delete")
async def delete_company(id_check: int, id_company: int, api_key: str = Header(...)):
    await(validate_api_key(api_key))
    await(validate_permissions(id_check, [ProfileEnum.TEACHER.value]))
    return delete_company_from_db(id_company)

# Update company
@app.put("/api/company/update")
async def update_company(id_check: int, id_company: int, updated_fields: dict, api_key: str = Header(...)):
    await(validate_api_key(api_key))
    await(validate_permissions(id_check, [ProfileEnum.TEACHER.value]))
    return update_company_from_db(id_company, updated_fields)

########## UNIT ##########

## Get unit
@app.get("/api/unit/get")
async def get_unit(id_check: int, id_unit: int, api_key: str = Header(...)):
    await(validate_api_key(api_key))
    await(validate_permissions(id_check, [ProfileEnum.TEACHER.value]))
    return get_unit_from_db(id_unit)

# Get all units
@app.get("/api/unit/get/all")
async def get_all_units(id_check: int, api_key: str = Header(...)):
    await(validate_api_key(api_key))
    await(validate_permissions(id_check, [ProfileEnum.ADMIN.value]))
    return get_all_units_from_db()

# Add unit
@app.post("/api/unit/add")
async def add_unit(id_check: int, unit: UnitCreate, api_key: str = Header(...)):
    await(validate_api_key(api_key))
    await(validate_permissions(id_check, [ProfileEnum.ADMIN.value]))
    return insert_unit_to_db(unit)

# Delete unit
@app.delete("/api/unit/delete")
async def delete_unit(id_check: int, id_unit: int, api_key: str = Header(...)):
    await(validate_api_key(api_key))
    await(validate_permissions(id_check, [ProfileEnum.ADMIN.value]))
    return delete_unit_from_db(T_UNIT, ID_NAME_UNIT, id_unit)

# Update unit
@app.put("/api/unit/update")
async def update_unit(id_check: int, id_unit: int, updated_fields: dict, api_key: str = Header(...)):
    await(validate_api_key(api_key))
    await(validate_permissions(id_check, [ProfileEnum.ADMIN.value]))
    return update_unit_from_db(id_unit, updated_fields)

########## MODULE ##########

# Get module #
@app.get("/api/module/get")
async def get_module(id_check: int, id_module: int, api_key: str = Header(...)):
    await(validate_api_key(api_key))
    await(validate_permissions(id_check, [ProfileEnum.TEACHER.value, ProfileEnum.LABOR.value]))
    return get_module_from_db(id_module)

# Get all modules #
@app.get("/api/module/get/all")
async def get_all_modules(id_check: int, api_key: str = Header(...)):
    await(validate_api_key(api_key))
    await(validate_permissions(id_check, [ProfileEnum.ADMIN.value]))
    return get_all_rows(T_MODULE)

# Get module from student OPCIONAL
@app.get("/api/module/get/student-modules")
async def get_modules_of_student(id_check: int, id_student: int, api_key: str = Header(...)):
    await(validate_api_key(api_key))
    await(validate_permissions(id_check, [ProfileEnum.LABOR.value]))
    return get_modules_of_student_from_db(id_student)

# Add module #
@app.post("/api/module/add")
async def add_module(id_check: int, module: ModuleCreate, api_key: str = Header(...)):
    await(validate_api_key(api_key))
    await(validate_permissions(id_check, [ProfileEnum.ADMIN.value]))
    return insert_module_to_db(module)

# Delete module #
@app.delete("/api/module/delete")
async def delete_module(id_check: int, id_module: int, api_key: str = Header(...)):
    await(validate_api_key(api_key))
    await(validate_permissions(id_check, [ProfileEnum.ADMIN.value]))
    return delete_module_from_db(id_module)

# Update module #
@app.put("/api/module/update")
async def update_module(id_check: int, id_module: int, updated_fields: dict, api_key: str = Header(...)):
    await(validate_api_key(api_key))
    await(validate_permissions(id_check, [ProfileEnum.ADMIN.value]))
    return update_module_from_db(id_module, updated_fields)

########## ENTRY ##########

@app.get("/api/entry/get")
async def get_entry(id_check: int, id_entry: int, api_key: str = Header(...)):
    await(validate_api_key(api_key))
    profile = await(validate_permissions(id_check, [ProfileEnum.STUDENT.value, ProfileEnum.TEACHER.value, ProfileEnum.LABOR.value]))
    return get_entry_from_db(id_entry, profile)

# Add entry MIRAR FECHA DE LA ENTRADA
@app.post("/api/entry/add")
async def add_entry(id_check: int, entry: EntryCreate, api_key: str = Header(...)):
    await(validate_api_key(api_key))
    await(validate_permissions(id_check, [ProfileEnum.STUDENT.value]))
    return insert_entry_to_db(entry)

#

## HAY QUE CHECKEAR SI ES LABOR QUE SOLO SEAN LAS ENTRADAS DE LOS QUE TUTORIZA,
# Y SI ES ALUMNO SOLO SUS PROPIAS ENTRADAS, SI NO, DENEGAR

# Get student entries
@app.get("/api/user/get-entries")
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


########## COMMENT ##########

## Get comment
@app.get("/api/comment/get")
async def get_comment(id_check: int, id_day: int, api_key: str = Header(...)):
    await(validate_api_key(api_key))
    await(validate_permissions(id_check, [ProfileEnum.STUDENT.value, ProfileEnum.TEACHER.value, ProfileEnum.LABOR.value]))
    return get_day_from_db(id_day)

## Update day
@app.put("/api/comment/update")
async def update_comment(id_check: int, id_day: int, updated_fields: dict, api_key: str = Header(...)):
    await(validate_api_key(api_key))
    await(validate_permissions(id_check, [ProfileEnum.STUDENT.value]))
    return update_table_db(T_DAY, ID_NAME_DAY, id_day, updated_fields)

########## AGREEMENT ##########

# Get agreement
@app.get("/api/agreement/get")
async def get_agreement(id_check: int, id_agreement: int, api_key: str = Header(...)):
    await(validate_api_key(api_key))
    permissions = [ProfileEnum.STUDENT.value, ProfileEnum.TEACHER.value, ProfileEnum.LABOR.value]
    profile = await(validate_permissions(id_check, permissions))
    return get_agreement_from_db(id_agreement, profile)

# Get all agreements
@app.get("/api/agreement/get/all")
async def get_all_agreements(id_check: int, api_key: str = Header(...)):
    await(validate_api_key(api_key))
    await(validate_permissions(id_check, [ProfileEnum.TEACHER.value]))
    return get_all_agreements_from_db()

# Add agreement
@app.post("/api/agreement/add")
async def add_agreement(id_check: int, agreement: AgreementCreate, api_key: str = Header(...)):
    await(validate_api_key(api_key))
    await(validate_permissions(id_check, [ProfileEnum.TEACHER.value]))
    return insert_agreement_to_db(agreement)

# Delete agreement
@app.delete("/api/agreement/delete")
async def delete_agreement(id_check: int, id_agreement: int, api_key: str = Header(...)):
    await(validate_api_key(api_key))
    await(validate_permissions(id_check, [ProfileEnum.TEACHER.value]))
    return delete_agreement_from_db(id_agreement)

# Update agreement
@app.put("/api/agreement/update")
async def update_agreement(id_check: int, id_agreement: int, updated_fields: dict, api_key: str = Header(...)):
    await(validate_api_key(api_key))
    await(validate_permissions(id_check, [ProfileEnum.TEACHER.value]))
    return update_agreement_from_db(id_agreement, updated_fields)

########## SCHOLAR YEAR ##########

# Add scholar year
@app.post("/api/scholar-year/add")
async def add_scholar_year(id_check: int, scholar_year: ScholarYearCreate, api_key: str = Header(...)):
    await(validate_api_key(api_key))
    await(validate_permissions(id_check, [ProfileEnum.ADMIN.value]))
    return insert_scholar_year_to_db(scholar_year)

# Update grade duration
@app.put("/api/scholar-year/grade-duration")
async def update_grade_duration(id_check: int, start_date: str, end_date: str, api_key: str = Header(...)):
    await(validate_api_key(api_key))
    await(validate_permissions(id_check, [ProfileEnum.ADMIN.value]))
    return update_grade_duration_from_db(start_date, end_date)

# Update holidays
@app.put("/api/scholar-year/holidays")
async def update_holidays(id_check: int, holidays: dict, api_key: str = Header(...)):
    await(validate_api_key(api_key))
    await(validate_permissions(id_check, [ProfileEnum.ADMIN.value]))
    return update_holidays_from_db(holidays)

# Update ponderation
@app.put("/api/scholar-year/ponderation")
async def update_ponderation(id_check: int, aptitudes_percent: int, subjects_percent: int, api_key: str = Header(...)):
    await(validate_api_key(api_key))
    await(validate_permissions(id_check, [ProfileEnum.ADMIN.value]))
    return update_ponderation_from_db(aptitudes_percent, subjects_percent)

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