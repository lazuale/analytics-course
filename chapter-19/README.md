# 🗄 Глава 19: SQL — основные запросы, агрегаты, GROUP BY!

## 🎯 Что вы изучите

После изучения этой главы вы сможете:

* **🗣️ Понимать SQL** как язык для "разговора" с базами данных
* **📊 Писать SELECT запросы** для извлечения нужных данных  
* **🔍 Фильтровать данные** с помощью WHERE и различных условий
* **📈 Использовать агрегатные функции** COUNT, SUM, AVG, MIN, MAX
* **👥 Группировать данные** с GROUP BY и HAVING для аналитики
* **🔗 Объединять таблицы** с помощью базовых JOIN операций
* **🔄 Интегрировать SQL с Power Query** для комплексной аналитики
* **📊 Применять SQL в бизнесе** для решения реальных аналитических задач

## 🌟 SQL простыми словами

**SQL (Structured Query Language)** — это как универсальный язык для разговора с любой базой данных. Представьте библиотеку:

### 📚 Метафора библиотеки:
* **📖 База данных** — огромная библиотека с миллионами книг
* **📚 Таблицы** — разные секции (художественная литература, наука, история)
* **📄 Строки** — отдельные книги на полках
* **📝 Столбцы** — характеристики книг (название, автор, год, жанр)
* **👩‍💼 Библиотекарь** — SQL движок, который понимает ваши запросы
* **🗣️ Ваш запрос** — вопрос библиотекарю на специальном языке

Вместо того чтобы бегать по библиотеке самостоятельно, вы говорите библиотекарю: *"Найди мне все книги по программированию, написанные после 2020 года, отсортируй по рейтингу"* — и получаете точно то, что нужно.

### 💼 Зачем аналитику SQL в 2025:

**Работа с большими данными:**
```sql
-- Вместо обработки миллионов строк в Excel
-- Получаем нужные данные за секунды
SELECT customer_id, SUM(order_amount) as total_spent
FROM orders 
WHERE order_date >= '2024-01-01'
GROUP BY customer_id
ORDER BY total_spent DESC;
```

**Автоматизация отчетов:**
```sql
-- Один запрос заменяет часы ручной работы
SELECT 
    DATE_FORMAT(order_date, '%Y-%m') as month,
    COUNT(*) as orders_count,
    SUM(amount) as revenue,
    AVG(amount) as avg_order_value
FROM sales 
WHERE order_date >= DATE_SUB(CURRENT_DATE, INTERVAL 12 MONTH)
GROUP BY month
ORDER BY month;
```

**Интеграция с BI инструментами:**
```sql
-- SQL запросы питают Power BI, Tableau, Excel дашборды
-- Данные обновляются автоматически
```

## 📚 Основы SQL

### 🏗️ Структура базы данных

**База данных** состоит из **таблиц**, а таблицы из **строк** и **столбцов**:

```sql
-- Пример таблицы "customers" (клиенты)
+----+------------+-------+------------+--------+
| id | name       | age   | city       | status |
+----+------------+-------+------------+--------+
| 1  | Иван       | 25    | Москва     | VIP    |
| 2  | Мария      | 32    | СПб        | Обычный|
| 3  | Петр       | 28    | Казань     | VIP    |
+----+------------+-------+------------+--------+
```

**Терминология:**
- **Таблица (Table)** — как лист Excel со структурированными данными
- **Строка (Row/Record)** — одна запись (например, один клиент)
- **Столбец (Column/Field)** — атрибут записи (имя, возраст, город)
- **Первичный ключ (Primary Key)** — уникальный идентификатор строки (id)

### 📝 Базовый синтаксис SQL

**Структура SQL запроса:**
```sql
SELECT столбцы          -- ЧТО выбираем
FROM таблица           -- ОТКУДА берем
WHERE условия          -- КАКИЕ условия
GROUP BY группировка   -- КАК группируем  
HAVING условия_групп   -- УСЛОВИЯ для групп
ORDER BY сортировка    -- КАК сортируем
LIMIT количество;      -- СКОЛЬКО записей
```

**Правила синтаксиса:**
- SQL **не чувствителен к регистру**: `SELECT` = `select` = `Select`
- **Точка с запятой** `;` завершает запрос
- **Одинарные кавычки** для текстовых значений: `'Москва'`
- **Комментарии**: `-- это комментарий` или `/* многострочный */`

## 📊 SELECT — основа всех запросов

### 🔍 Простые SELECT запросы

**Выбрать все данные из таблицы:**
```sql
-- Показать всех клиентов
SELECT * FROM customers;

-- Звездочка (*) означает "все столбцы"
```

**Выбрать конкретные столбцы:**
```sql
-- Показать только имена и города клиентов
SELECT name, city FROM customers;

-- Порядок столбцов в результате = порядок в SELECT
```

**Переименование столбцов (алиасы):**
```sql
-- Даем понятные названия столбцам
SELECT 
    name AS имя_клиента,
    age AS возраст,
    city AS город_проживания
FROM customers;

-- AS можно опустить: name имя_клиента
```

### 🧮 Вычисляемые поля

**Математические операции:**
```sql
-- Таблица заказов с ценой и количеством
SELECT 
    order_id,
    product_name,
    price,
    quantity,
    price * quantity AS total_amount,    -- Общая сумма
    price * quantity * 0.2 AS vat_amount -- НДС 20%
FROM orders;
```

**Работа с текстом:**
```sql
-- Объединение строк
SELECT 
    first_name,
    last_name,
    CONCAT(first_name, ' ', last_name) AS full_name,
    UPPER(city) AS city_uppercase,
    LENGTH(email) AS email_length
FROM customers;
```

**Работа с датами:**
```sql
-- Извлечение компонентов даты
SELECT 
    order_date,
    YEAR(order_date) AS год,
    MONTH(order_date) AS месяц,
    DAY(order_date) AS день,
    DAYNAME(order_date) AS день_недели,
    DATEDIFF(CURRENT_DATE, order_date) AS дней_назад
FROM orders;
```

## 🔍 WHERE — фильтрация данных

### ⚖️ Основные операторы сравнения

```sql
-- Равенство
SELECT * FROM customers WHERE city = 'Москва';

-- Неравенство  
SELECT * FROM customers WHERE age != 25;
SELECT * FROM customers WHERE age <> 25;  -- альтернативный синтаксис

-- Численные сравнения
SELECT * FROM orders WHERE amount > 1000;
SELECT * FROM orders WHERE amount <= 500;
SELECT * FROM customers WHERE age BETWEEN 25 AND 35;
```

### 🔤 Работа с текстом

```sql
-- Точное совпадение
SELECT * FROM customers WHERE name = 'Иван';

-- Поиск по шаблону (LIKE)
SELECT * FROM customers WHERE name LIKE 'И%';      -- Начинается с "И"
SELECT * FROM customers WHERE name LIKE '%ов';     -- Заканчивается на "ов"  
SELECT * FROM customers WHERE email LIKE '%@gmail.com'; -- Gmail адреса

-- Регистронезависимый поиск
SELECT * FROM products WHERE LOWER(name) LIKE '%телефон%';
```

### 📅 Фильтрация по датам

```sql
-- Конкретная дата
SELECT * FROM orders WHERE order_date = '2024-01-15';

-- Диапазон дат
SELECT * FROM orders 
WHERE order_date BETWEEN '2024-01-01' AND '2024-12-31';

-- Относительные даты
SELECT * FROM orders 
WHERE order_date >= DATE_SUB(CURRENT_DATE, INTERVAL 30 DAY);  -- За последние 30 дней

-- Извлечение компонентов
SELECT * FROM orders WHERE YEAR(order_date) = 2024;
SELECT * FROM orders WHERE MONTH(order_date) = 3;           -- Март
SELECT * FROM orders WHERE DAYNAME(order_date) = 'Monday';  -- Понедельники
```

### 🔗 Логические операторы

```sql
-- AND (И) - все условия должны выполняться
SELECT * FROM customers 
WHERE city = 'Москва' AND age > 30;

-- OR (ИЛИ) - хотя бы одно условие
SELECT * FROM customers 
WHERE city = 'Москва' OR city = 'СПб';

-- NOT (НЕ) - исключение  
SELECT * FROM customers 
WHERE NOT city = 'Москва';

-- Комбинирование с скобками
SELECT * FROM orders
WHERE (city = 'Москва' OR city = 'СПб') 
  AND amount > 1000 
  AND order_date >= '2024-01-01';
```

### 📋 Проверка множественных значений

```sql
-- IN - значение входит в список
SELECT * FROM customers 
WHERE city IN ('Москва', 'СПб', 'Казань');

-- NOT IN - значение НЕ входит в список  
SELECT * FROM customers
WHERE status NOT IN ('Заблокирован', 'Удален');

-- NULL значения
SELECT * FROM customers WHERE phone IS NULL;       -- Нет телефона
SELECT * FROM customers WHERE phone IS NOT NULL;   -- Есть телефон
```

## 📈 ORDER BY — сортировка результатов

### 🔢 Простая сортировка

```sql
-- По возрастанию (по умолчанию)
SELECT name, age FROM customers ORDER BY age;
SELECT name, age FROM customers ORDER BY age ASC;  -- явно указываем

-- По убыванию
SELECT name, age FROM customers ORDER BY age DESC;

-- По текстовому полю
SELECT * FROM products ORDER BY name;              -- А-Я
SELECT * FROM products ORDER BY name DESC;         -- Я-А
```

### 🔢 Сортировка по нескольким полям

```sql
-- Сначала по городу, потом по возрасту
SELECT name, city, age 
FROM customers 
ORDER BY city, age;

-- Разные направления сортировки
SELECT name, city, age 
FROM customers 
ORDER BY city ASC, age DESC;  -- Город А-Я, возраст убывание

-- Сортировка по вычисляемому полю
SELECT 
    name, 
    price, 
    quantity,
    price * quantity AS total
FROM orders
ORDER BY total DESC;  -- По убыванию общей суммы
```

### 📊 Практические примеры сортировки

```sql
-- Топ-10 самых дорогих заказов
SELECT customer_name, order_amount 
FROM orders 
ORDER BY order_amount DESC 
LIMIT 10;

-- Клиенты по алфавиту с номерами телефонов
SELECT name, phone 
FROM customers 
WHERE phone IS NOT NULL
ORDER BY name;

-- Продукты по популярности (количество заказов)
SELECT 
    product_name,
    COUNT(*) as orders_count
FROM order_items 
GROUP BY product_name
ORDER BY orders_count DESC;
```

## 🧮 Агрегатные функции

### 📊 Основные агрегатные функции

**COUNT — подсчет количества:**
```sql
-- Общее количество клиентов
SELECT COUNT(*) FROM customers;

-- Количество клиентов с телефонами (исключает NULL)
SELECT COUNT(phone) FROM customers;

-- Количество уникальных городов
SELECT COUNT(DISTINCT city) FROM customers;
```

**SUM — сумма значений:**
```sql
-- Общая сумма всех заказов
SELECT SUM(amount) AS total_revenue FROM orders;

-- Сумма заказов за текущий год
SELECT SUM(amount) AS revenue_2024
FROM orders 
WHERE YEAR(order_date) = 2024;
```

**AVG — среднее значение:**
```sql
-- Средний возраст клиентов
SELECT AVG(age) AS average_age FROM customers;

-- Средняя сумма заказа
SELECT AVG(amount) AS avg_order_value FROM orders;

-- Средняя сумма с округлением
SELECT ROUND(AVG(amount), 2) AS avg_order_value FROM orders;
```

**MIN и MAX — минимум и максимум:**
```sql
-- Самый молодой и старший клиент
SELECT 
    MIN(age) AS youngest,
    MAX(age) AS oldest 
FROM customers;

-- Диапазон сумм заказов
SELECT 
    MIN(amount) AS min_order,
    MAX(amount) AS max_order,
    MAX(amount) - MIN(amount) AS range_orders
FROM orders;
```

### 📊 Комбинирование агрегатных функций

```sql
-- Полная статистика по заказам
SELECT 
    COUNT(*) AS total_orders,
    COUNT(DISTINCT customer_id) AS unique_customers,
    SUM(amount) AS total_revenue,
    AVG(amount) AS avg_order_value,
    MIN(amount) AS min_order,
    MAX(amount) AS max_order,
    STDDEV(amount) AS std_deviation
FROM orders;
```

## 👥 GROUP BY — группировка данных

### 🏷️ Основы группировки

**Группировка по одному полю:**
```sql
-- Количество клиентов по городам
SELECT 
    city,
    COUNT(*) AS customers_count
FROM customers 
GROUP BY city;

-- Общая выручка по месяцам
SELECT 
    DATE_FORMAT(order_date, '%Y-%m') AS month,
    SUM(amount) AS monthly_revenue
FROM orders
GROUP BY month;
```

**Группировка по нескольким полям:**
```sql
-- Статистика по городам и статусам клиентов
SELECT 
    city,
    status,
    COUNT(*) AS count,
    AVG(age) AS avg_age
FROM customers
GROUP BY city, status;
```

### 📈 Практические примеры группировки

**Анализ продаж по категориям:**
```sql
SELECT 
    category,
    COUNT(*) AS products_count,
    SUM(price * quantity) AS total_sales,
    AVG(price) AS avg_price,
    MIN(price) AS min_price,
    MAX(price) AS max_price
FROM products p
JOIN order_items oi ON p.id = oi.product_id
GROUP BY category
ORDER BY total_sales DESC;
```

**Анализ клиентской активности:**
```sql
-- Сколько заказов делает каждый клиент
SELECT 
    customer_id,
    COUNT(*) AS orders_count,
    SUM(amount) AS total_spent,
    AVG(amount) AS avg_order_value,
    MIN(order_date) AS first_order,
    MAX(order_date) AS last_order
FROM orders
GROUP BY customer_id
ORDER BY total_spent DESC;
```

**Временной анализ:**
```sql
-- Активность по дням недели
SELECT 
    DAYNAME(order_date) AS day_of_week,
    COUNT(*) AS orders_count,
    SUM(amount) AS revenue,
    AVG(amount) AS avg_order
FROM orders
GROUP BY DAYNAME(order_date), DAYOFWEEK(order_date)
ORDER BY DAYOFWEEK(order_date);
```

## 🔍 HAVING — условия для групп

### ⚖️ Разница между WHERE и HAVING

```sql
-- WHERE фильтрует строки ДО группировки
-- HAVING фильтрует группы ПОСЛЕ группировки

-- Неправильно - агрегатные функции нельзя использовать в WHERE
-- SELECT city, COUNT(*) FROM customers WHERE COUNT(*) > 10 GROUP BY city;

-- Правильно - используем HAVING для фильтрации групп
SELECT 
    city, 
    COUNT(*) AS customers_count
FROM customers 
GROUP BY city
HAVING COUNT(*) > 10;  -- Только города с >10 клиентами
```

### 📊 Практические примеры HAVING

**Активные клиенты:**
```sql
-- Клиенты с более чем 5 заказами и суммой >50000
SELECT 
    customer_id,
    COUNT(*) AS orders_count,
    SUM(amount) AS total_spent
FROM orders
GROUP BY customer_id
HAVING COUNT(*) > 5 AND SUM(amount) > 50000
ORDER BY total_spent DESC;
```

**Популярные товары:**
```sql
-- Товары, которые заказывали более 100 раз
SELECT 
    product_name,
    COUNT(*) AS order_frequency,
    SUM(quantity) AS total_sold
FROM order_items
GROUP BY product_name
HAVING COUNT(*) > 100
ORDER BY order_frequency DESC;
```

**Анализ сезонности:**
```sql
-- Месяцы с выручкой выше среднего
SELECT 
    MONTH(order_date) AS month,
    SUM(amount) AS monthly_revenue
FROM orders
WHERE YEAR(order_date) = 2024
GROUP BY MONTH(order_date)
HAVING SUM(amount) > (
    SELECT AVG(monthly_total) FROM (
        SELECT SUM(amount) AS monthly_total
        FROM orders 
        WHERE YEAR(order_date) = 2024
        GROUP BY MONTH(order_date)
    ) AS subquery
);
```

## 🔗 JOIN — объединение таблиц

### 📊 Основы связей между таблицами

**Пример структуры данных:**
```sql
-- Таблица клиентов
customers: id, name, city, email

-- Таблица заказов  
orders: id, customer_id, amount, order_date

-- Связь: orders.customer_id = customers.id
```

### 🤝 INNER JOIN — внутреннее соединение

```sql
-- Заказы с информацией о клиентах
SELECT 
    c.name AS customer_name,
    c.city,
    o.amount,
    o.order_date
FROM customers c
INNER JOIN orders o ON c.id = o.customer_id;

-- Показывает только клиентов, у которых ЕСТЬ заказы
```

### ⬅️ LEFT JOIN — левое соединение

```sql
-- ВСЕ клиенты + их заказы (если есть)
SELECT 
    c.name AS customer_name,
    c.city,
    o.amount,
    o.order_date
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id;

-- Показывает ВСЕХ клиентов, даже без заказов (amount = NULL)
```

### ➡️ RIGHT JOIN — правое соединение

```sql
-- ВСЕ заказы + информация о клиентах
SELECT 
    c.name AS customer_name,
    o.amount,
    o.order_date
FROM customers c
RIGHT JOIN orders o ON c.id = o.customer_id;

-- Редко используется, можно заменить на LEFT JOIN с изменением порядка таблиц
```

### 📊 Практические примеры JOIN

**Детальный анализ заказов:**
```sql
-- Заказы с информацией о клиентах и товарах
SELECT 
    c.name AS customer_name,
    c.city,
    p.product_name,
    p.category,
    oi.quantity,
    oi.price,
    oi.quantity * oi.price AS item_total,
    o.order_date
FROM customers c
INNER JOIN orders o ON c.id = o.customer_id
INNER JOIN order_items oi ON o.id = oi.order_id
INNER JOIN products p ON oi.product_id = p.id
WHERE o.order_date >= '2024-01-01'
ORDER BY o.order_date DESC;
```

**Клиенты без заказов:**
```sql
-- Найти потенциальных клиентов для маркетинга
SELECT 
    c.name,
    c.email,
    c.registration_date
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id
WHERE o.customer_id IS NULL  -- Нет ни одного заказа
ORDER BY c.registration_date DESC;
```

**Топ клиентов по городам:**
```sql
-- Лучшие клиенты в каждом городе
SELECT 
    c.city,
    c.name,
    SUM(o.amount) AS total_spent,
    COUNT(o.id) AS orders_count
FROM customers c
INNER JOIN orders o ON c.id = o.customer_id
GROUP BY c.city, c.id, c.name
ORDER BY c.city, total_spent DESC;
```

## 🔄 Подзапросы (Subqueries)

### 📊 Скалярные подзапросы

```sql
-- Клиенты с суммой заказов выше среднего
SELECT 
    name,
    (SELECT SUM(amount) FROM orders WHERE customer_id = c.id) AS total_spent
FROM customers c
WHERE (
    SELECT SUM(amount) FROM orders WHERE customer_id = c.id
) > (
    SELECT AVG(total_per_customer) FROM (
        SELECT SUM(amount) AS total_per_customer
        FROM orders 
        GROUP BY customer_id
    ) AS avg_subquery
);
```

### 📋 Подзапросы с IN

```sql
-- Клиенты, которые покупали товары категории "Электроника"
SELECT name, email
FROM customers
WHERE id IN (
    SELECT DISTINCT o.customer_id
    FROM orders o
    INNER JOIN order_items oi ON o.id = oi.order_id
    INNER JOIN products p ON oi.product_id = p.id
    WHERE p.category = 'Электроника'
);
```

### 🔍 EXISTS подзапросы

```sql
-- Клиенты с заказами в текущем году (EXISTS более эффективен)
SELECT name, city
FROM customers c
WHERE EXISTS (
    SELECT 1 
    FROM orders o 
    WHERE o.customer_id = c.id 
      AND YEAR(o.order_date) = YEAR(CURRENT_DATE)
);
```

## 🔄 Интеграция SQL с Power Query

### 📊 Подключение к базе данных в Power Query

**Подключение к SQL Server:**
```
1. Power BI/Excel → Получить данные → База данных → SQL Server
2. Указать сервер и базу данных
3. Выбрать режим подключения (Import/DirectQuery)
4. Ввести SQL запрос или выбрать таблицы
```

**Пример интеграции:**
```sql
-- SQL запрос в Power Query для анализа продаж
SELECT 
    DATE_FORMAT(o.order_date, '%Y-%m') AS month,
    c.city,
    p.category,
    SUM(oi.quantity * oi.price) AS revenue,
    COUNT(DISTINCT o.customer_id) AS unique_customers,
    COUNT(o.id) AS orders_count
FROM orders o
INNER JOIN customers c ON o.customer_id = c.id
INNER JOIN order_items oi ON o.id = oi.order_id  
INNER JOIN products p ON oi.product_id = p.id
WHERE o.order_date >= DATE_SUB(CURRENT_DATE, INTERVAL 12 MONTH)
GROUP BY month, c.city, p.category
ORDER BY month, city, category;
```

### 🔧 Параметризация запросов в Power Query

**Создание параметров:**
```sql
-- В Power Query можно создать параметры для динамических запросов
SELECT *
FROM orders 
WHERE order_date >= @StartDate 
  AND order_date <= @EndDate
  AND city = @CityFilter;
```

**Функции M для SQL:**
```
// Power Query M код для динамического SQL
let
    StartDate = Date.ToText(#date(2024, 1, 1), "yyyy-MM-dd"),
    EndDate = Date.ToText(Date.From(DateTime.LocalNow()), "yyyy-MM-dd"),
    
    SqlQuery = "
    SELECT 
        customer_id,
        SUM(amount) as total_spent
    FROM orders 
    WHERE order_date BETWEEN '" & StartDate & "' AND '" & EndDate & "'
    GROUP BY customer_id
    ORDER BY total_spent DESC
    ",
    
    Source = Sql.Database("server", "database", [Query=SqlQuery])
in
    Source
```

## 🏢 Бизнес-применения SQL

### 📈 Аналитические отчеты

**Отчет по продажам:**
```sql
-- Ежемесячный отчет по продажам с трендами
SELECT 
    DATE_FORMAT(order_date, '%Y-%m') AS month,
    COUNT(*) AS orders_count,
    COUNT(DISTINCT customer_id) AS unique_customers,
    SUM(amount) AS total_revenue,
    AVG(amount) AS avg_order_value,
    SUM(amount) / COUNT(DISTINCT customer_id) AS revenue_per_customer,
    
    -- Сравнение с предыдущим месяцем
    LAG(SUM(amount)) OVER (ORDER BY DATE_FORMAT(order_date, '%Y-%m')) AS prev_month_revenue,
    
    -- Рост в процентах
    ROUND(
        (SUM(amount) - LAG(SUM(amount)) OVER (ORDER BY DATE_FORMAT(order_date, '%Y-%m'))) * 100.0 / 
        LAG(SUM(amount)) OVER (ORDER BY DATE_FORMAT(order_date, '%Y-%m')), 2
    ) AS growth_percent
    
FROM orders
WHERE order_date >= DATE_SUB(CURRENT_DATE, INTERVAL 12 MONTH)
GROUP BY DATE_FORMAT(order_date, '%Y-%m')
ORDER BY month;
```

**Сегментация клиентов:**
```sql
-- RFM анализ (Recency, Frequency, Monetary)
SELECT 
    customer_id,
    
    -- Recency: дни с последнего заказа
    DATEDIFF(CURRENT_DATE, MAX(order_date)) AS days_since_last_order,
    
    -- Frequency: количество заказов
    COUNT(*) AS order_frequency,
    
    -- Monetary: общая сумма покупок
    SUM(amount) AS total_spent,
    
    -- Сегментация
    CASE 
        WHEN DATEDIFF(CURRENT_DATE, MAX(order_date)) <= 30 AND COUNT(*) >= 5 AND SUM(amount) >= 50000 
        THEN 'Чемпионы'
        WHEN DATEDIFF(CURRENT_DATE, MAX(order_date)) <= 60 AND COUNT(*) >= 3 AND SUM(amount) >= 20000 
        THEN 'Лояльные'
        WHEN DATEDIFF(CURRENT_DATE, MAX(order_date)) <= 90 AND COUNT(*) >= 2 
        THEN 'Потенциальные'
        WHEN DATEDIFF(CURRENT_DATE, MAX(order_date)) > 180 
        THEN 'Спящие'
        ELSE 'Новички'
    END AS customer_segment
    
FROM orders
GROUP BY customer_id
ORDER BY total_spent DESC;
```

### 📊 KPI дашборды

**Ключевые метрики для дашборда:**
```sql
-- Основные KPI за последние 30 дней
SELECT 
    'Основные метрики' AS category,
    COUNT(DISTINCT DATE(order_date)) AS active_days,
    COUNT(*) AS total_orders,
    COUNT(DISTINCT customer_id) AS unique_customers,
    SUM(amount) AS total_revenue,
    AVG(amount) AS avg_order_value,
    SUM(amount) / COUNT(DISTINCT customer_id) AS revenue_per_customer,
    COUNT(*) / COUNT(DISTINCT DATE(order_date)) AS avg_orders_per_day
FROM orders
WHERE order_date >= DATE_SUB(CURRENT_DATE, INTERVAL 30 DAY)

UNION ALL

-- Сравнение с предыдущим периодом
SELECT 
    'Предыдущий период' AS category,
    COUNT(DISTINCT DATE(order_date)) AS active_days,
    COUNT(*) AS total_orders,
    COUNT(DISTINCT customer_id) AS unique_customers,
    SUM(amount) AS total_revenue,
    AVG(amount) AS avg_order_value,
    SUM(amount) / COUNT(DISTINCT customer_id) AS revenue_per_customer,
    COUNT(*) / COUNT(DISTINCT DATE(order_date)) AS avg_orders_per_day
FROM orders
WHERE order_date >= DATE_SUB(CURRENT_DATE, INTERVAL 60 DAY)
  AND order_date < DATE_SUB(CURRENT_DATE, INTERVAL 30 DAY);
```

### 🔍 Поиск аномалий

**Выявление необычной активности:**
```sql
-- Дни с аномально высокими/низкими продажами
WITH daily_stats AS (
    SELECT 
        DATE(order_date) AS order_day,
        COUNT(*) AS orders_count,
        SUM(amount) AS daily_revenue
    FROM orders
    WHERE order_date >= DATE_SUB(CURRENT_DATE, INTERVAL 90 DAY)
    GROUP BY DATE(order_date)
),
stats_summary AS (
    SELECT 
        AVG(daily_revenue) AS avg_revenue,
        STDDEV(daily_revenue) AS std_revenue
    FROM daily_stats
)
SELECT 
    ds.order_day,
    ds.orders_count,
    ds.daily_revenue,
    ROUND(ds.daily_revenue - ss.avg_revenue, 2) AS deviation_from_avg,
    CASE 
        WHEN ds.daily_revenue > ss.avg_revenue + 2 * ss.std_revenue THEN 'Аномально высокие'
        WHEN ds.daily_revenue < ss.avg_revenue - 2 * ss.std_revenue THEN 'Аномально низкие'
        ELSE 'Нормальные'
    END AS anomaly_type
FROM daily_stats ds
CROSS JOIN stats_summary ss
WHERE ds.daily_revenue > ss.avg_revenue + 2 * ss.std_revenue
   OR ds.daily_revenue < ss.avg_revenue - 2 * ss.std_revenue
ORDER BY ds.order_day DESC;
```

## ⚡ Основы оптимизации запросов

### 📊 Принципы эффективных запросов

**Использование индексов:**
```sql
-- Создание индекса для ускорения поиска
CREATE INDEX idx_orders_date ON orders(order_date);
CREATE INDEX idx_orders_customer ON orders(customer_id);
CREATE INDEX idx_orders_date_customer ON orders(order_date, customer_id);

-- Индексы ускоряют WHERE, JOIN, ORDER BY
```

**Эффективная фильтрация:**
```sql
-- ✅ Хорошо - фильтрация по индексированному полю
SELECT * FROM orders WHERE customer_id = 123;

-- ❌ Плохо - функция в WHERE замедляет запрос  
SELECT * FROM orders WHERE YEAR(order_date) = 2024;

-- ✅ Лучше - используем диапазон дат
SELECT * FROM orders 
WHERE order_date >= '2024-01-01' AND order_date < '2025-01-01';
```

**Оптимизация JOIN:**
```sql
-- ✅ Хорошо - JOIN по индексированным полям
SELECT c.name, SUM(o.amount)
FROM customers c
INNER JOIN orders o ON c.id = o.customer_id  -- id обычно индексированы
GROUP BY c.id, c.name;

-- ❌ Избегайте JOIN по вычисляемым полям
```

### 📈 EXPLAIN - анализ плана выполнения

```sql
-- Анализ производительности запроса
EXPLAIN SELECT 
    c.name,
    COUNT(o.id) as orders_count,
    SUM(o.amount) as total_spent
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id
WHERE c.city = 'Москва'
GROUP BY c.id, c.name
ORDER BY total_spent DESC;

-- EXPLAIN показывает как СУБД выполняет запрос
-- Ищите: table scans, missing indexes, expensive operations
```

### 🔧 Практические советы по оптимизации

**Ограничение результатов:**
```sql
-- Используйте LIMIT для больших результатов
SELECT * FROM orders ORDER BY order_date DESC LIMIT 100;

-- Пагинация
SELECT * FROM orders ORDER BY id LIMIT 50 OFFSET 100;  -- Страница 3 по 50 записей
```

**Оптимизация агрегатных запросов:**
```sql
-- ✅ Группировка по индексированным полям быстрее
SELECT customer_id, COUNT(*), SUM(amount)
FROM orders 
WHERE order_date >= '2024-01-01'
GROUP BY customer_id;  -- customer_id обычно индексирован

-- ✅ Предварительная фильтрация уменьшает объем данных для группировки
```

**Использование подходящих типов данных:**
```sql
-- ✅ Правильные типы данных экономят место и ускоряют запросы
customer_id INT NOT NULL,           -- Вместо VARCHAR
order_date DATE,                    -- Вместо VARCHAR
amount DECIMAL(10,2),              -- Вместо FLOAT для денег
status ENUM('new','paid','shipped') -- Вместо VARCHAR для статусов
```

## 🛠 Инструкции

Теперь переходите к практическим заданиям и изучите SQL на реальных данных:

- 📝 [Перейти к практическим заданиям](practice.md)
- ✅ [Перейти к чек-листу](checklist.md)
- 📁 [Посмотреть учебные файлы](files/README.md)

---

- 🔙 [Предыдущая глава: Глава 18 - Работа с API: получение и автоматизация данных](../chapter-18/README.md)
- 🔜 [Следующая глава: Глава 20 - SQL: JOIN, подзапросы, CTE](../chapter-20/README.md)

---

- 📢 Присоединяйтесь к чату курса: https://t.me/analytics_course_chat
- 📢 Канал курса: https://t.me/analytics_course_channel