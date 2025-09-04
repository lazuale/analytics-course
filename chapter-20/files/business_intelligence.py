import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime

# Настройка стиля для графиков
plt.style.use('default')
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10
sns.set_palette("husl")

class BusinessIntelligence:
    """Класс для создания бизнес-аналитических отчётов на основе SQL и Python"""
    
    def __init__(self, db_path='sales_data.db'):
        """Инициализация подключения к базе данных"""
        self.db_path = db_path
        print(f"🔗 Подключение к базе данных: {db_path}")
        
    def connect(self):
        """Создание подключения к базе данных"""
        return sqlite3.connect(self.db_path)
    
    def execute_query(self, query, description=""):
        """Выполнение SQL запроса с логированием"""
        conn = self.connect()
        try:
            if description:
                print(f"🔍 {description}")
            df = pd.read_sql_query(query, conn)
            print(f"   ✅ Получено {len(df)} записей")
            return df
        except Exception as e:
            print(f"   ❌ Ошибка: {e}")
            return pd.DataFrame()
        finally:
            conn.close()
    
    def executive_summary(self):
        """Создание исполнительской сводки"""
        print("\n📊 EXECUTIVE SUMMARY")
        print("="*50)
        
        # Основные KPI
        kpi_query = """
        WITH kpi_metrics AS (
            SELECT 
                -- Клиентские метрики
                COUNT(DISTINCT c.customer_id) as total_customers,
                COUNT(DISTINCT CASE WHEN o.order_id IS NOT NULL THEN c.customer_id END) as active_customers,
                
                -- Финансовые метрики
                COUNT(o.order_id) as total_orders,
                SUM(CASE WHEN o.status = 'Выполнен' THEN o.amount ELSE 0 END) as total_revenue,
                AVG(CASE WHEN o.status = 'Выполнен' THEN o.amount END) as avg_order_value,
                
                -- Операционные метрики
                COUNT(DISTINCT p.product_id) as total_products,
                COUNT(DISTINCT cat.category_id) as total_categories,
                COUNT(DISTINCT c.city) as cities_covered,
                
                -- Временные метрики
                MIN(o.order_date) as first_order_date,
                MAX(o.order_date) as last_order_date
            FROM customers c
            LEFT JOIN orders o ON c.customer_id = o.customer_id
            LEFT JOIN order_details od ON o.order_id = od.order_id
            LEFT JOIN products p ON od.product_id = p.product_id
            LEFT JOIN categories cat ON p.category_id = cat.category_id
        )
        SELECT 
            total_customers,
            active_customers,
            ROUND(active_customers * 100.0 / total_customers, 1) as activation_rate,
            total_orders,
            ROUND(total_revenue, 0) as total_revenue,
            ROUND(avg_order_value, 0) as avg_order_value,
            ROUND(total_revenue / active_customers, 0) as revenue_per_active_customer,
            total_products,
            total_categories,
            cities_covered,
            first_order_date,
            last_order_date,
            julianday(last_order_date) - julianday(first_order_date) + 1 as business_days
        FROM kpi_metrics;
        """
        
        kpi_df = self.execute_query(kpi_query, "Расчёт ключевых показателей")
        
        if not kpi_df.empty:
            kpi = kpi_df.iloc[0]
            print(f"👥 Всего клиентов: {kpi['total_customers']:,}")
            print(f"✅ Активных клиентов: {kpi['active_customers']:,} ({kpi['activation_rate']}%)")
            print(f"📦 Всего заказов: {kpi['total_orders']:,}")
            print(f"💰 Общая выручка: {kpi['total_revenue']:,.0f} руб.")
            print(f"💎 Средний чек: {kpi['avg_order_value']:,.0f} руб.")
            print(f"📈 Выручка на активного клиента: {kpi['revenue_per_active_customer']:,.0f} руб.")
            print(f"🛍️ Товаров в ассортименте: {kpi['total_products']:,}")
            print(f"📂 Категорий товаров: {kpi['total_categories']:,}")
            print(f"🌍 Городов охвата: {kpi['cities_covered']:,}")
            print(f"📅 Период работы: {kpi['business_days']:.0f} дней")
        
        return kpi_df
    
    def customer_segmentation_dashboard(self):
        """Создание дашборда сегментации клиентов"""
        print("\n🎯 CUSTOMER SEGMENTATION ANALYSIS")
        print("="*50)
        
        # RFM анализ с использованием CTE
        rfm_query = """
        WITH customer_rfm AS (
            SELECT 
                c.customer_id,
                c.customer_name,
                c.city,
                -- Recency: дни с последнего заказа
                COALESCE(
                    julianday('now') - julianday(MAX(CASE WHEN o.status = 'Выполнен' THEN o.order_date END)), 
                    999
                ) as recency_days,
                -- Frequency: количество выполненных заказов
                COUNT(CASE WHEN o.status = 'Выполнен' THEN o.order_id END) as frequency,
                -- Monetary: общая сумма выполненных заказов
                COALESCE(SUM(CASE WHEN o.status = 'Выполнен' THEN o.amount ELSE 0 END), 0) as monetary
            FROM customers c
            LEFT JOIN orders o ON c.customer_id = o.customer_id
            GROUP BY c.customer_id, c.customer_name, c.city
        ),
        rfm_quartiles AS (
            SELECT *,
                NTILE(4) OVER (ORDER BY recency_days DESC) as r_score,  -- Меньше дней = лучше, поэтому DESC
                NTILE(4) OVER (ORDER BY frequency ASC) as f_score,      -- Больше заказов = лучше
                NTILE(4) OVER (ORDER BY monetary ASC) as m_score       -- Больше денег = лучше
            FROM customer_rfm
            WHERE monetary > 0  -- Только клиенты с покупками
        ),
        rfm_segments AS (
            SELECT *,
                CASE 
                    WHEN r_score >= 3 AND f_score >= 3 AND m_score >= 3 THEN 'Champions'
                    WHEN r_score >= 3 AND m_score >= 3 THEN 'Loyal Customers'
                    WHEN r_score >= 3 AND f_score <= 2 THEN 'New Customers'
                    WHEN r_score <= 2 AND f_score >= 3 AND m_score >= 3 THEN 'At Risk'
                    WHEN r_score <= 2 AND f_score <= 2 THEN 'Lost'
                    ELSE 'Developing'
                END as rfm_segment
            FROM rfm_quartiles
        )
        SELECT 
            rfm_segment,
            COUNT(*) as customers_count,
            ROUND(AVG(monetary), 0) as avg_monetary,
            ROUND(AVG(frequency), 1) as avg_frequency,
            ROUND(AVG(recency_days), 0) as avg_recency_days,
            ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 1) as segment_share
        FROM rfm_segments
        GROUP BY rfm_segment
        ORDER BY avg_monetary DESC;
        """
        
        segments_df = self.execute_query(rfm_query, "RFM сегментация клиентов")
        
        if not segments_df.empty:
            # Создание визуализации сегментов
            fig, axes = plt.subplots(2, 2, figsize=(16, 12))
            fig.suptitle('🎯 Customer Segmentation Dashboard', fontsize=16, fontweight='bold')
            
            # График 1: Распределение клиентов по сегментам
            axes[0,0].bar(segments_df['rfm_segment'], segments_df['customers_count'], 
                         color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FECA57', '#FF9F43'])
            axes[0,0].set_title('👥 Количество клиентов по сегментам')
            axes[0,0].set_xlabel('RFM Сегмент')
            axes[0,0].set_ylabel('Количество клиентов')
            axes[0,0].tick_params(axis='x', rotation=45)
            
            # График 2: Средняя монетарная ценность
            axes[0,1].bar(segments_df['rfm_segment'], segments_df['avg_monetary'],
                         color=['#A8E6CF', '#FF8B94', '#FFD93D', '#6BCF7F', '#4D96FF', '#9B59B6'])
            axes[0,1].set_title('💰 Средняя ценность клиента')
            axes[0,1].set_xlabel('RFM Сегмент')
            axes[0,1].set_ylabel('Средние траты (руб.)')
            axes[0,1].tick_params(axis='x', rotation=45)
            
            # График 3: Доли сегментов (pie chart)
            axes[1,0].pie(segments_df['customers_count'], labels=segments_df['rfm_segment'], 
                         autopct='%1.1f%%', startangle=90)
            axes[1,0].set_title('🥧 Процентное распределение сегментов')
            
            # График 4: Frequency vs Recency
            axes[1,1].scatter(segments_df['avg_recency_days'], segments_df['avg_frequency'], 
                            s=segments_df['customers_count']*20, alpha=0.7, 
                            c=segments_df['avg_monetary'], cmap='viridis')
            axes[1,1].set_title('📊 Frequency vs Recency (размер = количество)')
            axes[1,1].set_xlabel('Средние дни с последнего заказа')
            axes[1,1].set_ylabel('Средняя частота заказов')
            
            # Добавление цветовой шкалы
            cbar = plt.colorbar(axes[1,1].collections[0], ax=axes[1,1])
            cbar.set_label('Средняя монетарная ценность')
            
            plt.tight_layout()
            plt.savefig('customer_segmentation_dashboard.png', dpi=300, bbox_inches='tight')
            plt.show()
            
            print("📈 Распределение по сегментам:")
            for _, row in segments_df.iterrows():
                print(f"   • {row['rfm_segment']}: {row['customers_count']} клиентов "
                      f"({row['segment_share']}%), средние траты: {row['avg_monetary']:,.0f} руб.")
        
        return segments_df
    
    def geographic_performance_analysis(self):
        """Анализ производительности по географии"""
        print("\n🌍 GEOGRAPHIC PERFORMANCE ANALYSIS")
        print("="*50)
        
        geo_query = """
        WITH city_metrics AS (
            SELECT 
                c.city,
                COUNT(DISTINCT c.customer_id) as total_customers,
                COUNT(DISTINCT CASE WHEN o.order_id IS NOT NULL THEN c.customer_id END) as active_customers,
                COUNT(o.order_id) as total_orders,
                SUM(CASE WHEN o.status = 'Выполнен' THEN o.amount ELSE 0 END) as total_revenue,
                AVG(CASE WHEN o.status = 'Выполнен' THEN o.amount END) as avg_order_value,
                MAX(o.order_date) as last_order_date
            FROM customers c
            LEFT JOIN orders o ON c.customer_id = o.customer_id
            GROUP BY c.city
        ),
        city_rankings AS (
            SELECT 
                *,
                ROUND(active_customers * 100.0 / total_customers, 1) as activation_rate,
                ROUND(total_revenue / NULLIF(active_customers, 0), 0) as revenue_per_active_customer,
                RANK() OVER (ORDER BY total_revenue DESC) as revenue_rank,
                RANK() OVER (ORDER BY activation_rate DESC) as activation_rank
            FROM city_metrics
        )
        SELECT 
            city,
            total_customers,
            active_customers,
            activation_rate,
            total_orders,
            ROUND(total_revenue, 0) as total_revenue,
            ROUND(avg_order_value, 0) as avg_order_value,
            revenue_per_active_customer,
            revenue_rank,
            activation_rank,
            last_order_date,
            -- Классификация городов
            CASE 
                WHEN total_revenue >= 200000 AND activation_rate >= 60 THEN 'Звездные города'
                WHEN total_revenue >= 100000 THEN 'Прибыльные города'
                WHEN activation_rate >= 70 THEN 'Активные города'
                WHEN total_customers >= 5 THEN 'Развивающиеся города'
                ELSE 'Новые города'
            END as city_category
        FROM city_rankings
        ORDER BY total_revenue DESC;
        """
        
        geo_df = self.execute_query(geo_query, "Анализ производительности по городам")
        
        if not geo_df.empty:
            # Создание географического дашборда
            fig, axes = plt.subplots(2, 2, figsize=(16, 12))
            fig.suptitle('🌍 Geographic Performance Dashboard', fontsize=16, fontweight='bold')
            
            # График 1: Выручка по городам
            top_cities = geo_df.head(8)  # Топ-8 городов
            axes[0,0].barh(top_cities['city'], top_cities['total_revenue'], color='skyblue')
            axes[0,0].set_title('💰 Выручка по городам (топ-8)')
            axes[0,0].set_xlabel('Общая выручка (руб.)')
            
            # График 2: Активация клиентов
            axes[0,1].bar(top_cities['city'], top_cities['activation_rate'], color='lightgreen')
            axes[0,1].set_title('📈 Процент активации клиентов')
            axes[0,1].set_ylabel('Процент активации (%)')
            axes[0,1].tick_params(axis='x', rotation=45)
            
            # График 3: Scatter plot - клиенты vs выручка
            scatter = axes[1,0].scatter(geo_df['total_customers'], geo_df['total_revenue'], 
                                      s=geo_df['activation_rate']*5, alpha=0.7, c=geo_df['avg_order_value'], 
                                      cmap='plasma')
            axes[1,0].set_title('🎯 Клиенты vs Выручка (размер = активация)')
            axes[1,0].set_xlabel('Всего клиентов')
            axes[1,0].set_ylabel('Общая выручка')
            
            # Добавление подписей городов
            for i, row in geo_df.iterrows():
                if row['total_revenue'] > geo_df['total_revenue'].quantile(0.7):  # Только крупные города
                    axes[1,0].annotate(row['city'], (row['total_customers'], row['total_revenue']), 
                                     xytext=(5, 5), textcoords='offset points', fontsize=8)
            
            plt.colorbar(scatter, ax=axes[1,0], label='Средний чек')
            
            # График 4: Категории городов
            city_categories = geo_df.groupby('city_category').size()
            axes[1,1].pie(city_categories.values, labels=city_categories.index, autopct='%1.1f%%')
            axes[1,1].set_title('🏙️ Категории городов')
            
            plt.tight_layout()
            plt.savefig('geographic_performance_dashboard.png', dpi=300, bbox_inches='tight')
            plt.show()
            
            print("🏆 Топ-5 городов по выручке:")
            for i, row in geo_df.head(5).iterrows():
                print(f"   {row['revenue_rank']}. {row['city']}: {row['total_revenue']:,.0f} руб. "
                      f"({row['active_customers']} активных клиентов)")
        
        return geo_df
    
    def product_performance_analysis(self):
        """Анализ производительности товаров"""
        print("\n🛍️ PRODUCT PERFORMANCE ANALYSIS")
        print("="*50)
        
        product_query = """
        WITH product_sales AS (
            SELECT 
                p.product_id,
                p.product_name,
                cat.category_name,
                p.price as catalog_price,
                COUNT(DISTINCT od.order_id) as times_ordered,
                SUM(od.quantity) as total_quantity_sold,
                SUM(od.quantity * od.unit_price * (1 - od.discount/100)) as total_revenue,
                AVG(od.unit_price) as avg_selling_price,
                MIN(o.order_date) as first_sale_date,
                MAX(o.order_date) as last_sale_date
            FROM products p
            LEFT JOIN order_details od ON p.product_id = od.product_id
            LEFT JOIN orders o ON od.order_id = o.order_id AND o.status = 'Выполнен'
            LEFT JOIN categories cat ON p.category_id = cat.category_id
            GROUP BY p.product_id, p.product_name, cat.category_name, p.price
        ),
        product_rankings AS (
            SELECT *,
                COALESCE(total_revenue, 0) as revenue,
                COALESCE(total_quantity_sold, 0) as quantity,
                RANK() OVER (ORDER BY COALESCE(total_revenue, 0) DESC) as revenue_rank,
                RANK() OVER (PARTITION BY category_name ORDER BY COALESCE(total_revenue, 0) DESC) as category_rank,
                CASE 
                    WHEN total_revenue IS NULL THEN 'Не продавался'
                    WHEN total_revenue >= (SELECT AVG(COALESCE(total_revenue, 0)) * 2 FROM product_sales WHERE total_revenue > 0) THEN 'Хит продаж'
                    WHEN total_revenue >= (SELECT AVG(COALESCE(total_revenue, 0)) FROM product_sales WHERE total_revenue > 0) THEN 'Популярный'
                    ELSE 'Обычный'
                END as performance_category,
                julianday('now') - julianday(last_sale_date) as days_since_last_sale
            FROM product_sales
        )
        SELECT 
            product_name,
            category_name,
            ROUND(catalog_price, 0) as catalog_price,
            COALESCE(times_ordered, 0) as times_ordered,
            COALESCE(total_quantity_sold, 0) as quantity_sold,
            ROUND(COALESCE(total_revenue, 0), 0) as total_revenue,
            ROUND(COALESCE(avg_selling_price, catalog_price), 0) as avg_selling_price,
            revenue_rank,
            category_rank,
            performance_category,
            COALESCE(ROUND(days_since_last_sale, 0), 999) as days_since_last_sale
        FROM product_rankings
        ORDER BY total_revenue DESC;
        """
        
        products_df = self.execute_query(product_query, "Анализ производительности товаров")
        
        if not products_df.empty:
            # Анализ по категориям
            category_analysis = products_df.groupby('category_name').agg({
                'product_name': 'count',
                'total_revenue': 'sum',
                'quantity_sold': 'sum',
                'times_ordered': 'sum'
            }).round(0)
            category_analysis.columns = ['products_count', 'category_revenue', 'category_quantity', 'category_orders']
            category_analysis = category_analysis.sort_values('category_revenue', ascending=False)
            
            print("📊 Производительность по категориям:")
            for category, row in category_analysis.iterrows():
                print(f"   • {category}: {row['category_revenue']:,.0f} руб. "
                      f"({row['products_count']} товаров, {row['category_quantity']} шт.)")
            
            print(f"\n🏆 Топ-10 товаров по выручке:")
            top_products = products_df[products_df['total_revenue'] > 0].head(10)
            for i, row in top_products.iterrows():
                print(f"   {row['revenue_rank']}. {row['product_name']} ({row['category_name']}): "
                      f"{row['total_revenue']:,.0f} руб.")
            
            # Анализ неактивных товаров
            inactive_products = len(products_df[products_df['total_revenue'] == 0])
            print(f"\n⚠️ Товаров без продаж: {inactive_products} из {len(products_df)} "
                  f"({inactive_products/len(products_df)*100:.1f}%)")
        
        return products_df, category_analysis
    
    def trend_analysis(self):
        """Анализ трендов продаж"""
        print("\n📈 TREND ANALYSIS")
        print("="*50)
        
        trend_query = """
        WITH monthly_trends AS (
            SELECT 
                strftime('%Y-%m', order_date) as month,
                COUNT(*) as orders_count,
                SUM(amount) as monthly_revenue,
                COUNT(DISTINCT customer_id) as active_customers,
                AVG(amount) as avg_order_value
            FROM orders
            WHERE status = 'Выполнен' 
              AND order_date >= DATE('now', '-12 months')
            GROUP BY strftime('%Y-%m', order_date)
        ),
        trend_calculations AS (
            SELECT *,
                LAG(monthly_revenue) OVER (ORDER BY month) as prev_month_revenue,
                LAG(orders_count) OVER (ORDER BY month) as prev_month_orders,
                SUM(monthly_revenue) OVER (ORDER BY month) as cumulative_revenue,
                AVG(monthly_revenue) OVER (
                    ORDER BY month 
                    ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
                ) as ma_3_months
            FROM monthly_trends
        )
        SELECT 
            month,
            orders_count,
            ROUND(monthly_revenue, 0) as monthly_revenue,
            active_customers,
            ROUND(avg_order_value, 0) as avg_order_value,
            ROUND(cumulative_revenue, 0) as cumulative_revenue,
            ROUND(ma_3_months, 0) as ma_3_months,
            CASE 
                WHEN prev_month_revenue IS NOT NULL 
                THEN ROUND((monthly_revenue - prev_month_revenue) * 100.0 / prev_month_revenue, 1)
                ELSE NULL
            END as revenue_growth_pct,
            CASE 
                WHEN prev_month_orders IS NOT NULL 
                THEN ROUND((orders_count - prev_month_orders) * 100.0 / prev_month_orders, 1)
                ELSE NULL
            END as orders_growth_pct
        FROM trend_calculations
        ORDER BY month;
        """
        
        trends_df = self.execute_query(trend_query, "Анализ месячных трендов")
        
        if not trends_df.empty:
            # Создание графика трендов
            fig, axes = plt.subplots(2, 2, figsize=(16, 12))
            fig.suptitle('📈 Sales Trend Analysis', fontsize=16, fontweight='bold')
            
            # График 1: Выручка и скользящее среднее
            axes[0,0].plot(trends_df['month'], trends_df['monthly_revenue'], 
                          marker='o', linewidth=2, label='Месячная выручка')
            axes[0,0].plot(trends_df['month'], trends_df['ma_3_months'], 
                          linestyle='--', linewidth=2, label='Скользящее среднее (3 месяца)')
            axes[0,0].set_title('💰 Динамика выручки')
            axes[0,0].set_ylabel('Выручка (руб.)')
            axes[0,0].legend()
            axes[0,0].tick_params(axis='x', rotation=45)
            axes[0,0].grid(True, alpha=0.3)
            
            # График 2: Количество заказов
            axes[0,1].plot(trends_df['month'], trends_df['orders_count'], 
                          marker='s', color='green', linewidth=2)
            axes[0,1].set_title('📦 Количество заказов')
            axes[0,1].set_ylabel('Количество заказов')
            axes[0,1].tick_params(axis='x', rotation=45)
            axes[0,1].grid(True, alpha=0.3)
            
            # График 3: Рост выручки
            growth_data = trends_df.dropna(subset=['revenue_growth_pct'])
            colors = ['green' if x >= 0 else 'red' for x in growth_data['revenue_growth_pct']]
            axes[1,0].bar(growth_data['month'], growth_data['revenue_growth_pct'], 
                         color=colors, alpha=0.7)
            axes[1,0].set_title('📊 Рост выручки месяц к месяцу (%)')
            axes[1,0].set_ylabel('Рост (%)')
            axes[1,0].tick_params(axis='x', rotation=45)
            axes[1,0].axhline(y=0, color='black', linestyle='-', alpha=0.5)
            
            # График 4: Активные клиенты vs Средний чек
            axes[1,1].scatter(trends_df['active_customers'], trends_df['avg_order_value'], 
                            s=trends_df['orders_count']*2, alpha=0.7, c=range(len(trends_df)), 
                            cmap='viridis')
            axes[1,1].set_title('🎯 Активные клиенты vs Средний чек')
            axes[1,1].set_xlabel('Активные клиенты')
            axes[1,1].set_ylabel('Средний чек')
            
            # Добавление подписей месяцев
            for i, row in trends_df.iterrows():
                axes[1,1].annotate(row['month'], 
                                 (row['active_customers'], row['avg_order_value']), 
                                 xytext=(3, 3), textcoords='offset points', fontsize=8)
            
            plt.tight_layout()
            plt.savefig('trend_analysis_dashboard.png', dpi=300, bbox_inches='tight')
            plt.show()
            
            # Анализ последних трендов
            latest_months = trends_df.tail(3)
            print("📊 Последние 3 месяца:")
            for _, row in latest_months.iterrows():
                growth_str = f" ({row['revenue_growth_pct']:+.1f}%)" if pd.notna(row['revenue_growth_pct']) else ""
                print(f"   • {row['month']}: {row['monthly_revenue']:,.0f} руб.{growth_str}, "
                      f"{row['orders_count']} заказов, {row['active_customers']} клиентов")
        
        return trends_df
    
    def generate_comprehensive_report(self):
        """Создание комплексного бизнес-отчёта"""
        print("\n🚀 GENERATING COMPREHENSIVE BUSINESS INTELLIGENCE REPORT")
        print("="*70)
        
        # Выполнение всех анализов
        kpi_df = self.executive_summary()
        segments_df = self.customer_segmentation_dashboard()
        geo_df = self.geographic_performance_analysis()
        products_df, categories_df = self.product_performance_analysis()
        trends_df = self.trend_analysis()
        
        # Сохранение всех результатов
        reports = {
            'executive_kpi': kpi_df,
            'customer_segments': segments_df,
            'geographic_performance': geo_df,
            'product_performance': products_df,
            'category_performance': categories_df,
            'trend_analysis': trends_df
        }
        
        print(f"\n💾 Сохранение отчётов в CSV...")
        for name, df in reports.items():
            if not df.empty:
                filename = f"bi_report_{name}.csv"
                df.to_csv(filename, index=False, sep=';')
                print(f"   ✅ {filename}")
        
        # Создание итоговой сводки
        print(f"\n📋 ИТОГОВАЯ СВОДКА АНАЛИЗА")
        print("="*40)
        
        if not kpi_df.empty:
            kpi = kpi_df.iloc[0]
            print(f"📊 Ключевые показатели:")
            print(f"   • Активация клиентов: {kpi['activation_rate']}%")
            print(f"   • Общая выручка: {kpi['total_revenue']:,.0f} руб.")
            print(f"   • Средний чек: {kpi['avg_order_value']:,.0f} руб.")
        
        if not segments_df.empty:
            top_segment = segments_df.iloc[0]
            print(f"🎯 Лучший сегмент клиентов: {top_segment['rfm_segment']}")
            print(f"   • Средние траты: {top_segment['avg_monetary']:,.0f} руб.")
            print(f"   • Доля клиентов: {top_segment['segment_share']}%")
        
        if not geo_df.empty:
            top_city = geo_df.iloc[0]
            print(f"🌍 Лучший город: {top_city['city']}")
            print(f"   • Выручка: {top_city['total_revenue']:,.0f} руб.")
            print(f"   • Активация: {top_city['activation_rate']}%")
        
        if not products_df.empty:
            bestseller = products_df[products_df['total_revenue'] > 0].iloc[0]
            print(f"🏆 Топ товар: {bestseller['product_name']}")
            print(f"   • Выручка: {bestseller['total_revenue']:,.0f} руб.")
            print(f"   • Категория: {bestseller['category_name']}")
        
        print(f"\n🎉 Комплексный бизнес-анализ завершён!")
        print(f"📁 Создано файлов отчётов: {len([df for df in reports.values() if not df.empty])}")
        print(f"📊 Создано дашбордов: 4")
        
        return reports

def main():
    """Основная функция для запуска бизнес-аналитики"""
    print("🎯 BUSINESS INTELLIGENCE SYSTEM")
    print("Система бизнес-аналитики на основе SQL и Python")
    print("="*70)
    
    # Создание экземпляра BI системы
    bi = BusinessIntelligence('sales_data.db')
    
    try:
        # Запуск комплексного анализа
        reports = bi.generate_comprehensive_report()
        
        print(f"\n✨ Все анализы успешно выполнены!")
        print(f"📈 Создано {len(reports)} типов отчётов")
        print(f"🖼️ Сохранено 4 аналитических дашборда:")
        print(f"   • customer_segmentation_dashboard.png")
        print(f"   • geographic_performance_dashboard.png")
        print(f"   • trend_analysis_dashboard.png")
        
    except Exception as e:
        print(f"❌ Ошибка выполнения анализа: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()