-- Примеры SQL-запросов для главы 5

-- 1. Простые SELECT запросы
SELECT * FROM customers WHERE city = 'Москва';
SELECT customer_name, city FROM customers ORDER BY registration_date DESC;
SELECT * FROM products WHERE price > 1000;

-- 2. Фильтрация с WHERE
SELECT * FROM orders WHERE order_date >= '2023-06-01';
SELECT * FROM products WHERE category = 'Электроника' AND price < 5000;
SELECT customer_name FROM customers WHERE city IN ('Москва', 'Санкт-Петербург');

-- 3. Группировка с GROUP BY
SELECT city, COUNT(*) as client_count 
FROM customers 
GROUP BY city 
ORDER BY client_count DESC;

SELECT category, AVG(price) as avg_price, COUNT(*) as product_count
FROM products 
GROUP BY category;

SELECT EXTRACT(MONTH FROM order_date) as month, SUM(total_amount) as monthly_sales
FROM orders 
GROUP BY EXTRACT(MONTH FROM order_date)
ORDER BY month;

-- 4. Соединения таблиц (JOINs)
-- Клиенты с их общей суммой покупок
SELECT c.customer_name, c.city, SUM(o.total_amount) as total_purchases
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.customer_name, c.city
ORDER BY total_purchases DESC;

-- Детализация заказов с названиями товаров
SELECT o.order_id, o.order_date, p.product_name, oi.quantity, oi.price
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
WHERE o.order_date >= '2023-01-01'
ORDER BY o.order_date DESC;

-- 5. Агрегатные функции
SELECT 
    COUNT(*) as total_orders,
    AVG(total_amount) as avg_order_value,
    MIN(total_amount) as min_order,
    MAX(total_amount) as max_order,
    SUM(total_amount) as total_revenue
FROM orders;

-- Топ-5 самых популярных товаров
SELECT p.product_name, SUM(oi.quantity) as total_sold
FROM products p
JOIN order_items oi ON p.product_id = oi.product_id
GROUP BY p.product_id, p.product_name
ORDER BY total_sold DESC
LIMIT 5;

-- 6. Подзапросы
-- Клиенты, которые потратили больше среднего
SELECT customer_name, city
FROM customers c
WHERE c.customer_id IN (
    SELECT customer_id 
    FROM orders 
    GROUP BY customer_id 
    HAVING SUM(total_amount) > (SELECT AVG(total_amount) FROM orders)
);

-- Товары, которые ни разу не покупали
SELECT product_name, category, price
FROM products 
WHERE product_id NOT IN (
    SELECT DISTINCT product_id FROM order_items
);

-- 7. Представления (Views)
CREATE VIEW customer_summary AS
SELECT 
    c.customer_id,
    c.customer_name,
    c.city,
    COUNT(o.order_id) as order_count,
    SUM(o.total_amount) as total_spent,
    AVG(o.total_amount) as avg_order_value,
    MAX(o.order_date) as last_order_date
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.customer_name, c.city;

CREATE VIEW monthly_sales AS
SELECT 
    EXTRACT(YEAR FROM order_date) as year,
    EXTRACT(MONTH FROM order_date) as month,
    COUNT(*) as order_count,
    SUM(total_amount) as revenue,
    AVG(total_amount) as avg_order_value
FROM orders
GROUP BY EXTRACT(YEAR FROM order_date), EXTRACT(MONTH FROM order_date)
ORDER BY year, month;

-- 8. Полезные запросы для анализа
-- Анализ продаж по категориям
SELECT 
    p.category,
    COUNT(DISTINCT oi.order_id) as orders_with_category,
    SUM(oi.quantity * oi.price) as category_revenue,
    AVG(oi.price) as avg_item_price
FROM products p
JOIN order_items oi ON p.product_id = oi.product_id
GROUP BY p.category
ORDER BY category_revenue DESC;

-- Сезонный анализ продаж
SELECT 
    CASE 
        WHEN EXTRACT(MONTH FROM order_date) IN (12, 1, 2) THEN 'Winter'
        WHEN EXTRACT(MONTH FROM order_date) IN (3, 4, 5) THEN 'Spring'
        WHEN EXTRACT(MONTH FROM order_date) IN (6, 7, 8) THEN 'Summer'
        ELSE 'Autumn'
    END as season,
    COUNT(*) as orders,
    SUM(total_amount) as revenue
FROM orders
GROUP BY 
    CASE 
        WHEN EXTRACT(MONTH FROM order_date) IN (12, 1, 2) THEN 'Winter'
        WHEN EXTRACT(MONTH FROM order_date) IN (3, 4, 5) THEN 'Spring'
        WHEN EXTRACT(MONTH FROM order_date) IN (6, 7, 8) THEN 'Summer'
        ELSE 'Autumn'
    END
ORDER BY revenue DESC;

-- RFM анализ (Recency, Frequency, Monetary)
WITH customer_rfm AS (
    SELECT 
        c.customer_id,
        c.customer_name,
        MAX(o.order_date) as last_order_date,
        COUNT(o.order_id) as frequency,
        SUM(o.total_amount) as monetary
    FROM customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.customer_name
)
SELECT 
    *,
    CURRENT_DATE - last_order_date as recency_days,
    CASE 
        WHEN frequency >= 5 THEN 'High'
        WHEN frequency >= 2 THEN 'Medium'
        ELSE 'Low'
    END as frequency_segment,
    CASE 
        WHEN monetary >= 10000 THEN 'High'
        WHEN monetary >= 5000 THEN 'Medium'
        ELSE 'Low'
    END as monetary_segment
FROM customer_rfm
ORDER BY monetary DESC;
