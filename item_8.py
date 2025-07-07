#Conexión con la DB

import psycopg2
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

conn = psycopg2.connect(database="Chinook",
                        host="localhost",
                        user="postgres",
                        password="Catalina1234",
                        port="5432")

cursor = conn.cursor()

cursor.execute('SELECT * FROM public."Album"')
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
