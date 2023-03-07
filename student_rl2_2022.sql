##### student_rl2_2019 SQL Project  

###########################  DDL ############################

CREATE TABLE student (
    student_id bigint NOT NULL PRIMARY KEY,
    name character varying(30) NOT NULL,
    record_number character varying(6) NOT NULL
);

CREATE TABLE city (
    city_id bigint NOT NULL PRIMARY KEY,
    city character varying(50) NOT NULL
);

CREATE TABLE control (
    control_id bigint NOT NULL PRIMARY KEY,
    control character varying(50) NOT NULL
);

CREATE TABLE mark (
    mark_id bigint NOT NULL PRIMARY KEY,
    mark character varying(15) NOT NULL
);

CREATE TABLE subject (
    subject_id bigint NOT NULL PRIMARY KEY,
    subject character varying(50) NOT NULL
);

CREATE TABLE discipline (
    discipline_id bigint NOT NULL PRIMARY KEY,
    discipline character varying(50) NOT NULL,
    control_id bigint NOT NULL REFERENCES control(control_id),
    semester integer
);

CREATE TABLE academic_performance (
    academic_performance_id bigint NOT NULL PRIMARY KEY,
    student_id bigint NOT NULL REFERENCES student(student_id),
    discipline_id bigint NOT NULL REFERENCES discipline(discipline_id),
    mark_id bigint NOT NULL REFERENCES mark(mark_id)
);

CREATE TABLE points_for_exam (
    points_for_exam_id bigint NOT NULL PRIMARY KEY,
    student_id bigint REFERENCES student(student_id),
    subject_id bigint REFERENCES subject(subject_id),
    points integer
);

CREATE TABLE student_info (
    student_info_id bigint NOT NULL PRIMARY KEY,
    student_id bigint REFERENCES student(student_id),
    gender character varying(6) NOT NULL,
    city_id bigint REFERENCES city(city_id),
    type character varying(30),
    company character varying(100),
    CONSTRAINT gender_constraint CHECK ((((gender)::text = 'Female'::text) OR ((gender)::text = 'Male'::text))),
    CONSTRAINT type_constraint CHECK ((((type)::text = 'budget'::text) OR ((type)::text = 'target'::text)))
);

###########################  DML ############################

## Importing the Data

COPY student from 'D:\python\DB_student_RL2_2022\source\student.csv' DELIMITER ',' CSV HEADER;

COPY city from 'D:\python\DB_student_RL2_2022\source\city.csv' DELIMITER ',' CSV HEADER;

COPY control from 'D:\python\DB_student_RL2_2022\source\control.csv' DELIMITER ',' CSV HEADER;

COPY mark from 'D:\python\DB_student_RL2_2022\source\mark.csv' DELIMITER ',' CSV HEADER;

COPY subject from 'D:\python\DB_student_RL2_2022\source\subject.csv' DELIMITER ',' CSV HEADER;

COPY discipline from 'D:\python\DB_student_RL2_2022\source\discipline.csv' DELIMITER ',' CSV HEADER;

COPY academic_performance from 'D:\python\DB_student_RL2_2022\source\academic_performance.csv' DELIMITER ',' CSV HEADER;

COPY points_for_exam from 'D:\python\DB_student_RL2_2022\source\points_for_exam.csv' DELIMITER ',' CSV HEADER;

COPY student_info from 'D:\python\DB_student_RL2_2022\source\student_info.csv' DELIMITER ',' CSV HEADER;

#Fetch all records

select * 
from 
	discipline
	INNER JOIN academic_performance ON academic_performance.discipline_id = discipline.discipline_id
	INNER JOIN student ON student.student_id = academic_performance.student_id
	INNER JOIN mark ON mark.mark_id = academic_performance.mark_id
	INNER JOIN control ON control.control_id = discipline.control_id
	INNER JOIN student_info ON student.student_id = student_info.student_id
	INNER JOIN city ON city.city_id = student_info.city_id
	INNER JOIN points_for_exam ON points_for_exam.student_id = student.student_id
	INNER JOIN subject ON points_for_exam.subject_id = subject.subject_id;

#GPA of students and their academic debts

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
ORDER BY 2 DESC, 1;