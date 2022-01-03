import mysql


def data_base():
    try:
        conn = mysql.connector.connect(
                        host = '127.0.0.1',
                        user = 'root',
                        passwd = '1234',
                        database="sql_project"
                        )
    
    except (mysql.connector.errors.ProgrammingError):
        conn = mysql.connector.connect(
                    host = '127.0.0.1',
                    user = 'root',
                    passwd = '1234'
                    )
        cur = conn.cursor()
        cur.execute("CREATE DATABASE sql_project")

    return conn   