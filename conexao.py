import uuid
import mysql.connector
from mysql.connector import Error
from model import Usuario

def criar_conexao():
    return mysql.connector.connect(
        host="31.220.105.141",
        user="spboxcom_alxac",
        password="spboxcom_bd123",
        database="spboxcom_bd")


def fechar_conexao(con):
    return con.close()

def retornaCon():
    return mysql.connector.connect(
        host="31.220.105.141",
        user="spboxcom_alxac",
        password="spboxcom_bd123",
        database="spboxcom_bd")

# Função inserir
def inserirTb(usuario):
    con = criar_conexao()
    cursor = con.cursor()
    sql = "INSERT INTO User (Name, Email, Id) VALUES(%s, %s, %s);"
    usuario.id = str(uuid.uuid1())
    valores = (usuario.name, usuario.email, usuario.id)
    print(valores)
    cursor.execute(sql, valores)
    cursor.close()
    con.commit()
    fechar_conexao(con)

def getTodos():
    con = criar_conexao()
    cursor = con.cursor()
    sql = "SELECT Id, Name, Email FROM spboxcom_bd.User;"
    cursor.execute(sql)
    u = []
    for(id, name, email) in cursor:
        u.append({"id": str(id), "name": name, "email": email})

    cursor.close()
    return u

def getPorID(id):
    con = criar_conexao()
    cursor = con.cursor()
    sql = "SELECT Id, Name, Email FROM spboxcom_bd.User where id in ('"+ id + "');"
    cursor.execute(sql)
    u = []
    for(id, name, email) in cursor:
        u.append([{"id": str(id), "name": name, "email": email}])

    cursor.close()
    return u

def getDel(id):
    retorno = False
    con = criar_conexao()
    cursor = con.cursor()
    sql_select_query = "select Id, Name, Email from spboxcom_bd.User WHERE Id in ('" + id + "');"
    cursor.execute(sql_select_query)
    record = cursor.fetchone()
    print(record)

    sql_Delete_query = "DELETE FROM User WHERE Id in ('" + id + "');"
    cursor.execute(sql_Delete_query)
    con.commit()

    cursor.execute(sql_select_query)
    records = cursor.fetchall()
    if len(records) == 0:
        retorno = True
        print("\nDeletado ")

    cursor.close()
    return retorno

def getEdit(nome, email, id):
    try:
        con = criar_conexao()
        cursor = con.cursor()

        sql_update_query = """UPDATE spboxcom_bd.User SET Name=%s, Email=%s WHERE Id in (%s);"""
        valores = (nome, email, id)
        print(sql_update_query, valores)
        cursor.execute(sql_update_query, valores)
        con.commit()
        print("Atualizado")

    except mysql.connector.Error as error:
        print("Falha, ao atualuzar table record: {}".format(error))
    finally:
        cursor.close()
    