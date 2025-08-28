# Утилитарные функции для описательной статистики

"""
Этот скрипт содержит функции для быстрого анализа любых наборов данных.
Используйте в Jupyter Notebook или любом Python-скрипте.
"""

def analyze_data(data, name="Показатель", unit=""):
    """Комплексный анализ любого набора данных"""
    import pandas as pd
    import numpy as np
    
    series = pd.Series(data)
    stats = {
        'Среднее': series.mean(),
        'Медиана': series.median(), 
        'Стд.откл': series.std(),
        'Минимум': series.min(),
        'Максимум': series.max(),
        'Размах': series.max() - series.min(),
        'Q1': series.quantile(0.25),
        'Q3': series.quantile(0.75)
    }
    stats['IQR'] = stats['Q3'] - stats['Q1']
    
    print(f"\n📊 Анализ: {name}")
    print("="*40)
    for key in ['Среднее','Медиана','Стд.откл','Минимум','Максимум','Размах']:
        val = stats[key]
        print(f"{key}: {val:.1f} {unit}")
    
    # Поиск выбросов
    lb = stats['Q1'] - 1.5 * stats['IQR']
    ub = stats['Q3'] + 1.5 * stats['IQR']
    outliers = series[(series < lb) | (series > ub)]
    if not outliers.empty:
        print(f"\n⚠️ Найдено выбросов: {len(outliers)}")
        print(outliers.tolist())

    return stats


def compare_groups(group1, group2, name1="Группа1", name2="Группа2"):
    """Сравнение двух групп данных по ключевым метрикам"""
    print(f"\n🔍 Сравнение: {name1} vs {name2}")
    print("="*50)
    stats1 = analyze_data(group1, name1)
    stats2 = analyze_data(group2, name2)
    
    # Сравнение средних
    diff = (stats2['Среднее'] - stats1['Среднее']) / stats1['Среднее'] * 100
    print(f"\n📈 Разница в средних: {diff:+.1f}%")
    
    # Сравнение стабильности
    cv1 = stats1['Стд.откл']/stats1['Среднее']*100
    cv2 = stats2['Стд.откл']/stats2['Среднее']*100
    print(f"📊 Коэф. вариации: {name1}: {cv1:.1f}%, {name2}: {cv2:.1f}%")
    if cv1 < cv2:
        print(f"→ {name1} стабильнее")
    else:
        print(f"→ {name2} стабильнее")
