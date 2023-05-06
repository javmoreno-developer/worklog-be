import mysql.connector
from models import *
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import subprocess
import secrets

FILENAME = "worklog.sql"

##Funciones generales
def get_conn_and_cursor():
    conn = mysql.connector.connect(user='root', password='',host='host.docker.internal', database='worklog')
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

def get_query_and_values(table_name: str, id_name: str, id_value, updated_fields):

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

def get_profile_from_user(id: int):
    # Get the connection and the cursor
    conn, cursor = get_conn_and_cursor()

    sql = f"SELECT profile FROM user WHERE idUser={id}"

    cursor.execute(sql)
    
    return cursor.fetchone()[0]

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

        reset_password(user["idUser"],new_password)
        
        return {"message": "Email sended"}
    else:
        return {"message": "The user does not exist"}
    


def import_mysql_database(profileUser: int):

    if(check_permission(profileUser,ProfileEnum.ADMIN) == True):
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
    else:
        return check_permission(profileUser,ProfileEnum.ADMIN)


def get_new_password():
    return secrets.token_hex(4)

def reset_password(id: int,new_password: str):
        # Get the connection and the cursor
        conn, cursor = get_conn_and_cursor()

        query, values = get_query_and_values("user", "idUser", id, {"password": new_password})

        cursor.execute(query,values)
        
        # Hacer commit de los cambios y cerrar la conexión
        do_commit(conn,cursor)


def check_user_by_email(email: str):
    conn, cursor = get_conn_and_cursor()
    ## Get the entries
    sql = f"SELECT * FROM user WHERE email='{email}'"

    cursor.execute(sql)

    result = cursor.fetchone()
    row = {}
    if result:
        for i, column in enumerate(cursor.description):
            row[column[0]] = result[i]
    return row