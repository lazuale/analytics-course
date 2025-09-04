-- ========================================
-- ДЕНОРМАЛИЗОВАННЫЕ ДАННЫЕ ДЛЯ УПРАЖНЕНИЙ ПО НОРМАЛИЗАЦИИ
-- Примеры нарушений 1НФ, 2НФ и 3НФ
-- ========================================

-- ========================================
-- НАРУШЕНИЕ 1НФ (Первая нормальная форма)
-- Проблема: Множественные значения в одной ячейке
-- ========================================

-- ПЛОХОЙ пример: Студенты с множественными курсами в одной ячейке
CREATE TABLE bad_students_1nf (
    student_id INTEGER PRIMARY KEY,
    student_name VARCHAR(100),
    email VARCHAR(100),
    courses TEXT,  -- НАРУШЕНИЕ: "Math101, Physics201, Chemistry301"
    professors TEXT,  -- НАРУШЕНИЕ: "Dr. Smith, Dr. Johnson, Dr. Brown"
    grades TEXT,  -- НАРУШЕНИЕ: "A, B+, A-"
    enrollment_date DATE
);

-- Вставка примеров плохих данных
INSERT INTO bad_students_1nf VALUES 
(1, 'Иван Петров', 'ivan@student.edu', 'CS101, MATH201, PHYS101', 'Смирнов И.И., Козлов А.В., Морозова Е.П.', 'A, B+, A-', '2023-09-01'),
(2, 'Мария Сидорова', 'maria@student.edu', 'CHEM101, BIO201', 'Новиков С.С., Федорова О.И.', 'A-, B', '2023-09-01'),
(3, 'Алексей Козлов', 'alexey@student.edu', 'ECON101, HIST201, LANG101', 'Орлов Н.Н., Попова Т.Т., Соколова Н.З.', 'B+, A, B-', '2023-09-01');

/*
ЗАДАНИЕ ДЛЯ СТУДЕНТОВ:
Приведите таблицу bad_students_1nf к 1НФ.
Подсказка: Создайте отдельные таблицы для студентов, курсов и записей на курсы.
*/

-- ========================================
-- НАРУШЕНИЕ 2НФ (Вторая нормальная форма)  
-- Проблема: Частичные зависимости от составного ключа
-- ========================================

-- ПЛОХОЙ пример: Детали записей с частичными зависимостями
CREATE TABLE bad_enrollment_details_2nf (
    student_id INTEGER,
    course_id INTEGER,
    student_name VARCHAR(100),  -- НАРУШЕНИЕ: зависит только от student_id
    student_email VARCHAR(100), -- НАРУШЕНИЕ: зависит только от student_id
    student_major VARCHAR(100), -- НАРУШЕНИЕ: зависит только от student_id
    course_name VARCHAR(100),   -- НАРУШЕНИЕ: зависит только от course_id
    course_credits INTEGER,     -- НАРУШЕНИЕ: зависит только от course_id
    professor_name VARCHAR(100),-- НАРУШЕНИЕ: зависит только от course_id
    semester VARCHAR(20),
    year INTEGER,
    grade VARCHAR(3),
    enrollment_date DATE,
    PRIMARY KEY (student_id, course_id, semester, year)
);

-- Вставка примеров данных с нарушением 2НФ
INSERT INTO bad_enrollment_details_2nf VALUES 
(1001, 101, 'Иван Петров', 'ivan@student.edu', 'Информатика', 'Основы программирования', 4, 'Смирнов И.И.', 'Fall', 2023, 'A', '2023-08-15'),
(1001, 102, 'Иван Петров', 'ivan@student.edu', 'Информатика', 'Математический анализ', 5, 'Козлов А.В.', 'Fall', 2023, 'B+', '2023-08-15'),
(1002, 101, 'Мария Сидорова', 'maria@student.edu', 'Математика', 'Основы программирования', 4, 'Смирнов И.И.', 'Fall', 2023, 'A-', '2023-08-16'),
(1002, 103, 'Мария Сидорова', 'maria@student.edu', 'Математика', 'Общая физика', 4, 'Морозова Е.П.', 'Fall', 2023, 'B', '2023-08-16');

/*
ЗАДАНИЕ ДЛЯ СТУДЕНТОВ:
Приведите таблицу bad_enrollment_details_2nf к 2НФ.
Подсказка: Вынесите атрибуты, которые зависят только от части составного ключа, в отдельные таблицы.
*/

-- ========================================
-- НАРУШЕНИЕ 3НФ (Третья нормальная форма)
-- Проблема: Транзитивные зависимости  
-- ========================================

-- ПЛОХОЙ пример: Курсы с транзитивными зависимостями
CREATE TABLE bad_courses_3nf (
    course_id INTEGER PRIMARY KEY,
    course_name VARCHAR(100),
    course_code VARCHAR(20),
    department_id INTEGER,
    department_name VARCHAR(100), -- НАРУШЕНИЕ: зависит от department_id, а не от course_id
    department_head VARCHAR(100), -- НАРУШЕНИЕ: зависит от department_id через department_name
    building VARCHAR(100),        -- НАРУШЕНИЕ: зависит от department_id
    building_address VARCHAR(200),-- НАРУШЕНИЕ: зависит от building, а не от course_id
    professor_id INTEGER,
    credit_hours INTEGER
);

-- Вставка примеров данных с нарушением 3НФ
INSERT INTO bad_courses_3nf VALUES 
(101, 'Основы программирования', 'CS101', 1, 'Информатика и ВТ', 'Смирнов И.И.', 'Главный корпус', 'ул. Университетская, 1', 1, 4),
(102, 'Алгоритмы и структуры данных', 'CS201', 1, 'Информатика и ВТ', 'Смирнов И.И.', 'Главный корпус', 'ул. Университетская, 1', 2, 4),
(201, 'Математический анализ', 'MATH101', 2, 'Математика', 'Козлов А.В.', 'Математический корпус', 'ул. Ломоносова, 3', 6, 5),
(202, 'Линейная алгебра', 'MATH201', 2, 'Математика', 'Козлов А.В.', 'Математический корпус', 'ул. Ломоносова, 3', 7, 4);

/*
ЗАДАНИЕ ДЛЯ СТУДЕНТОВ:
Приведите таблицу bad_courses_3nf к 3НФ.
Подсказка: Вынесите транзитивно зависимые атрибуты в отдельные таблицы.
*/

-- ========================================
-- КОМПЛЕКСНЫЙ ПРИМЕР: НАРУШЕНИЕ ВСЕХ ТРЕХ НФ
-- ========================================

-- ОЧЕНЬ ПЛОХОЙ пример: Таблица со всеми типами нарушений
CREATE TABLE very_bad_university_data (
    record_id INTEGER PRIMARY KEY,
    student_id INTEGER,
    student_name VARCHAR(100),
    student_courses TEXT,           -- НАРУШЕНИЕ 1НФ: множественные значения
    student_grades TEXT,            -- НАРУШЕНИЕ 1НФ: множественные значения  
    course_id INTEGER,
    course_name VARCHAR(100),       -- НАРУШЕНИЕ 2НФ: зависит только от course_id
    course_credits INTEGER,         -- НАРУШЕНИЕ 2НФ: зависит только от course_id
    department_id INTEGER,          -- НАРУШЕНИЕ 2НФ: зависит только от course_id
    department_name VARCHAR(100),   -- НАРУШЕНИЕ 3НФ: зависит от department_id
    department_building VARCHAR(100), -- НАРУШЕНИЕ 3НФ: зависит от department_name
    professor_id INTEGER,
    professor_name VARCHAR(100),    -- НАРУШЕНИЕ 2НФ: зависит только от professor_id  
    professor_salary DECIMAL(10,2), -- НАРУШЕНИЕ 2НФ: зависит только от professor_id
    semester VARCHAR(20),
    year INTEGER,
    enrollment_date DATE
);

-- Вставка комплексных плохих данных
INSERT INTO very_bad_university_data VALUES 
(1, 1001, 'Иван Петров', 'CS101, MATH201, PHYS101', 'A, B+, A-', 101, 'Основы программирования', 4, 1, 'Информатика', 'Главный корпус', 1, 'Смирнов И.И.', 85000.00, 'Fall', 2023, '2023-08-15'),
(2, 1002, 'Мария Сидорова', 'MATH101, CHEM201', 'A-, B', 201, 'Математический анализ', 5, 2, 'Математика', 'Мат. корпус', 6, 'Козлов А.В.', 90000.00, 'Fall', 2023, '2023-08-16');

/*
КОМПЛЕКСНОЕ ЗАДАНИЕ:
Проанализируйте таблицу very_bad_university_data и:
1. Определите все нарушения 1НФ, 2НФ и 3НФ
2. Спроектируйте нормализованную схему в 3НФ
3. Создайте правильные таблицы с корректными связями
4. Перенесите данные в нормализованную структуру
*/

-- ========================================
-- ДОПОЛНИТЕЛЬНЫЕ ПРИМЕРЫ ПЛОХОГО ПРОЕКТИРОВАНИЯ
-- ========================================

-- Пример: Нарушение атомарности адресов
CREATE TABLE bad_student_contacts (
    student_id INTEGER PRIMARY KEY,
    full_name VARCHAR(100),         -- НАРУШЕНИЕ: имя и фамилия вместе
    full_address TEXT,              -- НАРУШЕНИЕ: улица, город, индекс вместе
    phone_numbers TEXT,             -- НАРУШЕНИЕ 1НФ: несколько телефонов
    emergency_contacts TEXT         -- НАРУШЕНИЕ 1НФ: несколько контактов
);

INSERT INTO bad_student_contacts VALUES 
(1001, 'Петров Иван Сергеевич', 'ул. Ленина, 15, кв. 25, Москва, 123456', '+7-900-123-45-67, +7-495-987-65-43', 'Мама: Петрова М.И. +7-900-111-22-33, Папа: Петров С.В. +7-900-444-55-66');

-- Пример: Избыточность из-за отсутствия нормализации
CREATE TABLE bad_course_schedule (
    schedule_id INTEGER PRIMARY KEY,
    course_name VARCHAR(100),
    course_code VARCHAR(20),
    professor_name VARCHAR(100),
    professor_email VARCHAR(100),
    professor_phone VARCHAR(20),
    department_name VARCHAR(100),   -- Дублируется для каждого курса
    classroom VARCHAR(50),
    time_slot VARCHAR(50),
    day_of_week VARCHAR(20),
    semester VARCHAR(20),
    year INTEGER
);

-- ========================================
-- ПРАВИЛЬНЫЕ РЕШЕНИЯ (ОТВЕТЫ ДЛЯ ПРЕПОДАВАТЕЛЕЙ)
-- ========================================

/*
РЕШЕНИЕ 1НФ - Разделение на атомарные таблицы:

CREATE TABLE students_normalized (
    student_id INTEGER PRIMARY KEY,
    student_name VARCHAR(100),
    email VARCHAR(100),
    enrollment_date DATE
);

CREATE TABLE courses_normalized (
    course_id INTEGER PRIMARY KEY,
    course_name VARCHAR(100),
    professor_name VARCHAR(100)
);

CREATE TABLE student_courses_normalized (
    student_id INTEGER,
    course_id INTEGER,
    grade VARCHAR(3),
    PRIMARY KEY (student_id, course_id)
);
*/

/*
РЕШЕНИЕ 2НФ - Устранение частичных зависимостей:

CREATE TABLE students_2nf (
    student_id INTEGER PRIMARY KEY,
    student_name VARCHAR(100),
    student_email VARCHAR(100),
    student_major VARCHAR(100)
);

CREATE TABLE courses_2nf (
    course_id INTEGER PRIMARY KEY,
    course_name VARCHAR(100),
    course_credits INTEGER,
    professor_name VARCHAR(100)
);

CREATE TABLE enrollments_2nf (
    student_id INTEGER,
    course_id INTEGER,
    semester VARCHAR(20),
    year INTEGER,
    grade VARCHAR(3),
    enrollment_date DATE,
    PRIMARY KEY (student_id, course_id, semester, year)
);
*/

/*
РЕШЕНИЕ 3НФ - Устранение транзитивных зависимостей:

CREATE TABLE departments_3nf (
    department_id INTEGER PRIMARY KEY,
    department_name VARCHAR(100),
    department_head VARCHAR(100),
    building VARCHAR(100)
);

CREATE TABLE buildings_3nf (
    building_id INTEGER PRIMARY KEY,
    building_name VARCHAR(100),
    building_address VARCHAR(200)
);

CREATE TABLE courses_3nf (
    course_id INTEGER PRIMARY KEY,
    course_name VARCHAR(100),
    course_code VARCHAR(20),
    department_id INTEGER,
    professor_id INTEGER,
    credit_hours INTEGER,
    FOREIGN KEY (department_id) REFERENCES departments_3nf(department_id)
);
*/

-- ========================================
-- УПРАЖНЕНИЯ ДЛЯ САМОСТОЯТЕЛЬНОЙ РАБОТЫ
-- ========================================

/*
УПРАЖНЕНИЕ 1: Найдите нарушения нормализации
Проанализируйте каждую из приведенных выше таблиц и определите:
- Какие нормальные формы нарушены?
- Какие конкретно зависимости вызывают проблемы?
- Как исправить каждое нарушение?

УПРАЖНЕНИЕ 2: Создайте нормализованную схему
Спроектируйте полную нормализованную схему БД университета в 3НФ на основе денормализованных примеров.

УПРАЖНЕНИЕ 3: Миграция данных
Напишите SQL скрипты для переноса данных из денормализованных таблиц в правильно спроектированные.

УПРАЖНЕНИЕ 4: Анализ производительности
Сравните производительность запросов к денормализованным и нормализованным структурам.
*/

-- ========================================
-- КОНТРОЛЬНЫЕ ВОПРОСЫ
-- ========================================

/*
1. Почему хранение множественных значений в одной ячейке нарушает 1НФ?
2. Как частичные зависимости влияют на избыточность данных?
3. Приведите пример транзитивной зависимости из реальной жизни.
4. Когда денормализация может быть оправдана?
5. Как нормализация влияет на производительность INSERT vs SELECT операций?
*/