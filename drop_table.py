import psycopg2
import os
import dotenv

dotenv.load_dotenv()

def drop_tables():
    
    conn = None
    commands = ["DROP TABLE mentor;", 'DROP TABLE student;']
    
    try:
        conn = psycopg2.connect(
            post=os.getenv('DB_POST'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('PASSWORD'),
            port=os.getenv('DB_PORT')
        )
        cursor = conn.cursor()
        
        for command in reversed(commands):
            cursor.execute(command)
        conn.commit()
        cursor.close()
        
    except(Exception, psycopg2.DatabaseError) as error:
        raise error
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    drop_tables()