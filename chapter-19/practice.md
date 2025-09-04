# 📝 Практические задания для главы 19

📖 [Вернуться к теории](../README.md) | 📁 [Учебные файлы](../files/README.md) | ✅ [Чек-лист](../checklist.md)

## 🎯 Обзор заданий

В этой главе вы выполните **5 практических заданий** возрастающей сложности, работая с реальной базой данных интернет-магазина:

1. **📊 Базовые SELECT запросы** — знакомство с синтаксисом SQL  
2. **🔍 Фильтрация и сортировка** — WHERE, ORDER BY, LIKE
3. **📈 Агрегатные функции** — COUNT, SUM, AVG, GROUP BY, HAVING
4. **🔗 Объединение таблиц** — INNER JOIN, LEFT JOIN, анализ связей
5. **🚀 Комплексный бизнес-анализ** — подзапросы, интеграция с Power Query

**⏱️ Общее время выполнения:** 6-8 часов  
**🎯 Результат:** Навыки работы с SQL для решения реальных аналитических задач

---

## 📋 Задание 1: Знакомство с SQL и базовые SELECT

**🎯 Цель:** Освоить базовый синтаксис SQL и простые SELECT запросы

**🛠️ Инструменты:** SQLite DB Browser, предоставленная база данных

**⏱️ Время:** 60 минут

### Что нужно сделать:

#### 1️⃣ Подключение к базе данных

1. Скачайте и установите **DB Browser for SQLite** (бесплатно)
2. Откройте файл `ecommerce_database.db` из папки files/
3. Изучите структуру базы данных в разделе "Database Structure"

**Структура базы данных:**
- `customers` — информация о клиентах
- `orders` — заказы клиентов  
- `order_items` — товары в заказах
- `products` — каталог товаров
- `categories` — категории товаров

#### 2️⃣ Изучение структуры таблиц

Выполните следующие запросы для понимания данных:

```sql
-- Посмотреть первые 10 записей из каждой таблицы
SELECT * FROM customers LIMIT 10;
SELECT * FROM orders LIMIT 10;
SELECT * FROM order_items LIMIT 10;
SELECT * FROM products LIMIT 10;
SELECT * FROM categories LIMIT 10;

-- Узнать количество записей в каждой таблице
SELECT COUNT(*) as customers_count FROM customers;
SELECT COUNT(*) as orders_count FROM orders;
SELECT COUNT(*) as order_items_count FROM order_items;
SELECT COUNT(*) as products_count FROM products;
SELECT COUNT(*) as categories_count FROM categories;
```

#### 3️⃣ Простые SELECT запросы

```sql
-- Задача 1.1: Получить список всех клиентов из Москвы
SELECT customer_id, first_name, last_name, email, city
FROM customers
WHERE city = 'Москва';

-- Задача 1.2: Показать информацию о клиентах, упорядоченную по фамилии
SELECT customer_id, first_name, last_name, registration_date
FROM customers
ORDER BY last_name, first_name;

-- Задача 1.3: Получить список товаров дороже 5000 рублей
SELECT product_id, product_name, price, category_id
FROM products
WHERE price > 5000
ORDER BY price DESC;
```

#### 4️⃣ Работа с вычисляемыми полями

```sql
-- Задача 1.4: Добавить вычисляемые поля к информации о товарах
SELECT 
    product_name,
    price,
    price * 0.2 AS vat_amount,              -- НДС 20%
    price * 1.2 AS price_with_vat,          -- Цена с НДС
    CASE 
        WHEN price < 1000 THEN 'Бюджетный'
        WHEN price < 5000 THEN 'Средний'
        ELSE 'Премиум'
    END AS price_category
FROM products
WHERE category_id IN (1, 2, 3)             -- Только первые 3 категории
ORDER BY price;

-- Задача 1.5: Информация о клиентах с форматированием
SELECT 
    customer_id,
    first_name || ' ' || last_name AS full_name,  -- Объединение имени и фамилии
    email,
    city,
    UPPER(city) AS city_uppercase,              -- Город большими буквами
    LENGTH(email) AS email_length,              -- Длина email
    DATE('now') AS current_date,                -- Текущая дата
    julianday('now') - julianday(registration_date) AS days_since_registration
FROM customers
WHERE city IN ('Москва', 'Санкт-Петербург', 'Казань')
ORDER BY days_since_registration DESC;
```

#### 5️⃣ Создание отчета

Создайте итоговый запрос, который покажет:

```sql
-- Задача 1.6: Общая статистика по базе данных
SELECT 
    'Клиенты' AS entity_type,
    COUNT(*) AS total_count,
    NULL AS avg_value,
    NULL AS min_value,
    NULL AS max_value
FROM customers

UNION ALL

SELECT 
    'Заказы' AS entity_type,
    COUNT(*) AS total_count,
    ROUND(AVG(total_amount), 2) AS avg_value,
    MIN(total_amount) AS min_value,
    MAX(total_amount) AS max_value
FROM orders

UNION ALL

SELECT 
    'Товары' AS entity_type,
    COUNT(*) AS total_count,
    ROUND(AVG(price), 2) AS avg_value,
    MIN(price) AS min_value,
    MAX(price) AS max_value
FROM products;
```

### ✅ Ожидаемый результат:

- Понимание структуры реляционной базы данных
- Умение писать базовые SELECT запросы
- Навыки работы с вычисляемыми полями и функциями
- Первый аналитический отчет на SQL

---

## 📋 Задание 2: Фильтрация и сортировка данных

**🎯 Цель:** Освоить WHERE условия, LIKE операторы и сложную сортировку

**🛠️ Инструменты:** SQLite DB Browser

**⏱️ Время:** 75 минут

### Что нужно сделать:

#### 1️⃣ Фильтрация по различным условиям

```sql
-- Задача 2.1: Клиенты с конкретными характеристиками
-- Найти всех клиентов женского пола из крупных городов
SELECT customer_id, first_name, last_name, city, gender
FROM customers
WHERE gender = 'F' 
  AND city IN ('Москва', 'Санкт-Петербург', 'Новосибирск', 'Екатеринбург')
ORDER BY city, last_name;

-- Задача 2.2: Заказы в определенном диапазоне дат и сумм
SELECT order_id, customer_id, order_date, total_amount
FROM orders
WHERE order_date BETWEEN '2024-03-01' AND '2024-03-31'
  AND total_amount BETWEEN 5000 AND 25000
ORDER BY total_amount DESC;

-- Задача 2.3: Товары с определенными характеристиками
SELECT product_name, price, category_id, stock_quantity
FROM products
WHERE stock_quantity > 0                    -- Есть в наличии
  AND price < 10000                         -- Доступная цена
  AND category_id NOT IN (5, 6)            -- Исключаем определенные категории
ORDER BY category_id, price;
```

#### 2️⃣ Работа с текстовыми данными и LIKE

```sql
-- Задача 2.4: Поиск клиентов по части имени или email
-- Клиенты с именем, начинающимся на "А"
SELECT customer_id, first_name, last_name, email
FROM customers
WHERE first_name LIKE 'А%'
ORDER BY first_name;

-- Клиенты с email от Gmail
SELECT customer_id, first_name, last_name, email
FROM customers
WHERE email LIKE '%@gmail.com'
ORDER BY last_name;

-- Задача 2.5: Поиск товаров по описанию
SELECT product_id, product_name, description, price
FROM products
WHERE description LIKE '%телефон%' 
   OR description LIKE '%смартфон%'
   OR product_name LIKE '%iPhone%'
   OR product_name LIKE '%Samsung%'
ORDER BY price DESC;

-- Задача 2.6: Клиенты с фамилиями, заканчивающимися на определенные буквы
SELECT customer_id, first_name, last_name, city
FROM customers
WHERE last_name LIKE '%ов' 
   OR last_name LIKE '%ев' 
   OR last_name LIKE '%ин'
   OR last_name LIKE '%ский'
ORDER BY last_name;
```

#### 3️⃣ Работа с датами и временем

```sql
-- Задача 2.7: Анализ заказов по времени
-- Заказы, сделанные в выходные дни
SELECT 
    order_id,
    customer_id,
    order_date,
    CASE strftime('%w', order_date)
        WHEN '0' THEN 'Воскресенье'
        WHEN '1' THEN 'Понедельник'
        WHEN '2' THEN 'Вторник'
        WHEN '3' THEN 'Среда'
        WHEN '4' THEN 'Четверг'
        WHEN '5' THEN 'Пятница'
        WHEN '6' THEN 'Суббота'
    END AS day_of_week,
    total_amount
FROM orders
WHERE strftime('%w', order_date) IN ('0', '6')  -- Суббота и воскресенье
ORDER BY order_date DESC;

-- Задача 2.8: Заказы за последние 90 дней
SELECT 
    order_id,
    customer_id,
    order_date,
    total_amount,
    julianday('now') - julianday(order_date) AS days_ago
FROM orders
WHERE julianday('now') - julianday(order_date) <= 90
ORDER BY order_date DESC;

-- Задача 2.9: Клиенты, зарегистрированные в определенный период
SELECT 
    customer_id,
    first_name,
    last_name,
    registration_date,
    strftime('%Y-%m', registration_date) AS registration_month
FROM customers
WHERE registration_date >= '2023-01-01' 
  AND registration_date < '2024-01-01'
ORDER BY registration_date;
```

#### 4️⃣ Комплексная фильтрация с логическими операторами

```sql
-- Задача 2.10: Сложные условия с AND, OR, NOT
-- VIP клиенты: женщины из Москвы ИЛИ мужчины с заказами > 50000
SELECT DISTINCT
    c.customer_id,
    c.first_name,
    c.last_name,
    c.city,
    c.gender,
    c.email
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE (c.gender = 'F' AND c.city = 'Москва')
   OR (c.gender = 'M' AND o.total_amount > 50000)
ORDER BY c.last_name;

-- Задача 2.11: Товары исключая определенные условия
SELECT 
    product_id,
    product_name,
    price,
    category_id,
    stock_quantity
FROM products
WHERE NOT (price < 1000 OR stock_quantity = 0)  -- НЕ (дешевые ИЛИ отсутствуют)
  AND category_id BETWEEN 1 AND 4
ORDER BY category_id, price;
```

#### 5️⃣ Многоуровневая сортировка

```sql
-- Задача 2.12: Сложная сортировка заказов
SELECT 
    o.order_id,
    c.first_name,
    c.last_name,
    c.city,
    o.order_date,
    o.total_amount,
    CASE 
        WHEN o.total_amount >= 50000 THEN 'Крупный'
        WHEN o.total_amount >= 20000 THEN 'Средний'
        ELSE 'Малый'
    END AS order_size
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
WHERE o.order_date >= '2024-01-01'
ORDER BY 
    c.city,                    -- Сначала по городу
    order_size DESC,           -- Потом по размеру заказа (крупные первые)
    o.total_amount DESC,       -- Внутри размера по убыванию суммы
    o.order_date DESC;         -- При равных суммах новые первые

-- Задача 2.13: Топ товаров с детальной сортировкой
SELECT 
    p.product_name,
    c.category_name,
    p.price,
    p.stock_quantity,
    ROUND(p.price / NULLIF(p.stock_quantity, 0), 2) AS price_per_item
FROM products p
JOIN categories c ON p.category_id = c.category_id
WHERE p.stock_quantity > 0
ORDER BY 
    c.category_name,           -- По категории
    p.price DESC,              -- Дорогие первые
    p.stock_quantity DESC;     -- При равной цене больше остатка
```

### ✅ Ожидаемый результат:

- Уверенное владение WHERE условиями
- Умение работать с LIKE для текстового поиска
- Навыки фильтрации по датам и времени
- Понимание логических операторов AND, OR, NOT
- Способность создавать сложные многоуровневые сортировки

---

## 📋 Задание 3: Агрегатные функции и группировка

**🎯 Цель:** Освоить COUNT, SUM, AVG, MIN, MAX, GROUP BY, HAVING для аналитики

**🛠️ Инструменты:** SQLite DB Browser

**⏱️ Время:** 90 минут

### Что нужно сделать:

#### 1️⃣ Основные агрегатные функции

```sql
-- Задача 3.1: Общая статистика по заказам
SELECT 
    COUNT(*) AS total_orders,                    -- Общее количество заказов
    COUNT(DISTINCT customer_id) AS unique_customers, -- Уникальных клиентов
    SUM(total_amount) AS total_revenue,          -- Общая выручка
    AVG(total_amount) AS avg_order_value,        -- Средний чек
    MIN(total_amount) AS min_order,              -- Минимальный заказ
    MAX(total_amount) AS max_order,              -- Максимальный заказ
    ROUND(AVG(total_amount), 2) AS avg_rounded   -- Среднее с округлением
FROM orders;

-- Задача 3.2: Статистика по товарам
SELECT 
    COUNT(*) AS total_products,
    COUNT(DISTINCT category_id) AS categories_count,
    SUM(stock_quantity) AS total_stock,
    AVG(price) AS avg_price,
    MIN(price) AS cheapest_product,
    MAX(price) AS most_expensive,
    SUM(price * stock_quantity) AS inventory_value  -- Стоимость запасов
FROM products
WHERE stock_quantity > 0;  -- Только товары в наличии
```

#### 2️⃣ Группировка по одному полю

```sql
-- Задача 3.3: Анализ клиентов по городам
SELECT 
    city,
    COUNT(*) AS customers_count,
    COUNT(CASE WHEN gender = 'M' THEN 1 END) AS male_count,
    COUNT(CASE WHEN gender = 'F' THEN 1 END) AS female_count,
    ROUND(AVG(CASE WHEN gender = 'M' THEN 1.0 ELSE 0.0 END) * 100, 1) AS male_percentage
FROM customers
GROUP BY city
ORDER BY customers_count DESC;

-- Задача 3.4: Продажи по месяцам
SELECT 
    strftime('%Y-%m', order_date) AS month,
    COUNT(*) AS orders_count,
    COUNT(DISTINCT customer_id) AS unique_customers,
    SUM(total_amount) AS monthly_revenue,
    AVG(total_amount) AS avg_order_value,
    ROUND(SUM(total_amount) / COUNT(DISTINCT customer_id), 2) AS revenue_per_customer
FROM orders
WHERE order_date >= '2023-01-01'
GROUP BY strftime('%Y-%m', order_date)
ORDER BY month;

-- Задача 3.5: Анализ товаров по категориям
SELECT 
    c.category_name,
    COUNT(p.product_id) AS products_count,
    SUM(p.stock_quantity) AS total_stock,
    AVG(p.price) AS avg_price,
    MIN(p.price) AS min_price,
    MAX(p.price) AS max_price,
    SUM(p.price * p.stock_quantity) AS category_inventory_value
FROM categories c
LEFT JOIN products p ON c.category_id = p.category_id
GROUP BY c.category_id, c.category_name
ORDER BY category_inventory_value DESC;
```

#### 3️⃣ Группировка по нескольким полям

```sql
-- Задача 3.6: Анализ по городам и полу
SELECT 
    city,
    gender,
    COUNT(*) AS customers_count,
    ROUND(AVG(julianday('now') - julianday(registration_date)), 0) AS avg_days_registered
FROM customers
WHERE city IN ('Москва', 'Санкт-Петербург', 'Новосибирск', 'Екатеринбург')
GROUP BY city, gender
ORDER BY city, gender;

-- Задача 3.7: Продажи по месяцам и городам
SELECT 
    strftime('%Y-%m', o.order_date) AS month,
    c.city,
    COUNT(o.order_id) AS orders_count,
    SUM(o.total_amount) AS revenue,
    AVG(o.total_amount) AS avg_order_value,
    COUNT(DISTINCT o.customer_id) AS unique_customers
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
WHERE o.order_date >= '2024-01-01'
  AND c.city IN ('Москва', 'Санкт-Петербург', 'Казань')
GROUP BY strftime('%Y-%m', o.order_date), c.city
ORDER BY month, revenue DESC;
```

#### 4️⃣ HAVING — фильтрация групп

```sql
-- Задача 3.8: Активные клиенты (с количеством заказов > 3)
SELECT 
    c.customer_id,
    c.first_name,
    c.last_name,
    c.city,
    COUNT(o.order_id) AS orders_count,
    SUM(o.total_amount) AS total_spent,
    AVG(o.total_amount) AS avg_order_value,
    MIN(o.order_date) AS first_order,
    MAX(o.order_date) AS last_order
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name, c.city
HAVING COUNT(o.order_id) > 3 AND SUM(o.total_amount) > 50000
ORDER BY total_spent DESC;

-- Задача 3.9: Популярные категории (с выручкой > 500000)
SELECT 
    c.category_name,
    COUNT(DISTINCT p.product_id) AS products_count,
    COUNT(oi.order_item_id) AS items_sold,
    SUM(oi.quantity) AS total_quantity_sold,
    SUM(oi.quantity * oi.price) AS category_revenue,
    AVG(oi.price) AS avg_selling_price
FROM categories c
JOIN products p ON c.category_id = p.category_id
JOIN order_items oi ON p.product_id = oi.product_id
GROUP BY c.category_id, c.category_name
HAVING SUM(oi.quantity * oi.price) > 500000
ORDER BY category_revenue DESC;

-- Задача 3.10: Месяцы с высокими продажами
SELECT 
    strftime('%Y-%m', order_date) AS month,
    COUNT(*) AS orders_count,
    SUM(total_amount) AS monthly_revenue,
    AVG(total_amount) AS avg_order_value
FROM orders
WHERE order_date >= '2023-01-01'
GROUP BY strftime('%Y-%m', order_date)
HAVING COUNT(*) > 100 AND SUM(total_amount) > 1000000  -- >100 заказов и >1млн выручки
ORDER BY monthly_revenue DESC;
```

#### 5️⃣ Комплексный аналитический отчет

```sql
-- Задача 3.11: Сводный отчет по эффективности городов
SELECT 
    c.city,
    COUNT(DISTINCT c.customer_id) AS total_customers,
    COUNT(o.order_id) AS total_orders,
    ROUND(CAST(COUNT(o.order_id) AS FLOAT) / COUNT(DISTINCT c.customer_id), 2) AS orders_per_customer,
    SUM(o.total_amount) AS total_revenue,
    ROUND(SUM(o.total_amount) / COUNT(DISTINCT c.customer_id), 2) AS revenue_per_customer,
    ROUND(AVG(o.total_amount), 2) AS avg_order_value,
    COUNT(DISTINCT DATE(o.order_date)) AS active_days,
    ROUND(SUM(o.total_amount) / COUNT(DISTINCT DATE(o.order_date)), 2) AS avg_daily_revenue,
    
    -- Категоризация городов по эффективности
    CASE 
        WHEN SUM(o.total_amount) / COUNT(DISTINCT c.customer_id) > 100000 THEN 'Высокая эффективность'
        WHEN SUM(o.total_amount) / COUNT(DISTINCT c.customer_id) > 50000 THEN 'Средняя эффективность'
        ELSE 'Низкая эффективность'
    END AS efficiency_category
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE c.city IN ('Москва', 'Санкт-Петербург', 'Новосибирск', 'Екатеринбург', 'Казань', 'Нижний Новгород')
GROUP BY c.city
HAVING COUNT(o.order_id) > 0  -- Только города с заказами
ORDER BY revenue_per_customer DESC;

-- Задача 3.12: RFM сегментация клиентов (упрощенная)
SELECT 
    customer_segment,
    COUNT(*) AS customers_count,
    AVG(days_since_last_order) AS avg_recency,
    AVG(order_frequency) AS avg_frequency,
    AVG(total_spent) AS avg_monetary
FROM (
    SELECT 
        c.customer_id,
        c.first_name,
        c.last_name,
        COUNT(o.order_id) AS order_frequency,
        SUM(o.total_amount) AS total_spent,
        julianday('now') - julianday(MAX(o.order_date)) AS days_since_last_order,
        
        -- Простая сегментация
        CASE 
            WHEN COUNT(o.order_id) >= 5 AND SUM(o.total_amount) >= 100000 
                AND julianday('now') - julianday(MAX(o.order_date)) <= 90 
            THEN 'Чемпионы'
            
            WHEN COUNT(o.order_id) >= 3 AND SUM(o.total_amount) >= 50000 
                AND julianday('now') - julianday(MAX(o.order_date)) <= 180 
            THEN 'Лояльные клиенты'
            
            WHEN COUNT(o.order_id) >= 2 AND julianday('now') - julianday(MAX(o.order_date)) <= 365
            THEN 'Потенциальные'
            
            WHEN julianday('now') - julianday(MAX(o.order_date)) > 365
            THEN 'Спящие'
            
            ELSE 'Новички'
        END AS customer_segment
    FROM customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.first_name, c.last_name
    HAVING COUNT(o.order_id) > 0  -- Только клиенты с заказами
) AS customer_analysis
GROUP BY customer_segment
ORDER BY avg_monetary DESC;
```

### ✅ Ожидаемый результат:

- Уверенное владение агрегатными функциями
- Навыки группировки данных для аналитических отчетов
- Понимание разницы между WHERE и HAVING
- Способность создавать сложные аналитические запросы
- Опыт создания бизнес-сегментации на SQL

---

## 📋 Задание 4: Объединение таблиц с JOIN

**🎯 Цель:** Освоить JOIN операции для работы с связанными данными

**🛠️ Инструменты:** SQLite DB Browser

**⏱️ Время:** 105 минут

### Что нужно сделать:

#### 1️⃣ Изучение связей между таблицами

```sql
-- Задача 4.1: Понимание структуры связей
-- Сначала изучим связи в нашей базе данных

-- Связь customers -> orders (один ко многим)
SELECT 'customers -> orders' AS relationship,
       COUNT(DISTINCT c.customer_id) AS unique_customers,
       COUNT(o.order_id) AS total_orders
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id;

-- Связь orders -> order_items (один ко многим)  
SELECT 'orders -> order_items' AS relationship,
       COUNT(DISTINCT o.order_id) AS unique_orders,
       COUNT(oi.order_item_id) AS total_order_items
FROM orders o
LEFT JOIN order_items oi ON o.order_id = oi.order_id;

-- Связь products -> order_items (один ко многим)
SELECT 'products -> order_items' AS relationship,
       COUNT(DISTINCT p.product_id) AS unique_products,
       COUNT(oi.order_item_id) AS total_order_items
FROM products p
LEFT JOIN order_items oi ON p.product_id = oi.product_id;

-- Связь categories -> products (один ко многим)
SELECT 'categories -> products' AS relationship,
       COUNT(DISTINCT c.category_id) AS unique_categories,
       COUNT(p.product_id) AS total_products
FROM categories c
LEFT JOIN products p ON c.category_id = p.category_id;
```

#### 2️⃣ INNER JOIN — пересечение данных

```sql
-- Задача 4.2: Заказы с полной информацией о клиентах
SELECT 
    o.order_id,
    c.first_name,
    c.last_name,
    c.email,
    c.city,
    o.order_date,
    o.total_amount,
    CASE 
        WHEN o.total_amount >= 50000 THEN 'VIP заказ'
        WHEN o.total_amount >= 20000 THEN 'Крупный заказ'
        ELSE 'Обычный заказ'
    END AS order_type
FROM orders o
INNER JOIN customers c ON o.customer_id = c.customer_id
WHERE o.order_date >= '2024-01-01'
ORDER BY o.total_amount DESC
LIMIT 20;

-- Задача 4.3: Детализация заказов с товарами
SELECT 
    o.order_id,
    c.first_name || ' ' || c.last_name AS customer_name,
    p.product_name,
    cat.category_name,
    oi.quantity,
    oi.price,
    oi.quantity * oi.price AS item_total,
    o.order_date
FROM orders o
INNER JOIN customers c ON o.customer_id = c.customer_id
INNER JOIN order_items oi ON o.order_id = oi.order_id
INNER JOIN products p ON oi.product_id = p.product_id
INNER JOIN categories cat ON p.category_id = cat.category_id
WHERE o.order_date >= '2024-03-01' AND o.order_date < '2024-04-01'
ORDER BY o.order_date, o.order_id, oi.order_item_id;

-- Задача 4.4: Топ-продавцы товаров по категориям
SELECT 
    cat.category_name,
    p.product_name,
    SUM(oi.quantity) AS total_sold,
    SUM(oi.quantity * oi.price) AS total_revenue,
    COUNT(DISTINCT oi.order_id) AS orders_count,
    AVG(oi.price) AS avg_selling_price
FROM categories cat
INNER JOIN products p ON cat.category_id = p.category_id
INNER JOIN order_items oi ON p.product_id = oi.product_id
GROUP BY cat.category_id, cat.category_name, p.product_id, p.product_name
HAVING SUM(oi.quantity) >= 10  -- Минимум 10 проданных единиц
ORDER BY cat.category_name, total_revenue DESC;
```

#### 3️⃣ LEFT JOIN — включение всех записей левой таблицы

```sql
-- Задача 4.5: Все клиенты и их статистика заказов (включая тех, кто не заказывал)
SELECT 
    c.customer_id,
    c.first_name,
    c.last_name,
    c.city,
    c.gender,
    c.registration_date,
    COUNT(o.order_id) AS orders_count,
    COALESCE(SUM(o.total_amount), 0) AS total_spent,
    COALESCE(AVG(o.total_amount), 0) AS avg_order_value,
    COALESCE(MAX(o.order_date), 'Нет заказов') AS last_order_date,
    julianday('now') - julianday(c.registration_date) AS days_registered,
    
    -- Классификация клиентов
    CASE 
        WHEN COUNT(o.order_id) = 0 THEN 'Не покупал'
        WHEN COUNT(o.order_id) = 1 THEN 'Разовый покупатель'
        WHEN COUNT(o.order_id) <= 3 THEN 'Редкий покупатель'
        WHEN COUNT(o.order_id) <= 10 THEN 'Регулярный покупатель'
        ELSE 'VIP клиент'
    END AS customer_type
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name, c.city, c.gender, c.registration_date
ORDER BY total_spent DESC;

-- Задача 4.6: Товары и их продажи (включая непроданные)
SELECT 
    cat.category_name,
    p.product_id,
    p.product_name,
    p.price AS catalog_price,
    p.stock_quantity,
    COUNT(oi.order_item_id) AS times_ordered,
    COALESCE(SUM(oi.quantity), 0) AS total_sold,
    COALESCE(SUM(oi.quantity * oi.price), 0) AS total_revenue,
    COALESCE(AVG(oi.price), p.price) AS avg_selling_price,
    p.stock_quantity - COALESCE(SUM(oi.quantity), 0) AS remaining_stock,
    
    -- Статус товара
    CASE 
        WHEN COUNT(oi.order_item_id) = 0 THEN 'Не продавался'
        WHEN COUNT(oi.order_item_id) <= 5 THEN 'Низкий спрос'
        WHEN COUNT(oi.order_item_id) <= 20 THEN 'Средний спрос'
        ELSE 'Высокий спрос'
    END AS demand_level
FROM categories cat
LEFT JOIN products p ON cat.category_id = p.category_id
LEFT JOIN order_items oi ON p.product_id = oi.product_id
GROUP BY cat.category_name, p.product_id, p.product_name, p.price, p.stock_quantity
ORDER BY cat.category_name, total_revenue DESC;
```

#### 4️⃣ Сложные JOIN запросы

```sql
-- Задача 4.7: Анализ покупательского поведения по категориям
SELECT 
    c.city,
    c.gender,
    cat.category_name,
    COUNT(DISTINCT c.customer_id) AS customers_in_category,
    COUNT(DISTINCT o.order_id) AS orders_count,
    SUM(oi.quantity) AS items_purchased,
    SUM(oi.quantity * oi.price) AS category_revenue,
    AVG(oi.price) AS avg_item_price,
    AVG(o.total_amount) AS avg_order_value
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
INNER JOIN order_items oi ON o.order_id = oi.order_id
INNER JOIN products p ON oi.product_id = p.product_id
INNER JOIN categories cat ON p.category_id = cat.category_id
WHERE c.city IN ('Москва', 'Санкт-Петербург', 'Новосибирск')
  AND o.order_date >= '2024-01-01'
GROUP BY c.city, c.gender, cat.category_id, cat.category_name
HAVING COUNT(DISTINCT o.order_id) >= 5  -- Минимум 5 заказов
ORDER BY c.city, c.gender, category_revenue DESC;

-- Задача 4.8: Кросс-категорийный анализ (какие категории покупают вместе)
SELECT 
    cat1.category_name AS category_1,
    cat2.category_name AS category_2,
    COUNT(DISTINCT o.order_id) AS orders_with_both,
    COUNT(DISTINCT o.customer_id) AS customers_bought_both,
    AVG(o.total_amount) AS avg_order_value,
    SUM(oi1.quantity * oi1.price + oi2.quantity * oi2.price) AS combined_revenue
FROM orders o
INNER JOIN order_items oi1 ON o.order_id = oi1.order_id
INNER JOIN order_items oi2 ON o.order_id = oi2.order_id AND oi1.order_item_id != oi2.order_item_id
INNER JOIN products p1 ON oi1.product_id = p1.product_id
INNER JOIN products p2 ON oi2.product_id = p2.product_id
INNER JOIN categories cat1 ON p1.category_id = cat1.category_id
INNER JOIN categories cat2 ON p2.category_id = cat2.category_id
WHERE cat1.category_id < cat2.category_id  -- Избегаем дублирования пар
  AND o.order_date >= '2024-01-01'
GROUP BY cat1.category_id, cat1.category_name, cat2.category_id, cat2.category_name
HAVING COUNT(DISTINCT o.order_id) >= 10
ORDER BY orders_with_both DESC;
```

#### 5️⃣ Практические бизнес-запросы

```sql
-- Задача 4.9: Отчет по лояльности клиентов
SELECT 
    c.customer_id,
    c.first_name || ' ' || c.last_name AS customer_name,
    c.city,
    c.email,
    c.registration_date,
    COUNT(DISTINCT o.order_id) AS total_orders,
    COUNT(DISTINCT DATE(o.order_date)) AS active_days,
    SUM(o.total_amount) AS lifetime_value,
    AVG(o.total_amount) AS avg_order_value,
    MIN(o.order_date) AS first_order,
    MAX(o.order_date) AS last_order,
    julianday(MAX(o.order_date)) - julianday(MIN(o.order_date)) AS customer_lifespan_days,
    julianday('now') - julianday(MAX(o.order_date)) AS days_since_last_order,
    
    -- Метрики лояльности
    COUNT(DISTINCT strftime('%Y-%m', o.order_date)) AS active_months,
    ROUND(COUNT(DISTINCT o.order_id) * 1.0 / COUNT(DISTINCT strftime('%Y-%m', o.order_date)), 2) AS orders_per_month,
    
    -- Оценка лояльности
    CASE 
        WHEN COUNT(DISTINCT o.order_id) >= 10 AND julianday('now') - julianday(MAX(o.order_date)) <= 30 
            AND SUM(o.total_amount) >= 100000
        THEN 'Платиновый'
        WHEN COUNT(DISTINCT o.order_id) >= 5 AND julianday('now') - julianday(MAX(o.order_date)) <= 90 
            AND SUM(o.total_amount) >= 50000
        THEN 'Золотой'
        WHEN COUNT(DISTINCT o.order_id) >= 3 AND julianday('now') - julianday(MAX(o.order_date)) <= 180
        THEN 'Серебряный'
        WHEN julianday('now') - julianday(MAX(o.order_date)) > 365
        THEN 'Неактивный'
        ELSE 'Бронзовый'
    END AS loyalty_tier
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name, c.city, c.email, c.registration_date
ORDER BY lifetime_value DESC;

-- Задача 4.10: Анализ эффективности категорий товаров
SELECT 
    cat.category_name,
    COUNT(DISTINCT p.product_id) AS products_in_category,
    COUNT(DISTINCT oi.order_id) AS orders_with_category,
    COUNT(DISTINCT o.customer_id) AS customers_bought_category,
    SUM(oi.quantity) AS total_items_sold,
    SUM(oi.quantity * oi.price) AS total_revenue,
    AVG(oi.price) AS avg_selling_price,
    AVG(p.price) AS avg_catalog_price,
    ROUND(AVG(oi.price) / AVG(p.price) * 100, 2) AS avg_discount_percent,
    
    -- Показатели эффективности
    ROUND(SUM(oi.quantity * oi.price) / COUNT(DISTINCT p.product_id), 2) AS revenue_per_product,
    ROUND(SUM(oi.quantity) / COUNT(DISTINCT p.product_id), 2) AS items_sold_per_product,
    ROUND(COUNT(DISTINCT o.customer_id) * 100.0 / (SELECT COUNT(*) FROM customers), 2) AS customer_penetration_percent,
    
    -- Категоризация эффективности
    CASE 
        WHEN SUM(oi.quantity * oi.price) / COUNT(DISTINCT p.product_id) > 100000 THEN 'Высокодоходная'
        WHEN SUM(oi.quantity * oi.price) / COUNT(DISTINCT p.product_id) > 50000 THEN 'Среднедоходная'
        ELSE 'Низкодоходная'
    END AS revenue_category,
    
    CASE 
        WHEN COUNT(DISTINCT o.customer_id) * 100.0 / (SELECT COUNT(*) FROM customers) > 50 THEN 'Популярная'
        WHEN COUNT(DISTINCT o.customer_id) * 100.0 / (SELECT COUNT(*) FROM customers) > 25 THEN 'Средняя популярность'
        ELSE 'Нишевая'
    END AS popularity_category
FROM categories cat
LEFT JOIN products p ON cat.category_id = p.category_id
LEFT JOIN order_items oi ON p.product_id = oi.product_id
LEFT JOIN orders o ON oi.order_id = o.order_id
WHERE o.order_date >= '2024-01-01' OR o.order_date IS NULL
GROUP BY cat.category_id, cat.category_name
ORDER BY total_revenue DESC;
```

### ✅ Ожидаемый результат:

- Понимание типов JOIN и их применения
- Навыки работы с многотабличными запросами
- Опыт создания комплексных аналитических отчетов
- Понимание реляционных связей в базах данных
- Способность анализировать бизнес-метрики через JOIN запросы

---

## 📋 Задание 5: Комплексный бизнес-анализ (Capstone Project)

**🎯 Цель:** Создать полноценную аналитическую систему с подзапросами и интеграцией Power Query

**🛠️ Инструменты:** SQLite DB Browser, Power BI/Excel с Power Query

**⏱️ Время:** 150 минут

### Что нужно сделать:

#### 1️⃣ Создание представлений (Views) для анализа

```sql
-- Задача 5.1: Создание базовых представлений для удобства анализа

-- Представление: Детализированная информация о заказах
CREATE VIEW v_order_details AS
SELECT 
    o.order_id,
    o.customer_id,
    c.first_name || ' ' || c.last_name AS customer_name,
    c.city,
    c.gender,
    o.order_date,
    strftime('%Y', o.order_date) AS order_year,
    strftime('%m', o.order_date) AS order_month,
    strftime('%Y-%m', o.order_date) AS order_year_month,
    CASE strftime('%w', o.order_date)
        WHEN '0' THEN 'Воскресенье'
        WHEN '1' THEN 'Понедельник'
        WHEN '2' THEN 'Вторник'
        WHEN '3' THEN 'Среда'
        WHEN '4' THEN 'Четверг'
        WHEN '5' THEN 'Пятница'
        WHEN '6' THEN 'Суббота'
    END AS order_day_of_week,
    o.total_amount,
    CASE 
        WHEN o.total_amount >= 100000 THEN 'Премиум'
        WHEN o.total_amount >= 50000 THEN 'Высокий'
        WHEN o.total_amount >= 20000 THEN 'Средний'
        ELSE 'Базовый'
    END AS order_tier
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id;

-- Представление: Анализ товаров с продажами
CREATE VIEW v_product_performance AS
SELECT 
    p.product_id,
    p.product_name,
    cat.category_name,
    p.price AS catalog_price,
    p.stock_quantity,
    COUNT(oi.order_item_id) AS times_ordered,
    COALESCE(SUM(oi.quantity), 0) AS total_sold,
    COALESCE(SUM(oi.quantity * oi.price), 0) AS total_revenue,
    COALESCE(AVG(oi.price), p.price) AS avg_selling_price,
    COALESCE(MAX(DATE(o.order_date)), 'Никогда') AS last_sale_date
FROM products p
JOIN categories cat ON p.category_id = cat.category_id
LEFT JOIN order_items oi ON p.product_id = oi.product_id
LEFT JOIN orders o ON oi.order_id = o.order_id
GROUP BY p.product_id, p.product_name, cat.category_name, p.price, p.stock_quantity;

-- Тестируем представления
SELECT * FROM v_order_details WHERE order_year_month = '2024-03' LIMIT 10;
SELECT * FROM v_product_performance ORDER BY total_revenue DESC LIMIT 10;
```

#### 2️⃣ Продвинутые подзапросы и аналитические функции

```sql
-- Задача 5.2: Анализ трендов с подзапросами

-- Ежемесячный рост продаж
SELECT 
    order_year_month,
    monthly_revenue,
    customers_count,
    orders_count,
    
    -- Сравнение с предыдущим месяцем (используем подзапрос)
    (SELECT SUM(total_amount) 
     FROM v_order_details v2 
     WHERE v2.order_year_month = 
        (SELECT MAX(v3.order_year_month) 
         FROM v_order_details v3 
         WHERE v3.order_year_month < v1.order_year_month)) AS prev_month_revenue,
    
    -- Процент роста
    ROUND(
        (monthly_revenue - 
         (SELECT SUM(total_amount) 
          FROM v_order_details v2 
          WHERE v2.order_year_month = 
            (SELECT MAX(v3.order_year_month) 
             FROM v_order_details v3 
             WHERE v3.order_year_month < v1.order_year_month))
        ) * 100.0 / 
        NULLIF((SELECT SUM(total_amount) 
                FROM v_order_details v2 
                WHERE v2.order_year_month = 
                  (SELECT MAX(v3.order_year_month) 
                   FROM v_order_details v3 
                   WHERE v3.order_year_month < v1.order_year_month)), 0), 2
    ) AS growth_percent
FROM (
    SELECT 
        order_year_month,
        SUM(total_amount) AS monthly_revenue,
        COUNT(DISTINCT customer_id) AS customers_count,
        COUNT(*) AS orders_count
    FROM v_order_details
    WHERE order_year >= '2023'
    GROUP BY order_year_month
) v1
ORDER BY order_year_month;

-- Задача 5.3: Поиск выбросов и аномалий
-- Клиенты с аномально высокими заказами
SELECT 
    customer_id,
    customer_name,
    city,
    order_id,
    order_date,
    total_amount,
    
    -- Средний чек клиента
    (SELECT AVG(total_amount) 
     FROM v_order_details v2 
     WHERE v2.customer_id = v1.customer_id) AS customer_avg_order,
    
    -- Общий средний чек
    (SELECT AVG(total_amount) FROM v_order_details) AS global_avg_order,
    
    -- Отклонение от личной нормы клиента
    ROUND(total_amount / 
          NULLIF((SELECT AVG(total_amount) 
                  FROM v_order_details v2 
                  WHERE v2.customer_id = v1.customer_id), 0), 2) AS personal_deviation,
    
    -- Отклонение от общей нормы
    ROUND(total_amount / 
          (SELECT AVG(total_amount) FROM v_order_details), 2) AS global_deviation
FROM v_order_details v1
WHERE total_amount > (
    SELECT AVG(total_amount) + 2 * 
    (SELECT 
        SQRT(AVG((total_amount - (SELECT AVG(total_amount) FROM v_order_details)) * 
                 (total_amount - (SELECT AVG(total_amount) FROM v_order_details))))
     FROM v_order_details)
    FROM v_order_details
)
ORDER BY total_amount DESC;
```

#### 3️⃣ Создание KPI дашборда

```sql
-- Задача 5.4: Ключевые метрики для дашборда

-- Основные KPI за последние 30, 90 и 365 дней
WITH kpi_periods AS (
    SELECT 'Последние 30 дней' AS period, 30 AS days
    UNION ALL SELECT 'Последние 90 дней', 90
    UNION ALL SELECT 'Последние 365 дней', 365
),
kpi_calculations AS (
    SELECT 
        kp.period,
        COUNT(DISTINCT vod.order_id) AS orders_count,
        COUNT(DISTINCT vod.customer_id) AS unique_customers,
        SUM(vod.total_amount) AS total_revenue,
        AVG(vod.total_amount) AS avg_order_value,
        SUM(vod.total_amount) / COUNT(DISTINCT vod.customer_id) AS revenue_per_customer,
        COUNT(DISTINCT vod.order_id) / COUNT(DISTINCT vod.customer_id) AS orders_per_customer,
        COUNT(DISTINCT DATE(vod.order_date)) AS active_days,
        SUM(vod.total_amount) / COUNT(DISTINCT DATE(vod.order_date)) AS avg_daily_revenue
    FROM kpi_periods kp
    LEFT JOIN v_order_details vod ON 
        julianday('now') - julianday(vod.order_date) <= kp.days
    GROUP BY kp.period, kp.days
)
SELECT 
    period,
    orders_count,
    unique_customers,
    ROUND(total_revenue, 2) AS total_revenue,
    ROUND(avg_order_value, 2) AS avg_order_value,
    ROUND(revenue_per_customer, 2) AS revenue_per_customer,
    ROUND(orders_per_customer, 2) AS orders_per_customer,
    active_days,
    ROUND(avg_daily_revenue, 2) AS avg_daily_revenue
FROM kpi_calculations
ORDER BY 
    CASE 
        WHEN period = 'Последние 30 дней' THEN 1
        WHEN period = 'Последние 90 дней' THEN 2
        WHEN period = 'Последние 365 дней' THEN 3
    END;

-- Задача 5.5: Воронка продаж по городам
SELECT 
    city,
    total_customers,
    customers_with_orders,
    ROUND(customers_with_orders * 100.0 / total_customers, 2) AS conversion_rate,
    total_orders,
    ROUND(total_orders * 1.0 / customers_with_orders, 2) AS orders_per_active_customer,
    total_revenue,
    ROUND(total_revenue / customers_with_orders, 2) AS revenue_per_active_customer,
    ROUND(total_revenue / total_orders, 2) AS avg_order_value
FROM (
    SELECT 
        c.city,
        COUNT(c.customer_id) AS total_customers,
        COUNT(DISTINCT o.customer_id) AS customers_with_orders,
        COUNT(o.order_id) AS total_orders,
        COALESCE(SUM(o.total_amount), 0) AS total_revenue
    FROM customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id
    WHERE c.city IN ('Москва', 'Санкт-Петербург', 'Новосибирск', 'Екатеринбург', 'Казань')
    GROUP BY c.city
) city_stats
ORDER BY conversion_rate DESC;
```

#### 4️⃣ Интеграция с Power Query

```sql
-- Задача 5.6: Создание запросов для Power Query/Power BI

-- Запрос 1: Месячные тренды для временных графиков
-- Этот запрос будет использоваться в Power BI для создания трендовых графиков
SELECT 
    strftime('%Y-%m', order_date) AS YearMonth,
    strftime('%Y', order_date) AS Year,
    strftime('%m', order_date) AS Month,
    CASE strftime('%m', order_date)
        WHEN '01' THEN 'Январь'
        WHEN '02' THEN 'Февраль'
        WHEN '03' THEN 'Март'
        WHEN '04' THEN 'Апрель'
        WHEN '05' THEN 'Май'
        WHEN '06' THEN 'Июнь'
        WHEN '07' THEN 'Июль'
        WHEN '08' THEN 'Август'
        WHEN '09' THEN 'Сентябрь'
        WHEN '10' THEN 'Октябрь'
        WHEN '11' THEN 'Ноябрь'
        WHEN '12' THEN 'Декабрь'
    END AS MonthName,
    COUNT(*) AS OrdersCount,
    COUNT(DISTINCT customer_id) AS UniqueCustomers,
    SUM(total_amount) AS TotalRevenue,
    AVG(total_amount) AS AvgOrderValue,
    MIN(total_amount) AS MinOrderValue,
    MAX(total_amount) AS MaxOrderValue
FROM orders
WHERE order_date >= '2023-01-01'
GROUP BY strftime('%Y-%m', order_date)
ORDER BY YearMonth;

-- Запрос 2: Данные для геоаналитики (по городам)
SELECT 
    c.city AS City,
    COUNT(DISTINCT c.customer_id) AS TotalCustomers,
    COUNT(o.order_id) AS TotalOrders,
    COUNT(DISTINCT o.customer_id) AS ActiveCustomers,
    SUM(o.total_amount) AS TotalRevenue,
    AVG(o.total_amount) AS AvgOrderValue,
    ROUND(COUNT(o.order_id) * 1.0 / COUNT(DISTINCT c.customer_id), 2) AS OrdersPerCustomer,
    ROUND(SUM(o.total_amount) / COUNT(DISTINCT c.customer_id), 2) AS RevenuePerCustomer,
    ROUND(COUNT(DISTINCT o.customer_id) * 100.0 / COUNT(DISTINCT c.customer_id), 2) AS ConversionRate,
    
    -- Координаты для визуализации на карте (примерные)
    CASE c.city
        WHEN 'Москва' THEN 55.7558
        WHEN 'Санкт-Петербург' THEN 59.9311
        WHEN 'Новосибирск' THEN 55.0084
        WHEN 'Екатеринбург' THEN 56.8431
        WHEN 'Казань' THEN 55.8304
        WHEN 'Нижний Новгород' THEN 56.2965
        ELSE 55.0000
    END AS Latitude,
    
    CASE c.city
        WHEN 'Москва' THEN 37.6176
        WHEN 'Санкт-Петербург' THEN 30.3609
        WHEN 'Новосибирск' THEN 82.9357
        WHEN 'Екатеринбург' THEN 60.6454
        WHEN 'Казань' THEN 49.0661
        WHEN 'Нижний Новгород' THEN 44.0845
        ELSE 37.0000
    END AS Longitude
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.city
HAVING COUNT(DISTINCT c.customer_id) >= 10  -- Только города с минимум 10 клиентами
ORDER BY TotalRevenue DESC;

-- Запрос 3: Детализация по категориям для анализа продуктовой линейки
SELECT 
    cat.category_name AS CategoryName,
    p.product_name AS ProductName,
    p.price AS CatalogPrice,
    COUNT(oi.order_item_id) AS TimesOrdered,
    SUM(oi.quantity) AS TotalQuantitySold,
    SUM(oi.quantity * oi.price) AS TotalRevenue,
    AVG(oi.price) AS AvgSellingPrice,
    p.stock_quantity AS CurrentStock,
    
    -- Метрики эффективности
    ROUND(SUM(oi.quantity * oi.price) / NULLIF(COUNT(oi.order_item_id), 0), 2) AS RevenuePerOrder,
    ROUND(AVG(oi.price) / p.price * 100, 2) AS AvgDiscountPercent,
    
    -- Последняя продажа
    MAX(o.order_date) AS LastSaleDate,
    julianday('now') - julianday(MAX(o.order_date)) AS DaysSinceLastSale
FROM categories cat
JOIN products p ON cat.category_id = p.category_id
LEFT JOIN order_items oi ON p.product_id = oi.product_id
LEFT JOIN orders o ON oi.order_id = o.order_id
GROUP BY cat.category_name, p.product_id, p.product_name, p.price, p.stock_quantity
ORDER BY cat.category_name, TotalRevenue DESC;
```

#### 5️⃣ Создание Power Query подключения

**Инструкция для подключения Power BI к SQLite:**

```
1. Откройте Power BI Desktop
2. Получить данные → Больше → База данных → SQLite
3. Выберите файл ecommerce_database.db
4. В навигаторе выберите "Запрос SQL" 
5. Вставьте один из SQL запросов выше
6. Нажмите "Загрузить" или "Преобразовать данные"
```

**Power Query M код для параметризованного запроса:**

```m
// Параметризованный запрос для анализа по периодам
let
    // Параметры (можно сделать настраиваемыми)
    StartDate = #date(2024, 1, 1),
    EndDate = Date.From(DateTime.LocalNow()),
    
    // Преобразование дат в строки для SQL
    StartDateText = Date.ToText(StartDate, "yyyy-MM-dd"),
    EndDateText = Date.ToText(EndDate, "yyyy-MM-dd"),
    
    // SQL запрос с параметрами
    SqlQuery = "
    SELECT 
        strftime('%Y-%m', order_date) AS YearMonth,
        COUNT(*) AS OrdersCount,
        COUNT(DISTINCT customer_id) AS UniqueCustomers,
        SUM(total_amount) AS TotalRevenue,
        AVG(total_amount) AS AvgOrderValue
    FROM orders
    WHERE order_date >= '" & StartDateText & "' 
      AND order_date <= '" & EndDateText & "'
    GROUP BY strftime('%Y-%m', order_date)
    ORDER BY YearMonth
    ",
    
    // Подключение к базе данных
    Source = Sqlite.Database(File.Contents("C:\path\to\ecommerce_database.db"), [Query=SqlQuery]),
    
    // Преобразование типов данных
    ChangedTypes = Table.TransformColumnTypes(Source, {
        {"YearMonth", type text},
        {"OrdersCount", Int64.Type},
        {"UniqueCustomers", Int64.Type},
        {"TotalRevenue", type number},
        {"AvgOrderValue", type number}
    })
in
    ChangedTypes
```

#### 6️⃣ Финальный аналитический отчет

```sql
-- Задача 5.7: Исполнительное резюме (Executive Summary)
-- Создайте один комплексный запрос, который дает полную картину бизнеса

WITH business_summary AS (
    -- Основные метрики
    SELECT 
        COUNT(DISTINCT c.customer_id) AS total_customers,
        COUNT(DISTINCT o.order_id) AS total_orders,
        COUNT(DISTINCT p.product_id) AS total_products,
        COUNT(DISTINCT cat.category_id) AS total_categories,
        SUM(o.total_amount) AS total_revenue,
        AVG(o.total_amount) AS avg_order_value,
        MIN(o.order_date) AS first_order_date,
        MAX(o.order_date) AS last_order_date
    FROM customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id
    LEFT JOIN order_items oi ON o.order_id = oi.order_id
    LEFT JOIN products p ON oi.product_id = p.product_id
    LEFT JOIN categories cat ON p.category_id = cat.category_id
),
customer_segments AS (
    -- Сегментация клиентов
    SELECT 
        customer_segment,
        COUNT(*) AS customers_count,
        AVG(total_spent) AS avg_customer_value,
        SUM(total_spent) AS segment_revenue
    FROM (
        SELECT 
            c.customer_id,
            CASE 
                WHEN COUNT(o.order_id) >= 10 AND SUM(o.total_amount) >= 200000 THEN 'VIP'
                WHEN COUNT(o.order_id) >= 5 AND SUM(o.total_amount) >= 100000 THEN 'Премиум'
                WHEN COUNT(o.order_id) >= 3 AND SUM(o.total_amount) >= 50000 THEN 'Стандарт'
                WHEN COUNT(o.order_id) >= 1 THEN 'Базовый'
                ELSE 'Неактивный'
            END AS customer_segment,
            COALESCE(SUM(o.total_amount), 0) AS total_spent
        FROM customers c
        LEFT JOIN orders o ON c.customer_id = o.customer_id
        GROUP BY c.customer_id
    )
    GROUP BY customer_segment
),
top_categories AS (
    -- Топ категории
    SELECT 
        cat.category_name,
        SUM(oi.quantity * oi.price) AS category_revenue,
        COUNT(DISTINCT o.customer_id) AS customers_count
    FROM categories cat
    JOIN products p ON cat.category_id = p.category_id
    JOIN order_items oi ON p.product_id = oi.product_id
    JOIN orders o ON oi.order_id = o.order_id
    GROUP BY cat.category_id, cat.category_name
    ORDER BY category_revenue DESC
    LIMIT 5
)
-- Итоговый отчет
SELECT 
    'Общие метрики' AS section,
    'Всего клиентов: ' || bs.total_customers || 
    ', Заказов: ' || bs.total_orders ||
    ', Выручка: ' || ROUND(bs.total_revenue, 0) || ' руб.' ||
    ', Средний чек: ' || ROUND(bs.avg_order_value, 0) || ' руб.' AS metrics
FROM business_summary bs

UNION ALL

SELECT 
    'Сегменты клиентов' AS section,
    customer_segment || ': ' || customers_count || ' клиентов (' ||
    ROUND(segment_revenue, 0) || ' руб., средняя ценность: ' ||
    ROUND(avg_customer_value, 0) || ' руб.)' AS metrics
FROM customer_segments
ORDER BY 
    CASE 
        WHEN section = 'Общие метрики' THEN 1
        ELSE 2
    END,
    metrics DESC;
```

### ✅ Ожидаемый результат:

- **Создание представлений (Views)** для упрощения сложных запросов
- **Продвинутые аналитические запросы** с подзапросами и функциями  
- **KPI дашборд** с ключевыми метриками бизнеса
- **Интеграция с Power Query** для автоматизации отчетности
- **Комплексный бизнес-анализ** с исполнительным резюме
- **Файлы:** SQL скрипты, Power Query M код, аналитические отчеты

---

## 💡 Рекомендации по выполнению

### 📋 Общие советы:

1. **🔄 Итеративный подход:** Начинайте с простых запросов, постепенно усложняя
2. **📝 Документирование:** Сохраняйте все работающие запросы в отдельные .sql файлы
3. **🧪 Тестирование:** Проверяйте результаты на логичность и соответствие ожиданиям
4. **📊 Визуализация:** Представляйте, как результаты будут выглядеть в дашбордах

### 🔧 Технические требования:

**Необходимое ПО:**
- DB Browser for SQLite (бесплатно)
- Power BI Desktop или Excel с Power Query
- Текстовый редактор для SQL скриптов

**Файлы для работы:**
- `ecommerce_database.db` — основная база данных
- `sample_queries.sql` — примеры запросов для справки
- `powerquery_examples.txt` — M код для интеграции

### 📁 Структура результатов:

```
chapter-19-results/
├── task-1-basic-select.sql
├── task-2-filtering-sorting.sql  
├── task-3-aggregates-groupby.sql
├── task-4-joins.sql
├── task-5-complex-analysis.sql
├── power-query-integration.m
└── executive-summary.txt
```

### ❓ Часто задаваемые вопросы:

**Q: Какую СУБД использовать?**
A: SQLite для обучения (простота), PostgreSQL/MySQL для продакшена

**Q: Не работает GROUP BY?**  
A: Проверьте, что все поля в SELECT либо в GROUP BY, либо в агрегатных функциях

**Q: Медленно выполняются запросы?**
A: Используйте LIMIT для ограничения результатов, оптимизируйте WHERE условия

**Q: Как подключить Power Query к SQLite?**
A: Через "Получить данные" → "База данных" → "SQLite" → выберите .db файл

---

- 🔙 [Предыдущая глава: Глава 18 - Работа с API: получение и автоматизация данных](../chapter-18/README.md)
- 🔜 [Следующая глава: Глава 20 - SQL: JOIN, подзапросы, CTE](../chapter-20/README.md)

---

- 📢 Присоединяйтесь к чату курса: https://t.me/analytics_course_chat
- 📢 Канал курса: https://t.me/analytics_course_channel