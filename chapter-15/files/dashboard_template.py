"""
🎛️ Шаблон для создания профессиональных дашбордов - ваша студия аналитики!

Этот скрипт демонстрирует создание:
- Многопанельных дашбордов
- Автоматических KPI расчетов
- Корпоративного стиля
- Интерактивных элементов
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.patches as patches

print("🎛️ Создаем профессиональные дашборды!")
print("=" * 50)

def setup_corporate_style():
    """Настройка корпоративного стиля"""
    # Корпоративные цвета
    corporate_colors = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#592E83']
    
    # Настройки matplotlib
    plt.rcParams.update({
        'font.size': 10,
        'font.family': 'DejaVu Sans',
        'axes.titlesize': 12,
        'axes.labelsize': 10,
        'xtick.labelsize': 9,
        'ytick.labelsize': 9,
        'legend.fontsize': 9,
        'figure.titlesize': 16,
        'axes.grid': True,
        'grid.alpha': 0.3,
        'axes.axisbelow': True
    })
    
    # Устанавливаем палитру
    sns.set_palette(corporate_colors)
    sns.set_style("whitegrid")
    
    return corporate_colors

def load_sample_data():
    """Загрузка или генерация примера данных для дашборда"""
    try:
        # Пытаемся загрузить созданные файлы
        sales_df = pd.read_csv('sales_trends.csv')
        customers_df = pd.read_csv('customer_analytics.csv')
        print("✅ Данные загружены из файлов")
        return sales_df, customers_df
    except FileNotFoundError:
        print("📁 Файлы не найдены, генерируем пример данных...")
        return generate_dashboard_data()

def generate_dashboard_data():
    """Генерация примера данных для дашборда"""
    np.random.seed(42)
    
    # Данные продаж за последние 12 месяцев
    months = pd.date_range('2024-01-01', '2024-12-01', freq='MS')
    sales_data = []
    
    for month in months:
        base_sales = 1000000 + np.random.normal(0, 200000)
        # Добавляем сезонность
        if month.month in [11, 12]:  # Высокий сезон
            base_sales *= 1.3
        elif month.month in [6, 7, 8]:  # Средний сезон
            base_sales *= 1.1
        
        sales_data.append({
            'месяц': month.strftime('%Y-%m'),
            'дата': month,
            'выручка': max(base_sales, 500000),
            'количество_заказов': int(base_sales / np.random.normal(2000, 300)),
            'канал': np.random.choice(['Онлайн', 'Офлайн', 'Мобайл'])
        })
    
    sales_df = pd.DataFrame(sales_data)
    
    # Генерируем данные клиентов
    customers_data = []
    segments = ['VIP', 'Обычный', 'Новый']
    cities = ['Москва', 'СПб', 'Екатеринбург', 'Новосибирск']
    
    for i in range(200):
        segment = np.random.choice(segments, p=[0.1, 0.6, 0.3])
        city = np.random.choice(cities)
        
        customers_data.append({
            'сегмент': segment,
            'город': city,
            'доход': np.random.normal(80000 if segment == 'VIP' else 45000, 15000),
            'удовлетворенность': np.random.normal(8 if segment == 'VIP' else 7, 1)
        })
    
    customers_df = pd.DataFrame(customers_data)
    
    return sales_df, customers_df

def calculate_kpis(sales_df, customers_df):
    """Расчет ключевых показателей эффективности"""
    kpis = {}
    
    # Основные KPI продаж
    kpis['total_revenue'] = sales_df['выручка'].sum()
    kpis['avg_monthly_revenue'] = sales_df['выручка'].mean()
    kpis['total_orders'] = sales_df['количество_заказов'].sum()
    kpis['avg_order_value'] = kpis['total_revenue'] / kpis['total_orders']
    
    # Рост к предыдущему периоду (последние 6 vs предыдущие 6 месяцев)
    if len(sales_df) >= 12:
        recent_6 = sales_df.tail(6)['выручка'].sum()
        previous_6 = sales_df.iloc[-12:-6]['выручка'].sum()
        kpis['revenue_growth'] = ((recent_6 / previous_6) - 1) * 100
    else:
        kpis['revenue_growth'] = 0
    
    # KPI клиентов
    if not customers_df.empty:
        kpis['total_customers'] = len(customers_df)
        kpis['avg_satisfaction'] = customers_df['удовлетворенность'].mean()
        kpis['vip_customers'] = len(customers_df[customers_df['сегмент'] == 'VIP'])
        kpis['vip_percentage'] = (kpis['vip_customers'] / kpis['total_customers']) * 100
    
    return kpis

def create_sales_dashboard(sales_df, customers_df=None):
    """Создание комплексного дашборда продаж"""
    
    # Настройка корпоративного стиля
    colors = setup_corporate_style()
    
    # Расчет KPI
    kpis = calculate_kpis(sales_df, customers_df if customers_df is not None else pd.DataFrame())
    
    # Создание фигуры с настраиваемой сеткой
    fig = plt.figure(figsize=(20, 14))
    fig.suptitle('📊 Дашборд продаж компании', fontsize=20, y=0.96, fontweight='bold')
    
    # 1. Динамика продаж (главный график)
    ax1 = plt.subplot2grid((4, 6), (0, 0), colspan=4, rowspan=2)
    
    # Подготавливаем данные для временного ряда
    if 'дата' not in sales_df.columns:
        sales_df['дата'] = pd.to_datetime(sales_df['месяц'])
    
    monthly_sales = sales_df.groupby('месяц')['выручка'].sum().reset_index()
    monthly_sales['дата'] = pd.to_datetime(monthly_sales['месяц'])
    
    # Строим основной график динамики
    ax1.plot(monthly_sales['дата'], monthly_sales['выручка'], 
             marker='o', linewidth=3, markersize=8, color=colors[0])
    ax1.fill_between(monthly_sales['дата'], monthly_sales['выручка'], 
                     alpha=0.3, color=colors[0])
    
    ax1.set_title('📈 Динамика выручки по месяцам', fontsize=14, pad=20)
    ax1.set_ylabel('Выручка, млн руб.')
    ax1.tick_params(axis='x', rotation=45)
    
    # Добавляем аннотации для максимумов
    max_revenue = monthly_sales['выручка'].max()
    max_month = monthly_sales[monthly_sales['выручка'] == max_revenue]['дата'].iloc[0]
    ax1.annotate(f'Пик: {max_revenue/1e6:.1f}М руб', 
                xy=(max_month, max_revenue),
                xytext=(10, 20), textcoords='offset points',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7),
                arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))
    
    # 2. KPI блок
    ax2 = plt.subplot2grid((4, 6), (0, 4), colspan=2, rowspan=2)
    ax2.axis('off')
    
    # Создаем красивые KPI карточки
    kpi_text = f"""
    💰 КЛЮЧЕВЫЕ ПОКАЗАТЕЛИ
    
    📊 Общая выручка:
        {kpis['total_revenue']/1e6:.1f} млн руб.
    
    📈 Рост выручки:
        {kpis['revenue_growth']:+.1f}%
    
    🛒 Средний чек:
        {kpis['avg_order_value']:,.0f} руб.
    
    📦 Всего заказов:
        {kpis['total_orders']:,}
    
    🎯 Среднемесячная выручка:
        {kpis['avg_monthly_revenue']/1e6:.1f} млн руб.
    """
    
    # Определяем цвет для роста
    growth_color = 'green' if kpis['revenue_growth'] > 0 else 'red'
    
    ax2.text(0.05, 0.95, kpi_text, transform=ax2.transAxes, 
             fontsize=11, verticalalignment='top', fontweight='normal',
             bbox=dict(boxstyle="round,pad=1", facecolor='lightblue', alpha=0.8))
    
    # 3. Топ каналов продаж
    ax3 = plt.subplot2grid((4, 6), (2, 0), colspan=2)
    
    if 'канал' in sales_df.columns:
        channel_sales = sales_df.groupby('канал')['выручка'].sum().sort_values(ascending=True)
        bars = ax3.barh(range(len(channel_sales)), channel_sales.values, 
                        color=colors[:len(channel_sales)])
        
        # Добавляем значения на столбцы
        for i, (channel, value) in enumerate(channel_sales.items()):
            ax3.text(value + max(channel_sales) * 0.01, i, f'{value/1e6:.1f}М',
                     va='center', fontweight='bold')
        
        ax3.set_yticks(range(len(channel_sales)))
        ax3.set_yticklabels(channel_sales.index)
        ax3.set_title('🛒 Продажи по каналам')
        ax3.set_xlabel('Выручка, млн руб.')
    
    # 4. Региональные продажи (если есть данные о клиентах)
    ax4 = plt.subplot2grid((4, 6), (2, 2), colspan=2)
    
    if customers_df is not None and not customers_df.empty and 'город' in customers_df.columns:
        city_distribution = customers_df['город'].value_counts()
        
        # Создаем круговую диаграмму
        wedges, texts, autotexts = ax4.pie(city_distribution.values, 
                                           labels=city_distribution.index,
                                           autopct='%1.1f%%',
                                           colors=colors[:len(city_distribution)])
        
        ax4.set_title('🏙️ География клиентов')
        
        # Улучшаем читаемость процентов
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
    else:
        # Заглушка, если нет данных
        ax4.text(0.5, 0.5, '📍 География\nданных нет', 
                 ha='center', va='center', transform=ax4.transAxes,
                 bbox=dict(boxstyle="round,pad=0.3", facecolor='lightgray', alpha=0.7))
        ax4.set_xlim(0, 1)
        ax4.set_ylim(0, 1)
        ax4.axis('off')
    
    # 5. Сегментация клиентов
    ax5 = plt.subplot2grid((4, 6), (2, 4), colspan=2)
    
    if customers_df is not None and not customers_df.empty and 'сегмент' in customers_df.columns:
        segment_counts = customers_df['сегмент'].value_counts()
        colors_segments = [colors[0], colors[1], colors[2]]
        
        bars = ax5.bar(segment_counts.index, segment_counts.values, 
                       color=colors_segments[:len(segment_counts)])
        
        # Добавляем значения на столбцы
        for bar, value in zip(bars, segment_counts.values):
            height = bar.get_height()
            ax5.text(bar.get_x() + bar.get_width()/2., height + max(segment_counts) * 0.01,
                     f'{value}', ha='center', va='bottom', fontweight='bold')
        
        ax5.set_title('👥 Сегментация клиентов')
        ax5.set_ylabel('Количество клиентов')
    else:
        ax5.text(0.5, 0.5, '👥 Сегментация\nданных нет', 
                 ha='center', va='center', transform=ax5.transAxes,
                 bbox=dict(boxstyle="round,pad=0.3", facecolor='lightgray', alpha=0.7))
        ax5.set_xlim(0, 1)
        ax5.set_ylim(0, 1)
        ax5.axis('off')
    
    # 6. Анализ удовлетворенности (если есть данные)
    ax6 = plt.subplot2grid((4, 6), (3, 0), colspan=3)
    
    if customers_df is not None and not customers_df.empty and 'удовлетворенность' in customers_df.columns:
        # Гистограмма удовлетворенности
        ax6.hist(customers_df['удовлетворенность'], bins=10, 
                 color=colors[1], alpha=0.7, edgecolor='black')
        ax6.axvline(customers_df['удовлетворенность'].mean(), 
                    color='red', linestyle='--', linewidth=2,
                    label=f'Среднее: {customers_df["удовлетворенность"].mean():.1f}')
        ax6.set_title('📊 Распределение удовлетворенности клиентов')
        ax6.set_xlabel('Удовлетворенность (1-10)')
        ax6.set_ylabel('Количество клиентов')
        ax6.legend()
    else:
        ax6.text(0.5, 0.5, '😊 Удовлетворенность\nданных нет', 
                 ha='center', va='center', transform=ax6.transAxes,
                 bbox=dict(boxstyle="round,pad=0.3", facecolor='lightgray', alpha=0.7))
        ax6.set_xlim(0, 1)
        ax6.set_ylim(0, 1)
        ax6.axis('off')
    
    # 7. Инсайты и рекомендации
    ax7 = plt.subplot2grid((4, 6), (3, 3), colspan=3)
    ax7.axis('off')
    
    # Автоматические инсайты на основе данных
    insights = generate_insights(sales_df, customers_df, kpis)
    
    insights_text = "💡 АВТОМАТИЧЕСКИЕ ИНСАЙТЫ:\n\n" + "\n".join([f"• {insight}" for insight in insights])
    
    ax7.text(0.05, 0.95, insights_text, transform=ax7.transAxes, 
             fontsize=10, verticalalignment='top',
             bbox=dict(boxstyle="round,pad=1", facecolor='lightyellow', alpha=0.8))
    
    # Добавляем дату создания отчета
    fig.text(0.99, 0.01, f'Создано: {datetime.now().strftime("%Y-%m-%d %H:%M")}', 
             ha='right', va='bottom', fontsize=8, alpha=0.7)
    
    plt.tight_layout()
    plt.subplots_adjust(top=0.93, bottom=0.05)
    
    return fig

def generate_insights(sales_df, customers_df, kpis):
    """Генерация автоматических инсайтов на основе данных"""
    insights = []
    
    # Анализ тренда продаж
    if kpis['revenue_growth'] > 10:
        insights.append("Отличный рост выручки! Масштабируйте успешные каналы")
    elif kpis['revenue_growth'] > 0:
        insights.append("Положительный рост, но есть потенциал для ускорения")
    else:
        insights.append("Снижение выручки требует немедленного внимания")
    
    # Анализ среднего чека
    if kpis['avg_order_value'] > 3000:
        insights.append("Высокий средний чек - фокус на удержании клиентов")
    elif kpis['avg_order_value'] < 1500:
        insights.append("Низкий средний чек - рассмотрите upsell стратегии")
    
    # Анализ сезонности
    if 'месяц' in sales_df.columns:
        monthly_revenue = sales_df.groupby('месяц')['выручка'].sum()
        if len(monthly_revenue) >= 3:
            max_month = monthly_revenue.idxmax()
            insights.append(f"Пиковый месяц: {max_month} - подготовьтесь к сезону")
    
    # Анализ клиентской базы
    if customers_df is not None and not customers_df.empty:
        if 'vip_percentage' in kpis and kpis['vip_percentage'] < 15:
            insights.append("Мало VIP клиентов - развивайте программу лояльности")
        
        if 'avg_satisfaction' in kpis:
            if kpis['avg_satisfaction'] > 8:
                insights.append("Высокая удовлетворенность - используйте для реферралов")
            elif kpis['avg_satisfaction'] < 6:
                insights.append("Низкая удовлетворенность - срочно улучшайте сервис")
    
    # Если инсайтов мало, добавляем общие рекомендации
    if len(insights) < 3:
        insights.extend([
            "Регулярно отслеживайте ключевые метрики",
            "Проводите A/B тесты для оптимизации",
            "Анализируйте поведение лучших клиентов"
        ])
    
    return insights[:5]  # Максимум 5 инсайтов

def save_dashboard(fig, filename='dashboard'):
    """Сохранение дашборда в различных форматах"""
    formats = ['png', 'pdf', 'svg']
    
    for fmt in formats:
        full_filename = f'{filename}.{fmt}'
        fig.savefig(full_filename, dpi=300, bbox_inches='tight', 
                   facecolor='white', edgecolor='none')
        print(f"✅ Дашборд сохранен: {full_filename}")

# Функция для создания интерактивного дашборда с фильтрами
def create_interactive_dashboard():
    """Создание дашборда с возможностью фильтрации"""
    print("\n🎛️ Создание интерактивного дашборда...")
    
    # Загружаем данные
    sales_df, customers_df = load_sample_data()
    
    # Создаем основной дашборд
    fig = create_sales_dashboard(sales_df, customers_df)
    
    # Показываем дашборд
    plt.show()
    
    # Сохраняем в различных форматах
    save_dashboard(fig, 'professional_dashboard')
    
    return fig

# Пример использования различных стилей дашбордов
def create_dashboard_variants():
    """Создание дашбордов в различных стилях"""
    print("\n🎨 Создание вариантов дашбордов...")
    
    sales_df, customers_df = load_sample_data()
    
    styles = [
        ('corporate', ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D']),
        ('modern', ['#FF6B35', '#004E89', '#1A936F', '#88D498']),
        ('classic', ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'])
    ]
    
    for style_name, colors in styles:
        plt.style.use('default')
        sns.set_palette(colors)
        
        fig = create_sales_dashboard(sales_df, customers_df)
        save_dashboard(fig, f'dashboard_{style_name}')
        plt.close(fig)
        
        print(f"✅ Создан дашборд в стиле: {style_name}")

# Главная функция для демонстрации
def main():
    """Основная функция демонстрации дашбордов"""
    print("🚀 Запуск создания профессиональных дашбордов!")
    
    # Создаем основной интерактивный дашборд
    dashboard = create_interactive_dashboard()
    
    print("\n🎉 Дашборд создан успешно!")
    print("💡 Попробуйте:")
    print("  • Изменить данные в CSV файлах")
    print("  • Настроить корпоративные цвета")
    print("  • Добавить новые KPI метрики")

if __name__ == "__main__":
    main()