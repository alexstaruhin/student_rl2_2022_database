import psycopg2
from psycopg2 import OperationalError

#Пароль пользователя
password = "123456"
#Название базы данных
name_database = "student_rl2_2022"
#Адрес директории проекта
dir_addres = """D:\python\DB_student_RL2_2022\source"""


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
    "postgres", "postgres", password, "127.0.0.1", "5432"
)


#Функция создания базы данных
def create_database(connection, query):
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Query executed successfully")
    except OperationalError as e:
        print(f"The error '{e}' occurred")

#Создание базы данных
create_database_query = "CREATE DATABASE " + name_database
create_database(connection, create_database_query)


#Подключение к созданной базе данных
connection = create_connection(
    name_database, "postgres", password, "127.0.0.1", "5432"
)


#Функция для организации таблиц
def execute_query(connection, query):
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Query executed successfully")
    except OperationalError as e:
        print(f"The error '{e}' occurred")

###########################  DDL ############################

create_student_table = """
CREATE TABLE IF NOT EXISTS student (
    student_id bigint NOT NULL PRIMARY KEY,
    name character varying(30) NOT NULL,
    record_number character varying(6) NOT NULL
)
"""

execute_query(connection, create_student_table)


create_city_table = """
CREATE TABLE IF NOT EXISTS city (
    city_id bigint NOT NULL PRIMARY KEY,
    city character varying(50) NOT NULL
)
"""

execute_query(connection, create_city_table)


create_control_table = """
CREATE TABLE IF NOT EXISTS control (
    control_id bigint NOT NULL PRIMARY KEY,
    control character varying(50) NOT NULL
)
"""

execute_query(connection, create_control_table)


create_mark_table = """
CREATE TABLE IF NOT EXISTS mark (
    mark_id bigint NOT NULL PRIMARY KEY,
    mark character varying(15) NOT NULL
)
"""

execute_query(connection, create_mark_table)


create_subject_table = """
CREATE TABLE IF NOT EXISTS subject (
    subject_id bigint NOT NULL PRIMARY KEY,
    subject character varying(50) NOT NULL
)
"""

execute_query(connection, create_subject_table)


create_discipline_table = """
CREATE TABLE IF NOT EXISTS discipline (
    discipline_id bigint NOT NULL PRIMARY KEY,
    discipline character varying(50) NOT NULL,
    control_id bigint NOT NULL REFERENCES control(control_id),
    semester integer
)
"""

execute_query(connection, create_discipline_table)


create_academic_performance_table = """
CREATE TABLE IF NOT EXISTS academic_performance (
    academic_performance_id bigint NOT NULL PRIMARY KEY,
    student_id bigint NOT NULL REFERENCES student(student_id),
    discipline_id bigint NOT NULL REFERENCES discipline(discipline_id),
    mark_id bigint NOT NULL REFERENCES mark(mark_id)
)
"""

execute_query(connection, create_academic_performance_table)


create_points_for_exam_table = """
CREATE TABLE IF NOT EXISTS points_for_exam (
    points_for_exam_id bigint NOT NULL PRIMARY KEY,
    student_id bigint REFERENCES student(student_id),
    subject_id bigint REFERENCES subject(subject_id),
    points integer
)
"""

execute_query(connection, create_points_for_exam_table)


create_student_info_table = """
CREATE TABLE IF NOT EXISTS student_info (
    student_info_id bigint NOT NULL PRIMARY KEY,
    student_id bigint REFERENCES student(student_id),
    gender character varying(6) NOT NULL,
    city_id bigint REFERENCES city(city_id),
    type character varying(30),
    company character varying(100),
    CONSTRAINT gender_constraint CHECK ((((gender)::text = 'Female'::text) OR ((gender)::text = 'Male'::text))),
    CONSTRAINT type_constraint CHECK ((((type)::text = 'budget'::text) OR ((type)::text = 'target'::text)))
)
"""

execute_query(connection, create_student_info_table)

###########################  DML ############################

fill_student_table = """
COPY student from '""" + dir_addres + """\student.csv' DELIMITER ',' CSV HEADER
"""

execute_query(connection, fill_student_table)


fill_city_table = """
COPY city from '""" + dir_addres + """\city.csv' DELIMITER ',' CSV HEADER
"""

execute_query(connection, fill_city_table)


fill_control_table = """
COPY control from '""" + dir_addres + """\control.csv' DELIMITER ',' CSV HEADER
"""

execute_query(connection, fill_control_table)


fill_mark_table = """
COPY mark from '""" + dir_addres + """\mark.csv' DELIMITER ',' CSV HEADER
"""

execute_query(connection, fill_mark_table)


fill_subject_table = """
COPY subject from '""" + dir_addres + """\subject.csv' DELIMITER ',' CSV HEADER
"""

execute_query(connection, fill_subject_table)


fill_discipline_table = """
COPY discipline from '""" + dir_addres + """\discipline.csv' DELIMITER ',' CSV HEADER
"""

execute_query(connection, fill_discipline_table)


fill_academic_performance_table = """
COPY academic_performance from '""" + dir_addres + """\Academic_performance.csv' DELIMITER ',' CSV HEADER
"""

execute_query(connection, fill_academic_performance_table)


fill_points_for_exam_table = """
COPY points_for_exam from '""" + dir_addres + """\points_for_exam.csv' DELIMITER ',' CSV HEADER
"""

execute_query(connection, fill_points_for_exam_table)


fill_student_info_table = """
COPY student_info from '""" + dir_addres + """\student_info.csv' DELIMITER ',' CSV HEADER
"""

execute_query(connection, fill_student_info_table)