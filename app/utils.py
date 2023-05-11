import mysql.connector
from models import *
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fastapi.responses import FileResponse
from exceptions import GetUserException
import secrets
import subprocess

FILENAME = "worklog.sql"
USER = "root"
PASSWORD = ""
HOST = "host.docker.internal"
DATABASE = "worklog"

##Funciones generales

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

def get_query_and_values(table_name: str, exclude_list: dict, id_value, updated_fields):

    # Start building the query
    query = f"UPDATE {table_name} SET"
    values = []

    # Append to the query values that are not none, excluding ID
    for key, value in updated_fields.items():
        if value is not None and key not in exclude_list:
            query += f" {key} = %s,"
            values.append(value)

    # Remove the last comma and add the WHERE clause
    query = query.rstrip(",") + f" WHERE {exclude_list[-1]} = %s"
    values.append(id_value)

    return query, values

def check_permission(profile: int, level: int):
    #profile = get_profile_from_user(id)
    if(str(profile) == level or str(profile)=="1"):
        return True
    else:
        return "You can't do this opperation"


def send_email(emailReceiver: str):
    # Vemos si el correo existe como usuario
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
    sql = file.read()

    cnx = mysql.connector.connect(
        host="host.docker.internal",
        user="root",
        password="",
        database="mydatabase"
    )
    cursor = cnx.cursor()

    for result in cursor.execute(sql, multi=True):
        if result.with_rows:
            print("Rows produced by statement '{}':".format(
            result.statement))
            print(result.fetchall())
        else:
            print("Number of rows affected by statement '{}': {}".format(
            result.statement, result.rowcount))

    cnx.close()
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

def reset_password(id: int, new_password: str):
        # Get the connection and the cursor
        conn, cursor = get_conn_and_cursor()

        query, values = get_query_and_values("user", "idUser", id, {"password": new_password})

        cursor.execute(query, values)
        
        # Hacer commit de los cambios y cerrar la conexión
        do_commit(conn, cursor)


def check_user_by_email(email: str):
    conn, cursor = get_conn_and_cursor()
    ## Get the entries
    query = f"SELECT * FROM user WHERE email='{email}'"

    cursor.execute(query)

    result = cursor.fetchone()
    row = {}
    if result:
        for i, column in enumerate(cursor.description):
            row[column[0]] = result[i]
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