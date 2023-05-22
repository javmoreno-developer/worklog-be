import mysql.connector
import xml.etree.ElementTree as ET
from mysql.connector.errors import IntegrityError
from fastapi.exceptions import HTTPException
from exceptions import *
from models import *
from utils import *

########## COMPANY ##########

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

    # Get the connection and the cursor
    conn, cursor = get_conn_and_cursor()
    query = f"DELETE FROM {T_COMPANY} WHERE {ID_NAME_COMPANY} = {id_company}"
    cursor.execute(query)

    # Hacer commit de los cambios y cerrar la conexión
    do_commit(conn, cursor)

    return {"message": f"Company with id {id_company} has been deleted."}

# Insert module
def insert_module_to_db(module: ModuleCreate, profileUser: int):
    # Get the connection and the cursor
    conn, cursor = get_conn_and_cursor()

    # Ejecutar la consulta INSERT
    query = f"INSERT INTO {T_MODULE} (name, initials, hours, idUnit) VALUES (%s, %s, %s, %s)"
    values = (module.name, module.initials, int(
        module.hours), int(module.idUnit))
    cursor.execute(query, values)

    # Obtener el ID del nuevo módulo
    new_id = cursor.lastrowid

    # Hacer commit de los cambios y cerrar la conexión
    do_commit(conn, cursor)

    # Devolver el ID del nuevo módulo
    return {"message": f"Module with id {new_id} has been added."}

# Delete module
def delete_module_from_db(id_module: int):
    # Get the connection and the cursor
    conn, cursor = get_conn_and_cursor()

    query = f"DELETE FROM {T_MODULE} WHERE {ID_NAME_MODULE} = {id_module}"
    cursor.execute(query)

    # Hacer commit de los cambios y cerrar la conexión
    do_commit(conn, cursor)

    return {"message": f"Module with id {id_module} has been deleted."}

########## USER ##########

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
def insert_user_to_db(user: UserCreate, profile: ProfileEnum):

    try:
        # Check if email, name, and surname fields are not empty
        if not user.email or not user.name or not user.surname:
            raise InsertUserException(
                "error adding user, required fields are missing")

        # Get the connection and the cursor
        conn, cursor = get_conn_and_cursor()

        # Query to check email
        check_email_query = f"SELECT email FROM {T_USER} WHERE email = '{user.email}'"
        cursor.execute(check_email_query)
        result = cursor.fetchone()

        if result:
            # Email exists
            return {"error": "Error adding user, email already registered"}

        # Query
        query = f"INSERT INTO {T_USER} (name, surname, email, password, picture, linkedin, github, twitter, profile) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"

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

        return {"message": "User inserted successfully", "result": inserted_user}

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
            insert_user_to_db(student, ProfileEnum.STUDENT)
            # send_email_generating_password(email)
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

# Delete user
def delete_user_from_db(id_user: int):
    # Get the connection and the cursor
    conn, cursor = get_conn_and_cursor()
    # Set and execute the query
    query = f"DELETE FROM {T_USER} WHERE {ID_NAME_USER} = {id_user}"
    cursor.execute(query)
    # Do commit and close connections
    do_commit(conn, cursor)
    return {"message": f"User with id {id_user} has been deleted."}

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

########## UNIT ##########

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
    # Get the connection and the cursor
    conn, cursor = get_conn_and_cursor()

    query = f"DELETE FROM {T_UNIT} WHERE {ID_NAME_UNIT} = {id_unit}"
    cursor.execute(query)

    # Hacer commit de los cambios y cerrar la conexión
    do_commit(conn, cursor)

    return {"message": f"Unit with id {id_unit} has been deleted."}

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

# Get user #### TENEMOS YA UN GET GENERAL, VER SI ESTE HACE ALGUNA DIFERENCIA
def get_user_from_db(id_user: int):

    try:
        # Get the connection and the cursor
        conn, cursor = get_conn_and_cursor()

        query = f"SELECT * FROM {T_USER} WHERE {ID_NAME_USER} = {id_user}"

        cursor.execute(query)

        # Fetch the user from the result set
        result = cursor.fetchone()
        if result is None:
            raise GetUserException(f"User with id {id_user} not found")

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

def get_object_from_db(table_name: str, id_name: int, id_value: int):

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

        close_conn_and_cursor(conn, cursor)

        # Format the object with column names
        formatted_object = None
        if object != None:
            formatted_object = { column_names[i]: value for i, value in enumerate(object) }
            if formatted_object != None:
                return formatted_object
            else:
                return {"error": "Object has not been built correctly"}
        else:
            return {"error:": "Object does not exists"}
            

    except Exception as e:
        # Rollback changes and close connections
        rollback(conn, cursor)
        raise Exception(f"Error retrieving the object: {str(e)}")

########## General UPDATE for all tables  ##########

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

        # Get the update query and the values
        query, values = get_update_query_and_values(table_name, id_name, id_value, updated_fields)

        # Execute the query
        cursor.execute(query, values)

        # Commit changes
        do_commit(conn, cursor)

        # Get the updated object
        formatted_updated_obj = get_object_from_db(table_name, id_name, id_value)

        return {"message": f"{table_name.capitalize()} updated successfully", "result": formatted_updated_obj}

    except Exception as e:
        # Rollback changes and close connections
        rollback(conn, cursor)
        return {"error": f"Error updating the object: {str(e)}"}

########## General DELETE for all tables  ##########

# HAY QUE CONTROLAR MENSAJE AL BORRAR REGISTROS QUE DEPENDAN DE OTROS Y DE ERROR AL INTENTAR BORRAR
# Y CAMBIAR EL MENSAJE SI NO BORRA UN OBJETO PORQUE NO LO ENCUENTRA
def delete_object_from_db(table_name: str, id_name: str, id_value: int):

    try:
        # Get the connection and the cursor
        conn, cursor = get_conn_and_cursor()

        # Get the object that is going to be deleted
        formatted_deleted_obj = get_object_from_db(table_name, id_name, id_value)

        # Delete object
        delete_query = f"DELETE FROM {table_name} WHERE {id_name} = {id_value}"
        cursor.execute(delete_query)
        do_commit(conn, cursor)

        # Success message with deleted object
        return {"message": f"{table_name.capitalize()} with id {id_value} has been deleted.", "result": formatted_deleted_obj}

    except Exception as e:

        # Rollback changes and close connections
        rollback(conn, cursor)

        # Failure message
        return {"error": str(e)}

########## AGREEMENT ##########

def insert_agreement_to_db(agreement: AgreementCreate):
    
    conn, cursor = get_conn_and_cursor()
