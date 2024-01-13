import psycopg2
import os
import dotenv

dotenv.load_dotenv()

def setup(command, values):
    
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
        def exists(value):
            cursor.execute("SELECT id FROM mentor WHERE id = %s", (value[0],))
            return cursor.fetchone() is not None
        
        for value in values:
            if not exists(value):
                cursor.execute(command, (value[1],value[2]))
        
        conn.commit()
        cursor.close()
        
    except(Exception, psycopg2.DatabaseError) as error:
        raise error
    finally:
        if conn is not None:
            conn.close()


command = """INSERT INTO mentor(
        name, city)
        VALUES(%s, %s)
        ;"""

values = [
    (8, 'Rose Dupond', 'Brussels'),
    (9, 'Ahmed Ali', 'Marseille')
    ]

if __name__ == '__main__':
    setup(command, values)