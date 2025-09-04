# 📁 Описание учебных файлов — Глава 22

В этой папке содержатся все необходимые файлы для изучения оптимизации SQL-запросов, анализа планов выполнения, создания эффективных индексов и мониторинга производительности баз данных.

---

## 📊 Обзор данных

### 🛒 Система интернет-магазина для тестирования производительности

Учебные данные представляют реалистичную систему интернет-магазина с различными характеристиками для тестирования производительности:
- **Клиенты** — информация о покупателях из разных стран и городов
- **Заказы** — транзакции с различными статусами и суммами
- **Товары** — каталог продукции с категориями и ценами
- **Позиции заказов** — детализация покупок с количествами и скидками
- **Логи производительности** — система мониторинга выполнения запросов

### ⚡ Сценарии для оптимизации
```
Медленные запросы → Анализ планов → Создание индексов → Измерение улучшений
        ↓                ↓               ↓                    ↓
   Выявление         EXPLAIN         B-Tree, Hash,        Замеры времени
  узких мест          PLAN          Composite           выполнения
```

---

## 📋 Описание файлов

### 1️⃣ Базы данных для тестирования

#### `ecommerce_performance.db` — Основная база данных интернет-магазина
**Описание:** SQLite база данных с реалистичными данными для тестирования производительности

**Структура таблиц:**
```sql
customers (50,000 записей)
├─ customer_id (PK)
├─ customer_name  
├─ email (UNIQUE)
├─ country, city
├─ registration_date
└─ customer_segment

orders (200,000 записей)  
├─ order_id (PK)
├─ customer_id (FK)
├─ order_date
├─ total_amount
└─ status

products (10,000 записей)
├─ product_id (PK) 
├─ product_name
├─ category, subcategory
├─ price
└─ in_stock

order_items (800,000 записей)
├─ order_item_id (PK)
├─ order_id (FK)
├─ product_id (FK)
├─ quantity
├─ unit_price
└─ discount
```

**Особенности для тестирования:**
- Различное распределение данных по таблицам
- Реалистичные корреляции между полями
- Намеренно отсутствующие индексы для демонстрации проблем
- Данные за 3 года для временного анализа

---

#### `ecommerce_large.db` — Расширенная база для стресс-тестирования
**Описание:** Увеличенная версия базы данных для тестирования на больших объемах

**Масштаб данных:**
- Клиенты: 500,000 записей
- Заказы: 2,000,000 записей  
- Позиции заказов: 8,000,000 записей
- Размер файла: ~2GB
- Временной период: 5 лет данных

**Использование:** Для тестирования производительности индексов на больших данных

---

### 2️⃣ SQL скрипты для анализа и оптимизации

#### `slow_queries.sql` — Коллекция медленных запросов
**Описание:** Набор специально созданных неэффективных SQL-запросов для практики оптимизации

**Категории медленных запросов:**
```sql
-- 1. Запросы с функциями в WHERE
SELECT * FROM customers 
WHERE UPPER(email) LIKE '%GMAIL%';

-- 2. Неоптимальные JOIN без индексов
SELECT c.customer_name, COUNT(o.order_id)
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_name; -- без индекса на customer_id

-- 3. Коррелированные подзапросы
SELECT p.product_name
FROM products p  
WHERE p.price > (
    SELECT AVG(p2.price) 
    FROM products p2 
    WHERE p2.category = p.category
);

-- 4. Неэффективные OR условия
SELECT * FROM orders
WHERE status = 'pending' 
   OR status = 'processing'
   OR total_amount > 5000;

-- 5. Агрегации без индексов
SELECT 
    DATE_TRUNC('month', order_date) as month,
    COUNT(*) as orders_count
FROM orders
GROUP BY DATE_TRUNC('month', order_date)
ORDER BY month;
```

**Для каждого запроса предоставлены:**
- Описание проблемы производительности
- План выполнения до оптимизации
- Рекомендации по улучшению
- Оптимизированная версия запроса

---

#### `optimization_solutions.sql` — Решения для оптимизации
**Описание:** Оптимизированные версии медленных запросов с пояснениями

**Техники оптимизации:**
```sql
-- Решение 1: Избегание функций в WHERE
-- БЫЛО:
WHERE UPPER(email) LIKE '%GMAIL%'
-- СТАЛО:
WHERE email LIKE '%gmail%' OR email LIKE '%GMAIL%'
-- + функциональный индекс: CREATE INDEX idx_email_upper ON customers(UPPER(email))

-- Решение 2: Оптимизация JOIN
-- БЫЛО: JOIN без индексов
-- СТАЛО: CREATE INDEX idx_orders_customer_id ON orders(customer_id)

-- Решение 3: Замена коррелированных подзапросов
-- БЫЛО: коррелированный подзапрос
-- СТАЛО: оконные функции или JOIN с агрегацией

-- Решение 4: Оптимизация OR условий  
-- БЫЛО: множественные OR
-- СТАЛО: IN (...) или UNION запросы

-- Решение 5: Индексы для агрегаций
-- СТАЛО: CREATE INDEX idx_orders_date ON orders(order_date)
```

---

#### `index_creation_script.sql` — Скрипты создания оптимальных индексов
**Описание:** Комплексные скрипты для создания эффективной системы индексов

**Типы создаваемых индексов:**
```sql
-- B-Tree индексы для поиска
CREATE INDEX idx_customers_email ON customers(email);
CREATE INDEX idx_orders_date ON orders(order_date);

-- Составные индексы для сложных запросов
CREATE INDEX idx_orders_customer_date ON orders(customer_id, order_date);
CREATE INDEX idx_products_category_price ON products(category, price);

-- Покрывающие индексы
CREATE INDEX idx_customers_covering 
ON customers(city, customer_id, customer_name, email);

-- Частичные индексы для экономии места
CREATE INDEX idx_orders_pending 
ON orders(customer_id) 
WHERE status = 'pending';

-- Функциональные индексы
CREATE INDEX idx_orders_month 
ON orders(DATE_TRUNC('month', order_date));
```

**Каждый индекс содержит:**
- Обоснование создания
- Примеры запросов, которые он ускоряет
- Оценку влияния на производительность
- Рекомендации по обслуживанию

---

#### `remove_indexes.sql` — Удаление индексов для чистого тестирования
**Описание:** Скрипт для удаления всех индексов (кроме PRIMARY KEY) для базового тестирования

```sql
-- Получение списка всех пользовательских индексов
SELECT 'DROP INDEX ' || name || ';' as drop_statement
FROM sqlite_master 
WHERE type = 'index' 
  AND name NOT LIKE 'sqlite_autoindex%'
  AND name NOT LIKE '%_pk';

-- Удаление всех индексов одной командой
-- Используется для получения baseline производительности
```

---

### 3️⃣ Python скрипты для автоматизации

#### `performance_monitor.py` — Система мониторинга производительности
**Описание:** Комплексная система мониторинга выполнения SQL-запросов

**Основные возможности:**
```python
class DatabasePerformanceMonitor:
    def __init__(self, db_path):
        """Инициализация системы мониторинга"""
    
    def log_query_performance(self, query, execution_time, rows_affected):
        """Логирование производительности каждого запроса"""
    
    def detect_slow_queries(self, threshold_ms=5000):
        """Автоматическое выявление медленных запросов"""
    
    def analyze_query_patterns(self):
        """Анализ паттернов использования БД"""
    
    def generate_optimization_suggestions(self):
        """AI-рекомендации по оптимизации"""
    
    def create_performance_alerts(self):
        """Система уведомлений о проблемах"""
```

**Функциональность:**
- Автоматическое логирование времени выполнения запросов
- Выявление часто выполняемых медленных запросов
- Анализ планов выполнения через Python
- Генерация отчетов о производительности
- Интеграция с системами уведомлений

---

#### `automated_benchmarking.py` — Автоматизированное тестирование производительности
**Описание:** Инструмент для автоматического сравнения производительности до и после оптимизации

**Процесс тестирования:**
```python
class PerformanceBenchmark:
    def __init__(self):
        """Настройка тестовой среды"""
    
    def run_baseline_tests(self):
        """Тестирование без индексов (baseline)"""
        # Выполнение набора стандартных запросов
        # Измерение времени выполнения
        # Анализ планов выполнения
    
    def apply_optimizations(self):
        """Применение оптимизаций (индексы, переписывание запросов)"""
    
    def run_optimized_tests(self):
        """Тестирование с оптимизациями"""
    
    def generate_comparison_report(self):
        """Генерация отчета сравнения"""
        # Таблицы улучшений производительности
        # Графики времени выполнения
        # Рекомендации по дальнейшей оптимизации
```

**Метрики измерения:**
- Время выполнения запросов (мс)
- Количество прочитанных страниц
- Использование индексов
- Память, используемая для сортировки
- CPU время

---

#### `database_maintenance.py` — Автоматическое обслуживание БД
**Описание:** Система автоматического обслуживания для поддержания производительности

**Задачи обслуживания:**
```python
def update_table_statistics():
    """Обновление статистик для оптимизатора запросов"""
    # Выполнение ANALYZE для всех таблиц
    # Обновление гистограмм распределения данных

def reindex_fragmented_indexes():
    """Перестроение фрагментированных индексов"""
    # Анализ фрагментации индексов
    # Перестроение при превышении порога

def vacuum_database():
    """Дефрагментация базы данных"""
    # Освобождение неиспользуемого места
    # Оптимизация файловой структуры

def archive_old_data():
    """Архивирование устаревших данных"""
    # Перенос старых записей в архивные таблицы
    # Поддержание оптимального размера рабочих таблиц
```

---

### 4️⃣ Power BI файлы для интеграции

#### `ecommerce_dashboard.pbix` — Оптимизированный дашборд Power BI
**Описание:** Power BI файл с оптимизированной моделью данных и эффективными DAX мерами

**Содержимое модели:**
- Импорт данных из оптимизированных SQL представлений
- Правильно настроенные связи между таблицами
- Календарная таблица для временного анализа
- Эффективные меры DAX, использующие предагрегированные данные

**Оптимизированные DAX меры:**
```dax
// Использование предрасчитанных данных из SQL
Total Revenue = SUM(sales_summary[total_amount])

// Эффективные временные вычисления
Revenue YoY Growth = 
DIVIDE(
    [Total Revenue] - [Total Revenue PY],
    [Total Revenue PY]
)

// Оптимизированные ранжирования
Top Products = 
CALCULATE(
    [Total Revenue],
    TOPN(10, VALUES(products[product_name]), [Total Revenue], DESC)
)
```

---

#### `powerbi_optimized_views.sql` — SQL представления для Power BI
**Описание:** Оптимизированные SQL представления, специально созданные для быстрой работы Power BI

**Представления для различных аналитических задач:**
```sql
-- Агрегированные данные продаж по времени
CREATE VIEW sales_time_analysis AS
SELECT 
    DATE(o.order_date) as order_date,
    EXTRACT(YEAR FROM o.order_date) as year,
    EXTRACT(MONTH FROM o.order_date) as month,
    p.category,
    COUNT(DISTINCT o.order_id) as orders_count,
    SUM(oi.quantity * oi.unit_price) as total_revenue,
    COUNT(DISTINCT o.customer_id) as unique_customers
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
WHERE o.status = 'completed'
GROUP BY DATE(o.order_date), EXTRACT(YEAR FROM o.order_date), 
         EXTRACT(MONTH FROM o.order_date), p.category;

-- Клиентская аналитика с RFM метриками
CREATE VIEW customer_rfm_analysis AS
SELECT 
    c.customer_id,
    c.customer_name,
    c.city,
    c.country,
    -- Recency (дни с последнего заказа)
    julianday('now') - julianday(MAX(o.order_date)) as recency_days,
    -- Frequency (количество заказов)
    COUNT(o.order_id) as frequency,
    -- Monetary (общая сумма заказов)
    SUM(o.total_amount) as monetary_value
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id AND o.status = 'completed'
GROUP BY c.customer_id, c.customer_name, c.city, c.country;
```

---

### 5️⃣ Файлы для сравнения производительности

#### `performance_comparison_template.xlsx` — Шаблон для записи результатов
**Описание:** Excel шаблон для систематической записи результатов тестирования производительности

**Структура шаблона:**
- **Лист "Baseline"** — результаты без оптимизаций
- **Лист "Optimized"** — результаты после оптимизации
- **Лист "Comparison"** — сравнение и расчет улучшений
- **Лист "Charts"** — графики производительности

**Метрики для записи:**
```
Запрос | Время до (мс) | Время после (мс) | Улучшение (%) | Тип оптимизации
-------|---------------|------------------|---------------|----------------
Query1 |     5,240     |       150        |    97.1%      | Added index
Query2 |     2,180     |       340        |    84.4%      | Rewrite JOIN
Query3 |     8,900     |       420        |    95.3%      | Covering index
```

---

#### `query_analysis_template.sql` — Шаблон для анализа запросов
**Описание:** Структурированный шаблон для анализа планов выполнения запросов

**Структура анализа:**
```sql
-- ============================================
-- АНАЛИЗ ЗАПРОСА: [Название/описание]
-- ============================================

-- 1. ИСХОДНЫЙ ЗАПРОС
[SQL запрос]

-- 2. ПЛАН ВЫПОЛНЕНИЯ (до оптимизации)
EXPLAIN QUERY PLAN [SQL запрос];
/*
Результат EXPLAIN:
- Операции сканирования
- Использование индексов  
- Стоимость операций
*/

-- 3. ВЫЯВЛЕННЫЕ ПРОБЛЕМЫ
/*
- Полное сканирование таблицы X
- Отсутствие индекса на столбце Y
- Неэффективный JOIN алгоритм
*/

-- 4. ПРИМЕНЯЕМЫЕ ОПТИМИЗАЦИИ
[SQL команды создания индексов или изменения запроса]

-- 5. ПЛАН ВЫПОЛНЕНИЯ (после оптимизации)
EXPLAIN QUERY PLAN [Оптимизированный SQL запрос];

-- 6. ИЗМЕРЕНИЕ УЛУЧШЕНИЯ
/*
Время до: X мс
Время после: Y мс  
Улучшение: Z%
*/
```

---

### 6️⃣ Мониторинг и алерты

#### `monitoring_schema.sql` — Схема таблиц для мониторинга
**Описание:** SQL скрипт для создания таблиц системы мониторинга производительности

**Создаваемые таблицы:**
```sql
-- Логи производительности запросов
CREATE TABLE query_performance_log (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    log_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    query_hash TEXT,                    -- Хэш запроса для группировки
    query_text TEXT,                    -- Текст запроса (обрезанный)
    execution_time_ms INTEGER,          -- Время выполнения в мс
    rows_examined INTEGER,              -- Количество просмотренных строк
    rows_returned INTEGER,              -- Количество возвращенных строк
    index_usage TEXT,                   -- Информация об использованных индексах
    plan_hash TEXT                      -- Хэш плана выполнения
);

-- Ежедневная статистика производительности
CREATE TABLE daily_performance_stats (
    stat_date DATE PRIMARY KEY,
    total_queries INTEGER,             -- Всего выполнено запросов
    avg_query_time_ms REAL,           -- Среднее время выполнения
    slow_queries_count INTEGER,        -- Количество медленных запросов
    cache_hit_ratio REAL,             -- Процент попаданий в кэш
    connections_count INTEGER,         -- Количество подключений
    db_size_mb REAL                   -- Размер БД в мегабайтах
);

-- Алерты о проблемах производительности
CREATE TABLE performance_alerts (
    alert_id INTEGER PRIMARY KEY AUTOINCREMENT,
    alert_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    alert_type TEXT,                   -- Тип алерта (SLOW_QUERY, HIGH_CPU, etc.)
    severity TEXT,                     -- Критичность (LOW, MEDIUM, HIGH, CRITICAL)
    description TEXT,                  -- Описание проблемы
    query_details TEXT,                -- Детали проблемного запроса
    is_resolved BOOLEAN DEFAULT FALSE, -- Статус решения
    resolution_notes TEXT             -- Комментарии по решению
);
```

---

#### `alert_system.py` — Система уведомлений о проблемах
**Описание:** Python модуль для отправки уведомлений о критических проблемах производительности

**Каналы уведомлений:**
```python
class AlertSystem:
    def send_email_alert(self, subject, message):
        """Отправка email уведомлений администраторам"""
    
    def send_telegram_alert(self, message):
        """Отправка уведомлений в Telegram бот"""
    
    def send_slack_alert(self, message, channel="#database-alerts"):
        """Отправка уведомлений в Slack канал"""
    
    def create_jira_ticket(self, title, description):
        """Создание тикета в JIRA для критических проблем"""
```

**Типы алертов:**
- **SLOW_QUERY** — запрос выполняется дольше порога
- **HIGH_CPU** — высокая загрузка процессора БД
- **DISK_SPACE** — заканчивается место на диске
- **CONNECTION_LIMIT** — превышен лимит подключений
- **DEADLOCK** — обнаружены взаимоблокировки

---

## 🔧 Инструкции по использованию

### 📝 Для практических заданий

**Задание 1: Анализ планов выполнения**
```bash
# Подключение к базе данных
sqlite3 files/ecommerce_performance.db

# Выполнение анализа
.read files/query_analysis_template.sql
```

**Задание 2: Тестирование индексов**
```bash
# Удаление существующих индексов
.read files/remove_indexes.sql

# Базовое тестирование
.timer on
.read files/slow_queries.sql

# Создание индексов
.read files/index_creation_script.sql

# Повторное тестирование
.read files/slow_queries.sql
```

**Задание 3: Оптимизация запросов**
```bash
# Применение решений
.read files/optimization_solutions.sql

# Сравнение производительности
python files/automated_benchmarking.py
```

### 🐍 Для Python интеграции

**Установка зависимостей:**
```bash
pip install sqlite3 pandas matplotlib seaborn requests schedule
```

**Запуск мониторинга:**
```bash
python files/performance_monitor.py
```

**Автоматическое обслуживание:**
```bash
python files/database_maintenance.py
```

### 🎨 Для работы с Power BI

**Настройка подключения:**
1. Откройте файл `files/ecommerce_dashboard.pbix`
2. Обновите подключение к базе данных
3. Импортируйте оптимизированные представления
4. Проверьте настройки модели данных

**Создание оптимизированных представлений:**
```bash
sqlite3 files/ecommerce_performance.db < files/powerbi_optimized_views.sql
```

---

## ⚠️ Важные замечания

### 📊 Особенности тестирования
- **Размер данных:** Тесты корректны для таблиц > 100,000 записей
- **Кэширование:** Очищайте кэш между тестами для точных замеров
- **Параллелизм:** Избегайте других операций с БД во время тестирования
- **Статистика:** Регулярно обновляйте статистики командой ANALYZE

### 🔄 Совместимость СУБД
- **SQLite:** Полная совместимость всех скриптов
- **PostgreSQL:** Замените специфичные функции SQLite
- **MySQL:** Адаптируйте синтаксис индексов и планов выполнения
- **SQL Server:** Используйте специфичные инструменты производительности

### 🛠️ Настройка мониторинга
- **Пороги алертов:** Настройте под ваши требования производительности
- **Частота проверок:** Балансируйте между точностью и нагрузкой на систему
- **Хранение логов:** Настройте ротацию для контроля размера
- **Уведомления:** Сконфигурируйте каналы связи для команды

---

## 📈 Ожидаемые результаты обучения

После работы с этими файлами вы:
- **Научитесь** анализировать и оптимизировать SQL-запросы
- **Освоите** создание эффективных индексов
- **Сможете** интегрировать оптимизацию SQL с Power BI
- **Получите** навыки мониторинга производительности БД
- **Поймете** принципы высокопроизводительных баз данных

---

📖 [Вернуться к теории](../README.md) | 📝 [Перейти к практике](../practice.md) | ✅ [Перейти к чек-листу](../checklist.md)

---

- 🔙 [Предыдущая глава: Глава 21: - Реляционные модели данных и индексы](../chapter-21/README.md)
- 🔜 [Следующая глава: Глава 23: Презентация результатов: storytelling, отчёты](../chapter-23/README.md)

---

- 📢 Присоединяйтесь к чату курса: https://t.me/analytics_course_chat
- 📢 Канал курса: https://t.me/analytics_course_channel