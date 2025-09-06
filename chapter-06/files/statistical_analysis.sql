-- ================================================
-- Глава 6: Доверительные интервалы и статистика
-- Скрипт: Статистический анализ в PostgreSQL
-- ================================================

-- Раздел 1: Описательная статистика по группам
-- Рассчитываем основные статистики для разных сегментов данных

-- 1.1 Статистика продаж по категориям товаров
WITH sales_stats AS (
    SELECT 
        category_main,
        COUNT(*) as orders_count,
        AVG(order_amount) as avg_amount,
        STDDEV(order_amount) as std_dev,
        MIN(order_amount) as min_amount,
        MAX(order_amount) as max_amount,
        PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY order_amount) as q1,
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY order_amount) as median,
        PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY order_amount) as q3,
        -- Стандартная ошибка среднего
        STDDEV(order_amount) / SQRT(COUNT(*)) as std_error
    FROM sales_q4_data
    WHERE order_amount > 0
    GROUP BY category_main
    HAVING COUNT(*) >= 30  -- Минимум 30 наблюдений для нормального приближения
)
SELECT 
    category_main,
    orders_count,
    ROUND(avg_amount, 2) as avg_order_amount,
    ROUND(std_dev, 2) as std_deviation,
    ROUND(std_error, 2) as std_error,
    -- Приблизительный 95% доверительный интервал для среднего
    ROUND(avg_amount - 1.96 * std_error, 2) as ci_lower_95,
    ROUND(avg_amount + 1.96 * std_error, 2) as ci_upper_95,
    ROUND((avg_amount + 1.96 * std_error) - (avg_amount - 1.96 * std_error), 2) as ci_width,
    -- Дополнительная информация
    ROUND(min_amount, 2) as min_amount,
    ROUND(max_amount, 2) as max_amount,
    ROUND(median, 2) as median_amount
FROM sales_stats
ORDER BY avg_amount DESC;

-- 1.2 Статистика конверсии по источникам трафика
WITH conversion_stats AS (
    SELECT 
        traffic_source,
        COUNT(*) as total_sessions,
        SUM(conversion) as conversions,
        AVG(conversion::numeric) as conversion_rate,
        -- Стандартная ошибка для пропорции
        SQRT(AVG(conversion::numeric) * (1 - AVG(conversion::numeric)) / COUNT(*)) as se_proportion
    FROM website_analytics_data
    GROUP BY traffic_source
    HAVING COUNT(*) >= 100  -- Минимум для анализа пропорций
)
SELECT 
    traffic_source,
    total_sessions,
    conversions,
    ROUND(conversion_rate * 100, 2) as conversion_rate_pct,
    -- 95% доверительный интервал для пропорции
    ROUND((conversion_rate - 1.96 * se_proportion) * 100, 2) as ci_lower_95_pct,
    ROUND((conversion_rate + 1.96 * se_proportion) * 100, 2) as ci_upper_95_pct,
    ROUND(1.96 * se_proportion * 2 * 100, 2) as ci_width_pct
FROM conversion_stats
ORDER BY conversion_rate DESC;

-- Раздел 2: Подготовка данных для t-тестов
-- Создаем представления для сравнения групп

-- 2.1 Сравнение новых и постоянных клиентов
CREATE OR REPLACE VIEW customer_behavior_comparison AS
WITH customer_segments AS (
    SELECT 
        customer_id,
        COUNT(order_id) as total_orders,
        AVG(order_amount) as avg_order_amount,
        SUM(order_amount) as total_spent,
        CASE 
            WHEN COUNT(order_id) = 1 THEN 'Новый'
            WHEN COUNT(order_id) BETWEEN 2 AND 4 THEN 'Обычный'
            ELSE 'Постоянный'
        END as customer_type
    FROM sales_q4_data
    WHERE order_amount > 0
    GROUP BY customer_id
)
SELECT 
    customer_type,
    COUNT(*) as customers_count,
    ROUND(AVG(avg_order_amount), 2) as group_avg_order,
    ROUND(STDDEV(avg_order_amount), 2) as group_std_dev,
    ROUND(STDDEV(avg_order_amount) / SQRT(COUNT(*)), 2) as group_std_error,
    ROUND(MIN(avg_order_amount), 2) as min_order,
    ROUND(MAX(avg_order_amount), 2) as max_order,
    -- 95% ДИ для среднего чека по группам
    ROUND(AVG(avg_order_amount) - 1.96 * STDDEV(avg_order_amount) / SQRT(COUNT(*)), 2) as ci_lower,
    ROUND(AVG(avg_order_amount) + 1.96 * STDDEV(avg_order_amount) / SQRT(COUNT(*)), 2) as ci_upper
FROM customer_segments
GROUP BY customer_type
ORDER BY group_avg_order DESC;

-- Вывод данных для анализа
SELECT * FROM customer_behavior_comparison;

-- 2.2 Данные A/B-теста для статистического анализа
WITH ab_test_summary AS (
    SELECT 
        test_group,
        COUNT(*) as users_count,
        -- Средний чек среди совершивших покупку
        COUNT(CASE WHEN order_amount > 0 THEN 1 END) as active_users,
        AVG(CASE WHEN order_amount > 0 THEN order_amount END) as avg_order_amount,
        STDDEV(CASE WHEN order_amount > 0 THEN order_amount END) as std_order_amount,
        -- Доля совершивших повторную покупку
        AVG(repeat_purchase::numeric) as repeat_purchase_rate,
        SQRT(AVG(repeat_purchase::numeric) * (1 - AVG(repeat_purchase::numeric)) / COUNT(*)) as se_repeat_rate,
        -- Поведенческие метрики
        AVG(session_duration) as avg_session_duration,
        AVG(pages_per_session) as avg_pages_per_session
    FROM ab_test_data
    GROUP BY test_group
)
SELECT 
    test_group,
    users_count,
    active_users,
    ROUND(avg_order_amount, 2) as avg_order_amount,
    ROUND(std_order_amount, 2) as std_order_amount,
    ROUND(repeat_purchase_rate * 100, 2) as repeat_rate_pct,
    -- ДИ для доли повторных покупок
    ROUND((repeat_purchase_rate - 1.96 * se_repeat_rate) * 100, 2) as repeat_ci_lower,
    ROUND((repeat_purchase_rate + 1.96 * se_repeat_rate) * 100, 2) as repeat_ci_upper,
    ROUND(avg_session_duration, 1) as avg_session_duration,
    ROUND(avg_pages_per_session, 1) as avg_pages_per_session
FROM ab_test_summary
ORDER BY test_group;

-- Раздел 3: Анализ временных трендов с доверительными интервалами
-- Анализируем изменение показателей во времени

-- 3.1 Месячная динамика среднего чека с ДИ
WITH monthly_sales AS (
    SELECT 
        DATE_TRUNC('month', order_date::date) as month,
        COUNT(*) as orders_count,
        AVG(order_amount) as avg_amount,
        STDDEV(order_amount) as std_dev,
        STDDEV(order_amount) / SQRT(COUNT(*)) as std_error
    FROM sales_q4_data
    WHERE order_amount > 0
    GROUP BY DATE_TRUNC('month', order_date::date)
    HAVING COUNT(*) >= 20  -- Минимум заказов для анализа
)
SELECT 
    TO_CHAR(month, 'YYYY-MM') as month,
    orders_count,
    ROUND(avg_amount, 2) as avg_order_amount,
    -- 95% доверительный интервал
    ROUND(avg_amount - 1.96 * std_error, 2) as ci_lower,
    ROUND(avg_amount + 1.96 * std_error, 2) as ci_upper,
    ROUND(1.96 * std_error * 2, 2) as ci_width,
    -- Относительная ширина ДИ (%)
    ROUND((1.96 * std_error * 2 / avg_amount) * 100, 1) as ci_width_pct
FROM monthly_sales
ORDER BY month;

-- 3.2 Еженедельная динамика конверсии
WITH weekly_conversion AS (
    SELECT 
        DATE_TRUNC('week', session_date::date) as week,
        COUNT(*) as sessions,
        SUM(conversion) as conversions,
        AVG(conversion::numeric) as conversion_rate,
        SQRT(AVG(conversion::numeric) * (1 - AVG(conversion::numeric)) / COUNT(*)) as se_conversion
    FROM website_analytics_data
    GROUP BY DATE_TRUNC('week', session_date::date)
    HAVING COUNT(*) >= 100
)
SELECT 
    TO_CHAR(week, 'YYYY-MM-DD') as week_start,
    sessions,
    conversions,
    ROUND(conversion_rate * 100, 2) as conversion_rate_pct,
    -- 95% ДИ для конверсии
    ROUND((conversion_rate - 1.96 * se_conversion) * 100, 2) as conv_ci_lower,
    ROUND((conversion_rate + 1.96 * se_conversion) * 100, 2) as conv_ci_upper
FROM weekly_conversion
ORDER BY week_start;

-- Раздел 4: Обнаружение и анализ выбросов
-- Выявляем аномальные значения для корректного статистического анализа

-- 4.1 Выбросы в суммах заказов (правило 3 сигм)
WITH outlier_detection AS (
    SELECT 
        order_id,
        order_amount,
        category_main,
        AVG(order_amount) OVER() as overall_mean,
        STDDEV(order_amount) OVER() as overall_std,
        -- Z-score
        ABS(order_amount - AVG(order_amount) OVER()) / STDDEV(order_amount) OVER() as z_score,
        -- Межквартильный размах (IQR)
        PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY order_amount) OVER() as q3,
        PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY order_amount) OVER() as q1
    FROM sales_q4_data
    WHERE order_amount > 0
)
SELECT 
    'Выбросы по правилу 3 сигм (z > 3)' as method,
    COUNT(*) as outliers_count,
    ROUND(AVG(order_amount), 2) as avg_outlier_amount,
    ROUND(MIN(order_amount), 2) as min_outlier,
    ROUND(MAX(order_amount), 2) as max_outlier
FROM outlier_detection
WHERE z_score > 3

UNION ALL

SELECT 
    'Выбросы по IQR правилу' as method,
    COUNT(*) as outliers_count,
    ROUND(AVG(order_amount), 2) as avg_outlier_amount,
    ROUND(MIN(order_amount), 2) as min_outlier,
    ROUND(MAX(order_amount), 2) as max_outlier
FROM outlier_detection
WHERE order_amount > (q3 + 1.5 * (q3 - q1)) OR order_amount < (q1 - 1.5 * (q3 - q1));

-- 4.2 Статистика без выбросов
WITH clean_data AS (
    SELECT 
        *,
        ABS(order_amount - AVG(order_amount) OVER()) / STDDEV(order_amount) OVER() as z_score
    FROM sales_q4_data
    WHERE order_amount > 0
)
SELECT 
    'С выбросами' as data_type,
    COUNT(*) as n,
    ROUND(AVG(order_amount), 2) as mean_amount,
    ROUND(STDDEV(order_amount), 2) as std_amount,
    ROUND(AVG(order_amount) - 1.96 * STDDEV(order_amount) / SQRT(COUNT(*)), 2) as ci_lower,
    ROUND(AVG(order_amount) + 1.96 * STDDEV(order_amount) / SQRT(COUNT(*)), 2) as ci_upper
FROM clean_data

UNION ALL

SELECT 
    'Без выбросов (z < 3)' as data_type,
    COUNT(*) as n,
    ROUND(AVG(order_amount), 2) as mean_amount,
    ROUND(STDDEV(order_amount), 2) as std_amount,
    ROUND(AVG(order_amount) - 1.96 * STDDEV(order_amount) / SQRT(COUNT(*)), 2) as ci_lower,
    ROUND(AVG(order_amount) + 1.96 * STDDEV(order_amount) / SQRT(COUNT(*)), 2) as ci_upper
FROM clean_data
WHERE z_score <= 3;

-- Раздел 5: Специальные запросы для заданий главы 6

-- 5.1 Подготовка данных для множественных сравнений (Задание 4.1)
SELECT 
    region,
    COUNT(*) as sample_size,
    ROUND(AVG(quality_score), 2) as avg_quality,
    ROUND(STDDEV(quality_score), 2) as std_quality,
    ROUND(STDDEV(quality_score) / SQRT(COUNT(*)), 2) as std_error,
    -- 95% ДИ
    ROUND(AVG(quality_score) - 1.96 * STDDEV(quality_score) / SQRT(COUNT(*)), 2) as ci_lower,
    ROUND(AVG(quality_score) + 1.96 * STDDEV(quality_score) / SQRT(COUNT(*)), 2) as ci_upper
FROM quality_assessment_data
GROUP BY region
HAVING COUNT(*) >= 30
ORDER BY avg_quality DESC;

-- 5.2 Анализ соответствия стандартам времени ответа (Задание 4.2)
WITH response_analysis AS (
    SELECT 
        COUNT(*) as total_tickets,
        AVG(response_time) as avg_response_time,
        STDDEV(response_time) as std_response_time,
        STDDEV(response_time) / SQRT(COUNT(*)) as std_error,
        -- Доля превышающих 4 часа
        AVG(CASE WHEN response_time > 4 THEN 1 ELSE 0 END) as rate_over_4h,
        SQRT(AVG(CASE WHEN response_time > 4 THEN 1 ELSE 0 END) * 
             (1 - AVG(CASE WHEN response_time > 4 THEN 1 ELSE 0 END)) / COUNT(*)) as se_rate_over_4h
    FROM response_times_data
)
SELECT 
    total_tickets,
    ROUND(avg_response_time, 2) as avg_response_hours,
    ROUND(std_response_time, 2) as std_response_hours,
    -- 95% ДИ для среднего времени ответа
    ROUND(avg_response_time - 1.96 * std_error, 2) as ci_lower_time,
    ROUND(avg_response_time + 1.96 * std_error, 2) as ci_upper_time,
    -- Анализ соответствия стандарту "не более 4 часов"
    ROUND(rate_over_4h * 100, 1) as pct_over_4h,
    ROUND((rate_over_4h - 1.96 * se_rate_over_4h) * 100, 1) as pct_over_4h_ci_lower,
    ROUND((rate_over_4h + 1.96 * se_rate_over_4h) * 100, 1) as pct_over_4h_ci_upper,
    -- t-статистика для теста H0: μ ≤ 4
    ROUND((avg_response_time - 4) / std_error, 3) as t_statistic
FROM response_analysis;

-- 5.3 Контроль качества по категориям (Задание 4.3)
SELECT 
    category,
    COUNT(*) as total_orders,
    SUM(returned) as returns_count,
    ROUND(AVG(returned::numeric) * 100, 2) as return_rate_pct,
    -- Стандартная ошибка для пропорции
    ROUND(SQRT(AVG(returned::numeric) * (1 - AVG(returned::numeric)) / COUNT(*)) * 100, 2) as se_pct,
    -- 95% ДИ для доли возвратов
    ROUND((AVG(returned::numeric) - 1.96 * SQRT(AVG(returned::numeric) * (1 - AVG(returned::numeric)) / COUNT(*))) * 100, 2) as return_ci_lower,
    ROUND((AVG(returned::numeric) + 1.96 * SQRT(AVG(returned::numeric) * (1 - AVG(returned::numeric)) / COUNT(*))) * 100, 2) as return_ci_upper,
    -- Тест против стандарта 3%
    CASE 
        WHEN AVG(returned::numeric) - 1.96 * SQRT(AVG(returned::numeric) * (1 - AVG(returned::numeric)) / COUNT(*)) > 0.03 
        THEN 'Превышает стандарт'
        ELSE 'Соответствует стандарту'
    END as quality_status
FROM return_rates_data
GROUP BY category
ORDER BY return_rate_pct DESC;

-- Примеры использования:
-- 1. Выполните все запросы последовательно для получения статистических данных
-- 2. Используйте результаты для построения доверительных интервалов в Excel
-- 3. Сравните результаты SQL с расчетами в Excel для проверки
-- 4. Экспортируйте результаты для дальнейшего анализа

-- Дополнительные полезные запросы:

-- Корреляционный анализ (приближенный)
SELECT 
    ROUND(
        (COUNT(*) * SUM(pages_viewed * time_on_site) - SUM(pages_viewed) * SUM(time_on_site)) /
        SQRT(
            (COUNT(*) * SUM(pages_viewed * pages_viewed) - SUM(pages_viewed) * SUM(pages_viewed)) *
            (COUNT(*) * SUM(time_on_site * time_on_site) - SUM(time_on_site) * SUM(time_on_site))
        ), 3
    ) as correlation_pages_time
FROM website_analytics_data;

-- Сводная таблица для быстрого обзора всех данных
SELECT 
    'Продажи Q4' as dataset,
    COUNT(*) as records,
    'Сумма заказа' as key_metric,
    ROUND(AVG(order_amount::numeric), 2) as avg_value
FROM sales_q4_data
WHERE order_amount > 0

UNION ALL

SELECT 
    'Аналитика сайта' as dataset,
    COUNT(*) as records,
    'Конверсия %' as key_metric,
    ROUND(AVG(conversion::numeric) * 100, 2) as avg_value
FROM website_analytics_data

UNION ALL

SELECT 
    'Опрос клиентов' as dataset,
    COUNT(*) as records,
    'Удовлетворенность' as key_metric,
    ROUND(AVG(satisfaction_score::numeric), 2) as avg_value
FROM customer_satisfaction_data;