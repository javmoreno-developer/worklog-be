import mysql.connector
from models import *
from constants import *
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fastapi.exceptions import HTTPException
from mysql.connector.errors import Error
from datetime import datetime
import secrets
import smtplib
import os

# Funciones generales

def get_conn_and_cursor():
    conn = mysql.connector.connect(user=USER, password=PASSWORD, host=HOST, database=DATABASE)
    cursor = conn.cursor()
    return conn, cursor

def close_conn_and_cursor(conn, cursor):
    cursor.close()
    conn.close()

def do_commit(conn, cursor):
    conn.commit()
    close_conn_and_cursor(conn, cursor)

def rollback(conn, cursor):
    conn.rollback()
    close_conn_and_cursor(conn, cursor)

def get_update_query_and_values(table_name: str, id_name: str, id_value, updated_fields):

    # Start building the query
    query = f"UPDATE {table_name} SET"
    values = []

    # Append to the query values that are not none, excluding id_name, profile, and isActive
    updated_fields.pop(id_name, None)
    updated_fields.pop("profile", None)
    updated_fields.pop("isActive", None)

    for key, value in updated_fields.items():
        if value is not None:
            if key == "hours":
                query += f" {key} = SEC_TO_TIME(%s),"
            else:
                query += f" {key} = %s,"
            values.append(value)

    # Remove the last comma and add the WHERE clause
    query = query.rstrip(",") + f" WHERE {id_name} = %s"
    values.append(id_value)

    return query, values

def send_email(emailReceiver: str):
    # Check if the email exists in the database
    exist = False
    user = check_user_by_email(emailReceiver)

    if(len(user) != 0 ):
        exist = True

    # Configura los detalles del correo electrónico
    if(exist):
        sender_email = "javmoreno766@gmail.com"
        sender_password = "fluyetbuhqxpicsv"
        receiver_email = emailReceiver
        subject = "Recuperar contraseña"
        new_password = get_new_password()
        body = "Nueva contraseña: {}". format(new_password)

        # Configura el mensaje del correo electrónico
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        # Configura el servidor SMTP y envía el correo electrónico
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        text = message.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()

        reset_password(user["idUser"], new_password)
        
        return {"message": "Email sent"}
    else:
        raise HTTPException(status_code=404, detail="The user does not exist")
    
def import_mysql_database():
        
    # Conectar a la base de datos
    file = open(FILENAME)
    query = file.read()

    conn, cursor = get_conn_and_cursor()

    for result in cursor.execute(query, multi=True):
        if result.with_rows:
            print("Rows produced by statement '{}':".format(
            result.statement))
            print(result.fetchall())
        else:
            print("Number of rows affected by statement '{}': {}".format(result.statement, result.rowcount))

    close_conn_and_cursor(conn, cursor)

    return {"message": "database imported"}

def generate_backup_of_db():
    archivo_path = f"./{DATABASE}.sql"  # Ruta al archivo que deseas enviar
    if os.path.isfile(archivo_path):
        with open(archivo_path, 'r') as archivo:
            contenido = archivo.read()
        return contenido
    else:
        return {"message": "El archivo no existe o la ruta es incorrecta"}

def get_new_password():
    return secrets.token_hex(4)

def reset_password(id_user: int, new_password: str):
    # Get the connection and the cursor
    conn, cursor = get_conn_and_cursor()
    # Get the update query
    query, values = get_update_query_and_values(T_USER, ID_NAME_USER, id_user, {"password": new_password})
    # Execute the update query
    cursor.execute(query, values)
    # Do commit and close connections
    do_commit(conn, cursor)

def check_user_by_email(email: str):
    conn, cursor = get_conn_and_cursor()
    query = f"SELECT * FROM {T_USER} WHERE email = '{email}'"
    cursor.execute(query)
    result = cursor.fetchone()
    row = {}
    if result:
        for i, column in enumerate(cursor.description):
            row[column[0]] = result[i]
    close_conn_and_cursor(conn, cursor)
    return row

# XML
def extract_student_data_from_xml(student: str, position: int):
    # Check that the child is a student tag
    if student.tag.lower() != 'student':
        raise ValueError(f"Incorrect tag name: TAG '{student.tag}' should be named 'student' in [{position}]")

    # Mandatory fields
    # Check that `name` exists, and if not, add an error and continue the flow
    name_elem = student.find('name')
    if name_elem is None or name_elem.text is None:
        raise ValueError(f"Mandatory field 'name' is missing in [{position}]")
    name = name_elem.text
    # Check that `surname` exists, and if not, add an error and continue the flow
    surname_elem = student.find('surname')
    if surname_elem is None or surname_elem.text is None:
        raise ValueError(f"Mandatory field 'surname' is missing in [{position}]")
    surname = surname_elem.text
    # Check that `email` exists, and if not, add an error and continue the flow
    email_elem = student.find('email')
    if email_elem is None or email_elem.text is None:
        raise ValueError(f"Mandatory field 'email' is missing in [{position}]")
    result = check_user_by_email(email_elem.text)
    if result:
        raise ValueError(f"User with the email '{email_elem.text}' already exists in [{position}]")
    email = email_elem.text
    # Optional fields
    password = student.find('password').text if student.find('password') is not None and student.find('password').text is not None else ""
    picture = student.find('picture').text if student.find('picture') is not None and student.find('picture').text is not None else ""
    linkedin = student.find('linkedin').text if student.find('linkedin') is not None and student.find('linkedin').text is not None else ""
    github = student.find('github').text if student.find('github') is not None and student.find('github').text is not None else ""
    twitter = student.find('twitter').text if student.find('twitter') is not None and student.find('twitter').text is not None else ""
    # Set STUDENT PROFILE
    profile = ProfileEnum.STUDENT

    return UserCreate(name=name, surname=surname, email=email, password=password, picture=picture, linkedin=linkedin, github=github, twitter=twitter, profile=profile, isActive=StatusEnum.DISABLED)

# Is this list of dates valid
def is_date_format_valid(date_list, date_format):
    for date_str in date_list:
        try:
            datetime.strptime(date_str, date_format)
        except ValueError:
            return False
    return True

# Is date of fct + dual agreement valid
def is_fct_dual_dates_valid(fct_start, fct_end, dual_start, dual_end):

    if fct_start > fct_end:
        raise  HTTPException(status_code=400, detail="FCT start date must be before FCT end date")

    # Check if dual_start_at is lower than dual_end_at
    if dual_start > dual_end:
        raise  HTTPException(status_code=400, detail="Dual start date must be before Dual end date")

    # Check if dual_end_at is lower than fct_start_at
    if dual_end > fct_start:
        raise  HTTPException(status_code=400, detail="Dual end date must be before FCT start date")
    
    return True

# Get the year from two dates: Input 2022-09-15, 2023-06-20. Output: 2022-2023
def get_year_from_dates(start_date: str, end_date: str):
    start_year = datetime.strptime(start_date, '%Y-%m-%d').year
    end_year = datetime.strptime(end_date, '%Y-%m-%d').year
    return f"{start_year}-{end_year}"

# Is a date between two dates
def is_date_between_two_dates(start_date, end_date, date):
    if start_date <= date <= end_date:
        return True
    else:
        return False

