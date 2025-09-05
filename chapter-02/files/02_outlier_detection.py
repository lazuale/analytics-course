#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Глава 2: Описательная статистика
Скрипт: Продвинутые методы выявления выбросов в зарплатных данных

Этот скрипт демонстрирует различные методы поиска аномалий:
- Метод межквартильного размаха (IQR)
- Z-score метод
- Модифицированный Z-score метод
- Метод Isolation Forest (продвинутый)

Автор: Analytics Course
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from sklearn.ensemble import IsolationForest
import warnings
warnings.filterwarnings('ignore')

# Настройка отображения
plt.rcParams['figure.figsize'] = (14, 10)
plt.rcParams['font.size'] = 10
sns.set_style("whitegrid")

# Настройка для корректного отображения русских символов  
plt.rcParams['font.family'] = ['DejaVu Sans']

def load_data(file_path):
    """
    Загружает HR данные из CSV файла

    Args:
        file_path (str): Путь к CSV файлу

    Returns:
        pandas.DataFrame: Загруженные данные
    """
    try:
        df = pd.read_csv(file_path, sep=';', decimal=',', encoding='utf-8-sig')
        print("✅ HR данные загружены для анализа выбросов!")
        return df
    except Exception as e:
        print(f"❌ Ошибка при загрузке данных: {e}")
        return None

def iqr_method(data, column='salary', multiplier=1.5):
    """
    Выявляет выбросы методом межквартильного размаха (IQR)

    Args:
        data (DataFrame): Данные
        column (str): Название колонки для анализа
        multiplier (float): Множитель для IQR (обычно 1.5)

    Returns:
        dict: Результаты анализа
    """
    print("\n" + "="*60)
    print("📊 МЕТОД МЕЖКВАРТИЛЬНОГО РАЗМАХА (IQR)")
    print("="*60)

    values = data[column]

    # Расчет квартилей
    Q1 = values.quantile(0.25)
    Q3 = values.quantile(0.75)
    IQR = Q3 - Q1

    # Границы выбросов
    lower_bound = Q1 - multiplier * IQR
    upper_bound = Q3 + multiplier * IQR

    print(f"\n📏 СТАТИСТИЧЕСКИЕ ГРАНИЦЫ:")
    print(f"Q1 (25-й процентиль): {Q1:,.0f} руб.")
    print(f"Q3 (75-й процентиль): {Q3:,.0f} руб.")
    print(f"Межквартильный размах (IQR): {IQR:,.0f} руб.")
    print(f"Нижняя граница: {lower_bound:,.0f} руб.")
    print(f"Верхняя граница: {upper_bound:,.0f} руб.")

    # Поиск выбросов
    outliers_mask = (values < lower_bound) | (values > upper_bound)
    outliers = data[outliers_mask].copy()

    # Классификация выбросов
    mild_outliers = data[(values > upper_bound) & (values <= upper_bound + IQR)].copy()
    extreme_outliers = data[values > upper_bound + IQR].copy()

    print(f"\n🔍 РЕЗУЛЬТАТЫ ПОИСКА:")
    print(f"Общее количество выбросов: {len(outliers)} ({len(outliers)/len(data)*100:.1f}%)")
    print(f"Умеренные выбросы: {len(mild_outliers)}")
    print(f"Экстремальные выбросы: {len(extreme_outliers)}")

    if len(outliers) > 0:
        print(f"\n💰 ДИАПАЗОН ВЫБРОСОВ:")
        print(f"Минимальный выброс: {outliers[column].min():,.0f} руб.")
        print(f"Максимальный выброс: {outliers[column].max():,.0f} руб.")

    return {
        'method': 'IQR',
        'outliers': outliers,
        'outliers_mask': outliers_mask,
        'bounds': (lower_bound, upper_bound),
        'mild_outliers': mild_outliers,
        'extreme_outliers': extreme_outliers
    }

def zscore_method(data, column='salary', threshold=3):
    """
    Выявляет выбросы методом Z-score

    Args:
        data (DataFrame): Данные
        column (str): Название колонки для анализа  
        threshold (float): Пороговое значение |Z| (обычно 2.5-3)

    Returns:
        dict: Результаты анализа
    """
    print("\n" + "="*60)
    print("📈 МЕТОД Z-SCORE (СТАНДАРТИЗОВАННЫЕ ОТКЛОНЕНИЯ)")
    print("="*60)

    values = data[column]

    # Расчет Z-scores
    mean_val = values.mean()
    std_val = values.std()
    z_scores = np.abs((values - mean_val) / std_val)

    print(f"\n📊 ПАРАМЕТРЫ РАСПРЕДЕЛЕНИЯ:")
    print(f"Среднее значение: {mean_val:,.0f} руб.")
    print(f"Стандартное отклонение: {std_val:,.0f} руб.")
    print(f"Пороговое значение |Z|: {threshold}")

    # Поиск выбросов
    outliers_mask = z_scores > threshold
    outliers = data[outliers_mask].copy()
    outliers['z_score'] = z_scores[outliers_mask]

    print(f"\n🔍 РЕЗУЛЬТАТЫ ПОИСКА:")
    print(f"Количество выбросов: {len(outliers)} ({len(outliers)/len(data)*100:.1f}%)")

    if len(outliers) > 0:
        print(f"\n📊 ХАРАКТЕРИСТИКИ ВЫБРОСОВ:")
        print(f"Максимальный |Z-score|: {z_scores.max():.2f}")
        print(f"Минимальный Z-score выброса: {z_scores[outliers_mask].min():.2f}")

        # Показываем самые экстремальные выбросы
        top_outliers = outliers.nlargest(5, 'z_score')[['first_name', 'last_name', 'department', 
                                                        'position', column, 'z_score']]
        print(f"\n🎯 ТОП-5 САМЫХ ЭКСТРЕМАЛЬНЫХ ВЫБРОСОВ:")
        print(top_outliers.to_string(index=False, float_format='%.2f'))

    return {
        'method': 'Z-Score',
        'outliers': outliers,
        'outliers_mask': outliers_mask,
        'z_scores': z_scores,
        'threshold': threshold
    }

def modified_zscore_method(data, column='salary', threshold=3.5):
    """
    Выявляет выбросы модифицированным методом Z-score (на основе медианы)

    Args:
        data (DataFrame): Данные
        column (str): Название колонки для анализа
        threshold (float): Пороговое значение (обычно 3.5)

    Returns:
        dict: Результаты анализа
    """
    print("\n" + "="*60)
    print("📊 МОДИФИЦИРОВАННЫЙ Z-SCORE МЕТОД (РОБАСТНЫЙ)")
    print("="*60)

    values = data[column]

    # Расчет модифицированных Z-scores
    median_val = values.median()
    mad = np.median(np.abs(values - median_val))  # Median Absolute Deviation
    modified_z_scores = 0.6745 * (values - median_val) / mad

    print(f"\n📊 РОБАСТНЫЕ ПАРАМЕТРЫ:")
    print(f"Медиана: {median_val:,.0f} руб.")
    print(f"MAD (медианное абсолютное отклонение): {mad:,.0f} руб.")
    print(f"Пороговое значение: {threshold}")

    # Поиск выбросов
    outliers_mask = np.abs(modified_z_scores) > threshold
    outliers = data[outliers_mask].copy()
    outliers['modified_z_score'] = modified_z_scores[outliers_mask]

    print(f"\n🔍 РЕЗУЛЬТАТЫ ПОИСКА:")
    print(f"Количество выбросов: {len(outliers)} ({len(outliers)/len(data)*100:.1f}%)")

    return {
        'method': 'Modified Z-Score',
        'outliers': outliers,
        'outliers_mask': outliers_mask,
        'modified_z_scores': modified_z_scores
    }

def isolation_forest_method(data, contamination=0.05):
    """
    Выявляет выбросы методом Isolation Forest (машинное обучение)

    Args:
        data (DataFrame): Данные
        contamination (float): Ожидаемая доля выбросов (0.05 = 5%)

    Returns:
        dict: Результаты анализа
    """
    print("\n" + "="*60)
    print("🤖 ISOLATION FOREST (МАШИННОЕ ОБУЧЕНИЕ)")
    print("="*60)

    # Подготовка признаков для анализа
    features = ['salary', 'years_experience', 'age', 'performance_rating']

    # Кодируем категориальные переменные
    data_encoded = data.copy()
    education_encoding = {'Bachelor': 1, 'Master': 2, 'PhD': 3}
    data_encoded['education_encoded'] = data['education_level'].map(education_encoding)

    features_extended = features + ['education_encoded']
    X = data_encoded[features_extended].fillna(0)

    print(f"\n🎯 ПАРАМЕТРЫ МОДЕЛИ:")
    print(f"Используемые признаки: {', '.join(features_extended)}")
    print(f"Ожидаемая доля выбросов: {contamination*100:.1f}%")

    # Обучение модели
    iso_forest = IsolationForest(contamination=contamination, random_state=42)
    outliers_pred = iso_forest.fit_predict(X)

    # Получение аномальных баллов
    anomaly_scores = iso_forest.decision_function(X)

    # Поиск выбросов (-1 означает выброс)
    outliers_mask = outliers_pred == -1
    outliers = data[outliers_mask].copy()
    outliers['anomaly_score'] = anomaly_scores[outliers_mask]

    print(f"\n🔍 РЕЗУЛЬТАТЫ АНАЛИЗА:")
    print(f"Количество выбросов: {len(outliers)} ({len(outliers)/len(data)*100:.1f}%)")

    if len(outliers) > 0:
        print(f"\n🎯 САМЫЕ АНОМАЛЬНЫЕ СОТРУДНИКИ:")
        top_anomalies = outliers.nsmallest(5, 'anomaly_score')[['first_name', 'last_name', 
                                                               'department', 'position', 
                                                               'salary', 'anomaly_score']]
        print(top_anomalies.to_string(index=False, float_format='%.3f'))

    return {
        'method': 'Isolation Forest',
        'outliers': outliers,
        'outliers_mask': outliers_mask,
        'anomaly_scores': anomaly_scores
    }

def compare_methods(data, results_list):
    """
    Сравнивает результаты разных методов поиска выбросов

    Args:
        data (DataFrame): Исходные данные
        results_list (list): Список результатов от разных методов
    """
    print("\n" + "="*60)
    print("⚖️ СРАВНЕНИЕ МЕТОДОВ ПОИСКА ВЫБРОСОВ")
    print("="*60)

    print("\n📊 СВОДКА ПО МЕТОДАМ:")
    for result in results_list:
        method_name = result['method']
        outliers_count = len(result['outliers'])
        percentage = outliers_count / len(data) * 100
        print(f"{method_name:20s}: {outliers_count:3d} выбросов ({percentage:4.1f}%)")

    # Пересечения между методами
    print("\n🔗 ПЕРЕСЕЧЕНИЯ МЕЖДУ МЕТОДАМИ:")

    if len(results_list) >= 2:
        mask1 = results_list[0]['outliers_mask']
        mask2 = results_list[1]['outliers_mask']

        intersection = mask1 & mask2
        union = mask1 | mask2

        intersection_count = intersection.sum()
        union_count = union.sum()

        print(f"Пересечение {results_list[0]['method']} и {results_list[1]['method']}: {intersection_count}")
        print(f"Объединение: {union_count}")

        if intersection_count > 0:
            print("\n🎯 СОТРУДНИКИ, ВЫЯВЛЕННЫЕ НЕСКОЛЬКИМИ МЕТОДАМИ:")
            consensus_outliers = data[intersection][['first_name', 'last_name', 'department', 
                                                   'position', 'salary']]
            print(consensus_outliers.to_string(index=False))

def detailed_outlier_analysis(data, outliers_results):
    """
    Проводит детальный анализ найденных выбросов

    Args:
        data (DataFrame): Исходные данные
        outliers_results (dict): Результаты одного из методов
    """
    print("\n" + "="*60)
    print("🔍 ДЕТАЛЬНЫЙ АНАЛИЗ ВЫБРОСОВ")
    print("="*60)

    outliers = outliers_results['outliers']

    if len(outliers) == 0:
        print("Выбросы не найдены.")
        return

    print(f"\n📊 ХАРАКТЕРИСТИКИ {len(outliers)} ВЫБРОСОВ:")

    # Анализ по департаментам
    dept_outliers = outliers['department'].value_counts()
    print("\n🏢 РАСПРЕДЕЛЕНИЕ ПО ДЕПАРТАМЕНТАМ:")
    for dept, count in dept_outliers.items():
        dept_total = len(data[data['department'] == dept])
        percentage = count / dept_total * 100
        print(f"{dept:15s}: {count} из {dept_total} ({percentage:.1f}%)")

    # Анализ по должностям
    position_outliers = outliers['position'].value_counts()
    print("\n👔 РАСПРЕДЕЛЕНИЕ ПО ДОЛЖНОСТЯМ:")
    for position, count in position_outliers.items():
        position_total = len(data[data['position'] == position])
        percentage = count / position_total * 100 if position_total > 0 else 0
        print(f"{position:15s}: {count} из {position_total} ({percentage:.1f}%)")

    # Статистика зарплат выбросов
    print("\n💰 СТАТИСТИКА ЗАРПЛАТ ВЫБРОСОВ:")
    outlier_salaries = outliers['salary']
    print(f"Средняя зарплата выбросов: {outlier_salaries.mean():,.0f} руб.")
    print(f"Медианная зарплата выбросов: {outlier_salaries.median():,.0f} руб.")
    print(f"Диапазон: {outlier_salaries.min():,.0f} - {outlier_salaries.max():,.0f} руб.")

    # Рекомендации по каждому выбросу
    print("\n🎯 РЕКОМЕНДАЦИИ ПО ОБРАБОТКЕ:")

    # Очень высокие зарплаты (возможные ошибки)
    very_high = outliers[outliers['salary'] > outliers['salary'].quantile(0.9)]
    if len(very_high) > 0:
        print(f"\n❗ ТРЕБУЮТ ПРОВЕРКИ ({len(very_high)} сотрудников):")
        check_list = very_high[['first_name', 'last_name', 'department', 'position', 'salary']]
        print(check_list.to_string(index=False))
        print("   Возможные ошибки ввода данных или неправомерные выплаты")

    # Топ-менеджмент (законные выбросы)
    management = outliers[outliers['position'].isin(['Director', 'VP', 'CEO'])]
    if len(management) > 0:
        print(f"\n✅ ВОЗМОЖНО ОБОСНОВАНЫ ({len(management)} сотрудников):")
        mgmt_list = management[['first_name', 'last_name', 'department', 'position', 'salary']]
        print(mgmt_list.to_string(index=False))
        print("   Высокие зарплаты руководящих должностей")

def create_outlier_visualizations(data, results_list):
    """
    Создает визуализации для анализа выбросов

    Args:
        data (DataFrame): Исходные данные
        results_list (list): Результаты разных методов
    """
    print("\n📊 Создание визуализаций выбросов...")

    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Анализ выбросов в зарплатных данных', fontsize=16, fontweight='bold')

    # 1. Box plot с выбросами
    data.boxplot(column='salary', ax=axes[0, 0])
    axes[0, 0].set_title('Box Plot - Выявление выбросов')
    axes[0, 0].set_ylabel('Зарплата (руб.)')

    # 2. Гистограмма с выделенными выбросами
    axes[0, 1].hist(data['salary'], bins=50, alpha=0.7, color='lightblue', label='Все данные')
    if len(results_list) > 0 and len(results_list[0]['outliers']) > 0:
        outlier_salaries = results_list[0]['outliers']['salary']
        axes[0, 1].hist(outlier_salaries, bins=20, alpha=0.8, color='red', label='Выбросы')
    axes[0, 1].set_title('Распределение зарплат с выделенными выбросами')
    axes[0, 1].set_xlabel('Зарплата (руб.)')
    axes[0, 1].set_ylabel('Количество')
    axes[0, 1].legend()

    # 3. Scatter plot: зарплата vs стаж с выделенными выбросами
    axes[1, 0].scatter(data['years_experience'], data['salary'], alpha=0.6, color='blue', s=30, label='Нормальные')
    if len(results_list) > 0 and len(results_list[0]['outliers']) > 0:
        outliers = results_list[0]['outliers']
        axes[1, 0].scatter(outliers['years_experience'], outliers['salary'], 
                          color='red', s=60, alpha=0.8, label='Выбросы')
    axes[1, 0].set_title('Зарплата vs Стаж (с выбросами)')
    axes[1, 0].set_xlabel('Стаж (лет)')
    axes[1, 0].set_ylabel('Зарплата (руб.)')
    axes[1, 0].legend()

    # 4. Сравнение методов
    if len(results_list) > 1:
        method_counts = [len(result['outliers']) for result in results_list]
        method_names = [result['method'] for result in results_list]

        bars = axes[1, 1].bar(method_names, method_counts, color=['skyblue', 'lightcoral', 'lightgreen', 'gold'][:len(method_names)])
        axes[1, 1].set_title('Количество выбросов по методам')
        axes[1, 1].set_ylabel('Количество выбросов')
        axes[1, 1].tick_params(axis='x', rotation=45)

        # Добавляем значения на столбцы
        for bar, count in zip(bars, method_counts):
            axes[1, 1].text(bar.get_x() + bar.get_width()/2., bar.get_height() + 1,
                           str(count), ha='center', va='bottom')

    plt.tight_layout()
    plt.savefig('outlier_analysis_dashboard.png', dpi=300, bbox_inches='tight')
    plt.show()

    print("✅ Визуализации сохранены как 'outlier_analysis_dashboard.png'")

def main():
    """
    Главная функция для запуска всех методов поиска выбросов
    """
    print("🚀 ЗАПУСК КОМПЛЕКСНОГО АНАЛИЗА ВЫБРОСОВ")
    print("=" * 70)

    # Загружаем данные
    df = load_data('hr_salary_data.csv')
    if df is None:
        return

    # Список для хранения результатов всех методов
    all_results = []

    # 1. Метод межквартильного размаха
    iqr_results = iqr_method(df)
    all_results.append(iqr_results)

    # 2. Z-score метод
    zscore_results = zscore_method(df)
    all_results.append(zscore_results)

    # 3. Модифицированный Z-score метод
    mod_zscore_results = modified_zscore_method(df)
    all_results.append(mod_zscore_results)

    # 4. Isolation Forest метод
    try:
        iso_results = isolation_forest_method(df)
        all_results.append(iso_results)
    except Exception as e:
        print(f"⚠️ Isolation Forest недоступен: {e}")

    # 5. Сравнение методов
    compare_methods(df, all_results)

    # 6. Детальный анализ выбросов (используем IQR метод)
    detailed_outlier_analysis(df, iqr_results)

    # 7. Создание визуализаций
    create_outlier_visualizations(df, all_results)

    print("\n" + "="*70)
    print("✅ АНАЛИЗ ВЫБРОСОВ ЗАВЕРШЕН!")
    print("📊 Создан файл: outlier_analysis_dashboard.png")
    print("🎯 Все методы выявления аномалий применены")
    print("💡 Рекомендации по обработке выбросов сформированы")

if __name__ == "__main__":
    main()
