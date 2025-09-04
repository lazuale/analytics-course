"""
🧹 Шаблон для очистки данных
Используйте этот скрипт как основу для лечения "больных" данных
"""

import pandas as pd
import numpy as np
from datetime import datetime

def diagnose_data(df):
    """Диагностика проблем в данных"""
    print("🩺 ДИАГНОСТИКА ДАННЫХ")
    print("=" * 20)

    print(f"📏 Размер: {df.shape[0]} строк, {df.shape[1]} столбцов")
    print(f"❌ Пропуски: {df.isnull().sum().sum()}")
    print(f"🔄 Дубликаты: {df.duplicated().sum()}")

    print("\n📊 Типы данных:")
    for col, dtype in df.dtypes.items():
        print(f"   {col}: {dtype}")

    return df

def clean_duplicates(df):
    """Удаление дубликатов"""
    print("\n🧹 Удаление дубликатов...")

    before = len(df)
    df = df.drop_duplicates()
    after = len(df)

    print(f"   Удалено: {before - after} дубликатов")
    return df

def fix_data_types(df):
    """Исправление типов данных"""
    print("\n🔧 Исправление типов данных...")

    # Пример: исправляем цены
    if 'price' in df.columns:
        # Убираем символы валют и приводим к числам
        df['price'] = df['price'].astype(str).str.replace('$', '').str.replace('free', '0')
        df['price'] = pd.to_numeric(df['price'], errors='coerce')
        print("   ✅ Цены исправлены")

    # Пример: исправляем даты
    if 'order_date' in df.columns:
        df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
        print("   ✅ Даты исправлены")

    return df

def handle_missing_values(df):
    """Обработка пропущенных значений"""
    print("\n💊 Обработка пропусков...")

    # Заполняем пропуски в числовых столбцах медианой
    numeric_columns = df.select_dtypes(include=[np.number]).columns
    for col in numeric_columns:
        if df[col].isnull().sum() > 0:
            df[col] = df[col].fillna(df[col].median())
            print(f"   ✅ {col}: заполнено медианой")

    # Заполняем пропуски в текстовых столбцах
    text_columns = df.select_dtypes(include=['object']).columns
    for col in text_columns:
        if df[col].isnull().sum() > 0:
            df[col] = df[col].fillna('Неизвестно')
            print(f"   ✅ {col}: заполнено 'Неизвестно'")

    return df

def standardize_text(df):
    """Стандартизация текстовых полей"""
    print("\n📝 Стандартизация текста...")

    text_columns = df.select_dtypes(include=['object']).columns
    for col in text_columns:
        if col not in ['order_date']:  # Пропускаем даты
            df[col] = df[col].astype(str).str.strip().str.title()
            print(f"   ✅ {col}: стандартизирован")

    return df

# Главная функция очистки
def clean_data(filepath):
    """Полная очистка данных"""
    print("🏥 Начинаем лечение данных...")

    # Загружаем данные
    try:
        df = pd.read_csv(filepath)
        print(f"✅ Данные загружены: {filepath}")
    except FileNotFoundError:
        print(f"❌ Файл не найден: {filepath}")
        return None

    # Применяем все этапы лечения
    df = diagnose_data(df)
    df = clean_duplicates(df)
    df = fix_data_types(df)
    df = handle_missing_values(df)
    df = standardize_text(df)

    # Финальная проверка
    print("\n🎉 Лечение завершено!")
    print(f"📊 Итоговый размер: {df.shape[0]} строк, {df.shape[1]} столбцов")
    print(f"✅ Качество: {df.isnull().sum().sum()} пропусков, {df.duplicated().sum()} дубликатов")

    return df

# Пример использования
if __name__ == "__main__":
    # Раскомментируйте для использования:
    # cleaned_df = clean_data('messy_ecommerce_data.csv')
    # cleaned_df.to_csv('cleaned_data.csv', index=False)

    print("👨‍⚕️ Шаблон доктора данных готов к использованию!")
    print("Измените путь к файлу и запустите лечение.")
