import psycopg2
from psycopg2 import OperationalError
from psycopg2._psycopg import Error

#Пароль пользователя
password = "123456"
#Название базы данных
name_database = "student_rl2_2022"

#Функция подключения к базе данных
def create_connection(db_name, db_user, db_password, db_host, db_port):
    connection = None
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        print("Connection to PostgreSQL DB successful")
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    return connection

#Подключение к базе данных
connection = create_connection(
    name_database, "postgres", password, "127.0.0.1", "5432"
)

#Функция извлечения данных из базы данных
def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")

#Извлечение данных о среднем балле и академических задолженностях студентов из базы данных
get_info = """
SELECT DISTINCT name, ROUND(AVG(academic_performance.mark_id) OVER(PARTITION BY name), 2) AS avg_mark,
	CASE WHEN academic_performance.student_id IN (
		SELECT DISTINCT student_id
		FROM 
 			academic_performance 
			INNER JOIN discipline ON discipline.discipline_id = academic_performance.discipline_id
			INNER JOIN control ON control.control_id = discipline.control_id
		WHERE mark_id = 2 AND control = 'exam'
		) THEN 'NO' ELSE 'YES' END AS passed_all_exams,
	CASE WHEN academic_performance.student_id IN (
		SELECT DISTINCT student_id
		FROM
 			academic_performance 
			INNER JOIN discipline ON discipline.discipline_id = academic_performance.discipline_id
			INNER JOIN control ON control.control_id = discipline.control_id
		WHERE mark_id = 2 AND control = 'offset'
	) THEN 'NO' ELSE 'YES' END AS passed_all_offset,
	COALESCE((
		SELECT string_agg(discipline, ', ') 
		FROM
			control
			INNER JOIN discipline on control.control_id = discipline.control_id
			INNER JOIN academic_performance ON academic_performance.discipline_id = discipline.discipline_id
			INNER JOIN mark ON mark.mark_id = academic_performance.mark_id
		WHERE mark = 'fail' AND student_id = stu.student_id
		GROUP BY student_id), 'ALL PASSED') AS not_passed_disciplines
FROM
	student AS stu
	INNER JOIN academic_performance ON stu.student_id = academic_performance.student_id
	INNER JOIN mark ON mark.mark_id = academic_performance.mark_id
WHERE academic_performance.mark_id <> 1
ORDER BY 2 DESC, 1
"""

select_student_academic_debt = execute_read_query(connection, get_info)

#Вывод извлеченных записей
for user in select_student_academic_debt:
    print(user)