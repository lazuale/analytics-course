-- ========================================
-- СКРИПТ УДАЛЕНИЯ ИНДЕКСОВ
-- Для демонстрации производительности без оптимизации
-- ========================================

-- ========================================
-- ПОЛУЧЕНИЕ СПИСКА ВСЕХ ПОЛЬЗОВАТЕЛЬСКИХ ИНДЕКСОВ
-- ========================================

-- Просмотр всех существующих индексов (кроме автоматических)
SELECT 
    name,
    sql
FROM sqlite_master 
WHERE type = 'index' 
  AND name NOT LIKE 'sqlite_autoindex%'
  AND name NOT LIKE '%_pk'
ORDER BY name;

-- ========================================
-- УДАЛЕНИЕ ВСЕХ ПОЛЬЗОВАТЕЛЬСКИХ ИНДЕКСОВ
-- ========================================

-- ВНИМАНИЕ: Этот скрипт удаляет ВСЕ созданные индексы!
-- Используйте только для получения baseline производительности

-- Удаление индексов на таблице customers
DROP INDEX IF EXISTS idx_customers_email;
DROP INDEX IF EXISTS idx_customers_country;
DROP INDEX IF EXISTS idx_customers_segment;
DROP INDEX IF EXISTS idx_customers_active;
DROP INDEX IF EXISTS idx_customers_covering;
DROP INDEX IF EXISTS idx_customers_premium_active;

-- Удаление индексов на таблице products
DROP INDEX IF EXISTS idx_products_category;
DROP INDEX IF EXISTS idx_products_in_stock;
DROP INDEX IF EXISTS idx_products_price;
DROP INDEX IF EXISTS idx_products_category_price;
DROP INDEX IF EXISTS idx_products_covering_analysis;

-- Удаление индексов на таблице orders
DROP INDEX IF EXISTS idx_orders_customer_id;
DROP INDEX IF EXISTS idx_orders_date;
DROP INDEX IF EXISTS idx_orders_status;
DROP INDEX IF EXISTS idx_orders_customer_date;
DROP INDEX IF EXISTS idx_orders_date_status;
DROP INDEX IF EXISTS idx_orders_amount;
DROP INDEX IF EXISTS idx_orders_covering_sales;
DROP INDEX IF EXISTS idx_orders_delivered;
DROP INDEX IF EXISTS idx_orders_high_value;

-- Удаление индексов на таблице order_items
DROP INDEX IF EXISTS idx_order_items_order_id;
DROP INDEX IF EXISTS idx_order_items_product_id;
DROP INDEX IF EXISTS idx_order_items_order_product;
DROP INDEX IF EXISTS idx_order_items_quantity;

-- ========================================
-- ПРОВЕРКА РЕЗУЛЬТАТА УДАЛЕНИЯ
-- ========================================

-- Проверяем, что остались только автоматические индексы
SELECT 
    'После удаления остались индексы:' as info,
    name,
    sql
FROM sqlite_master 
WHERE type = 'index' 
  AND name NOT LIKE 'sqlite_autoindex%'
ORDER BY name;

-- Если результат пустой - все пользовательские индексы удалены

-- ========================================
-- ИЗМЕРЕНИЕ ПРОИЗВОДИТЕЛЬНОСТИ БЕЗ ИНДЕКСОВ
-- ========================================

-- Включаем измерение времени
.timer on

-- Тест 1: Поиск клиента по email (медленно без индекса)
.print "Тест 1: Поиск по email без индекса"
SELECT customer_id, customer_name, email
FROM customers 
WHERE email = 'customer1@gmail.com';

-- Тест 2: JOIN без индексов на внешних ключах (очень медленно)
.print "Тест 2: JOIN без индексов"
SELECT c.customer_name, COUNT(o.order_id) as order_count
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.customer_name
ORDER BY order_count DESC
LIMIT 10;

-- Тест 3: Фильтрация по дате без индекса (медленно)
.print "Тест 3: Фильтрация по дате без индекса"
SELECT COUNT(*) as orders_count, AVG(total_amount) as avg_amount
FROM orders
WHERE order_date >= '2024-01-01';

-- Тест 4: Сложная агрегация без индексов (очень медленно)
.print "Тест 4: Сложная агрегация без индексов"
SELECT 
    country,
    COUNT(DISTINCT c.customer_id) as customers,
    COUNT(o.order_id) as orders,
    SUM(o.total_amount) as revenue
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_date >= '2024-01-01'
GROUP BY country
ORDER BY revenue DESC;

-- ========================================
-- АНАЛИЗ ПЛАНОВ ВЫПОЛНЕНИЯ БЕЗ ИНДЕКСОВ
-- ========================================

-- Анализ плана для JOIN без индексов
.print "План выполнения JOIN без индексов:"
EXPLAIN QUERY PLAN
SELECT c.customer_name, o.order_date, o.total_amount
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE c.country = 'Russia'
ORDER BY o.order_date DESC;

-- Анализ плана для поиска без индекса
.print "План выполнения поиска без индекса:"
EXPLAIN QUERY PLAN
SELECT * FROM customers 
WHERE email LIKE '%gmail%';

-- ========================================
-- ИНСТРУКЦИИ ПО ВОССТАНОВЛЕНИЮ ИНДЕКСОВ
-- ========================================

/*
После тестирования производительности без индексов:

1. Запустите файл index_creation_script.sql для создания индексов:
   .read index_creation_script.sql

2. Повторите те же тесты для сравнения производительности

3. Запишите результаты в файл performance_comparison_template.xlsx

4. Проанализируйте улучшения производительности

ОЖИДАЕМЫЕ РЕЗУЛЬТАТЫ:
- Поиск по email: улучшение в 10-100 раз
- JOIN операции: улучшение в 5-50 раз  
- Фильтрация по дате: улучшение в 3-20 раз
- Сложные запросы: улучшение в 10-1000 раз

ВАЖНО: 
Не оставляйте базу данных без индексов в production среде!
Это только для демонстрации разницы в производительности.
*/

-- ========================================
-- АВТОМАТИЧЕСКОЕ ВОССТАНОВЛЕНИЕ ИНДЕКСОВ
-- ========================================

-- Раскомментируйте эту строку для автоматического восстановления:
-- .read index_creation_script.sql

.print "Скрипт удаления индексов выполнен."
.print "Для восстановления запустите: .read index_creation_script.sql"