import mysql.connector
import datetime
from datetime import timedelta
import xml.etree.ElementTree as ET
from mysql.connector.errors import IntegrityError
from fastapi.exceptions import HTTPException
from exceptions import *
from models import *
from utils import *

########## USER ##########

# Get user
def get_user_from_db(id_check: int, id_user: int, profile: str):

    grant_access = False

    # If its an admin or a teacher, always grant access
    if profile in [ProfileEnum.ADMIN.value, ProfileEnum.TEACHER.value]:
        grant_access = True

    # Else if its a student, grant access if its his/her own profile
    elif profile == ProfileEnum.STUDENT.value and id_check == id_user:
        grant_access = True

    # Else if its a laboral tutor, grant access if its his/her own profile or its his/her student
    elif profile == ProfileEnum.LABOR.value and id_check == id_user or is_student_under_labor_tutor(id_check, id_user):
        grant_access = True

    # Return the user if has granted access
    if grant_access:
        return get_row(T_USER, ID_NAME_USER, id_user)

    # Raise exception if has NOT granted access
    else:
        raise HTTPException(status_code=401, detail="Permission denied")

# Get students
def get_students_from_db():
    return get_all_rows_condition(T_USER, "profile", ProfileEnum.STUDENT.value)

# Get teachers
def get_teachers_from_db():
    return get_all_rows_condition(T_USER, "profile", ProfileEnum.TEACHER.value)

# Get laborals
def get_laborals_from_db():
    return get_all_rows_condition(T_USER, "profile", ProfileEnum.LABOR.value)

# Get disabled users
def get_disabled_users_from_db():
    return get_all_rows_condition(T_USER, "isActive", StatusEnum.DISABLED.value)

# Get user role or profile
def get_profile_from_user(id_user: int):

    try:

        # Get the connection and the cursor
        conn, cursor = get_conn_and_cursor()

        # Get the user profile
        query = f"SELECT profile FROM {T_USER} WHERE {ID_NAME_USER} = {id_user}"
        cursor.execute(query)
        result = cursor.fetchone()[0]
        close_conn_and_cursor(conn, cursor)

        # Map the result to the corresponding enum value
        if result == "1":
            return ProfileEnum.ADMIN.value
        elif result == "2":
            return ProfileEnum.STUDENT.value
        elif result == "3":
            return ProfileEnum.TEACHER.value
        elif result == "4":
            return ProfileEnum.LABOR.value
        else:
            raise ValueError(f"Invalid profile value: {result}")

    except Exception as e:
        raise GetUserException(f"error: {str(e)}")

# Insert user
def insert_user_to_db(user: UserCreate, profile: ProfileEnum, status: StatusEnum):

    try:
        # Check if email, name, and surname fields are not empty
        if not user.email or not user.name or not user.surname:
            raise InsertUserException("error adding user, required fields are missing")

        # Get the connection and the cursor
        conn, cursor = get_conn_and_cursor()

        # Query to check email
        check_email_query = f"SELECT email FROM {T_USER} WHERE email = '{user.email}'"
        cursor.execute(check_email_query)
        result = cursor.fetchone()

        if result:
            # Email exists
            raise HTTPException(status_code=409, detail="Error adding user, email already registered")

        # Query
        query = f"INSERT INTO {T_USER} (name, surname, email, password, picture, linkedin, github, twitter, profile, isActive) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

        # Values for the query
        values = (
            user.name,
            user.surname,
            user.email,
            user.password,
            user.picture,
            user.linkedin,
            user.github,
            user.twitter,
            profile.value,
            status.value
        )

        # Execute query
        cursor.execute(query, values)

        # Commit changes and close connections
        do_commit(conn, cursor)

        return {"message": "User inserted successfully"}

    except IntegrityError as e:
        # Rollback changes and close connections
        rollback(conn, cursor)
        return {"error": str(e)}

# Insert users by XML
def insert_students_to_db_xml(students_xml: str):

    try:
        root = ET.fromstring(students_xml)
    except Exception as e:
        # If there's an error parsing the XML or inserting into the database, raise an HTTPException
        raise HTTPException(status_code=400, detail=str(e))

    successful_inserts = []
    failed_inserts = []

    for position, student in enumerate(root, start=1):

        # Insert the student. If fails, continue the loop to get the next student
        try:
            student = extract_student_data_from_xml(student, position)
            insert_user_to_db(student, ProfileEnum.STUDENT, StatusEnum.DISABLED)
            # send_email_generating_password(email)
            successful_inserts.append(f"{student.surname}, {student.name}")
        except Exception as e:
            failed_inserts.append((position, str(e)))
            continue

    if len(failed_inserts) == 0:
        return {'message': 'All users inserted successfully'}
    else:
        message = "Some users were not inserted" if len(successful_inserts) else "No users were inserted"
        failed_inserts_position = [insert[0] for insert in failed_inserts]
        error_messages = [insert[1] for insert in failed_inserts]
        return {'message': message, 'successful_inserts': successful_inserts, 'failed_inserts': f'Students {failed_inserts_position} were not inserted', 'error_messages': error_messages}

# Delete user
def delete_user_from_db(id_user: int):
    profile = get_profile_from_user(id_user)
    if(profile == ProfileEnum.ADMIN.value):
        raise HTTPException(status_code=403, detail="This user can not be deleted")
    return delete_row(T_USER, ID_NAME_USER, id_user)

# Update user
def update_user_from_db(id_check: int, id_user: int, updated_fields: dict, profile: str):

    grant_access = False
    # Profile of the user that is going to be updated
    profile_of_user_updating = get_profile_from_user(id_user)

    # If is an Admin, always grant access
    if profile == ProfileEnum.ADMIN.value:
        grant_access = True

    # Else if is a Student or Laboral tutor, only can update their own data
    elif profile in [ProfileEnum.STUDENT.value, ProfileEnum.LABOR.value] and id_check == id_user:
        grant_access = True

    # Else if is an Teacher, grant access if the user that is going to be updated is not an admin or teacher
    elif profile == ProfileEnum.TEACHER.value and id_check == id_user or profile_of_user_updating not in [ProfileEnum.ADMIN.value, ProfileEnum.TEACHER.value]:
        grant_access = True

    # Update the user if has granted access
    if grant_access:
        return update_table(T_USER, ID_NAME_USER, id_user, updated_fields)
    # Raise exception if has NOT granted access
    else:
        raise HTTPException(status_code=401, detail="Permission denied")

# Update user status
def update_user_status_from_db(id_user: int, new_status: int):

    # Update the user status
    conn, cursor = get_conn_and_cursor()
    query = f"UPDATE {T_USER} SET isActive = %s WHERE {ID_NAME_USER} = %s"
    values = (new_status, id_user)
    cursor.execute(query, values)

    # Commit the changes and close connections
    do_commit(conn, cursor)

    return {"message": "User status changed successfully"}

# Get entries
def get_entries_from_user(id_student: int):
    # Get the idAgreement
    # RUTA: obtener el agreement a partir del profileUser,obtener los entries del agreement
    # Get the connection and the cursor
    conn, cursor = get_conn_and_cursor()

    query = f"SELECT {ID_NAME_AGREEMENT} FROM {T_AGREEMENT} WHERE {ID_NAME_STUDENT} = {id_student}"

    cursor.execute(query)

    id_agreement = cursor.fetchone()[0]

    # Get the entries
    query = f"SELECT * FROM {T_ENTRY} WHERE {ID_NAME_AGREEMENT} = {id_agreement}"

    cursor.execute(query)
    results = cursor.fetchall()

    rows = []
    columns = [column[0] for column in cursor.description]

    for row in results:
        row_dict = dict(zip(columns, row))
        rows.append(row_dict)

    # Close connections
    close_conn_and_cursor(conn, cursor)
    return rows

########## COMPANY ##########

# Get company
def get_company_from_db(id_check: int, id_company: int, profile: str):

    grant_access = False

    # If its a teacher or admin, grant access
    if profile in [ProfileEnum.TEACHER.value, ProfileEnum.ADMIN.value]:
        grant_access = True

    # If its an student, check if its his/her company
    elif profile == ProfileEnum.STUDENT.value and is_student_company(id_check, id_company):
        grant_access = True

    # Return the company if has granted access
    if grant_access:
        return get_row(T_COMPANY, ID_NAME_COMPANY, id_company)
    # Raise exception if has NOT granted access
    else:
        raise HTTPException(status_code=401, detail="Permission denied")

# Get all companies
def get_all_companies_from_db():
    return get_all_rows(T_COMPANY)

# Insert company
def insert_company_to_db(company: CompanyCreate):

    # Get the connection and the cursor
    conn, cursor = get_conn_and_cursor()

    # Ejecutar la consulta INSERT
    query = f"INSERT INTO {T_COMPANY} (name, address, latitude, longitude, phone) VALUES (%s, %s, %s, %s, %s)"
    values = (company.name, company.address, company.latitude, company.longitude, company.phone)
    cursor.execute(query, values)

    # Obtener el ID de la nueva compañía
    new_id = cursor.lastrowid

    # Hacer commit de los cambios y cerrar la conexión
    do_commit(conn, cursor)

    # Devolver el ID de la nueva compañía
    return {"message": f"Company with id {new_id} has been added."}

# Delete company
def delete_company_from_db(id_company: int):
    return delete_row(T_COMPANY, ID_NAME_COMPANY, id_company)

# Update company
def update_company_from_db(id_company: int, updated_fields: dict):
    return update_table(T_COMPANY, ID_NAME_COMPANY, id_company, updated_fields)

########## UNIT ##########

# Get unit
def get_unit_from_db(id_unit: int):
    return get_row(T_UNIT, ID_NAME_UNIT, id_unit)

# Get all unit
def get_all_units_from_db():
    return get_all_rows(T_UNIT)

# Insert unit
def insert_unit_to_db(unit: UnitCreate):
    # Obtener la conexión y el cursor
    conn, cursor = get_conn_and_cursor()

    # Ejecutar la consulta INSERT
    query = f"INSERT INTO {T_UNIT} (level, name, initials, charUnit, unitType) VALUES (%s, %s, %s, %s, %s)"
    values = (unit.level, unit.name, unit.initials, "A", unit.unitType)
    cursor.execute(query, values)

    # Obtener el ID de la nueva unidad
    new_id = cursor.lastrowid

    # Hacer commit de los cambios y cerrar la conexión
    do_commit(conn, cursor)

    # Devolver el ID de la nueva unidad
    return {"message": f"Unit with id {new_id} has been added."}

# Delete unit
def delete_unit_from_db(id_unit: int):
    return delete_row(T_UNIT, ID_NAME_UNIT, id_unit)

# Update unit
def update_unit_from_db(id_unit: int, updated_fields: dict):
     return update_table(T_UNIT, ID_NAME_UNIT, id_unit, updated_fields)

########## MODULE ##########

# Get module
def get_module_from_db(id_module: int):
    return get_row(T_MODULE, ID_NAME_MODULE, id_module)

# Get all modules

# Get modules from student
def get_modules_of_student_from_db(id_student: int):
    # I have to get the current scholar year id,
    # the student id and unit where idAgreement is not null in the table student_scholar_year
    # like this, i will get only a row. Of this row, take the unit
    return 

# Insert module
def insert_module_to_db(module: ModuleCreate):
    # Get the connection and the cursor
    conn, cursor = get_conn_and_cursor()

    # Ejecutar la consulta INSERT
    query = f"INSERT INTO {T_MODULE} (name, initials, hours, idUnit) VALUES (%s, %s, %s, %s)"
    values = (module.name, module.initials, int(module.hours), int(module.idUnit))
    cursor.execute(query, values)
    
    # Hacer commit de los cambios y cerrar la conexión
    do_commit(conn, cursor)

    # Devolver el ID del nuevo módulo
    return {"message": "Module inserted successfully"}

# Delete module
def delete_module_from_db(id_module: int):
    return delete_row(T_MODULE, ID_NAME_MODULE, id_module)

# Update module
def update_module_from_db(id_module: int, updated_fields: dict):
    return update_table(T_MODULE, ID_NAME_MODULE, id_module, updated_fields)

########## ENTRY ##########

# Get entry
def get_entry_from_db(id_check: int, id_entry: int, profile: str):
    
    grant_access = False

    # If is an Admin or Teacher, always grant access to the entry
    if profile in [ProfileEnum.ADMIN.value, ProfileEnum.TEACHER.value]:
        grant_access = True

    # Else if is a Student, only grant access if its his/her entry
    elif profile == ProfileEnum.STUDENT.value:
        return

    if grant_access:
        return get_row(T_ENTRY, ID_NAME_ENTRY, id_entry)
    else:
        raise HTTPException(status_code=401, detail="Permission denied")
    
# Get entries
def get_all_entries_from_student(id_student: int, profile):

    grant_access = False

    # If is an Admin or Teacher, always grant access to the student entries
    if profile in [ProfileEnum.ADMIN.value, ProfileEnum.TEACHER.value]:
        grant_access = True
    

    if grant_access:
        # TIENE QUE DEVOLVER LAS ENTRADAS DE UN USUARIO SOLO, Y DE EL ÚLTIMO CURSO ESCOLAR
        return
    else:
        raise HTTPException(status_code=401, detail="Permission denied")

# Insert entry
def insert_entry_to_db(entry: EntryCreate):

    # Get the current date
    today = datetime.today().date()

    # Calculate the date range
    start_date = today - timedelta(days=today.weekday())
    end_date = start_date + timedelta(days=6)

    # Get the connection and the cursor
    conn, cursor = get_conn_and_cursor()

    # Insert the entry
    query = f"INSERT INTO {T_ENTRY} (startWeek, endWeek, idAgreement) VALUES (%s, %s, %s)"
    values = (start_date, end_date, int(entry.idAgreement))
    cursor.execute(query, values)
    conn.commit()

    # Get the id of the inserted entry
    new_entry_id = cursor.lastrowid

    agreement = get_row(T_AGREEMENT, ID_NAME_AGREEMENT, entry.idAgreement)

    agreement_type = agreement.get('agreementType')
    fct_start_at = agreement.get('fctStartAt', None)
    fct_end_at = agreement.get('fctEndAt', None)

    # Now I have to add 5 rows to the comments table,
    # if the user agreement is FCT,
    # or if is FCT+DUAL and the current date is between fctStartDate and fctEndDate
    # The comment table has idComment as primary and idEntry as foreign, the id of the entry inserted


    if agreement_type == AgreementTypeEnum.FCT.value or (agreement_type == AgreementTypeEnum.FCT_DUAL.value and is_in_fct_date(fct_start_at, fct_end_at, today)):
        # Add five comments (Days of the week)
        for _ in range(5):
            # Insert comment into the comments table
            query = f"INSERT INTO {T_COMMENT} (text, hours, observations, idEntry) VALUES (%s, %s, %s, %s)"
            values = ("", 70000, None, new_entry_id)
            cursor.execute(query, values)
    else:
        # Insertar el MODULO
        modules = get_modules_of_student_from_db()
        return
    
     # Commit after loop
    do_commit(conn, cursor)

    return {"message": "Entry inserted successfully"}


# Delete entry

########## DAY ##########

# Get day
def get_day_from_db(id_day: int):
    conn, cursor = get_conn_and_cursor()
    # Get the entries
    query = f"SELECT * FROM {T_DAY} WHERE {ID_NAME_DAY} = {id_day}"

    cursor.execute(query)

    result = cursor.fetchone()
    row = {}
    if result:
        for i, column in enumerate(cursor.description):
            row[column[0]] = result[i]
    return row

# Login
def login_from_db(auth: LoginCreate):
    conn, cursor = get_conn_and_cursor()
    # Get the entries
    query = f"SELECT * FROM {T_USER} WHERE email = '{auth.email}' AND password = '{auth.password}'"

    cursor.execute(query)
    result = cursor.fetchone()
    close_conn_and_cursor(conn, cursor)
    row = {}
    if result:
        for i, column in enumerate(cursor.description):
            row[column[0]] = result[i]
    return row


# Drop the database
def drop_db():

    try:

        # Get the connection and the cursor
        conn, cursor = get_conn_and_cursor()

        # Execute DROP DATABASE query
        cursor.execute(f"DROP DATABASE {DATABASE}")
        close_conn_and_cursor(conn, cursor)
        return {"message": f"The {DATABASE} database has been dropped"}

    except mysql.connector.Error as e:
        # The specified database does not exist
        if e.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
            return {"error": f"The {DATABASE} database does not exist"}
        # The user does not have access to the specified database
        elif e.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
            return {"error": "Access denied"}
        # Some other error occurred
        else:
            return {"error": "An error occurred while dropping the database."}

########## General SELECT for all tables  ##########

# Get row
def get_row(table_name: str, id_name: int, id_value: int):

    try:
        # Get the connection and the cursor
        conn, cursor = get_conn_and_cursor()

        # Get the table's column names
        select_columns_query = f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}'"
        cursor.execute(select_columns_query)
        column_names = [col[0] for col in cursor.fetchall()]

        # Query to get the object
        select_object_query = f"SELECT * FROM {table_name} WHERE {id_name} = {id_value}"

        # Execute query to retrieve the object
        cursor.execute(select_object_query)
        object = cursor.fetchone()

        

        # Format the object with column names
        formatted_object = None
        if object != None:
            formatted_object = { column_names[i]: value for i, value in enumerate(object) }
            if formatted_object != None:
                return formatted_object
            else:
                return {"error": "Object has not been built correctly"}
        else:
            return
            

    except Exception as e:
        # Rollback changes and close connections
        conn.rollback()
        raise Exception(f"Error retrieving the object: {str(e)}")
    
    finally:
        cursor.close()
        conn.close()

# Get all rows
def get_all_rows(table_name: str):
    try:
        # Get the connection and the cursor
        conn, cursor = get_conn_and_cursor()

        # Get the table's column names
        select_columns_query = f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}'"
        cursor.execute(select_columns_query)
        column_names = [col[0] for col in cursor.fetchall()]

        # Query to get all rows
        select_all_rows_query = f"SELECT * FROM {table_name}"

        # Execute query to retrieve all rows
        cursor.execute(select_all_rows_query)
        rows = cursor.fetchall()

        # Format the rows with column names
        formatted_rows = []
        for row in rows:
            formatted_row = {column_names[i]: value for i, value in enumerate(row)}
            formatted_rows.append(formatted_row)

        return formatted_rows

    except Exception as e:
        # Rollback changes and close connections
        conn.rollback()
        raise Exception(f"Error retrieving rows from the table: {str(e)}")
    
    finally:
        cursor.close()
        conn.close()

# Get all rows with condition
def get_all_rows_condition(table_name: str, condition: str, value):
    try:
        # Get the connection and the cursor
        conn, cursor = get_conn_and_cursor()

        # Get the table's column names
        select_columns_query = f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}'"
        cursor.execute(select_columns_query)
        column_names = [col[0] for col in cursor.fetchall()]

        # Query to get all rows
        select_all_rows_query = f"SELECT * FROM {table_name} WHERE {condition} = {value}"

        # Execute query to retrieve all rows
        cursor.execute(select_all_rows_query)
        rows = cursor.fetchall()

        # Format the rows with column names
        formatted_rows = []
        for row in rows:
            formatted_row = {column_names[i]: value for i, value in enumerate(row)}
            formatted_rows.append(formatted_row)

        return formatted_rows

    except Exception as e:
        # Rollback changes and close connections
        conn.rollback()
        raise Exception(f"Error retrieving rows from the table: {str(e)}")
    
    finally:
        cursor.close()
        conn.close()

########## General UPDATE for all tables  ##########

def update_table(table_name: str, id_name: str, id_value: int, updated_fields: dict):

    try:
        # Get the connection and the cursor
        conn, cursor = get_conn_and_cursor()

        # Check if the object exists
        select_query = f"SELECT * FROM {table_name} WHERE {id_name} = {id_value}"
        cursor.execute(select_query)
        row = cursor.fetchone()
        if not row:
            raise ValueError("Object not found")

        # Get the update query and the values
        query, values = get_update_query_and_values(table_name, id_name, id_value, updated_fields)

        # Execute the query
        cursor.execute(query, values)

        # Commit changes
        do_commit(conn, cursor)

        # Get the updated object
        formatted_updated_obj = get_row(table_name, id_name, id_value)

        return {"message": f"{table_name.capitalize()} updated successfully", "result": formatted_updated_obj}

    except Exception as e:
        # Rollback changes and close connections
        rollback(conn, cursor)
        return {"error": f"Error updating the object: {str(e)}"}

########## General DELETE for all tables  ##########

# CAMBIAR EL MENSAJE SI NO BORRA UN OBJETO PORQUE NO LO ENCUENTRA
def delete_row(table_name: str, id_name: str, id_value: int):

    try:
        # Get the connection and the cursor
        conn, cursor = get_conn_and_cursor()

        # Get the object that is going to be deleted
        formatted_deleted_obj = get_row(table_name, id_name, id_value)

        # Delete object
        delete_query = f"DELETE FROM {table_name} WHERE {id_name} = {id_value}"
        cursor.execute(delete_query)
        conn.commit()

        # Error message
        if formatted_deleted_obj == None:
            return {"error": "Object not found"}
        # Success message with deleted object
        return {"message": f"{table_name.capitalize()} with id {id_value} has been deleted.", "result": formatted_deleted_obj}

    except Exception as e:

        # Rollback changes
        conn.rollback()

        # Failure message
        return {"error": str(e)}
    
    finally:
        cursor.close()
        conn.close()

########## AGREEMENT ##########

# Get agreement
def get_agreement_from_db(id_agreement: int, profile: str):

    grant_access = False

    # If its an Admin or Teacher, grant access
    if profile in [ProfileEnum.ADMIN.value, ProfileEnum.TEACHER.value]:
        grant_access = True

    # Else if its a Student and is requesting for his own agreement, grant access
    elif profile == ProfileEnum.STUDENT.value and is_student_agreement():
        grant_access = True

    # Else if its a Laboral tutor and is requesting for the agreement of their students, grant access
    elif profile == ProfileEnum.LABOR.value and is_agreement_from_his_students():
        grant_access = True
    
    # Return the agreement if has granted access
    if grant_access:
        return get_row(T_AGREEMENT, ID_NAME_AGREEMENT, id_agreement)
    # Raise exception if has NOT granted access
    else:
        raise HTTPException(status_code=401, detail="Permission denied")

# Get all agreements
def get_all_agreements_from_db():
    return get_all_rows(T_AGREEMENT)

# Insert agreement
def insert_agreement_to_db(agreement: AgreementCreate):

    try:

        # Get the connection and the cursor
        conn, cursor = get_conn_and_cursor()

        # Check if the foreign keys with the roles are valid
        if get_profile_from_user(agreement.idTeacher) != ProfileEnum.TEACHER:
            raise HTTPException(status_code=400, detail="Role for the provided idTeacher is wrong")
        
        if get_profile_from_user(agreement.idLabor) != ProfileEnum.LABOR:
            raise HTTPException(status_code=400, detail="Role for the provided idLabor is wrong")

        if agreement.agreementType == AgreementTypeEnum.DUAL:
            agreement.fctStartAt = None
            agreement.fctEndAt = None
        elif agreement.agreementType == AgreementTypeEnum.FCT:
            agreement.dualStartAt = None
            agreement.dualEndAt = None

        # Query
        query = f"INSERT INTO {T_AGREEMENT} (dualStartAt, dualEndAt, fctStartAt, fctEndAt, agreementType, idCompany, idTeacher, idLabor) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

        # Values for the query
        values = (
            agreement.dualStartAt,
            agreement.dualEndAt,
            agreement.fctStartAt,
            agreement.fctEndAt,
            agreement.agreementType,
            agreement.idCompany,
            agreement.idTeacher,
            agreement.idLabor
        )

        # Execute query
        cursor.execute(query, values)

        # Get the ID of the new row
        new_id = cursor.lastrowid

        # Commit changes and close connections
        do_commit(conn, cursor)

        inserted_agreement = get_row(T_AGREEMENT, ID_NAME_AGREEMENT, new_id)

        return {"message": "Agreement inserted successfully", "result": inserted_agreement}

    except IntegrityError as e:
        # Rollback changes and close connections
        rollback(conn, cursor)
        return {"error": str(e)}

# Delete agreement
def delete_agreement_from_db(id_agreement: int):
    return delete_row(T_AGREEMENT, ID_NAME_AGREEMENT, id_agreement)

# Update agreement
def update_agreement_from_db(id_agreement: int, updated_fields: dict):
    return update_table(T_AGREEMENT, ID_NAME_AGREEMENT, id_agreement, updated_fields)

########## SCHOLAR YEAR ##########

# Get scholar year
def get_scholar_year_from_db(id_scholar_year: int):
    return

# Insert scholar year
def insert_scholar_year_to_db(scholar_year: ScholarYearCreate):

    # Check that date format is valid
    if is_date_format_valid([scholar_year.startDate, scholar_year.endDate], DATE_FORMAT) == False:
        raise HTTPException(status_code=400, detail="Incorrect date format")
    
    # Check that start date is smaller than end date
    if scholar_year.startDate >= scholar_year.endDate:
        raise HTTPException(status_code=400, detail="Start date must be before end date")
    
    # Set the year between two dates as YYYY-YYYY format, 2022-2023
    year = get_year_from_dates(scholar_year.startDate, scholar_year.endDate)

    # Get the connection and the cursor
    conn, cursor = get_conn_and_cursor()

    # Execute the insert query and commit
    query = f"INSERT INTO {T_SCHOLAR_YEAR} (startDate, endDate, year, aptitudesPonderation, subjectsPonderation, holidays) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (scholar_year.startDate, scholar_year.endDate, year, scholar_year.aptitudesPonderation, scholar_year.subjectsPonderation, scholar_year.holidays)
    cursor.execute(query, values)
    new_id = cursor.lastrowid
    do_commit(conn, cursor)

    # Get the row inserted
    inserted_scholar_year = get_row(T_SCHOLAR_YEAR, ID_NAME_SCHOLAR_YEAR, new_id)

    # Return the inserted row
    return {"message": f"Scholar year inserted successfully", "result": inserted_scholar_year}

# Update grade duration from last scholar year
def update_grade_duration_from_db(start_date: str, end_date: str):

    # Check that date format is valid
    if is_date_format_valid([start_date, end_date], DATE_FORMAT) == False:
        raise HTTPException(status_code=400, detail="Incorrect date format")
    
    # Check that start date is smaller than end date
    if start_date and end_date and start_date >= end_date:
        raise HTTPException(status_code=400, detail="Start date must be before end date")
    
    year = get_year_from_dates(start_date, end_date)
    grade_duration = {"startDate": start_date, "endDate": end_date, "year": year}
    max_id = get_max_id_from_table(T_SCHOLAR_YEAR, ID_NAME_SCHOLAR_YEAR)
    return update_table(T_SCHOLAR_YEAR, ID_NAME_SCHOLAR_YEAR, max_id, grade_duration)

# Update holidays from last scholar year
def update_holidays_from_db(holidays: dict):
    max_id = get_max_id_from_table(T_SCHOLAR_YEAR, ID_NAME_SCHOLAR_YEAR)
    return update_table(T_SCHOLAR_YEAR, ID_NAME_SCHOLAR_YEAR, max_id, holidays)

# Update ponderation from last scholar year
def update_ponderation_from_db(aptitudes: int, subjects: int):

    # If ponderation does not equal 100, raise HTTPException
    if aptitudes + subjects != 100:
        raise HTTPException(status_code=400, detail="Aptitudes and Subjects must sum a total of 100")
    
    # If ponderation equals 100, update it
    ponderation = {"aptitudesPonderation": aptitudes, "subjectsPonderation": subjects}
    max_id = get_max_id_from_table(T_SCHOLAR_YEAR, ID_NAME_SCHOLAR_YEAR)
    return update_table(T_SCHOLAR_YEAR, ID_NAME_SCHOLAR_YEAR, max_id, ponderation)
