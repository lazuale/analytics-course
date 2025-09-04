import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def create_sample_database():
    """Создание демонстрационной базы данных с продвинутыми примерами"""
    conn = sqlite3.connect('advanced_sales_data.db')
    cursor = conn.cursor()
    
    # Создание расширенной структуры таблиц
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        customer_id INTEGER PRIMARY KEY,
        customer_name TEXT NOT NULL,
        city TEXT NOT NULL,
        registration_date DATE,
        customer_segment TEXT,
        lifetime_value DECIMAL(10,2) DEFAULT 0
    );
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        order_id INTEGER PRIMARY KEY,
        customer_id INTEGER,
        order_date DATE NOT NULL,
        amount DECIMAL(10,2) NOT NULL,
        status TEXT DEFAULT 'Выполнен',
        channel TEXT DEFAULT 'Online',
        FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
    );
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        product_id INTEGER PRIMARY KEY,
        product_name TEXT NOT NULL,
        category_id INTEGER,
        price DECIMAL(10,2) NOT NULL,
        cost DECIMAL(10,2) NOT NULL,
        margin_percent DECIMAL(5,2),
        stock_quantity INTEGER DEFAULT 0
    );
    """)
    
    # Вставка расширенных демо-данных
    cursor.execute("SELECT COUNT(*) FROM customers")
    if cursor.fetchone()[0] == 0:
        print("📝 Создание расширенных демонстрационных данных...")
        
        # Клиенты с разными сегментами
        customers_data = [
            (1, 'Иван Петров', 'Москва', '2023-01-15', 'VIP', 50000.00),
            (2, 'Мария Сидорова', 'Санкт-Петербург', '2023-02-20', 'Premium', 25000.00),
            (3, 'Алексей Козлов', 'Москва', '2023-03-10', 'Regular', 15000.00),
            (4, 'Елена Морозова', 'Екатеринбург', '2023-04-05', 'VIP', 45000.00),
            (5, 'Дмитрий Волков', 'Новосибирск', '2023-05-12', 'New', 5000.00),
            (6, 'Анна Лебедева', 'Москва', '2023-06-18', 'Premium', 30000.00),
            (7, 'Сергей Новиков', 'Казань', '2023-07-22', 'Regular', 12000.00),
            (8, 'Ольга Федорова', 'Самара', '2023-08-30', 'At Risk', 8000.00)
        ]
        cursor.executemany(
            "INSERT INTO customers VALUES (?, ?, ?, ?, ?, ?)",
            customers_data
        )
        
        # Заказы с разными каналами и статусами
        orders_data = [
            (1, 1, '2023-02-01', 1500.50, 'Выполнен', 'Online'),
            (2, 1, '2023-03-15', 2300.75, 'Выполнен', 'Mobile'),
            (3, 2, '2023-03-01', 980.25, 'Выполнен', 'Online'),
            (4, 3, '2023-04-10', 3200.00, 'Выполнен', 'Store'),
            (5, 1, '2023-04-20', 1800.30, 'В обработке', 'Online'),
            (6, 4, '2023-05-05', 4500.80, 'Выполнен', 'Online'),
            (7, 2, '2023-05-15', 1200.90, 'Отменён', 'Mobile'),
            (8, 5, '2023-06-01', 2800.45, 'Выполнен', 'Store'),
            (9, 6, '2023-06-15', 5200.00, 'Выполнен', 'Online'),
            (10, 3, '2023-07-01', 1750.25, 'Выполнен', 'Mobile'),
            (11, 7, '2023-07-20', 890.50, 'Выполнен', 'Store'),
            (12, 4, '2023-08-10', 3800.75, 'Выполнен', 'Online'),
            (13, 8, '2023-09-05', 650.30, 'Выполнен', 'Mobile'),
            (14, 1, '2023-09-20', 2100.00, 'Выполнен', 'Online'),
            (15, 6, '2023-10-15', 4200.80, 'Выполнен', 'Store')
        ]
        cursor.executemany(
            "INSERT INTO orders VALUES (?, ?, ?, ?, ?, ?)",
            orders_data
        )
        
        # Товары с маржинальностью
        products_data = [
            (1, 'iPhone 14 Pro', 1, 79990.00, 65000.00, 18.75, 25),
            (2, 'MacBook Air M2', 1, 109990.00, 88000.00, 19.99, 15),
            (3, 'AirPods Pro', 1, 24990.00, 18000.00, 27.99, 50),
            (4, 'Nike Air Max', 2, 8990.00, 6500.00, 27.70, 30),
            (5, 'Adidas Ultraboost', 2, 12990.00, 9200.00, 29.18, 25),
            (6, 'Dyson V15', 3, 45990.00, 32000.00, 30.41, 10),
            (7, 'KitchenAid Mixer', 3, 35990.00, 25000.00, 30.53, 8)
        ]
        cursor.executemany(
            "INSERT INTO products VALUES (?, ?, ?, ?, ?, ?, ?)",
            products_data
        )
    
    conn.commit()
    return conn

def demonstrate_advanced_cte_techniques(conn):
    """Демонстрация продвинутых CTE техник"""
    
    print("🏗️ Демонстрация продвинутых CTE техник")
    print("="*50)
    
    # 1. Каскадные CTE с оконными функциями
    cascade_query = """
    WITH customer_base AS (
        -- Базовая статистика клиентов
        SELECT 
            c.customer_id,
            c.customer_name,
            c.city,
            c.customer_segment,
            COUNT(o.order_id) as total_orders,
            COALESCE(SUM(o.amount), 0) as total_spent,
            COALESCE(AVG(o.amount), 0) as avg_order_value,
            MAX(o.order_date) as last_order_date
        FROM customers c
        LEFT JOIN orders o ON c.customer_id = o.customer_id
        WHERE o.status = 'Выполнен' OR o.status IS NULL
        GROUP BY c.customer_id, c.customer_name, c.city, c.customer_segment
    ),
    customer_rankings AS (
        -- Ранжирование клиентов
        SELECT 
            *,
            ROW_NUMBER() OVER (ORDER BY total_spent DESC) as spending_rank,
            ROW_NUMBER() OVER (PARTITION BY city ORDER BY total_spent DESC) as city_rank,
            NTILE(4) OVER (ORDER BY total_spent) as spending_quartile,
            PERCENT_RANK() OVER (ORDER BY total_spent) as spending_percentile
        FROM customer_base
    ),
    customer_analytics AS (
        -- Аналитические вычисления
        SELECT 
            *,
            -- Сравнение со средними показателями
            total_spent - AVG(total_spent) OVER () as vs_avg_spending,
            total_orders - AVG(total_orders) OVER () as vs_avg_orders,
            -- Скользящие окна по рангу
            AVG(total_spent) OVER (
                ORDER BY spending_rank 
                ROWS BETWEEN 2 PRECEDING AND 2 FOLLOWING
            ) as peer_avg_spending,
            -- Кумулятивные показатели
            SUM(total_spent) OVER (ORDER BY spending_rank) as cumulative_revenue_contribution,
            SUM(total_spent) OVER (ORDER BY spending_rank) * 100.0 / 
            SUM(total_spent) OVER () as cumulative_revenue_percent
        FROM customer_rankings
    )
    SELECT 
        customer_name,
        city,
        customer_segment,
        total_spent,
        spending_rank,
        city_rank,
        spending_quartile,
        ROUND(spending_percentile * 100, 1) as percentile,
        ROUND(vs_avg_spending, 2) as vs_avg,
        ROUND(peer_avg_spending, 2) as peer_avg,
        ROUND(cumulative_revenue_percent, 2) as cum_revenue_pct
    FROM customer_analytics
    ORDER BY spending_rank;
    """
    
    cascade_df = pd.read_sql_query(cascade_query, conn)
    print(f"✅ Каскадные CTE: обработано {len(cascade_df)} клиентов")
    
    # 2. Рекурсивный CTE для временной последовательности
    recursive_query = """
    WITH RECURSIVE monthly_sequence AS (
        -- Базовый случай: первый месяц с данными
        SELECT 
            DATE('2023-01-01') as month_start,
            DATE('2023-01-31') as month_end,
            1 as month_number
        
        UNION ALL
        
        -- Рекурсивный случай: следующие месяцы
        SELECT 
            DATE(month_start, '+1 month'),
            DATE(DATE(month_start, '+1 month'), '+1 month', '-1 day'),
            month_number + 1
        FROM monthly_sequence
        WHERE month_number < 12
    ),
    monthly_metrics AS (
        SELECT 
            ms.month_start,
            ms.month_number,
            COUNT(o.order_id) as orders_count,
            COALESCE(SUM(o.amount), 0) as monthly_revenue,
            COUNT(DISTINCT o.customer_id) as active_customers
        FROM monthly_sequence ms
        LEFT JOIN orders o ON DATE(o.order_date, 'start of month') = ms.month_start
                            AND o.status = 'Выполнен'
        GROUP BY ms.month_start, ms.month_number
    ),
    cumulative_metrics AS (
        SELECT 
            *,
            SUM(monthly_revenue) OVER (ORDER BY month_number) as ytd_revenue,
            AVG(monthly_revenue) OVER (
                ORDER BY month_number 
                ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
            ) as ma_3_months,
            monthly_revenue - LAG(monthly_revenue) OVER (ORDER BY month_number) as mom_change,
            CASE 
                WHEN LAG(monthly_revenue) OVER (ORDER BY month_number) > 0 
                THEN (monthly_revenue - LAG(monthly_revenue) OVER (ORDER BY month_number)) * 100.0 / 
                     LAG(monthly_revenue) OVER (ORDER BY month_number)
                ELSE NULL
            END as mom_growth_percent
        FROM monthly_metrics
    )
    SELECT 
        strftime('%Y-%m', month_start) as month,
        orders_count,
        ROUND(monthly_revenue, 2) as revenue,
        active_customers,
        ROUND(ytd_revenue, 2) as ytd_revenue,
        ROUND(ma_3_months, 2) as ma_3_months,
        ROUND(mom_change, 2) as mom_change,
        ROUND(mom_growth_percent, 2) as mom_growth_pct
    FROM cumulative_metrics
    ORDER BY month_number;
    """
    
    recursive_df = pd.read_sql_query(recursive_query, conn)
    print(f"✅ Рекурсивный CTE: создана последовательность из {len(recursive_df)} месяцев")
    
    return cascade_df, recursive_df

def demonstrate_complex_subqueries(conn):
    """Демонстрация сложных подзапросов"""
    
    print("\n🔍 Демонстрация сложных подзапросов")
    print("="*50)
    
    # 1. Многоуровневые коррелированные подзапросы
    complex_subquery = """
    SELECT 
        o1.order_id,
        o1.customer_id,
        c.customer_name,
        o1.order_date,
        o1.amount,
        
        -- Подзапрос: позиция заказа среди заказов клиента
        (SELECT COUNT(*) + 1 
         FROM orders o2 
         WHERE o2.customer_id = o1.customer_id 
           AND o2.amount > o1.amount 
           AND o2.status = 'Выполнен') as order_rank_for_customer,
        
        -- Подзапрос: накопительная сумма заказов клиента на дату
        (SELECT SUM(o3.amount) 
         FROM orders o3 
         WHERE o3.customer_id = o1.customer_id 
           AND o3.order_date <= o1.order_date 
           AND o3.status = 'Выполнен') as cumulative_spent_to_date,
        
        -- Подзапрос: средний чек клиента до этого заказа
        (SELECT AVG(o4.amount) 
         FROM orders o4 
         WHERE o4.customer_id = o1.customer_id 
           AND o4.order_date < o1.order_date 
           AND o4.status = 'Выполнен') as avg_previous_orders,
        
        -- Подзапрос: дней с предыдущего заказа
        (SELECT MIN(julianday(o1.order_date) - julianday(o5.order_date))
         FROM orders o5 
         WHERE o5.customer_id = o1.customer_id 
           AND o5.order_date < o1.order_date 
           AND o5.status = 'Выполнен') as days_since_previous_order,
        
        -- Подзапрос: сравнение с городским средним
        CASE 
            WHEN o1.amount > (
                SELECT AVG(ord.amount) 
                FROM orders ord 
                JOIN customers cust ON ord.customer_id = cust.customer_id 
                WHERE cust.city = c.city 
                  AND ord.status = 'Выполнен'
            ) THEN 'Выше среднего по городу'
            ELSE 'Ниже среднего по городу'
        END as vs_city_average
    FROM orders o1
    JOIN customers c ON o1.customer_id = c.customer_id
    WHERE o1.status = 'Выполнен'
      AND EXISTS (
          -- Подзапрос: только клиенты с более чем одним заказом
          SELECT 1 
          FROM orders o_check 
          WHERE o_check.customer_id = o1.customer_id 
            AND o_check.status = 'Выполнен' 
          GROUP BY o_check.customer_id 
          HAVING COUNT(*) > 1
      )
    ORDER BY o1.customer_id, o1.order_date;
    """
    
    subquery_df = pd.read_sql_query(complex_subquery, conn)
    print(f"✅ Сложные подзапросы: проанализировано {len(subquery_df)} заказов")
    
    # 2. Подзапросы с ANY/ALL
    any_all_query = """
    SELECT 
        c.customer_name,
        c.city,
        c.customer_segment,
        -- Максимальный заказ клиента
        (SELECT MAX(amount) FROM orders WHERE customer_id = c.customer_id AND status = 'Выполнен') as max_order,
        
        -- Проверка: есть ли заказ больше чем ANY заказ VIP клиентов из других городов
        CASE 
            WHEN (SELECT MAX(amount) FROM orders WHERE customer_id = c.customer_id AND status = 'Выполнен') > ANY (
                SELECT o.amount 
                FROM orders o 
                JOIN customers c2 ON o.customer_id = c2.customer_id 
                WHERE c2.customer_segment = 'VIP' 
                  AND c2.city != c.city 
                  AND o.status = 'Выполнен'
            ) THEN 'Превышает заказы некоторых VIP'
            ELSE 'Не превышает заказы VIP'
        END as vs_vip_any,
        
        -- Проверка: больше ли средний чек чем ALL заказы New сегмента
        CASE 
            WHEN (SELECT AVG(amount) FROM orders WHERE customer_id = c.customer_id AND status = 'Выполнен') > ALL (
                SELECT o.amount 
                FROM orders o 
                JOIN customers c2 ON o.customer_id = c2.customer_id 
                WHERE c2.customer_segment = 'New' 
                  AND o.status = 'Выполнен'
            ) THEN 'Средний чек выше всех New клиентов'
            ELSE 'Средний чек не выше всех New клиентов'
        END as vs_new_all
    FROM customers c
    WHERE EXISTS (
        SELECT 1 FROM orders WHERE customer_id = c.customer_id AND status = 'Выполнен'
    )
    ORDER BY c.customer_segment, c.customer_name;
    """
    
    any_all_df = pd.read_sql_query(any_all_query, conn)
    print(f"✅ ANY/ALL подзапросы: проанализировано {len(any_all_df)} клиентов")
    
    return subquery_df, any_all_df

def demonstrate_advanced_joins(conn):
    """Демонстрация продвинутых JOIN техник"""
    
    print("\n🔗 Демонстрация продвинутых JOIN техник")  
    print("="*50)
    
    # 1. Self JOIN для временных сравнений
    self_join_query = """
    SELECT 
        o1.order_id as current_order,
        o1.customer_id,
        c.customer_name,
        o1.order_date as current_date,
        o1.amount as current_amount,
        o2.order_id as previous_order,
        o2.order_date as previous_date,
        o2.amount as previous_amount,
        o1.amount - o2.amount as amount_change,
        julianday(o1.order_date) - julianday(o2.order_date) as days_between_orders,
        CASE 
            WHEN o1.amount > o2.amount THEN 'Увеличение'
            WHEN o1.amount < o2.amount THEN 'Уменьшение'
            ELSE 'Без изменений'
        END as trend
    FROM orders o1
    JOIN customers c ON o1.customer_id = c.customer_id
    LEFT JOIN orders o2 ON o1.customer_id = o2.customer_id 
                        AND o2.order_date = (
                            SELECT MAX(order_date) 
                            FROM orders o3 
                            WHERE o3.customer_id = o1.customer_id 
                              AND o3.order_date < o1.order_date
                              AND o3.status = 'Выполнен'
                        )
    WHERE o1.status = 'Выполнен'
    ORDER BY o1.customer_id, o1.order_date;
    """
    
    self_join_df = pd.read_sql_query(self_join_query, conn)
    print(f"✅ Self JOIN: проанализированы тренды для {len(self_join_df)} заказов")
    
    # 2. Множественные LEFT JOIN с агрегацией
    multiple_join_query = """
    SELECT 
        c.customer_id,
        c.customer_name,
        c.city,
        c.customer_segment,
        
        -- Статистика заказов
        COUNT(DISTINCT o.order_id) as total_orders,
        COALESCE(SUM(CASE WHEN o.status = 'Выполнен' THEN o.amount END), 0) as completed_revenue,
        COALESCE(SUM(CASE WHEN o.status = 'В обработке' THEN o.amount END), 0) as pending_revenue,
        COALESCE(SUM(CASE WHEN o.status = 'Отменён' THEN o.amount END), 0) as cancelled_revenue,
        
        -- Канальная статистика
        COUNT(CASE WHEN o.channel = 'Online' THEN 1 END) as online_orders,
        COUNT(CASE WHEN o.channel = 'Mobile' THEN 1 END) as mobile_orders,
        COUNT(CASE WHEN o.channel = 'Store' THEN 1 END) as store_orders,
        
        -- Временная статистика
        MIN(o.order_date) as first_order_date,
        MAX(o.order_date) as last_order_date,
        
        -- Расчетные показатели
        CASE 
            WHEN COUNT(DISTINCT o.order_id) > 0 
            THEN ROUND(SUM(CASE WHEN o.status = 'Выполнен' THEN o.amount ELSE 0 END) / 
                      NULLIF(COUNT(CASE WHEN o.status = 'Выполнен' THEN 1 END), 0), 2)
            ELSE 0
        END as avg_completed_order_value,
        
        -- Статус активности
        CASE 
            WHEN MAX(o.order_date) >= DATE('now', '-30 days') THEN 'Активный'
            WHEN MAX(o.order_date) >= DATE('now', '-90 days') THEN 'Умеренно активный'
            WHEN MAX(o.order_date) IS NOT NULL THEN 'Неактивный'
            ELSE 'Нет заказов'
        END as activity_status
        
    FROM customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.customer_name, c.city, c.customer_segment
    ORDER BY completed_revenue DESC;
    """
    
    multiple_join_df = pd.read_sql_query(multiple_join_query, conn)
    print(f"✅ Множественные JOIN: создан профиль для {len(multiple_join_df)} клиентов")
    
    return self_join_df, multiple_join_df

def create_comprehensive_business_report(conn):
    """Создание комплексного бизнес-отчета с использованием всех техник"""
    
    print("\n📊 Создание комплексного бизнес-отчета")
    print("="*50)
    
    comprehensive_query = """
    WITH 
    -- CTE 1: Базовые метрики клиентов
    customer_base AS (
        SELECT 
            c.customer_id,
            c.customer_name,
            c.city,
            c.customer_segment,
            c.registration_date,
            COUNT(o.order_id) as total_orders,
            SUM(CASE WHEN o.status = 'Выполнен' THEN o.amount ELSE 0 END) as lifetime_value,
            AVG(CASE WHEN o.status = 'Выполнен' THEN o.amount END) as avg_order_value,
            MAX(CASE WHEN o.status = 'Выполнен' THEN o.order_date END) as last_order_date,
            COUNT(DISTINCT o.channel) as channels_used
        FROM customers c
        LEFT JOIN orders o ON c.customer_id = o.customer_id
        GROUP BY c.customer_id, c.customer_name, c.city, c.customer_segment, c.registration_date
    ),
    
    -- CTE 2: Сегментация и ранжирование
    customer_segments AS (
        SELECT 
            *,
            -- Ранжирование
            ROW_NUMBER() OVER (ORDER BY lifetime_value DESC) as value_rank,
            ROW_NUMBER() OVER (PARTITION BY city ORDER BY lifetime_value DESC) as city_rank,
            NTILE(3) OVER (ORDER BY lifetime_value) as value_tercile,
            
            -- Актуальность
            CASE 
                WHEN last_order_date >= DATE('now', '-30 days') THEN 'Recent'
                WHEN last_order_date >= DATE('now', '-90 days') THEN 'Moderate'
                WHEN last_order_date IS NOT NULL THEN 'Old'
                ELSE 'Never Ordered'
            END as recency_segment,
            
            -- Омниканальность
            CASE 
                WHEN channels_used >= 3 THEN 'Omnichannel'
                WHEN channels_used = 2 THEN 'Multichannel'
                WHEN channels_used = 1 THEN 'Single Channel'
                ELSE 'No Orders'
            END as channel_behavior
        FROM customer_base
    ),
    
    -- CTE 3: Городская аналитика
    city_analytics AS (
        SELECT 
            city,
            COUNT(*) as total_customers,
            COUNT(CASE WHEN lifetime_value > 0 THEN 1 END) as active_customers,
            AVG(lifetime_value) as avg_city_ltv,
            SUM(lifetime_value) as city_total_revenue,
            -- Подзапрос: топ клиент города
            (SELECT customer_name 
             FROM customer_segments cs2 
             WHERE cs2.city = cs.city 
             ORDER BY cs2.lifetime_value DESC 
             LIMIT 1) as top_customer
        FROM customer_segments cs
        GROUP BY city
    ),
    
    -- CTE 4: Финальная аналитика
    final_analytics AS (
        SELECT 
            cs.*,
            ca.avg_city_ltv,
            ca.city_total_revenue,
            ca.top_customer as city_top_customer,
            
            -- Сравнительные показатели
            ROUND(cs.lifetime_value / NULLIF(ca.avg_city_ltv, 0), 2) as vs_city_avg_ratio,
            ROUND(cs.lifetime_value * 100.0 / ca.city_total_revenue, 2) as city_revenue_share,
            
            -- Комплексная сегментация
            CASE 
                WHEN cs.customer_segment = 'VIP' AND cs.recency_segment = 'Recent' THEN 'Champion'
                WHEN cs.customer_segment = 'VIP' AND cs.recency_segment != 'Recent' THEN 'At Risk VIP'
                WHEN cs.lifetime_value > ca.avg_city_ltv AND cs.recency_segment = 'Recent' THEN 'Rising Star'
                WHEN cs.lifetime_value > 0 AND cs.recency_segment = 'Recent' THEN 'Active Regular'
                WHEN cs.lifetime_value > 0 AND cs.recency_segment != 'Recent' THEN 'Dormant'
                ELSE 'Prospect'
            END as business_segment
        FROM customer_segments cs
        LEFT JOIN city_analytics ca ON cs.city = ca.city
    )
    
    -- Финальный запрос с подзапросами для дополнительного контекста
    SELECT 
        customer_name,
        city,
        customer_segment,
        business_segment,
        recency_segment,
        channel_behavior,
        total_orders,
        ROUND(lifetime_value, 0) as lifetime_value,
        value_rank,
        city_rank,
        vs_city_avg_ratio,
        city_revenue_share,
        
        -- Подзапрос: количество клиентов в том же бизнес-сегменте
        (SELECT COUNT(*) 
         FROM final_analytics fa2 
         WHERE fa2.business_segment = fa.business_segment) as segment_peers,
        
        -- Подзапрос: процентиль по lifetime value
        ROUND((SELECT COUNT(*) * 100.0 / (SELECT COUNT(*) FROM final_analytics)
         FROM final_analytics fa3 
         WHERE fa3.lifetime_value < fa.lifetime_value), 1) as ltv_percentile
        
    FROM final_analytics fa
    ORDER BY lifetime_value DESC;
    """
    
    comprehensive_df = pd.read_sql_query(comprehensive_query, conn)
    print(f"✅ Комплексный отчет: создан профиль для {len(comprehensive_df)} клиентов")
    
    # Сводная статистика по бизнес-сегментам
    segment_summary = comprehensive_df.groupby('business_segment').agg({
        'customer_name': 'count',
        'lifetime_value': ['sum', 'mean'],
        'total_orders': 'mean',
        'city_revenue_share': 'mean'
    }).round(2)
    
    print(f"\n📈 Распределение по бизнес-сегментам:")
    for segment in comprehensive_df['business_segment'].unique():
        count = len(comprehensive_df[comprehensive_df['business_segment'] == segment])
        avg_ltv = comprehensive_df[comprehensive_df['business_segment'] == segment]['lifetime_value'].mean()
        print(f"   • {segment}: {count} клиентов, средний LTV: {avg_ltv:.0f} руб.")
    
    return comprehensive_df, segment_summary

def main():
    """Основная функция демонстрации продвинутых SQL техник"""
    print("🎓 Демонстрация продвинутых SQL техник в Python")
    print("="*60)
    
    # Создание демонстрационной базы данных
    conn = create_sample_database()
    
    try:
        # 1. Продвинутые CTE техники
        cascade_df, recursive_df = demonstrate_advanced_cte_techniques(conn)
        
        # 2. Сложные подзапросы
        subquery_df, any_all_df = demonstrate_complex_subqueries(conn)
        
        # 3. Продвинутые JOIN техники
        self_join_df, multiple_join_df = demonstrate_advanced_joins(conn)
        
        # 4. Комплексный бизнес-отчет
        comprehensive_df, segment_summary = create_comprehensive_business_report(conn)
        
        # Сохранение результатов
        results = {
            'cascade_cte': cascade_df,
            'recursive_cte': recursive_df,
            'complex_subqueries': subquery_df,
            'any_all_subqueries': any_all_df,
            'self_join_analysis': self_join_df,
            'multiple_join_profiles': multiple_join_df,
            'comprehensive_report': comprehensive_df
        }
        
        for name, df in results.items():
            filename = f"{name}_results.csv"
            df.to_csv(filename, index=False, sep=';')
            print(f"💾 Сохранён файл: {filename}")
        
        print(f"\n🎉 Демонстрация завершена успешно!")
        print(f"📊 Создано {len(results)} аналитических отчётов")
        print(f"🗃️ Все результаты сохранены в CSV файлы")
        
        # Итоговая статистика
        print(f"\n📈 Итоговая статистика обработки:")
        print(f"   • Каскадные CTE: {len(cascade_df)} записей")
        print(f"   • Рекурсивные CTE: {len(recursive_df)} записей")
        print(f"   • Сложные подзапросы: {len(subquery_df)} записей")
        print(f"   • ANY/ALL запросы: {len(any_all_df)} записей")
        print(f"   • Self JOIN анализ: {len(self_join_df)} записей")
        print(f"   • Профили клиентов: {len(multiple_join_df)} записей")
        print(f"   • Комплексный отчёт: {len(comprehensive_df)} записей")
        
    except Exception as e:
        print(f"❌ Ошибка при выполнении демонстрации: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        conn.close()

if __name__ == "__main__":
    main()