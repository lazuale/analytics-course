-- ========================================
-- UNIVERSITY DATABASE SCHEMA
-- Полная структура реляционной модели данных для университета
-- ========================================

-- Удаление существующих таблиц (если есть)
DROP TABLE IF EXISTS enrollments;
DROP TABLE IF EXISTS courses;
DROP TABLE IF EXISTS professors;
DROP TABLE IF EXISTS departments;
DROP TABLE IF EXISTS students;

-- ========================================
-- ТАБЛИЦА ФАКУЛЬТЕТОВ
-- ========================================
CREATE TABLE departments (
    department_id INTEGER PRIMARY KEY,
    department_name VARCHAR(100) NOT NULL UNIQUE,
    building VARCHAR(100),
    phone VARCHAR(20),
    head_professor_id INTEGER,
    created_date DATE DEFAULT CURRENT_DATE
);

-- Комментарии к таблице факультетов
COMMENT ON TABLE departments IS 'Справочник факультетов университета';
COMMENT ON COLUMN departments.department_id IS 'Уникальный идентификатор факультета';
COMMENT ON COLUMN departments.department_name IS 'Название факультета';
COMMENT ON COLUMN departments.building IS 'Здание, где располагается факультет';
COMMENT ON COLUMN departments.head_professor_id IS 'Заведующий кафедрой (внешний ключ)';

-- ========================================
-- ТАБЛИЦА ПРЕПОДАВАТЕЛЕЙ
-- ========================================
CREATE TABLE professors (
    professor_id INTEGER PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    department_id INTEGER NOT NULL,
    hire_date DATE NOT NULL,
    salary DECIMAL(10,2) CHECK (salary > 0),
    title VARCHAR(50) CHECK (title IN ('Ассистент', 'Старший преподаватель', 'Доцент', 'Профессор')),
    is_active BOOLEAN DEFAULT TRUE,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Комментарии к таблице преподавателей
COMMENT ON TABLE professors IS 'Информация о профессорско-преподавательском составе';
COMMENT ON COLUMN professors.professor_id IS 'Уникальный идентификатор преподавателя';
COMMENT ON COLUMN professors.email IS 'Корпоративная электронная почта';
COMMENT ON COLUMN professors.department_id IS 'Факультет преподавателя';
COMMENT ON COLUMN professors.title IS 'Ученая степень или должность';
COMMENT ON COLUMN professors.is_active IS 'Статус активности (работает/уволен)';

-- ========================================
-- ТАБЛИЦА СТУДЕНТОВ
-- ========================================
CREATE TABLE students (
    student_id INTEGER PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    birth_date DATE NOT NULL,
    enrollment_date DATE NOT NULL DEFAULT CURRENT_DATE,
    status VARCHAR(20) CHECK (status IN ('active', 'graduated', 'suspended', 'transferred', 'expelled')) DEFAULT 'active',
    gpa DECIMAL(3,2) CHECK (gpa >= 0 AND gpa <= 4.0),
    total_credits INTEGER DEFAULT 0,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Комментарии к таблице студентов
COMMENT ON TABLE students IS 'Основная информация о студентах университета';
COMMENT ON COLUMN students.student_id IS 'Уникальный студенческий билет';
COMMENT ON COLUMN students.email IS 'Студенческая электронная почта';
COMMENT ON COLUMN students.status IS 'Текущий статус обучения студента';
COMMENT ON COLUMN students.gpa IS 'Средний балл (Grade Point Average) по шкале 4.0';
COMMENT ON COLUMN students.total_credits IS 'Общее количество накопленных кредитных часов';

-- ========================================
-- ТАБЛИЦА КУРСОВ
-- ========================================
CREATE TABLE courses (
    course_id INTEGER PRIMARY KEY,
    course_name VARCHAR(200) NOT NULL,
    course_code VARCHAR(20) UNIQUE,
    department_id INTEGER NOT NULL,
    credit_hours INTEGER NOT NULL CHECK (credit_hours > 0 AND credit_hours <= 10),
    max_students INTEGER CHECK (max_students > 0 AND max_students <= 100),
    professor_id INTEGER,
    description TEXT,
    prerequisites TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Комментарии к таблице курсов
COMMENT ON TABLE courses IS 'Каталог академических курсов университета';
COMMENT ON COLUMN courses.course_id IS 'Уникальный идентификатор курса';
COMMENT ON COLUMN courses.course_code IS 'Код курса (например, CS101, MATH201)';
COMMENT ON COLUMN courses.credit_hours IS 'Количество зачетных единиц за курс';
COMMENT ON COLUMN courses.max_students IS 'Максимальное количество студентов в группе';
COMMENT ON COLUMN courses.prerequisites IS 'Предварительные требования для записи на курс';

-- ========================================
-- ТАБЛИЦА ЗАПИСЕЙ НА КУРСЫ (связующая таблица M:N)
-- ========================================
CREATE TABLE enrollments (
    enrollment_id INTEGER PRIMARY KEY,
    student_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    professor_id INTEGER NOT NULL,
    semester VARCHAR(20) NOT NULL CHECK (semester IN ('Fall', 'Spring', 'Summer')),
    year INTEGER NOT NULL CHECK (year >= 2000 AND year <= 2030),
    enrollment_date DATE NOT NULL DEFAULT CURRENT_DATE,
    letter_grade VARCHAR(3) CHECK (letter_grade IN ('A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D', 'F', 'I', 'W')),
    grade_points DECIMAL(3,1) CHECK (grade_points >= 0 AND grade_points <= 4.0),
    attendance_percentage DECIMAL(5,2) CHECK (attendance_percentage >= 0 AND attendance_percentage <= 100),
    is_completed BOOLEAN DEFAULT FALSE,
    completion_date DATE,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Комментарии к таблице записей
COMMENT ON TABLE enrollments IS 'Записи студентов на курсы и их успеваемость';
COMMENT ON COLUMN enrollments.enrollment_id IS 'Уникальный идентификатор записи';
COMMENT ON COLUMN enrollments.semester IS 'Семестр (Fall, Spring, Summer)';
COMMENT ON COLUMN enrollments.letter_grade IS 'Буквенная оценка (A, B, C, D, F)';
COMMENT ON COLUMN enrollments.grade_points IS 'Численная оценка по шкале 4.0';
COMMENT ON COLUMN enrollments.attendance_percentage IS 'Процент посещаемости занятий';
COMMENT ON COLUMN enrollments.is_completed IS 'Завершен ли курс студентом';

-- ========================================
-- ВНЕШНИЕ КЛЮЧИ И СВЯЗИ
-- ========================================

-- Связь преподавателей с факультетами (многие к одному)
ALTER TABLE professors 
ADD CONSTRAINT fk_professor_department 
FOREIGN KEY (department_id) REFERENCES departments(department_id);

-- Связь заведующего кафедрой (один к одному)
ALTER TABLE departments 
ADD CONSTRAINT fk_department_head 
FOREIGN KEY (head_professor_id) REFERENCES professors(professor_id);

-- Связь курсов с факультетами (многие к одному)
ALTER TABLE courses 
ADD CONSTRAINT fk_course_department 
FOREIGN KEY (department_id) REFERENCES departments(department_id);

-- Связь курсов с преподавателями (многие к одному)
ALTER TABLE courses 
ADD CONSTRAINT fk_course_professor 
FOREIGN KEY (professor_id) REFERENCES professors(professor_id);

-- Связи в таблице записей (многие к одному)
ALTER TABLE enrollments 
ADD CONSTRAINT fk_enrollment_student 
FOREIGN KEY (student_id) REFERENCES students(student_id);

ALTER TABLE enrollments 
ADD CONSTRAINT fk_enrollment_course 
FOREIGN KEY (course_id) REFERENCES courses(course_id);

ALTER TABLE enrollments 
ADD CONSTRAINT fk_enrollment_professor 
FOREIGN KEY (professor_id) REFERENCES professors(professor_id);

-- ========================================
-- ИНДЕКСЫ ДЛЯ ОПТИМИЗАЦИИ ПРОИЗВОДИТЕЛЬНОСТИ
-- ========================================

-- Индексы на внешние ключи (для ускорения JOIN операций)
CREATE INDEX idx_professors_department ON professors(department_id);
CREATE INDEX idx_courses_department ON courses(department_id);
CREATE INDEX idx_courses_professor ON courses(professor_id);
CREATE INDEX idx_enrollments_student ON enrollments(student_id);
CREATE INDEX idx_enrollments_course ON enrollments(course_id);
CREATE INDEX idx_enrollments_professor ON enrollments(professor_id);

-- Индексы для частых поисков
CREATE INDEX idx_students_email ON students(email);
CREATE INDEX idx_professors_email ON professors(email);
CREATE INDEX idx_students_status ON students(status);
CREATE INDEX idx_students_gpa ON students(gpa);

-- Составные индексы для сложных запросов
CREATE INDEX idx_enrollments_semester_year ON enrollments(semester, year);
CREATE INDEX idx_enrollments_grade ON enrollments(letter_grade, grade_points);
CREATE INDEX idx_students_name ON students(last_name, first_name);
CREATE INDEX idx_professors_name ON professors(last_name, first_name);

-- ========================================
-- ОГРАНИЧЕНИЯ ЦЕЛОСТНОСТИ И БИЗНЕС-ПРАВИЛА
-- ========================================

-- Уникальное ограничение: студент не может записаться на один курс дважды в семестре
ALTER TABLE enrollments 
ADD CONSTRAINT unique_student_course_semester 
UNIQUE (student_id, course_id, semester, year);

-- Проверка корректности email адресов
ALTER TABLE students 
ADD CONSTRAINT check_student_email 
CHECK (email LIKE '%@student.university.edu');

ALTER TABLE professors 
ADD CONSTRAINT check_professor_email 
CHECK (email LIKE '%@university.edu');

-- Проверка возраста студентов (минимум 16 лет)
ALTER TABLE students 
ADD CONSTRAINT check_student_age 
CHECK (DATEDIFF(YEAR, birth_date, CURRENT_DATE) >= 16);

-- Проверка дат зачисления (не может быть в будущем)
ALTER TABLE students 
ADD CONSTRAINT check_enrollment_date 
CHECK (enrollment_date <= CURRENT_DATE);

-- ========================================
-- ПРЕДСТАВЛЕНИЯ ДЛЯ АНАЛИТИКИ
-- ========================================

-- Представление для анализа успеваемости студентов
CREATE VIEW student_performance AS
SELECT 
    s.student_id,
    s.first_name,
    s.last_name,
    s.email,
    COUNT(e.enrollment_id) as courses_taken,
    AVG(e.grade_points) as current_gpa,
    SUM(c.credit_hours) as total_credits_attempted,
    SUM(CASE WHEN e.grade_points >= 2.0 THEN c.credit_hours ELSE 0 END) as credits_earned,
    ROUND(
        SUM(CASE WHEN e.grade_points >= 2.0 THEN c.credit_hours ELSE 0 END) * 100.0 / 
        NULLIF(SUM(c.credit_hours), 0), 
        2
    ) as completion_rate
FROM students s
LEFT JOIN enrollments e ON s.student_id = e.student_id
LEFT JOIN courses c ON e.course_id = c.course_id
WHERE s.status = 'active'
GROUP BY s.student_id, s.first_name, s.last_name, s.email;

-- Представление для анализа загруженности преподавателей
CREATE VIEW professor_workload AS
SELECT 
    p.professor_id,
    p.first_name,
    p.last_name,
    p.title,
    d.department_name,
    COUNT(DISTINCT c.course_id) as courses_teaching,
    COUNT(DISTINCT e.student_id) as students_total,
    AVG(e.grade_points) as avg_student_grade,
    COUNT(e.enrollment_id) as total_enrollments
FROM professors p
JOIN departments d ON p.department_id = d.department_id
LEFT JOIN courses c ON p.professor_id = c.professor_id
LEFT JOIN enrollments e ON c.course_id = e.course_id
WHERE p.is_active = TRUE
GROUP BY p.professor_id, p.first_name, p.last_name, p.title, d.department_name;

-- Представление для трендового анализа поступлений
CREATE VIEW enrollment_trends AS
SELECT 
    e.year,
    e.semester,
    d.department_name,
    COUNT(DISTINCT e.student_id) as unique_students,
    COUNT(e.enrollment_id) as total_enrollments,
    AVG(e.grade_points) as avg_grade,
    SUM(c.credit_hours) as total_credit_hours
FROM enrollments e
JOIN courses c ON e.course_id = c.course_id
JOIN departments d ON c.department_id = d.department_id
GROUP BY e.year, e.semester, d.department_name
ORDER BY e.year DESC, e.semester, d.department_name;

-- ========================================
-- ТРИГГЕРЫ ДЛЯ АВТОМАТИЧЕСКОГО ОБНОВЛЕНИЯ
-- ========================================

-- Триггер для автоматического обновления GPA студента
CREATE TRIGGER update_student_gpa
AFTER INSERT OR UPDATE ON enrollments
FOR EACH ROW
WHEN NEW.grade_points IS NOT NULL
BEGIN
    UPDATE students 
    SET gpa = (
        SELECT AVG(grade_points)
        FROM enrollments
        WHERE student_id = NEW.student_id
        AND grade_points IS NOT NULL
    )
    WHERE student_id = NEW.student_id;
END;

-- Триггер для обновления общих кредитов студента
CREATE TRIGGER update_student_credits
AFTER UPDATE ON enrollments
FOR EACH ROW
WHEN NEW.is_completed = TRUE AND OLD.is_completed = FALSE
BEGIN
    UPDATE students
    SET total_credits = (
        SELECT COALESCE(SUM(c.credit_hours), 0)
        FROM enrollments e
        JOIN courses c ON e.course_id = c.course_id
        WHERE e.student_id = NEW.student_id
        AND e.is_completed = TRUE
        AND e.grade_points >= 2.0
    )
    WHERE student_id = NEW.student_id;
END;

-- ========================================
-- ПРОЦЕДУРЫ ДЛЯ ЧАСТО ИСПОЛЬЗУЕМЫХ ОПЕРАЦИЙ
-- ========================================

-- Процедура для записи студента на курс
CREATE PROCEDURE enroll_student_in_course(
    IN p_student_id INTEGER,
    IN p_course_id INTEGER,
    IN p_semester VARCHAR(20),
    IN p_year INTEGER
)
BEGIN
    DECLARE v_professor_id INTEGER;
    DECLARE v_current_enrollment INTEGER;
    DECLARE v_max_students INTEGER;
    
    -- Получаем преподавателя курса
    SELECT professor_id INTO v_professor_id
    FROM courses
    WHERE course_id = p_course_id;
    
    -- Проверяем лимит студентов
    SELECT COUNT(*), max_students
    INTO v_current_enrollment, v_max_students
    FROM enrollments e
    JOIN courses c ON e.course_id = c.course_id
    WHERE e.course_id = p_course_id
    AND e.semester = p_semester
    AND e.year = p_year
    GROUP BY c.max_students;
    
    -- Проверяем, есть ли места
    IF v_current_enrollment >= v_max_students THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Превышен лимит студентов для курса';
    ELSE
        -- Записываем студента
        INSERT INTO enrollments (student_id, course_id, professor_id, semester, year)
        VALUES (p_student_id, p_course_id, v_professor_id, p_semester, p_year);
    END IF;
END;

-- ========================================
-- ДАННЫЕ ДЛЯ ТЕСТИРОВАНИЯ (СПРАВОЧНЫЕ)
-- ========================================

-- Примеры кодов курсов для различных факультетов
/*
Информатика: CS101, CS201, CS301
Математика: MATH101, MATH201, MATH301  
Физика: PHYS101, PHYS201, PHYS301
Химия: CHEM101, CHEM201, CHEM301
Биология: BIO101, BIO201, BIO301
Экономика: ECON101, ECON201, ECON301
Языки: LANG101, LANG201, LANG301
История: HIST101, HIST201, HIST301
*/

-- ========================================
-- ЗАВЕРШЕНИЕ СОЗДАНИЯ СХЕМЫ
-- ========================================

-- Включение проверки внешних ключей (для SQLite)
PRAGMA foreign_keys = ON;

-- Анализ и оптимизация статистик
ANALYZE;