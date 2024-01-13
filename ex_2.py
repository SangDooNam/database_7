import psycopg2
import os
import dotenv

dotenv.load_dotenv()


def ex_2():
    
    conn = None
    command = """SELECT student.name AS Student,
                        mentor.name AS Mentor, 
                        student.city AS Student_city,
                        mentor.city AS Mentor_city
                FROM student
                LEFT JOIN mentor ON student.mentor_id = mentor.id
                ORDER BY student.name;
                """
    
    try:
        conn = psycopg2.connect(
            post=os.getenv('DB_POST'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('PASSWORD'),
            port=os.getenv('DB_PORT')
        )
        
        cursor = conn.cursor()
        
        cursor.execute(command)
        
        rows = cursor.fetchall()
        
        conn.commit()
        
        print("{:<20} | {:<20} | {:<20} | {:<20}".format("Student", "Mentor", "Student's City", "Mentor's City"))
        print("-" * 85)
        for row in rows:
            print("{:<20} | {:<20} | {:<20} | {:<20}".format(*(str(value) if value is not None else "" for value in row)))
            
        cursor.close()
            
    except(Exception, psycopg2.DatabaseError) as error:
        raise  error
        
    finally:
        if conn is not None:
            conn.close()



if __name__ == '__main__':
    ex_2()