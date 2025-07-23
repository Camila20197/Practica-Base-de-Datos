#Conexión con la DB

import psycopg2
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import os
from dotenv import load_dotenv

load_dotenv()

db_config = {
    "database": os.getenv("DB_NAME_TP_DB","Chinook"),  
    "host": os.getenv("DB_HOST_TP_DB", "localhost").split(':')[0],
    "user": os.getenv("DB_USER_TP_DB"),
    "password": os.getenv("DB_PASSWORD_TP_DB"),
    "port": os.getenv("DB_PORT_TP_DB", "5432")
}



if not db_config["user"] or not db_config["password"]:
    raise ValueError("Faltan credenciales esenciales de la base de datos en las variables de entorno")

try:
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
    """)
    print("Tablas existentes:", cursor.fetchall())
    #cursor.execute('SELECT * FROM public."Album"')
    #albunes = pd.DataFrame(cursor.fetchall(), columns=[desc[0] for desc in cursor.description])
    #print(albunes)

    query_emp = """
        SELECT e."FirstName" || ' ' || e."LastName" AS empleado,
            COUNT(c."CustomerId") AS cantidad_clientes
        FROM "Employee" e
        LEFT JOIN "Customer" c ON e."EmployeeId" = c."SupportRepId"
        GROUP BY empleado
        ORDER BY cantidad_clientes DESC;
    """

    cursor.execute(query_emp)
    resultado = cursor.fetchall()
    for fila in resultado:
        print(fila)
        
    df_emp = pd.read_sql_query(query_emp, conn)

    plt.figure(figsize=(8,5))
    sns.barplot(data=df_emp, x='empleado', y='cantidad_clientes', palette='Set2')
    plt.title("Clientes asignados por empleado")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    query_ventas = """
    SELECT DATE_TRUNC('month', "InvoiceDate") AS mes,
        SUM("Total") AS total_ventas
    FROM "Invoice"
    GROUP BY mes
    ORDER BY mes;
    """

    cursor.execute(query_ventas)
    resultado = cursor.fetchall()
    for fila in resultado:
        print(fila)
        
    df_ventas = pd.read_sql_query(query_ventas, conn)


    plt.figure(figsize=(10,5))
    plt.plot(df_ventas['mes'], df_ventas['total_ventas'], marker='o', linestyle='-', color='dodgerblue')
    plt.title("Evolución de ventas por mes en un periodo en 5 años")
    plt.xlabel("Año")
    plt.ylabel("Total ventas")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
except psycopg2.Error as e:
    print(f"Error al conectar a la base de datos: {e}")
