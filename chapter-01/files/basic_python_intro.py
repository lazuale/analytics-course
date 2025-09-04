"""
Этот скрипт демонстрирует основные возможности анализа данных в Python.
Мы работаем с данными интернет-магазина и показываем базовые аналитические операции.

Требования: pandas, numpy
Установка: pip install pandas numpy
"""

import pandas as pd
import numpy as np
import sys

print("🐍 Добро пожаловать в Python для анализа данных!")
print("=" * 60)

# Загружаем данные интернет-магазина
print("📥 Загружаем данные из файла shop_data.csv...")

try:
    # Загрузка с правильной кодировкой, разделителем и десятичным форматом
    data = pd.read_csv('shop_data.csv', 
                       encoding='utf-8', 
                       sep=';',
                       decimal=',')  # Используем запятую как разделитель дробей
    print("✅ Данные успешно загружены!")
    
except FileNotFoundError:
    print("❌ ОШИБКА: Файл shop_data.csv не найден в текущей папке.")
    print("   Убедитесь, что файл находится рядом с этим скриптом.")
    sys.exit(1)
    
except Exception as e:
    print(f"❌ ОШИБКА при загрузке данных: {e}")
    print("   Проверьте формат файла shop_data.csv")
    sys.exit(1)

print(f"\n📊 ОСНОВНАЯ ИНФОРМАЦИЯ О ДАННЫХ:")
print("=" * 45)
print(f"📦 Количество строк (заказов): {len(data):,}")
print(f"📋 Количество столбцов: {len(data.columns)}")
print(f"💾 Размер данных в памяти: {data.memory_usage(deep=True).sum() / 1024:.1f} KB")
print(f"📅 Период данных: с {data['order_date'].min()} по {data['order_date'].max()}")

# Информация о столбцах
print(f"\n📋 СТРУКТУРА ДАННЫХ - НАЗВАНИЯ СТОЛБЦОВ:")
print("=" * 50)
for i, col in enumerate(data.columns, 1):
    print(f"{i:2d}. {col}")

# Проверяем типы данных
print(f"\n🔍 ТИПЫ ДАННЫХ В СТОЛБЦАХ:")
print("=" * 35)
for col in data.columns:
    dtype = data[col].dtype
    null_count = data[col].isnull().sum()
    print(f"• {col:15} - {dtype} (пропусков: {null_count})")

print(f"\n📊 ПЕРВЫЕ 5 СТРОК ДАННЫХ:")
print("=" * 35)
print(data.head())

print(f"\n📈 ОСНОВНЫЕ ФИНАНСОВЫЕ ПОКАЗАТЕЛИ:")
print("=" * 40)

# Основная статистика по выручке
total_revenue = data['total_amount'].sum()
average_order = data['total_amount'].mean()
median_order = data['total_amount'].median()
max_order = data['total_amount'].max()
min_order = data['total_amount'].min()
std_order = data['total_amount'].std()

print(f"💰 Общая выручка магазина: {total_revenue:,.2f} руб.")
print(f"🛒 Средний чек заказа: {average_order:,.2f} руб.")
print(f"📊 Медианный чек: {median_order:,.2f} руб.")
print(f"💎 Максимальный заказ: {max_order:,.2f} руб.")
print(f"🔻 Минимальный заказ: {min_order:,.2f} руб.")
print(f"📏 Стандартное отклонение: {std_order:,.2f} руб.")

# Дополнительная статистика
total_quantity = data['quantity'].sum()
average_quantity = data['quantity'].mean()
unique_customers = data['customer_id'].nunique()
average_discount = data['discount_percent'].mean()

print(f"\n📦 ДОПОЛНИТЕЛЬНАЯ СТАТИСТИКА:")
print("=" * 35)
print(f"📦 Общее количество товаров продано: {total_quantity:,} шт.")
print(f"🛍 Среднее количество товаров в заказе: {average_quantity:.1f} шт.")
print(f"👥 Уникальных клиентов: {unique_customers:,} человек")
print(f"🏷 Средний размер скидки: {average_discount:.1f}%")

print(f"\n🏷️ АНАЛИЗ КАТЕГОРИЙ ТОВАРОВ:")
print("=" * 40)

# Статистика по категориям
category_stats = data['product_category'].value_counts()
category_revenue = data.groupby('product_category')['total_amount'].agg(['sum', 'mean', 'count'])

print("📊 Популярность категорий (по количеству заказов):")
for category, count in category_stats.items():
    percentage = (count / len(data)) * 100
    revenue = category_revenue.loc[category, 'sum']
    avg_check = category_revenue.loc[category, 'mean']
    print(f"• {category:12}: {count:3d} заказов ({percentage:4.1f}%) | "
          f"Выручка: {revenue:8,.0f} руб. | Средний чек: {avg_check:6,.0f} руб.")

print(f"\n🏙️ АНАЛИЗ ПО ГОРОДАМ:")
print("=" * 30)

# Статистика по городам
city_stats = data['city'].value_counts()
city_revenue = data.groupby('city')['total_amount'].agg(['sum', 'mean', 'count'])

print("📊 Активность по городам:")
for city, count in city_stats.items():
    percentage = (count / len(data)) * 100
    revenue = city_revenue.loc[city, 'sum']
    avg_check = city_revenue.loc[city, 'mean']
    print(f"• {city:15}: {count:3d} заказов ({percentage:4.1f}%) | "
          f"Выручка: {revenue:8,.0f} руб. | Средний чек: {avg_check:6,.0f} руб.")

print(f"\n💳 СПОСОБЫ ОПЛАТЫ:")
print("=" * 25)

# Статистика по способам оплаты
payment_stats = data['payment_method'].value_counts()
payment_revenue = data.groupby('payment_method')['total_amount'].agg(['sum', 'mean', 'count'])

print("💰 Предпочтения клиентов в оплате:")
for method, count in payment_stats.items():
    percentage = (count / len(data)) * 100
    revenue = payment_revenue.loc[method, 'sum']
    avg_check = payment_revenue.loc[method, 'mean']
    print(f"• {method:18}: {count:3d} заказов ({percentage:4.1f}%) | "
          f"Выручка: {revenue:8,.0f} руб. | Средний чек: {avg_check:6,.0f} руб.")

print(f"\n📅 АНАЛИЗ ПО ДНЯМ НЕДЕЛИ:")
print("=" * 35)

# Статистика по дням недели
dow_stats = data['day_of_week'].value_counts()
dow_revenue = data.groupby('day_of_week')['total_amount'].agg(['sum', 'mean', 'count'])

print("📊 Когда клиенты покупают больше всего:")
# Сортируем дни недели в правильном порядке
days_order = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
for day in days_order:
    if day in dow_stats.index:
        count = dow_stats[day]
        percentage = (count / len(data)) * 100
        revenue = dow_revenue.loc[day, 'sum']
        avg_check = dow_revenue.loc[day, 'mean']
        print(f"• {day:11}: {count:3d} заказов ({percentage:4.1f}%) | "
              f"Выручка: {revenue:8,.0f} руб. | Средний чек: {avg_check:6,.0f} руб.")

print(f"\n📈 АНАЛИЗ ПО МЕСЯЦАМ:")
print("=" * 30)

# Добавляем столбец с месяцем для анализа трендов
data['order_month'] = pd.to_datetime(data['order_date']).dt.to_period('M')
monthly_stats = data.groupby('order_month').agg({
    'order_id': 'count',
    'total_amount': ['sum', 'mean']
}).round(2)

print("📊 Динамика продаж по месяцам:")
for month in monthly_stats.index:
    count = monthly_stats.loc[month, ('order_id', 'count')]
    revenue = monthly_stats.loc[month, ('total_amount', 'sum')]
    avg_check = monthly_stats.loc[month, ('total_amount', 'mean')]
    print(f"• {month}: {count:3d} заказов | Выручка: {revenue:8,.0f} руб. | Средний чек: {avg_check:6,.0f} руб.")

print(f"\n🔍 ПОИСК ИНТЕРЕСНЫХ ФАКТОВ:")
print("=" * 40)

# Самый дорогой заказ
max_order_idx = data['total_amount'].idxmax()
max_order_info = data.loc[max_order_idx]
print(f"💎 Самый дорогой заказ:")
print(f"   • ID заказа: {max_order_info['order_id']}")
print(f"   • Товар: {max_order_info['product_name']}")
print(f"   • Категория: {max_order_info['product_category']}")
print(f"   • Сумма: {max_order_info['total_amount']:,.2f} руб.")
print(f"   • Город: {max_order_info['city']}")
print(f"   • Дата: {max_order_info['order_date']}")

# Самая популярная категория в каждом городе
print(f"\n🏆 Популярные категории по городам:")
city_category = data.groupby(['city', 'product_category']).size().unstack(fill_value=0)
for city in data['city'].unique():
    city_data = data[data['city'] == city]
    top_category = city_data['product_category'].value_counts().index[0]
    count = city_data['product_category'].value_counts().iloc[0]
    percentage = (count / len(city_data)) * 100
    print(f"   • {city}: {top_category} ({count} заказов, {percentage:.1f}%)")

# Средний чек по способам оплаты с анализом
print(f"\n💰 Детальный анализ по способам оплаты:")
payment_analysis = data.groupby('payment_method').agg({
    'total_amount': ['count', 'sum', 'mean', 'median'],
    'quantity': 'mean'
}).round(2)

for method in data['payment_method'].unique():
    method_data = payment_analysis.loc[method]
    count = int(method_data[('total_amount', 'count')])
    total = method_data[('total_amount', 'sum')]
    mean_check = method_data[('total_amount', 'mean')]
    median_check = method_data[('total_amount', 'median')]
    avg_qty = method_data[('quantity', 'mean')]
    
    print(f"   • {method}:")
    print(f"     - Заказов: {count}, Выручка: {total:,.0f} руб.")
    print(f"     - Средний чек: {mean_check:,.0f} руб., Медианный: {median_check:,.0f} руб.")
    print(f"     - Среднее кол-во товаров: {avg_qty:.1f} шт.")

print(f"\n🎯 КЛЮЧЕВЫЕ ВЫВОДЫ И ИНСАЙТЫ:")
print("=" * 40)

# Автоматические выводы на основе данных
total_days = (pd.to_datetime(data['order_date'].max()) - pd.to_datetime(data['order_date'].min())).days
avg_daily_revenue = total_revenue / total_days if total_days > 0 else 0
avg_daily_orders = len(data) / total_days if total_days > 0 else 0

print("📈 Общая производительность:")
print(f"   • Средняя дневная выручка: {avg_daily_revenue:,.0f} руб.")
print(f"   • Среднее количество заказов в день: {avg_daily_orders:.1f}")
print(f"   • Конверсия в покупку: данных недостаточно")

print(f"\n🔍 Интересные находки:")
# Находим день недели с максимальной выручкой
best_day = dow_revenue['sum'].idxmax()
best_day_revenue = dow_revenue.loc[best_day, 'sum']
print(f"   • Самый прибыльный день недели: {best_day} ({best_day_revenue:,.0f} руб.)")

# Находим самую прибыльную категорию
best_category = category_revenue['sum'].idxmax()
best_category_revenue = category_revenue.loc[best_category, 'sum']
best_category_percent = (best_category_revenue / total_revenue) * 100
print(f"   • Самая прибыльная категория: {best_category} ({best_category_percent:.1f}% от общей выручки)")

# Анализ скидок
orders_with_discount = data[data['discount_percent'] > 0]
discount_impact = orders_with_discount['total_amount'].mean() - data[data['discount_percent'] == 0]['total_amount'].mean()
print(f"   • Заказов со скидкой: {len(orders_with_discount)} из {len(data)} ({len(orders_with_discount)/len(data)*100:.1f}%)")

print(f"\n✅ ПРОВЕРКА КАЧЕСТВА ДАННЫХ:")
print("=" * 35)
print("🔍 Проверяем данные на ошибки и аномалии...")

# Проверки качества данных
issues_found = 0

# Проверка на пропущенные значения
missing_data = data.isnull().sum()
if missing_data.sum() > 0:
    print("⚠️  Найдены пропущенные значения:")
    for col, count in missing_data[missing_data > 0].items():
        print(f"     • {col}: {count} пропусков")
    issues_found += 1

# Проверка на отрицательные цены или суммы
negative_prices = data[data['price'] < 0]
if len(negative_prices) > 0:
    print(f"⚠️  Найдены отрицательные цены: {len(negative_prices)} записей")
    issues_found += 1

negative_amounts = data[data['total_amount'] < 0]
if len(negative_amounts) > 0:
    print(f"⚠️  Найдены отрицательные суммы: {len(negative_amounts)} записей")
    issues_found += 1

# Проверка логики скидок
discount_logic = data[data['total_amount'] > data['price'] * data['quantity']]
if len(discount_logic) > 0:
    print(f"⚠️  Найдены логические ошибки в скидках: {len(discount_logic)} записей")
    issues_found += 1

if issues_found == 0:
    print("✅ Данные выглядят корректно! Ошибок не обнаружено.")

print(f"\n🚀 РЕКОМЕНДАЦИИ ДЛЯ ДАЛЬНЕЙШЕГО АНАЛИЗА:")
print("=" * 50)
print("📊 На основе первичного анализа рекомендуем изучить:")
print("   1. Сезонность продаж - есть ли пики в определенные месяцы?")
print("   2. Поведение клиентов - кто покупает чаще всего?")
print("   3. Эффективность скидок - увеличивают ли они средний чек?")
print("   4. География продаж - в каких городах потенциал роста?")
print("   5. Товарная матрица - какие товары продаются вместе?")

print(f"\n🎓 ЗАКЛЮЧЕНИЕ:")
print("=" * 20)
print("✅ Python успешно загрузил и проанализировал данные!")
print("📊 Вы увидели основные возможности анализа данных:")
print("   • Загрузка данных из файлов с правильным форматированием")
print("   • Быстрый расчет статистик и показателей")
print("   • Группировка и агрегация данных по разным критериям")  
print("   • Поиск интересных закономерностей и инсайтов")
print("   • Проверка качества данных на ошибки")
print("   • Формулирование выводов и рекомендаций")

print(f"\n🚀 Теперь вы готовы к более сложным анализам в следующих главах!")
print("💡 Попробуйте повторить этот анализ в Excel и сравните результаты.")
print("📈 В следующей главе мы изучим описательную статистику более подробно.")

print("\n" + "="*60)
print("🐍 Анализ завершен! Спасибо за внимание!")
print("="*60)