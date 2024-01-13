import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def setup(command_mentor,
        command_student, 
        command_insert_mentor, 
        mentor_data, 
        command_insert_student, 
        student_data):
    conn = None
    try:
        conn = psycopg2.connect(
            host = os.getenv('DB_HOST'),
            database = os.getenv('DB_NAME'),
            user = os.getenv('DB_USER'),
            password = os.getenv('PASSWORD'),
            port = os.getenv('DB_PORT')
        )
        
        cursor = conn.cursor()
        
        cursor.execute(command_mentor)
        cursor.execute(command_student)
        
        def exists_mentor(data):
            cursor.execute('SELECT * FROM mentor WHERE id = %s', (data[0],))
            return cursor.fetchone() is not None
        
        def exists_student(data):
            cursor.execute('SELECT * FROM student WHERE id = %s', (data[0],))
            return cursor.fetchone() is not None
        
        for data in mentor_data:
            if not exists_mentor(data):
                cursor.execute(command_insert_mentor, (data[1],data[2]))
        
        for data in student_data:
            if not exists_student(data):
                cursor.execute(command_insert_student, (data[1],data[2],data[3]))
        
        conn.commit()
        cursor.close()
        
    except(Exception, psycopg2.DatabaseError) as error:
        raise error
        
    finally:
        if conn is not None:
            conn.close()

command_mentor = """CREATE TABLE IF NOT EXISTS mentor (
    id SERIAL PRIMARY KEY,
    name VARCHAR(25),
    city VARCHAR(25)
    );
    """
command_student = """CREATE TABLE IF NOT EXISTS student (
    id SERIAL PRIMARY KEY,
    name VARCHAR(25),
    city VARCHAR(25),
    mentor_id INT REFERENCES mentor(id)
    );
    """
command_insert_mentor = """INSERT INTO mentor(
    name, city)
    VALUES (%s,%s);
    """
mentor_data= [
    ('1', 'Peter Smith', 'New York'),
    ('2', 'Laura Wild', 'Chicago'),
    ('3', 'Julius Maxim', 'Berlin'),
    ('4', 'Melinda O''Connor', 'Berlin'),
    ('5', 'Patricia Boulard', 'Marseille'),
    ('6', 'Julia Vila', 'Barcelona'),
    ('7', 'Fabienne Martin', 'Paris')
    ]
command_insert_student = """INSERT INTO student(
    name, city, mentor_id)
    VALUES (%s,%s,%s);
    """
student_data =[
    ('1', 'Dolores Perez', 'Barcelona', '2'),
    ('2', 'Maria Highsmith', 'New York', '3'),
    ('3', 'Aimaar Abdul', 'Chicago', '1'),
    ('4', 'Gudrun Schmidt', 'Berlin', '5'),
    ('5', 'Gerald Hutticher', 'Berlin', '6'),
    ('6', 'Itzi Elizabal', 'Barcelona', '4'),
    ('7', 'Irmgard Seekircher', 'Berlin', '7'),
    ('8', 'Christian Blanc', 'Paris', '4'),
    ('9', 'Alex Anjou', 'Paris', '3'),
    ('10', 'John Goldwin', 'Chicago', '6')
    ]

if __name__ == '__main__':
    setup(command_mentor, 
        command_student, 
        command_insert_mentor, 
        mentor_data, 
        command_insert_student, 
        student_data)