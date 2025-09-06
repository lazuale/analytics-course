-- ================================================
-- Глава 5: Основы работы с базами данных
-- Примеры SQL-запросов для практики
-- ================================================

-- ВНИМАНИЕ: Эти запросы предназначены для изучения и адаптации
-- Выполняйте их на созданной базе данных "technomir_shop"

-- ================================================
-- РАЗДЕЛ 1: БАЗОВЫЕ ЗАПРОСЫ SELECT
-- ================================================

-- Пример 1: Простая выборка всех товаров
SELECT product_name, price, stock_quantity 
FROM products 
WHERE is_active = TRUE;

-- Пример 2: Сортировка товаров по цене
SELECT product_name, price 
FROM products 
WHERE price > 10000 
ORDER BY price DESC;

-- Пример 3: Ограничение количества результатов
SELECT first_name, last_name, city, registration_date
FROM customers 
ORDER BY registration_date DESC 
LIMIT 10;

-- Пример 4: Подсчет общего количества товаров
SELECT COUNT(*) as total_products 
FROM products 
WHERE is_active = TRUE;

-- ================================================
-- РАЗДЕЛ 2: ФИЛЬТРАЦИЯ С WHERE
-- ================================================

-- Пример 5: Точное совпадение
SELECT * FROM customers WHERE city = 'Москва';

-- Пример 6: Диапазон цен
SELECT product_name, price 
FROM products 
WHERE price BETWEEN 20000 AND 100000 
ORDER BY price;

-- Пример 7: Поиск по списку значений
SELECT order_id, status, total_amount 
FROM orders 
WHERE status IN ('shipped', 'delivered');

-- Пример 8: Поиск по шаблону (товары Apple)
SELECT product_name, price 
FROM products 
WHERE product_name LIKE '%iPhone%' 
   OR product_name LIKE '%iPad%' 
   OR product_name LIKE '%MacBook%';

-- Пример 9: Сложные условия
SELECT customer_id, first_name, last_name, email 
FROM customers 
WHERE city IN ('Москва', 'Санкт-Петербург') 
  AND registration_date >= '2024-01-01';

-- Пример 10: Работа с NULL значениями
SELECT first_name, last_name, phone 
FROM customers 
WHERE phone IS NOT NULL 
ORDER BY last_name;

-- ================================================
-- РАЗДЕЛ 3: АГРЕГАЦИЯ И ГРУППИРОВКА
-- ================================================

-- Пример 11: Количество товаров по категориям
SELECT c.category_name, COUNT(p.product_id) as products_count
FROM categories c
LEFT JOIN products p ON c.category_id = p.category_id
GROUP BY c.category_id, c.category_name
ORDER BY products_count DESC;

-- Пример 12: Средняя цена по категориям
SELECT c.category_name,
       COUNT(p.product_id) as products_count,
       ROUND(AVG(p.price), 2) as avg_price,
       MIN(p.price) as min_price,
       MAX(p.price) as max_price
FROM categories c
JOIN products p ON c.category_id = p.category_id
WHERE p.is_active = TRUE
GROUP BY c.category_id, c.category_name
HAVING COUNT(p.product_id) > 5
ORDER BY avg_price DESC;

-- Пример 13: Статистика заказов по статусам
SELECT status, 
       COUNT(*) as orders_count,
       ROUND(AVG(total_amount), 2) as avg_order_value,
       SUM(total_amount) as total_revenue
FROM orders 
GROUP BY status 
ORDER BY orders_count DESC;

-- Пример 14: Клиенты по городам
SELECT city, 
       COUNT(*) as customers_count,
       MIN(registration_date) as first_registration,
       MAX(registration_date) as last_registration
FROM customers 
GROUP BY city 
HAVING COUNT(*) >= 2
ORDER BY customers_count DESC;

-- ================================================
-- РАЗДЕЛ 4: РАБОТА С ДАТАМИ
-- ================================================

-- Пример 15: Заказы за последние 3 месяца
SELECT order_id, customer_id, order_date, total_amount
FROM orders 
WHERE order_date >= CURRENT_DATE - INTERVAL '3 months'
ORDER BY order_date DESC;

-- Пример 16: Группировка по месяцам
SELECT DATE_TRUNC('month', order_date) as order_month,
       COUNT(*) as orders_count,
       SUM(total_amount) as monthly_revenue
FROM orders 
WHERE order_date >= '2023-09-01'
GROUP BY DATE_TRUNC('month', order_date)
ORDER BY order_month;

-- Пример 17: День недели заказов
SELECT EXTRACT(DOW FROM order_date) as day_of_week,
       TO_CHAR(order_date, 'Day') as day_name,
       COUNT(*) as orders_count
FROM orders
GROUP BY EXTRACT(DOW FROM order_date), TO_CHAR(order_date, 'Day')
ORDER BY day_of_week;

-- ================================================
-- РАЗДЕЛ 5: ИСПОЛЬЗОВАНИЕ ПРЕДСТАВЛЕНИЙ
-- ================================================

-- Пример 18: Товары с категориями через представление
SELECT * FROM products_with_categories 
WHERE price > 50000 
ORDER BY category_name, price DESC;

-- Пример 19: Заказы с информацией о клиентах
SELECT * FROM orders_with_customers 
WHERE city = 'Москва' 
  AND status = 'delivered'
ORDER BY order_date DESC 
LIMIT 20;

-- ================================================
-- РАЗДЕЛ 6: ПОДЗАПРОСЫ
-- ================================================

-- Пример 20: Товары дороже средней цены
SELECT product_name, price 
FROM products 
WHERE price > (SELECT AVG(price) FROM products)
ORDER BY price DESC;

-- Пример 21: Клиенты с заказами
SELECT customer_id, first_name, last_name 
FROM customers 
WHERE customer_id IN (
    SELECT DISTINCT customer_id FROM orders
)
ORDER BY last_name;

-- Пример 22: Самые популярные товары
SELECT p.product_name, SUM(oi.quantity) as total_sold
FROM products p
JOIN order_items oi ON p.product_id = oi.product_id
JOIN orders o ON oi.order_id = o.order_id
WHERE o.status IN ('delivered', 'shipped')
GROUP BY p.product_id, p.product_name
ORDER BY total_sold DESC
LIMIT 10;

-- ================================================
-- РАЗДЕЛ 7: АНАЛИТИЧЕСКИЕ ЗАПРОСЫ
-- ================================================

-- Пример 23: Анализ клиентской активности
SELECT c.customer_id,
       c.first_name,
       c.last_name,
       c.city,
       COUNT(o.order_id) as orders_count,
       COALESCE(SUM(o.total_amount), 0) as total_spent,
       COALESCE(ROUND(AVG(o.total_amount), 2), 0) as avg_order_value
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id AND o.status = 'delivered'
GROUP BY c.customer_id, c.first_name, c.last_name, c.city
ORDER BY total_spent DESC;

-- Пример 24: Товары с низким остатком
SELECT c.category_name,
       p.product_name,
       p.stock_quantity,
       p.price
FROM products p
JOIN categories c ON p.category_id = c.category_id
WHERE p.stock_quantity < 20 AND p.is_active = TRUE
ORDER BY p.stock_quantity, c.category_name;

-- Пример 25: Сезонный анализ продаж
SELECT EXTRACT(QUARTER FROM o.order_date) as quarter,
       EXTRACT(YEAR FROM o.order_date) as year,
       COUNT(*) as orders_count,
       SUM(o.total_amount) as total_revenue,
       ROUND(AVG(o.total_amount), 2) as avg_order_value
FROM orders o
WHERE o.status IN ('delivered', 'shipped')
GROUP BY EXTRACT(QUARTER FROM o.order_date), EXTRACT(YEAR FROM o.order_date)
ORDER BY year, quarter;

-- ================================================
-- РАЗДЕЛ 8: ЗАПРОСЫ ДЛЯ ОТЧЕТНОСТИ
-- ================================================

-- Пример 26: Топ-10 клиентов по выручке
WITH customer_stats AS (
    SELECT c.customer_id,
           c.first_name || ' ' || c.last_name as full_name,
           c.city,
           c.email,
           COUNT(o.order_id) as orders_count,
           SUM(o.total_amount) as total_revenue
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    WHERE o.status = 'delivered'
    GROUP BY c.customer_id, c.first_name, c.last_name, c.city, c.email
)
SELECT * FROM customer_stats 
WHERE total_revenue > 50000
ORDER BY total_revenue DESC
LIMIT 10;

-- Пример 27: Конверсия статусов заказов
SELECT status,
       COUNT(*) as count,
       ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) as percentage
FROM orders
GROUP BY status
ORDER BY count DESC;

-- ================================================
-- ПОДСКАЗКИ ДЛЯ ПРАКТИКИ:
-- ================================================

/*
1. Начинайте с простых запросов и постепенно усложняйте
2. Всегда проверяйте результаты на здравый смысл
3. Используйте EXPLAIN для анализа производительности
4. Экспериментируйте с различными комбинациями условий
5. Создавайте свои запросы на базе этих примеров
*/

-- Для проверки производительности запроса:
-- EXPLAIN ANALYZE SELECT * FROM products WHERE price > 50000;

-- Для просмотра плана выполнения:
-- EXPLAIN SELECT * FROM orders o JOIN customers c ON o.customer_id = c.customer_id;
