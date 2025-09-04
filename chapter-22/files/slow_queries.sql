
-- ========================================
-- МЕДЛЕННЫЕ ЗАПРОСЫ ДЛЯ ДЕМОНСТРАЦИИ ПРОБЛЕМ ПРОИЗВОДИТЕЛЬНОСТИ
-- ========================================

-- Запрос 1: Поиск по email с функцией (блокирует использование индекса)
-- ПРОБЛЕМА: UPPER() в WHERE блокирует использование индексов
SELECT customer_id, customer_name, email, registration_date
FROM customers 
WHERE UPPER(email) LIKE '%GMAIL%'
  AND is_active = 1;

-- Запрос 2: JOIN без индексов на внешних ключах
-- ПРОБЛЕМА: отсутствуют индексы на customer_id в orders
SELECT 
    c.customer_name,
    c.country,
    COUNT(o.order_id) as total_orders,
    SUM(o.total_amount) as total_spent
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE c.registration_date >= '2023-01-01'
GROUP BY c.customer_id, c.customer_name, c.country
ORDER BY total_spent DESC;

-- Запрос 3: Сложная агрегация без подходящих индексов
-- ПРОБЛЕМА: GROUP BY по DATE() без функционального индекса
SELECT 
    DATE(o.order_date) as order_day,
    COUNT(DISTINCT o.customer_id) as unique_customers,
    COUNT(o.order_id) as total_orders,
    SUM(o.total_amount) as daily_revenue
FROM orders o
WHERE o.status = 'delivered'
  AND o.order_date >= '2024-01-01'
GROUP BY DATE(o.order_date)
ORDER BY order_day DESC;

-- Запрос 4: Коррелированный подзапрос (очень медленный)
-- ПРОБЛЕМА: подзапрос выполняется для каждой строки
SELECT 
    p.product_name,
    p.price,
    (SELECT COUNT(*) 
     FROM order_items oi 
     WHERE oi.product_id = p.product_id) as times_ordered
FROM products p
WHERE p.in_stock = 1
  AND p.price > (
    SELECT AVG(price) 
    FROM products p2 
    WHERE p2.category_id = p.category_id
  )
ORDER BY times_ordered DESC;

-- Запрос 5: Многотабличный JOIN без оптимизации
-- ПРОБЛЕМА: отсутствуют индексы для всех JOIN операций
SELECT 
    c.customer_name,
    c.city,
    p.product_name,
    p.category_id,
    oi.quantity,
    oi.unit_price,
    o.order_date
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
WHERE o.order_date BETWEEN '2024-01-01' AND '2024-03-31'
  AND c.country = 'Russia'
  AND p.price > 10000
ORDER BY o.order_date DESC, oi.unit_price DESC;
