import mysql.connector
from mysql.connector.errors import IntegrityError
from fastapi.exceptions import HTTPException
import xml.etree.ElementTree as ET
from typing import Type, TypeVar
from exceptions import *
from models import *
from utils import *

class ProfileEnum(str, Enum):
    ADMIN = '1'
    STUDENT = '2'
    TEACHER = '3'
    LABOR = '4'


def insert_company_to_db(company: CompanyCreate, profileUser: int):

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


def insert_module_to_db(module: ModuleCreate,profileUser: int):
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

def get_entries_from_user(idAlumn: int,profileUser: int):
    ## Get the idAgreement
    # RUTA: obtener el agreement a partir del profileUser,obtener los entries del agreement
    # Get the connection and the cursor
    if(check_permission(profileUser,ProfileEnum.TEACHER) == True):
        conn, cursor = get_conn_and_cursor()

        query = f"SELECT idAgreement FROM agreement WHERE idAlumn={idAlumn}"

        cursor.execute(query)
   
        idAgr = cursor.fetchone()[0]

        ## Get the entries
        query = f"SELECT * FROM entry WHERE idAgreement={idAgr}"

        cursor.execute(query)
        results = cursor.fetchall()

        rows = []
        columns = [column[0] for column in cursor.description]
        for row in results:
            row_dict = dict(zip(columns, row))
            rows.append(row_dict)

        return rows
    else:
        return check_permission(profileUser,ProfileEnum.TEACHER)    

def get_data_from_user(id_user: int):
    # Get the connection and the cursor
    conn, cursor = get_conn_and_cursor()

    query = f"SELECT * FROM user WHERE idUser={id_user}"

    cursor.execute(query)
    result = cursor.fetchone()
    row = {}
    if result:
        for i, column in enumerate(cursor.description):
            row[column[0]] = result[i]
    return row


def insert_unit_to_db(unit: UnitCreate):
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

def get_day_from_db(idDay: int,profileUser: int):
    if((check_permission(profileUser,ProfileEnum.STUDENT) == True) or (check_permission(profileUser,ProfileEnum.TEACHER) == True)):
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
        
    else: 
        return check_permission(profileUser,ProfileEnum.STUDENT)

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


def login_from_db(auth: LoginCreate,profileUser: int):
    if((check_permission(profileUser,ProfileEnum.STUDENT) == True) or (check_permission(profileUser,ProfileEnum.TEACHER) == True)):
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
        
    else: 
        return check_permission(profileUser,ProfileEnum.STUDENT)


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


# HAY QUE CONTROLAR MENSAJE AL BORRAR REGISTROS QUE DEPENDAN DE OTROS Y DE ERROR AL INTENTAR BORRAR Y CAMBIAR EL MENSAJE SI NO BORRA UN OBJETO PORQUE NO LO ENCUENTRA
def delete_row_db(table_name: str, id_name: str, id_value: int):

    try:
        # Get the connection and the cursor
        conn, cursor = get_conn_and_cursor()

        # Get the table's column names
        select_columns_query = f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}'"
        cursor.execute(select_columns_query)
        column_names = [col[0] for col in cursor.fetchall()]

        # Query to get the object that is going to be deleted
        select_object_query = f"SELECT * FROM {table_name} WHERE {id_name} = {id_value}"

        # Execute query to retrieve the deleted object
        cursor.execute(select_object_query)
        deleted_object = cursor.fetchone()

        # Query to delete the object
        delete_query = f"DELETE FROM {table_name} WHERE {id_name} = {id_value}"

        # Execute query
        cursor.execute(delete_query)

        if cursor.rowcount == 0:
            raise


        # Commit changes and close connections
        do_commit(conn, cursor)

        # Format the deleted object with column names
        formatted_deleted_obj = None
        if deleted_object:
            formatted_deleted_obj = {column_names[i]: value for i, value in enumerate(deleted_object)}

        # Success message with deleted object
        return {"message": f"{table_name.capitalize()} with id {id_value} has been deleted.", "result": formatted_deleted_obj}

    except Exception as e:

        # Rollback changes and close connections
        rollback(conn, cursor)

        # Failure message
        raise Exception(f"Error deleting {table_name}: {str(e)}")

# Update table in database
def update_table_db(table_name: str, id_name: str, id_value: int, updated_fields: dict):

    try:
        # Get the connection and the cursor
        conn, cursor = get_conn_and_cursor()

        # Check if the object exists
        select_query = f"SELECT * FROM {table_name} WHERE {id_name} = {id_value}"
        cursor.execute(select_query)
        row = cursor.fetchone()
        if not row:
            raise ValueError("Object not found")

        # Get the query and the values
        query, values = get_query_and_values(table_name, id_name, id_value, updated_fields)

        # Execute the query
        cursor.execute(query, values)

        # Commit changes
        conn.commit()

        # Get the table's column names
        select_columns_query = f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}'"
        cursor.execute(select_columns_query)
        column_names = [col[0] for col in cursor.fetchall()]

        # Query to get the object that has been updated
        select_object_query = f"SELECT * FROM {table_name} WHERE {id_name} = {id_value}"

        # Execute query to retrieve the updated object
        cursor.execute(select_object_query)
        updated_object = cursor.fetchone()

        # Format the updated object with column names
        formatted_updated_obj = None
        if updated_object:
            formatted_updated_obj = {column_names[i]: value for i, value in enumerate(updated_object)}

        # Close connection and cursor
        close_conn_and_cursor(conn, cursor)

        return {"message": f"{table_name.capitalize()} updated successfully", "result": formatted_updated_obj}

    except Exception as e:

        # Rollback changes and close connections
        rollback(conn, cursor)

        return {"error": f"Error updating the object: {str(e)}"}

def get_object_from_db(table: str, id_name: int, id_value: int, cls: Type) -> object:

    try:
        # Get the connection and the cursor
        conn, cursor = get_conn_and_cursor()

        query = f"SELECT * FROM {table} WHERE {id_name} = {id_value}"
        cursor.execute(query)

        row = cursor.fetchone()
        if not row:
            raise ValueError(f"{cls.__name__} with {id_name}={id_value} not found")
        
        # Create a dictionary of attribute names and values
        # based on the cursor description
        attrs = dict(zip((d[0] for d in cursor.description), row))
        print(f"XXX ATR {attrs}")
        print(f"CLS attrs: {dir(cls)}")


        # Remove any attribute that does not exist in the class
        print(f"XXX CLASS {dir(cls)}")
        attrs = {k: v for k, v in attrs.items() if hasattr(cls, k)}
        print(f"XXX ATR REM {attrs}")

        # Create an instance of the class and set its attributes
        obj = cls(**attrs)

        return obj

    except Exception as e:
        # Rollback changes and close connections
        rollback(conn, cursor)

        raise Exception(f"Error retrieving {cls.__name__}: {str(e)}")
