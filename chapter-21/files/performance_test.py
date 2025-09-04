import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

class DatabasePerformanceTester:
    """Класс для тестирования производительности базы данных с индексами"""
    
    def __init__(self, db_path='university_database.db'):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.conn.execute("PRAGMA foreign_keys = ON")
        
    def create_large_dataset(self, students_count=10000, enrollments_per_student=8):
        """Создание большого набора данных для тестирования"""
        print(f"🏗️ Создание тестового набора из {students_count} студентов...")
        
        cursor = self.conn.cursor()
        
        # Генерация студентов
        first_names = ['Александр', 'Мария', 'Дмитрий', 'Анна', 'Максим', 'Елена', 'Артем', 'Ольга', 'Никита', 'Екатерина'] * 100
        last_names = ['Иванов', 'Петров', 'Сидоров', 'Козлов', 'Морозов', 'Новиков', 'Федоров', 'Орлов', 'Попов', 'Соколов'] * 100
        
        students_data = []
        for i in range(students_count):
            student_id = 10000 + i
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            email = f"{first_name.lower()}.{last_name.lower()}{i}@test.university.edu"
            birth_date = datetime(1990, 1, 1) + timedelta(days=random.randint(0, 4000))
            enrollment_date = datetime(2018, 9, 1) + timedelta(days=random.randint(0, 1800))
            gpa = round(random.uniform(2.0, 4.0), 2)
            
            students_data.append((
                student_id, first_name, last_name, email, 
                f"+7-9{random.randint(10,99)}-{random.randint(100,999)}-{random.randint(10,99)}-{random.randint(10,99)}",
                birth_date.strftime('%Y-%m-%d'), enrollment_date.strftime('%Y-%m-%d'),
                'active', gpa, 0
            ))
        
        # Массовая вставка студентов
        cursor.executemany("""
            INSERT INTO students 
            (student_id, first_name, last_name, email, phone, birth_date, enrollment_date, status, gpa, total_credits)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, students_data)
        
        print(f"✅ Создано {len(students_data)} студентов")
        
        # Генерация записей на курсы
        cursor.execute("SELECT course_id, professor_id FROM courses")
        courses = cursor.fetchall()
        
        semesters = ['Fall', 'Spring']
        years = [2020, 2021, 2022, 2023, 2024]
        grades = ['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D', 'F']
        grade_points = {'A': 4.0, 'A-': 3.7, 'B+': 3.3, 'B': 3.0, 'B-': 2.7, 'C+': 2.3, 'C': 2.0, 'C-': 1.7, 'D': 1.0, 'F': 0.0}
        
        enrollments_data = []
        enrollment_id = 100000
        
        for student in students_data:
            student_id = student[0]
            courses_taken = random.sample(courses, min(enrollments_per_student, len(courses)))
            
            for course_id, professor_id in courses_taken:
                semester = random.choice(semesters)
                year = random.choice(years)
                grade = random.choice(grades)
                enrollment_date = datetime(year, 1 if semester == 'Spring' else 9, random.randint(1, 15))
                
                enrollments_data.append((
                    enrollment_id, student_id, course_id, professor_id,
                    semester, year, enrollment_date.strftime('%Y-%m-%d'),
                    grade, grade_points[grade], 1
                ))
                enrollment_id += 1
        
        # Массовая вставка записей на курсы (по частям для избежания ошибок памяти)
        chunk_size = 1000
        for i in range(0, len(enrollments_data), chunk_size):
            chunk = enrollments_data[i:i+chunk_size]
            try:
                cursor.executemany("""
                    INSERT OR IGNORE INTO enrollments 
                    (enrollment_id, student_id, course_id, professor_id, semester, year, enrollment_date, letter_grade, grade_points, is_completed)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, chunk)
            except sqlite3.IntegrityError:
                # Пропускаем дубликаты
                pass
        
        self.conn.commit()
        print(f"✅ Создано записей на курсы")
        
    def run_performance_tests(self):
        """Запуск тестов производительности"""
        print("\n🚀 Запуск тестов производительности...")
        
        cursor = self.conn.cursor()
        
        # Включаем измерение времени
        cursor.execute("PRAGMA timer = ON")
        
        test_queries = [
            {
                'name': 'Поиск студента по фамилии',
                'query': "SELECT * FROM students WHERE last_name = 'Иванов'",
                'index': "CREATE INDEX IF NOT EXISTS idx_student_lastname ON students(last_name)"
            },
            {
                'name': 'Список курсов студента',
                'query': """
                    SELECT s.first_name, s.last_name, c.course_name, e.letter_grade
                    FROM students s
                    JOIN enrollments e ON s.student_id = e.student_id
                    JOIN courses c ON e.course_id = c.course_id
                    WHERE s.student_id = 10500
                """,
                'index': "CREATE INDEX IF NOT EXISTS idx_enrollment_student_course ON enrollments(student_id, course_id)"
            },
            {
                'name': 'Средние оценки по курсам',
                'query': """
                    SELECT c.course_name, AVG(e.grade_points) as avg_grade, COUNT(*) as students
                    FROM courses c
                    JOIN enrollments e ON c.course_id = e.course_id
                    WHERE e.semester = 'Fall' AND e.year = 2023
                    GROUP BY c.course_name
                    ORDER BY avg_grade DESC
                """,
                'index': "CREATE INDEX IF NOT EXISTS idx_enrollment_semester_year_grade ON enrollments(semester, year, grade_points)"
            },
            {
                'name': 'Топ студентов по GPA',
                'query': """
                    SELECT first_name, last_name, gpa
                    FROM students
                    WHERE status = 'active' AND gpa >= 3.5
                    ORDER BY gpa DESC
                    LIMIT 100
                """,
                'index': "CREATE INDEX IF NOT EXISTS idx_student_status_gpa ON students(status, gpa)"
            },
            {
                'name': 'Загрузка преподавателей',
                'query': """
                    SELECT p.first_name, p.last_name, COUNT(DISTINCT e.student_id) as students_count
                    FROM professors p
                    JOIN enrollments e ON p.professor_id = e.professor_id
                    WHERE e.year = 2024
                    GROUP BY p.professor_id, p.first_name, p.last_name
                    HAVING students_count > 50
                    ORDER BY students_count DESC
                """,
                'index': "CREATE INDEX IF NOT EXISTS idx_enrollment_prof_year ON enrollments(professor_id, year)"
            }
        ]
        
        results = []
        
        for test in test_queries:
            print(f"\n📊 Тестирование: {test['name']}")
            
            # Тест без индекса (удаляем если существует)
            cursor.execute("DROP INDEX IF EXISTS " + test['index'].split()[-1])
            
            start_time = datetime.now()
            cursor.execute("EXPLAIN QUERY PLAN " + test['query'])
            plan_before = cursor.fetchall()
            
            cursor.execute(test['query'])
            rows_before = len(cursor.fetchall())
            end_time = datetime.now()
            time_before = (end_time - start_time).total_seconds()
            
            print(f"   Без индекса: {time_before:.4f} сек, {rows_before} строк")
            
            # Создаем индекс
            cursor.execute(test['index'])
            
            # Тест с индексом
            start_time = datetime.now()
            cursor.execute("EXPLAIN QUERY PLAN " + test['query'])
            plan_after = cursor.fetchall()
            
            cursor.execute(test['query'])
            rows_after = len(cursor.fetchall())
            end_time = datetime.now()
            time_after = (end_time - start_time).total_seconds()
            
            print(f"   С индексом:  {time_after:.4f} сек, {rows_after} строк")
            
            improvement = ((time_before - time_after) / time_before * 100) if time_before > 0 else 0
            print(f"   Улучшение:   {improvement:.1f}%")
            
            results.append({
                'test': test['name'],
                'time_before': time_before,
                'time_after': time_after,
                'improvement': improvement,
                'rows': rows_after
            })
        
        # Сохраняем результаты
        results_df = pd.DataFrame(results)
        results_df.to_csv('performance_test_results.csv', index=False, sep=';')
        
        return results_df
    
    def analyze_index_usage(self):
        """Анализ использования индексов"""
        print("\n🔍 Анализ использования индексов...")
        
        cursor = self.conn.cursor()
        
        # Получаем список всех индексов
        cursor.execute("""
            SELECT name, sql 
            FROM sqlite_master 
            WHERE type = 'index' 
            AND name NOT LIKE 'sqlite_autoindex%'
        """)
        
        indexes = cursor.fetchall()
        
        print(f"\n📋 Найдено индексов: {len(indexes)}")
        for name, sql in indexes:
            print(f"   • {name}")
        
        # Статистика таблиц
        cursor.execute("""
            SELECT 
                name,
                (SELECT COUNT(*) FROM sqlite_master WHERE type='index' AND tbl_name=m.name) as index_count
            FROM sqlite_master m
            WHERE type = 'table'
            AND name NOT LIKE 'sqlite_%'
        """)
        
        table_stats = cursor.fetchall()
        
        print(f"\n📊 Статистика индексов по таблицам:")
        for table, idx_count in table_stats:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            row_count = cursor.fetchone()[0]
            print(f"   {table}: {row_count:,} строк, {idx_count} индексов")
    
    def generate_recommendations(self):
        """Генерация рекомендаций по оптимизации"""
        print("\n💡 Рекомендации по оптимизации:")
        
        cursor = self.conn.cursor()
        
        # Анализ больших таблиц без индексов
        cursor.execute("""
            SELECT name
            FROM sqlite_master 
            WHERE type = 'table' 
            AND name NOT LIKE 'sqlite_%'
        """)
        
        tables = cursor.fetchall()
        
        for (table,) in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            row_count = cursor.fetchone()[0]
            
            cursor.execute(f"""
                SELECT COUNT(*) 
                FROM sqlite_master 
                WHERE type = 'index' 
                AND tbl_name = '{table}'
                AND name NOT LIKE 'sqlite_autoindex%'
            """)
            index_count = cursor.fetchone()[0]
            
            if row_count > 1000 and index_count < 2:
                print(f"   ⚠️ Таблица {table} ({row_count:,} строк) имеет мало индексов ({index_count})")
        
        print(f"\n✅ Общие рекомендации:")
        print(f"   • Создавайте индексы на столбцы в WHERE условиях")
        print(f"   • Используйте составные индексы для часто используемых комбинаций")
        print(f"   • Мониторьте размер индексов vs улучшение производительности")
        print(f"   • Регулярно обновляйте статистику: ANALYZE")
    
    def cleanup_test_data(self):
        """Очистка тестовых данных"""
        print("\n🧹 Очистка тестовых данных...")
        
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM enrollments WHERE enrollment_id >= 100000")
        cursor.execute("DELETE FROM students WHERE student_id >= 10000")
        self.conn.commit()
        
        print("✅ Тестовые данные удалены")
    
    def close(self):
        """Закрытие подключения"""
        self.conn.close()

def main():
    """Основная функция для запуска тестирования производительности"""
    print("⚡ СИСТЕМА ТЕСТИРОВАНИЯ ПРОИЗВОДИТЕЛЬНОСТИ БД")
    print("="*60)
    
    tester = DatabasePerformanceTester()
    
    try:
        # Создание большого набора данных
        tester.create_large_dataset(students_count=5000, enrollments_per_student=6)
        
        # Запуск тестов производительности
        results = tester.run_performance_tests()
        
        # Анализ использования индексов
        tester.analyze_index_usage()
        
        # Генерация рекомендаций
        tester.generate_recommendations()
        
        # Вывод итоговых результатов
        print(f"\n📊 ИТОГОВЫЕ РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ:")
        print("="*50)
        avg_improvement = results['improvement'].mean()
        best_improvement = results.loc[results['improvement'].idxmax()]
        
        print(f"Среднее улучшение производительности: {avg_improvement:.1f}%")
        print(f"Лучший результат: {best_improvement['test']} - {best_improvement['improvement']:.1f}%")
        
        # Очистка тестовых данных
        response = input("\nУдалить тестовые данные? (y/n): ")
        if response.lower() == 'y':
            tester.cleanup_test_data()
        
    except Exception as e:
        print(f"❌ Ошибка тестирования: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        tester.close()

if __name__ == "__main__":
    main()