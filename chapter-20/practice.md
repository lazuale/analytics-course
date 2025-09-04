# 📝 Практические задания — Глава 20

📖 [Вернуться к теории](../README.md) | 📁 [Учебные файлы](../files/README.md) | ✅ [Чек-лист](../checklist.md)

---

## 🎯 Задание 1: Освоение JOIN операций

### 📊 Описание
Изучите различные типы JOIN на примере базы данных интернет-магазина. Вы будете объединять таблицы клиентов, заказов и товаров.

### 🔧 Что нужно сделать

**1️⃣ INNER JOIN — активные клиенты**
```sql
-- Найдите всех клиентов, у которых есть заказы
-- Покажите: имя клиента, город, дату заказа, сумму заказа
SELECT c.customer_name, c.city, o.order_date, o.amount
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
ORDER BY o.order_date DESC;
```

**2️⃣ LEFT JOIN — все клиенты**
```sql
-- Покажите всех клиентов, включая тех, кто ничего не заказывал
-- Для клиентов без заказов покажите NULL в колонках заказов
SELECT 
    c.customer_name, 
    c.city, 
    o.order_date, 
    o.amount,
    CASE 
        WHEN o.order_id IS NULL THEN 'Нет заказов'
        ELSE 'Есть заказы'
    END as order_status
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
ORDER BY c.customer_name;
```

**3️⃣ Множественный JOIN**
```sql
-- Объедините 4 таблицы: клиенты, заказы, детали заказов, товары
-- Покажите полную информацию о каждой покупке
SELECT 
    c.customer_name,
    o.order_date,
    p.product_name,
    od.quantity,
    od.unit_price,
    (od.quantity * od.unit_price) as line_total
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
INNER JOIN order_details od ON o.order_id = od.order_id
INNER JOIN products p ON od.product_id = p.product_id
ORDER BY o.order_date, c.customer_name;
```

### 📋 Файлы для работы
- `files/customers.csv` — данные о клиентах
- `files/orders.csv` — данные о заказах  
- `files/order_details.csv` — детали заказов
- `files/products.csv` — каталог товаров

### 🎯 Ожидаемый результат
- Понимание разницы между типами JOIN
- Умение объединять несколько таблиц
- Навык обработки NULL значений

---

## 🔍 Задание 2: Мастерство подзапросов

### 📊 Описание
Научитесь использовать различные типы подзапросов для решения аналитических задач. Найдите клиентов с необычным поведением и проанализируйте продажи.

### 🔧 Что нужно сделать

**1️⃣ Скалярный подзапрос — сравнение со средним**
```sql
-- Найдите клиентов, которые тратят больше среднего
SELECT 
    customer_name,
    total_spent,
    (SELECT AVG(total_spent) FROM customer_totals) as average_spent,
    ROUND(total_spent / (SELECT AVG(total_spent) FROM customer_totals), 2) as ratio_to_avg
FROM (
    SELECT 
        c.customer_name,
        SUM(o.amount) as total_spent
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.customer_name
) as customer_totals
WHERE total_spent > (SELECT AVG(total_spent) FROM customer_totals);
```

**2️⃣ Подзапрос с IN — географический анализ**
```sql
-- Найдите всех клиентов из городов с высокими продажами
SELECT customer_name, city
FROM customers
WHERE city IN (
    SELECT c.city
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.city
    HAVING SUM(o.amount) > 50000
)
ORDER BY city, customer_name;
```

**3️⃣ EXISTS — клиенты с определённым поведением**
```sql
-- Найдите клиентов, которые покупали дорогие товары (цена > 1000)
SELECT DISTINCT c.customer_name, c.city
FROM customers c
WHERE EXISTS (
    SELECT 1
    FROM orders o
    JOIN order_details od ON o.order_id = od.order_id
    JOIN products p ON od.product_id = p.product_id
    WHERE o.customer_id = c.customer_id
    AND p.price > 1000
)
ORDER BY c.customer_name;
```

**4️⃣ Коррелированный подзапрос — сравнение с личным средним**
```sql
-- Найдите заказы клиентов, которые больше их личного среднего чека
SELECT 
    c.customer_name,
    o.order_date,
    o.amount,
    (SELECT AVG(o2.amount) 
     FROM orders o2 
     WHERE o2.customer_id = c.customer_id) as personal_avg
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE o.amount > (
    SELECT AVG(o3.amount)
    FROM orders o3
    WHERE o3.customer_id = c.customer_id
)
ORDER BY c.customer_name, o.order_date;
```

### 🎯 Ожидаемый результат
- Навык написания сложных условий с подзапросами
- Понимание разницы между типами подзапросов
- Умение оптимизировать запросы

---

## 🏗️ Задание 3: Продвинутые CTE

### 📊 Описание
Используйте Common Table Expressions для структурирования сложных аналитических запросов. Создайте многоуровневый анализ продаж и клиентской базы.

### 🔧 Что нужно сделать

**1️⃣ Простой CTE — подготовка данных**
```sql
-- Создайте CTE для расчёта общих трат каждого клиента
WITH customer_spending AS (
    SELECT 
        c.customer_id,
        c.customer_name,
        c.city,
        COUNT(o.order_id) as order_count,
        SUM(o.amount) as total_spent,
        AVG(o.amount) as avg_order_value
    FROM customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.customer_name, c.city
)
-- Используйте CTE для сегментации клиентов
SELECT 
    customer_name,
    city,
    total_spent,
    CASE 
        WHEN total_spent >= 10000 THEN 'VIP'
        WHEN total_spent >= 5000 THEN 'Premium'
        WHEN total_spent >= 1000 THEN 'Regular'
        WHEN total_spent > 0 THEN 'New'
        ELSE 'Inactive'
    END as customer_segment
FROM customer_spending
ORDER BY total_spent DESC;
```

**2️⃣ Множественные CTE — сложная аналитика**
```sql
-- Многоуровневый анализ с несколькими CTE
WITH 
-- CTE 1: Статистика по клиентам
customer_stats AS (
    SELECT 
        c.customer_id,
        c.customer_name,
        c.city,
        COUNT(o.order_id) as order_count,
        SUM(o.amount) as total_spent
    FROM customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.customer_name, c.city
),
-- CTE 2: Средние показатели по городам
city_averages AS (
    SELECT 
        city,
        AVG(total_spent) as avg_city_spending,
        COUNT(*) as customers_in_city
    FROM customer_stats
    GROUP BY city
),
-- CTE 3: Сегментация клиентов
customer_segments AS (
    SELECT 
        cs.*,
        ca.avg_city_spending,
        CASE 
            WHEN cs.total_spent > ca.avg_city_spending * 1,5 THEN 'Above Average'
            WHEN cs.total_spent > ca.avg_city_spending * 0,8 THEN 'Average'
            ELSE 'Below Average'
        END as city_performance
    FROM customer_stats cs
    JOIN city_averages ca ON cs.city = ca.city
)
-- Финальный запрос
SELECT 
    city,
    city_performance,
    COUNT(*) as customers_count,
    AVG(total_spent) as avg_spending
FROM customer_segments
GROUP BY city, city_performance
ORDER BY city, city_performance;
```

**3️⃣ Рекурсивный CTE — анализ временных рядов**
```sql
-- Создайте последовательность дат для анализа продаж
WITH RECURSIVE date_series AS (
    -- Начальная дата
    SELECT DATE('2024-01-01') as sale_date
    
    UNION ALL
    
    -- Добавляем по одному дню
    SELECT DATE(sale_date, '+1 day')
    FROM date_series
    WHERE sale_date < DATE('2024-12-31')
),
-- Продажи по дням (включая дни без продаж)
daily_sales AS (
    SELECT 
        ds.sale_date,
        COALESCE(SUM(o.amount), 0) as daily_total,
        COUNT(o.order_id) as orders_count
    FROM date_series ds
    LEFT JOIN orders o ON DATE(o.order_date) = ds.sale_date
    GROUP BY ds.sale_date
)
SELECT 
    sale_date,
    daily_total,
    orders_count,
    -- Скользящее среднее за 7 дней
    AVG(daily_total) OVER (
        ORDER BY sale_date 
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) as moving_avg_7days
FROM daily_sales
WHERE sale_date <= DATE('2024-03-31')  -- Первый квартал
ORDER BY sale_date;
```

### 🎯 Ожидаемый результат
- Умение структурировать сложные запросы с CTE
- Навык создания многоуровневой аналитики
- Понимание рекурсивных CTE

---

## 🐍 Задание 4: Интеграция SQL и Python

### 📊 Описание
Объедините мощь SQL для обработки данных с возможностями Python для визуализации и дополнительного анализа.

### 🔧 Что нужно сделать

**1️⃣ Создайте Python скрипт `files/sql_integration.py`**
```python
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Подключение к базе данных
def connect_to_db():
    """Создание подключения к SQLite базе данных"""
    conn = sqlite3.connect('sales_data.db')
    return conn

# Функция для выполнения SQL запросов
def execute_sql_query(conn, query):
    """Выполнение SQL запроса и возврат DataFrame"""
    return pd.read_sql_query(query, conn)

# Анализ 1: Продажи по месяцам
def monthly_sales_analysis(conn):
    """Анализ месячных продаж с использованием CTE"""
    query = """
    WITH monthly_sales AS (
        SELECT 
            strftime('%Y-%m', order_date) as month,
            SUM(amount) as total_sales,
            COUNT(*) as order_count,
            AVG(amount) as avg_order_value
        FROM orders
        WHERE order_date >= date('now', '-12 months')
        GROUP BY strftime('%Y-%m', order_date)
    )
    SELECT * FROM monthly_sales
    ORDER BY month;
    """
    
    df = execute_sql_query(conn, query)
    
    # Визуализация
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    # График продаж
    axes[0,0].plot(df['month'], df['total_sales'], marker='o', linewidth=2)
    axes[0,0].set_title('📈 Динамика продаж по месяцам')
    axes[0,0].set_xlabel('Месяц')
    axes[0,0].set_ylabel('Общие продажи')
    axes[0,0].tick_params(axis='x', rotation=45)
    
    # График количества заказов
    axes[0,1].bar(df['month'], df['order_count'], color='skyblue')
    axes[0,1].set_title('📊 Количество заказов по месяцам')
    axes[0,1].set_xlabel('Месяц')
    axes[0,1].set_ylabel('Количество заказов')
    axes[0,1].tick_params(axis='x', rotation=45)
    
    # График среднего чека
    axes[1,0].plot(df['month'], df['avg_order_value'], marker='s', color='green')
    axes[1,0].set_title('💰 Средний чек по месяцам')
    axes[1,0].set_xlabel('Месяц')
    axes[1,0].set_ylabel('Средний чек')
    axes[1,0].tick_params(axis='x', rotation=45)
    
    # Корреляция между метриками
    correlation_data = df[['total_sales', 'order_count', 'avg_order_value']].corr()
    sns.heatmap(correlation_data, annot=True, ax=axes[1,1], cmap='coolwarm')
    axes[1,1].set_title('🔥 Корреляция между метриками')
    
    plt.tight_layout()
    plt.savefig('monthly_sales_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    return df

# Анализ 2: Сегментация клиентов
def customer_segmentation_analysis(conn):
    """RFM анализ клиентов с использованием подзапросов"""
    query = """
    WITH customer_rfm AS (
        SELECT 
            c.customer_id,
            c.customer_name,
            c.city,
            -- Recency: дни с последнего заказа
            julianday('now') - julianday(MAX(o.order_date)) as recency_days,
            -- Frequency: количество заказов
            COUNT(o.order_id) as frequency,
            -- Monetary: общая сумма заказов
            SUM(o.amount) as monetary
        FROM customers c
        LEFT JOIN orders o ON c.customer_id = o.customer_id
        WHERE o.order_id IS NOT NULL
        GROUP BY c.customer_id, c.customer_name, c.city
    ),
    customer_scores AS (
        SELECT *,
            -- RFM скоры (1-5, где 5 лучше)
            CASE 
                WHEN recency_days <= 30 THEN 5
                WHEN recency_days <= 90 THEN 4
                WHEN recency_days <= 180 THEN 3
                WHEN recency_days <= 365 THEN 2
                ELSE 1
            END as r_score,
            CASE 
                WHEN frequency >= 10 THEN 5
                WHEN frequency >= 7 THEN 4
                WHEN frequency >= 4 THEN 3
                WHEN frequency >= 2 THEN 2
                ELSE 1
            END as f_score,
            CASE 
                WHEN monetary >= 10000 THEN 5
                WHEN monetary >= 5000 THEN 4
                WHEN monetary >= 2000 THEN 3
                WHEN monetary >= 500 THEN 2
                ELSE 1
            END as m_score
        FROM customer_rfm
    )
    SELECT 
        *,
        -- Общий RFM сегмент
        CASE 
            WHEN r_score >= 4 AND f_score >= 4 AND m_score >= 4 THEN 'Champions'
            WHEN r_score >= 3 AND f_score >= 3 AND m_score >= 3 THEN 'Loyal Customers'
            WHEN r_score >= 4 AND f_score <= 2 THEN 'New Customers'
            WHEN r_score <= 2 AND f_score >= 3 AND m_score >= 3 THEN 'At Risk'
            ELSE 'Others'
        END as rfm_segment
    FROM customer_scores;
    """
    
    df = execute_sql_query(conn, query)
    
    # Визуализация сегментов
    plt.figure(figsize=(12, 8))
    
    # Распределение по сегментам
    plt.subplot(2, 2, 1)
    segment_counts = df['rfm_segment'].value_counts()
    plt.bar(segment_counts.index, segment_counts.values, color='lightcoral')
    plt.title('👥 Распределение клиентов по сегментам')
    plt.xlabel('RFM Сегмент')
    plt.ylabel('Количество клиентов')
    plt.xticks(rotation=45)
    
    # Scatter plot R vs F
    plt.subplot(2, 2, 2)
    scatter = plt.scatter(df['r_score'], df['f_score'], 
                         c=df['m_score'], cmap='viridis', alpha=0.6)
    plt.colorbar(scatter, label='Monetary Score')
    plt.title('🎯 RFM Скоры: Recency vs Frequency')
    plt.xlabel('Recency Score')
    plt.ylabel('Frequency Score')
    
    # Boxplot по сегментам
    plt.subplot(2, 2, 3)
    df.boxplot(column='monetary', by='rfm_segment', ax=plt.gca())
    plt.title('💰 Распределение трат по сегментам')
    plt.xlabel('RFM Сегмент')
    plt.ylabel('Общие траты')
    plt.xticks(rotation=45)
    
    # Средние значения по сегментам
    plt.subplot(2, 2, 4)
    segment_avg = df.groupby('rfm_segment')[['recency_days', 'frequency', 'monetary']].mean()
    segment_avg.plot(kind='bar', ax=plt.gca())
    plt.title('📊 Средние показатели по сегментам')
    plt.xlabel('RFM Сегмент')
    plt.ylabel('Средние значения')
    plt.legend(['Recency (дни)', 'Frequency (заказы)', 'Monetary (рубли)'])
    plt.xticks(rotation=45)
    
    plt.tight_layout()
    plt.savefig('customer_segmentation.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    return df

# Главная функция
def main():
    """Основная функция для запуска всех анализов"""
    conn = connect_to_db()
    
    try:
        print("🚀 Запуск анализа месячных продаж...")
        monthly_df = monthly_sales_analysis(conn)
        print(f"✅ Обработано {len(monthly_df)} месяцев данных")
        
        print("\n🎯 Запуск RFM сегментации клиентов...")
        rfm_df = customer_segmentation_analysis(conn)
        print(f"✅ Сегментировано {len(rfm_df)} клиентов")
        
        # Сохранение результатов
        monthly_df.to_csv('monthly_sales_results.csv', index=False, sep=';')
        rfm_df.to_csv('customer_rfm_segments.csv', index=False, sep=';')
        
        print("\n📊 Анализ завершён! Результаты сохранены в CSV файлы.")
        
    finally:
        conn.close()

if __name__ == "__main__":
    main()
```

**2️⃣ Создайте дополнительный скрипт `files/advanced_sql_python.py`**
```python
import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def create_sample_database():
    """Создание демонстрационной базы данных"""
    conn = sqlite3.connect('sales_data.db')
    cursor = conn.cursor()
    
    # Создание таблиц (если они не существуют)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        customer_id INTEGER PRIMARY KEY,
        customer_name TEXT NOT NULL,
        city TEXT NOT NULL,
        registration_date DATE
    );
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        order_id INTEGER PRIMARY KEY,
        customer_id INTEGER,
        order_date DATE NOT NULL,
        amount DECIMAL(10,2) NOT NULL,
        FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
    );
    """)
    
    # Пример данных (если таблицы пустые)
    cursor.execute("SELECT COUNT(*) FROM customers")
    if cursor.fetchone()[0] == 0:
        print("📝 Создание демонстрационных данных...")
        
        # Вставка клиентов
        customers_data = [
            (1, 'Иван Петров', 'Москва', '2023-01-15'),
            (2, 'Мария Сидорова', 'Санкт-Петербург', '2023-02-20'),
            (3, 'Алексей Козлов', 'Москва', '2023-03-10'),
            (4, 'Елена Морозова', 'Екатеринбург', '2023-04-05'),
            (5, 'Дмитрий Волков', 'Новосибирск', '2023-05-12')
        ]
        cursor.executemany(
            "INSERT INTO customers (customer_id, customer_name, city, registration_date) VALUES (?, ?, ?, ?)",
            customers_data
        )
        
        # Вставка заказов
        orders_data = [
            (1, 1, '2023-02-01', 1500.50),
            (2, 1, '2023-03-15', 2300.75),
            (3, 2, '2023-03-01', 980.25),
            (4, 3, '2023-04-10', 3200.00),
            (5, 1, '2023-04-20', 1800.30),
            (6, 4, '2023-05-05', 4500.80),
            (7, 2, '2023-05-15', 1200.90),
            (8, 5, '2023-06-01', 2800.45)
        ]
        cursor.executemany(
            "INSERT INTO orders (order_id, customer_id, order_date, amount) VALUES (?, ?, ?, ?)",
            orders_data
        )
    
    conn.commit()
    return conn

def demonstrate_complex_queries():
    """Демонстрация сложных SQL запросов"""
    conn = create_sample_database()
    
    # Запрос 1: CTE с оконными функциями
    query1 = """
    WITH customer_analysis AS (
        SELECT 
            c.customer_name,
            c.city,
            o.order_date,
            o.amount,
            -- Оконные функции
            ROW_NUMBER() OVER (PARTITION BY c.customer_id ORDER BY o.order_date) as order_sequence,
            SUM(o.amount) OVER (PARTITION BY c.customer_id ORDER BY o.order_date) as running_total,
            AVG(o.amount) OVER (PARTITION BY c.city) as city_avg_amount
        FROM customers c
        JOIN orders o ON c.customer_id = o.customer_id
    )
    SELECT 
        customer_name,
        city,
        order_sequence,
        amount,
        running_total,
        city_avg_amount,
        ROUND(amount / city_avg_amount, 2) as ratio_to_city_avg
    FROM customer_analysis
    ORDER BY customer_name, order_sequence;
    """
    
    print("🔍 Запрос 1: CTE с оконными функциями")
    df1 = pd.read_sql_query(query1, conn)
    print(df1.to_string(index=False))
    print("\n" + "="*80 + "\n")
    
    # Запрос 2: Сложные подзапросы
    query2 = """
    SELECT 
        c.customer_name,
        c.city,
        -- Подзапрос: общие траты клиента
        (SELECT SUM(amount) FROM orders WHERE customer_id = c.customer_id) as total_spent,
        -- Подзапрос: средние траты по городу
        (SELECT AVG(city_totals.total) 
         FROM (SELECT SUM(amount) as total 
               FROM orders o2 
               JOIN customers c2 ON o2.customer_id = c2.customer_id 
               WHERE c2.city = c.city 
               GROUP BY o2.customer_id) as city_totals) as city_avg_spent,
        -- Подзапрос: ранг клиента в городе
        (SELECT COUNT(*) + 1 
         FROM customers c3 
         WHERE c3.city = c.city 
         AND (SELECT SUM(amount) FROM orders WHERE customer_id = c3.customer_id) > 
             (SELECT SUM(amount) FROM orders WHERE customer_id = c.customer_id)) as city_rank
    FROM customers c
    WHERE EXISTS (SELECT 1 FROM orders WHERE customer_id = c.customer_id)
    ORDER BY c.city, city_rank;
    """
    
    print("🔍 Запрос 2: Сложные подзапросы")
    df2 = pd.read_sql_query(query2, conn)
    print(df2.to_string(index=False))
    
    conn.close()
    return df1, df2

if __name__ == "__main__":
    demonstrate_complex_queries()
```

### 📋 Файлы для работы
- `files/sql_integration.py` — интеграция SQL и Python
- `files/advanced_sql_python.py` — сложные запросы в Python
- `files/sales_data.db` — база данных SQLite

### 🎯 Ожидаемый результат
- Навык интеграции SQL и Python
- Умение создавать аналитические скрипты
- Опыт визуализации SQL результатов

---

## 🧮 Задание 5: Комплексный проект — Аналитическая панель

### 📊 Описание
Создайте комплексную аналитическую систему, объединяющую все изученные техники: JOIN, подзапросы, CTE и интеграцию с Python.

### 🔧 Что нужно сделать

**1️⃣ Создайте основной SQL запрос с использованием всех техник**
```sql
-- Комплексный анализ бизнеса
WITH 
-- CTE 1: Базовая статистика клиентов
customer_base AS (
    SELECT 
        c.customer_id,
        c.customer_name,
        c.city,
        c.registration_date,
        COUNT(o.order_id) as total_orders,
        COALESCE(SUM(o.amount), 0) as total_spent,
        COALESCE(AVG(o.amount), 0) as avg_order_value,
        MAX(o.order_date) as last_order_date
    FROM customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.customer_name, c.city, c.registration_date
),
-- CTE 2: Сегментация клиентов
customer_segments AS (
    SELECT 
        *,
        -- Сегментация по активности
        CASE 
            WHEN last_order_date >= DATE('now', '-30 days') THEN 'Active'
            WHEN last_order_date >= DATE('now', '-90 days') THEN 'Cooling'
            WHEN last_order_date >= DATE('now', '-365 days') THEN 'At Risk'
            WHEN last_order_date IS NOT NULL THEN 'Lost'
            ELSE 'Never Purchased'
        END as activity_segment,
        -- Сегментация по ценности
        CASE 
            WHEN total_spent >= 10000 THEN 'High Value'
            WHEN total_spent >= 3000 THEN 'Medium Value'
            WHEN total_spent > 0 THEN 'Low Value'
            ELSE 'No Value'
        END as value_segment
    FROM customer_base
),
-- CTE 3: Анализ по городам
city_performance AS (
    SELECT 
        city,
        COUNT(*) as total_customers,
        SUM(CASE WHEN activity_segment = 'Active' THEN 1 ELSE 0 END) as active_customers,
        AVG(total_spent) as avg_customer_value,
        SUM(total_spent) as city_total_revenue
    FROM customer_segments
    GROUP BY city
)
-- Финальный запрос с подзапросами
SELECT 
    cs.customer_name,
    cs.city,
    cs.activity_segment,
    cs.value_segment,
    cs.total_orders,
    cs.total_spent,
    cs.avg_order_value,
    -- Подзапрос: ранг в городе по тратам
    (SELECT COUNT(*) + 1 
     FROM customer_segments cs2 
     WHERE cs2.city = cs.city AND cs2.total_spent > cs.total_spent) as city_spending_rank,
    -- Подзапрос: процент от общей выручки города
    ROUND(cs.total_spent * 100.0 / cp.city_total_revenue, 2) as city_revenue_share,
    cp.avg_customer_value as city_avg_value,
    -- Сравнение с городским средним
    ROUND(cs.total_spent / cp.avg_customer_value, 2) as ratio_to_city_avg
FROM customer_segments cs
JOIN city_performance cp ON cs.city = cp.city
WHERE cs.total_orders > 0  -- Только клиенты с заказами
ORDER BY cs.city, cs.total_spent DESC;
```

**2️⃣ Создайте Python скрипт для автоматизации `files/business_intelligence.py`**
```python
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

class BusinessIntelligence:
    """Класс для бизнес-аналитики на основе SQL и Python"""
    
    def __init__(self, db_path='sales_data.db'):
        self.db_path = db_path
        
    def connect(self):
        """Создание подключения к базе данных"""
        return sqlite3.connect(self.db_path)
    
    def generate_executive_dashboard(self):
        """Создание исполнительской панели"""
        conn = self.connect()
        
        # Основные метрики
        metrics_query = """
        SELECT 
            COUNT(DISTINCT customer_id) as total_customers,
            COUNT(DISTINCT CASE WHEN total_orders > 0 THEN customer_id END) as active_customers,
            SUM(total_spent) as total_revenue,
            AVG(total_spent) as avg_customer_value,
            MAX(last_order_date) as latest_order_date
        FROM (
            SELECT 
                c.customer_id,
                COUNT(o.order_id) as total_orders,
                COALESCE(SUM(o.amount), 0) as total_spent,
                MAX(o.order_date) as last_order_date
            FROM customers c
            LEFT JOIN orders o ON c.customer_id = o.customer_id
            GROUP BY c.customer_id
        ) customer_stats;
        """
        
        metrics_df = pd.read_sql_query(metrics_query, conn)
        
        # Детальный анализ
        detailed_query = """
        WITH customer_analysis AS (
            SELECT 
                c.customer_id,
                c.customer_name,
                c.city,
                COUNT(o.order_id) as order_count,
                COALESCE(SUM(o.amount), 0) as total_spent,
                CASE 
                    WHEN MAX(o.order_date) >= DATE('now', '-30 days') THEN 'Active'
                    WHEN MAX(o.order_date) >= DATE('now', '-90 days') THEN 'Cooling'
                    WHEN MAX(o.order_date) IS NOT NULL THEN 'At Risk'
                    ELSE 'Never Purchased'
                END as segment
            FROM customers c
            LEFT JOIN orders o ON c.customer_id = o.customer_id
            GROUP BY c.customer_id, c.customer_name, c.city
        )
        SELECT 
            segment,
            COUNT(*) as customers_count,
            SUM(total_spent) as segment_revenue,
            AVG(total_spent) as avg_customer_value
        FROM customer_analysis
        GROUP BY segment
        ORDER BY segment_revenue DESC;
        """
        
        segments_df = pd.read_sql_query(detailed_query, conn)
        
        # Создание дашборда
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('📊 Executive Business Intelligence Dashboard', fontsize=16, fontweight='bold')
        
        # График 1: Распределение клиентов по сегментам
        axes[0,0].bar(segments_df['segment'], segments_df['customers_count'], 
                     color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'])
        axes[0,0].set_title('👥 Распределение клиентов по сегментам')
        axes[0,0].set_xlabel('Сегмент')
        axes[0,0].set_ylabel('Количество клиентов')
        
        # График 2: Выручка по сегментам
        axes[0,1].pie(segments_df['segment_revenue'], labels=segments_df['segment'], 
                     autopct='%1.1f%%', startangle=90)
        axes[0,1].set_title('💰 Выручка по сегментам')
        
        # График 3: Средняя ценность клиента
        axes[1,0].bar(segments_df['segment'], segments_df['avg_customer_value'],
                     color=['#FF9F43', '#10AC84', '#5F27CD', '#00D2D3'])
        axes[1,0].set_title('💎 Средняя ценность клиента по сегментам')
        axes[1,0].set_xlabel('Сегмент')
        axes[1,0].set_ylabel('Средняя ценность (руб.)')
        
        # График 4: Ключевые метрики
        metrics_text = f"""
        📈 КЛЮЧЕВЫЕ ПОКАЗАТЕЛИ
        
        👥 Всего клиентов: {metrics_df['total_customers'].iloc[0]:,}
        ✅ Активных клиентов: {metrics_df['active_customers'].iloc[0]:,}
        💰 Общая выручка: {metrics_df['total_revenue'].iloc[0]:,.2f} руб.
        💎 Средняя ценность: {metrics_df['avg_customer_value'].iloc[0]:,.2f} руб.
        📅 Последний заказ: {metrics_df['latest_order_date'].iloc[0]}
        
        📊 КОНВЕРСИЯ
        Активация: {(metrics_df['active_customers'].iloc[0] / metrics_df['total_customers'].iloc[0] * 100):.1f}%
        """
        
        axes[1,1].text(0.1, 0.5, metrics_text, fontsize=12, 
                      verticalalignment='center', transform=axes[1,1].transAxes,
                      bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.7))
        axes[1,1].set_xlim(0, 1)
        axes[1,1].set_ylim(0, 1)
        axes[1,1].axis('off')
        axes[1,1].set_title('📋 Сводка метрик')
        
        plt.tight_layout()
        plt.savefig('executive_dashboard.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        conn.close()
        return metrics_df, segments_df
    
    def generate_detailed_report(self):
        """Создание детального отчёта"""
        conn = self.connect()
        
        # Сложный запрос с всеми техниками
        complex_query = """
        WITH 
        customer_metrics AS (
            SELECT 
                c.customer_id,
                c.customer_name,
                c.city,
                COUNT(o.order_id) as order_count,
                COALESCE(SUM(o.amount), 0) as total_spent,
                COALESCE(AVG(o.amount), 0) as avg_order_value,
                MAX(o.order_date) as last_order_date,
                MIN(o.order_date) as first_order_date
            FROM customers c
            LEFT JOIN orders o ON c.customer_id = o.customer_id
            GROUP BY c.customer_id, c.customer_name, c.city
        ),
        city_benchmarks AS (
            SELECT 
                city,
                AVG(total_spent) as city_avg_spent,
                COUNT(*) as city_customers
            FROM customer_metrics
            GROUP BY city
        )
        SELECT 
            cm.customer_name,
            cm.city,
            cm.order_count,
            cm.total_spent,
            cm.avg_order_value,
            cb.city_avg_spent,
            -- Сравнение с городским средним
            ROUND(cm.total_spent / cb.city_avg_spent, 2) as vs_city_avg,
            -- Ранг в городе
            (SELECT COUNT(*) + 1 
             FROM customer_metrics cm2 
             WHERE cm2.city = cm.city AND cm2.total_spent > cm.total_spent) as city_rank,
            -- Дни с последнего заказа
            CASE 
                WHEN cm.last_order_date IS NOT NULL 
                THEN julianday('now') - julianday(cm.last_order_date)
                ELSE NULL
            END as days_since_last_order
        FROM customer_metrics cm
        JOIN city_benchmarks cb ON cm.city = cb.city
        WHERE cm.order_count > 0
        ORDER BY cm.city, cm.total_spent DESC;
        """
        
        detailed_df = pd.read_sql_query(complex_query, conn)
        
        # Сохранение в CSV
        detailed_df.to_csv('detailed_customer_report.csv', index=False, sep=';')
        
        conn.close()
        return detailed_df

# Использование класса
if __name__ == "__main__":
    bi = BusinessIntelligence()
    
    print("🚀 Генерация исполнительского дашборда...")
    metrics, segments = bi.generate_executive_dashboard()
    
    print("\n📊 Создание детального отчёта...")
    detailed_report = bi.generate_detailed_report()
    
    print(f"\n✅ Анализ завершён! Обработано {len(detailed_report)} записей.")
    print("📁 Файлы сохранены:")
    print("   • executive_dashboard.png")
    print("   • detailed_customer_report.csv")
```

### 🎯 Ожидаемый результат
- Комплексная аналитическая система
- Автоматизированная генерация отчётов
- Интеграция всех изученных техник SQL
- Профессиональные навыки бизнес-аналитики

---

- 🔙 [Предыдущая глава: Глава 19 - SQL: основные запросы, агрегаты, GROUP BY](../chapter-19/README.md)
- 🔜 [Следующая глава: Глава 21 - Реляционные модели данных и индексы](../chapter-21/README.md)

---

- 📢 Присоединяйтесь к чату курса: https://t.me/analytics_course_chat
- 📢 Канал курса: https://t.me/analytics_course_channel