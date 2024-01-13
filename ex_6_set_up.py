import psycopg2
import os
import dotenv

dotenv.load_dotenv()

def setup(commands):
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
        
        for command in commands:
            cursor.execute(command)
        
        conn.commit()
        cursor.close()
        
    except(Exception, psycopg2.DatabaseError) as error:
        raise  error
    
    finally:
        if conn is not None:
            conn.close()
            
            
commands = ["""ALTER TABLE student ADD COLUMN local_mentor INT;""",
            """ALTER TABLE student 
            ADD CONSTRAINT student_local_mentor_fkey 
            FOREIGN KEY (local_mentor) 
            REFERENCES mentor(id);"""
            ]
    
if __name__ == '__main__':
    setup(commands)