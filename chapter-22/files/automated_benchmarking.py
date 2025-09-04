"""
Система автоматизированного тестирования производительности SQL-запросов
Сравнение производительности до и после применения индексов и оптимизаций
"""

import sqlite3
import time
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os

class PerformanceBenchmark:
    """Класс для автоматизированного тестирования производительности SQL"""
    
    def __init__(self, db_path='ecommerce_performance.db'):
        """
        Инициализация системы тестирования
        
        Args:
            db_path (str): Путь к базе данных SQLite
        """
        self.db_path = db_path
        self.test_queries = []
        self.baseline_results = []
        self.optimized_results = []
        
    def add_test_query(self, name, query, description=""):
        """
        Добавление тестового запроса
        
        Args:
            name (str): Название теста
            query (str): SQL запрос для тестирования
            description (str): Описание что тестирует запрос
        """
        self.test_queries.append({
            'name': name,
            'query': query,
            'description': description
        })
        
    def measure_query_performance(self, query, iterations=3):
        """
        Измерение производительности одного запроса
        
        Args:
            query (str): SQL запрос
            iterations (int): Количество повторений для усреднения
            
        Returns:
            dict: Результаты измерения
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        times = []
        row_counts = []
        
        for i in range(iterations):
            start_time = time.time()
            cursor.execute(query)
            rows = cursor.fetchall()
            end_time = time.time()
            
            execution_time_ms = (end_time - start_time) * 1000
            times.append(execution_time_ms)
            row_counts.append(len(rows))
        
        conn.close()
        
        return {
            'avg_time_ms': sum(times) / len(times),
            'min_time_ms': min(times),
            'max_time_ms': max(times),
            'rows_returned': row_counts[0],  # Должно быть одинаково
            'iterations': iterations
        }
    
    def get_query_plan(self, query):
        """
        Получение плана выполнения запроса
        
        Args:
            query (str): SQL запрос
            
        Returns:
            list: План выполнения
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(f"EXPLAIN QUERY PLAN {query}")
        plan = cursor.fetchall()
        
        conn.close()
        return plan
    
    def run_baseline_tests(self):
        """Выполнение базового тестирования без индексов"""
        print("🚀 Запуск базового тестирования (без индексов)...")
        
        # Убеждаемся, что индексы удалены
        self.remove_all_indexes()
        
        self.baseline_results = []
        
        for test in self.test_queries:
            print(f"   Тестирование: {test['name']}")
            
            # Измерение производительности
            performance = self.measure_query_performance(test['query'])
            
            # Получение плана выполнения
            plan = self.get_query_plan(test['query'])
            
            result = {
                'name': test['name'],
                'description': test['description'],
                'performance': performance,
                'query_plan': plan,
                'query': test['query']
            }
            
            self.baseline_results.append(result)
            
            print(f"      Время: {performance['avg_time_ms']:.2f}ms, Строк: {performance['rows_returned']}")
        
        print(f"✅ Базовое тестирование завершено ({len(self.baseline_results)} тестов)")
    
    def apply_optimizations(self):
        """Применение оптимизаций (создание индексов)"""
        print("🔧 Применение оптимизаций...")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Чтение и выполнение скрипта создания индексов
        try:
            with open('index_creation_script.sql', 'r', encoding='utf-8') as f:
                index_script = f.read()
            
            # Разделение на отдельные команды (простая реализация)
            commands = [cmd.strip() for cmd in index_script.split(';') if cmd.strip() and not cmd.strip().startswith('--')]
            
            created_indexes = 0
            for command in commands:
                if 'CREATE INDEX' in command.upper():
                    try:
                        cursor.execute(command)
                        created_indexes += 1
                    except sqlite3.Error as e:
                        print(f"      Предупреждение: {e}")
            
            conn.commit()
            print(f"   Создано индексов: {created_indexes}")
            
        except FileNotFoundError:
            print("   Файл index_creation_script.sql не найден, создаем базовые индексы...")
            
            # Базовые индексы если файл не найден
            basic_indexes = [
                "CREATE INDEX IF NOT EXISTS idx_customers_email ON customers(email)",
                "CREATE INDEX IF NOT EXISTS idx_orders_customer_id ON orders(customer_id)",
                "CREATE INDEX IF NOT EXISTS idx_orders_date ON orders(order_date)",
                "CREATE INDEX IF NOT EXISTS idx_order_items_order_id ON order_items(order_id)",
                "CREATE INDEX IF NOT EXISTS idx_order_items_product_id ON order_items(product_id)"
            ]
            
            for index_sql in basic_indexes:
                cursor.execute(index_sql)
            
            conn.commit()
            print(f"   Создано базовых индексов: {len(basic_indexes)}")
        
        conn.close()
        print("✅ Оптимизации применены")
    
    def run_optimized_tests(self):
        """Выполнение тестирования с оптимизациями"""
        print("🚀 Запуск оптимизированного тестирования (с индексами)...")
        
        self.optimized_results = []
        
        for i, test in enumerate(self.test_queries):
            print(f"   Тестирование: {test['name']}")
            
            # Измерение производительности
            performance = self.measure_query_performance(test['query'])
            
            # Получение плана выполнения
            plan = self.get_query_plan(test['query'])
            
            result = {
                'name': test['name'],
                'description': test['description'],
                'performance': performance,
                'query_plan': plan,
                'query': test['query']
            }
            
            self.optimized_results.append(result)
            
            # Сравнение с baseline
            baseline_time = self.baseline_results[i]['performance']['avg_time_ms']
            improvement = ((baseline_time - performance['avg_time_ms']) / baseline_time) * 100
            
            print(f"      Время: {performance['avg_time_ms']:.2f}ms, Улучшение: {improvement:.1f}%")
        
        print(f"✅ Оптимизированное тестирование завершено ({len(self.optimized_results)} тестов)")
    
    def remove_all_indexes(self):
        """Удаление всех пользовательских индексов"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Получение списка всех индексов
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type = 'index' 
            AND name NOT LIKE 'sqlite_autoindex%'
        """)
        
        indexes = cursor.fetchall()
        
        # Удаление каждого индекса
        for (index_name,) in indexes:
            try:
                cursor.execute(f"DROP INDEX IF EXISTS {index_name}")
            except sqlite3.Error:
                pass
        
        conn.commit()
        conn.close()
        
        print(f"   Удалено индексов: {len(indexes)}")
    
    def generate_comparison_report(self):
        """Генерация отчета сравнения производительности"""
        if not self.baseline_results or not self.optimized_results:
            print("❌ Недостаточно данных для генерации отчета")
            return
        
        print("📊 Генерация отчета сравнения...")
        
        # Подготовка данных для отчета
        comparison_data = []
        
        for i, test_name in enumerate([r['name'] for r in self.baseline_results]):
            baseline_time = self.baseline_results[i]['performance']['avg_time_ms']
            optimized_time = self.optimized_results[i]['performance']['avg_time_ms']
            improvement = ((baseline_time - optimized_time) / baseline_time) * 100
            speedup = baseline_time / optimized_time if optimized_time > 0 else float('inf')
            
            comparison_data.append({
                'Тест': test_name,
                'Время без индексов (мс)': round(baseline_time, 2),
                'Время с индексами (мс)': round(optimized_time, 2),
                'Улучшение (%)': round(improvement, 1),
                'Ускорение (раз)': round(speedup, 1),
                'Строк': self.baseline_results[i]['performance']['rows_returned']
            })
        
        # Создание DataFrame и сохранение в CSV
        df = pd.DataFrame(comparison_data)
        df.to_csv('performance_comparison_results.csv', index=False, encoding='utf-8-sig')
        
        # Вывод результатов в консоль
        print("\n" + "="*80)
        print("📈 РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ ПРОИЗВОДИТЕЛЬНОСТИ")
        print("="*80)
        print(df.to_string(index=False))
        
        # Статистика
        avg_improvement = df['Улучшение (%)'].mean()
        max_improvement = df['Улучшение (%)'].max()
        avg_speedup = df['Ускорение (раз)'].mean()
        
        print(f"\n📊 Общая статистика:")
        print(f"   Среднее улучшение: {avg_improvement:.1f}%")
        print(f"   Максимальное улучшение: {max_improvement:.1f}%")
        print(f"   Среднее ускорение: {avg_speedup:.1f} раз")
        
        print(f"\n📁 Результаты сохранены в: performance_comparison_results.csv")
        
        # Создание графика
        self.create_performance_chart(df)
    
    def create_performance_chart(self, df):
        """Создание графика сравнения производительности"""
        plt.figure(figsize=(12, 8))
        
        # График времени выполнения
        plt.subplot(2, 1, 1)
        x = range(len(df))
        plt.bar([i-0.2 for i in x], df['Время без индексов (мс)'], 0.4, label='Без индексов', color='red', alpha=0.7)
        plt.bar([i+0.2 for i in x], df['Время с индексами (мс)'], 0.4, label='С индексами', color='green', alpha=0.7)
        
        plt.xlabel('Тесты')
        plt.ylabel('Время выполнения (мс)')
        plt.title('Сравнение времени выполнения запросов')
        plt.xticks(x, df['Тест'], rotation=45, ha='right')
        plt.legend()
        plt.yscale('log')  # Логарифмическая шкала для больших различий
        
        # График улучшений
        plt.subplot(2, 1, 2)
        plt.bar(x, df['Улучшение (%)'], color='blue', alpha=0.7)
        plt.xlabel('Тесты')
        plt.ylabel('Улучшение (%)')
        plt.title('Процент улучшения производительности')
        plt.xticks(x, df['Тест'], rotation=45, ha='right')
        
        # Добавление значений на столбцы
        for i, v in enumerate(df['Улучшение (%)']):
            plt.text(i, v + 1, f'{v:.1f}%', ha='center', va='bottom')
        
        plt.tight_layout()
        plt.savefig('performance_comparison_chart.png', dpi=300, bbox_inches='tight')
        print(f"📊 График сохранен в: performance_comparison_chart.png")
    
    def run_full_benchmark(self):
        """Запуск полного цикла тестирования"""
        print("🎯 Запуск полного тестирования производительности")
        print("="*60)
        
        start_time = datetime.now()
        
        # Полный цикл тестирования
        self.run_baseline_tests()
        self.apply_optimizations()
        self.run_optimized_tests()
        self.generate_comparison_report()
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        print(f"\n🏁 Тестирование завершено за {duration:.1f} секунд")
        print(f"📅 Время: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")

def main():
    """Основная функция для запуска тестирования"""
    
    # Создание экземпляра тестера
    benchmark = PerformanceBenchmark()
    
    # Добавление тестовых запросов
    benchmark.add_test_query(
        "Поиск по email",
        "SELECT customer_id, customer_name FROM customers WHERE email = 'customer1@gmail.com'",
        "Тестирование поиска по уникальному значению"
    )
    
    benchmark.add_test_query(
        "JOIN клиентов и заказов",
        """SELECT c.customer_name, COUNT(o.order_id) as order_count
           FROM customers c
           LEFT JOIN orders o ON c.customer_id = o.customer_id
           GROUP BY c.customer_id, c.customer_name
           ORDER BY order_count DESC LIMIT 10""",
        "Тестирование JOIN операции с агрегацией"
    )
    
    benchmark.add_test_query(
        "Фильтрация по дате",
        "SELECT COUNT(*) FROM orders WHERE order_date >= '2024-01-01'",
        "Тестирование фильтрации по дате"
    )
    
    benchmark.add_test_query(
        "Сложный многотабличный запрос",
        """SELECT c.customer_name, o.order_date, o.total_amount
           FROM customers c
           JOIN orders o ON c.customer_id = o.customer_id
           WHERE o.order_date >= '2024-01-01' AND c.country = 'Russia'
           ORDER BY o.order_date DESC LIMIT 20""",
        "Тестирование сложного запроса с фильтрами и сортировкой"
    )
    
    # Запуск полного тестирования
    benchmark.run_full_benchmark()

if __name__ == "__main__":
    main()