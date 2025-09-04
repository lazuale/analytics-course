# 📝 Практические задания — Глава 21

📖 [Вернуться к теории](../README.md) | 📁 [Учебные файлы](../files/README.md) | ✅ [Чек-лист](../checklist.md)

---

## 🎯 Задание 1: Проектирование реляционной модели данных

### 📊 Описание
Спроектируйте полную реляционную модель данных для системы управления университетом. Создайте все необходимые таблицы, определите связи и примените нормализацию.

### 🔧 Что нужно сделать

**1️⃣ Создание основных таблиц с правильными типами данных**

```sql
-- Создайте таблицы для университетской системы
-- Используйте файл files/university_schema.sql как основу

-- Студенты
CREATE TABLE students (
    student_id INTEGER PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(20),
    birth_date DATE,
    enrollment_date DATE DEFAULT CURRENT_DATE,
    status VARCHAR(20) CHECK (status IN ('active', 'graduated', 'suspended'))
);

-- Преподаватели  
CREATE TABLE professors (
    professor_id INTEGER PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE,
    department_id INTEGER,
    hire_date DATE,
    salary DECIMAL(10,2) CHECK (salary > 0),
    title VARCHAR(50)
);

-- Факультеты
CREATE TABLE departments (
    department_id INTEGER PRIMARY KEY,
    department_name VARCHAR(100) NOT NULL,
    building VARCHAR(50),
    phone VARCHAR(20),
    head_professor_id INTEGER
);
```

**2️⃣ Определение связей между таблицами**

```sql
-- Добавьте внешние ключи для создания связей
-- Проанализируйте типы связей (1:1, 1:N, M:N)

-- Связь преподавателя с факультетом (многие к одному)
ALTER TABLE professors 
ADD CONSTRAINT fk_professor_department 
FOREIGN KEY (department_id) REFERENCES departments(department_id);

-- Связь заведующего кафедрой (один к одному)  
ALTER TABLE departments 
ADD CONSTRAINT fk_department_head 
FOREIGN KEY (head_professor_id) REFERENCES professors(professor_id);

-- Создайте промежуточную таблицу для связи многие-ко-многим
CREATE TABLE course_enrollments (
    enrollment_id INTEGER PRIMARY KEY,
    student_id INTEGER,
    course_id INTEGER,
    professor_id INTEGER,
    semester VARCHAR(20),
    year INTEGER,
    grade DECIMAL(3,2) CHECK (grade >= 0 AND grade <= 4.0),
    enrollment_date DATE DEFAULT CURRENT_DATE,
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id),
    FOREIGN KEY (professor_id) REFERENCES professors(professor_id)
);
```

**3️⃣ Применение нормализации**

```sql
-- Приведите структуру к 3НФ
-- Исправьте нарушения нормальных форм в файле files/denormalized_data.sql

-- До нормализации (нарушения 2НФ и 3НФ)
-- student_courses (student_id, course_id, student_name, professor_name, department_name)

-- После нормализации (3НФ)
-- Разделите данные на правильные таблицы с устранением избыточности
```

### 📋 Файлы для работы
- `files/university_schema.sql` — базовая структура схемы
- `files/denormalized_data.sql` — данные для нормализации
- `files/university_sample_data.csv` — примеры данных для заполнения

### 🎯 Ожидаемый результат
- Корректная реляционная модель в 3НФ
- Все связи между таблицами определены через внешние ключи
- Применены ограничения целостности данных

---

## ⚡ Задание 2: Создание и оптимизация индексов

### 📊 Описание
Проанализируйте производительность запросов к университетской базе данных и создайте оптимальные индексы для ускорения операций поиска и сортировки.

### 🔧 Что нужно сделать

**1️⃣ Анализ медленных запросов**

```sql
-- Проанализируйте план выполнения запросов
-- Используйте EXPLAIN для анализа производительности

-- Запрос 1: Поиск студентов по фамилии
EXPLAIN QUERY PLAN
SELECT * FROM students 
WHERE last_name = 'Иванов';

-- Запрос 2: Список курсов студента
EXPLAIN QUERY PLAN  
SELECT s.first_name, s.last_name, c.course_name, ce.grade
FROM students s
JOIN course_enrollments ce ON s.student_id = ce.student_id
JOIN courses c ON ce.course_id = c.course_id
WHERE s.student_id = 12345;

-- Запрос 3: Средние оценки по курсам
EXPLAIN QUERY PLAN
SELECT c.course_name, AVG(ce.grade) as avg_grade
FROM courses c
JOIN course_enrollments ce ON c.course_id = ce.course_id
WHERE ce.semester = 'Fall' AND ce.year = 2024
GROUP BY c.course_name
ORDER BY avg_grade DESC;
```

**2️⃣ Создание оптимальных индексов**

```sql
-- Создайте индексы для ускорения частых операций

-- Индекс для поиска по фамилии студентов
CREATE INDEX idx_students_last_name ON students(last_name);

-- Составной индекс для поиска по имени и фамилии
CREATE INDEX idx_students_full_name ON students(last_name, first_name);

-- Индекс для JOIN операций
CREATE INDEX idx_enrollments_student_id ON course_enrollments(student_id);
CREATE INDEX idx_enrollments_course_id ON course_enrollments(course_id);

-- Составной индекс для фильтрации по семестру и году
CREATE INDEX idx_enrollments_semester_year ON course_enrollments(semester, year);

-- Индекс для сортировки по оценкам
CREATE INDEX idx_enrollments_grade ON course_enrollments(grade);
```

**3️⃣ Тестирование производительности**

```sql
-- Сравните производительность до и после создания индексов
-- Используйте файл files/performance_test.sql

-- Тест 1: Время выполнения поиска без индекса
.timer on
SELECT * FROM students WHERE last_name = 'Петров';

-- Создайте индекс и повторите тест
CREATE INDEX idx_students_lastname ON students(last_name);
SELECT * FROM students WHERE last_name = 'Петров';

-- Тест 2: Сложный JOIN запрос
SELECT 
    s.first_name, 
    s.last_name,
    COUNT(ce.course_id) as courses_count,
    AVG(ce.grade) as avg_grade
FROM students s
LEFT JOIN course_enrollments ce ON s.student_id = ce.student_id
GROUP BY s.student_id, s.first_name, s.last_name
HAVING COUNT(ce.course_id) > 5
ORDER BY avg_grade DESC;
```

**4️⃣ Мониторинг использования индексов**

```sql
-- Проверьте, какие индексы используются запросами
-- Удалите неиспользуемые индексы

-- Анализ статистики индексов (PostgreSQL)
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan,  -- количество использований
    idx_tup_read,
    idx_tup_fetch
FROM pg_stat_user_indexes 
ORDER BY idx_scan DESC;

-- Поиск неиспользуемых индексов
SELECT 
    schemaname,
    tablename,
    indexname
FROM pg_stat_user_indexes 
WHERE idx_scan = 0;
```

### 🎯 Ожидаемый результат
- Создана оптимальная система индексов
- Значительно улучшена производительность запросов
- Понимание компромиссов между скоростью чтения и записи

---

## 🎨 Задание 3: Построение модели данных в Power Pivot

### 📊 Описание
Создайте аналитическую модель данных в Power Pivot для анализа успеваемости студентов и эффективности курсов в университете.

### 🔧 Что нужно сделать

**1️⃣ Импорт данных в Power Pivot**

```excel
' Откройте файл files/university_analytics.xlsx
' Перейдите в Power Pivot -> Управление данными

' Импортируйте таблицы из разных источников:
' - students_data.csv
' - courses_data.csv  
' - enrollments_data.csv
' - professors_data.csv
' - departments_data.csv

' Настройте типы данных для каждого столбца
```

**2️⃣ Создание связей между таблицами**

```dax
// В окне диаграммы Power Pivot создайте связи:

// students (1) -> enrollments (много)
// Связь: students[student_id] -> enrollments[student_id]

// courses (1) -> enrollments (много)  
// Связь: courses[course_id] -> enrollments[course_id]

// professors (1) -> enrollments (много)
// Связь: professors[professor_id] -> enrollments[professor_id]

// departments (1) -> professors (много)
// Связь: departments[department_id] -> professors[department_id]

// Убедитесь, что все связи имеют правильное направление фильтрации
```

**3️⃣ Создание календарной таблицы**

```dax
// Создайте календарную таблицу для временного анализа
Calendar = 
ADDCOLUMNS(
    CALENDAR(DATE(2020,1,1), DATE(2025,12,31)),
    "Year", YEAR([Date]),
    "Month", MONTH([Date]),
    "MonthName", FORMAT([Date], "mmmm"),
    "Quarter", "Q" & ROUNDUP(MONTH([Date])/3, 0),
    "Semester", IF(MONTH([Date]) <= 6, "Spring", "Fall"),
    "AcademicYear", 
        IF(MONTH([Date]) >= 9, 
           YEAR([Date]) & "/" & (YEAR([Date]) + 1),
           (YEAR([Date]) - 1) & "/" & YEAR([Date])
        )
)

// Создайте связь Calendar[Date] -> enrollments[enrollment_date]
```

**4️⃣ Создание вычисляемых столбцов**

```dax
// Добавьте вычисляемые столбцы в таблицы

// В таблице students:
[Age] = DATEDIFF(students[birth_date], TODAY(), YEAR)

[Years Enrolled] = DATEDIFF(students[enrollment_date], TODAY(), YEAR)

// В таблице enrollments:
[Grade Point] = 
SWITCH(
    enrollments[letter_grade],
    "A", 4.0,
    "A-", 3.7,
    "B+", 3.3,
    "B", 3.0,
    "B-", 2.7,
    "C+", 2.3,
    "C", 2.0,
    "C-", 1.7,
    "D", 1.0,
    "F", 0.0,
    BLANK()
)

[Pass/Fail] = IF(enrollments[Grade Point] >= 2.0, "Pass", "Fail")

// В таблице courses:
[Credit Hours Category] = 
IF(courses[credit_hours] >= 4, "High Credit", 
   IF(courses[credit_hours] >= 2, "Medium Credit", "Low Credit"))
```

**5️⃣ Создание аналитических мер**

```dax
// Основные метрики успеваемости

Total Students = DISTINCTCOUNT(enrollments[student_id])

Total Enrollments = COUNT(enrollments[enrollment_id])

Average GPA = AVERAGE(enrollments[Grade Point])

Pass Rate = 
DIVIDE(
    COUNTROWS(FILTER(enrollments, enrollments[Pass/Fail] = "Pass")),
    COUNTROWS(enrollments),
    0
)

// Сравнительные метрики

GPA vs Department Average = 
VAR DeptAvgGPA = 
    CALCULATE(
        [Average GPA],
        ALLEXCEPT(enrollments, professors[department_id])
    )
RETURN
    [Average GPA] - DeptAvgGPA

Student Retention Rate = 
VAR StudentsThisSemester = [Total Students]
VAR StudentsPrevSemester = 
    CALCULATE(
        [Total Students],
        DATEADD(Calendar[Date], -6, MONTH)
    )
RETURN
    DIVIDE(StudentsThisSemester, StudentsPrevSemester, 0)

// Ранжирующие меры

Professor Ranking by Student Performance = 
RANKX(
    ALL(professors[professor_name]),
    [Average GPA],
    ,
    DESC
)

Top Performing Courses = 
CALCULATE(
    [Average GPA],
    TOPN(10, courses, [Average GPA], DESC)
)
```

### 📋 Файлы для работы
- `files/university_analytics.xlsx` — Power Pivot файл
- `files/students_data.csv` — данные студентов
- `files/courses_data.csv` — данные курсов
- `files/enrollments_data.csv` — данные записей на курсы
- `files/professors_data.csv` — данные преподавателей

### 🎯 Ожидаемый результат
- Полная аналитическая модель данных в Power Pivot
- Корректно настроенные связи между всеми таблицами
- Набор полезных мер для анализа успеваемости

---

## 🔍 Задание 4: Создание ER-диаграммы и документации

### 📊 Описание
Создайте профессиональную документацию модели данных, включая ER-диаграмму, описание бизнес-правил и рекомендации по использованию.

### 🔧 Что нужно сделать

**1️⃣ Построение ER-диаграммы**

```
// Используйте инструмент для создания диаграмм (например, draw.io, Lucidchart)
// Создайте полную ER-диаграмму со всеми элементами:

Сущности (прямоугольники):
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│    СТУДЕНТ      │    │   ПРЕПОДАВАТЕЛЬ  │    │    ФАКУЛЬТЕТ    │
├─────────────────┤    ├─────────────────┤    ├─────────────────┤
│ student_id (PK) │    │ professor_id(PK)│    │ department_id(PK│
│ first_name      │    │ first_name      │    │ department_name │
│ last_name       │    │ last_name       │    │ building        │
│ email           │    │ email           │    │ head_prof_id(FK)│
│ enrollment_date │    │ hire_date       │    │ phone           │
└─────────────────┘    └─────────────────┘    └─────────────────┘

Связи (ромбы с кардинальностью):
СТУДЕНТ ──┤1    N├── ЗАПИСЫВАЕТСЯ ──┤N    M├── КУРС
ПРЕПОДАВАТЕЛЬ ──┤1    N├── ВЕДЕТ ──┤N    1├── КУРС  
ФАКУЛЬТЕТ ──┤1    N├── ВКЛЮЧАЕТ ──┤N    1├── ПРЕПОДАВАТЕЛЬ
```

**2️⃣ Документирование бизнес-правил**

```markdown
# Бизнес-правила университетской системы

## Правила для студентов:
1. Каждый студент должен иметь уникальный email
2. Студент может записаться на несколько курсов в семестре
3. Максимальное количество кредитных часов в семестре: 18
4. Минимальная оценка для зачета курса: 2.0 (C-)

## Правила для преподавателей:
1. Преподаватель принадлежит только одному факультету
2. Преподаватель может вести несколько курсов
3. У каждого факультета есть один заведующий кафедрой
4. Заведующий кафедрой должен быть преподавателем этого факультета

## Правила для курсов:
1. Каждый курс имеет фиксированное количество кредитных часов
2. Курс ведется одним основным преподавателем
3. Оценки выставляются по шкале от 0.0 до 4.0
4. Пререквизиты курса должны быть выполнены перед записью
```

**3️⃣ Создание словаря данных**

```sql
-- Создайте подробное описание каждой таблицы и столбца
-- Используйте комментарии SQL для документирования

-- Таблица студентов
COMMENT ON TABLE students IS 
'Основная таблица с информацией о студентах университета';

COMMENT ON COLUMN students.student_id IS 
'Уникальный идентификатор студента. Автоинкремент. Первичный ключ.';

COMMENT ON COLUMN students.email IS 
'Электронная почта студента. Должна быть уникальной в системе.';

COMMENT ON COLUMN students.status IS 
'Текущий статус студента: active, graduated, suspended, transferred';

-- Создайте аналогичные комментарии для всех таблиц
-- Документируйте все ограничения и бизнес-правила
```

**4️⃣ Создание руководства пользователя**

Создайте файл `files/database_user_guide.md` с инструкциями:

```markdown
# Руководство пользователя базы данных университета

## Часто используемые запросы

### 1. Найти всех студентов курса
```sql
SELECT s.first_name, s.last_name, s.email
FROM students s
JOIN course_enrollments ce ON s.student_id = ce.student_id  
WHERE ce.course_id = :course_id
  AND ce.semester = :semester
  AND ce.year = :year;
```

### 2. Рассчитать GPA студента
```sql
SELECT 
    s.first_name,
    s.last_name,
    ROUND(AVG(ce.grade), 2) as gpa
FROM students s
JOIN course_enrollments ce ON s.student_id = ce.student_id
WHERE s.student_id = :student_id
GROUP BY s.student_id, s.first_name, s.last_name;
```

## Рекомендации по производительности
- Всегда используйте индексы на student_id при JOIN операциях
- Добавляйте фильтры по семестру и году для ограничения результатов
- Используйте LIMIT для ограничения больших результатов
```

### 🎯 Ожидаемый результат
- Профессиональная ER-диаграмма
- Полная документация модели данных
- Руководство пользователя с примерами запросов

---

## 🔄 Задание 5: Интеграция SQL и Power Pivot

### 📊 Описание
Создайте интегрированное решение, которое использует SQL для подготовки данных и Power Pivot для создания интерактивной аналитической панели.

### 🔧 Что нужно сделать

**1️⃣ Создание аналитических представлений в SQL**

```sql
-- Создайте представления для различных аналитических задач
-- Используйте файл files/analytical_views.sql

-- Представление для анализа успеваемости студентов
CREATE VIEW student_performance_summary AS
SELECT 
    s.student_id,
    s.first_name,
    s.last_name,
    s.enrollment_date,
    d.department_name,
    COUNT(ce.course_id) as courses_taken,
    AVG(ce.grade) as gpa,
    SUM(c.credit_hours) as total_credits,
    CASE 
        WHEN AVG(ce.grade) >= 3.7 THEN 'Honors'
        WHEN AVG(ce.grade) >= 3.0 THEN 'Good Standing'
        WHEN AVG(ce.grade) >= 2.0 THEN 'Satisfactory'
        ELSE 'Probation'
    END as academic_status
FROM students s
LEFT JOIN course_enrollments ce ON s.student_id = ce.student_id
LEFT JOIN courses c ON ce.course_id = c.course_id
LEFT JOIN professors p ON ce.professor_id = p.professor_id
LEFT JOIN departments d ON p.department_id = d.department_id
GROUP BY s.student_id, s.first_name, s.last_name, s.enrollment_date, d.department_name;

-- Представление для анализа эффективности преподавателей
CREATE VIEW professor_effectiveness AS
SELECT 
    p.professor_id,
    p.first_name,
    p.last_name,
    d.department_name,
    COUNT(DISTINCT ce.student_id) as students_taught,
    COUNT(DISTINCT ce.course_id) as courses_taught,
    AVG(ce.grade) as avg_student_grade,
    SUM(CASE WHEN ce.grade >= 2.0 THEN 1 ELSE 0 END) * 100.0 / COUNT(ce.grade) as pass_rate,
    COUNT(ce.enrollment_id) as total_enrollments
FROM professors p
JOIN departments d ON p.department_id = d.department_id
LEFT JOIN course_enrollments ce ON p.professor_id = ce.professor_id
GROUP BY p.professor_id, p.first_name, p.last_name, d.department_name;

-- Представление для трендового анализа
CREATE VIEW enrollment_trends AS
SELECT 
    ce.year,
    ce.semester,
    d.department_name,
    COUNT(DISTINCT ce.student_id) as student_count,
    COUNT(ce.enrollment_id) as enrollment_count,
    AVG(ce.grade) as avg_grade,
    SUM(c.credit_hours) as total_credit_hours
FROM course_enrollments ce
JOIN courses c ON ce.course_id = c.course_id
JOIN professors p ON ce.professor_id = p.professor_id
JOIN departments d ON p.department_id = d.department_id
GROUP BY ce.year, ce.semester, d.department_name;
```

**2️⃣ Подключение SQL данных к Power Pivot**

```dax
// В Power Pivot подключитесь к SQL базе данных
// Импортируйте созданные представления

// Настройте автоматическое обновление данных
// Data -> Connections -> Properties -> Refresh every X minutes

// Создайте связи между импортированными представлениями
// student_performance_summary -> enrollment_trends (по department_name)
// professor_effectiveness -> enrollment_trends (по department_name)
```

**3️⃣ Создание KPI и аналитических мер**

```dax
// Ключевые показатели эффективности

// Общие метрики
Total Students = DISTINCTCOUNT(student_performance_summary[student_id])

Average University GPA = AVERAGE(student_performance_summary[gpa])

Retention Rate = 
VAR CurrentYearStudents = 
    CALCULATE([Total Students], enrollment_trends[year] = MAX(enrollment_trends[year]))
VAR PreviousYearStudents = 
    CALCULATE([Total Students], enrollment_trends[year] = MAX(enrollment_trends[year]) - 1)
RETURN
    DIVIDE(CurrentYearStudents, PreviousYearStudents, 0) - 1

// Метрики качества обучения
High Performers Percentage = 
VAR HighPerformers = 
    COUNTROWS(
        FILTER(
            student_performance_summary,
            student_performance_summary[academic_status] = "Honors"
        )
    )
RETURN
    DIVIDE(HighPerformers, [Total Students], 0)

At Risk Students = 
COUNTROWS(
    FILTER(
        student_performance_summary,
        student_performance_summary[academic_status] = "Probation"
    )
)

// Департментские сравнения
Department Ranking by GPA = 
RANKX(
    ALL(student_performance_summary[department_name]),
    CALCULATE(AVERAGE(student_performance_summary[gpa])),
    ,
    DESC
)

Best Performing Department = 
CALCULATE(
    VALUES(student_performance_summary[department_name]),
    TOPN(1, 
         ALL(student_performance_summary[department_name]),
         CALCULATE(AVERAGE(student_performance_summary[gpa])),
         DESC)
)
```

**4️⃣ Создание интерактивного дашборда**

```excel
' Создайте сводную таблицу со следующими элементами:

' Фильтры:
' - Год (слайсер)
' - Семестр (слайсер)  
' - Факультет (слайсер)

' Основные KPI (карточки):
' - Общее количество студентов
' - Средний GPA по университету
' - Процент отличников
' - Количество студентов в группе риска

' Диаграммы:
' 1. Столбчатая диаграмма: GPA по факультетам
' 2. Линейная диаграмма: Тренд поступлений по годам
' 3. Круговая диаграмма: Распределение студентов по статусам
' 4. Тепловая карта: Успеваемость по курсам и семестрам

' Детализированные таблицы:
' - Топ-10 студентов по GPA
' - Рейтинг преподавателей по эффективности
' - Курсы с наименьшим процентом прохождения
```

**5️⃣ Автоматизация обновления данных**

```python
# Создайте Python скрипт для автоматического обновления
# Используйте файл files/data_refresh_automation.py

import pyodbc
import pandas as pd
from datetime import datetime
import win32com.client

def refresh_power_pivot_data():
    """Обновление данных в Power Pivot модели"""
    
    # Подключение к Excel файлу с Power Pivot
    excel = win32com.client.Dispatch("Excel.Application")
    workbook = excel.Workbooks.Open(r"C:\path\to\university_analytics.xlsx")
    
    # Обновление всех подключений к данным
    workbook.RefreshAll()
    
    # Сохранение изменений
    workbook.Save()
    workbook.Close()
    excel.Quit()
    
    print(f"Данные обновлены: {datetime.now()}")

def update_sql_views():
    """Обновление SQL представлений с новыми данными"""
    
    conn = pyodbc.connect('DRIVER={SQL Server};SERVER=server;DATABASE=university_db')
    
    # SQL скрипт для обновления агрегированных таблиц
    refresh_script = """
    -- Обновление материализованных представлений
    EXEC sp_refreshview 'student_performance_summary';
    EXEC sp_refreshview 'professor_effectiveness';  
    EXEC sp_refreshview 'enrollment_trends';
    
    -- Обновление статистик для оптимизации
    UPDATE STATISTICS student_performance_summary;
    UPDATE STATISTICS professor_effectiveness;
    UPDATE STATISTICS enrollment_trends;
    """
    
    cursor = conn.cursor()
    cursor.execute(refresh_script)
    conn.commit()
    conn.close()
    
    print("SQL представления обновлены")

if __name__ == "__main__":
    update_sql_views()
    refresh_power_pivot_data()
```

### 📋 Файлы для работы
- `files/analytical_views.sql` — SQL представления
- `files/university_dashboard.xlsx` — Power Pivot дашборд
- `files/data_refresh_automation.py` — автоматизация обновления
- `files/dashboard_requirements.md` — требования к дашборду

### 🎯 Ожидаемый результат
- Интегрированное решение SQL + Power Pivot
- Автоматизированное обновление данных
- Интерактивный аналитический дашборд

---

- 🔙 [Предыдущая глава: Глава 20 - SQL: JOIN и подзапросы](../chapter-20/README.md)
- 🔜 [Следующая глава: Глава 22: Оптимизация SQL-запросов](../chapter-22/README.md)

---

- 📢 Присоединяйтесь к чату курса: https://t.me/analytics_course_chat
- 📢 Канал курса: https://t.me/analytics_course_channel