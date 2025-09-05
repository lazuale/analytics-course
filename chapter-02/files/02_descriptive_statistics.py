#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Глава 2: Описательная статистика
Скрипт: Полный статистический анализ зарплатной политики компании

Этот скрипт демонстрирует все ключевые методы описательной статистики:
- Меры центральной тенденции
- Меры разброса и вариации
- Сравнительный анализ групп
- Корреляционный анализ
- Выявление выбросов

Автор: Analytics Course
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Настройка отображения
plt.rcParams['figure.figsize'] = (12, 8)
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
        print("✅ HR данные успешно загружены!")
        print(f"📊 Загружено {len(df)} записей сотрудников")
        return df
    except Exception as e:
        print(f"❌ Ошибка при загрузке данных: {e}")
        return None

def basic_descriptive_stats(df):
    """
    Рассчитывает базовые описательные статистики для зарплат

    Args:
        df (pandas.DataFrame): Данные сотрудников
    """
    print("\n" + "="*60)
    print("📊 ОПИСАТЕЛЬНАЯ СТАТИСТИКА ЗАРПЛАТ")
    print("="*60)

    salary_data = df['salary']

    # Меры центральной тенденции
    mean_salary = salary_data.mean()
    median_salary = salary_data.median()
    mode_salary = salary_data.mode().iloc[0] if not salary_data.mode().empty else "Нет моды"

    print("\n🎯 МЕРЫ ЦЕНТРАЛЬНОЙ ТЕНДЕНЦИИ:")
    print(f"Среднее арифметическое: {mean_salary:,.0f} руб.")
    print(f"Медиана: {median_salary:,.0f} руб.")
    print(f"Мода: {mode_salary:,.0f} руб." if mode_salary != "Нет моды" else f"Мода: {mode_salary}")

    # Интерпретация различий
    diff_mean_median = mean_salary - median_salary
    if diff_mean_median > mean_salary * 0.1:
        print("📈 Среднее значительно больше медианы → распределение смещено вправо (есть высокие выбросы)")
    elif diff_mean_median < -mean_salary * 0.1:
        print("📉 Среднее значительно меньше медианы → распределение смещено влево")
    else:
        print("⚖️ Среднее ≈ медиана → распределение близко к симметричному")

    # Меры разброса
    print("\n📏 МЕРЫ РАЗБРОСА:")
    std_dev = salary_data.std()
    variance = salary_data.var()
    range_val = salary_data.max() - salary_data.min()
    iqr = salary_data.quantile(0.75) - salary_data.quantile(0.25)
    coef_variation = std_dev / mean_salary

    print(f"Стандартное отклонение: {std_dev:,.0f} руб.")
    print(f"Дисперсия: {variance:,.0f}")
    print(f"Размах (min-max): {range_val:,.0f} руб.")
    print(f"Межквартильный размах (IQR): {iqr:,.0f} руб.")
    print(f"Коэффициент вариации: {coef_variation:.2%}")

    # Интерпретация вариации
    if coef_variation < 0.15:
        print("✅ Низкая вариация - зарплаты довольно однородны")
    elif coef_variation < 0.35:
        print("⚠️ Умеренная вариация - есть различия, но они приемлемы")
    else:
        print("❗ Высокая вариация - зарплаты очень неоднородны")

    # Квартили и процентили
    print("\n📊 КВАРТИЛИ И ПРОЦЕНТИЛИ:")
    quartiles = salary_data.quantile([0.25, 0.5, 0.75, 0.9, 0.95, 0.99])
    print(f"25-й процентиль (Q1): {quartiles[0.25]:,.0f} руб.")
    print(f"50-й процентиль (Q2, медиана): {quartiles[0.5]:,.0f} руб.")
    print(f"75-й процентиль (Q3): {quartiles[0.75]:,.0f} руб.")
    print(f"90-й процентиль: {quartiles[0.9]:,.0f} руб.")
    print(f"95-й процентиль: {quartiles[0.95]:,.0f} руб.")
    print(f"99-й процентиль: {quartiles[0.99]:,.0f} руб.")

    return {
        'mean': mean_salary,
        'median': median_salary,
        'std': std_dev,
        'q1': quartiles[0.25],
        'q3': quartiles[0.75]
    }

def departmental_analysis(df):
    """
    Проводит сравнительный анализ зарплат по департаментам

    Args:
        df (pandas.DataFrame): Данные сотрудников
    """
    print("\n" + "="*60)
    print("🏢 СРАВНИТЕЛЬНЫЙ АНАЛИЗ ПО ДЕПАРТАМЕНТАМ")
    print("="*60)

    # Статистика по департаментам
    dept_stats = df.groupby('department')['salary'].agg([
        'count', 'mean', 'median', 'std', 'min', 'max'
    ]).round(0)

    dept_stats.columns = ['Количество', 'Среднее', 'Медиана', 'Стд_откл', 'Минимум', 'Максимум']
    dept_stats = dept_stats.sort_values('Среднее', ascending=False)

    print("\n📊 Сводная таблица по департаментам:")
    print(dept_stats.to_string())

    # Коэффициенты вариации по департаментам
    dept_cv = df.groupby('department')['salary'].agg(['mean', 'std'])
    dept_cv['cv'] = dept_cv['std'] / dept_cv['mean']
    dept_cv = dept_cv.sort_values('cv')

    print("\n📈 Коэффициенты вариации по департаментам (от самого стабильного):")
    for dept, data in dept_cv.iterrows():
        print(f"{dept:15s}: {data['cv']:.2%}")

    # Анализ различий
    highest_dept = dept_stats.index[0]
    lowest_dept = dept_stats.index[-1]
    salary_gap = dept_stats.loc[highest_dept, 'Среднее'] / dept_stats.loc[lowest_dept, 'Среднее']

    print(f"\n💰 КЛЮЧЕВЫЕ ВЫВОДЫ:")
    print(f"📈 Самый высокооплачиваемый департамент: {highest_dept}")
    print(f"📉 Самый низкооплачиваемый департамент: {lowest_dept}")
    print(f"⚖️ Разрыв в оплате: {salary_gap:.1f}x")

    if salary_gap > 2:
        print("❗ Значительные различия в оплате между департаментами")
    elif salary_gap > 1.5:
        print("⚠️ Умеренные различия в оплате")
    else:
        print("✅ Относительно справедливое распределение зарплат")

    return dept_stats

def position_analysis(df):
    """
    Анализирует зарплаты по должностям

    Args:
        df (pandas.DataFrame): Данные сотрудников
    """
    print("\n" + "="*60)
    print("👔 АНАЛИЗ ЗАРПЛАТ ПО ДОЛЖНОСТЯМ")
    print("="*60)

    position_stats = df.groupby('position')['salary'].agg([
        'count', 'mean', 'median', 'std'
    ]).round(0)

    position_stats.columns = ['Количество', 'Среднее', 'Медиана', 'Стд_откл']
    position_stats = position_stats.sort_values('Среднее', ascending=False)

    print("\n📊 Статистика по должностям:")
    print(position_stats.to_string())

    return position_stats

def correlation_analysis(df):
    """
    Проводит корреляционный анализ факторов зарплаты

    Args:
        df (pandas.DataFrame): Данные сотрудников
    """
    print("\n" + "="*60)
    print("🔗 КОРРЕЛЯЦИОННЫЙ АНАЛИЗ ФАКТОРОВ ЗАРПЛАТЫ")
    print("="*60)

    # Подготавливаем данные для корреляционного анализа
    correlation_data = df[['salary', 'years_experience', 'age', 'performance_rating']].copy()

    # Добавляем закодированные категориальные переменные
    education_encoding = {'Bachelor': 1, 'Master': 2, 'PhD': 3}
    correlation_data['education_encoded'] = df['education_level'].map(education_encoding)

    # Рассчитываем корреляционную матрицу
    corr_matrix = correlation_data.corr()

    print("\n📊 Корреляция с зарплатой:")
    salary_correlations = corr_matrix['salary'].drop('salary').sort_values(ascending=False)

    for factor, correlation in salary_correlations.items():
        strength = ""
        if abs(correlation) > 0.7:
            strength = "💪 Сильная"
        elif abs(correlation) > 0.3:
            strength = "➡️ Умеренная"
        else:
            strength = "📉 Слабая"

        direction = "положительная" if correlation > 0 else "отрицательная"
        print(f"{factor:20s}: {correlation:6.3f} ({strength} {direction})")

    print("\n💡 ИНТЕРПРЕТАЦИЯ КОРРЕЛЯЦИЙ:")

    # Анализ каждого фактора
    exp_corr = salary_correlations['years_experience']
    if exp_corr > 0.5:
        print(f"✅ Стаж работы сильно влияет на зарплату (r={exp_corr:.3f})")
    elif exp_corr > 0.3:
        print(f"➡️ Стаж работы умеренно влияет на зарплату (r={exp_corr:.3f})")
    else:
        print(f"❓ Слабая связь стажа и зарплаты - возможны проблемы в системе оплаты")

    perf_corr = salary_correlations['performance_rating']
    if perf_corr > 0.3:
        print(f"✅ Производительность влияет на зарплату (r={perf_corr:.3f})")
    else:
        print(f"❓ Слабая связь производительности и зарплаты")

    edu_corr = salary_correlations['education_encoded']
    if edu_corr > 0.3:
        print(f"🎓 Образование влияет на зарплату (r={edu_corr:.3f})")
    else:
        print(f"📚 Слабое влияние образования на зарплату")

    return correlation_data, corr_matrix

def create_visualizations(df, basic_stats):
    """
    Создает статистические визуализации

    Args:
        df (pandas.DataFrame): Данные сотрудников
        basic_stats (dict): Базовые статистики
    """
    print("\n" + "="*60)
    print("📈 СОЗДАНИЕ СТАТИСТИЧЕСКИХ ВИЗУАЛИЗАЦИЙ")
    print("="*60)

    # Создаем фигуру с подграфиками
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.suptitle('Статистический анализ зарплат сотрудников', fontsize=16, fontweight='bold')

    # 1. Гистограмма распределения зарплат
    axes[0, 0].hist(df['salary'], bins=50, alpha=0.7, color='skyblue', edgecolor='black')
    axes[0, 0].axvline(basic_stats['mean'], color='red', linestyle='--', linewidth=2, label=f'Среднее: {basic_stats["mean"]:,.0f}')
    axes[0, 0].axvline(basic_stats['median'], color='green', linestyle='--', linewidth=2, label=f'Медиана: {basic_stats["median"]:,.0f}')
    axes[0, 0].set_title('Распределение зарплат')
    axes[0, 0].set_xlabel('Зарплата (руб.)')
    axes[0, 0].set_ylabel('Количество сотрудников')
    axes[0, 0].legend()

    # 2. Box plot по департаментам
    df.boxplot(column='salary', by='department', ax=axes[0, 1], rot=45)
    axes[0, 1].set_title('Распределение зарплат по департаментам')
    axes[0, 1].set_xlabel('Департамент')
    axes[0, 1].set_ylabel('Зарплата (руб.)')

    # 3. Зарплаты по должностям
    position_means = df.groupby('position')['salary'].mean().sort_values(ascending=True)
    position_means.plot(kind='barh', ax=axes[0, 2], color='lightgreen')
    axes[0, 2].set_title('Средние зарплаты по должностям')
    axes[0, 2].set_xlabel('Средняя зарплата (руб.)')

    # 4. Корреляция стажа и зарплаты
    axes[1, 0].scatter(df['years_experience'], df['salary'], alpha=0.6, color='orange')
    axes[1, 0].set_title('Зарплата vs Стаж работы')
    axes[1, 0].set_xlabel('Стаж (лет)')
    axes[1, 0].set_ylabel('Зарплата (руб.)')

    # Добавляем линию тренда
    z = np.polyfit(df['years_experience'], df['salary'], 1)
    p = np.poly1d(z)
    axes[1, 0].plot(df['years_experience'], p(df['years_experience']), "r--", alpha=0.8)

    # 5. Зарплата vs Возраст
    axes[1, 1].scatter(df['age'], df['salary'], alpha=0.6, color='purple')
    axes[1, 1].set_title('Зарплата vs Возраст')
    axes[1, 1].set_xlabel('Возраст (лет)')
    axes[1, 1].set_ylabel('Зарплата (руб.)')

    # 6. Зарплаты по рейтингу производительности
    performance_means = df.groupby('performance_rating')['salary'].mean()
    performance_means.plot(kind='bar', ax=axes[1, 2], color='coral')
    axes[1, 2].set_title('Зарплата vs Рейтинг производительности')
    axes[1, 2].set_xlabel('Рейтинг производительности')
    axes[1, 2].set_ylabel('Средняя зарплата (руб.)')
    axes[1, 2].set_xticklabels([f'Рейтинг {x}' for x in performance_means.index], rotation=0)

    plt.tight_layout()
    plt.savefig('statistical_analysis_dashboard.png', dpi=300, bbox_inches='tight')
    plt.show()

    print("✅ Дашборд сохранен как 'statistical_analysis_dashboard.png'")

def generate_insights_report(df, dept_stats, basic_stats):
    """
    Генерирует итоговый отчет с инсайтами

    Args:
        df (pandas.DataFrame): Данные сотрудников  
        dept_stats (DataFrame): Статистика по департаментам
        basic_stats (dict): Базовые статистики
    """
    print("\n" + "="*60)
    print("💡 КЛЮЧЕВЫЕ ИНСАЙТЫ И РЕКОМЕНДАЦИИ")
    print("="*60)

    print("\n🎯 ОСНОВНЫЕ ВЫВОДЫ:")

    # 1. Общая картина зарплат
    mean_salary = basic_stats['mean']
    median_salary = basic_stats['median']

    if mean_salary > median_salary * 1.2:
        print("1. 📊 РАСПРЕДЕЛЕНИЕ ЗАРПЛАТ: Сильно смещено вправо")
        print("   💡 Есть группа высокооплачиваемых сотрудников, поднимающих среднее")
        print("   🎯 Рекомендация: Проанализировать обоснованность высоких зарплат")

    # 2. Анализ департаментов
    highest_dept = dept_stats.index[0]
    lowest_dept = dept_stats.index[-1]
    gap_ratio = dept_stats.loc[highest_dept, 'Среднее'] / dept_stats.loc[lowest_dept, 'Среднее']

    print(f"\n2. 🏢 ДЕПАРТАМЕНТЫ:")
    print(f"   📈 Лидер по зарплатам: {highest_dept} ({dept_stats.loc[highest_dept, 'Среднее']:,.0f} руб.)")
    print(f"   📉 Аутсайдер: {lowest_dept} ({dept_stats.loc[lowest_dept, 'Среднее']:,.0f} руб.)")
    print(f"   ⚖️ Разрыв: {gap_ratio:.1f} раза")

    if gap_ratio > 2.5:
        print("   ❗ ПРОБЛЕМА: Слишком большой разрыв между департаментами")
        print("   🎯 Рекомендация: Пересмотреть зарплатную политику")

    # 3. Корреляционный анализ
    corr_exp = df['salary'].corr(df['years_experience'])
    if corr_exp > 0.6:
        print(f"\n3. 📊 СТАЖ И ЗАРПЛАТА: Сильная связь (r={corr_exp:.3f})")
        print("   ✅ Система мотивации работает правильно")
    elif corr_exp > 0.3:
        print(f"\n3. 📊 СТАЖ И ЗАРПЛАТА: Умеренная связь (r={corr_exp:.3f})")
        print("   ⚠️ Можно улучшить связь стажа и зарплаты")
    else:
        print(f"\n3. 📊 СТАЖ И ЗАРПЛАТА: Слабая связь (r={corr_exp:.3f})")
        print("   ❗ ПРОБЛЕМА: Стаж слабо влияет на зарплату")

    # 4. Выбросы
    q1 = basic_stats['q1']
    q3 = basic_stats['q3']
    iqr = q3 - q1
    upper_bound = q3 + 1.5 * iqr
    outliers = df[df['salary'] > upper_bound]

    print(f"\n4. 🔍 ВЫБРОСЫ:")
    print(f"   📊 Найдено потенциальных выбросов: {len(outliers)}")
    if len(outliers) > 0:
        print("   🎯 Требуется детальный анализ аномально высоких зарплат")

    # 5. Рекомендации
    print(f"\n🎯 РЕКОМЕНДАЦИИ ДЛЯ HR-ДЕПАРТАМЕНТА:")
    print("1. 📋 Провести аудит высоких зарплат на предмет обоснованности")
    print("2. ⚖️ Сгладить различия в оплате между департаментами")  
    print("3. 📈 Усилить связь между стажем/производительностью и зарплатой")
    print("4. 📊 Внедрить регулярный статистический мониторинг зарплат")
    print("5. 🎯 Создать прозрачные критерии оплаты труда")

def main():
    """
    Главная функция, выполняющая полный статистический анализ
    """
    print("🚀 ЗАПУСК ПОЛНОГО СТАТИСТИЧЕСКОГО АНАЛИЗА HR ДАННЫХ")
    print("=" * 80)

    # Загружаем данные
    df = load_data('hr_salary_data.csv')
    if df is None:
        return

    # 1. Базовые описательные статистики
    basic_stats = basic_descriptive_stats(df)

    # 2. Анализ по департаментам
    dept_stats = departmental_analysis(df)

    # 3. Анализ по должностям
    position_stats = position_analysis(df)

    # 4. Корреляционный анализ
    corr_data, corr_matrix = correlation_analysis(df)

    # 5. Создание визуализаций
    create_visualizations(df, basic_stats)

    # 6. Генерация итогового отчета
    generate_insights_report(df, dept_stats, basic_stats)

    print("\n✅ АНАЛИЗ ЗАВЕРШЕН!")
    print("📊 Создан файл: statistical_analysis_dashboard.png")
    print("🎯 Все ключевые статистические показатели рассчитаны")

if __name__ == "__main__":
    main()
