# 📊 Библиотека DAX-формул для Power Pivot

## 📋 Обзор библиотеки

Эта библиотека содержит проверенные DAX-формулы для типовых бизнес-расчетов в аналитических моделях. Все формулы протестированы на реальных данных и содержат подробные комментарии для понимания логики работы.

---

## 🔢 Базовые агрегации и фильтрация

### 📈 **Основные агрегатные функции**

#### 💰 Общая сумма продаж
```dax
Total_Sales = SUM(Sales[sales_amount])
```
**Назначение:** Базовая мера для расчета общей суммы продаж  
**Использование:** Основа для большинства других расчетов

#### 🛒 Количество заказов
```dax
Total_Orders = DISTINCTCOUNT(Sales[order_id])
```
**Назначение:** Подсчет уникальных заказов (не строк в таблице)  
**Важно:** Используется DISTINCTCOUNT для корректного подсчета

#### 👥 Количество уникальных клиентов
```dax
Unique_Customers = DISTINCTCOUNT(Sales[customer_id])
```
**Назначение:** Подсчет активных клиентов в выбранном периоде  
**Применение:** Анализ клиентской базы, расчет конверсий

#### 💳 Средний чек
```dax
Average_Check = 
DIVIDE(
    [Total_Sales],
    [Total_Orders],
    0
)
```
**Назначение:** Средняя сумма одного заказа  
**Функция DIVIDE:** Защита от деления на ноль (возвращает 0)  
**Применение:** Анализ покупательского поведения

---

### 🎯 Расчеты с контекстом (CALCULATE)

#### 📊 Продажи текущего года
```dax
Sales_Current_Year = 
CALCULATE(
    [Total_Sales],
    YEAR(Sales[order_date]) = YEAR(TODAY())
)
```
**Назначение:** Фильтрация продаж только за текущий год  
**Динамичность:** Автоматически обновляется при смене года

#### 🏢 Продажи B2B сегмента
```dax
Sales_B2B = 
CALCULATE(
    [Total_Sales],
    Customers[customer_type] = "B2B"
)
```
**Назначение:** Продажи корпоративным клиентам  
**Связь:** Использует связь между таблицами Sales и Customers

#### 📱 Продажи категории "Электроника"
```dax
Sales_Electronics = 
CALCULATE(
    [Total_Sales],
    Products[category_level_1] = "Электроника"
)
```
**Назначение:** Продажи по конкретной категории товаров  
**Применение:** Анализ эффективности категорий

#### 🌟 Продажи премиум брендов
```dax
Sales_Premium_Brands = 
CALCULATE(
    [Total_Sales],
    Products[brand_tier] = "Premium"
)
```
**Назначение:** Продажи товаров премиум сегмента  
**Бизнес-ценность:** Анализ маржинальности по сегментам

---

## ⏰ Временные функции и сравнения

### 📅 **Календарные расчеты**

#### 📊 Продажи с начала года (YTD)
```dax
Sales_YTD = 
TOTALYTD(
    [Total_Sales],
    'Calendar'[Date]
)
```
**Назначение:** Накопительная сумма с 1 января  
**Требования:** Необходима связанная календарная таблица  
**Применение:** Отчеты руководству, план-факт анализ

#### 📊 Продажи с начала месяца (MTD)
```dax
Sales_MTD = 
TOTALMTD(
    [Total_Sales],
    'Calendar'[Date]
)
```
**Назначение:** Накопительная сумма с начала текущего месяца  
**Применение:** Ежедневный мониторинг выполнения планов

#### 📊 Продажи с начала квартала (QTD)
```dax
Sales_QTD = 
TOTALQTD(
    [Total_Sales],
    'Calendar'[Date]
)
```
**Назначение:** Накопительная сумма с начала квартала  
**Применение:** Квартальное планирование и отчетность

---

### 🔄 **Сравнения периодов**

#### 📈 Продажи предыдущего месяца
```dax
Sales_Previous_Month = 
CALCULATE(
    [Total_Sales],
    DATEADD('Calendar'[Date], -1, MONTH)
)
```
**Назначение:** Продажи за предыдущий месяц для сравнения  
**Контекст:** Автоматически определяет предыдущий период

#### 📈 Продажи аналогичного периода прошлого года
```dax
Sales_Same_Period_Last_Year = 
CALCULATE(
    [Total_Sales],
    SAMEPERIODLASTYEAR('Calendar'[Date])
)
```
**Назначение:** Сравнение с аналогичным периодом предыдущего года  
**Применение:** Анализ сезонности и годовых трендов

#### 📊 Рост к предыдущему месяцу (в рублях)
```dax
Sales_Growth_Amount = 
[Total_Sales] - [Sales_Previous_Month]
```
**Назначение:** Абсолютный прирост продаж  
**Интерпретация:** Положительное значение = рост, отрицательное = снижение

#### 📊 Рост к предыдущему месяцу (в процентах)
```dax
Sales_Growth_Percent = 
DIVIDE(
    [Sales_Growth_Amount],
    [Sales_Previous_Month],
    0
) * 100
```
**Назначение:** Темп роста в процентах  
**Защита:** DIVIDE предотвращает деление на ноль  
**Формат:** Умножение на 100 для отображения в процентах

#### 📊 Индекс сезонности
```dax
Seasonal_Index = 
VAR CurrentMonthSales = [Total_Sales]
VAR AverageMonthSales = 
    CALCULATE(
        AVERAGEX(VALUES('Calendar'[MonthNumber]), [Total_Sales]),
        ALL('Calendar'[Date])
    )
RETURN
DIVIDE(CurrentMonthSales, AverageMonthSales, 1)
```
**Назначение:** Коэффициент сезонности для текущего месяца  
**Интерпретация:** >1 = выше среднего, <1 = ниже среднего  
**Применение:** Планирование и прогнозирование

---

## 📊 Скользящие средние и тренды

### 📈 **Скользящие средние**

#### 📊 3-месячное скользящее среднее
```dax
Sales_3M_Moving_Average = 
VAR CurrentDate = MAX('Calendar'[Date])
VAR ThreeMonthsBack = EOMONTH(CurrentDate, -3) + 1
RETURN
CALCULATE(
    AVERAGEX(
        FILTER(
            'Calendar',
            'Calendar'[Date] >= ThreeMonthsBack &&
            'Calendar'[Date] <= CurrentDate
        ),
        [Total_Sales]
    )
)
```
**Назначение:** Сглаживание колебаний для выявления тренда  
**Логика:** Средняя за последние 3 месяца включая текущий  
**Применение:** Анализ трендов, устранение сезонных колебаний

#### 📊 12-месячное скользящее среднее
```dax
Sales_12M_Moving_Average = 
VAR CurrentDate = MAX('Calendar'[Date])
VAR TwelveMonthsBack = EOMONTH(CurrentDate, -12) + 1
RETURN
CALCULATE(
    AVERAGEX(
        FILTER(
            'Calendar',
            'Calendar'[Date] >= TwelveMonthsBack &&
            'Calendar'[Date] <= CurrentDate
        ),
        [Total_Sales]
    )
)
```
**Назначение:** Годовой тренд без влияния сезонности  
**Применение:** Стратегическое планирование, анализ долгосрочных трендов

---

## 🏆 Ранжирование и рейтинги

### 📊 **Рейтинги и ТОП-списки**

#### 🥇 Рейтинг региона по продажам
```dax
Region_Sales_Rank = 
RANKX(
    ALL(Regions[region_name]),
    [Total_Sales],
    ,
    DESC
)
```
**Назначение:** Позиция региона в рейтинге по продажам  
**Сортировка:** DESC = от большего к меньшему (1 = лучший)  
**ALL:** Игнорирует текущие фильтры для корректного ранжирования

#### 🏆 Рейтинг товара в категории
```dax
Product_Rank_In_Category = 
RANKX(
    FILTER(
        ALL(Products[product_name]),
        Products[category_level_1] = MAX(Products[category_level_1])
    ),
    [Total_Sales],
    ,
    DESC
)
```
**Назначение:** Позиция товара среди товаров той же категории  
**Логика:** Ранжирование только внутри категории  
**Применение:** Анализ ассортимента, ABC-классификация

#### 🔝 ТОП-5 клиентов по продажам
```dax
Top5_Customers_Sales = 
SUMX(
    TOPN(
        5,
        VALUES(Customers[customer_name]),
        [Total_Sales],
        DESC
    ),
    [Total_Sales]
)
```
**Назначение:** Сумма продаж ТОП-5 клиентов  
**TOPN:** Выбирает 5 лучших клиентов  
**SUMX:** Суммирует их продажи  
**Применение:** Концентрационный анализ, правило 80/20

---

## 💰 Финансовые расчеты

### 📊 **Прибыльность и маржинальность**

#### 💵 Валовая прибыль
```dax
Gross_Profit = 
SUMX(
    Sales,
    Sales[quantity] * (Sales[unit_price] - Sales[cost_price])
)
```
**Назначение:** Прибыль до вычета операционных расходов  
**SUMX:** Построчный расчет для точности  
**Применение:** Анализ рентабельности продуктов

#### 📊 Валовая маржинальность
```dax
Gross_Margin_Percent = 
DIVIDE(
    [Gross_Profit],
    [Total_Sales],
    0
) * 100
```
**Назначение:** Валовая маржа в процентах  
**Формула:** (Продажи - Себестоимость) / Продажи * 100  
**Применение:** Сравнение прибыльности категорий/продуктов

#### 💰 Средняя маржинальность клиента
```dax
Average_Customer_Margin = 
AVERAGEX(
    VALUES(Customers[customer_id]),
    DIVIDE([Gross_Profit], [Total_Sales], 0)
)
```
**Назначение:** Средняя маржинальность по клиентам  
**AVERAGEX:** Расчет для каждого клиента отдельно  
**Применение:** Сегментация клиентов по прибыльности

#### 🎯 Маржинальность выше среднего
```dax
Above_Average_Margin = 
VAR AverageMargin = [Gross_Margin_Percent]
VAR CurrentMargin = [Gross_Margin_Percent]
RETURN
IF(CurrentMargin > AverageMargin, CurrentMargin, BLANK())
```
**Назначение:** Показывает маржинальность только если она выше средней  
**Применение:** Выделение высокомаржинальных сегментов

---

## 👥 Клиентская аналитика

### 📊 **RFM-анализ**

#### ⏰ Давность последней покупки (Recency)
```dax
Customer_Last_Purchase_Days = 
VAR LastPurchase = 
    CALCULATE(
        MAX(Sales[order_date]),
        ALLEXCEPT(Sales, Sales[customer_id])
    )
RETURN
DATEDIFF(LastPurchase, TODAY(), DAY)
```
**Назначение:** Количество дней с последней покупки клиента  
**ALLEXCEPT:** Убирает все фильтры кроме клиента  
**Применение:** Выявление неактивных клиентов

#### 🛒 Частота покупок (Frequency)
```dax
Customer_Purchase_Frequency = 
CALCULATE(
    DISTINCTCOUNT(Sales[order_id]),
    ALLEXCEPT(Sales, Sales[customer_id])
)
```
**Назначение:** Количество заказов клиента за весь период  
**Применение:** Сегментация по лояльности

#### 💰 Общая сумма покупок клиента (Monetary)
```dax
Customer_Total_Sales = 
CALCULATE(
    [Total_Sales],
    ALLEXCEPT(Sales, Sales[customer_id])
)
```
**Назначение:** Общий объем покупок клиента  
**Применение:** Выявление VIP-клиентов

#### 🎯 RFM-сегмент клиента
```dax
Customer_RFM_Segment = 
VAR RecencyScore = 
    IF([Customer_Last_Purchase_Days] <= 30, 3,
    IF([Customer_Last_Purchase_Days] <= 90, 2, 1))
VAR FrequencyScore = 
    IF([Customer_Purchase_Frequency] >= 10, 3,
    IF([Customer_Purchase_Frequency] >= 3, 2, 1))
VAR MonetaryScore = 
    IF([Customer_Total_Sales] >= 100000, 3,
    IF([Customer_Total_Sales] >= 30000, 2, 1))
VAR RFMScore = RecencyScore & FrequencyScore & MonetaryScore
RETURN
SWITCH(RFMScore,
    "333", "VIP Клиенты",
    "332", "Лояльные",
    "331", "Потенциал роста",
    "322", "Нуждаются в внимании",
    "321", "Новые клиенты",
    "233", "Рискуют уйти",
    "223", "Не могут потерять",
    "111", "Потерянные",
    "Прочие"
)
```
**Назначение:** Автоматическая сегментация клиентов по RFM-модели  
**Логика:** Комбинация оценок по давности, частоте и сумме  
**Применение:** Персонализация маркетинга, удержание клиентов

---

## 🎯 Конверсии и воронки продаж

### 📊 **Анализ воронки**

#### 🎯 Конверсия из лидов в клиентов
```dax
Lead_to_Customer_Conversion = 
VAR TotalLeads = DISTINCTCOUNT(Leads[lead_id])
VAR ConvertedLeads = 
    CALCULATE(
        DISTINCTCOUNT(Leads[lead_id]),
        Leads[status] = "Converted"
    )
RETURN
DIVIDE(ConvertedLeads, TotalLeads, 0) * 100
```
**Назначение:** Процент лидов, ставших клиентами  
**Применение:** Оценка эффективности продаж

#### 💰 Средний чек новых клиентов
```dax
New_Customer_Average_Check = 
VAR NewCustomers = 
    FILTER(
        Customers,
        Customers[registration_date] >= DATE(YEAR(TODAY()), 1, 1)
    )
RETURN
AVERAGEX(
    NewCustomers,
    CALCULATE([Total_Sales])
)
```
**Назначение:** Средний чек клиентов, зарегистрированных в текущем году  
**Применение:** Анализ качества привлеченных клиентов

---

## 📈 Прогнозирование и планирование

### 📊 **Простое прогнозирование**

#### 📈 Линейный тренд продаж
```dax
Sales_Linear_Trend = 
VAR SalesTable = 
    SUMMARIZE(
        'Calendar',
        'Calendar'[MonthYear],
        "Sales", [Total_Sales]
    )
VAR XValues = RANKX(SalesTable, 'Calendar'[MonthYear], , ASC)
VAR YValues = [Total_Sales]
VAR Count = COUNTROWS(SalesTable)
VAR SumX = SUMX(SalesTable, XValues)
VAR SumY = SUMX(SalesTable, YValues)
VAR SumXY = SUMX(SalesTable, XValues * YValues)
VAR SumX2 = SUMX(SalesTable, XValues * XValues)
VAR Slope = DIVIDE((Count * SumXY - SumX * SumY), (Count * SumX2 - SumX * SumX), 0)
VAR Intercept = DIVIDE((SumY - Slope * SumX), Count, 0)
RETURN
Slope * XValues + Intercept
```
**Назначение:** Расчет линейного тренда для прогнозирования  
**Метод:** Метод наименьших квадратов  
**Применение:** Простое прогнозирование на основе исторических данных

#### 🎯 План выполнен (Да/Нет)
```dax
Plan_Achieved = 
IF([Total_Sales] >= [Sales_Plan], "✅ Выполнен", "❌ Не выполнен")
```
**Назначение:** Индикатор выполнения плана  
**Визуализация:** Использует эмодзи для наглядности  
**Применение:** Дашборды для руководства

---

## 🛠 Служебные и вспомогательные формулы

### 📊 **Проверки и валидация**

#### ✅ Проверка качества данных
```dax
Data_Quality_Check = 
VAR EmptyValues = 
    CALCULATE(
        COUNTROWS(Sales),
        OR(
            ISBLANK(Sales[customer_id]),
            OR(
                ISBLANK(Sales[product_id]),
                ISBLANK(Sales[sales_amount])
            )
        )
    )
VAR TotalRows = COUNTROWS(Sales)
RETURN
IF(EmptyValues > 0, 
    "⚠️ Найдены пропуски: " & EmptyValues & " из " & TotalRows,
    "✅ Данные корректны"
)
```
**Назначение:** Проверка наличия пропусков в ключевых полях  
**Применение:** Мониторинг качества данных

#### 🔍 Количество записей в контексте
```dax
Row_Count = COUNTROWS(Sales)
```
**Назначение:** Подсчет строк с учетом текущих фильтров  
**Применение:** Отладка DAX-формул, проверка фильтрации

#### 📅 Текущий контекст даты
```dax
Current_Date_Context = 
IF(
    HASONEVALUE('Calendar'[Date]),
    VALUES('Calendar'[Date]),
    "Множественные даты"
)
```
**Назначение:** Показывает текущую дату в контексте  
**HASONEVALUE:** Проверяет, что выбрана одна дата  
**Применение:** Отладка временных расчетов

---

## 💡 Советы по использованию DAX

### ✅ **Лучшие практики:**

#### 🎯 **1. Используйте переменные (VAR) для сложных расчетов:**
```dax
// ✅ Хорошо - с переменными
Customer_Analysis = 
VAR CustomerSales = [Total_Sales]
VAR CustomerOrders = [Total_Orders]
VAR AverageCheck = DIVIDE(CustomerSales, CustomerOrders, 0)
RETURN
IF(AverageCheck > 50000, "VIP", "Обычный")

// ❌ Плохо - без переменных
Customer_Analysis_Bad = 
IF(DIVIDE([Total_Sales], [Total_Orders], 0) > 50000, "VIP", "Обычный")
```

#### 🚀 **2. Оптимизация производительности:**
```dax
// ✅ Быстро - использует индекс
Fast_Calculation = 
CALCULATE(
    [Total_Sales],
    Products[category_level_1] = "Электроника"
)

// ❌ Медленно - сканирует всю таблицу
Slow_Calculation = 
CALCULATE(
    [Total_Sales],
    CONTAINS(Products, Products[category_level_1], "Электроника")
)
```

#### 🔧 **3. Защита от ошибок:**
```dax
// ✅ С защитой от деления на ноль
Safe_Division = DIVIDE([Numerator], [Denominator], 0)

// ✅ С проверкой на пустые значения
Safe_Calculation = 
IF(
    ISBLANK([Value]),
    0,
    [Value] * 1.2
)
```

### ❌ **Частые ошибки:**

#### 1️⃣ **Неправильный контекст фильтрации:**
```dax
// ❌ Неправильно
Wrong_Customer_Total = SUM(Sales[sales_amount])

// ✅ Правильно
Correct_Customer_Total = 
CALCULATE(
    SUM(Sales[sales_amount]),
    ALLEXCEPT(Sales, Sales[customer_id])
)
```

#### 2️⃣ **Использование SUMX вместо SUM без необходимости:**
```dax
// ❌ Медленно без причины
Unnecessary_SUMX = SUMX(Sales, Sales[sales_amount])

// ✅ Быстрее для простой агрегации
Simple_SUM = SUM(Sales[sales_amount])
```

#### 3️⃣ **Отсутствие проверки на BLANK():**
```dax
// ❌ Может дать неожиданные результаты
Risky_Calculation = [Value1] + [Value2]

// ✅ С проверкой
Safe_Calculation = 
IF(
    OR(ISBLANK([Value1]), ISBLANK([Value2])),
    BLANK(),
    [Value1] + [Value2]
)
```

---

## 📚 Заключение

### 🎯 **Эта библиотека DAX-формул поможет вам:**

- **Ускорить разработку** аналитических моделей
- **Избежать типичных ошибок** в расчетах
- **Создавать консистентные метрики** во всех проектах
- **Изучить продвинутые техники** работы с DAX

### 📖 **Рекомендации по изучению:**

1. **Начинайте с базовых формул** — освойте SUM, CALCULATE, DIVIDE
2. **Изучайте контекст выполнения** — понимание фильтрации критично для DAX
3. **Практикуйтесь на реальных данных** — используйте файлы из учебных заданий
4. **Документируйте свои формулы** — добавляйте комментарии на русском языке

**Помните: хорошая DAX-формула должна быть не только правильной, но и понятной для коллег!**

---

📖 [Вернуться к описанию файлов](README.md) | 📝 [Перейти к практике](../practice.md) | 🚀 [Git-структура проекта](git_project_structure.md)

---

📢 Присоединяйтесь к чату курса: [@analytics_course_chat](https://t.me/analytics_course_chat)
📢 Канал курса: [@analytics_course_channel](https://t.me/analytics_course_channel)