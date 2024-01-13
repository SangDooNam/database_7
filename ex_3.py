import psycopg2
import os
import dotenv

dotenv.load_dotenv()

def ex_3(command):
    conn = None
    
    try:
        conn = psycopg2.connect(
            post=os.getenv('DB_POST'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('PASSWORD'),
            port=os.getenv('DB_PORT'),
        )
        
        cursor = conn.cursor()
        
        cursor.execute(command)
        
        rows = cursor.fetchall()
        
        print('{:<20} | {:<20} | {:<20} | {:<20}'.format("Mentor", "Student" , "Mentor's city", "Student's city"))
        print('-' * 85)
        for row in rows:
            print('{:<20} | {:<20} | {:<20} | {:<20}'.format(*(str(value) if value is not None else '' for value in row)))

    except(Exception, psycopg2.DatabaseError) as error:
        raise error
    finally:
        if conn is not None:
            conn.close()


command = """SELECT mentor.name AS Mentor, 
                    student.name AS Student, 
                    mentor.city AS Mentor_city, 
                    student.city AS Student_city
            FROM student
            RIGHT JOIN mentor ON student.mentor_id = mentor.id
            ORDER BY mentor.name;
            """
            
if __name__ == '__main__':
    ex_3(command)