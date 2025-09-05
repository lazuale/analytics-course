#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Глава 3: Визуализация и сводные таблицы
Скрипт: Интерактивный веб-дашборд с Streamlit

Этот скрипт создает полнофункциональный веб-дашборд:
- Фильтры по датам, городам и категориям
- Интерактивные графики с Plotly
- Экспорт данных и отчетов
- Режим реального времени

Запуск: streamlit run 03_interactive_dashboard.py

Автор: Analytics Course
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date
import numpy as np

# Настройка страницы
st.set_page_config(
    page_title="ТехноМарт - Аналитический дашборд",
    page_icon="🏪",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data
def load_data():
    """Загружает данные с кэшированием"""
    try:
        df = pd.read_csv('retail_sales_data.csv', sep=';', decimal=',', encoding='utf-8-sig')
        df['date'] = pd.to_datetime(df['date'])
        return df
    except FileNotFoundError:
        st.error("❌ Файл retail_sales_data.csv не найден!")
        st.stop()

def main():
    # Заголовок приложения
    st.title("🏪 ТехноМарт - Аналитический дашборд")
    st.markdown("---")

    # Загрузка данных
    df = load_data()

    # Боковая панель с фильтрами
    st.sidebar.header("🎛 Фильтры данных")

    # Фильтр по датам
    date_range = st.sidebar.date_input(
        "Выберите период",
        value=[df['date'].min().date(), df['date'].max().date()],
        min_value=df['date'].min().date(),
        max_value=df['date'].max().date()
    )

    # Фильтр по городам
    cities = st.sidebar.multiselect(
        "Выберите города",
        options=sorted(df['city'].unique()),
        default=sorted(df['city'].unique())
    )

    # Фильтр по категориям
    categories = st.sidebar.multiselect(
        "Выберите категории",
        options=sorted(df['category'].unique()),
        default=sorted(df['category'].unique())
    )

    # Применение фильтров
    if len(date_range) == 2:
        mask = (df['date'].dt.date >= date_range[0]) & (df['date'].dt.date <= date_range[1])
        filtered_df = df[mask]
    else:
        filtered_df = df

    filtered_df = filtered_df[filtered_df['city'].isin(cities)]
    filtered_df = filtered_df[filtered_df['category'].isin(categories)]

    # Основные метрики
    col1, col2, col3, col4 = st.columns(4)

    total_revenue = filtered_df['total_amount'].sum()
    total_transactions = len(filtered_df)
    avg_check = filtered_df['total_amount'].mean()
    total_profit = filtered_df['profit'].sum()

    col1.metric("💰 Выручка", f"{total_revenue:,.0f} ₽")
    col2.metric("🛒 Транзакций", f"{total_transactions:,}")
    col3.metric("💳 Средний чек", f"{avg_check:,.0f} ₽")
    col4.metric("📈 Прибыль", f"{total_profit:,.0f} ₽")

    st.markdown("---")

    # Графики в два столбца
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📈 Динамика продаж")
        monthly_sales = filtered_df.groupby(filtered_df['date'].dt.to_period('M'))['total_amount'].sum().reset_index()
        monthly_sales['date'] = monthly_sales['date'].astype(str)

        fig_trend = px.line(monthly_sales, x='date', y='total_amount',
                           title="Выручка по месяцам")
        st.plotly_chart(fig_trend, use_container_width=True)

    with col2:
        st.subheader("🏙 Продажи по городам")
        city_sales = filtered_df.groupby('city')['total_amount'].sum().sort_values(ascending=True)

        fig_cities = px.bar(x=city_sales.values, y=city_sales.index,
                           orientation='h', title="Выручка по городам")
        st.plotly_chart(fig_cities, use_container_width=True)

    # Вторая строка графиков
    col3, col4 = st.columns(2)

    with col3:
        st.subheader("📦 Структура продаж")
        category_sales = filtered_df.groupby('category')['total_amount'].sum()

        fig_pie = px.pie(values=category_sales.values, names=category_sales.index,
                        title="Доли категорий в выручке")
        st.plotly_chart(fig_pie, use_container_width=True)

    with col4:
        st.subheader("📊 Средний чек по категориям")
        avg_check_cat = filtered_df.groupby('category')['total_amount'].mean().sort_values()

        fig_avg = px.bar(x=avg_check_cat.values, y=avg_check_cat.index,
                        orientation='h', title="Средний чек")
        st.plotly_chart(fig_avg, use_container_width=True)

    # Детальная таблица
    st.markdown("---")
    st.subheader("📋 Детальные данные")

    # Показать только последние N записей для производительности
    display_rows = st.slider("Количество строк для отображения", 10, 100, 20)
    st.dataframe(filtered_df.tail(display_rows))

    # Кнопки экспорта
    st.markdown("---")
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📥 Экспорт в CSV"):
            csv = filtered_df.to_csv(sep=';', decimal=',', index=False)
            st.download_button(
                label="Скачать CSV",
                data=csv,
                file_name=f"technomart_data_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )

    with col2:
        if st.button("📊 Сводная статистика"):
            st.json({
                "total_revenue": float(total_revenue),
                "total_transactions": int(total_transactions),
                "avg_check": float(avg_check),
                "total_profit": float(total_profit),
                "margin_percent": float(total_profit / total_revenue * 100)
            })

if __name__ == "__main__":
    main()
