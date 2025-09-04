# 📝 Практические задания — Глава 22

📖 [Вернуться к теории](../README.md) | 📁 [Учебные файлы](../files/README.md) | ✅ [Чек-лист](../checklist.md)

---

## ⚡ Задание 1: Анализ планов выполнения запросов

### 📊 Описание
Изучите планы выполнения различных типов SQL-запросов, научитесь читать EXPLAIN PLAN и выявлять узкие места в производительности.

### 🔧 Что нужно сделать

**1️⃣ Анализ простых запросов**

```sql
-- Проанализируйте план выполнения для поиска по индексу
-- Используйте базу данных files/ecommerce_performance.db

-- Запрос 1: Поиск клиента по email
EXPLAIN QUERY PLAN
SELECT customer_id, customer_name, registration_date
FROM customers 
WHERE email = 'john.doe@email.com';

-- Запрос 2: Поиск заказов за период  
EXPLAIN QUERY PLAN
SELECT order_id, customer_id, order_date, total_amount
FROM orders
WHERE order_date BETWEEN '2024-01-01' AND '2024-03-31'
ORDER BY order_date DESC;

-- Запрос 3: Агрегация по категориям
EXPLAIN QUERY PLAN  
SELECT p.category, COUNT(*) as products_count, AVG(p.price) as avg_price
FROM products p
WHERE p.in_stock = 1
GROUP BY p.category
ORDER BY products_count DESC;
```

**Анализируйте каждый план и ответьте на вопросы:**
- Использует ли запрос индексы?
- Какие операции занимают больше всего времени?
- Есть ли полные сканирования таблиц (TABLE SCAN)?
- Можно ли улучшить производительность?

**2️⃣ Анализ сложных JOIN запросов**

```sql
-- Запрос 4: Многотабличный JOIN
EXPLAIN QUERY PLAN
SELECT 
    c.customer_name,
    o.order_date,
    p.product_name,
    oi.quantity,
    oi.unit_price,
    (oi.quantity * oi.unit_price) as line_total
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id  
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
WHERE o.order_date >= '2024-01-01'
  AND c.country = 'Russia'
  AND p.category = 'Electronics';

-- Запрос 5: LEFT JOIN с агрегацией
EXPLAIN QUERY PLAN
SELECT 
    c.customer_name,
    c.email,
    COUNT(o.order_id) as total_orders,
    COALESCE(SUM(o.total_amount), 0) as total_spent,
    MAX(o.order_date) as last_order_date
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE c.registration_date >= '2023-01-01'
GROUP BY c.customer_id, c.customer_name, c.email
HAVING COUNT(o.order_id) >= 5
ORDER BY total_spent DESC;
```

**3️⃣ Анализ подзапросов**

```sql
-- Запрос 6: Коррелированный подзапрос (медленный)
EXPLAIN QUERY PLAN
SELECT 
    p.product_name,
    p.price,
    p.category
FROM products p
WHERE p.price > (
    SELECT AVG(p2.price) 
    FROM products p2 
    WHERE p2.category = p.category
);

-- Запрос 7: EXISTS подзапрос
EXPLAIN QUERY PLAN
SELECT c.customer_name, c.email
FROM customers c
WHERE EXISTS (
    SELECT 1 
    FROM orders o 
    WHERE o.customer_id = c.customer_id 
      AND o.order_date >= '2024-01-01'
      AND o.total_amount > 1000
);

-- Запрос 8: IN подзапрос
EXPLAIN QUERY PLAN  
SELECT product_name, price
FROM products
WHERE product_id IN (
    SELECT DISTINCT product_id
    FROM order_items oi
    JOIN orders o ON oi.order_id = o.order_id
    WHERE o.order_date >= '2024-01-01'
    GROUP BY product_id
    HAVING SUM(quantity) > 100
);
```

### 📋 Файлы для работы
- `files/ecommerce_performance.db` — база данных интернет-магазина
- `files/query_analysis_template.sql` — шаблон для анализа
- `files/performance_baseline.sql` — базовые замеры производительности

### 🎯 Ожидаемый результат
- Понимание структуры планов выполнения
- Умение выявлять неэффективные операции
- Навыки интерпретации статистики выполнения

---

## 📊 Задание 2: Создание и тестирование индексов

### 📊 Описание
Создайте различные типы индексов для оптимизации медленных запросов и измерьте улучшение производительности.

### 🔧 Что нужно сделать

**1️⃣ Тестирование запросов без индексов**

```sql
-- Сначала удалим все существующие индексы (кроме PRIMARY KEY)
-- Используйте файл files/remove_indexes.sql

-- Замерьте время выполнения базовых запросов
.timer on

-- Тест 1: Поиск по email (без индекса)
SELECT * FROM customers WHERE email = 'maria.petrov@email.com';

-- Тест 2: Фильтрация заказов по дате (без индекса) 
SELECT COUNT(*) FROM orders WHERE order_date >= '2024-01-01';

-- Тест 3: JOIN операция (без индексов на внешних ключах)
SELECT c.customer_name, COUNT(o.order_id) as order_count
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.customer_name
ORDER BY order_count DESC
LIMIT 20;

-- Тест 4: Сложная агрегация
SELECT 
    p.category,
    COUNT(DISTINCT oi.order_id) as orders_with_category,
    SUM(oi.quantity * oi.unit_price) as category_revenue
FROM products p
JOIN order_items oi ON p.product_id = oi.product_id
JOIN orders o ON oi.order_id = o.order_id
WHERE o.order_date >= '2024-01-01'
GROUP BY p.category
ORDER BY category_revenue DESC;
```

**Запишите время выполнения каждого запроса**

**2️⃣ Создание оптимальных индексов**

```sql
-- Создайте индексы для ускорения запросов из предыдущего пункта

-- Индекс для поиска по email
CREATE INDEX idx_customers_email ON customers(email);

-- Индекс для фильтрации по дате заказов
CREATE INDEX idx_orders_date ON orders(order_date);

-- Индексы для JOIN операций
CREATE INDEX idx_orders_customer_id ON orders(customer_id);
CREATE INDEX idx_order_items_order_id ON order_items(order_id);
CREATE INDEX idx_order_items_product_id ON order_items(product_id);

-- Составные индексы для сложных запросов
CREATE INDEX idx_orders_date_customer ON orders(order_date, customer_id);
CREATE INDEX idx_products_category ON products(category);

-- Покрывающий индекс для частого запроса
CREATE INDEX idx_products_category_covering 
ON products(category, product_id, product_name);
```

**3️⃣ Повторное тестирование с индексами**

```sql
-- Повторите те же тесты с созданными индексами
-- Сравните время выполнения

-- Обновите статистику для точных замеров
ANALYZE;

-- Повторите все 4 теста из пункта 1
-- Запишите новое время выполнения
```

**4️⃣ Создание специализированных индексов**

```sql
-- Частичный индекс для активных клиентов
CREATE INDEX idx_customers_active_email 
ON customers(email) 
WHERE is_active = 1;

-- Функциональный индекс для поиска по верхнему регистру
CREATE INDEX idx_customers_upper_email 
ON customers(UPPER(email));

-- Составной индекс с правильным порядком столбцов
CREATE INDEX idx_orders_customer_date_amount 
ON orders(customer_id, order_date, total_amount);

-- Тестируйте специфические запросы для этих индексов
SELECT * FROM customers 
WHERE is_active = 1 AND email = 'test@example.com';

SELECT * FROM customers 
WHERE UPPER(email) = 'JOHN.DOE@EMAIL.COM';

SELECT customer_id, SUM(total_amount) 
FROM orders 
WHERE customer_id = 12345 
  AND order_date >= '2024-01-01'
GROUP BY customer_id;
```

**5️⃣ Анализ использования индексов**

```sql
-- Проверьте, какие индексы используются
EXPLAIN QUERY PLAN
SELECT c.customer_name, o.order_date, o.total_amount
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE c.email = 'john@example.com'
  AND o.order_date >= '2024-01-01'
ORDER BY o.order_date DESC;

-- Найдите неиспользуемые индексы
-- (команда зависит от СУБД, для SQLite используйте визуальный анализ)

-- Проанализируйте размер индексов
SELECT 
    name,
    sql
FROM sqlite_master 
WHERE type = 'index' 
  AND name NOT LIKE 'sqlite_autoindex%'
ORDER BY name;
```

### 📋 Файлы для работы
- `files/remove_indexes.sql` — удаление существующих индексов
- `files/index_creation_script.sql` — скрипт создания индексов
- `files/performance_comparison.xlsx` — таблица для записи результатов

### 🎯 Ожидаемый результат
- Измеримое улучшение производительности запросов
- Понимание влияния различных типов индексов
- Навыки выбора правильной стратегии индексации

---

## 🎯 Задание 3: Оптимизация медленных запросов

### 📊 Описание
Возьмите набор медленных запросов и примените различные техники оптимизации для значительного улучшения их производительности.

### 🔧 Что нужно сделать

**1️⃣ Оптимизация WHERE условий**

```sql
-- Исходный медленный запрос 1
-- Проблема: функция в WHERE блокирует использование индекса
SELECT customer_id, customer_name, registration_date
FROM customers
WHERE YEAR(registration_date) = 2024
  AND LOWER(email) LIKE '%gmail%';

-- Ваша оптимизация:
-- TODO: Переписать запрос без функций в WHERE
-- TODO: Создать необходимые индексы

-- Исходный медленный запрос 2  
-- Проблема: неэффективные OR условия
SELECT product_id, product_name, price
FROM products
WHERE category = 'Electronics' 
   OR category = 'Computers'
   OR category = 'Phones'
   OR price > 10000;

-- Ваша оптимизация:
-- TODO: Использовать IN вместо множественных OR
-- TODO: Разделить на несколько запросов если нужно
```

**2️⃣ Оптимизация JOIN операций**

```sql
-- Исходный медленный запрос 3
-- Проблема: неэффективный порядок JOIN и отсутствие фильтров
SELECT 
    c.customer_name,
    p.product_name,
    SUM(oi.quantity) as total_quantity
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN order_items oi ON o.order_id = oi.order_id  
JOIN products p ON oi.product_id = p.product_id
GROUP BY c.customer_name, p.product_name
ORDER BY total_quantity DESC;

-- Ваша оптимизация:
-- TODO: Добавить временные фильтры
-- TODO: Оптимизировать порядок JOIN
-- TODO: Создать необходимые индексы

-- Исходный медленный запрос 4
-- Проблема: коррелированный подзапрос
SELECT 
    o.order_id,
    o.order_date,
    o.total_amount,
    (SELECT COUNT(*) 
     FROM order_items oi 
     WHERE oi.order_id = o.order_id) as items_count,
    (SELECT AVG(oi2.unit_price) 
     FROM order_items oi2 
     WHERE oi2.order_id = o.order_id) as avg_item_price
FROM orders o
WHERE o.order_date >= '2024-01-01';

-- Ваша оптимизация:
-- TODO: Заменить подзапросы на JOIN с агрегацией
-- TODO: Использовать оконные функции если доступно
```

**3️⃣ Оптимизация GROUP BY и агрегаций**

```sql
-- Исходный медленный запрос 5
-- Проблема: группировка по невыборочным полям
SELECT 
    CONCAT(c.first_name, ' ', c.last_name) as full_name,
    DATE_FORMAT(o.order_date, '%Y-%m') as order_month,
    COUNT(DISTINCT o.order_id) as orders_count,
    SUM(o.total_amount) as monthly_revenue
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_date >= '2023-01-01'
GROUP BY 
    CONCAT(c.first_name, ' ', c.last_name),
    DATE_FORMAT(o.order_date, '%Y-%m')
ORDER BY monthly_revenue DESC;

-- Ваша оптимизация:
-- TODO: Избегать функций в GROUP BY
-- TODO: Использовать более эффективную агрегацию
-- TODO: Добавить LIMIT для больших результатов

-- Исходный медленный запрос 6
-- Проблема: сложная логика в SELECT
SELECT 
    p.category,
    COUNT(*) as products_count,
    AVG(p.price) as avg_price,
    (SELECT COUNT(*) 
     FROM order_items oi2
     JOIN products p2 ON oi2.product_id = p2.product_id  
     WHERE p2.category = p.category) as category_sales_count,
    CASE 
        WHEN AVG(p.price) > 1000 THEN 'Premium'
        WHEN AVG(p.price) > 500 THEN 'Mid-range'  
        ELSE 'Budget'
    END as price_segment
FROM products p
GROUP BY p.category
ORDER BY avg_price DESC;

-- Ваша оптимизация:
-- TODO: Предварительные вычисления в CTE
-- TODO: Материализованные представления
```

**4️⃣ Создание оптимизированных представлений**

```sql
-- Создайте материализованное представление для частых запросов
CREATE VIEW customer_order_summary AS
SELECT 
    c.customer_id,
    c.customer_name,
    c.email,
    c.registration_date,
    COUNT(o.order_id) as total_orders,
    COALESCE(SUM(o.total_amount), 0) as total_spent,
    COALESCE(AVG(o.total_amount), 0) as avg_order_value,
    MAX(o.order_date) as last_order_date,
    MIN(o.order_date) as first_order_date
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE o.status = 'completed' OR o.status IS NULL
GROUP BY c.customer_id, c.customer_name, c.email, c.registration_date;

-- Создайте индексы для представления
CREATE INDEX idx_customer_summary_spent ON customer_order_summary(total_spent);
CREATE INDEX idx_customer_summary_orders ON customer_order_summary(total_orders);

-- Используйте представление для быстрых запросов
SELECT customer_name, total_spent, total_orders
FROM customer_order_summary
WHERE total_spent > 5000
ORDER BY total_spent DESC
LIMIT 50;
```

**5️⃣ Сравнение производительности**

```sql
-- Измерьте время выполнения до и после оптимизации
-- Используйте файл files/performance_comparison_template.sql

-- Запишите результаты в таблицу:
CREATE TABLE optimization_results (
    query_id INTEGER,
    query_description TEXT,
    time_before_ms INTEGER,
    time_after_ms INTEGER,
    improvement_percent REAL,
    optimization_technique TEXT
);

-- Пример записи результата
INSERT INTO optimization_results VALUES 
(1, 'Customer search by email', 1500, 45, 97.0, 'Added index on email');
```

### 📋 Файлы для работы
- `files/slow_queries.sql` — набор медленных запросов
- `files/optimization_solutions.sql` — примеры решений
- `files/performance_comparison_template.sql` — шаблон для замеров

### 🎯 Ожидаемый результат
- Улучшение производительности запросов в 10-100 раз
- Понимание различных техник оптимизации
- Навыки системного подхода к оптимизации

---

## 🔄 Задание 4: Интеграция SQL оптимизации с Power BI и DAX

### 📊 Описание
Создайте оптимизированную связку SQL базы данных и Power BI модели с эффективными DAX мерами, учитывающими принципы оптимизации SQL.

### 🔧 Что нужно сделать

**1️⃣ Создание оптимизированных представлений для Power BI**

```sql
-- Создайте агрегированные представления для быстрой работы Power BI
-- Используйте файл files/powerbi_optimized_views.sql

-- Представление для анализа продаж по времени
CREATE VIEW sales_time_analysis AS
SELECT 
    DATE(o.order_date) as order_date,
    EXTRACT(YEAR FROM o.order_date) as year,
    EXTRACT(MONTH FROM o.order_date) as month,
    EXTRACT(DOW FROM o.order_date) as day_of_week,
    p.category,
    p.subcategory,
    COUNT(DISTINCT o.order_id) as orders_count,
    COUNT(DISTINCT o.customer_id) as customers_count,
    SUM(oi.quantity) as total_quantity,
    SUM(oi.quantity * oi.unit_price) as total_revenue,
    AVG(oi.unit_price) as avg_unit_price
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
WHERE o.status = 'completed'
  AND o.order_date >= DATE('now', '-2 years')
GROUP BY 
    DATE(o.order_date),
    EXTRACT(YEAR FROM o.order_date),
    EXTRACT(MONTH FROM o.order_date), 
    EXTRACT(DOW FROM o.order_date),
    p.category,
    p.subcategory;

-- Представление для клиентского анализа  
CREATE VIEW customer_analytics AS
SELECT 
    c.customer_id,
    c.customer_name,
    c.email,
    c.city,
    c.country,
    c.registration_date,
    c.customer_segment,
    COUNT(o.order_id) as lifetime_orders,
    SUM(o.total_amount) as lifetime_value,
    AVG(o.total_amount) as avg_order_value,
    MAX(o.order_date) as last_order_date,
    MIN(o.order_date) as first_order_date,
    -- RFM компоненты
    julianday('now') - julianday(MAX(o.order_date)) as recency_days,
    COUNT(o.order_id) as frequency,
    SUM(o.total_amount) as monetary
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id AND o.status = 'completed'
GROUP BY 
    c.customer_id, c.customer_name, c.email, c.city, 
    c.country, c.registration_date, c.customer_segment;

-- Создайте индексы для представлений
CREATE INDEX idx_sales_time_date_category ON sales_time_analysis(order_date, category);
CREATE INDEX idx_customer_analytics_segment ON customer_analytics(customer_segment, lifetime_value);
```

**2️⃣ Настройка Power BI модели данных**

```excel
' Откройте файл files/ecommerce_dashboard.pbix
' Настройте подключение к вашей оптимизированной базе данных

' Импортируйте оптимизированные представления:
' - sales_time_analysis  
' - customer_analytics
' - products (основная таблица)
' - categories (справочник)

' Создайте правильные связи между таблицами:
' sales_time_analysis[category] -> categories[category_name]
' customer_analytics[customer_id] -> sales_time_analysis[customer_id] (если есть)

' Настройте типы данных:
' - order_date: Date
' - total_revenue: Currency  
' - lifetime_value: Currency
' - recency_days: Whole Number
```

**3️⃣ Создание оптимизированных DAX мер**

```dax
// Базовые меры, использующие предагрегированные данные
Total Revenue = SUM(sales_time_analysis[total_revenue])

Total Orders = SUM(sales_time_analysis[orders_count])

Average Order Value = 
DIVIDE([Total Revenue], [Total Orders], 0)

// Временные вычисления с оптимизацией
Revenue YoY Growth = 
VAR CurrentYearRevenue = [Total Revenue]
VAR PreviousYearRevenue = 
    CALCULATE(
        [Total Revenue],
        DATEADD(sales_time_analysis[order_date], -1, YEAR)
    )
RETURN
    DIVIDE(CurrentYearRevenue - PreviousYearRevenue, PreviousYearRevenue, 0)

// Клиентские метрики на основе предрасчитанных данных
Active Customers = 
CALCULATE(
    DISTINCTCOUNT(customer_analytics[customer_id]),
    customer_analytics[recency_days] <= 90
)

Customer Lifetime Value = 
AVERAGE(customer_analytics[lifetime_value])

// RFM сегментация на основе SQL данных
RFM Score = 
VAR RecencyScore = 
    SWITCH(
        TRUE(),
        MAX(customer_analytics[recency_days]) <= 30, 5,
        MAX(customer_analytics[recency_days]) <= 60, 4,
        MAX(customer_analytics[recency_days]) <= 90, 3,
        MAX(customer_analytics[recency_days]) <= 180, 2,
        1
    )
VAR FrequencyScore = 
    SWITCH(
        TRUE(),
        MAX(customer_analytics[frequency]) >= 20, 5,
        MAX(customer_analytics[frequency]) >= 10, 4,
        MAX(customer_analytics[frequency]) >= 5, 3,
        MAX(customer_analytics[frequency]) >= 2, 2,
        1
    )
VAR MonetaryScore = 
    SWITCH(
        TRUE(),
        MAX(customer_analytics[monetary]) >= 10000, 5,
        MAX(customer_analytics[monetary]) >= 5000, 4,
        MAX(customer_analytics[monetary]) >= 2000, 3,
        MAX(customer_analytics[monetary]) >= 500, 2,
        1
    )
RETURN
    RecencyScore & FrequencyScore & MonetaryScore

// Продвинутые аналитические меры
Market Basket Size = 
DIVIDE(
    SUM(sales_time_analysis[total_quantity]),
    SUM(sales_time_analysis[orders_count]),
    0
)

Customer Retention Rate = 
VAR CustomersThisMonth = 
    CALCULATE(
        DISTINCTCOUNT(customer_analytics[customer_id]),
        FILTER(
            customer_analytics,
            customer_analytics[last_order_date] >= DATE(YEAR(TODAY()), MONTH(TODAY()), 1)
        )
    )
VAR CustomersPrevMonth = 
    CALCULATE(
        DISTINCTCOUNT(customer_analytics[customer_id]),
        FILTER(
            customer_analytics,
            customer_analytics[last_order_date] >= DATE(YEAR(TODAY()), MONTH(TODAY())-1, 1) &&
            customer_analytics[last_order_date] < DATE(YEAR(TODAY()), MONTH(TODAY()), 1)
        )
    )
RETURN
    DIVIDE(CustomersThisMonth, CustomersPrevMonth, 0) - 1
```

**4️⃣ Мониторинг производительности Power BI**

```dax
// Создайте меры для мониторинга производительности модели
Data Refresh Time = 
"Последнее обновление: " & FORMAT(NOW(), "DD.MM.YYYY HH:mm")

Model Size Info = 
"Строк в модели: " & 
FORMAT(
    SUMX(
        VALUES(sales_time_analysis[order_date]),
        1
    ) +
    SUMX(
        VALUES(customer_analytics[customer_id]), 
        1
    ),
    "#,##0"
)

// Создайте страницу диагностики в Power BI
// со следующими визуалами:
// 1. Карточка с временем обновления данных
// 2. Таблица с количеством записей по таблицам  
// 3. График производительности мер (если доступно)
```

**5️⃣ Сравнение производительности до и после оптимизации**

```excel
' Создайте два подключения к Power BI:
' 1. К исходным таблицам (без оптимизации)
' 2. К оптимизированным представлениям

' Сравните:
' - Время загрузки данных в модель
' - Время отклика визуалов при фильтрации
' - Размер модели данных в памяти
' - Производительность сложных вычислений

' Запишите результаты в files/powerbi_performance_comparison.xlsx
```

**6️⃣ Автоматизация обновления оптимизированных представлений**

```python
# Создайте скрипт для автоматического обновления представлений
# Используйте файл files/automated_view_refresh.py

import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import schedule
import time

def refresh_analytical_views():
    """Обновление аналитических представлений"""
    
    conn = sqlite3.connect('files/ecommerce_performance.db')
    
    # Удаляем и пересоздаем представления с новыми данными
    refresh_queries = [
        "DROP VIEW IF EXISTS sales_time_analysis",
        "DROP VIEW IF EXISTS customer_analytics",
        # Здесь добавить CREATE VIEW запросы из пункта 1
    ]
    
    for query in refresh_queries:
        conn.execute(query)
    
    conn.commit()
    conn.close()
    
    print(f"Представления обновлены: {datetime.now()}")

# Настройка расписания обновления
schedule.every().hour.do(refresh_analytical_views)  # Каждый час
schedule.every().day.at("06:00").do(refresh_analytical_views)  # Каждый день в 6 утра

while True:
    schedule.run_pending()
    time.sleep(60)  # Проверка каждую минуту
```

### 📋 Файлы для работы
- `files/powerbi_optimized_views.sql` — SQL для создания представлений
- `files/ecommerce_dashboard.pbix` — Power BI файл
- `files/powerbi_performance_comparison.xlsx` — сравнение производительности
- `files/automated_view_refresh.py` — автоматизация обновления

### 🎯 Ожидаемый результат
- Значительно более быстрая работа Power BI дашбордов
- Эффективные DAX меры, использующие оптимизированные SQL данные
- Автоматизированная система обновления аналитических представлений

---

## 📊 Задание 5: Мониторинг и поддержка производительности

### 📊 Описание
Создайте систему мониторинга производительности базы данных с автоматическими уведомлениями о проблемах и регулярным обслуживанием.

### 🔧 Что нужно сделать

**1️⃣ Создание системы логирования производительности**

```sql
-- Создайте таблицы для мониторинга производительности
-- Используйте файл files/monitoring_schema.sql

CREATE TABLE query_performance_log (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    log_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    query_hash TEXT,
    query_text TEXT,
    execution_time_ms INTEGER,
    rows_examined INTEGER,
    rows_returned INTEGER,
    index_usage TEXT,
    optimization_suggestions TEXT
);

CREATE TABLE daily_performance_stats (
    stat_date DATE PRIMARY KEY,
    total_queries INTEGER,
    avg_query_time_ms REAL,
    slow_queries_count INTEGER,
    cache_hit_ratio REAL,
    index_usage_ratio REAL,
    db_size_mb REAL
);

CREATE TABLE performance_alerts (
    alert_id INTEGER PRIMARY KEY AUTOINCREMENT,
    alert_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    alert_type TEXT,
    severity TEXT, -- 'LOW', 'MEDIUM', 'HIGH', 'CRITICAL'
    description TEXT,
    query_details TEXT,
    is_resolved BOOLEAN DEFAULT FALSE,
    resolution_notes TEXT
);
```

**2️⃣ Реализация автоматического мониторинга**

```python
# Создайте систему мониторинга производительности
# Используйте файл files/performance_monitor.py

import sqlite3
import time
import json
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText

class DatabasePerformanceMonitor:
    def __init__(self, db_path):
        self.db_path = db_path
        self.alert_thresholds = {
            'slow_query_ms': 5000,      # > 5 секунд
            'high_cpu_percent': 80,      # > 80% CPU
            'cache_hit_ratio': 0.85,     # < 85% cache hit
            'connection_count': 50       # > 50 соединений
        }
    
    def log_query_performance(self, query, execution_time_ms, rows_examined, rows_returned):
        """Логирование производительности запроса"""
        conn = sqlite3.connect(self.db_path)
        
        query_hash = hash(query) % 1000000  # Простой хэш
        
        conn.execute("""
            INSERT INTO query_performance_log 
            (query_hash, query_text, execution_time_ms, rows_examined, rows_returned)
            VALUES (?, ?, ?, ?, ?)
        """, (query_hash, query[:500], execution_time_ms, rows_examined, rows_returned))
        
        # Проверка на медленные запросы
        if execution_time_ms > self.alert_thresholds['slow_query_ms']:
            self.create_alert('SLOW_QUERY', 'HIGH', 
                            f'Медленный запрос: {execution_time_ms}ms', query[:200])
        
        conn.commit()
        conn.close()
    
    def collect_daily_stats(self):
        """Сбор ежедневной статистики"""
        conn = sqlite3.connect(self.db_path)
        
        # Статистика за вчера
        yesterday = (datetime.now() - timedelta(days=1)).date()
        
        stats = conn.execute("""
            SELECT 
                COUNT(*) as total_queries,
                AVG(execution_time_ms) as avg_query_time,
                COUNT(CASE WHEN execution_time_ms > ? THEN 1 END) as slow_queries,
                ? as db_size_mb
            FROM query_performance_log
            WHERE DATE(log_timestamp) = ?
        """, (self.alert_thresholds['slow_query_ms'], 
              self.get_db_size_mb(), yesterday)).fetchone()
        
        conn.execute("""
            INSERT OR REPLACE INTO daily_performance_stats
            (stat_date, total_queries, avg_query_time_ms, slow_queries_count, db_size_mb)
            VALUES (?, ?, ?, ?, ?)
        """, (yesterday, stats[0], stats[1], stats[2], stats[3]))
        
        conn.commit()
        conn.close()
        
        # Проверка трендов
        self.analyze_performance_trends()
    
    def create_alert(self, alert_type, severity, description, query_details=""):
        """Создание алерта о проблеме"""
        conn = sqlite3.connect(self.db_path)
        
        conn.execute("""
            INSERT INTO performance_alerts
            (alert_type, severity, description, query_details)
            VALUES (?, ?, ?, ?)
        """, (alert_type, severity, description, query_details))
        
        conn.commit()
        conn.close()
        
        # Отправка уведомления при критических алертах
        if severity in ['HIGH', 'CRITICAL']:
            self.send_alert_notification(alert_type, severity, description)
    
    def analyze_performance_trends(self):
        """Анализ трендов производительности"""
        conn = sqlite3.connect(self.db_path)
        
        # Получение статистики за последние 7 дней
        week_stats = conn.execute("""
            SELECT stat_date, avg_query_time_ms, slow_queries_count
            FROM daily_performance_stats
            WHERE stat_date >= DATE('now', '-7 days')
            ORDER BY stat_date
        """).fetchall()
        
        if len(week_stats) >= 7:
            # Анализ тренда времени выполнения
            recent_avg = sum(row[1] for row in week_stats[-3:]) / 3
            previous_avg = sum(row[1] for row in week_stats[:3]) / 3
            
            if recent_avg > previous_avg * 1.5:  # Ухудшение на 50%
                self.create_alert('PERFORMANCE_DEGRADATION', 'MEDIUM',
                                f'Производительность ухудшилась: {recent_avg:.1f}ms vs {previous_avg:.1f}ms')
        
        conn.close()
    
    def get_optimization_suggestions(self):
        """Анализ и предложения по оптимизации"""
        conn = sqlite3.connect(self.db_path)
        
        # Поиск часто выполняемых медленных запросов
        slow_queries = conn.execute("""
            SELECT 
                query_hash,
                COUNT(*) as execution_count,
                AVG(execution_time_ms) as avg_time,
                MAX(execution_time_ms) as max_time,
                substr(query_text, 1, 100) as query_sample
            FROM query_performance_log
            WHERE execution_time_ms > ?
              AND log_timestamp >= DATE('now', '-7 days')
            GROUP BY query_hash
            HAVING COUNT(*) >= 10
            ORDER BY execution_count * avg_time DESC
            LIMIT 5
        """, (1000,)).fetchall()  # > 1 секунды
        
        suggestions = []
        for query in slow_queries:
            suggestion = f"""
            Медленный запрос (выполнялся {query[1]} раз):
            Среднее время: {query[2]:.0f}ms
            Максимальное время: {query[3]:.0f}ms
            Пример: {query[4]}...
            
            Рекомендации:
            - Проверить план выполнения с EXPLAIN
            - Добавить индексы на столбцы в WHERE/JOIN
            - Рассмотреть денормализацию для частых запросов
            """
            suggestions.append(suggestion)
        
        conn.close()
        return suggestions
    
    def send_alert_notification(self, alert_type, severity, description):
        """Отправка уведомлений о критических проблемах"""
        # Здесь реализация отправки email/Slack/Telegram уведомлений
        print(f"🚨 ALERT [{severity}] {alert_type}: {description}")
        
        # Пример отправки email (настройте SMTP параметры)
        # msg = MIMEText(f"Database Performance Alert:\n{description}")
        # msg['Subject'] = f"DB Alert: {alert_type}"
        # msg['From'] = "monitoring@company.com"  
        # msg['To'] = "dba@company.com"
        # smtp_server.send_message(msg)
    
    def get_db_size_mb(self):
        """Получение размера базы данных"""
        import os
        try:
            size_bytes = os.path.getsize(self.db_path)
            return round(size_bytes / (1024 * 1024), 2)
        except:
            return 0

# Использование монитора
monitor = DatabasePerformanceMonitor('files/ecommerce_performance.db')
monitor.collect_daily_stats()
suggestions = monitor.get_optimization_suggestions()
for suggestion in suggestions:
    print(suggestion)
```

**3️⃣ Создание дашборда мониторинга**

```sql
-- Создайте представления для дашборда мониторинга
CREATE VIEW performance_dashboard AS
SELECT 
    DATE(log_timestamp) as date,
    COUNT(*) as total_queries,
    ROUND(AVG(execution_time_ms), 2) as avg_execution_time,
    MAX(execution_time_ms) as max_execution_time,
    COUNT(CASE WHEN execution_time_ms > 5000 THEN 1 END) as slow_queries,
    COUNT(CASE WHEN execution_time_ms > 10000 THEN 1 END) as very_slow_queries,
    ROUND(COUNT(CASE WHEN execution_time_ms > 5000 THEN 1 END) * 100.0 / COUNT(*), 2) as slow_query_percent
FROM query_performance_log
WHERE log_timestamp >= DATE('now', '-30 days')
GROUP BY DATE(log_timestamp)
ORDER BY date DESC;

CREATE VIEW alert_summary AS  
SELECT 
    alert_type,
    severity,
    COUNT(*) as alert_count,
    MAX(alert_timestamp) as last_alert,
    COUNT(CASE WHEN is_resolved = 0 THEN 1 END) as unresolved_count
FROM performance_alerts
WHERE alert_timestamp >= DATE('now', '-7 days')
GROUP BY alert_type, severity
ORDER BY 
    CASE severity 
        WHEN 'CRITICAL' THEN 1
        WHEN 'HIGH' THEN 2  
        WHEN 'MEDIUM' THEN 3
        ELSE 4
    END,
    alert_count DESC;
```

**4️⃣ Автоматическое обслуживание базы данных**

```python
# Создайте систему автоматического обслуживания
# Используйте файл files/database_maintenance.py

import sqlite3
import schedule
import time
from datetime import datetime, timedelta

class DatabaseMaintenance:
    def __init__(self, db_path):
        self.db_path = db_path
    
    def update_statistics(self):
        """Обновление статистик для оптимизатора"""
        conn = sqlite3.connect(self.db_path)
        
        # В SQLite статистика обновляется командой ANALYZE
        conn.execute("ANALYZE")
        conn.commit()
        conn.close()
        
        print(f"✅ Статистика обновлена: {datetime.now()}")
    
    def cleanup_old_logs(self, days_to_keep=30):
        """Очистка старых логов производительности"""
        conn = sqlite3.connect(self.db_path)
        
        cutoff_date = datetime.now() - timedelta(days=days_to_keep)
        
        # Удаление старых логов запросов
        deleted_logs = conn.execute("""
            DELETE FROM query_performance_log
            WHERE log_timestamp < ?
        """, (cutoff_date,)).rowcount
        
        # Удаление решенных алертов старше 7 дней  
        deleted_alerts = conn.execute("""
            DELETE FROM performance_alerts
            WHERE is_resolved = 1 
              AND alert_timestamp < ?
        """, (datetime.now() - timedelta(days=7),)).rowcount
        
        conn.commit()
        conn.close()
        
        print(f"🧹 Очистка завершена: удалено {deleted_logs} логов, {deleted_alerts} алертов")
    
    def vacuum_database(self):
        """Дефрагментация базы данных"""
        conn = sqlite3.connect(self.db_path)
        
        # Получение размера до оптимизации
        size_before = self.get_db_size_mb()
        
        # Выполнение VACUUM для дефрагментации
        conn.execute("VACUUM")
        conn.close()
        
        size_after = self.get_db_size_mb()
        saved_mb = size_before - size_after
        
        print(f"🗜️ Дефрагментация завершена: было {size_before}MB, стало {size_after}MB (сэкономлено {saved_mb}MB)")
    
    def check_index_usage(self):
        """Анализ использования индексов"""
        conn = sqlite3.connect(self.db_path)
        
        # Получение списка всех индексов
        indexes = conn.execute("""
            SELECT name, sql 
            FROM sqlite_master 
            WHERE type = 'index' 
              AND name NOT LIKE 'sqlite_autoindex%'
        """).fetchall()
        
        print(f"📊 Найдено {len(indexes)} пользовательских индексов")
        
        # В реальной системе здесь был бы анализ статистики использования
        # Для SQLite можно анализировать планы выполнения популярных запросов
        
        conn.close()
    
    def generate_maintenance_report(self):
        """Генерация отчета об обслуживании"""
        conn = sqlite3.connect(self.db_path)
        
        # Общая статистика
        stats = conn.execute("""
            SELECT 
                (SELECT COUNT(*) FROM query_performance_log) as total_logged_queries,
                (SELECT COUNT(*) FROM performance_alerts WHERE is_resolved = 0) as open_alerts,
                (SELECT AVG(avg_query_time_ms) FROM daily_performance_stats WHERE stat_date >= DATE('now', '-7 days')) as avg_week_time,
                (SELECT db_size_mb FROM daily_performance_stats ORDER BY stat_date DESC LIMIT 1) as current_db_size
        """).fetchone()
        
        report = f"""
        📋 ОТЧЕТ ОБ ОБСЛУЖИВАНИИ БД - {datetime.now().strftime('%Y-%m-%d %H:%M')}
        {'='*60}
        
        📊 Общая статистика:
        - Всего логов запросов: {stats[0]:,}
        - Открытых алертов: {stats[1]}
        - Среднее время запроса (7 дней): {stats[2]:.1f}ms
        - Размер БД: {stats[3]}MB
        
        ✅ Выполненные операции обслуживания:
        - Обновление статистик оптимизатора
        - Очистка устаревших логов  
        - Дефрагментация базы данных
        - Анализ использования индексов
        
        🔍 Следующие действия:
        - Регулярный мониторинг производительности
        - Анализ медленных запросов
        - Проверка роста размера БД
        """
        
        print(report)
        
        # Сохранение отчета в файл
        with open(f'maintenance_report_{datetime.now().strftime("%Y%m%d")}.txt', 'w', encoding='utf-8') as f:
            f.write(report)
        
        conn.close()
    
    def get_db_size_mb(self):
        """Получение размера БД в мегабайтах"""
        import os
        try:
            size_bytes = os.path.getsize(self.db_path)
            return round(size_bytes / (1024 * 1024), 2)
        except:
            return 0

# Настройка автоматического обслуживания
maintenance = DatabaseMaintenance('files/ecommerce_performance.db')

# Расписание обслуживания
schedule.every().day.at("02:00").do(maintenance.update_statistics)
schedule.every().day.at("03:00").do(maintenance.cleanup_old_logs)  
schedule.every().sunday.at("04:00").do(maintenance.vacuum_database)
schedule.every().monday.at("09:00").do(maintenance.generate_maintenance_report)

print("🔧 Система автоматического обслуживания запущена")
print("📅 Расписание:")
print("   - 02:00 ежедневно: обновление статистик")
print("   - 03:00 ежедневно: очистка старых логов")  
print("   - 04:00 по воскресеньям: дефрагментация")
print("   - 09:00 по понедельникам: генерация отчета")

# Запуск планировщика
while True:
    schedule.run_pending()
    time.sleep(3600)  # Проверка каждый час
```

**5️⃣ Создание системы алертов и уведомлений**

```python
# Реализация системы уведомлений
# Используйте файл files/alert_system.py

import requests
import json
from datetime import datetime

class AlertSystem:
    def __init__(self):
        self.telegram_bot_token = "YOUR_BOT_TOKEN"
        self.telegram_chat_id = "YOUR_CHAT_ID"  
        self.slack_webhook_url = "YOUR_SLACK_WEBHOOK"
    
    def send_telegram_alert(self, message):
        """Отправка алерта в Telegram"""
        url = f"https://api.telegram.org/bot{self.telegram_bot_token}/sendMessage"
        
        payload = {
            'chat_id': self.telegram_chat_id,
            'text': f"🚨 Database Alert\n\n{message}",
            'parse_mode': 'HTML'
        }
        
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                print("✅ Telegram уведомление отправлено")
            else:
                print(f"❌ Ошибка Telegram: {response.status_code}")
        except Exception as e:
            print(f"❌ Ошибка отправки в Telegram: {e}")
    
    def send_slack_alert(self, message, severity="warning"):
        """Отправка алерта в Slack"""
        color_map = {
            "good": "#36a64f",     # зеленый  
            "warning": "#ff9500",   # оранжевый
            "danger": "#ff0000"     # красный
        }
        
        payload = {
            "attachments": [
                {
                    "color": color_map.get(severity, "#ff9500"),
                    "fields": [
                        {
                            "title": "Database Performance Alert",
                            "value": message,
                            "short": False
                        }
                    ],
                    "footer": "DB Monitoring System",
                    "ts": int(datetime.now().timestamp())
                }
            ]
        }
        
        try:
            response = requests.post(self.slack_webhook_url, json=payload)
            if response.status_code == 200:
                print("✅ Slack уведомление отправлено")
            else:
                print(f"❌ Ошибка Slack: {response.status_code}")
        except Exception as e:
            print(f"❌ Ошибка отправки в Slack: {e}")
    
    def process_critical_alert(self, alert_type, description, query_details=""):
        """Обработка критических алертов"""
        
        message = f"""
        <b>Тип:</b> {alert_type}
        <b>Время:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        <b>Описание:</b> {description}
        
        {query_details[:200] + '...' if len(query_details) > 200 else query_details}
        """
        
        # Отправка в несколько каналов для критических алертов
        self.send_telegram_alert(message)
        self.send_slack_alert(description, "danger")
        
        # Логирование в файл
        with open('critical_alerts.log', 'a', encoding='utf-8') as f:
            f.write(f"{datetime.now().isoformat()} - {alert_type}: {description}\n")

# Интеграция с системой мониторинга
alert_system = AlertSystem()

def enhanced_create_alert(alert_type, severity, description, query_details=""):
    """Улучшенная функция создания алертов"""
    
    # Сохранение в БД (как в предыдущем коде)
    conn = sqlite3.connect('files/ecommerce_performance.db')
    conn.execute("""
        INSERT INTO performance_alerts
        (alert_type, severity, description, query_details)
        VALUES (?, ?, ?, ?)
    """, (alert_type, severity, description, query_details))
    conn.commit()
    conn.close()
    
    # Отправка уведомлений для важных алертов
    if severity in ['HIGH', 'CRITICAL']:
        alert_system.process_critical_alert(alert_type, description, query_details)
    
    print(f"📝 Алерт создан: [{severity}] {alert_type}")
```

### 📋 Файлы для работы
- `files/monitoring_schema.sql` — схема таблиц мониторинга
- `files/performance_monitor.py` — основная система мониторинга
- `files/database_maintenance.py` — автоматическое обслуживание
- `files/alert_system.py` — система уведомлений

### 🎯 Ожидаемый результат
- Полноценная система мониторинга производительности БД
- Автоматические уведомления о проблемах
- Регулярное обслуживание для поддержания производительности
- Исторические данные для анализа трендов

---

✅ [Перейти к чек-листу](checklist.md)

---

- 🔙 [Предыдущая глава: Глава 21: - Реляционные модели данных и индексы](../chapter-21/README.md)
- 🔜 [Следующая глава: Глава 23: Презентация результатов: storytelling, отчёты](../chapter-23/README.md)

---

- 📢 Присоединяйтесь к чату курса: https://t.me/analytics_course_chat
- 📢 Канал курса: https://t.me/analytics_course_channel