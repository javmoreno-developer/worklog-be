import mysql.connector
from mysql.connector.errors import IntegrityError
from fastapi.exceptions import HTTPException
import xml.etree.ElementTree as ET
from exceptions import *
from models import *
from utils import *

class ProfileEnum(str, Enum):
    ADMIN = '1'
    STUDENT = '2'
    TEACHER = '3'
    LABOR = '4'


def insert_company_to_db(company: CompanyCreate):
        # Get the connection and the cursor
        conn, cursor = get_conn_and_cursor()

        # Ejecutar la consulta INSERT
        query = "INSERT INTO company (name, direction, latitude, longitude, phone) VALUES (%s, %s, %s, %s, %s)"
        values = (company.name, company.direction, company.latitude, company.longitude, company.phone)
        cursor.execute(query, values)

        # Obtener el ID de la nueva compañía
        new_id = cursor.lastrowid

        # Hacer commit de los cambios y cerrar la conexión
        do_commit(conn,cursor)

        # Devolver el ID de la nueva compañía
        return {"message": f"Company with id {new_id} has been added."}



def delete_company_from_db(idCompany: int):


        # Get the connection and the cursor
        conn, cursor = get_conn_and_cursor()
        sql = f"DELETE FROM company WHERE idCompany = {idCompany}"
        cursor.execute(sql)
    
        # Hacer commit de los cambios y cerrar la conexión
        do_commit(conn,cursor)

        return {"message": f"Company with id {idCompany} has been deleted."}



def update_company_from_db(company:CompanyCreate,idCompany:int):

        # Get the connection and the cursor
        conn, cursor = get_conn_and_cursor()

        query, values = get_query_and_values("company", "idCompany", idCompany, {"name": company.name,"direction": company.direction,"latitude": company.latitude,"longitude": company.longitude,"phone": company.phone})

        #sql = f"UPDATE company SET name='{company.name}',direction='{company.direction}',latitude={company.latitude},longitude={company.latitude},phone='{company.phone}' WHERE idComp={id}"
        cursor.execute(query,values)
        
        # Hacer commit de los cambios y cerrar la conexión
        do_commit(conn,cursor)

        return {"message": f"Company with id {idCompany} has been updated."}



def insert_module_to_db(module: ModuleCreate):

        # Get the connection and the cursor
        conn, cursor = get_conn_and_cursor()

        # Ejecutar la consulta INSERT
        query = "INSERT INTO module (name, initials, hours, idUnit) VALUES (%s, %s, %s, %s)"
        values = (module.name, module.initials, int(module.hours), int(module.idUnit))
        cursor.execute(query, values)

        # Obtener el ID del nuevo módulo
        new_id = cursor.lastrowid

        # Hacer commit de los cambios y cerrar la conexión
        do_commit(conn,cursor)

        # Devolver el ID del nuevo módulo
        return {"message": f"Module with id {new_id} has been added."}



def delete_module_from_db(idModule: int):

        # Get the connection and the cursor
        conn, cursor = get_conn_and_cursor()

        sql = f"DELETE FROM module WHERE idModule = {idModule}"
        cursor.execute(sql)
        
        # Hacer commit de los cambios y cerrar la conexión
        do_commit(conn,cursor)

        return {"message": f"Module with id {idModule} has been deleted."}

    
def update_module_from_db(module:ModuleCreate,idModule: int):
   
        # Get the connection and the cursor
        conn, cursor = get_conn_and_cursor()

        query, values = get_query_and_values("module", "idModule", idModule, {"name": module.name,"initials": module.initials,"hours": module.hours,"idUnit": module.idUnit})

        #sql = f"UPDATE module SET name='{module.name}',initials='{module.initials}',hours={module.hours},idUni={module.idUni} WHERE idMod={id}"
        cursor.execute(query,values)
        
        # Hacer commit de los cambios y cerrar la conexión
        do_commit(conn,cursor)

        return {"message": f"Module with id {idModule} has been updated."}



def insert_user_to_db(user: UserCreate, profile: ProfileEnum): 
            
    try:
        # Check if email, name, and surname fields are not empty
        if not user.email or not user.name or not user.surname:
            raise InsertUserException("error adding user, required fields are missing")

        # Get the connection and the cursor
        conn, cursor = get_conn_and_cursor()

        # Query to check email
        check_email_query = f"SELECT email FROM user WHERE email = '{user.email}'"
        cursor.execute(check_email_query)
        result = cursor.fetchone()

        if result:
            # Email exists
            raise InsertUserException("error adding user, email already registered")

        # Query
        query = "INSERT INTO user (name, surname, email, password, picture, linkedin, github, twitter, profile) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"

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
            profile.value
        )

        # Execute query
        cursor.execute(query, values)

        # Get the ID of the new row
        id = cursor.lastrowid

        # Commit changes and close connections
        do_commit(conn, cursor)

        inserted_user = get_user_from_db(id)

        return inserted_user
    
    except IntegrityError as e:

        # Rollback changes and close connections
        rollback(conn, cursor)

        raise InsertUserException(f"Error adding user: {str(e)}")

def insert_student_to_db(student: UserCreate):

    try:
        # Insert user and get the user inserted
        insertedUser = insert_user_to_db(student, ProfileEnum.STUDENT)
        
        # Return inserted user
        return insertedUser
        
    except InsertUserException as e:
        raise InsertUserException(f"error: {str(e)}")

def insert_teacher_to_db(teacher: UserCreate):

    try:
        # Insert user and get the user inserted
        insertedUser = insert_user_to_db(teacher, ProfileEnum.TEACHER)
        
        # Return inserted user
        return insertedUser
        
    except InsertUserException as e:
        raise InsertUserException(f"error: {str(e)}")

def insert_labor_to_db(labor: UserCreate):

    try:
        # Insert user and get the user inserted
        insertedUser = insert_user_to_db(labor, ProfileEnum.LABOR)
        
        # Return inserted user
        return insertedUser
        
    except InsertUserException as e:
        raise InsertUserException(f"error: {str(e)}")

def delete_student_from_db(idAlumn: int):
    # Get the connection and the cursor
    conn, cursor = get_conn_and_cursor()

    sql = f"DELETE FROM user WHERE idUser = {idAlumn}"
    cursor.execute(sql)
    
    # Hacer commit de los cambios y cerrar la conexión
    do_commit(conn,cursor)

    return {"message": f"User with id {idAlumn} has been deleted."}


def get_entries_from_user(idAlumn: int):
    ## Get the idAgreement
    # RUTA: obtener el agreement a partir del profileUser,obtener los entries del agreement
    # Get the connection and the cursor
        conn, cursor = get_conn_and_cursor()

        sql = f"SELECT idAgreement FROM agreement WHERE idAlumn={idAlumn}"

        cursor.execute(sql)
   
        idAgr = cursor.fetchone()[0]

        ## Get the entries
        sql = f"SELECT * FROM entry WHERE idAgreement={idAgr}"

        cursor.execute(sql)
        results = cursor.fetchall()

        rows = []
        columns = [column[0] for column in cursor.description]
        for row in results:
            row_dict = dict(zip(columns, row))
            rows.append(row_dict)

        return rows
  

def get_data_from_user(idAlumn: int):

        # Get the connection and the cursor
        conn, cursor = get_conn_and_cursor()

        sql = f"SELECT * FROM user WHERE idUser={idAlumn}"

        cursor.execute(sql)
        
  

        result = cursor.fetchone()
        row = {}
        if result:
            for i, column in enumerate(cursor.description):
                row[column[0]] = result[i]
        return row



def insert_unit_to_db(unit: UnitCreate):
        #return unit
        # Obtener la conexión y el cursor
        conn, cursor = get_conn_and_cursor()

        # Ejecutar la consulta INSERT
        query = "INSERT INTO unit (level, name, initials, charUnit, unitType) VALUES (%s, %s, %s, %s, %s)"
        values = (unit.level, unit.name, unit.initials, "a", unit.unitType)
        cursor.execute(query, values)

        # Obtener el ID de la nueva unidad
        new_id = cursor.lastrowid

        # Hacer commit de los cambios y cerrar la conexión
        do_commit(conn, cursor)

        # Devolver el ID de la nueva unidad
        return {"message": f"Unit with id {new_id} has been added."}
 

def delete_unit_from_db(idUnit: int):

        # Get the connection and the cursor
        conn, cursor = get_conn_and_cursor()

        sql = f"DELETE FROM unit WHERE idUnit = {idUnit}"
        cursor.execute(sql)
        
        # Hacer commit de los cambios y cerrar la conexión
        do_commit(conn,cursor)

        return {"message": f"Unit with id {idUnit} has been deleted."}

  

def update_unit_from_db(unit: UnitCreate,idUnit: int):

        # Get the connection and the cursor
        conn, cursor = get_conn_and_cursor()

        query, values = get_query_and_values("unit", "idUnit", idUnit, {"level": unit.level,"name": unit.name,"initials": unit.initials,"charUnit": unit.charUnit, "unitType": unit.unitType})

        #sql = f"UPDATE module SET name='{module.name}',initials='{module.initials}',hours={module.hours},idUni={module.idUni} WHERE idMod={id}"
        cursor.execute(query,values)
        
        # Hacer commit de los cambios y cerrar la conexión
        do_commit(conn,cursor)

        return {"message": f"Unit with id {idUnit} has been updated."}



def get_day_from_db(idDay: int):
   
        conn, cursor = get_conn_and_cursor()
        ## Get the entries
        sql = f"SELECT * FROM day WHERE idDay={idDay}"

        cursor.execute(sql)

        result = cursor.fetchone()
        row = {}
        if result:
            for i, column in enumerate(cursor.description):
                row[column[0]] = result[i]
        return row
        
 

def update_day_from_db(day: DayCreate,idDay: int):
        # Get the connection and the cursor
        conn, cursor = get_conn_and_cursor()

        query, values = get_query_and_values("day", "idDay", idDay, {"text": day.text,"hours": day.hours,"observations": day.observations,"idEntry": day.idEntry})

        #sql = f"UPDATE module SET name='{module.name}',initials='{module.initials}',hours={module.hours},idUni={module.idUni} WHERE idMod={id}"
        cursor.execute(query,values)
        
        # Hacer commit de los cambios y cerrar la conexión
        do_commit(conn,cursor)

        return {"message": f"Day with id {idDay} has been updated."}



def get_user_from_db(id: int):

    try:
        # Get the connection and the cursor
        conn, cursor = get_conn_and_cursor()

        query = f"SELECT * FROM user WHERE idUser = {id}"

        cursor.execute(query)

        # Fetch the user from the result set
        result = cursor.fetchone()
        if result is None:
            raise GetUserException(f"User with id {id} not found")

        # Create a User object from the database row
        user = User(
            idUser=result[0],
            name=result[1],
            surname=result[2],
            email=result[3],
            password=result[4],
            picture=result[5],
            linkedin=result[6],
            github=result[7],
            twitter=result[8],
            profile=ProfileEnum(result[9])
        )

        return user

    except Exception as e:
        # Rollback changes and close connections
        rollback(conn, cursor)

        raise Exception(f"Error retrieving user: {str(e)}")


def login_from_db(auth: LoginCreate):
        conn, cursor = get_conn_and_cursor()
        ## Get the entries
        sql = f"SELECT * FROM user WHERE email='{auth.email}' AND password='{auth.password}'"

        cursor.execute(sql)

        result = cursor.fetchone()
        row = {}
        if result:
            for i, column in enumerate(cursor.description):
                row[column[0]] = result[i]
        return row
        



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
            insert_student_to_db(student)
            ####### send_email_generating_password(email)
            successful_inserts.append(f"{student.surname}, {student.name}")
        except Exception as e:
            failed_inserts.append((position, str(e)))
            continue

    if len(failed_inserts) == 0:
        return {'message': 'All users inserted successfully.'}
    else:
        failed_inserts_position = [insert[0] for insert in failed_inserts]
        error_messages = [insert[1] for insert in failed_inserts]
        return {'message': 'Some users were not inserted.', 'successful_inserts': successful_inserts, 'failed_inserts': f'Elements in the position {failed_inserts_position} were not inserted', 'error_messages': error_messages}
    

def get_profile_from_user(id: int):
    
    try:
        # Get the connection and the cursor
        conn, cursor = get_conn_and_cursor()

        sql = f"SELECT profile FROM user WHERE idUser = {id}"

        cursor.execute(sql)
        result = cursor.fetchone()[0]

        close_conn_and_cursor(conn, cursor)
        
        return result
    
    except Exception as e:
        raise GetUserException(f"error: {str(e)}")
    
# Drop the database
def drop_db():
    '''
    
    '''
    try:
        # Get the connection and the cursor
        conn, cursor = get_conn_and_cursor()
        # Execute DROP DATABASE query
        cursor.execute(f"DROP DATABASE {DATABASE}")
        # Close connections
        close_conn_and_cursor(conn, cursor)
        # Success message
        return {"message": f"The {DATABASE} database has been dropped."}
        
    except mysql.connector.Error as e:
        # The specified database does not exist
        if e.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
            return {"error": f"The {DATABASE} database does not exist."}
        # The user does not have access to the specified database
        elif e.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
            return {"error": "Access denied."}
        # Some other error occurred
        else:
            return {"error": "An error occurred while dropping the database."}

# Update user
def update_user_in_db(user_id: int, updated_fields: dict):

    try:
        # Get the connection and the cursor
        conn, cursor = get_conn_and_cursor()

        # Get the query and the values
        query, values = get_query_and_values("user", "idUser", user_id, updated_fields)

        # Execute the query
        cursor.execute(query, values)

        # Commit changes and close connections
        do_commit(conn, cursor)

        user_inserted = get_user_from_db(user_id)

        return user_inserted

    except Exception as e:

        # Rollback changes and close connections
        rollback(conn, cursor)

        return {"error": f"Error updating user: {str(e)}"}