"""
🗄️ Пример работы с базой данных SQLite из Python
Демонстрирует интеграцию Pandas и SQL
"""

import sqlite3
import pandas as pd

def connect_to_database(db_path):
    """Подключение к базе данных"""
    try:
        conn = sqlite3.connect(db_path)
        print(f"✅ Подключение к БД: {db_path}")
        return conn
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
        return None

def explore_database(conn):
    """Исследование структуры базы данных"""
    print("\n🔍 Исследование базы данных:")

    # Получаем список таблиц
    tables_query = "SELECT name FROM sqlite_master WHERE type='table';"
    tables = pd.read_sql_query(tables_query, conn)

    print("📋 Доступные таблицы:")
    for table in tables['name']:
        print(f"   📊 {table}")

        # Считаем записи в каждой таблице
        count_query = f"SELECT COUNT(*) as count FROM {table};"
        count = pd.read_sql_query(count_query, conn)
        print(f"      Записей: {count['count'].iloc[0]:,}")

def load_customers_analysis(conn):
    """Анализ клиентов"""
    print("\n👥 АНАЛИЗ КЛИЕНТОВ")
    print("-" * 15)

    query = """
    SELECT 
        customer_name,
        city,
        country,
        customer_segment,
        total_spent
    FROM customers
    ORDER BY total_spent DESC
    LIMIT 5
    """

    df = pd.read_sql_query(query, conn)
    print("🏆 Топ-5 клиентов по тратам:")
    print(df.to_string(index=False))

    return df

def load_sales_analysis(conn):
    """Анализ продаж"""
    print("\n💰 АНАЛИЗ ПРОДАЖ")
    print("-" * 13)

    query = """
    SELECT 
        c.customer_name,
        o.order_date,
        o.total_amount,
        o.status
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
    WHERE o.status = 'Completed'
    ORDER BY o.total_amount DESC
    LIMIT 5
    """

    df = pd.read_sql_query(query, conn)
    print("💎 Топ-5 заказов:")
    print(df.to_string(index=False))

    return df

def create_summary_report(conn):
    """Создание сводного отчета"""
    print("\n📊 СВОДНЫЙ ОТЧЕТ")
    print("-" * 13)

    # Общая статистика
    summary_query = """
    SELECT 
        COUNT(DISTINCT c.customer_id) as total_customers,
        COUNT(o.order_id) as total_orders,
        SUM(o.total_amount) as total_revenue,
        AVG(o.total_amount) as avg_order_value
    FROM customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id
    WHERE o.status = 'Completed'
    """

    summary = pd.read_sql_query(summary_query, conn)

    print("📈 Ключевые показатели:")
    print(f"   👥 Всего клиентов: {summary['total_customers'].iloc[0]:,}")
    print(f"   🛒 Всего заказов: {summary['total_orders'].iloc[0]:,}")
    print(f"   💰 Общая выручка: ${summary['total_revenue'].iloc[0]:,.2f}")
    print(f"   💳 Средний чек: ${summary['avg_order_value'].iloc[0]:,.2f}")

def save_results_to_database(conn, df, table_name):
    """Сохранение результатов анализа обратно в БД"""
    print(f"\n💾 Сохранение в таблицу: {table_name}")

    try:
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        print(f"   ✅ Данные сохранены в {table_name}")
    except Exception as e:
        print(f"   ❌ Ошибка сохранения: {e}")

# Главная функция
def main():
    """Основной процесс анализа"""
    print("🗄️ Pandas + SQL = Суперсила аналитика!")
    print("=" * 40)

    # Подключаемся к БД
    conn = connect_to_database('sample_database.db')
    if not conn:
        return

    try:
        # Исследуем структуру
        explore_database(conn)

        # Проводим анализы
        customers_df = load_customers_analysis(conn)
        sales_df = load_sales_analysis(conn)

        # Создаем отчет
        create_summary_report(conn)

        # Дополнительная аналитика в Pandas
        print("\n🐍 Дополнительная аналитика в Pandas:")

        # Загружаем все заказы для анализа
        all_orders = pd.read_sql_query("""
            SELECT o.*, c.customer_segment, c.city, c.country
            FROM orders o
            JOIN customers c ON o.customer_id = c.customer_id
            WHERE o.status = 'Completed'
        """, conn)

        # Анализ по сегментам
        segment_analysis = all_orders.groupby('customer_segment').agg({
            'total_amount': ['sum', 'mean', 'count']
        }).round(2)

        print("📊 Анализ по сегментам клиентов:")
        print(segment_analysis)

        # Сохраняем результат обратно в БД
        save_results_to_database(conn, segment_analysis.reset_index(), 'segment_analysis')

    finally:
        conn.close()
        print("\n🔒 Соединение с БД закрыто")

    print("\n✅ Анализ завершен! SQL + Pandas = 💪")

if __name__ == "__main__":
    main()
