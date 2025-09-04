# 📊 Глава 21: Реляционные модели данных и индексы

## 🎯 Цели обучения

После изучения этой главы вы сможете:

- 🏗️ **Проектировать реляционные модели данных** для бизнес-задач
- 🔗 **Создавать правильные связи** между таблицами с помощью ключей
- 📐 **Применять нормализацию** для устранения избыточности данных
- ⚡ **Использовать индексы** для оптимизации производительности запросов
- 🎨 **Строить модели данных в Power Pivot** для аналитики
- 🔍 **Анализировать и улучшать** существующие структуры данных

---

## 📚 Теория

### 🏗️ Реляционные модели данных: Основы

#### 🎭 Метафора: Библиотека
Представьте, что вы организуете большую библиотеку. Реляционная модель данных — это как система каталогов в библиотеке:

- **Таблицы** — это разные каталоги (книги, авторы, читатели, выдачи)
- **Строки** — это карточки в каталоге (конкретная книга, конкретный автор)
- **Связи** — это ссылки между каталогами (какой автор написал какую книгу)
- **Ключи** — это уникальные номера (ISBN книги, номер читательского билета)

#### 🧩 Основные понятия

**1️⃣ Таблица (Table/Relation)**
```sql
-- Таблица "Читатели"
CREATE TABLE readers (
    reader_id INTEGER PRIMARY KEY,    -- Первичный ключ
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE,
    registration_date DATE
);
```

**2️⃣ Первичный ключ (Primary Key)**
```sql
-- Уникальный идентификатор каждой строки
-- Как паспортный номер для человека
ALTER TABLE books 
ADD CONSTRAINT pk_books PRIMARY KEY (book_id);
```

**3️⃣ Внешний ключ (Foreign Key)**
```sql
-- Связь между таблицами
-- Как ссылка на другой каталог в библиотеке
ALTER TABLE loans 
ADD CONSTRAINT fk_loans_reader 
FOREIGN KEY (reader_id) REFERENCES readers(reader_id);
```

---

### 🔗 Типы связей между таблицами

#### 🎭 Метафора: Семейные отношения
Связи между таблицами похожи на родственные связи в большой семье:

**1️⃣ Один-к-одному (1:1) — Муж и жена**
```sql
-- Каждый человек имеет один паспорт, каждый паспорт принадлежит одному человеку
CREATE TABLE persons (
    person_id INTEGER PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50)
);

CREATE TABLE passports (
    passport_id INTEGER PRIMARY KEY,
    person_id INTEGER UNIQUE,  -- UNIQUE обеспечивает связь 1:1
    passport_number VARCHAR(20),
    issue_date DATE,
    FOREIGN KEY (person_id) REFERENCES persons(person_id)
);
```

**2️⃣ Один-ко-многим (1:N) — Мать и дети**
```sql
-- Один автор может написать много книг
CREATE TABLE authors (
    author_id INTEGER PRIMARY KEY,
    author_name VARCHAR(100)
);

CREATE TABLE books (
    book_id INTEGER PRIMARY KEY,
    title VARCHAR(200),
    author_id INTEGER,  -- Внешний ключ
    publication_year INTEGER,
    FOREIGN KEY (author_id) REFERENCES authors(author_id)
);
```

**3️⃣ Многие-ко-многим (M:N) — Студенты и курсы**
```sql
-- Один студент может изучать много курсов, один курс могут изучать много студентов
-- Нужна промежуточная таблица (таблица связи)

CREATE TABLE students (
    student_id INTEGER PRIMARY KEY,
    student_name VARCHAR(100)
);

CREATE TABLE courses (
    course_id INTEGER PRIMARY KEY,
    course_name VARCHAR(100)
);

CREATE TABLE enrollments (  -- Таблица связи
    enrollment_id INTEGER PRIMARY KEY,
    student_id INTEGER,
    course_id INTEGER,
    enrollment_date DATE,
    grade DECIMAL(3,2),
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);
```

---

### 📐 Нормализация данных

#### 🎭 Метафора: Уборка в доме
Нормализация — это как генеральная уборка в доме, где мы:
- **Убираем дубликаты** (не храним одну и ту же вещь в разных комнатах)
- **Организуем по категориям** (посуда на кухне, одежда в шкафу)
- **Создаём логичные связи** (ключи от машины рядом с документами)

#### 🏠 Первая нормальная форма (1НФ)

**Правило:** Каждая ячейка содержит только одно значение

❌ **Неправильно (не в 1НФ):**
```sql
-- Проблема: несколько значений в одной ячейке
CREATE TABLE orders_bad (
    order_id INTEGER,
    customer_name VARCHAR(100),
    products VARCHAR(500)  -- "Хлеб, Молоко, Сыр" - несколько значений!
);
```

✅ **Правильно (в 1НФ):**
```sql
CREATE TABLE orders (
    order_id INTEGER,
    customer_name VARCHAR(100)
);

CREATE TABLE order_items (
    order_id INTEGER,
    product_name VARCHAR(100),
    quantity INTEGER,
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
);
```

#### 🏡 Вторая нормальная форма (2НФ)

**Правило:** Все неключевые атрибуты зависят от всего первичного ключа

❌ **Неправильно (не в 2НФ):**
```sql
-- Проблема: customer_name зависит только от customer_id, а не от составного ключа
CREATE TABLE order_details_bad (
    order_id INTEGER,
    customer_id INTEGER,
    customer_name VARCHAR(100),  -- Зависит только от customer_id!
    product_id INTEGER,
    product_name VARCHAR(100),   -- Зависит только от product_id!
    quantity INTEGER,
    PRIMARY KEY (order_id, product_id)
);
```

✅ **Правильно (в 2НФ):**
```sql
CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    customer_name VARCHAR(100)
);

CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    product_name VARCHAR(100),
    price DECIMAL(10,2)
);

CREATE TABLE order_details (
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    PRIMARY KEY (order_id, product_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);
```

#### 🏘️ Третья нормальная форма (3НФ)

**Правило:** Нет транзитивных зависимостей (неключевые атрибуты не зависят друг от друга)

❌ **Неправильно (не в 3НФ):**
```sql
-- Проблема: city_region зависит от city, а не от customer_id
CREATE TABLE customers_bad (
    customer_id INTEGER PRIMARY KEY,
    customer_name VARCHAR(100),
    city VARCHAR(50),
    city_region VARCHAR(50)  -- Зависит от city, а не от customer_id!
);
```

✅ **Правильно (в 3НФ):**
```sql
CREATE TABLE regions (
    region_id INTEGER PRIMARY KEY,
    region_name VARCHAR(50)
);

CREATE TABLE cities (
    city_id INTEGER PRIMARY KEY,
    city_name VARCHAR(50),
    region_id INTEGER,
    FOREIGN KEY (region_id) REFERENCES regions(region_id)
);

CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    customer_name VARCHAR(100),
    city_id INTEGER,
    FOREIGN KEY (city_id) REFERENCES cities(city_id)
);
```

---

### ⚡ Индексы: Ускорение поиска данных

#### 🎭 Метафора: Алфавитный указатель в книге
Индекс в базе данных — это как алфавитный указатель в конце учебника:

- **Без индекса** — читаете всю книгу от начала до конца, чтобы найти нужную тему
- **С индексом** — смотрите в указатель, находите номер страницы и сразу переходите к нужному месту

#### 🔍 Типы индексов

**1️⃣ Первичный индекс (Primary Index)**
```sql
-- Создается автоматически для PRIMARY KEY
CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,  -- Автоматически создается индекс
    customer_name VARCHAR(100)
);
```

**2️⃣ Уникальный индекс (Unique Index)**
```sql
-- Для столбцов с уникальными значениями
CREATE UNIQUE INDEX idx_customer_email 
ON customers(email);

-- Альтернативный способ
ALTER TABLE customers 
ADD CONSTRAINT unique_email UNIQUE (email);
```

**3️⃣ Обычный индекс (Non-unique Index)**
```sql
-- Для ускорения поиска по часто используемым столбцам
CREATE INDEX idx_customer_city 
ON customers(city);

CREATE INDEX idx_order_date 
ON orders(order_date);

-- Составной индекс (по нескольким столбцам)
CREATE INDEX idx_customer_city_name 
ON customers(city, last_name);
```

**4️⃣ Частичный индекс (Partial Index)**
```sql
-- Индекс только для части данных (PostgreSQL, SQLite)
CREATE INDEX idx_active_customers 
ON customers(customer_id) 
WHERE status = 'active';
```

#### ⚖️ Когда использовать индексы

✅ **Создавайте индексы для:**
- Столбцов в WHERE условиях
- Столбцов в JOIN условиях  
- Столбцов в ORDER BY
- Часто используемых для поиска полей

❌ **Не создавайте индексы для:**
- Таблиц с частыми INSERT/UPDATE/DELETE
- Столбцов с небольшим количеством уникальных значений
- Очень маленьких таблиц (< 1000 строк)

```sql
-- Анализ использования индексов
EXPLAIN QUERY PLAN 
SELECT * FROM customers 
WHERE city = 'Москва' 
ORDER BY last_name;

-- Создание индекса для оптимизации
CREATE INDEX idx_customers_city_name 
ON customers(city, last_name);
```

---

### 🎨 Модели данных в Power Pivot

#### 🎭 Метафора: Конструктор LEGO
Power Pivot — это как конструктор LEGO для данных:
- **Таблицы** — это наборы деталей разных типов
- **Связи** — это способы соединения деталей
- **Модель** — это готовая конструкция из связанных элементов

#### 🔗 Создание модели данных в Power Pivot

**1️⃣ Импорт таблиц**
```dax
// В Power Pivot можно импортировать из различных источников:
// - Excel таблицы
// - SQL базы данных  
// - CSV файлы
// - Web источники
```

**2️⃣ Создание связей**
```dax
// Связи создаются автоматически или вручную
// Типы связей в Power Pivot:
// - Один-ко-многим (наиболее распространенный)
// - Один-к-одному (редко используется)
```

**3️⃣ Построение star schema (схема звезды)**
```dax
// Центральная таблица фактов
Sales = 
TABLE(
    SalesAmount, 
    Quantity, 
    CustomerID, 
    ProductID, 
    DateID
)

// Таблицы измерений вокруг фактов
Customers = TABLE(CustomerID, CustomerName, City, Region)
Products = TABLE(ProductID, ProductName, Category, Price)
Calendar = TABLE(DateID, Date, Year, Month, Quarter)
```

**4️⃣ Создание вычисляемых столбцов**
```dax
// Добавление вычисляемых полей в модель
[Total Sales] = [Quantity] * [Unit Price]

[Customer Segment] = 
IF([Total Customer Sales] > 100000, "VIP",
   IF([Total Customer Sales] > 50000, "Premium", "Regular"))
```

**5️⃣ Создание мер (Measures)**
```dax
// Агрегированные вычисления
Total Revenue = SUM(Sales[SalesAmount])

Average Order Value = 
DIVIDE(
    SUM(Sales[SalesAmount]), 
    DISTINCTCOUNT(Sales[OrderID])
)

Year-over-Year Growth = 
VAR CurrentYearSales = [Total Revenue]
VAR PreviousYearSales = 
    CALCULATE(
        [Total Revenue],
        DATEADD(Calendar[Date], -1, YEAR)
    )
RETURN
    DIVIDE(CurrentYearSales - PreviousYearSales, PreviousYearSales)
```

---

### 🔍 ER-диаграммы: Визуальное проектирование

#### 🎭 Метафора: Архитектурный план
ER-диаграмма (Entity-Relationship) — это как план здания перед строительством:
- **Сущности** (прямоугольники) — это комнаты в доме
- **Атрибуты** (овалы) — это мебель и оборудование в комнатах  
- **Связи** (ромбы) — это двери и коридоры между комнатами

#### 🏗️ Элементы ER-диаграммы

**📦 Сущности (Entities)**
```
┌─────────────┐
│   КЛИЕНТ    │
├─────────────┤
│ id          │
│ имя         │
│ email       │
│ телефон     │
└─────────────┘
```

**🔗 Связи (Relationships)**
```
КЛИЕНТ ────┐
           │ размещает
           ▼
         ЗАКАЗ ────┐
                   │ содержит
                   ▼
                 ТОВАР
```

**📋 Кардинальность связей**
- `1:1` — Один к одному
- `1:N` — Один ко многим  
- `M:N` — Многие ко многим

---

### 🛠️ Практические принципы проектирования

#### ✅ Лучшие практики

**1️⃣ Именование**
```sql
-- Используйте понятные имена
CREATE TABLE customers (          -- ✅ Хорошо
    customer_id INTEGER,
    first_name VARCHAR(50)
);

CREATE TABLE cust (               -- ❌ Плохо
    id INTEGER,
    fn VARCHAR(50)
);
```

**2️⃣ Типы данных**
```sql
-- Выбирайте правильные типы данных
CREATE TABLE products (
    product_id INTEGER,           -- Для целых чисел
    price DECIMAL(10,2),          -- Для денег (точность важна)
    description TEXT,             -- Для длинного текста
    created_date TIMESTAMP,       -- Для даты и времени
    is_active BOOLEAN             -- Для логических значений
);
```

**3️⃣ Ограничения целостности**
```sql
-- Добавляйте ограничения для защиты данных
CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    order_date DATE NOT NULL DEFAULT CURRENT_DATE,
    total_amount DECIMAL(10,2) CHECK (total_amount > 0),
    status VARCHAR(20) CHECK (status IN ('pending', 'completed', 'cancelled')),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);
```

**4️⃣ Документирование**
```sql
-- Добавляйте комментарии к таблицам и столбцам
COMMENT ON TABLE customers IS 'Информация о клиентах компании';
COMMENT ON COLUMN customers.customer_id IS 'Уникальный идентификатор клиента';
COMMENT ON COLUMN customers.created_date IS 'Дата регистрации клиента в системе';
```

#### ⚠️ Частые ошибки

❌ **Избегайте этих ошибок:**
- Отсутствие первичных ключей
- Хранение вычисляемых значений
- Слишком много или слишком мало нормализации
- Игнорирование производительности
- Плохое именование таблиц и столбцов

---

### 🔄 Интеграция SQL и Power Pivot

#### 🌉 Мост между технологиями

**1️⃣ Подготовка данных в SQL**
```sql
-- Создание представления для Power Pivot
CREATE VIEW sales_analytics AS
SELECT 
    s.sale_date,
    c.customer_name,
    c.city,
    p.product_name,
    p.category,
    s.quantity,
    s.unit_price,
    s.quantity * s.unit_price AS total_amount
FROM sales s
JOIN customers c ON s.customer_id = c.customer_id
JOIN products p ON s.product_id = p.product_id
WHERE s.sale_date >= DATE('now', '-2 years');
```

**2️⃣ Импорт в Power Pivot**
```dax
// Подключение к SQL базе данных
// Данные → Получить данные → Из базы данных → Из SQL Server

// Создание связей в модели данных
// Связи создаются автоматически на основе внешних ключей
```

**3️⃣ Создание аналитических мер**
```dax
// Использование подготовленной модели для аналитики
Total Sales = SUM([total_amount])

Sales Growth = 
VAR CurrentMonth = [Total Sales]
VAR PreviousMonth = 
    CALCULATE(
        [Total Sales], 
        DATEADD(Calendar[Date], -1, MONTH)
    )
RETURN
    DIVIDE(CurrentMonth - PreviousMonth, PreviousMonth)

Top Products by Sales = 
CALCULATE(
    [Total Sales],
    TOPN(10, Products, [Total Sales], DESC)
)
```

---

## 📋 Инструкции

Эта глава знакомит вас с основами проектирования баз данных — навыком, критически важным для любого аналитика данных. Вы изучите, как правильно структурировать информацию, создавать эффективные связи между таблицами и оптимизировать производительность.

Особое внимание уделите практическим упражнениям в Power Pivot — этот инструмент позволяет создавать мощные аналитические модели без глубокого знания SQL.

- 📝 [Перейти к практическим заданиям](practice.md)
- ✅ [Перейти к чек-листу](checklist.md)
- 📁 [Посмотреть учебные файлы](files/README.md)

---

- 🔙 [Предыдущая глава: Глава 20 - SQL: JOIN и подзапросы](../chapter-20/README.md)
- 🔜 [Следующая глава: Глава 22: Оптимизация SQL-запросов](../chapter-22/README.md)

---

- 📢 Присоединяйтесь к чату курса: https://t.me/analytics_course_chat
- 📢 Канал курса: https://t.me/analytics_course_channel