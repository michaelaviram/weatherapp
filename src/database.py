import subprocess 
import os 
import mysql.connector 
from mysql.connector import Error

def get_db_connection(namespace):
    """
    Establishes a connection to the MySQL database
    That runs inside the minikube cluster.
    """

    host = f"db-mysql.{namespace}.svc.cluster.local"
    database = "weather"
    user = "root"
    get_password = f"kubectl get secret --namespace {namespace} db-mysql -o jsonpath='{{.data.mysql-root-password}}' | base64 -d"
    password = subprocess.run(get_password, shell=True, stdout=subprocess.PIPE, text=True)
    try:
        connection = mysql.connector.connect(
            host=host,
            port=3306,
            database=database,
            user=user,
            password=password.stdout.strip()
        )
        if connection.is_connected():
            return connection

    except Error as e:
        return None


def write_to_db(namespace):
    """
    Writes the forecast data to the MySQL database.
    """

    connection = get_db_connection(namespace)
    if connection is None:
        return "Failed to connect to MySQL database"

    try:
        cursor = connection.cursor()
        cursor.execute("USE weather;")
        cursor.execute(f"CREATE TABLE {location};")
        return None

    except Error as err:
        return f"{err}"

    except Exception as e:
        return f"{e}"

    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()


