#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Глава 1: Что такое аналитика данных
Скрипт: Базовый анализ данных интернет-магазина

Этот скрипт демонстрирует основные принципы анализа данных:
- Загрузка и первичный осмотр данных
- Расчет ключевых показателей
- Создание простых визуализаций
- Формулирование выводов

Автор: Analytics Course
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Настройка отображения
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 12
sns.set_style("whitegrid")

# Настройка для корректного отображения русских символов
plt.rcParams['font.family'] = ['DejaVu Sans']

def load_data(file_path):
    """
    Загружает данные из CSV файла с правильными настройками

    Args:
        file_path (str): Путь к CSV файлу

    Returns:
        pandas.DataFrame: Загруженные данные
    """
    try:
        df = pd.read_csv(file_path, sep=';', decimal=',', encoding='utf-8-sig')
        df['order_date'] = pd.to_datetime(df['order_date'])
        print("✅ Данные успешно загружены!")
        return df
    except Exception as e:
        print(f"❌ Ошибка при загрузке данных: {e}")
        return None

def basic_info(df):
    """
    Выводит базовую информацию о датасете

    Args:
        df (pandas.DataFrame): Датафрейм с данными
    """
    print("\n📊 БАЗОВАЯ ИНФОРМАЦИЯ О ДАННЫХ")
    print("=" * 50)
    print(f"Количество записей: {len(df):,}")
    print(f"Количество столбцов: {df.shape[1]}")
    print(f"Период данных: {df['order_date'].min().date()} - {df['order_date'].max().date()}")
    print(f"Пропущенные значения: {df.isnull().sum().sum()}")

    print("\n📋 Структура данных:")
    print(df.dtypes.to_string())

    print("\n👀 Первые 5 записей:")
    print(df.head().to_string(index=False))

def calculate_kpi(df):
    """
    Рассчитывает ключевые показатели эффективности

    Args:
        df (pandas.DataFrame): Датафрейм с данными

    Returns:
        dict: Словарь с KPI
    """
    kpi = {
        'total_revenue': df['total_amount'].sum(),
        'total_orders': len(df),
        'average_order_value': df['total_amount'].mean(),
        'unique_customers': df['customer_name'].nunique(),
        'orders_per_customer': len(df) / df['customer_name'].nunique()
    }

    print("\n💰 КЛЮЧЕВЫЕ ПОКАЗАТЕЛИ")
    print("=" * 50)
    print(f"Общая выручка: {kpi['total_revenue']:,.2f} руб.")
    print(f"Количество заказов: {kpi['total_orders']:,}")
    print(f"Средний чек: {kpi['average_order_value']:,.2f} руб.")
    print(f"Уникальных клиентов: {kpi['unique_customers']:,}")
    print(f"Заказов на клиента: {kpi['orders_per_customer']:.2f}")

    return kpi

def analyze_categories(df):
    """
    Анализирует продажи по категориям товаров

    Args:
        df (pandas.DataFrame): Датафрейм с данными
    """
    print("\n🛍️ АНАЛИЗ ПО КАТЕГОРИЯМ")
    print("=" * 50)

    category_analysis = df.groupby('category').agg({
        'total_amount': ['sum', 'mean', 'count']
    }).round(2)

    category_analysis.columns = ['Выручка', 'Средний_чек', 'Количество_заказов']
    category_analysis = category_analysis.sort_values('Выручка', ascending=False)

    print(category_analysis.to_string())

    # Визуализация
    plt.figure(figsize=(12, 8))

    # График 1: Выручка по категориям
    plt.subplot(2, 2, 1)
    category_analysis['Выручка'].plot(kind='bar', color='skyblue')
    plt.title('Выручка по категориям')
    plt.ylabel('Выручка (руб.)')
    plt.xticks(rotation=45)

    # График 2: Количество заказов
    plt.subplot(2, 2, 2)
    category_analysis['Количество_заказов'].plot(kind='bar', color='lightgreen')
    plt.title('Количество заказов по категориям')
    plt.ylabel('Количество заказов')
    plt.xticks(rotation=45)

    # График 3: Средний чек
    plt.subplot(2, 2, 3)
    category_analysis['Средний_чек'].plot(kind='bar', color='orange')
    plt.title('Средний чек по категориям')
    plt.ylabel('Средний чек (руб.)')
    plt.xticks(rotation=45)

    # График 4: Круговая диаграмма выручки
    plt.subplot(2, 2, 4)
    category_analysis['Выручка'].plot(kind='pie', autopct='%1.1f%%')
    plt.title('Доля категорий в выручке')
    plt.ylabel('')

    plt.tight_layout()
    plt.savefig('category_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()

def analyze_time_trends(df):
    """
    Анализирует временные тренды в данных

    Args:
        df (pandas.DataFrame): Датафрейм с данными
    """
    print("\n📈 ВРЕМЕННОЙ АНАЛИЗ")
    print("=" * 50)

    # Анализ по месяцам
    df['month'] = df['order_date'].dt.month
    df['month_name'] = df['order_date'].dt.strftime('%B')

    monthly_stats = df.groupby(['month', 'month_name']).agg({
        'total_amount': ['sum', 'count', 'mean']
    }).round(2)

    monthly_stats.columns = ['Выручка', 'Заказов', 'Средний_чек']
    print("Статистика по месяцам:")
    print(monthly_stats.to_string())

    # Визуализация временных трендов
    plt.figure(figsize=(15, 5))

    # График 1: Динамика выручки
    plt.subplot(1, 3, 1)
    monthly_stats['Выручка'].plot(kind='line', marker='o', color='blue')
    plt.title('Динамика выручки по месяцам')
    plt.ylabel('Выручка (руб.)')
    plt.xlabel('Месяц')

    # График 2: Количество заказов
    plt.subplot(1, 3, 2)
    monthly_stats['Заказов'].plot(kind='line', marker='s', color='green')
    plt.title('Количество заказов по месяцам')
    plt.ylabel('Количество заказов')
    plt.xlabel('Месяц')

    # График 3: Средний чек
    plt.subplot(1, 3, 3)
    monthly_stats['Средний_чек'].plot(kind='line', marker='^', color='red')
    plt.title('Средний чек по месяцам')
    plt.ylabel('Средний чек (руб.)')
    plt.xlabel('Месяц')

    plt.tight_layout()
    plt.savefig('time_trends.png', dpi=300, bbox_inches='tight')
    plt.show()

def analyze_geography(df):
    """
    Анализирует географическое распределение заказов

    Args:
        df (pandas.DataFrame): Датафрейм с данными
    """
    print("\n🗺️ ГЕОГРАФИЧЕСКИЙ АНАЛИЗ")
    print("=" * 50)

    geo_stats = df.groupby('city').agg({
        'total_amount': ['sum', 'mean', 'count']
    }).round(2)

    geo_stats.columns = ['Выручка', 'Средний_чек', 'Заказов']
    geo_stats = geo_stats.sort_values('Выручка', ascending=False)

    print("Топ-10 городов по выручке:")
    print(geo_stats.head(10).to_string())

    # Визуализация
    plt.figure(figsize=(12, 6))

    # График 1: Топ-5 городов по выручке
    plt.subplot(1, 2, 1)
    geo_stats.head(5)['Выручка'].plot(kind='bar', color='purple')
    plt.title('Топ-5 городов по выручке')
    plt.ylabel('Выручка (руб.)')
    plt.xticks(rotation=45)

    # График 2: Количество заказов по городам
    plt.subplot(1, 2, 2)
    geo_stats.head(5)['Заказов'].plot(kind='bar', color='teal')
    plt.title('Топ-5 городов по количеству заказов')
    plt.ylabel('Количество заказов')
    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.savefig('geography_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()

def generate_insights(df, kpi):
    """
    Генерирует ключевые инсайты на основе анализа

    Args:
        df (pandas.DataFrame): Датафрейм с данными
        kpi (dict): Ключевые показатели
    """
    print("\n💡 КЛЮЧЕВЫЕ ИНСАЙТЫ")
    print("=" * 50)

    # Инсайт 1: Самая прибыльная категория
    top_category = df.groupby('category')['total_amount'].sum().idxmax()
    top_category_revenue = df.groupby('category')['total_amount'].sum().max()
    total_revenue = df['total_amount'].sum()
    category_share = (top_category_revenue / total_revenue) * 100

    print(f"1. 📱 Самая прибыльная категория: {top_category}")
    print(f"   Доля в выручке: {category_share:.1f}% ({top_category_revenue:,.0f} руб.)")

    # Инсайт 2: Лучший город
    top_city = df.groupby('city')['total_amount'].sum().idxmax()
    top_city_orders = df[df['city'] == top_city].shape[0]

    print(f"\n2. 🏙️ Лидер по продажам: {top_city}")
    print(f"   Количество заказов: {top_city_orders}")

    # Инсайт 3: Клиентская лояльность
    repeat_customers = df['customer_name'].value_counts()
    loyal_customers = (repeat_customers > 1).sum()
    loyalty_rate = (loyal_customers / kpi['unique_customers']) * 100

    print(f"\n3. 👥 Повторные покупки:")
    print(f"   Клиентов с повторными заказами: {loyal_customers} из {kpi['unique_customers']}")
    print(f"   Уровень лояльности: {loyalty_rate:.1f}%")

    # Инсайт 4: Способы оплаты
    payment_stats = df['payment_method'].value_counts()
    top_payment = payment_stats.index[0]
    top_payment_share = (payment_stats.iloc[0] / len(df)) * 100

    print(f"\n4. 💳 Предпочтительный способ оплаты: {top_payment}")
    print(f"   Доля: {top_payment_share:.1f}% заказов")

    print("\n📋 РЕКОМЕНДАЦИИ:")
    print("1. Увеличить маркетинговые расходы на категорию", top_category)
    print("2. Развивать присутствие в городе", top_city)
    print("3. Внедрить программу лояльности для повторных покупок")
    print("4. Оптимизировать процесс оплаты через", top_payment.lower())

def main():
    """
    Главная функция, выполняющая весь анализ
    """
    print("🚀 ЗАПУСК АНАЛИЗА ДАННЫХ ИНТЕРНЕТ-МАГАЗИНА")
    print("=" * 60)

    # Загружаем данные
    df = load_data('shop_sales_data.csv')
    if df is None:
        return

    # Базовая информация
    basic_info(df)

    # Расчет KPI
    kpi = calculate_kpi(df)

    # Анализ по категориям
    analyze_categories(df)

    # Временной анализ
    analyze_time_trends(df)

    # Географический анализ
    analyze_geography(df)

    # Генерация инсайтов
    generate_insights(df, kpi)

    print("\n✅ АНАЛИЗ ЗАВЕРШЕН!")
    print("Созданы файлы: category_analysis.png, time_trends.png, geography_analysis.png")

if __name__ == "__main__":
    main()
