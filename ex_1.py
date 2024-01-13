import psycopg2
import os
import dotenv

dotenv.load_dotenv()


def join_table():
    
    conn = None
    command = """SELECT student.name AS Student, 
                        mentor.name AS Mentor, 
                        student.city AS Student_city, 
                        mentor.city AS Mentor_city
                FROM student
                JOIN mentor ON student.mentor_id = mentor.id
                ORDER BY student.name ASC;
                """
    
    try:
        conn = psycopg2.connect(
            host = os.getenv('DB_HOST'),
            database = os.getenv('DB_NAME'),
            user = os.getenv('DB_USER'),
            password = os.getenv('PASSWORD'),
            port = os.getenv('DB_PORT')
        )

        cursor = conn.cursor()
        cursor.execute(command)
        rows = cursor.fetchall()
        
        conn.commit()
        print("{:<20} | {:<20} | {:<20} | {:<20}".format("Student", "Mentor", "Student's City", "Mentor's City"))
        print("-" * 85) 
        for row in rows:
            print("{:<20} | {:<20} | {:<20} | {:<20}".format(row[0], row[1], row[2], row[3]))
        
        cursor.close()
        
    except(Exception, psycopg2.DatabaseError) as error:
        raise error
    finally:
        if conn is not None:
            conn.close()

if __name__ == '__main__':
    join_table()