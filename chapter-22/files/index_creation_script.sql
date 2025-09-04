-- ========================================
-- СКРИПТ СОЗДАНИЯ ОПТИМАЛЬНЫХ ИНДЕКСОВ
-- Для улучшения производительности запросов
-- ========================================

-- ========================================
-- 1. ИНДЕКСЫ ДЛЯ ПОИСКА И ФИЛЬТРАЦИИ
-- ========================================

-- Индекс для поиска клиентов по email
CREATE INDEX IF NOT EXISTS idx_customers_email ON customers(email);

-- Индекс для фильтрации по стране
CREATE INDEX IF NOT EXISTS idx_customers_country ON customers(country);

-- Индекс для поиска по сегменту клиентов
CREATE INDEX IF NOT EXISTS idx_customers_segment ON customers(customer_segment);

-- Индекс для фильтрации активных клиентов
CREATE INDEX IF NOT EXISTS idx_customers_active ON customers(is_active) WHERE is_active = 1;

-- ========================================
-- 2. ИНДЕКСЫ ДЛЯ ТОВАРОВ
-- ========================================

-- Индекс для поиска по категории
CREATE INDEX IF NOT EXISTS idx_products_category ON products(category);

-- Индекс для фильтрации товаров в наличии
CREATE INDEX IF NOT EXISTS idx_products_in_stock ON products(in_stock) WHERE in_stock = 1;

-- Индекс для поиска по ценовому диапазону
CREATE INDEX IF NOT EXISTS idx_products_price ON products(price);

-- Составной индекс категория + цена
CREATE INDEX IF NOT EXISTS idx_products_category_price ON products(category, price);

-- ========================================
-- 3. ИНДЕКСЫ ДЛЯ ЗАКАЗОВ
-- ========================================

-- КРИТИЧЕСКИ ВАЖНЫЙ: индекс на внешний ключ для JOIN
CREATE INDEX IF NOT EXISTS idx_orders_customer_id ON orders(customer_id);

-- Индекс для фильтрации по дате заказов
CREATE INDEX IF NOT EXISTS idx_orders_date ON orders(order_date);

-- Индекс для фильтрации по статусу
CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(status);

-- Составной индекс для временного анализа по клиентам
CREATE INDEX IF NOT EXISTS idx_orders_customer_date ON orders(customer_id, order_date);

-- Составной индекс для анализа статусов по датам
CREATE INDEX IF NOT EXISTS idx_orders_date_status ON orders(order_date, status);

-- Индекс для поиска по сумме заказов
CREATE INDEX IF NOT EXISTS idx_orders_amount ON orders(total_amount);

-- ========================================
-- 4. ИНДЕКСЫ ДЛЯ ПОЗИЦИЙ ЗАКАЗОВ
-- ========================================

-- КРИТИЧЕСКИ ВАЖНЫЕ: индексы на внешние ключи для JOIN
CREATE INDEX IF NOT EXISTS idx_order_items_order_id ON order_items(order_id);
CREATE INDEX IF NOT EXISTS idx_order_items_product_id ON order_items(product_id);

-- Составной индекс для связи заказ-товар
CREATE INDEX IF NOT EXISTS idx_order_items_order_product ON order_items(order_id, product_id);

-- Индекс для анализа количества
CREATE INDEX IF NOT EXISTS idx_order_items_quantity ON order_items(quantity);

-- ========================================
-- 5. ПОКРЫВАЮЩИЕ ИНДЕКСЫ
-- ========================================

-- Покрывающий индекс для частых запросов клиентов
CREATE INDEX IF NOT EXISTS idx_customers_covering 
ON customers(customer_segment, customer_id, customer_name, email, country);

-- Покрывающий индекс для анализа продаж
CREATE INDEX IF NOT EXISTS idx_orders_covering_sales 
ON orders(order_date, customer_id, total_amount, status);

-- Покрывающий индекс для товарного анализа
CREATE INDEX IF NOT EXISTS idx_products_covering_analysis 
ON products(category, product_id, product_name, price, in_stock);

-- ========================================
-- 6. ФУНКЦИОНАЛЬНЫЕ ИНДЕКСЫ (для некоторых СУБД)
-- ========================================

-- Индекс для поиска по верхнему регистру email (PostgreSQL/MySQL)
-- CREATE INDEX idx_customers_email_upper ON customers(UPPER(email));

-- Индекс для группировки по году заказа (PostgreSQL)  
-- CREATE INDEX idx_orders_year ON orders(EXTRACT(YEAR FROM order_date));

-- Индекс для группировки по месяцу (PostgreSQL)
-- CREATE INDEX idx_orders_month ON orders(DATE_TRUNC('month', order_date));

-- ========================================
-- 7. ЧАСТИЧНЫЕ ИНДЕКСЫ (для экономии места)
-- ========================================

-- Индекс только для доставленных заказов
CREATE INDEX IF NOT EXISTS idx_orders_delivered 
ON orders(customer_id, order_date) 
WHERE status = 'delivered';

-- Индекс только для дорогих заказов
CREATE INDEX IF NOT EXISTS idx_orders_high_value 
ON orders(customer_id, order_date) 
WHERE total_amount > 5000;

-- Индекс только для активных клиентов премиум сегмента
CREATE INDEX IF NOT EXISTS idx_customers_premium_active 
ON customers(registration_date) 
WHERE customer_segment = 'Premium' AND is_active = 1;

-- ========================================
-- 8. ПРОВЕРКА СОЗДАННЫХ ИНДЕКСОВ
-- ========================================

-- Просмотр всех созданных индексов
SELECT 
    name as index_name,
    sql as index_definition
FROM sqlite_master 
WHERE type = 'index' 
  AND name NOT LIKE 'sqlite_autoindex%'
ORDER BY name;

-- ========================================
-- 9. РЕКОМЕНДАЦИИ ПО ИСПОЛЬЗОВАНИЮ
-- ========================================

/*
ПРАВИЛА ЭФФЕКТИВНОГО ИСПОЛЬЗОВАНИЯ ИНДЕКСОВ:

1. СЕЛЕКТИВНОСТЬ
   - Создавайте индексы на столбцы с высокой селективностью
   - Избегайте индексов на столбцы с малым количеством уникальных значений

2. ПОРЯДОК СТОЛБЦОВ В СОСТАВНЫХ ИНДЕКСАХ
   - Самый селективный столбец — первый
   - Столбцы в WHERE условиях — перед столбцами в ORDER BY

3. ПОКРЫВАЮЩИЕ ИНДЕКСЫ
   - Включайте все столбцы из SELECT, WHERE, ORDER BY
   - Особенно эффективны для частых запросов

4. ОБСЛУЖИВАНИЕ
   - Регулярно обновляйте статистику: ANALYZE
   - Мониторьте использование: неиспользуемые индексы удаляйте
   - Следите за фрагментацией: перестраивайте при необходимости

5. КОМПРОМИССЫ
   - Индексы ускоряют SELECT, но замедляют INSERT/UPDATE/DELETE
   - Занимают дополнительное место на диске
   - Требуют обслуживания
*/

-- ========================================
-- 10. ТЕСТОВЫЕ ЗАПРОСЫ ДЛЯ ПРОВЕРКИ
-- ========================================

-- Тест 1: Поиск клиента по email (должен использовать idx_customers_email)
EXPLAIN QUERY PLAN
SELECT customer_id, customer_name 
FROM customers 
WHERE email = 'customer1@gmail.com';

-- Тест 2: JOIN заказов и клиентов (должен использовать idx_orders_customer_id)
EXPLAIN QUERY PLAN
SELECT c.customer_name, COUNT(o.order_id) as order_count
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.customer_name;

-- Тест 3: Фильтрация по дате (должен использовать idx_orders_date)
EXPLAIN QUERY PLAN
SELECT * FROM orders 
WHERE order_date >= '2024-01-01' 
ORDER BY order_date DESC;

-- Тест 4: Сложный многотабличный запрос
EXPLAIN QUERY PLAN
SELECT 
    c.customer_name,
    p.product_name,
    oi.quantity,
    o.order_date
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN order_items oi ON o.order_id = oi.order_id  
JOIN products p ON oi.product_id = p.product_id
WHERE o.order_date >= '2024-01-01'
  AND c.country = 'Russia'
ORDER BY o.order_date DESC;

-- Конец скрипта
ANALYZE;