#!/usr/bin/env python
import psycopg2
import datetime
from configparser import ConfigParser

def conectar_bd():
    config = ler_config()
    return psycopg2.connect(**config)

def data_e_hora():
    return formatar_data(datetime.datetime.today())

def formatar_data(data):
    return data.strftime('%d/%m/%Y %H:%M')

def solicitar_registro():
    escreva = input('Escreva sobre o seu dia: \n{}: '.format(data_e_hora()))
    escreva = escreva.strip()
    return escreva

def incluir_registro(conn, registro):
    cur = conn.cursor()
    cur.execute(f"INSERT into registros (horario, texto) values(now(), '{registro}')")
    conn.commit()
    cur.close()

def mostrar_ultimo(conn):
    cur = conn.cursor()
    cur.execute("SELECT * from registros order by horario desc limit 1")
    ultimo_registro = cur.fetchone()
    print("Seu último registro foi: \n{}: {}".format(formatar_data(ultimo_registro[0]), ultimo_registro[1]))
    cur.close()

def ler_config():
    parser = ConfigParser()
    parser.read("config.ini")
    db = {}
    if parser.has_section("postgresql"):
        params = parser.items("postgresql")
        for param in params:
            db[param[0]] = param[1]
    return db

conn = conectar_bd()
mostrar_ultimo(conn)
registro = solicitar_registro()
incluir_registro(conn, registro)
conn.close()
