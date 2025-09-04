# 📝 Практические задания для главы 5

📖 [Вернуться к теории](../README.md) | 📁 [Учебные файлы](../files/README.md) | ✅ [Чек-лист](../checklist.md)

---

## 🔍 Задание 1: Подключение к различным источникам данных

**🎯 Цель:** Научиться подключаться к разным типам источников данных с помощью Power Query и понимать специфику каждого типа.

**📋 Описание:**  
Освойте подключение к основным типам источников данных, которые встречаются в корпоративной аналитике.

**🛠 Что нужно сделать:**

### 🔗 1. Создание подключений к файловым источникам:

**a) CSV файл с проблемами:**
1. Откройте Excel → **Данные** → **Получить данные** → **Из файла** → **Из текста/CSV**
2. Выберите файл [`files/messy_sales_data.csv`](files/messy_sales_data.csv)
3. В окне предварительного просмотра проанализируйте:
   - Корректность определения разделителей
   - Типы данных столбцов
   - Наличие заголовков
4. Нажмите **Преобразовать данные** для входа в редактор Power Query

**b) Excel файл с несколькими листами:**
1. Создайте новое подключение: **Данные** → **Получить данные** → **Из файла** → **Из книги Excel**
2. Выберите [`files/regional_data.xlsx`](files/regional_data.xlsx)
3. Изучите структуру файла — сколько листов, какие данные на каждом
4. Подключитесь ко всем листам и создайте навигатор по данным

**c) Текстовый файл с веб-логами:**
1. Подключитесь к [`files/web_data.txt`](files/web_data.txt) 
2. Настройте правильное разделение по столбцам (пробел как разделитель)
3. Создайте правильные заголовки: IP, Дата, Метод, URL, Статус, Размер, User_Agent

**d) Папка с множественными файлами:**
1. **Получить данные** → **Из папки** → выберите [`files/monthly_reports/`](files/monthly_reports/)
2. Объедините все файлы в одну таблицу
3. Добавьте столбец с именем исходного файла для идентификации источника
4. Убедитесь, что все файлы имеют одинаковую структуру

### 📊 2. Анализ подключенных источников:

Создайте сводную таблицу с информацией:
- Название источника
- Тип источника (CSV, Excel, TXT, Папка)  
- Количество записей
- Количество столбцов
- Выявленные проблемы качества данных
- Время последнего обновления

### 🔄 3. Настройка автоматического обновления:

Для каждого подключения:
1. Настройте **Свойства подключения**
2. Установите **"Обновлять при открытии файла"**
3. Установите периодичность обновления каждые 30 минут

**📊 Ожидаемый результат:**  
Excel-файл [`task1_data_connections.xlsx`] с подключениями ко всем источникам и анализом их характеристик.

---

## 🧹 Задание 2: Комплексная очистка и стандартизация данных

**🎯 Цель:** Освоить все основные техники очистки "грязных" данных и приведения их к аналитическому виду.

**📋 Описание:**  
Примените полный цикл очистки данных к реальному набору с типичными проблемами качества.

**🛠 Что нужно сделать:**

### 🔍 1. Анализ проблем в данных:

Откройте [`files/messy_sales_data.csv`](files/messy_sales_data.csv) в Power Query и задокументируйте найденные проблемы:

**Проблемы структуры:**
- [ ] Объединенные ячейки в заголовках
- [ ] Промежуточные итоги внутри данных  
- [ ] Пустые строки между записями
- [ ] Данные в неправильных столбцах

**Проблемы форматирования:**  
- [ ] Числа, сохраненные как текст (с пробелами, лишними символами)
- [ ] Разные форматы дат (ДД.ММ.ГГГГ, ММ/ДД/ГГГГ, текстом)
- [ ] Лишние пробелы в начале и конце текстовых значений
- [ ] Смешанный регистр в названиях (МОСКВА, москва, Москва)

**Проблемы качества:**
- [ ] Пропущенные значения в критических полях
- [ ] Полные дубликаты записей
- [ ] Выбросы в числовых данных (нереалистичные суммы)
- [ ] Противоречивые значения (отрицательные количества)

### 🛠 2. Пошаговая очистка данных:

**Шаг 1: Исправление структуры**
```m
// Пример кода Power Query (язык M)
let
    // Загрузка исходных данных
    Источник = Csv.Document(File.Contents("messy_sales_data.csv")),
    
    // Установка заголовков
    Заголовки = Table.PromoteHeaders(Источник, [PromoteAllScalars=true]),
    
    // Удаление пустых строк
    УдалениеПустых = Table.SelectRows(Заголовки, each not List.IsEmpty(List.RemoveMatchingItems(Record.FieldValues(_), {"", null})))
in
    УдалениеПустых
```

**Шаг 2: Стандартизация форматов**  
1. **Числовые поля:** уберите лишние символы, преобразуйте в числовой формат
2. **Даты:** приведите все к формату ДД.ММ.ГГГГ
3. **Текст:** удалите лишние пробелы, приведите к правильному регистру
4. **Суммы:** убедитесь, что все суммы положительные и в правильном формате

**Шаг 3: Обработка пропусков**
- **Количественные данные:** заполните медианными значениями по категориям  
- **Категориальные данные:** заполните модальными значениями
- **Даты:** используйте интерполяцию для временных рядов
- **Критические поля:** удалите строки с пропусками

**Шаг 4: Работа с дубликатами**
1. Определите ключевые поля для сравнения (дата, клиент, товар)
2. Найдите полные дубликаты и удалите их
3. Найдите частичные дубликаты и решите стратегию обработки

### 📋 3. Создание справочников соответствий:

**Справочник клиентов:**
```
Исходное название → Стандартное название
"ООО Ромашка" → "ООО «Ромашка»"  
"ромашка" → "ООО «Ромашка»"
"Romashka Ltd" → "ООО «Ромашка»"
```

**Справочник городов:**
```
"СПб" → "Санкт-Петербург"
"Moskva" → "Москва" 
"Н.Новгород" → "Нижний Новгород"
```

### 📊 4. Отчет о качестве данных:

Создайте сравнительный анализ **"до и после"** очистки:

| Метрика | До очистки | После очистки | Улучшение |
|---------|------------|---------------|-----------|
| Общее количество записей | | | |
| Записи с пропусками | | | |
| Дублированные записи | | | |
| Некорректные форматы дат | | | |
| Числа в текстовом формате | | | |
| Стандартизированные названия | | | |

**📊 Ожидаемый результат:**  
1. Очищенные данные: [`task2_cleaned_data.xlsx`]
2. Отчет о качестве: [`task2_data_quality_report.xlsx`]
3. Справочники соответствий: [`task2_reference_tables.xlsx`]

---

## 💾 Задание 3: Освоение основ SQL для аналитики

**🎯 Цель:** Научиться извлекать и анализировать данные из реляционной базы данных с помощью SQL-запросов.

**📋 Описание:**  
Работайте с учебной базой данных для решения типичных аналитических задач.

**🛠 Что нужно сделать:**

### 🗄 1. Подключение к базе данных:

**Подготовка данных:**
1. Используйте файлы CSV для создания таблиц:
   - [`files/sql_customers.csv`](files/sql_customers.csv) → таблица `customers`
   - [`files/sql_orders.csv`](files/sql_orders.csv) → таблица `orders`  
   - [`files/sql_products.csv`](files/sql_products.csv) → таблица `products`
   - [`files/sql_order_items.csv`](files/sql_order_items.csv) → таблица `order_items`

**Создание структуры БД:**
```sql
-- Создание таблицы клиентов
CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    city VARCHAR(50) NOT NULL,
    registration_date DATE NOT NULL
);

-- Создание таблицы товаров  
CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    price DECIMAL(10,2) NOT NULL
);

-- Создание таблицы заказов
CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(customer_id),
    order_date DATE NOT NULL,
    total_amount DECIMAL(12,2) NOT NULL
);

-- Создание таблицы позиций заказов
CREATE TABLE order_items (
    item_id INTEGER PRIMARY KEY,
    order_id INTEGER REFERENCES orders(order_id),
    product_id INTEGER REFERENCES products(product_id),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    price DECIMAL(10,2) NOT NULL
);
```

### 🔍 2. Базовые аналитические запросы:

**a) Простая фильтрация и сортировка:**
```sql
-- Задание 2.1: Все заказы за последние 6 месяцев 
SELECT order_id, customer_id, order_date, total_amount
FROM orders 
WHERE order_date >= '2023-07-01'
ORDER BY order_date DESC;

-- Задание 2.2: Клиенты из крупных городов
SELECT customer_name, city, registration_date
FROM customers 
WHERE city IN ('Москва', 'Санкт-Петербург', 'Новосибирск')
ORDER BY city, customer_name;

-- Задание 2.3: Топ-20 самых дорогих товаров
SELECT product_name, category, price
FROM products 
ORDER BY price DESC 
LIMIT 20;
```

**b) Агрегация и группировка:**
```sql
-- Задание 2.4: Количество заказов и выручка по месяцам
SELECT 
    EXTRACT(YEAR FROM order_date) AS год,
    EXTRACT(MONTH FROM order_date) AS месяц,
    COUNT(*) AS количество_заказов,
    SUM(total_amount) AS выручка,
    AVG(total_amount) AS средний_чек
FROM orders 
WHERE order_date >= '2023-01-01'
GROUP BY EXTRACT(YEAR FROM order_date), EXTRACT(MONTH FROM order_date)
ORDER BY год, месяц;

-- Задание 2.5: Распределение клиентов по городам  
SELECT 
    city AS город,
    COUNT(*) AS количество_клиентов,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM customers), 2) AS процент_от_общего
FROM customers 
GROUP BY city
ORDER BY количество_клиентов DESC;

-- Задание 2.6: Средняя цена по категориям товаров
SELECT 
    category AS категория,
    COUNT(*) AS количество_товаров,
    AVG(price) AS средняя_цена,
    MIN(price) AS минимальная_цена,
    MAX(price) AS максимальная_цена
FROM products 
GROUP BY category
ORDER BY средняя_цена DESC;
```

### 🔗 3. Запросы с объединением таблиц (JOIN):

```sql
-- Задание 3.1: Клиенты с их общей суммой покупок
SELECT 
    c.customer_name AS клиент,
    c.city AS город,
    COUNT(o.order_id) AS количество_заказов,
    COALESCE(SUM(o.total_amount), 0) AS общая_сумма,
    COALESCE(AVG(o.total_amount), 0) AS средний_чек
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.customer_name, c.city
ORDER BY общая_сумма DESC;

-- Задание 3.2: Детализация продаж по товарам
SELECT 
    p.product_name AS товар,
    p.category AS категория,
    SUM(oi.quantity) AS продано_штук,
    SUM(oi.quantity * oi.price) AS выручка_по_товару,
    COUNT(DISTINCT oi.order_id) AS заказов_с_товаром
FROM products p
JOIN order_items oi ON p.product_id = oi.product_id
GROUP BY p.product_id, p.product_name, p.category
ORDER BY выручка_по_товару DESC;

-- Задание 3.3: Товары, которые ни разу не покупали
SELECT 
    product_name AS непопулярный_товар,
    category AS категория,
    price AS цена
FROM products 
WHERE product_id NOT IN (
    SELECT DISTINCT product_id 
    FROM order_items
)
ORDER BY price DESC;
```

### 📊 4. Продвинутые аналитические запросы:

```sql
-- Задание 4.1: RFM анализ клиентов
WITH customer_rfm AS (
    SELECT 
        c.customer_id,
        c.customer_name,
        c.city,
        MAX(o.order_date) AS последний_заказ,
        COUNT(o.order_id) AS частота_заказов,
        SUM(o.total_amount) AS денежная_стоимость
    FROM customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.customer_name, c.city
)
SELECT *,
    CURRENT_DATE - последний_заказ AS дней_с_последнего_заказа,
    CASE 
        WHEN частота_заказов >= 5 THEN 'Высокая'
        WHEN частота_заказов >= 2 THEN 'Средняя'
        ELSE 'Низкая'
    END AS сегмент_частоты,
    CASE 
        WHEN денежная_стоимость >= 50000 THEN 'VIP'
        WHEN денежная_стоимость >= 15000 THEN 'Постоянный'
        WHEN денежная_стоимость > 0 THEN 'Обычный'
        ELSE 'Неактивный'
    END AS сегмент_ценности
FROM customer_rfm
ORDER BY денежная_стоимость DESC;

-- Задание 4.2: Когортный анализ по месяцам регистрации
SELECT 
    DATE_TRUNC('month', c.registration_date) AS когорта_регистрации,
    DATE_TRUNC('month', o.order_date) AS месяц_заказа,
    COUNT(DISTINCT c.customer_id) AS активных_клиентов,
    SUM(o.total_amount) AS выручка_когорты
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY DATE_TRUNC('month', c.registration_date), DATE_TRUNC('month', o.order_date)
ORDER BY когорта_регистрации, месяц_заказа;
```

### 📋 5. Создание представлений (Views):

```sql
-- Представление: Сводка по клиентам
CREATE VIEW customer_summary AS
SELECT 
    c.customer_id,
    c.customer_name,
    c.city,
    c.registration_date,
    COUNT(o.order_id) AS total_orders,
    COALESCE(SUM(o.total_amount), 0) AS total_spent,
    COALESCE(AVG(o.total_amount), 0) AS avg_order_value,
    MAX(o.order_date) AS last_order_date
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.customer_name, c.city, c.registration_date;

-- Представление: Ежемесячные продажи  
CREATE VIEW monthly_sales AS
SELECT 
    EXTRACT(YEAR FROM order_date) AS year,
    EXTRACT(MONTH FROM order_date) AS month,
    COUNT(*) AS order_count,
    SUM(total_amount) AS revenue,
    AVG(total_amount) AS avg_order_value,
    COUNT(DISTINCT customer_id) AS unique_customers
FROM orders
GROUP BY EXTRACT(YEAR FROM order_date), EXTRACT(MONTH FROM order_date);
```

**📊 Ожидаемый результат:**  
1. Файл с SQL запросами: [`task3_sql_queries.sql`]  
2. Результаты анализов в Excel: [`task3_sql_analysis.xlsx`]
3. Документация по созданным представлениям: [`task3_views_documentation.md`]

---

## 🔄 Задание 4: Автоматизация и мониторинг данных

**🎯 Цель:** Создать систему автоматического обновления данных с контролем качества и мониторингом ошибок.

**📋 Описание:**  
Настройте полностью автоматизированный процесс работы с данными от загрузки до контроля качества.

**🛠 Что нужно сделать:**

### ⚙️ 1. Создание автоматизированного ETL процесса:

**VBA макрос для автообновления:**
```vba
Sub AutoRefreshAllData()
'
' Автоматическое обновление всех подключений к данным
' Выполняется при открытии файла и по расписанию
'
    Dim conn As WorkbookConnection
    Dim startTime As Date
    Dim endTime As Date
    Dim duration As Double
    Dim errorCount As Integer
    
    ' Логирование начала процесса
    startTime = Now()
    Call LogRefreshEvent("INFO", "Начало автообновления данных", startTime)
    
    ' Отключение обновления экрана для ускорения
    Application.ScreenUpdating = False
    Application.DisplayAlerts = False
    
    On Error GoTo ErrorHandler
    
    ' Цикл обновления всех подключений
    For Each conn In ThisWorkbook.Connections
        DoEvents ' Позволяет прервать выполнение
        
        Select Case conn.Type
            Case xlConnectionTypeOLEDB, xlConnectionTypeODBC
                ' Обновление подключений к БД
                conn.Refresh
                Call LogRefreshEvent("SUCCESS", "Обновлено: " & conn.Name, Now())
                
            Case xlConnectionTypeWEB  
                ' Обновление веб-источников
                conn.Refresh
                Call LogRefreshEvent("SUCCESS", "Обновлен веб-источник: " & conn.Name, Now())
                
            Case Else
                ' Обновление файловых источников  
                conn.Refresh
                Call LogRefreshEvent("SUCCESS", "Обновлен файл: " & conn.Name, Now())
        End Select
        
    Next conn
    
    ' Запуск проверки качества данных
    Call DataQualityCheck
    
    ' Завершение процесса
    endTime = Now()
    duration = DateDiff("s", startTime, endTime)
    
    Application.ScreenUpdating = True
    Application.DisplayAlerts = True
    
    MsgBox "Обновление данных завершено!" & vbCrLf & _
           "Время выполнения: " & duration & " секунд" & vbCrLf & _
           "Обновлено подключений: " & ThisWorkbook.Connections.Count, _
           vbInformation, "Автообновление данных"
    
    Call LogRefreshEvent("INFO", "Автообновление завершено. Время: " & duration & "с", endTime)
    
    Exit Sub
    
ErrorHandler:
    errorCount = errorCount + 1
    Call LogRefreshEvent("ERROR", "Ошибка: " & Err.Description & " в " & conn.Name, Now())
    
    If errorCount < 3 Then
        Resume Next ' Продолжить со следующим подключением
    Else
        MsgBox "Критическое количество ошибок! Процесс остановлен.", vbCritical
        Call SendEmailAlert("Критические ошибки при обновлении данных")
        End
    End If
End Sub
```

**Функция логирования событий:**
```vba
Sub LogRefreshEvent(logLevel As String, message As String, timestamp As Date)
    Dim wsLog As Worksheet
    Dim lastRow As Long
    
    ' Создание листа логов если не существует
    On Error Resume Next
    Set wsLog = ThisWorkbook.Worksheets("RefreshLog")
    On Error GoTo 0
    
    If wsLog Is Nothing Then
        Set wsLog = ThisWorkbook.Worksheets.Add
        wsLog.Name = "RefreshLog"
        
        ' Создание заголовков
        wsLog.Cells(1, 1).Value = "Timestamp"
        wsLog.Cells(1, 2).Value = "Level"  
        wsLog.Cells(1, 3).Value = "Message"
        wsLog.Cells(1, 4).Value = "User"
    End If
    
    ' Добавление новой записи в лог
    lastRow = wsLog.Cells(wsLog.Rows.Count, 1).End(xlUp).Row + 1
    wsLog.Cells(lastRow, 1).Value = timestamp
    wsLog.Cells(lastRow, 2).Value = logLevel
    wsLog.Cells(lastRow, 3).Value = message  
    wsLog.Cells(lastRow, 4).Value = Application.UserName
    
    ' Форматирование по уровню важности
    Select Case logLevel
        Case "ERROR"
            wsLog.Rows(lastRow).Interior.Color = RGB(255, 200, 200)
        Case "WARNING"  
            wsLog.Rows(lastRow).Interior.Color = RGB(255, 255, 200)
        Case "SUCCESS"
            wsLog.Rows(lastRow).Interior.Color = RGB(200, 255, 200)
    End Select
End Sub
```

### 🔍 2. Система контроля качества данных:

**Функция проверки качества:**
```vba
Sub DataQualityCheck()
'
' Комплексная проверка качества данных после обновления
'
    Dim wsData As Worksheet
    Dim wsQuality As Worksheet
    Dim lastRow As Long
    Dim totalRecords As Long
    Dim missingValues As Long
    Dim duplicates As Long
    
    Set wsData = ThisWorkbook.Worksheets("CleanedData") 
    
    ' Создание листа контроля качества
    On Error Resume Next
    Set wsQuality = ThisWorkbook.Worksheets("DataQuality")
    On Error GoTo 0
    
    If wsQuality Is Nothing Then
        Set wsQuality = ThisWorkbook.Worksheets.Add
        wsQuality.Name = "DataQuality"
        Call CreateQualityDashboard(wsQuality)
    End If
    
    ' Подсчет основных метрик
    lastRow = wsData.Cells(wsData.Rows.Count, 1).End(xlUp).Row
    totalRecords = lastRow - 1 ' Исключаем заголовок
    
    ' Проверка 1: Общее количество записей
    wsQuality.Cells(2, 2).Value = totalRecords
    wsQuality.Cells(2, 3).Value = Now() ' Время проверки
    
    ' Проверка 2: Критические пропуски (в поле "Сумма")
    missingValues = Application.CountBlank(wsData.Range("E2:E" & lastRow))
    wsQuality.Cells(3, 2).Value = missingValues
    wsQuality.Cells(3, 3).Value = Round(missingValues / totalRecords * 100, 2) & "%"
    
    ' Проверка 3: Дубликаты (по комбинации дата+клиент)
    duplicates = CountDuplicates(wsData, "A2:B" & lastRow)
    wsQuality.Cells(4, 2).Value = duplicates
    
    ' Проверка 4: Аномальные значения (выбросы в суммах)
    Dim anomalies As Long
    anomalies = CountAnomalies(wsData, "E2:E" & lastRow)
    wsQuality.Cells(5, 2).Value = anomalies
    
    ' Проверка 5: Актуальность данных (последняя дата)
    Dim maxDate As Date
    maxDate = Application.Max(wsData.Range("A2:A" & lastRow))
    wsQuality.Cells(6, 2).Value = maxDate
    wsQuality.Cells(6, 3).Value = Date - maxDate & " дн. назад"
    
    ' Общая оценка качества данных
    Dim qualityScore As Integer
    qualityScore = CalculateQualityScore(totalRecords, missingValues, duplicates, anomalies)
    wsQuality.Cells(8, 2).Value = qualityScore & "%"
    
    ' Цветовая индикация статуса
    If qualityScore >= 90 Then
        wsQuality.Cells(8, 2).Interior.Color = RGB(0, 255, 0) ' Зеленый
        wsQuality.Cells(8, 3).Value = "ОТЛИЧНО"
    ElseIf qualityScore >= 75 Then
        wsQuality.Cells(8, 2).Interior.Color = RGB(255, 255, 0) ' Желтый  
        wsQuality.Cells(8, 3).Value = "ХОРОШО"
    Else
        wsQuality.Cells(8, 2).Interior.Color = RGB(255, 0, 0) ' Красный
        wsQuality.Cells(8, 3).Value = "ТРЕБУЕТ ВНИМАНИЯ"
        
        ' Отправка уведомления при низком качестве
        Call SendEmailAlert("Низкое качество данных: " & qualityScore & "%")
    End If
    
    Call LogRefreshEvent("INFO", "Проверка качества завершена. Оценка: " & qualityScore & "%", Now())
End Sub
```

### 📊 3. Создание дашборда мониторинга:

**Дашборд контроля качества данных:**

| Метрика | Значение | Статус | Обновлено |
|---------|----------|---------|-----------|
| **Общее количество записей** | =CountA(CleanedData!A:A)-1 | ✅ | =NOW() |
| **Пропуски в ключевых полях** | =COUNTBLANK(CleanedData!E:E) | ⚠️ | =NOW() |
| **Дублированные записи** | =COUNTIF(...) | ✅ | =NOW() |  
| **Аномальные значения** | =COUNTIFS(...) | ⚠️ | =NOW() |
| **Последняя дата данных** | =MAX(CleanedData!A:A) | ✅ | =NOW() |
| **Время последнего обновления** | =RefreshLog!A2 | ✅ | =NOW() |
| **Общая оценка качества** | **85%** | **🟡 ХОРОШО** | =NOW() |

**Визуальные индикаторы:**
- 🟢 **90-100%** — Данные в отличном состоянии
- 🟡 **75-89%** — Данные в хорошем состоянии, есть незначительные проблемы
- 🔴 **<75%** — Критические проблемы, требуется вмешательство

### 📧 4. Настройка уведомлений:

**Функция отправки email-уведомлений:**
```vba
Sub SendEmailAlert(alertMessage As String)
'
' Отправка email-уведомлений при критических ошибках
'
    Dim OutlookApp As Object
    Dim OutlookMail As Object
    
    Set OutlookApp = CreateObject("Outlook.Application")
    Set OutlookMail = OutlookApp.CreateItem(0)
    
    With OutlookMail
        .To = "admin@company.com;analyst@company.com"
        .Subject = "АЛЕРТ: Система мониторинга данных - " & Format(Now(), "DD.MM.YYYY HH:MM")
        .Body = "Обнаружена проблема в системе данных:" & vbCrLf & vbCrLf & _
                "Сообщение: " & alertMessage & vbCrLf & _
                "Время: " & Format(Now(), "DD.MM.YYYY HH:MM:SS") & vbCrLf & _
                "Пользователь: " & Application.UserName & vbCrLf & _
                "Файл: " & ThisWorkbook.FullName & vbCrLf & vbCrLf & _
                "Пожалуйста, проверьте систему данных." & vbCrLf & vbCrLf & _
                "Автоматически сгенерировано системой мониторинга данных."
        .Send
    End With
    
    Set OutlookMail = Nothing
    Set OutlookApp = Nothing
    
    Call LogRefreshEvent("INFO", "Отправлено email-уведомление: " & alertMessage, Now())
End Sub
```

### ⏰ 5. Настройка расписания:

**Автоматический запуск при открытии файла:**
```vba
Private Sub Workbook_Open()
'
' Автоматический запуск при открытии файла
'
    ' Проверяем, прошло ли достаточно времени с последнего обновления
    Dim lastRefresh As Date
    Dim hoursElapsed As Double
    
    On Error Resume Next
    lastRefresh = ThisWorkbook.Worksheets("RefreshLog").Cells(2, 1).Value
    On Error GoTo 0
    
    hoursElapsed = (Now() - lastRefresh) * 24
    
    ' Если прошло более 2 часов, запускаем автообновление
    If hoursElapsed > 2 Or lastRefresh = 0 Then
        MsgBox "Данные устарели. Запускается автоматическое обновление...", vbInformation
        Call AutoRefreshAllData
    Else
        MsgBox "Данные актуальны. Последнее обновление: " & Format(lastRefresh, "DD.MM.YYYY HH:MM"), vbInformation
    End If
End Sub
```

**📊 Ожидаемый результат:**  
Полностью автоматизированная система: [`task4_automated_data_system.xlsx`] включающая:
1. Автоматическое обновление всех источников данных
2. Систему логирования и мониторинга ошибок  
3. Дашборд контроля качества данных с цветовыми индикаторами
4. Email-уведомления при критических проблемах
5. Документацию по настройке и использованию системы

---

## 🏗 Задание 5: Создание корпоративной витрины данных

**🎯 Цель:** Спроектировать и реализовать полноценную витрину данных (Data Mart) для корпоративной аналитики с многоуровневой архитектурой.

**📋 Описание:**  
Объедините все источники данных в единую систему с правильной архитектурой, моделью данных и аналитическими возможностями.

**🛠 Что нужно сделать:**

### 🎯 1. Проектирование архитектуры витрины данных:

**Концептуальная модель:**
```
📊 ИСТОЧНИКИ ДАННЫХ
├── Файлы продаж (месячные отчеты)
├── Справочники (клиенты, товары)  
├── Веб-логи (активность пользователей)
└── База данных (заказы, транзакции)

🔄 ETL ПРОЦЕССЫ
├── Извлечение (Extract)
├── Трансформация (Transform)  
└── Загрузка (Load)

🏗 СЛОИ ДАННЫХ  
├── Raw Layer (сырые данные)
├── Clean Layer (очищенные данные)
└── Analytics Layer (витрины данных)

📈 АНАЛИТИЧЕСКИЕ ВИТРИНЫ
├── Витрина продаж
├── Витрина клиентов
├── Витрина товаров  
└── Витрина веб-активности
```

### 📊 2. Создание слоя сырых данных (Raw Layer):

**Структура Raw Layer:**
```
raw_data/
├── sales/
│   ├── raw_monthly_sales_202301.csv
│   ├── raw_monthly_sales_202302.csv  
│   └── raw_monthly_sales_202303.csv
├── customers/
│   └── raw_customers_master.csv
├── products/  
│   └── raw_products_catalog.csv
└── web_logs/
    └── raw_web_activity.csv
```

**Power Query для Raw Layer:**
```m
let
    // Функция загрузки сырых данных с метаданными
    LoadRawData = (SourcePath as text, SourceType as text) =>
    let
        RawSource = Csv.Document(File.Contents(SourcePath)),
        
        // Добавление метаданных
        WithMetadata = Table.AddColumn(RawSource, "load_timestamp", each DateTime.LocalNow()),
        WithSource = Table.AddColumn(WithMetadata, "source_file", each SourcePath),
        WithType = Table.AddColumn(WithSource, "source_type", each SourceType),
        WithChecksum = Table.AddColumn(WithType, "data_checksum", each Text.From(Binary.ToText(Binary.FromText(Text.Combine(Record.FieldValues(_), "|")))))
    in
        WithChecksum,
        
    // Загрузка всех месячных отчетов
    MonthlySales = Folder.Files("files/monthly_reports/"),
    ProcessedSales = Table.AddColumn(MonthlySales, "Data", each LoadRawData([Folder Path] & [Name], "monthly_sales")),
    
    // Объединение всех данных
    ExpandedSales = Table.ExpandTableColumn(ProcessedSales, "Data", {"Column1", "Column2", "Column3", "Column4", "Column5", "load_timestamp", "source_file", "source_type", "data_checksum"})
in
    ExpandedSales
```

### 🧹 3. Создание слоя очищенных данных (Clean Layer):

**Стандартизированная схема данных:**

**Таблица: clean_sales**
```sql
CREATE TABLE clean_sales (
    sale_id SERIAL PRIMARY KEY,
    sale_date DATE NOT NULL,
    customer_name VARCHAR(200) NOT NULL,
    product_name VARCHAR(200) NOT NULL,  
    quantity INTEGER CHECK (quantity > 0),
    unit_price DECIMAL(10,2) CHECK (unit_price > 0),
    total_amount DECIMAL(12,2),
    currency_code CHAR(3) DEFAULT 'RUB',
    source_file VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Таблица: clean_customers**
```sql
CREATE TABLE clean_customers (
    customer_id SERIAL PRIMARY KEY,
    customer_name VARCHAR(200) NOT NULL,
    customer_name_standard VARCHAR(200), -- стандартизированное название
    city VARCHAR(100) NOT NULL,
    city_standard VARCHAR(100), -- стандартизированный город
    registration_date DATE,
    customer_type VARCHAR(50), -- B2B, B2C
    inn VARCHAR(12), -- для юридических лиц
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Power Query для очистки данных:**
```m
let
    // Загрузка сырых данных продаж
    RawSales = Excel.CurrentWorkbook(){[Name="raw_monthly_sales"]}[Content],
    
    // Шаг 1: Установка правильных заголовков
    PromotedHeaders = Table.PromoteHeaders(RawSales, [PromoteAllScalars=true]),
    
    // Шаг 2: Удаление пустых строк
    FilteredRows = Table.SelectRows(PromotedHeaders, each not List.IsEmpty(List.RemoveMatchingItems(Record.FieldValues(_), {"", null}))),
    
    // Шаг 3: Стандартизация типов данных
    ChangedType = Table.TransformColumnTypes(FilteredRows,{
        {"Дата", type date}, 
        {"Товар", type text}, 
        {"Количество", Int64.Type}, 
        {"Цена", type number}, 
        {"Сумма", type number}
    }),
    
    // Шаг 4: Очистка текстовых полей
    CleanedText = Table.TransformColumns(ChangedType,{
        {"Товар", Text.Trim, type text}
    }),
    
    // Шаг 5: Стандартизация названий товаров
    StandardizedProducts = Table.ReplaceValue(CleanedText,"Товар А","Товар Alpha",Replacer.ReplaceText,{"Товар"}),
    
    // Шаг 6: Добавление вычисляемых полей
    WithCalculated = Table.AddColumn(StandardizedProducts, "Проверка суммы", 
        each if [Количество] * [Цена] <> [Сумма] then "ОШИБКА" else "ОК"),
    
    // Шаг 7: Фильтрация корректных записей
    ValidRecords = Table.SelectRows(WithCalculated, each [Проверка суммы] = "ОК"),
    
    // Шаг 8: Добавление метаданных очистки
    WithCleaningInfo = Table.AddColumn(ValidRecords, "cleaned_at", each DateTime.LocalNow())
in
    WithCleaningInfo
```

### 📊 4. Создание аналитических витрин (Analytics Layer):

**Витрина продаж по периодам:**
```sql
CREATE VIEW sales_analytics AS
SELECT 
    DATE_TRUNC('month', sale_date) AS period_month,
    DATE_TRUNC('quarter', sale_date) AS period_quarter,
    DATE_TRUNC('year', sale_date) AS period_year,
    
    -- Объемные показатели
    COUNT(*) AS transactions_count,
    SUM(quantity) AS total_quantity,
    SUM(total_amount) AS total_revenue,
    
    -- Средние показатели  
    AVG(total_amount) AS avg_transaction_amount,
    AVG(quantity) AS avg_quantity_per_transaction,
    
    -- Уникальные объекты
    COUNT(DISTINCT customer_name) AS unique_customers,
    COUNT(DISTINCT product_name) AS unique_products,
    
    -- Метрики качества
    MIN(sale_date) AS period_start,
    MAX(sale_date) AS period_end,
    COUNT(*) FILTER (WHERE total_amount > 0) AS valid_transactions
    
FROM clean_sales 
GROUP BY 
    DATE_TRUNC('month', sale_date),
    DATE_TRUNC('quarter', sale_date), 
    DATE_TRUNC('year', sale_date);
```

**Витрина клиентской аналитики (RFM):**
```sql
CREATE VIEW customer_rfm_analysis AS
WITH customer_metrics AS (
    SELECT 
        customer_name,
        COUNT(*) AS frequency, -- Frequency: количество покупок
        SUM(total_amount) AS monetary, -- Monetary: общая сумма покупок  
        MAX(sale_date) AS last_purchase_date,
        MIN(sale_date) AS first_purchase_date,
        
        -- Дополнительные метрики
        AVG(total_amount) AS avg_purchase_amount,
        STDDEV(total_amount) AS purchase_amount_variance,
        
        -- Временные метрики
        EXTRACT(DAYS FROM (MAX(sale_date) - MIN(sale_date))) AS customer_lifetime_days
        
    FROM clean_sales
    GROUP BY customer_name
),
rfm_scores AS (
    SELECT *,
        -- Recency Score (дни с последней покупки)
        CURRENT_DATE - last_purchase_date AS recency_days,
        
        -- Подсчет процентилей для RFM сегментации
        NTILE(5) OVER (ORDER BY CURRENT_DATE - last_purchase_date DESC) AS recency_score,
        NTILE(5) OVER (ORDER BY frequency) AS frequency_score,  
        NTILE(5) OVER (ORDER BY monetary) AS monetary_score
        
    FROM customer_metrics
)
SELECT *,
    -- Создание RFM сегментов
    CASE 
        WHEN recency_score >= 4 AND frequency_score >= 4 AND monetary_score >= 4 THEN 'VIP Champions'
        WHEN recency_score >= 3 AND frequency_score >= 3 AND monetary_score >= 3 THEN 'Loyal Customers'  
        WHEN recency_score >= 4 AND frequency_score <= 2 THEN 'New Customers'
        WHEN recency_score <= 2 AND frequency_score >= 3 THEN 'At Risk'
        WHEN recency_score <= 2 AND frequency_score <= 2 THEN 'Lost Customers'
        ELSE 'Regular Customers'
    END AS rfm_segment,
    
    -- Рекомендации по работе с сегментом  
    CASE 
        WHEN recency_score >= 4 AND frequency_score >= 4 THEN 'Reward loyalty, upsell premium products'
        WHEN recency_score >= 4 AND frequency_score <= 2 THEN 'Welcome campaign, onboarding'
        WHEN recency_score <= 2 AND frequency_score >= 3 THEN 'Win-back campaign, special offers'
        WHEN recency_score <= 2 AND frequency_score <= 2 THEN 'Re-engagement campaign'
        ELSE 'Standard marketing approach'
    END AS marketing_recommendation

FROM rfm_scores;
```

### 📈 5. Создание Power Pivot модели данных:

**Схема связей в Power Pivot:**
```
dim_time (календарная таблица)
├── date_key → fact_sales.sale_date
├── year, quarter, month, day
└── is_weekend, is_holiday

dim_customers (справочник клиентов)  
├── customer_key → fact_sales.customer_key
├── customer_name, city, segment
└── registration_date, customer_type

dim_products (справочник товаров)
├── product_key → fact_sales.product_key  
├── product_name, category
└── unit_price, is_active

fact_sales (факты продаж)
├── sale_date → dim_time.date_key
├── customer_key → dim_customers.customer_key
├── product_key → dim_products.product_key
└── quantity, amount, unit_price
```

**DAX меры для аналитики:**
```dax
// Базовые меры продаж
Total Revenue = SUM(fact_sales[total_amount])

Total Transactions = COUNT(fact_sales[sale_id])

Average Transaction Value = 
DIVIDE([Total Revenue], [Total Transactions], 0)

// Меры сравнения с предыдущим периодом
Revenue Previous Month = 
CALCULATE(
    [Total Revenue],
    DATEADD(dim_time[date_key], -1, MONTH)
)

Revenue Growth % = 
DIVIDE(
    [Total Revenue] - [Revenue Previous Month], 
    [Revenue Previous Month], 
    0
) * 100

// Меры для анализа клиентов  
Unique Customers = DISTINCTCOUNT(fact_sales[customer_key])

New Customers = 
CALCULATE(
    DISTINCTCOUNT(fact_sales[customer_key]),
    FILTER(
        dim_customers,
        dim_customers[registration_date] >= STARTOFMONTH(TODAY())
    )
)

Customer Retention Rate % = 
VAR CustomersLastMonth = 
    CALCULATE(
        DISTINCTCOUNT(fact_sales[customer_key]),
        DATEADD(dim_time[date_key], -1, MONTH)
    )
VAR ReturningCustomers = 
    CALCULATE(
        DISTINCTCOUNT(fact_sales[customer_key]),
        FILTER(
            fact_sales,
            fact_sales[customer_key] IN 
            CALCULATETABLE(
                VALUES(fact_sales[customer_key]),
                DATEADD(dim_time[date_key], -1, MONTH)
            )
        )
    )
RETURN
DIVIDE(ReturningCustomers, CustomersLastMonth, 0) * 100

// Меры для товарного анализа
Top Products by Revenue = 
RANKX(
    ALL(dim_products[product_name]),
    [Total Revenue],
    ,
    DESC
)

Product Performance Score = 
VAR ProductRevenue = [Total Revenue]
VAR AverageProductRevenue = 
    CALCULATE(
        AVERAGE(fact_sales[total_amount]),
        ALL(dim_products)
    )
RETURN
DIVIDE(ProductRevenue, AverageProductRevenue, 0)
```

### 📊 6. Создание интерактивного дашборда:

**Главный дашборд KPI:**

| 📊 **КЛЮЧЕВЫЕ ПОКАЗАТЕЛИ** | **ТЕКУЩИЙ МЕСЯЦ** | **ИЗМЕНЕНИЕ** |
|---|---|---|
| 💰 Общая выручка | =FORMAT([Total Revenue],"# ### ### ₽") | =IF([Revenue Growth %]>0,"↗ ","↘ ") & FORMAT([Revenue Growth %],"0.0%") |
| 🛒 Количество транзакций | =[Total Transactions] | =IF([Transaction Growth %]>0,"↗ ","↘ ") & [Transaction Growth %] |
| 💳 Средний чек | =FORMAT([Average Transaction Value],"# ### ₽") | =FORMAT([ATV Growth %],"0.0%") |
| 👥 Уникальные клиенты | =[Unique Customers] | =FORMAT([Customer Growth %],"0.0%") |
| 🔄 Retention Rate | =FORMAT([Customer Retention Rate %],"0.0%") | =FORMAT([Retention Change],"0.0 п.п.") |

**Срезы и фильтры:**
- 📅 **Период**: Выбор месяца, квартала, года
- 🏙 **Город**: Фильтр по географии  
- 📦 **Категория товаров**: Группировка по товарным категориям
- 👤 **Сегмент клиентов**: RFM сегменты, B2B/B2C
- 💼 **Тип транзакции**: Новые/повторные покупки

**Детализация (Drill-Down):**
```
Год → Квартал → Месяц → День
Регион → Город → Район  
Категория → Товар → SKU
Сегмент клиентов → Клиент → Транзакция
```

### 📚 7. Документация витрины данных:

**Каталог данных (Data Catalog):**

| **Таблица** | **Описание** | **Источник** | **Частота обновления** | **Ответственный** |
|-------------|-------------|-------------|----------------------|------------------|
| **dim_time** | Календарная таблица с атрибутами времени | Автогенерация | При необходимости | IT отдел |
| **dim_customers** | Справочник клиентов с атрибутами | CRM система + файлы | Ежедневно | Отдел продаж |
| **dim_products** | Справочник товаров и услуг | Система управления товарами | Еженедельно | Товарный отдел |  
| **fact_sales** | Транзакции продаж | Учетная система + файлы | Ежедневно | Финансовый отдел |
| **web_activity** | Активность на веб-сайте | Веб-аналитика | В реальном времени | IT отдел |

**Словарь бизнес-терминов:**

| **Термин** | **Определение** | **Формула расчета** |
|------------|-----------------|-------------------|
| **Выручка** | Общая сумма продаж за период | SUM(quantity × unit_price) |
| **Средний чек** | Средняя сумма одной транзакции | Общая выручка ÷ Количество транзакций |
| **ARPU** | Average Revenue Per User | Общая выручка ÷ Количество уникальных клиентов |
| **LTV** | Life Time Value клиента | Средний чек × Частота покупок × Срок жизни клиента |
| **Retention Rate** | Доля вернувшихся клиентов | Клиенты текущего периода ∩ Клиенты предыдущего ÷ Клиенты предыдущего |

### 🔄 8. Процедуры обслуживания:

**Ежедневные процедуры:**
```sql
-- Процедура ежедневного обновления витрин
CREATE OR REPLACE PROCEDURE daily_data_refresh()
LANGUAGE plpgsql AS $$
BEGIN
    -- 1. Загрузка новых данных в Raw Layer
    INSERT INTO raw_sales_staging 
    SELECT * FROM external_sales_feed 
    WHERE load_date = CURRENT_DATE;
    
    -- 2. Очистка и валидация данных
    INSERT INTO clean_sales
    SELECT 
        sale_date,
        TRIM(UPPER(customer_name)) AS customer_name,
        TRIM(product_name) AS product_name,
        quantity,
        unit_price,
        quantity * unit_price AS total_amount
    FROM raw_sales_staging 
    WHERE quantity > 0 AND unit_price > 0;
    
    -- 3. Обновление агрегированных витрин
    REFRESH MATERIALIZED VIEW sales_analytics;
    REFRESH MATERIALIZED VIEW customer_rfm_analysis;
    
    -- 4. Обновление статистики для оптимизатора
    ANALYZE clean_sales;
    ANALYZE dim_customers;
    
    -- 5. Архивирование старых данных (>2 лет)
    DELETE FROM raw_sales_staging 
    WHERE load_date < CURRENT_DATE - INTERVAL '730 days';
    
    -- 6. Логирование результата
    INSERT INTO etl_log (process_name, status, records_processed, execution_time)
    VALUES ('daily_refresh', 'SUCCESS', ROW_COUNT, NOW());
    
EXCEPTION
    WHEN OTHERS THEN
        INSERT INTO etl_log (process_name, status, error_message, execution_time)
        VALUES ('daily_refresh', 'ERROR', SQLERRM, NOW());
        RAISE;
END;
$$;
```

**📊 Ожидаемый результат:**  
Полноценная корпоративная витрина данных: [`task5_enterprise_data_mart.xlsx`] включающая:

1. **Архитектурную документацию** — схемы данных, процессов ETL
2. **Многослойную модель данных** — Raw/Clean/Analytics layers  
3. **Power Pivot модель** с правильными связями и DAX мерами
4. **Интерактивный дашборд** с KPI, срезами и drill-down возможностями
5. **Каталог данных** с описанием всех таблиц и метрик
6. **Процедуры обслуживания** для поддержания витрины в актуальном состоянии
7. **Руководство пользователя** по работе с витриной данных

---

## 💡 Методические рекомендации по выполнению заданий

### 🔧 **Работа с Power Query:**

**Лучшие практики:**
- **Планируйте трансформации** — продумайте последовательность операций заранее  
- **Используйте описательные названия шагов** — "Удаление пустых строк", "Стандартизация дат"
- **Тестируйте на образцах** — проверяйте логику на 100-1000 записях
- **Создавайте параметры** — для путей к файлам, дат, пороговых значений
- **Документируйте сложные формулы** — добавляйте комментарии в M коде

**Типичные ошибки:**
- ❌ Изменение исходных файлов — всегда работайте с копиями
- ❌ Игнорирование ошибок трансформации — исследуйте причины
- ❌ Слишком много операций за раз — разбивайте на логические этапы
- ❌ Отсутствие контроля качества — проверяйте результаты на каждом шаге

### 💾 **SQL для аналитиков:**

**Подход к написанию запросов:**
1. **Начинайте с простого** — базовый SELECT без JOIN и агрегации  
2. **Изучайте схему данных** — понимайте связи между таблицами
3. **Используйте алиасы** — краткие, понятные названия для таблиц и полей
4. **Форматируйте код** — отступы, переносы строк для читаемости
5. **Тестируйте по частям** — проверяйте каждый JOIN и фильтр отдельно

**Оптимизация производительности:**
```sql
-- ✅ Хорошо: фильтрация до JOIN
SELECT c.customer_name, SUM(o.total_amount)
FROM customers c
JOIN (
    SELECT customer_id, total_amount 
    FROM orders 
    WHERE order_date >= '2023-01-01'  -- фильтр до JOIN
) o ON c.customer_id = o.customer_id
GROUP BY c.customer_name;

-- ❌ Плохо: фильтрация после JOIN  
SELECT c.customer_name, SUM(o.total_amount)
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_date >= '2023-01-01'  -- фильтр после JOIN
GROUP BY c.customer_name;
```

### 🧹 **Контроль качества данных:**

**Иерархия проверок:**
1. **Структурные проверки** — правильность схемы, типов данных
2. **Ограничения целостности** — внешние ключи, NOT NULL, CHECK constraints  
3. **Бизнес-правила** — логические ограничения (цена > 0, дата <= сегодня)
4. **Статистические проверки** — выбросы, аномалии, тренды

**Автоматизация проверок:**
```sql
-- Универсальная функция профилирования таблицы
CREATE OR REPLACE FUNCTION profile_table(table_name TEXT)
RETURNS TABLE(
    column_name TEXT,
    data_type TEXT,
    total_count BIGINT,
    null_count BIGINT,
    null_percentage NUMERIC,
    distinct_count BIGINT,
    min_value TEXT,
    max_value TEXT
) AS $$
BEGIN
    RETURN QUERY EXECUTE format('
        SELECT 
            column_name::TEXT,
            data_type::TEXT,
            COUNT(*)::BIGINT as total_count,
            COUNT(*) - COUNT(%I)::BIGINT as null_count,
            ROUND((COUNT(*) - COUNT(%I)) * 100.0 / COUNT(*), 2) as null_percentage,
            COUNT(DISTINCT %I)::BIGINT as distinct_count,
            MIN(%I::TEXT) as min_value,
            MAX(%I::TEXT) as max_value
        FROM %I
        GROUP BY column_name, data_type
    ', column_name, column_name, column_name, column_name, column_name, table_name);
END;
$$ LANGUAGE plpgsql;
```

### 🔄 **Автоматизация процессов:**

**Принципы надежной автоматизации:**
- **Идемпотентность** — повторный запуск не должен нарушать результат
- **Транзакционность** — либо все операции выполнились, либо ни одна
- **Мониторинг** — логирование всех операций с детальностью
- **Восстановимость** — возможность откатиться к предыдущему состоянию

**Обработка ошибок:**
```vba
Sub SafeDataProcessing()
    Dim errorCount As Integer
    Dim maxErrors As Integer: maxErrors = 3
    
    On Error GoTo ErrorHandler
    
    ' Основная логика обработки данных
    Call ProcessDataSource1
    Call ProcessDataSource2  
    Call ProcessDataSource3
    
    Exit Sub
    
ErrorHandler:
    errorCount = errorCount + 1
    
    ' Логирование ошибки
    Call LogError(Err.Number, Err.Description, "ProcessDataSource")
    
    ' Попытка восстановления
    If errorCount <= maxErrors Then
        Wait Application.Wait(Now + TimeValue("00:00:05")) ' Пауза 5 секунд
        Resume Next
    Else
        MsgBox "Превышено максимальное количество ошибок!", vbCritical
        Call SendAlertToAdmin("Critical error in data processing")
        End
    End If
End Sub
```

### ❓ **Решение типичных проблем:**

#### **Проблема: Медленное выполнение Power Query**
**Решение:**
- Применяйте фильтры на ранних этапах
- Удаляйте ненужные столбцы сразу после загрузки
- Используйте "Загрузить только подключение" для промежуточных запросов
- Включите "Fast Data Load" в настройках

#### **Проблема: Ошибки типов данных при объединении источников**  
**Решение:**
```m
// Универсальная функция приведения типов
let
    ConvertToSafeType = (value as any, targetType as type) =>
        try targetType(value) otherwise 
            if targetType = type text then Text.From(value)
            else if targetType = type number then 0
            else if targetType = type date then #date(1900,1,1)
            else null
in
    ConvertToSafeType
```

#### **Проблема: Дубликаты при объединении данных**
**Решение:**
```sql  
-- Использование ROW_NUMBER для дедупликации
WITH deduplicated AS (
    SELECT *,
        ROW_NUMBER() OVER (
            PARTITION BY customer_name, order_date, amount 
            ORDER BY created_at DESC
        ) as rn
    FROM sales_data
)
SELECT * FROM deduplicated WHERE rn = 1;
```

#### **Проблема: Несоответствие форматов дат**
**Решение:**
```m
// Универсальная функция парсинга дат
let
    ParseDate = (dateText as text) =>
        try Date.FromText(dateText, "ru-RU") otherwise
        try Date.FromText(dateText, "en-US") otherwise  
        try #date(
            Number.FromText(Text.End(dateText, 4)),
            Number.FromText(Text.Middle(dateText, 3, 2)), 
            Number.FromText(Text.Start(dateText, 2))
        ) otherwise null
in
    ParseDate
```

---

- 🔙 [Предыдущая глава: Глава 4 - Распределения](../chapter-04/README.md)
- 🔜 [Следующая глава: Глава 6 - Выборки и доверительные интервалы](../chapter-06/README.md)

---

- 📢 Присоединяйтесь к чату курса: [https://t.me/analytics_course_chat](https://t.me/analytics_course_chat)
- 📢 Канал курса: [https://t.me/analytics_course_channel](https://t.me/analytics_course_channel)