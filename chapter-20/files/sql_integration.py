import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime

# Установка русского шрифта для matplotlib
plt.rcParams['font.family'] = 'DejaVu Sans'

def connect_to_db():
    """Создание подключения к SQLite базе данных"""
    conn = sqlite3.connect('sales_data.db')
    return conn

def execute_sql_query(conn, query):
    """Выполнение SQL запроса и возврат DataFrame"""
    return pd.read_sql_query(query, conn)

def create_database_from_csv():
    """Создание базы данных из CSV файлов"""
    conn = sqlite3.connect('sales_data.db')
    
    # Загрузка CSV файлов
    customers_df = pd.read_csv('customers.csv', sep=';')
    categories_df = pd.read_csv('categories.csv', sep=';')
    products_df = pd.read_csv('products.csv', sep=';')
    orders_df = pd.read_csv('orders.csv', sep=';')
    order_details_df = pd.read_csv('order_details.csv', sep=';')
    
    # Замена запятых на точки в числовых полях
    products_df['price'] = products_df['price'].str.replace(',', '.').astype(float)
    orders_df['amount'] = orders_df['amount'].str.replace(',', '.').astype(float)
    order_details_df['unit_price'] = order_details_df['unit_price'].str.replace(',', '.').astype(float)
    order_details_df['discount'] = order_details_df['discount'].str.replace(',', '.').astype(float)
    
    # Создание таблиц в базе данных
    customers_df.to_sql('customers', conn, if_exists='replace', index=False)
    categories_df.to_sql('categories', conn, if_exists='replace', index=False)
    products_df.to_sql('products', conn, if_exists='replace', index=False)
    orders_df.to_sql('orders', conn, if_exists='replace', index=False)
    order_details_df.to_sql('order_details', conn, if_exists='replace', index=False)
    
    print("✅ База данных создана из CSV файлов")
    return conn

def monthly_sales_analysis(conn):
    """Анализ месячных продаж с использованием CTE"""
    query = """
    WITH monthly_sales AS (
        SELECT 
            strftime('%Y-%m', order_date) as month,
            SUM(amount) as total_sales,
            COUNT(*) as order_count,
            AVG(amount) as avg_order_value,
            COUNT(DISTINCT customer_id) as unique_customers
        FROM orders
        WHERE status = 'Выполнен'
          AND order_date >= date('now', '-12 months')
        GROUP BY strftime('%Y-%m', order_date)
    ),
    sales_with_growth AS (
        SELECT *,
            LAG(total_sales) OVER (ORDER BY month) as prev_month_sales,
            total_sales - LAG(total_sales) OVER (ORDER BY month) as sales_growth,
            ROUND(
                (total_sales - LAG(total_sales) OVER (ORDER BY month)) * 100.0 / 
                NULLIF(LAG(total_sales) OVER (ORDER BY month), 0), 2
            ) as growth_percent
        FROM monthly_sales
    )
    SELECT * FROM sales_with_growth
    ORDER BY month;
    """
    
    df = execute_sql_query(conn, query)
    
    # Визуализация
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('📈 Анализ месячных продаж', fontsize=16, fontweight='bold')
    
    # График продаж
    axes[0,0].plot(df['month'], df['total_sales'], marker='o', linewidth=3, color='#2E86AB')
    axes[0,0].set_title('💰 Динамика продаж по месяцам')
    axes[0,0].set_xlabel('Месяц')
    axes[0,0].set_ylabel('Общие продажи (руб.)')
    axes[0,0].tick_params(axis='x', rotation=45)
    axes[0,0].grid(True, alpha=0.3)
    
    # График количества заказов
    axes[0,1].bar(df['month'], df['order_count'], color='#A23B72', alpha=0.7)
    axes[0,1].set_title('📊 Количество заказов по месяцам')
    axes[0,1].set_xlabel('Месяц')
    axes[0,1].set_ylabel('Количество заказов')
    axes[0,1].tick_params(axis='x', rotation=45)
    
    # График среднего чека
    axes[1,0].plot(df['month'], df['avg_order_value'], marker='s', color='#F18F01', linewidth=2)
    axes[1,0].set_title('💎 Средний чек по месяцам')
    axes[1,0].set_xlabel('Месяц')
    axes[1,0].set_ylabel('Средний чек (руб.)')
    axes[1,0].tick_params(axis='x', rotation=45)
    axes[1,0].grid(True, alpha=0.3)
    
    # График роста продаж
    colors = ['green' if x >= 0 else 'red' for x in df['growth_percent'].fillna(0)]
    axes[1,1].bar(df['month'][1:], df['growth_percent'][1:], color=colors[1:], alpha=0.7)
    axes[1,1].set_title('📈 Рост продаж месяц к месяцу (%)')
    axes[1,1].set_xlabel('Месяц')
    axes[1,1].set_ylabel('Рост (%)')
    axes[1,1].tick_params(axis='x', rotation=45)
    axes[1,1].axhline(y=0, color='black', linestyle='-', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('monthly_sales_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    return df

def customer_segmentation_analysis(conn):
    """RFM анализ клиентов с использованием подзапросов и CTE"""
    query = """
    WITH customer_rfm_base AS (
        SELECT 
            c.customer_id,
            c.customer_name,
            c.city,
            -- Recency: дни с последнего заказа
            COALESCE(
                julianday('now') - julianday(MAX(o.order_date)), 
                julianday('now') - julianday(c.registration_date)
            ) as recency_days,
            -- Frequency: количество заказов
            COUNT(CASE WHEN o.status = 'Выполнен' THEN o.order_id END) as frequency,
            -- Monetary: общая сумма заказов
            COALESCE(SUM(CASE WHEN o.status = 'Выполнен' THEN o.amount ELSE 0 END), 0) as monetary
        FROM customers c
        LEFT JOIN orders o ON c.customer_id = o.customer_id
        GROUP BY c.customer_id, c.customer_name, c.city, c.registration_date
    ),
    customer_rfm_scores AS (
        SELECT *,
            -- RFM скоры (1-5, где 5 лучше)
            CASE 
                WHEN recency_days <= 30 THEN 5
                WHEN recency_days <= 90 THEN 4
                WHEN recency_days <= 180 THEN 3
                WHEN recency_days <= 365 THEN 2
                ELSE 1
            END as r_score,
            CASE 
                WHEN frequency >= 8 THEN 5
                WHEN frequency >= 5 THEN 4
                WHEN frequency >= 3 THEN 3
                WHEN frequency >= 1 THEN 2
                ELSE 1
            END as f_score,
            CASE 
                WHEN monetary >= 20000 THEN 5
                WHEN monetary >= 10000 THEN 4
                WHEN monetary >= 5000 THEN 3
                WHEN monetary >= 1000 THEN 2
                ELSE 1
            END as m_score
        FROM customer_rfm_base
    ),
    customer_segments AS (
        SELECT *,
            -- Общий RFM сегмент
            CASE 
                WHEN r_score >= 4 AND f_score >= 4 AND m_score >= 4 THEN 'Champions'
                WHEN r_score >= 3 AND f_score >= 3 AND m_score >= 3 THEN 'Loyal Customers'
                WHEN r_score >= 4 AND f_score <= 2 THEN 'New Customers'
                WHEN r_score <= 2 AND f_score >= 3 AND m_score >= 3 THEN 'At Risk'
                WHEN r_score <= 2 AND f_score <= 2 THEN 'Lost'
                ELSE 'Others'
            END as rfm_segment
        FROM customer_rfm_scores
    )
    SELECT 
        customer_name,
        city,
        frequency,
        ROUND(monetary, 0) as monetary,
        ROUND(recency_days, 0) as recency_days,
        r_score,
        f_score,
        m_score,
        rfm_segment
    FROM customer_segments;
    """
    
    df = execute_sql_query(conn, query)
    
    # Анализ сегментов
    segment_analysis = df.groupby('rfm_segment').agg({
        'customer_name': 'count',
        'monetary': ['mean', 'sum'],
        'frequency': 'mean',
        'recency_days': 'mean'
    }).round(2)
    
    # Визуализация сегментов
    plt.figure(figsize=(16, 12))
    
    # Распределение по сегментам
    plt.subplot(2, 3, 1)
    segment_counts = df['rfm_segment'].value_counts()
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FECA57', '#FF9FF3']
    plt.bar(segment_counts.index, segment_counts.values, color=colors[:len(segment_counts)])
    plt.title('👥 Распределение клиентов по сегментам')
    plt.xlabel('RFM Сегмент')
    plt.ylabel('Количество клиентов')
    plt.xticks(rotation=45)
    
    # Scatter plot R vs F, цвет = M
    plt.subplot(2, 3, 2)
    scatter = plt.scatter(df['r_score'], df['f_score'], 
                         c=df['m_score'], cmap='viridis', alpha=0.6, s=50)
    plt.colorbar(scatter, label='Monetary Score')
    plt.title('🎯 RFM Скоры: Recency vs Frequency')
    plt.xlabel('Recency Score')
    plt.ylabel('Frequency Score')
    
    # Boxplot монетарной ценности по сегментам
    plt.subplot(2, 3, 3)
    segments_for_box = df[df['monetary'] > 0]['rfm_segment'].unique()
    data_for_box = [df[df['rfm_segment'] == seg]['monetary'].values for seg in segments_for_box]
    plt.boxplot(data_for_box, labels=segments_for_box)
    plt.title('💰 Распределение трат по сегментам')
    plt.xlabel('RFM Сегмент')
    plt.ylabel('Общие траты (руб.)')
    plt.xticks(rotation=45)
    
    # Средние показатели по сегментам
    plt.subplot(2, 3, 4)
    segment_means = df.groupby('rfm_segment')[['recency_days', 'frequency', 'monetary']].mean()
    segment_means_norm = segment_means / segment_means.max()  # Нормализация для визуализации
    
    x = np.arange(len(segment_means.index))
    width = 0.25
    plt.bar(x - width, segment_means_norm['recency_days'], width, label='Recency (норм)', alpha=0.7)
    plt.bar(x, segment_means_norm['frequency'], width, label='Frequency (норм)', alpha=0.7)
    plt.bar(x + width, segment_means_norm['monetary'], width, label='Monetary (норм)', alpha=0.7)
    
    plt.title('📊 Нормализованные средние показатели')
    plt.xlabel('RFM Сегмент')
    plt.ylabel('Нормализованные значения')
    plt.xticks(x, segment_means.index, rotation=45)
    plt.legend()
    
    # География сегментов
    plt.subplot(2, 3, 5)
    city_segments = pd.crosstab(df['city'], df['rfm_segment'])
    city_segments.plot(kind='bar', stacked=True, ax=plt.gca(), colormap='Set3')
    plt.title('🌍 География RFM сегментов')
    plt.xlabel('Город')
    plt.ylabel('Количество клиентов')
    plt.xticks(rotation=45)
    plt.legend(title='RFM Сегмент', bbox_to_anchor=(1.05, 1), loc='upper left')
    
    # Таблица ключевых метрик
    plt.subplot(2, 3, 6)
    plt.axis('off')
    
    summary_text = "📋 КЛЮЧЕВЫЕ МЕТРИКИ ПО СЕГМЕНТАМ\n\n"
    for segment in df['rfm_segment'].unique():
        seg_data = df[df['rfm_segment'] == segment]
        if len(seg_data) > 0:
            summary_text += f"{segment}:\n"
            summary_text += f"  👥 Клиентов: {len(seg_data)}\n"
            summary_text += f"  💰 Ср. трата: {seg_data['monetary'].mean():.0f} руб.\n"
            summary_text += f"  📦 Ср. заказов: {seg_data['frequency'].mean():.1f}\n"
            summary_text += f"  ⏰ Дней с заказа: {seg_data['recency_days'].mean():.0f}\n\n"
    
    plt.text(0.1, 0.9, summary_text, fontsize=10, verticalalignment='top', 
             transform=plt.gca().transAxes,
             bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.7))
    
    plt.tight_layout()
    plt.savefig('customer_segmentation.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    return df, segment_analysis

def complex_join_analysis(conn):
    """Комплексный анализ с использованием множественных JOIN"""
    query = """
    WITH product_performance AS (
        SELECT 
            p.product_id,
            p.product_name,
            c.category_name,
            p.brand,
            COUNT(DISTINCT od.order_id) as times_ordered,
            SUM(od.quantity) as total_quantity_sold,
            SUM(od.quantity * od.unit_price * (1 - od.discount/100)) as total_revenue,
            AVG(od.unit_price) as avg_selling_price,
            p.price as catalog_price,
            p.stock_quantity
        FROM products p
        LEFT JOIN categories c ON p.category_id = c.category_id
        LEFT JOIN order_details od ON p.product_id = od.product_id
        LEFT JOIN orders o ON od.order_id = o.order_id
        WHERE o.status = 'Выполнен' OR o.status IS NULL
        GROUP BY p.product_id, p.product_name, c.category_name, p.brand, p.price, p.stock_quantity
    ),
    category_totals AS (
        SELECT 
            category_name,
            SUM(total_revenue) as category_revenue
        FROM product_performance
        WHERE total_revenue > 0
        GROUP BY category_name
    )
    SELECT 
        pp.product_name,
        pp.category_name,
        pp.brand,
        COALESCE(pp.times_ordered, 0) as times_ordered,
        COALESCE(pp.total_quantity_sold, 0) as total_quantity_sold,
        COALESCE(pp.total_revenue, 0) as total_revenue,
        COALESCE(pp.avg_selling_price, pp.catalog_price) as avg_selling_price,
        pp.catalog_price,
        pp.stock_quantity,
        -- Доля в выручке категории
        CASE 
            WHEN pp.total_revenue > 0 AND ct.category_revenue > 0 
            THEN ROUND(pp.total_revenue * 100.0 / ct.category_revenue, 2)
            ELSE 0
        END as category_share_percent,
        -- Статус товара
        CASE 
            WHEN pp.total_revenue = 0 THEN 'Не продавался'
            WHEN pp.total_revenue >= (
                SELECT AVG(total_revenue) * 1.5 
                FROM product_performance 
                WHERE total_revenue > 0
            ) THEN 'Хит продаж'
            WHEN pp.total_revenue >= (
                SELECT AVG(total_revenue) 
                FROM product_performance 
                WHERE total_revenue > 0
            ) THEN 'Популярный'
            ELSE 'Обычный'
        END as product_status
    FROM product_performance pp
    LEFT JOIN category_totals ct ON pp.category_name = ct.category_name
    ORDER BY pp.total_revenue DESC;
    """
    
    df = execute_sql_query(conn, query)
    
    # Анализ по категориям
    category_analysis = df.groupby('category_name').agg({
        'product_name': 'count',
        'total_revenue': 'sum',
        'total_quantity_sold': 'sum',
        'times_ordered': 'sum'
    }).round(2)
    
    print("\n📊 Анализ производительности товаров:")
    print("="*60)
    print(f"Всего товаров: {len(df)}")
    print(f"Товаров с продажами: {len(df[df['total_revenue'] > 0])}")
    print(f"Товаров без продаж: {len(df[df['total_revenue'] == 0])}")
    
    print("\n🏆 Топ-5 товаров по выручке:")
    top_products = df[df['total_revenue'] > 0].head(5)
    for idx, row in top_products.iterrows():
        print(f"  {row['product_name']} ({row['category_name']}) - {row['total_revenue']:.2f} руб.")
    
    return df, category_analysis

def demonstrate_advanced_sql_techniques(conn):
    """Демонстрация продвинутых SQL техник"""
    
    # 1. Коррелированные подзапросы
    correlated_query = """
    SELECT 
        c.customer_name,
        c.city,
        o.order_date,
        o.amount,
        -- Подзапрос: средний чек клиента
        (SELECT AVG(o2.amount) 
         FROM orders o2 
         WHERE o2.customer_id = c.customer_id 
           AND o2.status = 'Выполнен') as customer_avg_order,
        -- Подзапрос: ранг заказа среди заказов клиента
        (SELECT COUNT(*) + 1 
         FROM orders o3 
         WHERE o3.customer_id = c.customer_id 
           AND o3.amount > o.amount 
           AND o3.status = 'Выполнен') as order_rank_for_customer
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    WHERE o.status = 'Выполнен'
      AND o.amount > (
          SELECT AVG(o4.amount) 
          FROM orders o4 
          WHERE o4.customer_id = c.customer_id 
            AND o4.status = 'Выполнен'
      )
    ORDER BY c.customer_name, o.order_date;
    """
    
    correlated_df = execute_sql_query(conn, correlated_query)
    
    # 2. Рекурсивный CTE для иерархии (имитация)
    hierarchy_query = """
    WITH RECURSIVE date_series AS (
        -- Базовый случай: начальная дата
        SELECT DATE('2023-01-01') as analysis_date, 0 as days_offset
        
        UNION ALL
        
        -- Рекурсивный случай: добавляем дни
        SELECT 
            DATE(analysis_date, '+7 day'),
            days_offset + 7
        FROM date_series
        WHERE days_offset < 365
    ),
    weekly_sales AS (
        SELECT 
            ds.analysis_date,
            ds.days_offset,
            COALESCE(SUM(o.amount), 0) as weekly_sales,
            COUNT(o.order_id) as weekly_orders
        FROM date_series ds
        LEFT JOIN orders o ON DATE(o.order_date) = ds.analysis_date
                           AND o.status = 'Выполнен'
        GROUP BY ds.analysis_date, ds.days_offset
    )
    SELECT 
        analysis_date,
        weekly_sales,
        weekly_orders,
        SUM(weekly_sales) OVER (ORDER BY analysis_date) as cumulative_sales,
        AVG(weekly_sales) OVER (
            ORDER BY analysis_date 
            ROWS BETWEEN 3 PRECEDING AND CURRENT ROW
        ) as moving_avg_4weeks
    FROM weekly_sales
    ORDER BY analysis_date;
    """
    
    hierarchy_df = execute_sql_query(conn, hierarchy_query)
    
    # 3. Сложный CTE с EXISTS
    complex_cte_query = """
    WITH high_value_customers AS (
        SELECT customer_id, SUM(amount) as total_spent
        FROM orders
        WHERE status = 'Выполнен'
        GROUP BY customer_id
        HAVING SUM(amount) >= 5000
    ),
    multi_category_customers AS (
        SELECT DISTINCT o.customer_id
        FROM orders o
        JOIN order_details od ON o.order_id = od.order_id
        JOIN products p ON od.product_id = p.product_id
        WHERE o.status = 'Выполнен'
        GROUP BY o.customer_id
        HAVING COUNT(DISTINCT p.category_id) >= 3
    ),
    customer_analytics AS (
        SELECT 
            c.customer_name,
            c.city,
            hvc.total_spent,
            CASE WHEN mcc.customer_id IS NOT NULL THEN 'Да' ELSE 'Нет' END as multi_category_buyer,
            -- Последний заказ
            (SELECT MAX(order_date) 
             FROM orders 
             WHERE customer_id = c.customer_id 
               AND status = 'Выполнен') as last_order_date,
            -- Количество категорий
            (SELECT COUNT(DISTINCT p.category_id)
             FROM orders o
             JOIN order_details od ON o.order_id = od.order_id  
             JOIN products p ON od.product_id = p.product_id
             WHERE o.customer_id = c.customer_id 
               AND o.status = 'Выполнен') as categories_purchased
        FROM customers c
        JOIN high_value_customers hvc ON c.customer_id = hvc.customer_id
        LEFT JOIN multi_category_customers mcc ON c.customer_id = mcc.customer_id
        WHERE EXISTS (
            SELECT 1 FROM orders 
            WHERE customer_id = c.customer_id 
              AND order_date >= DATE('now', '-6 months')
              AND status = 'Выполнен'
        )
    )
    SELECT * FROM customer_analytics
    ORDER BY total_spent DESC;
    """
    
    complex_df = execute_sql_query(conn, complex_cte_query)
    
    print("\n🔍 Результаты продвинутых SQL техник:")
    print("="*50)
    print(f"1. Коррелированные подзапросы: {len(correlated_df)} записей")
    print(f"2. Рекурсивный CTE (временной ряд): {len(hierarchy_df)} недель")
    print(f"3. Сложный CTE с EXISTS: {len(complex_df)} VIP клиентов")
    
    return correlated_df, hierarchy_df, complex_df

def main():
    """Основная функция для запуска всех анализов"""
    print("🚀 Запуск интеграционного анализа SQL + Python")
    print("="*60)
    
    # Создание базы данных
    conn = create_database_from_csv()
    
    try:
        # 1. Анализ месячных продаж
        print("\n📈 1. Анализ месячных продаж...")
        monthly_df = monthly_sales_analysis(conn)
        print(f"   ✅ Обработано {len(monthly_df)} месяцев")
        
        # 2. RFM сегментация клиентов
        print("\n🎯 2. RFM сегментация клиентов...")
        rfm_df, segment_stats = customer_segmentation_analysis(conn)
        print(f"   ✅ Сегментировано {len(rfm_df)} клиентов")
        print(f"   📊 Найдено {rfm_df['rfm_segment'].nunique()} уникальных сегментов")
        
        # 3. Комплексный анализ товаров
        print("\n🛍️ 3. Анализ производительности товаров...")
        products_df, category_stats = complex_join_analysis(conn)
        print(f"   ✅ Проанализировано {len(products_df)} товаров")
        
        # 4. Демонстрация продвинутых техник
        print("\n🎓 4. Демонстрация продвинутых SQL техник...")
        corr_df, hier_df, complex_df = demonstrate_advanced_sql_techniques(conn)
        
        # Сохранение результатов
        monthly_df.to_csv('monthly_sales_results.csv', index=False, sep=';')
        rfm_df.to_csv('customer_rfm_segments.csv', index=False, sep=';')
        products_df.to_csv('product_performance_analysis.csv', index=False, sep=';')
        
        print(f"\n📁 Результаты сохранены в CSV файлы:")
        print(f"   • monthly_sales_results.csv")
        print(f"   • customer_rfm_segments.csv")  
        print(f"   • product_performance_analysis.csv")
        print(f"   • monthly_sales_analysis.png")
        print(f"   • customer_segmentation.png")
        
        print(f"\n🎉 Анализ успешно завершён!")
        print(f"📊 Обработано:")
        print(f"   • {len(monthly_df)} месяцев продаж")
        print(f"   • {len(rfm_df)} клиентов")
        print(f"   • {len(products_df)} товаров")
        print(f"   • Создано 2 аналитических дашборда")
        
    except Exception as e:
        print(f"❌ Ошибка при выполнении анализа: {e}")
    
    finally:
        conn.close()

if __name__ == "__main__":
    main()