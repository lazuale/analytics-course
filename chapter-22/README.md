# ⚡ Глава 22: Оптимизация SQL-запросов: индексы, EXPLAIN

## 🎯 Цели обучения

После изучения этой главы вы сможете:

- ⚡ **Анализировать производительность SQL-запросов** с помощью EXPLAIN PLAN
- 🔍 **Выявлять узкие места** в медленных запросах и оптимизировать их
- 📊 **Создавать эффективные индексы** для различных типов запросов
- 🎯 **Применять стратегии оптимизации** запросов в реальных проектах
- 🔄 **Интегрировать принципы оптимизации SQL с DAX** в Power BI
- 📈 **Мониторить производительность** и поддерживать высокую скорость работы БД

---

## 📚 Теория

### ⚡ Основы оптимизации SQL-запросов

#### 🎭 Метафора: Городское движение
Представьте, что SQL-запрос — это маршрут по городу, а база данных — это транспортная сеть:

- **Таблицы** — это районы города, которые нужно посетить
- **Индексы** — это скоростные магистрали и указатели
- **EXPLAIN PLAN** — это GPS-навигатор, показывающий лучший маршрут
- **Оптимизация запросов** — это выбор самого быстрого пути без пробок
- **Статистика таблиц** — это информация о загруженности дорог

#### 🚗 Как работает оптимизатор запросов

Оптимизатор SQL — это как умный GPS-навигатор:

1. **Анализ запроса** — изучает, куда нужно добраться
2. **Оценка альтернатив** — рассматривает разные маршруты
3. **Расчет стоимости** — оценивает время каждого пути
4. **Выбор плана** — выбирает самый быстрый маршрут
5. **Выполнение** — следует по выбранному плану

```sql
-- Простой запрос может выполняться множеством способов
SELECT p.product_name, SUM(s.quantity) as total_sold
FROM products p
JOIN sales s ON p.product_id = s.product_id
WHERE p.category = 'Electronics'
  AND s.sale_date >= '2024-01-01'
GROUP BY p.product_name;

-- Оптимизатор выберет один из вариантов:
-- 1. Сначала фильтровать products, потом JOIN
-- 2. Сначала фильтровать sales, потом JOIN
-- 3. Сделать JOIN, потом фильтровать
```

---

### 🔍 EXPLAIN PLAN: GPS для SQL-запросов

#### 🎭 Метафора: Детальная карта маршрута
EXPLAIN PLAN — это как детальная карта от GPS, которая показывает:
- Какими дорогами вы поедете (какие таблицы будут использованы)
- В каком порядке (последовательность операций)
- Сколько времени займет каждый участок (стоимость операций)
- Есть ли пробки на пути (узкие места производительности)

#### 📊 Чтение плана выполнения

**1️⃣ Основные операции в плане выполнения:**

```sql
-- Получение плана выполнения
EXPLAIN QUERY PLAN
SELECT c.customer_name, COUNT(o.order_id) as order_count
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE c.city = 'Москва'
GROUP BY c.customer_id, c.customer_name
ORDER BY order_count DESC;
```

**Типичный вывод EXPLAIN:**
```
SCAN customers USING INDEX idx_customers_city (city=?)
SEARCH orders USING INDEX idx_orders_customer_id (customer_id=?)
USE TEMP B-TREE FOR GROUP BY
USE TEMP B-TREE FOR ORDER BY
```

**2️⃣ Ключевые термины в планах выполнения:**

| Операция | Описание | Аналогия |
|----------|----------|----------|
| **SCAN** | Полный просмотр таблицы | Объезд всего района |
| **SEARCH** | Поиск с индексом | Движение по скоростной дороге |
| **NESTED LOOP** | Вложенные циклы | Посещение каждого дома на каждой улице |
| **HASH JOIN** | Соединение через хэш-таблицу | Умный алгоритм поиска пересечений |
| **SORT** | Сортировка | Выстраивание в очередь |
| **GROUP BY** | Группировка | Сбор по категориям |

**3️⃣ Анализ стоимости операций:**

```sql
-- В PostgreSQL или SQL Server можно увидеть детальную стоимость
EXPLAIN (ANALYZE, BUFFERS)
SELECT p.product_name, AVG(r.rating) as avg_rating
FROM products p
JOIN reviews r ON p.product_id = r.product_id
WHERE p.price BETWEEN 1000 AND 5000
GROUP BY p.product_id, p.product_name
HAVING COUNT(r.review_id) >= 10;

/*
Пример вывода:
HashAggregate (cost=15234.56..15456.78 rows=1000 width=32)
  -> Hash Join (cost=1234.56..12345.67 rows=5000 width=28)
    Hash Cond: (p.product_id = r.product_id)
    -> Seq Scan on products p (cost=0.00..456.78 rows=2000 width=20)
      Filter: (price >= 1000 AND price <= 5000)
    -> Hash (cost=789.01..789.01 rows=10000 width=12)
      -> Seq Scan on reviews r (cost=0.00..789.01 rows=10000 width=12)
*/
```

---

### 📊 Стратегии индексации

#### 🎭 Метафора: Библиотечная система
Индексы в базе данных — это как система каталогов в огромной библиотеке:

- **Алфавитный каталог** (B-Tree индекс) — быстро найти по фамилии автора
- **Тематический каталог** (индекс по жанру) — найти все книги по теме
- **Хронологический каталог** (индекс по дате) — найти книги определенного года
- **Составной каталог** (составной индекс) — найти по автору И году одновременно

#### 🌳 B-Tree индексы: Основа быстрого поиска

**1️⃣ Как работает B-Tree индекс:**

```sql
-- Создание простого B-Tree индекса
CREATE INDEX idx_products_name ON products(product_name);

-- Этот индекс ускоряет такие запросы:
SELECT * FROM products WHERE product_name = 'iPhone 15';
SELECT * FROM products WHERE product_name LIKE 'iPhone%';
SELECT * FROM products ORDER BY product_name;
```

**Внутренняя структура B-Tree:**
```
                   [M-T]
                 /       \
            [A-F]           [U-Z]
           /     \         /     \
       [A-C]   [G-L]   [U-W]   [X-Z]
       / | \   / | \   / | \   / | \
     A B C   G H L   U V W   X Y Z
```

**2️⃣ Составные индексы:**

```sql
-- Составной индекс по нескольким столбцам
CREATE INDEX idx_orders_customer_date ON orders(customer_id, order_date);

-- Этот индекс эффективен для:
-- ✅ WHERE customer_id = 123
-- ✅ WHERE customer_id = 123 AND order_date = '2024-01-01'
-- ✅ WHERE customer_id = 123 AND order_date >= '2024-01-01'

-- Но НЕ эффективен для:
-- ❌ WHERE order_date = '2024-01-01' (без customer_id)
```

**Правило левой границы:** Составной индекс можно использовать только если запрос включает левые столбцы индекса.

**3️⃣ Покрывающие индексы:**

```sql
-- Покрывающий индекс включает все нужные столбцы
CREATE INDEX idx_products_covering 
ON products(category, price, product_name, description);

-- Для этого запроса данные берутся только из индекса
SELECT product_name, price 
FROM products 
WHERE category = 'Electronics' 
  AND price BETWEEN 500 AND 1500;
```

#### 📈 Индексы для разных типов запросов

**1️⃣ Индексы для WHERE условий:**

```sql
-- Для точного поиска
CREATE INDEX idx_customers_email ON customers(email);
SELECT * FROM customers WHERE email = 'john@example.com';

-- Для диапазонов
CREATE INDEX idx_products_price ON products(price);
SELECT * FROM products WHERE price BETWEEN 1000 AND 2000;

-- Для поиска по началу строки
CREATE INDEX idx_products_name ON products(product_name);
SELECT * FROM products WHERE product_name LIKE 'iPhone%';
```

**2️⃣ Индексы для JOIN операций:**

```sql
-- Индексы на внешние ключи обязательны!
CREATE INDEX idx_orders_customer_id ON orders(customer_id);
CREATE INDEX idx_order_items_order_id ON order_items(order_id);
CREATE INDEX idx_order_items_product_id ON order_items(product_id);

-- Ускоряют JOIN операции
SELECT c.customer_name, COUNT(o.order_id)
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.customer_name;
```

**3️⃣ Индексы для ORDER BY и GROUP BY:**

```sql
-- Для сортировки
CREATE INDEX idx_products_name_price ON products(product_name, price);
SELECT * FROM products ORDER BY product_name, price;

-- Для группировки
CREATE INDEX idx_sales_date_product ON sales(sale_date, product_id);
SELECT product_id, SUM(amount)
FROM sales 
WHERE sale_date >= '2024-01-01'
GROUP BY product_id;
```

#### ⚠️ Когда индексы могут навредить

**1️⃣ Слишком много индексов:**
- Замедляют INSERT, UPDATE, DELETE операции
- Занимают дополнительное место на диске
- Усложняют выбор оптимизатору

**2️⃣ Неиспользуемые индексы:**
```sql
-- Мониторинг использования индексов (PostgreSQL)
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan,           -- количество использований
    idx_tup_read,       -- прочитано строк
    idx_tup_fetch       -- возвращено строк
FROM pg_stat_user_indexes
WHERE idx_scan = 0      -- неиспользуемые индексы
ORDER BY schemaname, tablename;
```

**3️⃣ Неправильные индексы:**
```sql
-- ПЛОХО: индекс на столбец с малым количеством уникальных значений
CREATE INDEX bad_idx_gender ON users(gender); -- только M/F

-- ПЛОХО: функциональные операции в WHERE без функционального индекса
SELECT * FROM customers WHERE UPPER(email) = 'JOHN@EXAMPLE.COM';
-- Лучше создать: CREATE INDEX idx_email_upper ON customers(UPPER(email));
```

---

### 🎯 Методы оптимизации запросов

#### 🎭 Метафора: Настройка спортивного автомобиля
Оптимизация SQL-запросов — это как тюнинг гоночного автомобиля:
- **Анализ текущей производительности** — замеры на трассе
- **Выявление узких мест** — поиск слабых компонентов
- **Точечная оптимизация** — замена конкретных деталей
- **Тестирование улучшений** — новые замеры производительности

#### 🔧 Оптимизация WHERE условий

**1️⃣ Селективность фильтров:**

```sql
-- ПЛОХО: неселективный фильтр сначала
SELECT * FROM customers 
WHERE country = 'Russia'           -- 80% записей
  AND premium_status = 'VIP'       -- 1% записей
  AND registration_date >= '2024-01-01';

-- ХОРОШО: селективные фильтры сначала  
SELECT * FROM customers 
WHERE premium_status = 'VIP'       -- 1% записей (самый селективный)
  AND registration_date >= '2024-01-01'  -- 10% записей
  AND country = 'Russia';          -- 80% записей
```

**2️⃣ Избегание функций в WHERE:**

```sql
-- ПЛОХО: функция в WHERE блокирует использование индекса
SELECT * FROM orders 
WHERE YEAR(order_date) = 2024;

-- ХОРОШО: используем диапазон дат
SELECT * FROM orders 
WHERE order_date >= '2024-01-01' 
  AND order_date < '2025-01-01';

-- ПЛОХО: вычисления в WHERE
SELECT * FROM products 
WHERE price * 1.2 > 1000;

-- ХОРОШО: вычисления в правой части
SELECT * FROM products 
WHERE price > 1000 / 1.2;
```

**3️⃣ Оптимизация LIKE операций:**

```sql
-- ХОРОШО: поиск по началу строки использует индекс
SELECT * FROM customers 
WHERE customer_name LIKE 'Петр%';

-- ПЛОХО: поиск с % в начале не использует индекс
SELECT * FROM customers 
WHERE customer_name LIKE '%Петр%';

-- Решение: полнотекстовый поиск или специальные индексы
CREATE INDEX idx_customers_name_gin 
ON customers USING gin(to_tsvector('russian', customer_name));
```

#### 🔄 Оптимизация JOIN операций

**1️⃣ Порядок JOIN:**

```sql
-- Оптимизатор обычно сам выбирает порядок, но можно помочь:

-- Начинаем с самой маленькой таблицы
SELECT p.product_name, c.category_name, SUM(s.quantity)
FROM categories c                    -- 10 записей (начинаем с малой)
JOIN products p ON c.category_id = p.category_id     -- 1,000 записей  
JOIN sales s ON p.product_id = s.product_id         -- 1,000,000 записей
WHERE c.category_name = 'Electronics'
GROUP BY p.product_id, p.product_name, c.category_name;
```

**2️⃣ Типы JOIN алгоритмов:**

```sql
-- NESTED LOOP JOIN - хорош для маленьких таблиц
-- HASH JOIN - хорош для больших таблиц без индексов
-- MERGE JOIN - хорош для отсортированных данных

-- Можно принудительно указать тип JOIN (в некоторых СУБД)
SELECT /*+ USE_HASH(c, p) */ 
       c.customer_name, 
       COUNT(p.purchase_id)
FROM customers c
JOIN purchases p ON c.customer_id = p.customer_id;
```

**3️⃣ Оптимизация подзапросов:**

```sql
-- ПЛОХО: коррелированный подзапрос
SELECT c.customer_name
FROM customers c
WHERE (SELECT COUNT(*) 
       FROM orders o 
       WHERE o.customer_id = c.customer_id) > 5;

-- ХОРОШО: JOIN с агрегацией
SELECT c.customer_name
FROM customers c
JOIN (
    SELECT customer_id, COUNT(*) as order_count
    FROM orders
    GROUP BY customer_id
    HAVING COUNT(*) > 5
) o ON c.customer_id = o.customer_id;

-- ЕЩЕ ЛУЧШЕ: использование EXISTS
SELECT c.customer_name
FROM customers c
WHERE EXISTS (
    SELECT 1 
    FROM orders o 
    WHERE o.customer_id = c.customer_id
    GROUP BY o.customer_id
    HAVING COUNT(*) > 5
);
```

#### 📊 Оптимизация GROUP BY и ORDER BY

**1️⃣ Эффективная группировка:**

```sql
-- Используйте индексы для GROUP BY
CREATE INDEX idx_sales_product_date ON sales(product_id, sale_date);

-- Такой запрос будет быстрым
SELECT product_id, DATE_TRUNC('month', sale_date), SUM(amount)
FROM sales
WHERE sale_date >= '2024-01-01'
GROUP BY product_id, DATE_TRUNC('month', sale_date);
```

**2️⃣ Эффективная сортировка:**

```sql
-- Используйте LIMIT с ORDER BY для больших результатов
SELECT customer_name, total_purchases
FROM customer_stats
ORDER BY total_purchases DESC
LIMIT 100;  -- Только топ-100, не все записи

-- Избегайте ORDER BY без LIMIT на больших данных
-- ПЛОХО для миллионов записей:
SELECT * FROM large_table ORDER BY some_column;
```

---

### 🔄 Интеграция SQL оптимизации с DAX

#### 🎭 Метафора: Двухэтажный дом
Представьте систему аналитики как двухэтажный дом:
- **Первый этаж (SQL)** — фундамент и основные помещения, где живут данные
- **Второй этаж (DAX в Power BI)** — комнаты для анализа и визуализации
- **Лестница** — это процесс передачи данных между SQL и DAX
- **Лифт** — это оптимизированные запросы, которые работают быстро

#### 📊 Оптимизация на уровне SQL для Power BI

**1️⃣ Создание оптимизированных представлений:**

```sql
-- Создаем материализованное представление для Power BI
CREATE MATERIALIZED VIEW sales_summary AS
SELECT 
    DATE_TRUNC('month', s.sale_date) as sale_month,
    p.category_id,
    c.category_name,
    p.product_id,
    p.product_name,
    SUM(s.quantity) as total_quantity,
    SUM(s.amount) as total_amount,
    COUNT(s.sale_id) as transaction_count,
    COUNT(DISTINCT s.customer_id) as unique_customers
FROM sales s
JOIN products p ON s.product_id = p.product_id
JOIN categories c ON p.category_id = c.category_id
WHERE s.sale_date >= DATE_TRUNC('year', CURRENT_DATE - INTERVAL '2 years')
GROUP BY 
    DATE_TRUNC('month', s.sale_date),
    p.category_id,
    c.category_name, 
    p.product_id,
    p.product_name;

-- Создаем индекс для быстрого доступа
CREATE INDEX idx_sales_summary_month_category 
ON sales_summary(sale_month, category_id);
```

**2️⃣ Оптимизация для DirectQuery режима:**

```sql
-- В DirectQuery каждый визуал Power BI генерирует SQL запрос
-- Нужно оптимизировать таблицы для частых паттернов

-- Создаем индексы для типичных фильтров Power BI
CREATE INDEX idx_sales_date_customer ON sales(sale_date, customer_id);
CREATE INDEX idx_products_category_price ON products(category_id, price);
CREATE INDEX idx_customers_city_segment ON customers(city, customer_segment);

-- Создаем колоночные индексы (если поддерживается)
CREATE COLUMNSTORE INDEX idx_sales_columnstore 
ON sales(sale_date, product_id, customer_id, amount, quantity);
```

#### 📈 DAX оптимизация с учетом SQL

**1️⃣ Эффективные DAX меры для оптимизированных SQL данных:**

```dax
// Используем предагрегированные данные из SQL
Total Sales = SUM(sales_summary[total_amount])

// Вместо сложных вычислений в DAX, используем подготовленные SQL данные
Monthly Growth = 
VAR CurrentMonth = [Total Sales]
VAR PrevMonth = 
    CALCULATE(
        [Total Sales],
        DATEADD(sales_summary[sale_month], -1, MONTH)
    )
RETURN
    DIVIDE(CurrentMonth - PrevMonth, PrevMonth)

// Оптимизированные фильтры, которые используют SQL индексы
Top Products by Category = 
CALCULATE(
    [Total Sales],
    TOPN(10, 
         VALUES(sales_summary[product_name]), 
         [Total Sales], 
         DESC)
)
```

**2️⃣ Избегание медленных DAX паттернов:**

```dax
// ПЛОХО: сложная логика в DAX, которая заставляет сканировать всю таблицу
Customers with High AOV = 
SUMX(
    VALUES(customers[customer_id]),
    IF(
        DIVIDE(
            SUM(RELATED(sales[amount])),
            COUNT(RELATED(sales[sale_id]))
        ) > 1000,
        1,
        0
    )
)

// ХОРОШО: предварительная обработка в SQL
High AOV Customers = SUM(customer_stats[is_high_aov])

-- Где customer_stats создается в SQL:
CREATE VIEW customer_stats AS
SELECT 
    customer_id,
    AVG(amount) as avg_order_value,
    CASE WHEN AVG(amount) > 1000 THEN 1 ELSE 0 END as is_high_aov
FROM sales
GROUP BY customer_id;
```

#### 🔧 Мониторинг производительности связки SQL-DAX

**1️⃣ Анализ SQL запросов от Power BI:**

```sql
-- Включение логирования запросов (PostgreSQL)
ALTER SYSTEM SET log_statement = 'all';
ALTER SYSTEM SET log_min_duration_statement = 1000; -- запросы > 1 сек

-- Анализ медленных запросов
SELECT 
    query,
    calls,
    total_time,
    mean_time,
    rows
FROM pg_stat_statements 
WHERE query LIKE '%sales%'
ORDER BY mean_time DESC;
```

**2️⃣ Оптимизация модели данных Power BI:**

```dax
// Создание эффективных связей на уровне модели
// Используем Integer ключи вместо текстовых

// Создание календарной таблицы для оптимизации временных расчетов
Calendar = 
ADDCOLUMNS(
    CALENDARAUTO(),
    "Year", YEAR([Date]),
    "Month", MONTH([Date]),
    "Quarter", "Q" & FORMAT(ROUNDUP(MONTH([Date])/3,0),"0"),
    "MonthYear", FORMAT([Date], "MMM YYYY")
)

// Установка правильных типов данных и форматов
// Это влияет на генерируемые SQL запросы
```

---

### 📊 Мониторинг и поддержка производительности

#### 🎭 Метафора: Медицинская диагностика
Мониторинг производительности БД — это как регулярные медицинские осмотры:
- **Профилактические проверки** — регулярный анализ медленных запросов
- **Диагностика симптомов** — выявление причин снижения производительности
- **Лечение** — применение оптимизаций и исправлений
- **Контрольные осмотры** — проверка эффективности лечения

#### 📈 Системы мониторинга

**1️⃣ Ключевые метрики производительности:**

```sql
-- Мониторинг загрузки системы
SELECT 
    'Database Size' as metric,
    pg_size_pretty(pg_database_size(current_database())) as value
UNION ALL
SELECT 
    'Active Connections' as metric,
    COUNT(*)::text as value
FROM pg_stat_activity
WHERE state = 'active'
UNION ALL
SELECT 
    'Cache Hit Ratio' as metric,
    ROUND(
        100.0 * sum(blks_hit) / nullif(sum(blks_hit) + sum(blks_read), 0), 
        2
    )::text || '%' as value
FROM pg_stat_database;
```

**2️⃣ Автоматизированный мониторинг:**

```sql
-- Создание таблицы для логирования производительности
CREATE TABLE query_performance_log (
    log_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    query_type VARCHAR(50),
    execution_time_ms INTEGER,
    rows_affected INTEGER,
    query_text TEXT
);

-- Триггер для автоматического логирования медленных запросов
-- (реализация зависит от СУБД)
```

#### 🔧 Процедуры обслуживания

**1️⃣ Обновление статистик:**

```sql
-- Регулярное обновление статистик для оптимизатора
ANALYZE; -- PostgreSQL
-- или
UPDATE STATISTICS; -- SQL Server
-- или
EXEC DBMS_STATS.GATHER_DATABASE_STATS; -- Oracle
```

**2️⃣ Реиндексация и дефрагментация:**

```sql
-- Перестроение фрагментированных индексов
REINDEX INDEX idx_sales_date; -- PostgreSQL

-- Проверка фрагментации индексов (SQL Server)
SELECT 
    i.name as index_name,
    s.avg_fragmentation_in_percent,
    s.page_count
FROM sys.dm_db_index_physical_stats(DB_ID(), NULL, NULL, NULL, 'LIMITED') s
JOIN sys.indexes i ON s.object_id = i.object_id AND s.index_id = i.index_id
WHERE s.avg_fragmentation_in_percent > 30;
```

**3️⃣ Архивирование старых данных:**

```sql
-- Стратегия партиционирования по датам
CREATE TABLE sales_2024 PARTITION OF sales 
FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');

-- Автоматическое удаление старых партиций
DROP TABLE sales_2022; -- после архивирования
```

---

## 📋 Инструкции

Эта глава посвящена критически важному навыку — оптимизации производительности SQL-запросов. Вы изучите, как анализировать планы выполнения, создавать эффективные индексы и интегрировать оптимизацию SQL с DAX в Power BI.

Особое внимание уделите практическим упражнениям с реальными данными — они покажут разительное отличие в производительности до и после оптимизации.

- 📝 [Перейти к практическим заданиям](practice.md)
- ✅ [Перейти к чек-листу](checklist.md)
- 📁 [Посмотреть учебные файлы](files/README.md)

---

- 🔙 [Предыдущая глава: Глава 21: - Реляционные модели данных и индексы](../chapter-21/README.md)
- 🔜 [Следующая глава: Глава 23: Презентация результатов: storytelling, отчёты](../chapter-23/README.md)

---

- 📢 Присоединяйтесь к чату курса: https://t.me/analytics_course_chat
- 📢 Канал курса: https://t.me/analytics_course_channel