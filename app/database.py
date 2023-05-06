import mysql.connector
from models import *
from utils import *


class ProfileEnum(str, Enum):
    ADMIN = '1'
    STUDENT = '2'
    TEACHER = '3'
    LABOR = '4'


def insert_company_to_db(company: CompanyCreate,profileUser: int):

    if(check_permission(profileUser,ProfileEnum.TEACHER) == True):
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
    else:
        return check_permission(profileUser,ProfileEnum.TEACHER)



def delete_company_from_db(idCompany: int,profileUser: int):

    if(check_permission(profileUser,ProfileEnum.TEACHER) == True):
        # Get the connection and the cursor
        conn, cursor = get_conn_and_cursor()
        sql = f"DELETE FROM company WHERE idCompany = {idCompany}"
        cursor.execute(sql)
    
        # Hacer commit de los cambios y cerrar la conexión
        do_commit(conn,cursor)

        return {"message": f"Company with id {idCompany} has been deleted."}
    else:
        return check_permission(profileUser,ProfileEnum.TEACHER)


def update_company_from_db(company:CompanyCreate,idCompany:int,profileUser: int):
    if(check_permission(profileUser,ProfileEnum.TEACHER) == True):
        # Get the connection and the cursor
        conn, cursor = get_conn_and_cursor()

        query, values = get_query_and_values("company", "idCompany", idCompany, {"name": company.name,"direction": company.direction,"latitude": company.latitude,"longitude": company.longitude,"phone": company.phone})

        #sql = f"UPDATE company SET name='{company.name}',direction='{company.direction}',latitude={company.latitude},longitude={company.latitude},phone='{company.phone}' WHERE idComp={id}"
        cursor.execute(query,values)
        
        # Hacer commit de los cambios y cerrar la conexión
        do_commit(conn,cursor)

        return {"message": f"Company with id {idCompany} has been updated."}
    else:
        return check_permission(profileUser,ProfileEnum.TEACHER)


def insert_module_to_db(module: ModuleCreate,profileUser: int):
    if(check_permission(profileUser,ProfileEnum.ADMIN) == True):
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
    else:
        return check_permission(profileUser,ProfileEnum.ADMIN)


def delete_module_from_db(idModule: int,profileUser: int):
    if(check_permission(profileUser,ProfileEnum.ADMIN) == True):
        # Get the connection and the cursor
        conn, cursor = get_conn_and_cursor()

        sql = f"DELETE FROM module WHERE idModule = {idModule}"
        cursor.execute(sql)
        
        # Hacer commit de los cambios y cerrar la conexión
        do_commit(conn,cursor)

        return {"message": f"Module with id {idModule} has been deleted."}
    else:
        return check_permission(profileUser,ProfileEnum.ADMIN)

    
def update_module_from_db(module:ModuleCreate,idModule: int,profileUser: int):
    if(check_permission(profileUser,ProfileEnum.ADMIN) == True):
        # Get the connection and the cursor
        conn, cursor = get_conn_and_cursor()

        query, values = get_query_and_values("module", "idModule", idModule, {"name": module.name,"initials": module.initials,"hours": module.hours,"idUnit": module.idUnit})

        #sql = f"UPDATE module SET name='{module.name}',initials='{module.initials}',hours={module.hours},idUni={module.idUni} WHERE idMod={id}"
        cursor.execute(query,values)
        
        # Hacer commit de los cambios y cerrar la conexión
        do_commit(conn,cursor)

        return {"message": f"Module with id {idModule} has been updated."}
    else:
        return check_permission(profileUser,ProfileEnum.ADMIN)


def insert_alumn_to_db(alumn: UserCreate,profileUser: int):
    if(check_permission(profileUser,ProfileEnum.TEACHER) == True):
        # Get the connection and the cursor
        conn, cursor = get_conn_and_cursor()

        # Ejecutar la consulta INSERT
        try:
            query = "INSERT INTO user (name, surname, email, password, picture, linkedin, github, twitter, profile) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            values = (alumn.name, alumn.surname, alumn.email, alumn.password, alumn.picture, alumn.linkedin, alumn.github, alumn.twitter, 2)
            cursor.execute(query, values)
        
            # Obtener el ID del nuevo módulo
            new_id = cursor.lastrowid

            # Hacer commit de los cambios y cerrar la conexión
            do_commit(conn,cursor)

        except mysql.connector.errors.IntegrityError as error:
            return {"message": "Email column already exist"}

        # Devolver el ID del nuevo módulo
        return {"message": f"User with id {new_id} has been added."}
    else:
        return check_permission(profileUser,ProfileEnum.TEACHER)



def delete_alumn_from_db(idAlumn: int,profileUser: int):
   if(check_permission(profileUser,ProfileEnum.TEACHER) == True):
    # Get the connection and the cursor
    conn, cursor = get_conn_and_cursor()

    sql = f"DELETE FROM user WHERE idUser = {idAlumn}"
    cursor.execute(sql)
    
    # Hacer commit de los cambios y cerrar la conexión
    do_commit(conn,cursor)

    return {"message": f"User with id {idAlumn} has been deleted."}
   else:
    return check_permission(profileUser,ProfileEnum.TEACHER)


def get_entries_from_user(idAlumn: int,profileUser: int):
    ## Get the idAgreement
    # RUTA: obtener el agreement a partir del profileUser,obtener los entries del agreement
    # Get the connection and the cursor
    if(check_permission(profileUser,ProfileEnum.TEACHER) == True):
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
    else:
        return check_permission(profileUser,ProfileEnum.TEACHER)    

def get_data_from_user(idAlumn: int,profileUser: int):
    if(check_permission(profileUser,ProfileEnum.TEACHER) == True):
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
    else:
        return check_permission(profileUser,ProfileEnum.TEACHER)  


def insert_unit_to_db(unit: UnitCreate,profileUser: int):
    if(check_permission(profileUser,ProfileEnum.TEACHER) == True):
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
    else:
        return check_permission(profileUser,ProfileEnum.ADMIN)

def delete_unit_from_db(idUnit: int,profileUser: int):
    if(check_permission(profileUser,ProfileEnum.ADMIN) == True):
        # Get the connection and the cursor
        conn, cursor = get_conn_and_cursor()

        sql = f"DELETE FROM unit WHERE idUnit = {idUnit}"
        cursor.execute(sql)
        
        # Hacer commit de los cambios y cerrar la conexión
        do_commit(conn,cursor)

        return {"message": f"Unit with id {idUnit} has been deleted."}
    else:
        return check_permission(profileUser,ProfileEnum.ADMIN)
  

def update_unit_from_db(unit: UnitCreate,idUnit: int,profileUser: int):
    if(check_permission(profileUser,ProfileEnum.ADMIN) == True):
        # Get the connection and the cursor
        conn, cursor = get_conn_and_cursor()

        query, values = get_query_and_values("unit", "idUnit", idUnit, {"level": unit.level,"name": unit.name,"initials": unit.initials,"charUnit": unit.charUnit, "unitType": unit.unitType})

        #sql = f"UPDATE module SET name='{module.name}',initials='{module.initials}',hours={module.hours},idUni={module.idUni} WHERE idMod={id}"
        cursor.execute(query,values)
        
        # Hacer commit de los cambios y cerrar la conexión
        do_commit(conn,cursor)

        return {"message": f"Unit with id {idUnit} has been updated."}
    else:
        return check_permission(profileUser,ProfileEnum.ADMIN)


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

def update_day_from_db(day: DayCreate,idDay: int,profileUser: int):
    if((check_permission(profileUser,ProfileEnum.STUDENT) == True) or (check_permission(profileUser,ProfileEnum.TEACHER) == True)):
        # Get the connection and the cursor
        conn, cursor = get_conn_and_cursor()

        query, values = get_query_and_values("day", "idDay", idDay, {"text": day.text,"hours": day.hours,"observations": day.observations,"idEntry": day.idEntry})

        #sql = f"UPDATE module SET name='{module.name}',initials='{module.initials}',hours={module.hours},idUni={module.idUni} WHERE idMod={id}"
        cursor.execute(query,values)
        
        # Hacer commit de los cambios y cerrar la conexión
        do_commit(conn,cursor)

        return {"message": f"Day with id {idDay} has been updated."}
    else:
        return check_permission(profileUser,ProfileEnum.STUDENT)


def get_user_from_db(idUser: int,profileUser: int):
    if((check_permission(profileUser,ProfileEnum.STUDENT) == True) or (check_permission(profileUser,ProfileEnum.TEACHER) == True)):
        conn, cursor = get_conn_and_cursor()
        ## Get the entries
        sql = f"SELECT * FROM user WHERE idUser={idUser}"

        cursor.execute(sql)

        result = cursor.fetchone()
        row = {}
        if result:
            for i, column in enumerate(cursor.description):
                row[column[0]] = result[i]
        return row
        
    else: 
        return check_permission(profileUser,ProfileEnum.STUDENT)


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
