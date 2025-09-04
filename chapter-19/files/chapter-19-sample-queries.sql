-- ========================================
-- СПРАВОЧНЫЕ SQL ЗАПРОСЫ ДЛЯ ГЛАВЫ 19
-- Analytics Course: github.com/lazuale/analytics-course
-- ========================================

-- Этот файл содержит готовые примеры SQL запросов
-- для изучения основ SQL и выполнения практических заданий

-- ========================================
-- 1. БАЗОВЫЕ SELECT ЗАПРОСЫ
-- ========================================

-- Простой выбор всех данных
SELECT * FROM customers LIMIT 10;

-- Выбор конкретных столбцов
SELECT customer_id, first_name, last_name, city FROM customers;

-- Использование алиасов для переименования столбцов
SELECT 
    customer_id AS id,
    first_name AS имя,
    last_name AS фамилия,
    city AS город
FROM customers
LIMIT 5;

-- Вычисляемые поля
SELECT 
    product_name,
    price,
    price * 0.2 AS налог,
    price * 1.2 AS цена_с_налогом,
    CASE 
        WHEN price < 5000 THEN 'Бюджетный'
        WHEN price < 20000 THEN 'Средний'
        ELSE 'Премиум'
    END AS ценовая_категория
FROM products
LIMIT 10;

-- Объединение строк
SELECT 
    first_name || ' ' || last_name AS полное_имя,
    'Email: ' || email AS контакт,
    LENGTH(email) AS длина_email
FROM customers
LIMIT 5;

-- Работа с датами
SELECT 
    order_id,
    order_date,
    strftime('%Y', order_date) AS год,
    strftime('%m', order_date) AS месяц,
    strftime('%d', order_date) AS день,
    julianday('now') - julianday(order_date) AS дней_назад
FROM orders
LIMIT 10;

-- ========================================
-- 2. WHERE УСЛОВИЯ И ФИЛЬТРАЦИЯ
-- ========================================

-- Фильтрация по тексту
SELECT * FROM customers WHERE city = 'Москва';

-- Фильтрация по числу
SELECT * FROM products WHERE price > 10000;
SELECT * FROM products WHERE price BETWEEN 5000 AND 15000;

-- Фильтрация по дате
SELECT * FROM orders WHERE order_date >= '2024-01-01';
SELECT * FROM orders WHERE order_date BETWEEN '2024-03-01' AND '2024-03-31';

-- Поиск по шаблону (LIKE)
SELECT * FROM customers WHERE first_name LIKE 'А%';  -- Начинается с "А"
SELECT * FROM customers WHERE email LIKE '%@gmail.com';  -- Email от Gmail
SELECT * FROM products WHERE product_name LIKE '%телефон%';  -- Содержит "телефон"

-- Множественные значения (IN)
SELECT * FROM customers WHERE city IN ('Москва', 'Санкт-Петербург', 'Казань');
SELECT * FROM products WHERE category_id IN (1, 2, 3);

-- Логические операторы
SELECT * FROM customers 
WHERE city = 'Москва' AND gender = 'F';

SELECT * FROM products 
WHERE price > 5000 OR category_id = 1;

SELECT * FROM customers 
WHERE NOT city = 'Москва';

-- Проверка NULL значений
SELECT * FROM customers WHERE email IS NOT NULL;

-- Комплексные условия
SELECT * FROM orders 
WHERE (total_amount > 50000 OR customer_id IN (1, 2, 3))
  AND order_date >= '2024-01-01';

-- ========================================
-- 3. СОРТИРОВКА (ORDER BY)
-- ========================================

-- Простая сортировка
SELECT * FROM customers ORDER BY last_name;
SELECT * FROM products ORDER BY price DESC;

-- Сортировка по нескольким полям
SELECT * FROM customers ORDER BY city, last_name;
SELECT * FROM orders ORDER BY order_date DESC, total_amount DESC;

-- Сортировка по вычисляемому полю
SELECT 
    product_name,
    price,
    stock_quantity,
    price * stock_quantity AS общая_стоимость
FROM products
ORDER BY общая_стоимость DESC;

-- ========================================
-- 4. АГРЕГАТНЫЕ ФУНКЦИИ
-- ========================================

-- Подсчет количества
SELECT COUNT(*) AS всего_клиентов FROM customers;
SELECT COUNT(email) AS клиентов_с_email FROM customers;
SELECT COUNT(DISTINCT city) AS уникальных_городов FROM customers;

-- Суммирование
SELECT SUM(total_amount) AS общая_выручка FROM orders;
SELECT SUM(quantity) AS всего_товаров_продано FROM order_items;

-- Среднее значение
SELECT AVG(total_amount) AS средний_чек FROM orders;
SELECT ROUND(AVG(price), 2) AS средняя_цена FROM products;

-- Минимум и максимум
SELECT 
    MIN(price) AS самый_дешевый,
    MAX(price) AS самый_дорогой,
    MAX(price) - MIN(price) AS диапазон_цен
FROM products;

-- Комбинация агрегатных функций
SELECT 
    COUNT(*) AS количество_заказов,
    SUM(total_amount) AS общая_сумма,
    AVG(total_amount) AS средний_чек,
    MIN(total_amount) AS минимальный_заказ,
    MAX(total_amount) AS максимальный_заказ
FROM orders;

-- ========================================
-- 5. GROUP BY - ГРУППИРОВКА
-- ========================================

-- Группировка по одному полю
SELECT 
    city,
    COUNT(*) AS количество_клиентов
FROM customers
GROUP BY city
ORDER BY количество_клиентов DESC;

-- Статистика заказов по месяцам
SELECT 
    strftime('%Y-%m', order_date) AS месяц,
    COUNT(*) AS количество_заказов,
    SUM(total_amount) AS выручка_за_месяц,
    AVG(total_amount) AS средний_чек
FROM orders
GROUP BY strftime('%Y-%m', order_date)
ORDER BY месяц;

-- Группировка по нескольким полям
SELECT 
    city,
    gender,
    COUNT(*) AS количество
FROM customers
GROUP BY city, gender
ORDER BY city, gender;

-- Анализ продаж по категориям
SELECT 
    category_id,
    COUNT(*) AS количество_товаров,
    AVG(price) AS средняя_цена,
    SUM(stock_quantity) AS общий_остаток
FROM products
GROUP BY category_id
ORDER BY средняя_цена DESC;

-- ========================================
-- 6. HAVING - ФИЛЬТРАЦИЯ ГРУПП
-- ========================================

-- Города с количеством клиентов больше 50
SELECT 
    city,
    COUNT(*) AS количество_клиентов
FROM customers
GROUP BY city
HAVING COUNT(*) > 50
ORDER BY количество_клиентов DESC;

-- Клиенты с суммой заказов больше 100000
SELECT 
    customer_id,
    COUNT(*) AS количество_заказов,
    SUM(total_amount) AS общая_сумма
FROM orders
GROUP BY customer_id
HAVING SUM(total_amount) > 100000
ORDER BY общая_сумма DESC;

-- Месяцы с выручкой больше 1 млн
SELECT 
    strftime('%Y-%m', order_date) AS месяц,
    COUNT(*) AS заказов,
    SUM(total_amount) AS выручка
FROM orders
GROUP BY strftime('%Y-%m', order_date)
HAVING SUM(total_amount) > 1000000
ORDER BY выручка DESC;

-- ========================================
-- 7. БАЗОВЫЕ JOIN ОПЕРАЦИИ
-- ========================================

-- INNER JOIN - заказы с информацией о клиентах
SELECT 
    o.order_id,
    c.first_name,
    c.last_name,
    c.city,
    o.order_date,
    o.total_amount
FROM orders o
INNER JOIN customers c ON o.customer_id = c.customer_id
ORDER BY o.order_date DESC
LIMIT 20;

-- LEFT JOIN - все клиенты и их статистика заказов
SELECT 
    c.customer_id,
    c.first_name,
    c.last_name,
    c.city,
    COUNT(o.order_id) AS количество_заказов,
    COALESCE(SUM(o.total_amount), 0) AS общая_сумма
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name, c.city
ORDER BY общая_сумма DESC;

-- Многотабличный JOIN
SELECT 
    c.first_name || ' ' || c.last_name AS клиент,
    p.product_name AS товар,
    cat.category_name AS категория,
    oi.quantity AS количество,
    oi.price AS цена,
    o.order_date
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
INNER JOIN order_items oi ON o.order_id = oi.order_id
INNER JOIN products p ON oi.product_id = p.product_id
INNER JOIN categories cat ON p.category_id = cat.category_id
WHERE o.order_date >= '2024-03-01'
ORDER BY o.order_date DESC, c.last_name
LIMIT 50;

-- ========================================
-- 8. ПРАКТИЧЕСКИЕ БИЗНЕС-ЗАПРОСЫ
-- ========================================

-- Топ-10 клиентов по выручке
SELECT 
    c.customer_id,
    c.first_name || ' ' || c.last_name AS клиент,
    c.city,
    COUNT(o.order_id) AS заказов,
    SUM(o.total_amount) AS общая_сумма,
    AVG(o.total_amount) AS средний_чек,
    MAX(o.order_date) AS последний_заказ
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name, c.city
ORDER BY общая_сумма DESC
LIMIT 10;

-- Анализ продаж по категориям товаров
SELECT 
    cat.category_name AS категория,
    COUNT(DISTINCT p.product_id) AS товаров_в_категории,
    COUNT(oi.order_item_id) AS продано_позиций,
    SUM(oi.quantity) AS общее_количество,
    SUM(oi.quantity * oi.price) AS выручка_категории,
    AVG(oi.price) AS средняя_цена_продажи
FROM categories cat
LEFT JOIN products p ON cat.category_id = p.category_id
LEFT JOIN order_items oi ON p.product_id = oi.product_id
GROUP BY cat.category_id, cat.category_name
ORDER BY выручка_категории DESC;

-- Сезонный анализ продаж
SELECT 
    CASE strftime('%m', order_date)
        WHEN '12' THEN 'Зима'
        WHEN '01' THEN 'Зима'
        WHEN '02' THEN 'Зима'
        WHEN '03' THEN 'Весна'
        WHEN '04' THEN 'Весна'
        WHEN '05' THEN 'Весна'
        WHEN '06' THEN 'Лето'
        WHEN '07' THEN 'Лето'
        WHEN '08' THEN 'Лето'
        WHEN '09' THEN 'Осень'
        WHEN '10' THEN 'Осень'
        WHEN '11' THEN 'Осень'
    END AS сезон,
    COUNT(*) AS количество_заказов,
    SUM(total_amount) AS выручка_сезона,
    AVG(total_amount) AS средний_чек
FROM orders
WHERE strftime('%Y', order_date) = '2024'
GROUP BY сезон
ORDER BY выручка_сезона DESC;

-- RFM анализ (упрощенный)
SELECT 
    c.customer_id,
    c.first_name || ' ' || c.last_name AS клиент,
    
    -- Recency: дни с последнего заказа
    julianday('now') - julianday(MAX(o.order_date)) AS дней_с_последнего_заказа,
    
    -- Frequency: частота заказов
    COUNT(o.order_id) AS количество_заказов,
    
    -- Monetary: сумма покупок
    SUM(o.total_amount) AS общая_сумма,
    
    -- Сегментация
    CASE 
        WHEN COUNT(o.order_id) >= 10 AND SUM(o.total_amount) >= 200000 
            AND julianday('now') - julianday(MAX(o.order_date)) <= 90
        THEN 'VIP'
        WHEN COUNT(o.order_id) >= 5 AND SUM(o.total_amount) >= 100000
            AND julianday('now') - julianday(MAX(o.order_date)) <= 180
        THEN 'Золотой'
        WHEN COUNT(o.order_id) >= 3 AND julianday('now') - julianday(MAX(o.order_date)) <= 365
        THEN 'Серебряный'
        WHEN julianday('now') - julianday(MAX(o.order_date)) > 365
        THEN 'Спящий'
        ELSE 'Бронзовый'
    END AS сегмент_клиента
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name
HAVING COUNT(o.order_id) > 0
ORDER BY общая_сумма DESC;

-- ========================================
-- 9. ПОДЗАПРОСЫ (ОСНОВЫ)
-- ========================================

-- Клиенты с суммой заказов выше среднего
SELECT 
    customer_id,
    first_name,
    last_name,
    (SELECT SUM(total_amount) FROM orders WHERE customer_id = c.customer_id) AS сумма_заказов
FROM customers c
WHERE (
    SELECT SUM(total_amount) FROM orders WHERE customer_id = c.customer_id
) > (
    SELECT AVG(customer_total) FROM (
        SELECT SUM(total_amount) AS customer_total
        FROM orders 
        GROUP BY customer_id
    )
);

-- Товары, которые ни разу не покупали
SELECT 
    product_id,
    product_name,
    price
FROM products
WHERE product_id NOT IN (
    SELECT DISTINCT product_id 
    FROM order_items
);

-- ========================================
-- 10. ПОЛЕЗНЫЕ ФУНКЦИИ И ТРЮКИ
-- ========================================

-- Условная агрегация с CASE
SELECT 
    city,
    COUNT(*) AS всего_клиентов,
    COUNT(CASE WHEN gender = 'M' THEN 1 END) AS мужчин,
    COUNT(CASE WHEN gender = 'F' THEN 1 END) AS женщин,
    ROUND(COUNT(CASE WHEN gender = 'M' THEN 1 END) * 100.0 / COUNT(*), 1) AS процент_мужчин
FROM customers
GROUP BY city
ORDER BY всего_клиентов DESC;

-- Ранжирование с использованием подзапросов
SELECT 
    product_name,
    price,
    (SELECT COUNT(*) FROM products p2 WHERE p2.price > p1.price) + 1 AS ранг_по_цене
FROM products p1
ORDER BY price DESC;

-- Создание сводной таблицы (pivot)
SELECT 
    strftime('%Y-%m', order_date) AS месяц,
    SUM(CASE WHEN strftime('%w', order_date) = '1' THEN total_amount ELSE 0 END) AS понедельник,
    SUM(CASE WHEN strftime('%w', order_date) = '2' THEN total_amount ELSE 0 END) AS вторник,
    SUM(CASE WHEN strftime('%w', order_date) = '3' THEN total_amount ELSE 0 END) AS среда,
    SUM(CASE WHEN strftime('%w', order_date) = '4' THEN total_amount ELSE 0 END) AS четверг,
    SUM(CASE WHEN strftime('%w', order_date) = '5' THEN total_amount ELSE 0 END) AS пятница,
    SUM(CASE WHEN strftime('%w', order_date) = '6' THEN total_amount ELSE 0 END) AS суббота,
    SUM(CASE WHEN strftime('%w', order_date) = '0' THEN total_amount ELSE 0 END) AS воскресенье
FROM orders
WHERE order_date >= '2024-01-01'
GROUP BY strftime('%Y-%m', order_date)
ORDER BY месяц;

-- ========================================
-- 11. СОЗДАНИЕ ПРЕДСТАВЛЕНИЙ (VIEWS)
-- ========================================

-- Представление для анализа клиентов
CREATE VIEW customer_analytics AS
SELECT 
    c.customer_id,
    c.first_name || ' ' || c.last_name AS full_name,
    c.city,
    c.gender,
    c.registration_date,
    COUNT(o.order_id) AS orders_count,
    COALESCE(SUM(o.total_amount), 0) AS lifetime_value,
    COALESCE(AVG(o.total_amount), 0) AS avg_order_value,
    COALESCE(MAX(o.order_date), 'No orders') AS last_order_date,
    julianday('now') - julianday(c.registration_date) AS days_as_customer
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name, c.city, c.gender, c.registration_date;

-- Использование представления
SELECT * FROM customer_analytics WHERE lifetime_value > 50000 ORDER BY lifetime_value DESC;

-- ========================================
-- КОНЕЦ ФАЙЛА
-- ========================================

-- Этот файл содержит основные паттерны SQL запросов
-- Используйте эти примеры как основу для ваших собственных запросов
-- Изменяйте условия, добавляйте новые поля, экспериментируйте!

-- Документация SQLite: https://www.sqlite.org/lang.html
-- SQL Tutorial: https://www.w3schools.com/sql/