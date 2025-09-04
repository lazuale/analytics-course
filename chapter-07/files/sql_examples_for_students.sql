-- Примеры SQL-запросов для анализа A/B-тестов
-- 
-- Используйте эти запросы как отправную точку для практических заданий
-- Не забудьте адаптировать имена таблиц под вашу SQL-среду

-- =====================================================
-- БАЗОВЫЕ ЗАПРОСЫ ДЛЯ ab_test_data.csv
-- =====================================================

-- 1. Общая статистика по группам
SELECT 
    test_group as "Группа теста",
    COUNT(*) as "Участников",
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 1) as "Процент от общего"
FROM ab_test_users 
GROUP BY test_group
ORDER BY test_group;

-- 2. Базовые метрики конверсии по группам
SELECT 
    test_group as "Группа",
    COUNT(*) as "Всего участников",
    SUM(made_purchase) as "Конверсий",
    ROUND(AVG(made_purchase) * 100, 2) as "Конверсия %",
    ROUND(SUM(purchase_amount), 2) as "Общая выручка"
FROM ab_test_users
GROUP BY test_group
ORDER BY test_group;

-- 3. Сравнение конверсии между группами  
WITH group_stats AS (
    SELECT 
        test_group,
        COUNT(*) as total_users,
        SUM(made_purchase) as conversions,
        AVG(made_purchase) as conversion_rate
    FROM ab_test_users
    GROUP BY test_group
)
SELECT 
    a.test_group as "Группа A",
    a.conversion_rate as "Конверсия A",
    b.test_group as "Группа B", 
    b.conversion_rate as "Конверсия B",
    ROUND((b.conversion_rate - a.conversion_rate) * 100, 2) as "Абсолютная разница %",
    ROUND(((b.conversion_rate / a.conversion_rate) - 1) * 100, 2) as "Относительное улучшение %"
FROM group_stats a, group_stats b
WHERE a.test_group = 'A' AND b.test_group = 'B';

-- =====================================================
-- ДЕМОГРАФИЧЕСКИЙ АНАЛИЗ
-- =====================================================

-- 4. Конверсия по возрастным группам
SELECT 
    test_group as "Группа теста",
    CASE 
        WHEN age BETWEEN 18 AND 25 THEN '18-25'
        WHEN age BETWEEN 26 AND 35 THEN '26-35'
        WHEN age BETWEEN 36 AND 45 THEN '36-45'
        WHEN age BETWEEN 46 AND 55 THEN '46-55'
        ELSE '55+'
    END as "Возрастная группа",
    COUNT(*) as "Участников",
    SUM(made_purchase) as "Конверсий",
    ROUND(AVG(made_purchase) * 100, 2) as "Конверсия %"
FROM ab_test_users
GROUP BY test_group, 
    CASE 
        WHEN age BETWEEN 18 AND 25 THEN '18-25'
        WHEN age BETWEEN 26 AND 35 THEN '26-35'
        WHEN age BETWEEN 36 AND 45 THEN '36-45'
        WHEN age BETWEEN 46 AND 55 THEN '46-55'
        ELSE '55+'
    END
ORDER BY test_group, "Возрастная группа";

-- 5. Конверсия по городам
SELECT 
    test_group as "Группа теста",
    city as "Город",
    COUNT(*) as "Участников",
    SUM(made_purchase) as "Конверсий", 
    ROUND(AVG(made_purchase) * 100, 2) as "Конверсия %",
    ROUND(AVG(age), 1) as "Средний возраст"
FROM ab_test_users
GROUP BY test_group, city
ORDER BY city, test_group;

-- 6. Проверка случайности распределения по полу
SELECT 
    test_group as "Группа",
    gender as "Пол",
    COUNT(*) as "Количество",
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY test_group), 1) as "Процент в группе"
FROM ab_test_users
GROUP BY test_group, gender
ORDER BY test_group, gender;

-- =====================================================
-- ВРЕМЕННОЙ АНАЛИЗ
-- =====================================================

-- 7. Конверсия по дням недели
SELECT 
    test_group as "Группа",
    EXTRACT(DOW FROM test_start_date::date) as day_number,
    CASE EXTRACT(DOW FROM test_start_date::date)
        WHEN 0 THEN 'Воскресенье'
        WHEN 1 THEN 'Понедельник'  
        WHEN 2 THEN 'Вторник'
        WHEN 3 THEN 'Среда'
        WHEN 4 THEN 'Четверг'
        WHEN 5 THEN 'Пятница'
        WHEN 6 THEN 'Суббота'
    END as "День недели",
    COUNT(*) as "Участников",
    ROUND(AVG(made_purchase) * 100, 2) as "Конверсия %"
FROM ab_test_users
GROUP BY test_group, EXTRACT(DOW FROM test_start_date::date)
ORDER BY test_group, day_number;

-- 8. Динамика конверсии по дням теста
SELECT 
    test_start_date as "Дата",
    test_group as "Группа",
    COUNT(*) as "Новых участников",
    SUM(made_purchase) as "Конверсий",
    ROUND(AVG(made_purchase) * 100, 2) as "Дневная конверсия %"
FROM ab_test_users
GROUP BY test_start_date, test_group
ORDER BY test_start_date, test_group;

-- 9. Влияние времени с регистрации на конверсию
SELECT 
    test_group as "Группа",
    CASE 
        WHEN days_since_registration <= 30 THEN '0-30 дней'
        WHEN days_since_registration <= 90 THEN '31-90 дней'
        WHEN days_since_registration <= 180 THEN '91-180 дней'
        WHEN days_since_registration <= 365 THEN '181-365 дней'
        ELSE '365+ дней'
    END as "Время с регистрации",
    COUNT(*) as "Участников",
    ROUND(AVG(made_purchase) * 100, 2) as "Конверсия %"
FROM ab_test_users
GROUP BY test_group,
    CASE 
        WHEN days_since_registration <= 30 THEN '0-30 дней'
        WHEN days_since_registration <= 90 THEN '31-90 дней'
        WHEN days_since_registration <= 180 THEN '91-180 дней'
        WHEN days_since_registration <= 365 THEN '181-365 дней'
        ELSE '365+ дней'
    END
ORDER BY test_group, "Время с регистрации";

-- =====================================================
-- ФИНАНСОВЫЙ АНАЛИЗ (ab_test_order_values.csv)
-- =====================================================

-- 10. Средний чек и выручка по группам
SELECT 
    test_group as "Группа",
    COUNT(*) as "Заказов",
    ROUND(AVG(order_value), 2) as "Средний чек",
    ROUND(MIN(order_value), 2) as "Минимальный заказ",
    ROUND(MAX(order_value), 2) as "Максимальный заказ",
    ROUND(SUM(order_value), 2) as "Общая выручка"
FROM ab_test_orders
GROUP BY test_group
ORDER BY test_group;

-- 11. Распределение заказов по категориям
SELECT 
    test_group as "Группа",
    product_category as "Категория товара",
    COUNT(*) as "Заказов",
    ROUND(AVG(order_value), 2) as "Средний чек",
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY test_group), 1) as "Доля в группе %"
FROM ab_test_orders
GROUP BY test_group, product_category
ORDER BY test_group, product_category;

-- 12. Анализ по способам оплаты
SELECT 
    test_group as "Группа",
    payment_method as "Способ оплаты",
    COUNT(*) as "Заказов",
    ROUND(AVG(order_value), 2) as "Средний чек"
FROM ab_test_orders
GROUP BY test_group, payment_method
ORDER BY test_group, payment_method;

-- =====================================================
-- ИСТОРИЧЕСКИЙ АНАЛИЗ (website_historical_data.csv)
-- =====================================================

-- 13. Средние метрики по дням недели
SELECT 
    day_of_week as "День недели (число)",
    CASE day_of_week
        WHEN 1 THEN 'Понедельник'
        WHEN 2 THEN 'Вторник'
        WHEN 3 THEN 'Среда'
        WHEN 4 THEN 'Четверг'
        WHEN 5 THEN 'Пятница'
        WHEN 6 THEN 'Суббота'
        WHEN 7 THEN 'Воскресенье'
    END as "День недели",
    ROUND(AVG(visitors), 0) as "Средне посетителей",
    ROUND(AVG(purchases * 100.0 / visitors), 2) as "Средняя конверсия %",
    ROUND(AVG(total_revenue), 0) as "Средняя выручка"
FROM website_data
GROUP BY day_of_week
ORDER BY day_of_week;

-- 14. Влияние праздников на метрики
SELECT 
    CASE is_holiday
        WHEN 1 THEN 'Праздничный день'
        ELSE 'Обычный день'
    END as "Тип дня",
    COUNT(*) as "Дней в выборке",
    ROUND(AVG(visitors), 0) as "Средне посетителей",
    ROUND(AVG(purchases * 100.0 / visitors), 2) as "Средняя конверсия %",
    ROUND(AVG(total_revenue / visitors), 2) as "Выручка на посетителя"
FROM website_data
GROUP BY is_holiday;

-- 15. Эффективность рекламных расходов
SELECT 
    CASE 
        WHEN marketing_spend <= 30000 THEN 'Низкие расходы (≤30K)'
        WHEN marketing_spend <= 40000 THEN 'Средние расходы (30K-40K)'
        ELSE 'Высокие расходы (>40K)'
    END as "Уровень расходов",
    COUNT(*) as "Дней",
    ROUND(AVG(visitors), 0) as "Средне посетителей",
    ROUND(AVG(purchases), 0) as "Средне покупок",
    ROUND(AVG(total_revenue / marketing_spend), 2) as "ROI (выручка/расходы)"
FROM website_data
WHERE marketing_spend > 0
GROUP BY 
    CASE 
        WHEN marketing_spend <= 30000 THEN 'Низкие расходы (≤30K)'
        WHEN marketing_spend <= 40000 THEN 'Средние расходы (30K-40K)'
        ELSE 'Высокие расходы (>40K)'
    END;

-- =====================================================
-- МНОГОМЕРНЫЙ АНАЛИЗ (mvt_test_results.csv) 
-- =====================================================

-- 16. Результаты MVT по комбинациям
SELECT 
    combination as "Комбинация",
    header_version as "Заголовок",
    button_version as "Кнопка",
    COUNT(*) as "Участников",
    SUM(clicked_button) as "Кликов",
    ROUND(AVG(clicked_button) * 100, 2) as "CTR %",
    SUM(made_inquiry) as "Заявок",
    ROUND(AVG(made_inquiry) * 100, 2) as "Конверсия %"
FROM mvt_test_results
GROUP BY combination, header_version, button_version
ORDER BY combination;

-- 17. Главные эффекты заголовков
SELECT 
    header_version as "Версия заголовка",
    COUNT(*) as "Участников",
    ROUND(AVG(clicked_button) * 100, 2) as "CTR %",
    ROUND(AVG(made_inquiry) * 100, 2) as "Конверсия %",
    ROUND(AVG(session_duration), 0) as "Средняя сессия (сек)"
FROM mvt_test_results
GROUP BY header_version
ORDER BY header_version;

-- 18. Главные эффекты кнопок
SELECT 
    button_version as "Версия кнопки",
    COUNT(*) as "Участников", 
    ROUND(AVG(clicked_button) * 100, 2) as "CTR %",
    ROUND(AVG(made_inquiry) * 100, 2) as "Конверсия %"
FROM mvt_test_results
GROUP BY button_version
ORDER BY button_version;

-- 19. Анализ по сегментам пользователей
SELECT 
    user_segment as "Сегмент пользователя",
    combination as "Комбинация",
    COUNT(*) as "Участников",
    ROUND(AVG(made_inquiry) * 100, 2) as "Конверсия %",
    ROUND(AVG(session_duration), 0) as "Средняя сессия"
FROM mvt_test_results
GROUP BY user_segment, combination
ORDER BY user_segment, combination;

-- =====================================================
-- ПРОВЕРКА КАЧЕСТВА ДАННЫХ
-- =====================================================

-- 20. Проверка баланса групп A/B
SELECT 
    'Баланс групп A/B' as "Проверка",
    test_group as "Группа",
    COUNT(*) as "Участников",
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 1) as "Процент"
FROM ab_test_users
GROUP BY test_group;

-- 21. Поиск аномалий в данных
SELECT 
    'Аномалии в возрасте' as "Тип проверки",
    COUNT(CASE WHEN age < 18 OR age > 80 THEN 1 END) as "Аномальных записей",
    MIN(age) as "Минимальный возраст",
    MAX(age) as "Максимальный возраст"
FROM ab_test_users
UNION ALL
SELECT 
    'Аномалии в суммах заказов' as "Тип проверки",
    COUNT(CASE WHEN order_value <= 0 OR order_value > 50000 THEN 1 END) as "Аномальных записей",
    MIN(order_value) as "Минимальная сумма", 
    MAX(order_value) as "Максимальная сумма"
FROM ab_test_orders;

-- =====================================================
-- ДОПОЛНИТЕЛЬНЫЕ ПОЛЕЗНЫЕ ЗАПРОСЫ
-- =====================================================

-- 22. Воронка конверсии (для исторических данных)
SELECT 
    'Этапы воронки' as "Анализ",
    AVG(visitors) as "Посетители",
    AVG(catalog_clicks) as "Клики в каталог",
    AVG(cart_additions) as "Добавления в корзину",
    AVG(purchases) as "Покупки",
    ROUND(AVG(catalog_clicks * 100.0 / visitors), 2) as "Конверсия в каталог %",
    ROUND(AVG(cart_additions * 100.0 / catalog_clicks), 2) as "Конверсия в корзину %",
    ROUND(AVG(purchases * 100.0 / cart_additions), 2) as "Конверсия в покупку %"
FROM website_data;

-- 23. Топ дни по конверсии
SELECT 
    date as "Дата",
    visitors as "Посетители",
    purchases as "Покупки",
    ROUND(purchases * 100.0 / visitors, 2) as "Конверсия %",
    CASE is_holiday WHEN 1 THEN 'Праздник' ELSE 'Обычный' END as "Тип дня"
FROM website_data
WHERE visitors > 0
ORDER BY (purchases * 100.0 / visitors) DESC
LIMIT 10;

-- ====================================================
-- ПРИМЕЧАНИЯ ПО ИСПОЛЬЗОВАНИЮ:
-- ====================================================
-- 
-- 1. Замените имена таблиц на соответствующие вашей БД:
--    - ab_test_users → ваша таблица с данными A/B-теста
--    - ab_test_orders → ваша таблица с заказами
--    - website_data → ваша таблица с историческими данными
--    - mvt_test_results → ваша таблица с MVT данными
--
-- 2. Проверьте типы данных столбцов в вашей БД
-- 3. Адаптируйте функции даты под вашу СУБД (PostgreSQL/MySQL/SQLite)
-- 4. При импорте CSV учитывайте разделители (;) и десятичные дроби (,)