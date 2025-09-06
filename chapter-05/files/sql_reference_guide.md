# 📚 Справочник SQL для PostgreSQL

## 📋 Основные концепции

**SQL (Structured Query Language)** — стандартизированный язык для работы с реляционными базами данных. В этом справочнике собраны все основные команды и конструкции, необходимые для изучения главы 5.

---

## 🏗 DDL - Data Definition Language (Определение структуры данных)

### CREATE TABLE - Создание таблицы

**Базовый синтаксис:**
```sql
CREATE TABLE table_name (
    column1 datatype constraints,
    column2 datatype constraints,
    ...
    table_constraints
);
```

**Пример с ограничениями:**
```sql
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(200) NOT NULL,
    price DECIMAL(10,2) NOT NULL CHECK (price > 0),
    stock_quantity INTEGER DEFAULT 0 CHECK (stock_quantity >= 0),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Типы данных PostgreSQL

#### Числовые типы:
- `SERIAL` — автоинкрементное целое (1, 2, 3, ...)
- `INTEGER` / `INT` — целые числа (-2147483648 до +2147483647)
- `BIGINT` — большие целые числа
- `DECIMAL(p,s)` — точные десятичные числа (p=всего цифр, s=после запятой)
- `NUMERIC(p,s)` — аналог DECIMAL
- `REAL` / `FLOAT4` — числа с плавающей точкой (4 байта)
- `DOUBLE PRECISION` / `FLOAT8` — числа с плавающей точкой (8 байт)

#### Текстовые типы:
- `VARCHAR(n)` — строка переменной длины (до n символов)
- `CHAR(n)` — строка фиксированной длины (дополняется пробелами)
- `TEXT` — строка неограниченной длины
- `UUID` — уникальный идентификатор

#### Дата и время:
- `DATE` — дата (год-месяц-день)
- `TIME` — время (час:минута:секунда)
- `TIMESTAMP` — дата и время
- `TIMESTAMPTZ` — дата и время с часовым поясом
- `INTERVAL` — интервал времени

#### Логические и специальные:
- `BOOLEAN` — TRUE/FALSE/NULL
- `JSON` — данные в формате JSON
- `JSONB` — бинарный JSON (оптимизированный)
- `ARRAY` — массивы

### Ограничения (Constraints)

```sql
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,                    -- Первичный ключ
    email VARCHAR(100) NOT NULL UNIQUE,                -- Не NULL и уникальный
    age INTEGER CHECK (age >= 18),                     -- Проверка значения
    city VARCHAR(50) DEFAULT 'Москва',                 -- Значение по умолчанию
    registration_date DATE DEFAULT CURRENT_DATE,        -- Текущая дата
    category_id INTEGER REFERENCES categories(id)       -- Внешний ключ
);
```

**Типы ограничений:**
- `PRIMARY KEY` — первичный ключ (уникальный, не NULL)
- `UNIQUE` — уникальные значения
- `NOT NULL` — значение обязательно
- `CHECK (condition)` — проверка условия
- `DEFAULT value` — значение по умолчанию
- `REFERENCES table(column)` — внешний ключ

### CREATE INDEX - Создание индексов

```sql
-- Простой индекс
CREATE INDEX idx_products_name ON products(product_name);

-- Составной индекс
CREATE INDEX idx_orders_customer_date ON orders(customer_id, order_date);

-- Уникальный индекс
CREATE UNIQUE INDEX idx_customers_email ON customers(email);

-- Частичный индекс (только для активных записей)
CREATE INDEX idx_products_active ON products(product_name) WHERE is_active = TRUE;
```

### ALTER TABLE - Изменение структуры

```sql
-- Добавление столбца
ALTER TABLE products ADD COLUMN description TEXT;

-- Удаление столбца  
ALTER TABLE products DROP COLUMN old_column;

-- Изменение типа данных
ALTER TABLE products ALTER COLUMN price TYPE DECIMAL(12,2);

-- Добавление ограничения
ALTER TABLE products ADD CONSTRAINT chk_price CHECK (price > 0);

-- Переименование столбца
ALTER TABLE products RENAME COLUMN old_name TO new_name;
```

### DROP - Удаление объектов

```sql
-- Удаление таблицы
DROP TABLE table_name;

-- Удаление с каскадом (удаляет зависимые объекты)
DROP TABLE table_name CASCADE;

-- Удаление индекса
DROP INDEX index_name;

-- Удаление базы данных
DROP DATABASE database_name;
```

---

## 📊 DML - Data Manipulation Language (Манипуляция данными)

### SELECT - Выборка данных

**Базовый синтаксис:**
```sql
SELECT column1, column2, ...
FROM table_name
WHERE condition
GROUP BY column
HAVING group_condition
ORDER BY column ASC|DESC
LIMIT number OFFSET number;
```

**Примеры SELECT:**
```sql
-- Все столбцы
SELECT * FROM customers;

-- Конкретные столбцы
SELECT first_name, last_name, email FROM customers;

-- С псевдонимами столбцов
SELECT 
    first_name AS "Имя",
    last_name AS "Фамилия",
    email AS "Email"
FROM customers;

-- Вычисляемые поля
SELECT 
    product_name,
    price,
    price * 0.8 AS discounted_price
FROM products;
```

### WHERE - Условия фильтрации

**Операторы сравнения:**
```sql
-- Равенство
SELECT * FROM products WHERE price = 1000;

-- Неравенство
SELECT * FROM products WHERE price != 1000;
SELECT * FROM products WHERE price <> 1000;

-- Больше, меньше
SELECT * FROM products WHERE price > 1000;
SELECT * FROM products WHERE price <= 1000;

-- Диапазон значений
SELECT * FROM products WHERE price BETWEEN 1000 AND 5000;

-- Список значений
SELECT * FROM customers WHERE city IN ('Москва', 'СПб', 'Казань');

-- Исключение значений
SELECT * FROM customers WHERE city NOT IN ('Москва', 'СПб');
```

**Работа с текстом:**
```sql
-- Точное совпадение
SELECT * FROM customers WHERE first_name = 'Иван';

-- Поиск по шаблону
SELECT * FROM products WHERE product_name LIKE '%iPhone%';
SELECT * FROM products WHERE product_name LIKE 'Samsung%';
SELECT * FROM customers WHERE phone LIKE '+7-9__-___-__-__';

-- Регистронезависимый поиск
SELECT * FROM customers WHERE email ILIKE '%GMAIL%';

-- Регулярные выражения
SELECT * FROM customers WHERE phone ~ '^\+7-9[0-9]{2}-[0-9]{3}-[0-9]{2}-[0-9]{2}$';
```

**Работа с NULL:**
```sql
-- Проверка на NULL
SELECT * FROM customers WHERE phone IS NULL;
SELECT * FROM customers WHERE phone IS NOT NULL;

-- Замена NULL значений
SELECT 
    first_name,
    COALESCE(phone, 'Не указан') AS phone
FROM customers;
```

**Логические операторы:**
```sql
-- AND (И)
SELECT * FROM products 
WHERE price > 1000 AND category_id = 1;

-- OR (ИЛИ)
SELECT * FROM customers 
WHERE city = 'Москва' OR city = 'СПб';

-- NOT (НЕ)
SELECT * FROM products 
WHERE NOT (price > 10000);

-- Комбинирование с скобками
SELECT * FROM orders
WHERE (status = 'delivered' OR status = 'shipped')
  AND order_date >= '2024-01-01';
```

### ORDER BY - Сортировка

```sql
-- По одному полю (по возрастанию)
SELECT * FROM products ORDER BY price;
SELECT * FROM products ORDER BY price ASC;

-- По убыванию
SELECT * FROM products ORDER BY price DESC;

-- По нескольким полям
SELECT * FROM customers 
ORDER BY city, last_name, first_name;

-- NULL значения в конце
SELECT * FROM customers 
ORDER BY phone NULLS LAST;

-- Сортировка по вычисляемому полю
SELECT first_name, last_name 
FROM customers 
ORDER BY LENGTH(first_name) DESC;
```

### LIMIT и OFFSET - Ограничение результатов

```sql
-- Первые 10 записей
SELECT * FROM products ORDER BY price LIMIT 10;

-- Записи с 11 по 20 (пагинация)
SELECT * FROM products ORDER BY price LIMIT 10 OFFSET 10;

-- Только самый дорогой товар
SELECT * FROM products ORDER BY price DESC LIMIT 1;
```

### INSERT - Добавление данных

```sql
-- Одна запись со всеми полями
INSERT INTO customers (first_name, last_name, email, city)
VALUES ('Иван', 'Петров', 'ivan.petrov@email.com', 'Москва');

-- Несколько записей за раз
INSERT INTO categories (category_name, description) VALUES
('Электроника', 'Бытовая техника и электроника'),
('Одежда', 'Мужская и женская одежда'),
('Книги', 'Художественная и техническая литература');

-- Вставка с возвратом значений
INSERT INTO products (product_name, price, category_id)
VALUES ('iPhone 15', 99990.00, 1)
RETURNING product_id, product_name;

-- Вставка из другой таблицы
INSERT INTO archived_orders (order_id, customer_id, total_amount)
SELECT order_id, customer_id, total_amount 
FROM orders 
WHERE status = 'delivered';
```

### UPDATE - Обновление данных

```sql
-- Обновление одной записи
UPDATE products 
SET price = 89990.00 
WHERE product_id = 1;

-- Обновление нескольких полей
UPDATE customers 
SET 
    phone = '+7-900-123-45-67',
    city = 'Санкт-Петербург'
WHERE customer_id = 5;

-- Обновление с условием
UPDATE products 
SET price = price * 0.9 
WHERE category_id = 1 AND stock_quantity > 10;

-- Обновление с подзапросом
UPDATE orders 
SET status = 'shipped'
WHERE order_id IN (
    SELECT order_id FROM order_shipments 
    WHERE shipped_date = CURRENT_DATE
);
```

### DELETE - Удаление данных

```sql
-- Удаление конкретной записи
DELETE FROM customers WHERE customer_id = 10;

-- Удаление с условием
DELETE FROM products 
WHERE is_active = FALSE AND stock_quantity = 0;

-- Удаление всех записей (осторожно!)
DELETE FROM temp_table;

-- Удаление с подзапросом
DELETE FROM orders 
WHERE customer_id IN (
    SELECT customer_id FROM customers 
    WHERE is_active = FALSE
);
```

---

## 📈 Агрегатные функции и группировка

### Основные агрегатные функции

```sql
-- Подсчет записей
SELECT COUNT(*) FROM products;                    -- Все записи
SELECT COUNT(phone) FROM customers;               -- Не NULL значения
SELECT COUNT(DISTINCT city) FROM customers;       -- Уникальные значения

-- Суммирование
SELECT SUM(price) FROM products;                  -- Сумма цен
SELECT SUM(price * stock_quantity) FROM products; -- Общая стоимость

-- Среднее значение
SELECT AVG(price) FROM products;                  -- Средняя цена
SELECT ROUND(AVG(price), 2) FROM products;       -- Округление до 2 знаков

-- Минимум и максимум
SELECT MIN(price), MAX(price) FROM products;      -- Мин и макс цена
SELECT MIN(registration_date) FROM customers;     -- Первая регистрация
```

### GROUP BY - Группировка

```sql
-- Группировка по одному полю
SELECT 
    category_id,
    COUNT(*) as products_count,
    AVG(price) as avg_price
FROM products 
GROUP BY category_id;

-- Группировка по нескольким полям
SELECT 
    category_id,
    is_active,
    COUNT(*) as count,
    SUM(stock_quantity) as total_stock
FROM products 
GROUP BY category_id, is_active;

-- Группировка с JOIN
SELECT 
    c.category_name,
    COUNT(p.product_id) as products_count,
    ROUND(AVG(p.price), 2) as avg_price
FROM categories c
LEFT JOIN products p ON c.category_id = p.category_id
GROUP BY c.category_id, c.category_name
ORDER BY products_count DESC;
```

### HAVING - Фильтрация групп

```sql
-- HAVING применяется к группам (после GROUP BY)
SELECT 
    category_id,
    COUNT(*) as products_count,
    AVG(price) as avg_price
FROM products 
GROUP BY category_id
HAVING COUNT(*) > 5 AND AVG(price) > 10000;

-- Сложные условия HAVING
SELECT 
    city,
    COUNT(*) as customers_count
FROM customers 
GROUP BY city
HAVING COUNT(*) >= 3
ORDER BY customers_count DESC;
```

---

## 🔗 JOIN - Объединение таблиц

### INNER JOIN - Внутреннее соединение

```sql
-- Основной синтаксис
SELECT 
    c.first_name,
    c.last_name,
    o.order_date,
    o.total_amount
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id;

-- JOIN с условиями WHERE
SELECT 
    p.product_name,
    cat.category_name,
    p.price
FROM products p
INNER JOIN categories cat ON p.category_id = cat.category_id
WHERE p.price > 50000;
```

### LEFT JOIN - Левое соединение

```sql
-- Все клиенты, включая тех, кто не делал заказов
SELECT 
    c.first_name,
    c.last_name,
    COUNT(o.order_id) as orders_count
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name;

-- Клиенты без заказов
SELECT c.*
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE o.customer_id IS NULL;
```

### RIGHT JOIN и FULL JOIN

```sql
-- RIGHT JOIN (редко используется)
SELECT *
FROM orders o
RIGHT JOIN customers c ON o.customer_id = c.customer_id;

-- FULL OUTER JOIN - все записи из обеих таблиц
SELECT *
FROM customers c
FULL OUTER JOIN orders o ON c.customer_id = o.customer_id;
```

### Множественные JOIN

```sql
-- Соединение трех таблиц
SELECT 
    c.first_name,
    c.last_name,
    o.order_date,
    p.product_name,
    oi.quantity,
    oi.unit_price
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
WHERE o.status = 'delivered'
ORDER BY o.order_date DESC;
```

---

## 🔍 Подзапросы (Subqueries)

### Скалярные подзапросы

```sql
-- Товары дороже средней цены
SELECT product_name, price
FROM products
WHERE price > (SELECT AVG(price) FROM products);

-- Клиенты с максимальной суммой заказов
SELECT *
FROM customers
WHERE customer_id = (
    SELECT customer_id 
    FROM orders 
    ORDER BY total_amount DESC 
    LIMIT 1
);
```

### Подзапросы с IN/NOT IN

```sql
-- Клиенты, которые делали заказы
SELECT *
FROM customers
WHERE customer_id IN (
    SELECT DISTINCT customer_id FROM orders
);

-- Товары, которые никогда не заказывали
SELECT *
FROM products
WHERE product_id NOT IN (
    SELECT DISTINCT product_id 
    FROM order_items 
    WHERE product_id IS NOT NULL
);
```

### EXISTS и NOT EXISTS

```sql
-- Клиенты с заказами (эффективнее чем IN)
SELECT *
FROM customers c
WHERE EXISTS (
    SELECT 1 FROM orders o 
    WHERE o.customer_id = c.customer_id
);

-- Категории без товаров
SELECT *
FROM categories cat
WHERE NOT EXISTS (
    SELECT 1 FROM products p 
    WHERE p.category_id = cat.category_id
);
```

---

## 📅 Работа с датами и временем

### Функции даты и времени

```sql
-- Текущие дата и время
SELECT 
    CURRENT_DATE as today,
    CURRENT_TIME as now_time,
    CURRENT_TIMESTAMP as now_full,
    NOW() as now_function;

-- Извлечение частей даты
SELECT 
    EXTRACT(YEAR FROM order_date) as order_year,
    EXTRACT(MONTH FROM order_date) as order_month,
    EXTRACT(DAY FROM order_date) as order_day,
    EXTRACT(DOW FROM order_date) as day_of_week  -- 0=Sunday
FROM orders;

-- Форматирование дат
SELECT 
    order_date,
    TO_CHAR(order_date, 'DD.MM.YYYY') as formatted_date,
    TO_CHAR(order_date, 'Month YYYY') as month_year,
    TO_CHAR(order_date, 'Day') as day_name
FROM orders;
```

### Арифметика с датами

```sql
-- Добавление/вычитание интервалов
SELECT 
    CURRENT_DATE,
    CURRENT_DATE + INTERVAL '1 day' as tomorrow,
    CURRENT_DATE - INTERVAL '1 week' as week_ago,
    CURRENT_DATE + INTERVAL '1 month' as next_month;

-- Разность между датами
SELECT 
    order_date,
    CURRENT_DATE - order_date as days_since_order
FROM orders;

-- Группировка по месяцам
SELECT 
    DATE_TRUNC('month', order_date) as month,
    COUNT(*) as orders_count
FROM orders
GROUP BY DATE_TRUNC('month', order_date)
ORDER BY month;
```

---

## 🧮 Строковые функции

```sql
-- Длина строки
SELECT LENGTH(product_name) FROM products;

-- Объединение строк
SELECT 
    first_name || ' ' || last_name as full_name,
    CONCAT(first_name, ' ', last_name) as full_name2
FROM customers;

-- Изменение регистра
SELECT 
    UPPER(city) as city_upper,
    LOWER(email) as email_lower,
    INITCAP(first_name) as name_proper
FROM customers;

-- Обрезка пробелов
SELECT TRIM('  текст с пробелами  ') as trimmed;

-- Извлечение подстроки
SELECT 
    SUBSTRING(phone FROM 1 FOR 3) as country_code,
    LEFT(email, POSITION('@' IN email) - 1) as username
FROM customers;

-- Замена текста
SELECT REPLACE(phone, '-', '.') as phone_dots FROM customers;
```

---

## 🎛 Условная логика

### CASE WHEN

```sql
-- Простой CASE
SELECT 
    product_name,
    price,
    CASE 
        WHEN price < 10000 THEN 'Бюджетный'
        WHEN price < 50000 THEN 'Средний'
        WHEN price < 100000 THEN 'Премиум'
        ELSE 'Люкс'
    END as price_category
FROM products;

-- CASE в агрегации
SELECT 
    SUM(CASE WHEN status = 'delivered' THEN total_amount ELSE 0 END) as delivered_revenue,
    SUM(CASE WHEN status = 'cancelled' THEN total_amount ELSE 0 END) as cancelled_revenue
FROM orders;
```

### COALESCE и NULLIF

```sql
-- COALESCE - первое не NULL значение
SELECT 
    first_name,
    COALESCE(phone, email, 'Контакт не указан') as contact
FROM customers;

-- NULLIF - возвращает NULL если значения равны
SELECT 
    product_name,
    NULLIF(stock_quantity, 0) as stock_or_null
FROM products;
```

---

## 📊 Window Functions (Оконные функции)

```sql
-- ROW_NUMBER - нумерация строк
SELECT 
    product_name,
    price,
    ROW_NUMBER() OVER (ORDER BY price DESC) as price_rank
FROM products;

-- RANK и DENSE_RANK
SELECT 
    customer_id,
    total_amount,
    RANK() OVER (ORDER BY total_amount DESC) as rank,
    DENSE_RANK() OVER (ORDER BY total_amount DESC) as dense_rank
FROM orders;

-- Партицирование (разбиение по группам)
SELECT 
    category_id,
    product_name,
    price,
    AVG(price) OVER (PARTITION BY category_id) as avg_price_in_category
FROM products;

-- LAG и LEAD - предыдущие и следующие значения
SELECT 
    order_date,
    total_amount,
    LAG(total_amount) OVER (ORDER BY order_date) as prev_order_amount
FROM orders
ORDER BY order_date;
```

---

## 💡 Полезные советы по оптимизации

### Использование индексов

```sql
-- Создание индексов для частых запросов
CREATE INDEX idx_orders_customer_id ON orders(customer_id);
CREATE INDEX idx_products_category_id ON products(category_id);
CREATE INDEX idx_orders_date ON orders(order_date);

-- Составные индексы
CREATE INDEX idx_orders_customer_date ON orders(customer_id, order_date);
```

### Анализ производительности

```sql
-- Просмотр плана выполнения
EXPLAIN SELECT * FROM products WHERE price > 50000;

-- Анализ с временем выполнения
EXPLAIN ANALYZE SELECT * FROM products p 
JOIN categories c ON p.category_id = c.category_id;
```

### Лучшие практики

1. **Всегда используйте WHERE** для ограничения результатов
2. **Создавайте индексы** на поля, используемые в WHERE и JOIN
3. **Используйте LIMIT** при тестировании запросов на больших таблицах
4. **Избегайте SELECT *** в продакшене, указывайте нужные поля
5. **Используйте EXISTS вместо IN** для больших подзапросов

---

📚 **Этот справочник покрывает 90% SQL-запросов, которые вам понадобятся в главе 5!**

🔗 Дополнительные ресурсы:
- [Официальная документация PostgreSQL](https://www.postgresql.org/docs/)
- [SQL Tutorial от W3Schools](https://www.w3schools.com/sql/)
- [PostgreSQL Exercises](https://pgexercises.com/)
