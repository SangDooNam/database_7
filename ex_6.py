import psycopg2
import os
import dotenv

dotenv.load_dotenv()

def ex_6(command):
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
        
        cursor.execute(command)
        
        cursor.execute("SELECT * FROM student ORDER BY name;")
        rows = cursor.fetchall()
        
        print("{:<5} | {:<20} | {:<20} | {:<20} | {:<20} ".format("id", "name", "city", "mentor_id", "local_mentor"))
        print('-' * 90)
        for row in rows:
            print("{:<5} | {:<20} | {:<20} | {:<20} | {:<20} ".format(*(str(value) if value is not None else '' for value in row)))
        
    except(Exception, psycopg2.DatabaseError) as error:
        raise error
    finally:
        if conn is not None:
            conn.close()


command = """
        UPDATE student 
        SET local_mentor = mentor.id
        FROM mentor
        WHERE student.city = mentor.city;
        """



if __name__ == '__main__':
    ex_6(command)