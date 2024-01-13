import psycopg2
import os
import dotenv

dotenv.load_dotenv()

def setup_ex_2(command, data):
    conn = None
    
    try:
        conn = psycopg2.connect(
            post=os.getenv('DB_POST'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('PASSWORD'),
            port=os.getenv('DB_PORT')
        )
        cursor = conn.cursor()
        
        def exists(data):
            cursor.execute('SELECT * FROM student WHERE id =%s', (data[0],))
            return cursor.fetchone() is not None
        
        for i in data:
            if not exists(i):
                cursor.execute(command, (i[1],i[2]))
        
        conn.commit()
        cursor.close()
        
    except(Exception, psycopg2.DatabaseError) as error:
        raise error
    finally:
        if conn is not None:
            conn.close()

command = """INSERT INTO student(
    name, city)
    VALUES (%s, %s)"""

data = [(11, 'Emilio Ramiro', 'Barcelona'),
        (12, 'Wayne Green', 'New York')]

if __name__ == '__main__':
    setup_ex_2(command, data)