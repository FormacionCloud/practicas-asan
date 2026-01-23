import sys
import logging
import pymysql
import json
import os

# Variables de entorno
user_name = os.environ['USER_NAME']
password = os.environ['PASSWORD']
rds_proxy_host = os.environ['RDS_PROXY_HOST']
db_name = os.environ['DB_NAME']

logger = logging.getLogger()
logger.setLevel(logging.INFO)

try:
    conn = pymysql.connect(host=rds_proxy_host, user=user_name, passwd=password, db=db_name, connect_timeout=5)
except pymysql.MySQLError as e:
    logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
    logger.error(e)
    sys.exit(1)

logger.info("SUCCESS: Connection to RDS for MySQL instance succeeded")

def lambda_handler(event, context):
    """
    This function creates a new RDS database table and writes records to it
    """
    CustID = event['CustID']
    Name = event['Name']

    item_count = 0
    sql_string = f"insert into Customer (CustID, Name) values(%s, %s)"

    try:
      with conn.cursor() as cur:
          cur.execute("create table if not exists Customer ( CustID  int NOT NULL, Name varchar(255) NOT NULL, PRIMARY KEY (CustID))")
          cur.execute(sql_string, (CustID, Name))
          conn.commit()
          cur.execute("select * from Customer")
          logger.info("The following items have been added to the database:")
          for row in cur:
              item_count += 1
              logger.info(row)
      conn.commit()

      return "Added %d items to RDS for MySQL table" %(item_count)
    except Exception as e:
      return(e)
    

# Este código solo se ejecuta en local. Al final tienes ejemplos sobre cómo ejecutar el código en la línea de comando de Visual Studio Code
if __name__ == '__main__':
    # Configurar logger para mostrar en local
    logger.addHandler(logging.StreamHandler(sys.stdout))
    # Obtener datos de entrada (evento) a partir de CLI
    cliData = json.loads(sys.argv[1])
    # Ejecución de la función
    res = lambda_handler(cliData, '')
    print("---")
    print("Resultado de ejecución de la función:")
    print(res)
    print("---")


# Ejemplo de ejecución en local (observar la comilla simple para introducir el parámetro como texto)
# python lambda.py '{"CustID": "13339", "Name": "Mi Nombre y Apellido"}'

# Evento lambda test (objeto json, no string)
# {"CustID": "123123123", "Name": "PPRIETO"}
