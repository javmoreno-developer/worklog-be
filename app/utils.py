import mysql.connector
from models import *
from constants import *
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fastapi.responses import FileResponse
from exceptions import GetUserException
import secrets
import smtplib
import subprocess

## Funciones generales

def get_conn_and_cursor():
    conn = mysql.connector.connect(user=USER, password=PASSWORD,host=HOST, database=DATABASE)
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

    # Append to the query values that are not none, excluding ID
    for key, value in updated_fields.items():
        if value is not None and key != id_name:
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
        return {"message": "The user does not exist"}
    


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

### HAY QUE MIRARLO
def generate_backup_of_db():
        
    # Set the backup file name
    filename = f"{DATABASE}.sql"    
    # Build the command to generate the backup
    command = f"mysqldump -u {USER} -p{PASSWORD} {DATABASE} > {filename}"
    # Execute the command using subprocess
    try:
        subprocess.run(command, shell=True, check=True)
        # Return the backup file
        return FileResponse(filename, media_type="application/octet-stream", filename=filename)
    except subprocess.CalledProcessError:
        raise subprocess.CalledProcessError({"error": "Failed to generate backup."})


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

## XML

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
    email = email_elem.text
    # Optional fields
    password = student.find('password').text if student.find('password') is not None and student.find('password').text is not None else ""
    picture = student.find('picture').text if student.find('picture') is not None and student.find('picture').text is not None else ""
    linkedin = student.find('linkedin').text if student.find('linkedin') is not None and student.find('linkedin').text is not None else ""
    github = student.find('github').text if student.find('github') is not None and student.find('github').text is not None else ""
    twitter = student.find('twitter').text if student.find('twitter') is not None and student.find('twitter').text is not None else ""
    # Set STUDENT PROFILE
    profile = ProfileEnum.STUDENT

    return UserCreate(name=name, surname=surname, email=email, password=password, picture=picture, linkedin=linkedin, github=github, twitter=twitter, profile=profile)


def is_student_under_labor_tutor(id_laboral_tutor: int, id_student: int):

    # CAMINO PARA LLEGAR A SI ES TUTOR O NO DE ESE ALUMNO. 
    # TENEMOS UNA TABLA AGREEMENT, CON EL ID DEL LABORAL Y EL ID DEL ESTUDIANTE. 
    # SI HAY OCURRENCIAS, ES SU ALUMNO.
    # LA COSA ES, QUE ESE ALUMNO PUEDE QUE HAYA ESTADO DOS VECES EN UN CONVENIO CON ESE MISMO LABORAL,
    # ASÍ QUE HAY QUE COMPROBAR ALGO MÁS

    conn, cursor = get_conn_and_cursor()

    # Try to get the agreement by the id of the laboral tutor and the id of the student
    query = f"SELECT * FROM {T_AGREEMENT} WHERE {ID_NAME_LABOR} = {id_laboral_tutor} AND {ID_NAME_STUDENT} = {id_student}"
    cursor.execute(query)
    result = cursor.fetchone()
    close_conn_and_cursor(conn, cursor)

    # If there is a result, this laboral tutor is the tutor of this student, else, he/she is not
    if result:
        return True
    else:
        return False
    
def is_student_under_teacher_tutor(id_teacher_tutor: int, id_student: int):

    # CAMINO PARA LLEGAR A SI ES TUTOR O NO DE ESE ALUMNO. 
    # TENEMOS UNA TABLA AGREEMENT, CON EL ID DEL DOCENTE Y EL ID DEL ESTUDIANTE. 
    # SI HAY OCURRENCIAS, ES SU ALUMNO.
    # LA COSA ES, QUE ESE ALUMNO PUEDE QUE HAYA ESTADO DOS VECES EN UN CONVENIO CON ESE MISMO PROFESOR,
    # ASÍ QUE HAY QUE COMPROBAR ALGO MÁS

    conn, cursor = get_conn_and_cursor()

    # Try to get the agreement by the id of the teacher and the id of the student
    query = f"SELECT * FROM {T_AGREEMENT} WHERE {ID_NAME_TEACHER} = {id_teacher_tutor} AND {ID_NAME_STUDENT} = {id_student}"
    cursor.execute(query)
    result = cursor.fetcone()
    close_conn_and_cursor(conn, cursor)

    # If there is a result, this teacher tutor is the tutor of this student, else, he/she is not
    if result:
        return True
    else:
        return False

def is_student_company(id_student: int, id_company: int):
    
    # Get the connection
    conn, cursor = get_conn_and_cursor()

    # Try to get the agreement by the id of the student and the id of the company
    query = f"SELECT * FROM {T_AGREEMENT} WHERE {ID_NAME_STUDENT} = {id_student} AND {ID_NAME_COMPANY} = {id_company}"
    cursor.execute(query)
    result = cursor.fetchone()
    close_conn_and_cursor(conn, cursor)

    # If there is a result, this company is where the student is at, else, this is not
    if result:
        return True
    else:
        return False