-- ================================================
-- Глава 7: A/B-тестирование
-- Скрипт: Комплексный анализ A/B-тестов в PostgreSQL
-- ================================================

-- Раздел 1: Рандомизация пользователей
-- Создаем устойчивую и воспроизводимую систему распределения по группам

-- 1.1 Функция устойчивой рандомизации на основе hash
CREATE OR REPLACE FUNCTION stable_ab_group(user_id INT, test_name TEXT DEFAULT 'default')
RETURNS TEXT AS $$
BEGIN
    -- Используем MD5 hash от комбинации user_id и test_name
    -- Это обеспечивает устойчивость и уникальность для каждого теста
    RETURN CASE 
        WHEN (ABS(('x' || SUBSTR(MD5(user_id::TEXT || test_name), 1, 8))::BIT(32)::INT) % 100) < 50 
        THEN 'A' 
        ELSE 'B' 
    END;
END;
$$ LANGUAGE plpgsql;

-- 1.2 Пример использования функции рандомизации
WITH user_randomization AS (
    SELECT 
        user_id,
        stable_ab_group(user_id, 'checkout_test_2024') as ab_group,
        -- Дополнительная информация о пользователе
        registration_date,
        city,
        device_type
    FROM users
    WHERE registration_date >= '2024-01-01'
      AND is_test_user = FALSE
      AND city IN ('Москва', 'Санкт-Петербург', 'Екатеринбург', 'Новосибирск')
)
SELECT 
    ab_group,
    COUNT(*) as users_count,
    ROUND(COUNT(*)::NUMERIC / SUM(COUNT(*)) OVER() * 100, 2) as percentage,
    -- Проверка баланса по ключевым характеристикам
    ROUND(AVG(CASE WHEN city = 'Москва' THEN 1.0 ELSE 0.0 END) * 100, 1) as pct_moscow,
    ROUND(AVG(CASE WHEN device_type = 'mobile' THEN 1.0 ELSE 0.0 END) * 100, 1) as pct_mobile
FROM user_randomization
GROUP BY ab_group
ORDER BY ab_group;

-- 1.3 Многовариантное тестирование (A/B/C/D тест)
CREATE OR REPLACE FUNCTION multi_variant_group(user_id INT, variants_count INT DEFAULT 4)
RETURNS TEXT AS $$
DECLARE
    variant_letter CHAR;
BEGIN
    -- Распределяем пользователей по вариантам A, B, C, D...
    variant_letter := CHR(65 + (ABS(('x' || SUBSTR(MD5(user_id::TEXT), 1, 8))::BIT(32)::INT) % variants_count));
    RETURN variant_letter;
END;
$$ LANGUAGE plpgsql;

-- Пример многовариантного теста
SELECT 
    multi_variant_group(user_id, 6) as test_variant,
    COUNT(*) as users_count,
    ROUND(COUNT(*)::NUMERIC * 100.0 / SUM(COUNT(*)) OVER(), 1) as percentage
FROM generate_series(1, 10000) as user_id
GROUP BY test_variant
ORDER BY test_variant;

-- Раздел 2: Анализ результатов A/B-тестов
-- Основные статистические расчеты для binary и continuous метрик

-- 2.1 Анализ конверсионных метрик (пропорции)
WITH ab_test_results AS (
    SELECT 
        user_id,
        stable_ab_group(user_id, 'checkout_test') as test_group,
        converted,
        order_amount,
        device_type,
        traffic_source
    FROM checkout_ab_test_results
),

conversion_analysis AS (
    SELECT 
        test_group,
        COUNT(*) as total_users,
        SUM(converted) as conversions,
        ROUND(AVG(converted::NUMERIC) * 100, 2) as conversion_rate_pct,
        
        -- Стандартная ошибка для пропорции
        ROUND(SQRT(AVG(converted::NUMERIC) * (1 - AVG(converted::NUMERIC)) / COUNT(*)) * 100, 3) as se_conversion_pct,
        
        -- 95% доверительный интервал для конверсии
        ROUND((AVG(converted::NUMERIC) - 1.96 * SQRT(AVG(converted::NUMERIC) * (1 - AVG(converted::NUMERIC)) / COUNT(*))) * 100, 2) as ci_lower_pct,
        ROUND((AVG(converted::NUMERIC) + 1.96 * SQRT(AVG(converted::NUMERIC) * (1 - AVG(converted::NUMERIC)) / COUNT(*))) * 100, 2) as ci_upper_pct
    FROM ab_test_results
    GROUP BY test_group
),

-- Z-тест для сравнения пропорций
statistical_test AS (
    SELECT 
        a.conversion_rate_pct / 100.0 as p_control,
        b.conversion_rate_pct / 100.0 as p_treatment,
        a.total_users as n_control,
        b.total_users as n_treatment,
        
        -- Объединенная пропорция
        ((a.conversions + b.conversions)::NUMERIC / (a.total_users + b.total_users)) as p_combined
    FROM conversion_analysis a
    CROSS JOIN conversion_analysis b  
    WHERE a.test_group = 'A' AND b.test_group = 'B'
)

SELECT 
    -- Результаты по группам
    ca.test_group,
    ca.total_users,
    ca.conversions,
    ca.conversion_rate_pct || '%' as conversion_rate,
    '[' || ca.ci_lower_pct || '%; ' || ca.ci_upper_pct || '%]' as ci_95_pct,
    
    -- Статистический тест (только для строки с группой B)
    CASE WHEN ca.test_group = 'B' THEN
        -- Разность конверсий
        ROUND((st.p_treatment - st.p_control) * 100, 2) || ' п.п.'
    END as absolute_lift,
    
    CASE WHEN ca.test_group = 'B' THEN
        -- Относительное улучшение  
        ROUND((st.p_treatment - st.p_control) / st.p_control * 100, 1) || '%'
    END as relative_lift,
    
    CASE WHEN ca.test_group = 'B' THEN
        -- Z-статистика
        ROUND(
            (st.p_treatment - st.p_control) / 
            SQRT(st.p_combined * (1 - st.p_combined) * (1.0/st.n_control + 1.0/st.n_treatment))
        , 3)
    END as z_statistic,
    
    CASE WHEN ca.test_group = 'B' THEN
        -- P-value (приближенный)
        CASE 
            WHEN ABS((st.p_treatment - st.p_control) / 
                    SQRT(st.p_combined * (1 - st.p_combined) * (1.0/st.n_control + 1.0/st.n_treatment))) > 2.576 
            THEN '< 0.001'
            WHEN ABS((st.p_treatment - st.p_control) / 
                    SQRT(st.p_combined * (1 - st.p_combined) * (1.0/st.n_control + 1.0/st.n_treatment))) > 1.96 
            THEN '< 0.05'
            ELSE '≥ 0.05'
        END
    END as p_value_range

FROM conversion_analysis ca
CROSS JOIN statistical_test st
ORDER BY ca.test_group;

-- 2.2 Анализ непрерывных метрик (средний чек, время на сайте)
WITH continuous_metrics AS (
    SELECT 
        stable_ab_group(user_id, 'checkout_test') as test_group,
        order_amount,
        time_on_checkout_page
    FROM checkout_ab_test_results
    WHERE converted = 1  -- Только для конвертированных пользователей
),

descriptive_stats AS (
    SELECT 
        test_group,
        COUNT(*) as sample_size,
        
        -- Средний чек
        ROUND(AVG(order_amount), 2) as mean_order_amount,
        ROUND(STDDEV(order_amount), 2) as std_order_amount,
        ROUND(STDDEV(order_amount) / SQRT(COUNT(*)), 2) as se_order_amount,
        
        -- 95% ДИ для среднего чека
        ROUND(AVG(order_amount) - 1.96 * STDDEV(order_amount) / SQRT(COUNT(*)), 2) as aov_ci_lower,
        ROUND(AVG(order_amount) + 1.96 * STDDEV(order_amount) / SQRT(COUNT(*)), 2) as aov_ci_upper,
        
        -- Время на странице
        ROUND(AVG(time_on_checkout_page), 1) as mean_time_seconds,
        ROUND(STDDEV(time_on_checkout_page), 1) as std_time_seconds
    FROM continuous_metrics
    GROUP BY test_group
)

SELECT 
    test_group,
    sample_size,
    mean_order_amount || '₽' as avg_order_value,
    '[' || aov_ci_lower || '₽; ' || aov_ci_upper || '₽]' as aov_95_ci,
    mean_time_seconds || ' сек' as avg_time_on_page,
    
    -- T-тест результат (только для группы B)
    CASE WHEN test_group = 'B' THEN
        ROUND((LAG(mean_order_amount) OVER(ORDER BY test_group DESC) - mean_order_amount), 2) || '₽'
    END as aov_difference,
    
    CASE WHEN test_group = 'B' THEN
        ROUND((LAG(mean_time_seconds) OVER(ORDER BY test_group DESC) - mean_time_seconds), 1) || ' сек'
    END as time_difference

FROM descriptive_stats
ORDER BY test_group;

-- Раздел 3: Сегментированный анализ
-- Анализ эффектов по различным сегментам пользователей

-- 3.1 Анализ по возрастным группам
WITH segmented_analysis AS (
    SELECT 
        age_group,
        test_group,
        COUNT(*) as users_count,
        SUM(converted) as conversions,
        ROUND(AVG(converted::NUMERIC) * 100, 2) as conversion_rate_pct,
        ROUND(SQRT(AVG(converted::NUMERIC) * (1 - AVG(converted::NUMERIC)) / COUNT(*)) * 100, 3) as se_pct
    FROM segmented_ab_results
    GROUP BY age_group, test_group
),

segment_comparison AS (
    SELECT 
        s1.age_group,
        s1.conversion_rate_pct as control_conversion,
        s2.conversion_rate_pct as treatment_conversion,
        ROUND(s2.conversion_rate_pct - s1.conversion_rate_pct, 2) as absolute_lift,
        ROUND((s2.conversion_rate_pct - s1.conversion_rate_pct) / s1.conversion_rate_pct * 100, 1) as relative_lift,
        s1.users_count + s2.users_count as total_sample_size,
        
        -- Приблизительная оценка значимости
        CASE 
            WHEN ABS(s2.conversion_rate_pct - s1.conversion_rate_pct) > 2 * SQRT(s1.se_pct^2 + s2.se_pct^2)
            THEN 'Вероятно значимо'
            ELSE 'Вероятно не значимо'
        END as significance_estimate
    FROM segmented_analysis s1
    JOIN segmented_analysis s2 ON s1.age_group = s2.age_group
    WHERE s1.test_group = 'A' AND s2.test_group = 'B'
)

SELECT 
    age_group,
    control_conversion || '%' as control_rate,
    treatment_conversion || '%' as treatment_rate,
    absolute_lift || ' п.п.' as effect_absolute,
    relative_lift || '%' as effect_relative,
    total_sample_size,
    significance_estimate
FROM segment_comparison
ORDER BY absolute_lift DESC;

-- 3.2 Анализ по устройствам и каналам трафика
SELECT 
    device_type,
    traffic_source,
    test_group,
    COUNT(*) as users,
    ROUND(AVG(converted::NUMERIC) * 100, 1) as conversion_pct,
    ROUND(AVG(CASE WHEN converted = 1 THEN order_amount END), 0) as avg_order_value
FROM segmented_ab_results
GROUP BY CUBE(device_type, traffic_source, test_group)
HAVING COUNT(*) > 50  -- Фильтруем малые сегменты
ORDER BY device_type, traffic_source, test_group;

-- Раздел 4: Временной анализ и мониторинг
-- Динамика метрик в течение времени проведения теста

-- 4.1 Ежедневная динамика результатов
WITH daily_results AS (
    SELECT 
        session_date::DATE,
        stable_ab_group(user_id, 'multiple_test') as test_group,
        COUNT(*) as daily_users,
        SUM(converted) as daily_conversions,
        ROUND(AVG(converted::NUMERIC) * 100, 2) as daily_conversion_rate,
        
        -- Кумулятивные показатели
        SUM(COUNT(*)) OVER (PARTITION BY stable_ab_group(user_id, 'multiple_test') 
                           ORDER BY session_date::DATE 
                           ROWS UNBOUNDED PRECEDING) as cumulative_users,
        SUM(SUM(converted)) OVER (PARTITION BY stable_ab_group(user_id, 'multiple_test') 
                                 ORDER BY session_date::DATE 
                                 ROWS UNBOUNDED PRECEDING) as cumulative_conversions
    FROM multiple_tests_results
    WHERE variant = 'A_control' OR variant = 'B_red_button'  -- Сравниваем только 2 группы
    GROUP BY session_date::DATE, stable_ab_group(user_id, 'multiple_test')
),

daily_with_cumulative AS (
    SELECT 
        *,
        ROUND(cumulative_conversions::NUMERIC / cumulative_users * 100, 2) as cumulative_conversion_rate
    FROM daily_results
)

SELECT 
    session_date,
    test_group,
    daily_users,
    daily_conversion_rate || '%' as daily_conv_rate,
    cumulative_users,
    cumulative_conversion_rate || '%' as cumul_conv_rate,
    
    -- Доверительный интервал для кумулятивной конверсии
    ROUND((cumulative_conversions::NUMERIC / cumulative_users - 
           1.96 * SQRT((cumulative_conversions::NUMERIC / cumulative_users) * 
                      (1 - cumulative_conversions::NUMERIC / cumulative_users) / cumulative_users)) * 100, 2) 
    || '%' as ci_lower,
    
    ROUND((cumulative_conversions::NUMERIC / cumulative_users + 
           1.96 * SQRT((cumulative_conversions::NUMERIC / cumulative_users) * 
                      (1 - cumulative_conversions::NUMERIC / cumulative_users) / cumulative_users)) * 100, 2)
    || '%' as ci_upper

FROM daily_with_cumulative
ORDER BY session_date, test_group;

-- Раздел 5: Множественное тестирование и поправки
-- Анализ одновременных A/B/C/D/E/F тестов с поправками

-- 5.1 Результаты всех вариантов против контроля
WITH variant_results AS (
    SELECT 
        variant,
        variant_description,
        COUNT(*) as sample_size,
        SUM(converted) as conversions,
        ROUND(AVG(converted::NUMERIC) * 100, 2) as conversion_rate_pct
    FROM multiple_tests_results
    GROUP BY variant, variant_description
),

control_metrics AS (
    SELECT conversion_rate_pct / 100.0 as p_control, sample_size as n_control
    FROM variant_results WHERE variant = 'A_control'
),

pairwise_tests AS (
    SELECT 
        vr.variant,
        vr.variant_description,
        vr.conversion_rate_pct,
        vr.sample_size,
        cm.p_control,
        vr.conversion_rate_pct / 100.0 as p_variant,
        
        -- Разность конверсий
        ROUND((vr.conversion_rate_pct / 100.0 - cm.p_control) * 100, 2) as lift_pp,
        ROUND((vr.conversion_rate_pct / 100.0 - cm.p_control) / cm.p_control * 100, 1) as lift_relative,
        
        -- Z-статистика для каждого сравнения с контролем
        ROUND(
            (vr.conversion_rate_pct / 100.0 - cm.p_control) / 
            SQRT(((vr.conversions + cm.p_control * cm.n_control) / (vr.sample_size + cm.n_control)) * 
                 (1 - (vr.conversions + cm.p_control * cm.n_control) / (vr.sample_size + cm.n_control)) * 
                 (1.0/vr.sample_size + 1.0/cm.n_control))
        , 3) as z_statistic
    FROM variant_results vr
    CROSS JOIN control_metrics cm
    WHERE vr.variant != 'A_control'
)

SELECT 
    variant,
    variant_description,
    conversion_rate_pct || '%' as conversion_rate,
    lift_pp || ' п.п.' as absolute_lift,
    lift_relative || '%' as relative_lift,
    z_statistic,
    
    -- P-value categories
    CASE 
        WHEN ABS(z_statistic) > 2.576 THEN '< 0.01'
        WHEN ABS(z_statistic) > 1.96 THEN '< 0.05'  
        WHEN ABS(z_statistic) > 1.645 THEN '< 0.10'
        ELSE '≥ 0.10'
    END as p_value_range,
    
    -- Значимость без поправки
    CASE WHEN ABS(z_statistic) > 1.96 THEN 'Да' ELSE 'Нет' END as significant_raw,
    
    -- Значимость с поправкой Bonferroni (5 тестов, α = 0.01)
    CASE WHEN ABS(z_statistic) > 2.576 THEN 'Да' ELSE 'Нет' END as significant_bonferroni

FROM pairwise_tests
ORDER BY z_statistic DESC;

-- 5.2 Поправка методом Холма (Holm's method)
WITH p_values AS (
    -- Здесь были бы точные p-values, но для примера используем категории
    SELECT 
        variant,
        z_statistic,
        ABS(z_statistic) as abs_z,
        ROW_NUMBER() OVER (ORDER BY ABS(z_statistic) DESC) as rank,
        COUNT(*) OVER () as total_tests
    FROM pairwise_tests
),

holm_correction AS (
    SELECT 
        variant,
        z_statistic,
        rank,
        -- Скорректированный уровень значимости для каждого ранга
        ROUND(0.05 / (total_tests + 1 - rank), 4) as alpha_holm,
        -- Критическое значение z для скорректированной альфы
        CASE 
            WHEN 0.05 / (total_tests + 1 - rank) < 0.01 THEN 2.576
            WHEN 0.05 / (total_tests + 1 - rank) < 0.05 THEN 1.96
            ELSE 1.645
        END as z_critical_holm
    FROM p_values
)

SELECT 
    rank as test_rank,
    variant,
    z_statistic,
    alpha_holm,
    z_critical_holm,
    CASE WHEN ABS(z_statistic) > z_critical_holm THEN 'Значимо' ELSE 'Не значимо' END as holm_result,
    CASE WHEN ABS(z_statistic) > z_critical_holm THEN 'Продолжить процедуру' ELSE 'Остановить' END as continue_testing
FROM holm_correction
ORDER BY rank;

-- Раздел 6: Качество рандомизации и диагностика
-- Проверка корректности проведения эксперимента

-- 6.1 A/A тест для проверки системы рандомизации
WITH aa_test AS (
    -- Создаем искусственный A/A тест, разбивая контрольную группу пополам
    SELECT 
        user_id,
        CASE 
            WHEN ABS(('x' || SUBSTR(MD5(user_id::TEXT || 'aa_test'), 1, 8))::BIT(32)::INT) % 2 = 0 
            THEN 'A1' 
            ELSE 'A2' 
        END as aa_group,
        converted
    FROM checkout_ab_test_results
    WHERE test_group = 'A'  -- Берем только контрольную группу
),

aa_comparison AS (
    SELECT 
        aa_group,
        COUNT(*) as sample_size,
        SUM(converted) as conversions,
        ROUND(AVG(converted::NUMERIC) * 100, 3) as conversion_rate_pct
    FROM aa_test
    GROUP BY aa_group
)

SELECT 
    aa_group,
    sample_size,
    conversions,
    conversion_rate_pct || '%' as conversion_rate,
    
    -- Разность между A1 и A2 (должна быть близка к 0)
    CASE WHEN aa_group = 'A2' THEN
        ROUND(conversion_rate_pct - LAG(conversion_rate_pct) OVER(ORDER BY aa_group), 3) || ' п.п.'
    END as difference_from_a1
    
FROM aa_comparison
ORDER BY aa_group;

-- 6.2 Проверка баланса групп по характеристикам пользователей
WITH balance_check AS (
    SELECT 
        test_group,
        COUNT(*) as total_users,
        
        -- Демографические характеристики
        ROUND(AVG(CASE WHEN age_group = '18-25' THEN 1.0 ELSE 0.0 END) * 100, 1) as pct_young,
        ROUND(AVG(CASE WHEN age_group = '26-35' THEN 1.0 ELSE 0.0 END) * 100, 1) as pct_middle_aged,
        ROUND(AVG(CASE WHEN gender = 'M' THEN 1.0 ELSE 0.0 END) * 100, 1) as pct_male,
        ROUND(AVG(CASE WHEN city = 'Москва' THEN 1.0 ELSE 0.0 END) * 100, 1) as pct_moscow,
        
        -- Технические характеристики
        ROUND(AVG(CASE WHEN device_type = 'mobile' THEN 1.0 ELSE 0.0 END) * 100, 1) as pct_mobile,
        ROUND(AVG(CASE WHEN traffic_source = 'organic' THEN 1.0 ELSE 0.0 END) * 100, 1) as pct_organic
    FROM segmented_ab_results
    GROUP BY test_group
)

SELECT 
    test_group,
    total_users,
    pct_young || '%' as young_users,
    pct_middle_aged || '%' as middle_aged_users, 
    pct_male || '%' as male_users,
    pct_moscow || '%' as moscow_users,
    pct_mobile || '%' as mobile_users,
    pct_organic || '%' as organic_traffic
FROM balance_check
ORDER BY test_group;

-- 6.3 Анализ выбывания пользователей (Sample Ratio Mismatch)
SELECT 
    'Планируемое распределение' as metric,
    '50.0%' as group_a,
    '50.0%' as group_b
UNION ALL
SELECT 
    'Фактическое распределение' as metric,
    ROUND(SUM(CASE WHEN test_group = 'A' THEN 1 ELSE 0 END)::NUMERIC / COUNT(*) * 100, 1) || '%' as group_a,
    ROUND(SUM(CASE WHEN test_group = 'B' THEN 1 ELSE 0 END)::NUMERIC / COUNT(*) * 100, 1) || '%' as group_b
FROM checkout_ab_test_results
UNION ALL
SELECT 
    'Отклонение от 50/50' as metric,
    ROUND(ABS(SUM(CASE WHEN test_group = 'A' THEN 1 ELSE 0 END)::NUMERIC / COUNT(*) - 0.5) * 100, 2) || ' п.п.' as group_a,
    ROUND(ABS(SUM(CASE WHEN test_group = 'B' THEN 1 ELSE 0 END)::NUMERIC / COUNT(*) - 0.5) * 100, 2) || ' п.п.' as group_b
FROM checkout_ab_test_results;

-- Раздел 7: Готовые шаблоны для мониторинга
-- Автоматические отчеты и алерты

-- 7.1 Ежедневный мониторинг A/B-теста
CREATE OR REPLACE VIEW ab_test_daily_monitor AS
WITH daily_stats AS (
    SELECT 
        CURRENT_DATE as report_date,
        stable_ab_group(user_id, 'checkout_test') as test_group,
        COUNT(*) as daily_users,
        SUM(converted) as daily_conversions,
        ROUND(AVG(converted::NUMERIC) * 100, 2) as daily_conversion_rate,
        
        -- Кумулятивная статистика
        (SELECT COUNT(*) FROM checkout_ab_test_results cb2 
         WHERE stable_ab_group(cb2.user_id, 'checkout_test') = stable_ab_group(cb1.user_id, 'checkout_test')) as total_users,
        
        (SELECT SUM(converted) FROM checkout_ab_test_results cb2 
         WHERE stable_ab_group(cb2.user_id, 'checkout_test') = stable_ab_group(cb1.user_id, 'checkout_test')) as total_conversions
    FROM checkout_ab_test_results cb1
    GROUP BY stable_ab_group(user_id, 'checkout_test')
),

significance_test AS (
    SELECT 
        a.daily_conversion_rate / 100.0 as p_a,
        b.daily_conversion_rate / 100.0 as p_b,
        a.total_users as n_a,
        b.total_users as n_b,
        ((a.total_conversions + b.total_conversions)::NUMERIC / (a.total_users + b.total_users)) as p_combined
    FROM daily_stats a, daily_stats b
    WHERE a.test_group = 'A' AND b.test_group = 'B'
)

SELECT 
    ds.*,
    CASE WHEN ds.test_group = 'B' THEN
        ROUND((st.p_b - st.p_a) * 100, 2) || ' п.п.'
    END as conversion_lift,
    
    CASE WHEN ds.test_group = 'B' THEN
        ROUND(
            (st.p_b - st.p_a) / 
            SQRT(st.p_combined * (1 - st.p_combined) * (1.0/st.n_a + 1.0/st.n_b))
        , 2)
    END as z_statistic,
    
    CASE WHEN ds.test_group = 'B' THEN
        CASE 
            WHEN ABS((st.p_b - st.p_a) / 
                    SQRT(st.p_combined * (1 - st.p_combined) * (1.0/st.n_a + 1.0/st.n_b))) > 1.96 
            THEN 'ЗНАЧИМО'
            ELSE 'Не значимо'
        END
    END as significance_status

FROM daily_stats ds
CROSS JOIN significance_test st;

-- 7.2 Алерты и аномалии
WITH anomaly_detection AS (
    SELECT 
        stable_ab_group(user_id, 'checkout_test') as test_group,
        COUNT(*) as sample_size,
        ROUND(AVG(converted::NUMERIC) * 100, 2) as conversion_rate,
        
        -- Проверяем аномалии
        CASE 
            WHEN COUNT(*) < 1000 THEN 'АЛЕРТ: Малый размер выборки'
            WHEN ABS(AVG(converted::NUMERIC) * 100 - 9.0) > 3.0 THEN 'АЛЕРТ: Конверсия вне ожидаемого диапазона'
            ELSE 'Норма'
        END as anomaly_alert
    FROM checkout_ab_test_results
    GROUP BY stable_ab_group(user_id, 'checkout_test')
)

SELECT * FROM anomaly_detection;

-- Примеры использования:
-- 1. Запустите скрипты рандомизации для настройки новых тестов
-- 2. Используйте раздел 2 для анализа завершенных экспериментов
-- 3. Применяйте раздел 3 для глубокого понимания эффектов по сегментам
-- 4. Мониторьте тесты с помощью раздела 4
-- 5. Учитывайте множественность тестирования с разделом 5
-- 6. Проверяйте качество экспериментов с разделом 6
-- 7. Автоматизируйте отчетность с разделом 7