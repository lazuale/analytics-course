# 📋 Глава 20: SQL: JOIN, подзапросы, CTE

## 🎯 Цели обучения

После изучения этой главы вы сможете:

- 🔗 **Объединять данные** из нескольких таблиц с помощью различных типов JOIN
- 🔍 **Создавать сложные запросы** с использованием подзапросов (субзапросов)
- 🏗️ **Структурировать запросы** с помощью Common Table Expressions (CTE)
- 🧮 **Решать многоуровневые аналитические задачи** в SQL
- 🐍 **Интегрировать SQL и Python** для комплексного анализа данных

---

## 📚 Теория

### 🔗 JOIN: Объединение таблиц

#### 🎭 Метафора: Свадебная церемония
Представьте, что у вас есть два списка гостей на свадьбу: **список невесты** и **список жениха**. JOIN в SQL — это способ объединить эти списки по различным правилам:

- **INNER JOIN** — только те, кто есть в обоих списках (общие друзья)
- **LEFT JOIN** — все из списка невесты + совпадающие из списка жениха
- **RIGHT JOIN** — все из списка жениха + совпадающие из списка невесты  
- **FULL OUTER JOIN** — все гости из обоих списков

#### 🔧 Типы JOIN операций

**1️⃣ INNER JOIN (внутреннее соединение)**
```sql
-- Показать только клиентов, у которых есть заказы
SELECT c.name, o.order_date, o.amount
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id;
```

**2️⃣ LEFT JOIN (левое соединение)**
```sql
-- Показать всех клиентов, даже без заказов
SELECT c.name, o.order_date, o.amount
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id;
```

**3️⃣ RIGHT JOIN (правое соединение)**
```sql
-- Показать все заказы и информацию о клиентах
SELECT c.name, o.order_date, o.amount
FROM customers c
RIGHT JOIN orders o ON c.customer_id = o.customer_id;
```

**4️⃣ FULL OUTER JOIN (полное внешнее соединение)**
```sql
-- Показать всех клиентов и все заказы
SELECT c.name, o.order_date, o.amount
FROM customers c
FULL OUTER JOIN orders o ON c.customer_id = o.customer_id;
```

**5️⃣ CROSS JOIN (декартово произведение)**
```sql
-- Каждый клиент с каждым продуктом (осторожно с размером результата!)
SELECT c.name, p.product_name
FROM customers c
CROSS JOIN products p;
```

#### 🌟 Множественные JOIN
```sql
-- Объединение трёх и более таблиц
SELECT 
    c.customer_name,
    o.order_date,
    p.product_name,
    oi.quantity,
    oi.price
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
INNER JOIN order_items oi ON o.order_id = oi.order_id
INNER JOIN products p ON oi.product_id = p.product_id;
```

---

### 🔍 Подзапросы (Субзапросы)

#### 🎭 Метафора: Матрёшка
Подзапрос — это как матрёшка в матрёшке. Сначала SQL "открывает" внутренний запрос (маленькую матрёшку), получает результат, а затем использует его во внешнем запросе (большой матрёшке).

#### 🔧 Типы подзапросов

**1️⃣ Скалярные подзапросы (возвращают одно значение)**
```sql
-- Клиенты с суммой заказов выше средней
SELECT customer_name
FROM customers
WHERE total_orders > (
    SELECT AVG(total_orders) 
    FROM customers
);
```

**2️⃣ Подзапросы в WHERE с IN**
```sql
-- Клиенты из городов с населением больше 1 млн
SELECT customer_name
FROM customers
WHERE city IN (
    SELECT city_name 
    FROM cities 
    WHERE population > 1000000
);
```

**3️⃣ Подзапросы с EXISTS**
```sql
-- Клиенты, у которых есть заказы
SELECT customer_name
FROM customers c
WHERE EXISTS (
    SELECT 1 
    FROM orders o 
    WHERE o.customer_id = c.customer_id
);
```

**4️⃣ Коррелированные подзапросы**
```sql
-- Клиенты с заказом больше их среднего заказа
SELECT customer_name, order_amount
FROM orders o1
WHERE order_amount > (
    SELECT AVG(order_amount)
    FROM orders o2
    WHERE o2.customer_id = o1.customer_id
);
```

**5️⃣ Подзапросы в SELECT**
```sql
-- Добавление вычисляемых полей
SELECT 
    customer_name,
    (SELECT COUNT(*) 
     FROM orders 
     WHERE customer_id = c.customer_id) as order_count,
    (SELECT SUM(amount) 
     FROM orders 
     WHERE customer_id = c.customer_id) as total_spent
FROM customers c;
```

---

### 🏗️ CTE: Common Table Expressions

#### 🎭 Метафора: Строительные леса
CTE — это как строительные леса при возведении здания. Они помогают построить сложную конструкцию (запрос) по частям, а потом можно эти "леса" убрать, оставив готовое "здание" (результат).

#### 🔧 Синтаксис и примеры CTE

**1️⃣ Простой CTE**
```sql
-- Определяем CTE для активных клиентов
WITH active_customers AS (
    SELECT customer_id, customer_name
    FROM customers
    WHERE last_order_date >= DATE('now', '-30 days')
)
-- Используем CTE в основном запросе
SELECT ac.customer_name, COUNT(o.order_id) as recent_orders
FROM active_customers ac
JOIN orders o ON ac.customer_id = o.customer_id
GROUP BY ac.customer_name;
```

**2️⃣ Множественные CTE**
```sql
-- Несколько CTE в одном запросе
WITH 
-- Первый CTE: топ клиенты
top_customers AS (
    SELECT customer_id, SUM(amount) as total_spent
    FROM orders
    GROUP BY customer_id
    HAVING SUM(amount) > 10000
),
-- Второй CTE: популярные товары
popular_products AS (
    SELECT product_id, COUNT(*) as order_count
    FROM order_items
    GROUP BY product_id
    HAVING COUNT(*) > 50
)
-- Основной запрос использует оба CTE
SELECT tc.customer_id, pp.product_id
FROM top_customers tc
JOIN orders o ON tc.customer_id = o.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
JOIN popular_products pp ON oi.product_id = pp.product_id;
```

**3️⃣ Рекурсивный CTE**
```sql
-- Иерархия сотрудников (кто кому подчиняется)
WITH RECURSIVE employee_hierarchy AS (
    -- Начальное условие: топ-менеджеры
    SELECT employee_id, employee_name, manager_id, 1 as level
    FROM employees
    WHERE manager_id IS NULL
    
    UNION ALL
    
    -- Рекурсивная часть: подчинённые
    SELECT e.employee_id, e.employee_name, e.manager_id, eh.level + 1
    FROM employees e
    JOIN employee_hierarchy eh ON e.manager_id = eh.employee_id
    WHERE eh.level < 5  -- Ограничение глубины
)
SELECT * FROM employee_hierarchy
ORDER BY level, employee_name;
```

---

### 🔄 Комбинирование техник

#### 🎯 CTE + JOIN + Подзапросы
```sql
-- Комплексный анализ: клиенты с высокой активностью
WITH 
-- Средние показатели по всем клиентам
customer_averages AS (
    SELECT 
        AVG(order_count) as avg_orders,
        AVG(total_spent) as avg_spent
    FROM (
        SELECT 
            customer_id,
            COUNT(*) as order_count,
            SUM(amount) as total_spent
        FROM orders
        GROUP BY customer_id
    ) customer_stats
),
-- Клиенты выше среднего
above_average_customers AS (
    SELECT 
        c.customer_id,
        c.customer_name,
        COUNT(o.order_id) as order_count,
        SUM(o.amount) as total_spent
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.customer_name
    HAVING 
        COUNT(o.order_id) > (SELECT avg_orders FROM customer_averages) AND
        SUM(o.amount) > (SELECT avg_spent FROM customer_averages)
)
-- Финальный результат с дополнительной информацией
SELECT 
    aac.customer_name,
    aac.order_count,
    aac.total_spent,
    -- Подзапрос: последний заказ
    (SELECT MAX(order_date) 
     FROM orders 
     WHERE customer_id = aac.customer_id) as last_order_date,
    -- Сравнение со средними
    ROUND(aac.order_count / ca.avg_orders, 2) as order_ratio,
    ROUND(aac.total_spent / ca.avg_spent, 2) as spending_ratio
FROM above_average_customers aac
CROSS JOIN customer_averages ca
ORDER BY aac.total_spent DESC;
```

---

### 🐍 Интеграция SQL и Python

#### 📊 Использование результатов SQL в Python
```python
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Подключение к базе данных
conn = sqlite3.connect('sales_database.db')

# Выполнение сложного SQL запроса
sql_query = """
WITH monthly_sales AS (
    SELECT 
        strftime('%Y-%m', order_date) as month,
        SUM(amount) as total_sales,
        COUNT(*) as order_count
    FROM orders
    WHERE order_date >= date('now', '-12 months')
    GROUP BY strftime('%Y-%m', order_date)
)
SELECT * FROM monthly_sales
ORDER BY month;
"""

# Загрузка данных в DataFrame
df = pd.read_sql_query(sql_query, conn)

# Визуализация в Python
plt.figure(figsize=(10, 6))
plt.plot(df['month'], df['total_sales'], marker='o')
plt.title('📈 Динамика продаж по месяцам')
plt.xlabel('Месяц')
plt.ylabel('Общие продажи')
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)
plt.show()

conn.close()
```

---

### 🎯 Практические советы

#### ✅ Лучшие практики JOIN
- Всегда указывайте условие соединения в ON
- Используйте алиасы таблиц для читаемости
- Внимательно выбирайте тип JOIN под задачу
- Проверяйте размер результата при CROSS JOIN

#### ✅ Лучшие практики подзапросов
- Используйте подзапросы для читаемости кода
- EXISTS быстрее IN для больших таблиц
- Избегайте коррелированных подзапросов в циклах
- Тестируйте подзапросы отдельно

#### ✅ Лучшие практики CTE
- Используйте описательные имена для CTE
- Разбивайте сложную логику на несколько CTE
- Документируйте назначение каждого CTE
- Помните об ограничениях рекурсии

#### ⚠️ Частые ошибки
- Забывание условия ON в JOIN
- Дублирование строк при неправильном JOIN
- Бесконечная рекурсия в CTE
- Использование коррелированных подзапросов без необходимости

---

## 📋 Инструкции

Эта глава содержит продвинутые техники работы с SQL, которые позволяют решать сложные аналитические задачи. Сначала изучите теоретический материал, обращая особое внимание на метафоры и примеры. Затем переходите к практическим заданиям, где вы примените все изученные техники на реальных данных.

Особое внимание уделите интеграции SQL с Python — это мощное сочетание для современной аналитики данных.

- 📝 [Перейти к практическим заданиям](practice.md)
- ✅ [Перейти к чек-листу](checklist.md)
- 📁 [Посмотреть учебные файлы](files/README.md)

---

- 🔙 [Предыдущая глава: Глава 19 - SQL: основные запросы, агрегаты, GROUP BY](../chapter-19/README.md)
- 🔜 [Следующая глава: Глава 21 - Реляционные модели данных и индексы](../chapter-21/README.md)

---

- 📢 Присоединяйтесь к чату курса: https://t.me/analytics_course_chat
- 📢 Канал курса: https://t.me/analytics_course_channel