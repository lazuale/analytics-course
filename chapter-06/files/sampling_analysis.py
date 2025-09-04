"""
Модуль для выборочного анализа и построения доверительных интервалов

Модуль содержит функции для:
- Создания различных типов выборок
- Анализа репрезентативности выборок
- Расчета размера выборки
- Построения доверительных интервалов
- Проведения симуляций выборочных распределений
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.stats import t, norm
import warnings
import os
from typing import Union, Tuple, List, Dict, Optional

warnings.filterwarnings('ignore')

# Настройка matplotlib для корректного отображения русского текста
plt.rcParams['font.size'] = 12
plt.rcParams['figure.figsize'] = (10, 6)

def load_population(filename: str = 'customer_population.csv') -> Optional[pd.DataFrame]:
    """
    Загружает генеральную совокупность из CSV файла
    
    Parameters:
    -----------
    filename : str
        Имя файла с данными (по умолчанию 'customer_population.csv')
    
    Returns:
    --------
    pd.DataFrame or None
        DataFrame с данными генеральной совокупности или None при ошибке
    """
    try:
        # Пробуем разные пути к файлу
        possible_paths = [
            filename,
            f'files/{filename}',
            f'./{filename}',
            f'../files/{filename}'
        ]
        
        df = None
        for path in possible_paths:
            if os.path.exists(path):
                df = pd.read_csv(path, sep=';', encoding='utf-8')
                print(f"✅ Файл загружен из {path}")
                break
        
        if df is None:
            print(f"❌ Файл {filename} не найден ни по одному из путей:")
            for path in possible_paths:
                print(f"   - {path}")
            return None
            
        # Проверяем корректность загрузки
        expected_columns = ['customer_id', 'age', 'annual_spend', 'satisfaction', 'city', 'is_premium', 'gender']
        missing_columns = set(expected_columns) - set(df.columns)
        
        if missing_columns:
            print(f"⚠️ Предупреждение: отсутствуют столбцы {missing_columns}")
        
        print(f"📊 Загружена генеральная совокупность: {len(df)} записей")
        print(f"📋 Столбцы: {list(df.columns)}")
        
        return df
        
    except Exception as e:
        print(f"❌ Ошибка при загрузке файла {filename}: {str(e)}")
        return None

def create_random_sample(population: pd.DataFrame, size: int, seed: int = 42) -> pd.DataFrame:
    """
    Создает простую случайную выборку
    
    Parameters:
    -----------
    population : pd.DataFrame
        Генеральная совокупность
    size : int
        Размер выборки
    seed : int
        Семя для воспроизводимости результатов
        
    Returns:
    --------
    pd.DataFrame
        Случайная выборка
    """
    if size > len(population):
        print(f"⚠️ Предупреждение: размер выборки ({size}) больше размера популяции ({len(population)})")
        print(f"Размер выборки установлен равным размеру популяции")
        size = len(population)
    
    np.random.seed(seed)
    sample = population.sample(n=size, random_state=seed).reset_index(drop=True)
    
    print(f"🎲 Создана случайная выборка размером {len(sample)} из {len(population)} записей")
    return sample

def create_stratified_sample(population: pd.DataFrame, strata_column: str, size: int, 
                           proportional: bool = True, seed: int = 42) -> pd.DataFrame:
    """
    Создает стратифицированную выборку
    
    Parameters:
    -----------
    population : pd.DataFrame
        Генеральная совокупность
    strata_column : str
        Колонка для стратификации (например, 'city')
    size : int
        Общий размер выборки
    proportional : bool
        Если True, то пропорциональная стратификация
        Если False, то равные размеры страт
    seed : int
        Семя для воспроизводимости
        
    Returns:
    --------
    pd.DataFrame
        Стратифицированная выборка
    """
    np.random.seed(seed)
    
    # Получаем информацию о стратах
    strata_info = population[strata_column].value_counts()
    print(f"📊 Распределение по стратам ({strata_column}):")
    for stratum, count in strata_info.items():
        percentage = (count / len(population)) * 100
        print(f"   {stratum}: {count} ({percentage:.1f}%)")
    
    stratified_sample = pd.DataFrame()
    
    if proportional:
        # Пропорциональная стратификация
        proportions = population[strata_column].value_counts(normalize=True)
        
        for stratum, proportion in proportions.items():
            stratum_data = population[population[strata_column] == stratum]
            stratum_size = int(size * proportion)
            
            # Корректировка для последней страты (чтобы сумма была равна size)
            if stratum == proportions.index[-1]:
                current_total = len(stratified_sample)
                stratum_size = size - current_total
            
            if stratum_size > 0 and len(stratum_data) > 0:
                actual_size = min(stratum_size, len(stratum_data))
                stratum_sample = stratum_data.sample(n=actual_size, random_state=seed+hash(stratum)%1000)
                stratified_sample = pd.concat([stratified_sample, stratum_sample])
                print(f"   {stratum}: отобрано {actual_size} из {len(stratum_data)}")
    else:
        # Равные размеры страт
        size_per_stratum = size // len(strata_info)
        remainder = size % len(strata_info)
        
        for i, (stratum, count) in enumerate(strata_info.items()):
            stratum_data = population[population[strata_column] == stratum]
            stratum_size = size_per_stratum + (1 if i < remainder else 0)
            
            if len(stratum_data) > 0:
                actual_size = min(stratum_size, len(stratum_data))
                stratum_sample = stratum_data.sample(n=actual_size, random_state=seed+i)
                stratified_sample = pd.concat([stratified_sample, stratum_sample])
                print(f"   {stratum}: отобрано {actual_size} из {len(stratum_data)}")
    
    stratified_sample = stratified_sample.reset_index(drop=True)
    print(f"🏗 Создана стратифицированная выборка размером {len(stratified_sample)}")
    
    return stratified_sample

def create_systematic_sample(population: pd.DataFrame, size: int, seed: int = 42) -> pd.DataFrame:
    """
    Создает систематическую выборку
    
    Parameters:
    -----------
    population : pd.DataFrame
        Генеральная совокупность
    size : int
        Размер выборки
    seed : int
        Семя для выбора случайного старта
        
    Returns:
    --------
    pd.DataFrame
        Систематическая выборка
    """
    N = len(population)
    
    if size >= N:
        print(f"⚠️ Размер выборки больше или равен размеру популяции")
        return population.copy()
    
    # Интервал выборки
    k = N // size
    
    # Случайный старт
    np.random.seed(seed)
    start = np.random.randint(0, k)
    
    # Индексы для выборки
    indices = [start + i * k for i in range(size) if start + i * k < N]
    
    # Если не хватает элементов, добавляем из начала
    while len(indices) < size and len(indices) < N:
        additional_indices = [i for i in range(N) if i not in indices]
        indices.extend(additional_indices[:size - len(indices)])
    
    systematic_sample = population.iloc[indices].reset_index(drop=True)
    
    print(f"📊 Создана систематическая выборка:")
    print(f"   Размер популяции: {N}")
    print(f"   Интервал выборки (k): {k}")
    print(f"   Случайный старт: {start}")
    print(f"   Размер выборки: {len(systematic_sample)}")
    
    return systematic_sample

def calculate_sample_statistics(sample: pd.DataFrame, 
                               variables: Optional[List[str]] = None) -> Dict[str, Dict[str, float]]:
    """
    Рассчитывает основные статистики выборки
    
    Parameters:
    -----------
    sample : pd.DataFrame
        Выборка данных
    variables : list, optional
        Список переменных для анализа (если None, то все числовые)
        
    Returns:
    --------
    dict
        Словарь со статистиками для каждой переменной
    """
    if variables is None:
        # Автоматически определяем числовые колонки
        numeric_cols = sample.select_dtypes(include=[np.number]).columns.tolist()
    else:
        numeric_cols = [col for col in variables if col in sample.columns and 
                       sample[col].dtype in ['int64', 'float64']]
    
    stats_dict = {}
    
    for col in numeric_cols:
        if sample[col].notna().sum() > 0:  # Проверяем что есть не-NaN значения
            stats_dict[col] = {
                'count': int(sample[col].count()),
                'mean': float(sample[col].mean()),
                'std': float(sample[col].std()),
                'min': float(sample[col].min()),
                'max': float(sample[col].max()),
                'median': float(sample[col].median()),
                'q25': float(sample[col].quantile(0.25)),
                'q75': float(sample[col].quantile(0.75))
            }
    
    # Для категориальных переменных
    categorical_cols = sample.select_dtypes(include=['object', 'category']).columns.tolist()
    
    for col in categorical_cols:
        if col not in stats_dict:
            value_counts = sample[col].value_counts()
            proportions = sample[col].value_counts(normalize=True)
            
            stats_dict[col] = {
                'count': int(sample[col].count()),
                'unique_values': int(sample[col].nunique()),
                'most_frequent': str(value_counts.index[0]) if len(value_counts) > 0 else None,
                'most_frequent_count': int(value_counts.iloc[0]) if len(value_counts) > 0 else 0,
                'most_frequent_prop': float(proportions.iloc[0]) if len(proportions) > 0 else 0.0
            }
    
    return stats_dict

def confidence_interval_mean(data: Union[pd.Series, np.ndarray, List], 
                           confidence: float = 0.95) -> Tuple[float, Tuple[float, float]]:
    """
    Рассчитывает доверительный интервал для среднего
    
    Parameters:
    -----------
    data : array-like
        Данные для анализа
    confidence : float
        Уровень доверия (по умолчанию 0.95)
        
    Returns:
    --------
    tuple
        (среднее, (нижняя_граница, верхняя_граница))
    """
    data = np.array(data)
    data = data[~np.isnan(data)]  # Удаляем NaN значения
    
    if len(data) == 0:
        raise ValueError("Нет валидных данных для анализа")
    
    n = len(data)
    mean = np.mean(data)
    std_err = stats.sem(data)  # Стандартная ошибка среднего
    
    # Используем t-распределение для малых выборок или когда σ неизвестно
    alpha = 1 - confidence
    t_critical = stats.t.ppf(1 - alpha/2, df=n-1)
    
    # Границы интервала
    margin_error = t_critical * std_err
    ci_lower = mean - margin_error
    ci_upper = mean + margin_error
    
    return mean, (ci_lower, ci_upper)

def confidence_interval_proportion(successes: int, n: int, 
                                 confidence: float = 0.95) -> Tuple[float, Tuple[float, float]]:
    """
    Рассчитывает доверительный интервал для доли
    
    Parameters:
    -----------
    successes : int
        Количество успехов
    n : int
        Размер выборки
    confidence : float
        Уровень доверия
        
    Returns:
    --------
    tuple
        (доля, (нижняя_граница, верхняя_граница))
    """
    if n <= 0:
        raise ValueError("Размер выборки должен быть положительным")
    
    if successes < 0 or successes > n:
        raise ValueError("Количество успехов должно быть от 0 до n")
    
    p = successes / n
    alpha = 1 - confidence
    z_critical = stats.norm.ppf(1 - alpha/2)
    
    # Стандартная ошибка доли
    std_err = np.sqrt(p * (1 - p) / n)
    
    # Границы интервала
    margin_error = z_critical * std_err
    ci_lower = max(0, p - margin_error)
    ci_upper = min(1, p + margin_error)
    
    return p, (ci_lower, ci_upper)

def sample_size_for_mean(z: float, sigma: float, error: float) -> int:
    """
    Рассчитывает необходимый размер выборки для среднего
    
    Parameters:
    -----------
    z : float
        z-критическое значение (например, 1.96 для 95%)
    sigma : float
        Стандартное отклонение популяции (или его оценка)
    error : float
        Допустимая ошибка
        
    Returns:
    --------
    int
        Необходимый размер выборки
    """
    if z <= 0 or sigma <= 0 or error <= 0:
        raise ValueError("Все параметры должны быть положительными")
    
    n = ((z * sigma) / error) ** 2
    return int(np.ceil(n))

def sample_size_for_proportion(z: float, p: float, error: float) -> int:
    """
    Рассчитывает необходимый размер выборки для доли
    
    Parameters:
    -----------
    z : float
        z-критическое значение
    p : float
        Ожидаемая доля (если неизвестна, используйте 0.5)
    error : float
        Допустимая ошибка
        
    Returns:
    --------
    int
        Необходимый размер выборки
    """
    if z <= 0 or error <= 0:
        raise ValueError("z и error должны быть положительными")
    
    if p < 0 or p > 1:
        raise ValueError("Доля p должна быть от 0 до 1")
    
    n = (z ** 2 * p * (1 - p)) / (error ** 2)
    return int(np.ceil(n))

def compare_sampling_methods(population: pd.DataFrame, size: int = 500, 
                           strata_column: str = 'city') -> pd.DataFrame:
    """
    Сравнивает различные методы выборки
    
    Parameters:
    -----------
    population : pd.DataFrame
        Генеральная совокупность
    size : int
        Размер выборок для сравнения
    strata_column : str
        Колонка для стратификации
        
    Returns:
    --------
    pd.DataFrame
        Сравнительная таблица результатов
    """
    # Истинные параметры популяции
    numeric_vars = population.select_dtypes(include=[np.number]).columns
    true_params = {}
    
    for var in numeric_vars:
        if var != 'customer_id':  # Исключаем ID
            true_params[var] = {
                'mean': population[var].mean(),
                'std': population[var].std()
            }
    
    # Создаем выборки разными методами
    try:
        random_sample = create_random_sample(population, size, seed=42)
        stratified_sample = create_stratified_sample(population, strata_column, size, seed=42)
        systematic_sample = create_systematic_sample(population, size, seed=42)
        
        samples = {
            'Random': random_sample,
            'Stratified': stratified_sample, 
            'Systematic': systematic_sample
        }
        
        # Анализируем результаты
        results = []
        
        for method_name, sample in samples.items():
            for var in true_params.keys():
                if var in sample.columns:
                    sample_mean = sample[var].mean()
                    sample_std = sample[var].std()
                    true_mean = true_params[var]['mean']
                    
                    bias = sample_mean - true_mean
                    relative_bias = (bias / true_mean) * 100 if true_mean != 0 else 0
                    
                    results.append({
                        'Method': method_name,
                        'Variable': var,
                        'True_Mean': round(true_mean, 2),
                        'Sample_Mean': round(sample_mean, 2),
                        'Bias': round(bias, 2),
                        'Relative_Bias_%': round(relative_bias, 2),
                        'Sample_Std': round(sample_std, 2),
                        'Sample_Size': len(sample)
                    })
        
        comparison_df = pd.DataFrame(results)
        
        print("📊 Сравнение методов выборки:")
        print("="*60)
        
        # Группируем по переменным для удобства чтения
        for var in true_params.keys():
            if var in comparison_df['Variable'].values:
                print(f"\n📈 {var.upper()}:")
                var_data = comparison_df[comparison_df['Variable'] == var]
                for _, row in var_data.iterrows():
                    print(f"  {row['Method']:12} | Смещение: {row['Bias']:>6.1f} | "
                          f"Относительное: {row['Relative_Bias_%']:>5.1f}%")
        
        return comparison_df
        
    except Exception as e:
        print(f"❌ Ошибка при сравнении методов: {str(e)}")
        return pd.DataFrame()

def simulate_confidence_intervals(population: pd.DataFrame, column: str, 
                                n_simulations: int = 100, sample_size: int = 200, 
                                confidence: float = 0.95) -> Dict:
    """
    Симулирует множественные доверительные интервалы
    
    Parameters:
    -----------
    population : pd.DataFrame
        Генеральная совокупность
    column : str
        Колонка для анализа
    n_simulations : int
        Количество симуляций
    sample_size : int
        Размер каждой выборки
    confidence : float
        Уровень доверия
        
    Returns:
    --------
    dict
        Результаты симуляций
    """
    if column not in population.columns:
        raise ValueError(f"Колонка '{column}' не найдена в данных")
    
    true_mean = population[column].mean()
    results = []
    
    print(f"🔬 Запуск симуляции доверительных интервалов:")
    print(f"   Переменная: {column}")
    print(f"   Истинное среднее: {true_mean:.2f}")
    print(f"   Количество симуляций: {n_simulations}")
    print(f"   Размер выборки: {sample_size}")
    print(f"   Уровень доверия: {confidence:.0%}")
    
    for i in range(n_simulations):
        # Создаем случайную выборку
        sample = population[column].sample(n=sample_size, replace=False, random_state=i+42)
        
        # Строим доверительный интервал
        try:
            mean, (ci_lower, ci_upper) = confidence_interval_mean(sample, confidence)
            
            # Проверяем, содержит ли интервал истинное значение
            contains_true = ci_lower <= true_mean <= ci_upper
            
            results.append({
                'simulation': i+1,
                'sample_mean': mean,
                'ci_lower': ci_lower,
                'ci_upper': ci_upper,
                'ci_width': ci_upper - ci_lower,
                'contains_true': contains_true
            })
            
        except Exception as e:
            print(f"⚠️ Ошибка в симуляции {i+1}: {str(e)}")
            continue
    
    if not results:
        print("❌ Не удалось провести ни одной успешной симуляции")
        return {}
    
    results_df = pd.DataFrame(results)
    
    # Статистика покрытия
    coverage = results_df['contains_true'].mean()
    mean_width = results_df['ci_width'].mean()
    
    print(f"\n📊 Результаты симуляции:")
    print(f"   Покрытие доверительных интервалов: {coverage:.1%}")
    print(f"   Ожидаемое покрытие: {confidence:.1%}")
    print(f"   Средняя ширина ДИ: {mean_width:.2f}")
    print(f"   Успешных симуляций: {len(results_df)} из {n_simulations}")
    
    return {
        'results': results_df,
        'true_mean': true_mean,
        'coverage': coverage,
        'expected_coverage': confidence,
        'mean_width': mean_width
    }

def plot_confidence_intervals_simulation(simulation_results: Dict, max_intervals: int = 50):
    """
    Визуализирует результаты симуляции доверительных интервалов
    
    Parameters:
    -----------
    simulation_results : dict
        Результаты симуляции из функции simulate_confidence_intervals
    max_intervals : int
        Максимальное количество интервалов для отображения
    """
    if 'results' not in simulation_results:
        print("❌ Некорректные данные для визуализации")
        return
    
    results_df = simulation_results['results']
    true_mean = simulation_results['true_mean']
    
    # Ограничиваем количество интервалов для визуализации
    plot_data = results_df.head(max_intervals).copy()
    
    # Создаем график
    fig, ax = plt.subplots(figsize=(12, 8))
    
    for i, (_, row) in enumerate(plot_data.iterrows()):
        # Цвет зависит от того, содержит ли интервал истинное значение
        color = 'blue' if row['contains_true'] else 'red'
        alpha = 0.7 if row['contains_true'] else 1.0
        linewidth = 1 if row['contains_true'] else 2
        
        # Рисуем интервал
        ax.plot([row['ci_lower'], row['ci_upper']], [i, i], 
               color=color, alpha=alpha, linewidth=linewidth)
        
        # Рисуем среднее выборки
        ax.plot(row['sample_mean'], i, 'o', color=color, alpha=alpha, markersize=3)
    
    # Истинное среднее
    ax.axvline(true_mean, color='green', linestyle='--', linewidth=2,
              label=f'Истинное среднее: {true_mean:.2f}')
    
    # Подсчитываем статистику для легенды
    n_correct = plot_data['contains_true'].sum()
    n_total = len(plot_data)
    coverage_rate = n_correct / n_total
    
    ax.set_xlabel('Значение')
    ax.set_ylabel('Номер выборки')
    ax.set_title(f'Доверительные интервалы для {n_total} выборок\n'
                f'Покрытие: {n_correct}/{n_total} ({coverage_rate:.1%})')
    
    # Создаем легенду
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], color='green', linestyle='--', linewidth=2, label=f'Истинное среднее: {true_mean:.2f}'),
        Line2D([0], [0], color='blue', linewidth=1, label=f'Содержат истинное значение: {n_correct}'),
        Line2D([0], [0], color='red', linewidth=2, label=f'Не содержат истинное значение: {n_total - n_correct}')
    ]
    ax.legend(handles=legend_elements, loc='upper right')
    
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()
    
    print(f"📊 Показано {len(plot_data)} интервалов из {len(results_df)} общих")

def analyze_sample_representativeness(sample: pd.DataFrame, population: pd.DataFrame, 
                                    key_variables: List[str]) -> pd.DataFrame:
    """
    Анализирует репрезентативность выборки по ключевым переменным
    
    Parameters:
    -----------
    sample : pd.DataFrame
        Данные выборки
    population : pd.DataFrame
        Данные генеральной совокупности
    key_variables : list
        Список ключевых переменных для сравнения
        
    Returns:
    --------
    pd.DataFrame
        Таблица сравнения характеристик
    """
    results = []
    
    for var in key_variables:
        if var not in sample.columns or var not in population.columns:
            print(f"⚠️ Переменная '{var}' не найдена в данных")
            continue
        
        if sample[var].dtype in ['int64', 'float64']:
            # Для количественных переменных
            pop_mean = population[var].mean()
            sample_mean = sample[var].mean()
            bias = sample_mean - pop_mean
            relative_bias = (bias / pop_mean) * 100 if pop_mean != 0 else 0
            
            # Доверительный интервал для выборочного среднего
            try:
                _, (ci_lower, ci_upper) = confidence_interval_mean(sample[var])
                contains_true = ci_lower <= pop_mean <= ci_upper
            except:
                ci_lower = ci_upper = np.nan
                contains_true = False
            
            results.append({
                'Variable': var,
                'Type': 'Numeric',
                'Population_Value': round(pop_mean, 3),
                'Sample_Value': round(sample_mean, 3),
                'Bias': round(bias, 3),
                'Relative_Bias_%': round(relative_bias, 2),
                'CI_Lower': round(ci_lower, 3),
                'CI_Upper': round(ci_upper, 3),
                'Contains_True': contains_true
            })
            
        else:
            # Для категориальных переменных
            pop_dist = population[var].value_counts(normalize=True).sort_index()
            sample_dist = sample[var].value_counts(normalize=True).sort_index()
            
            for category in pop_dist.index:
                pop_prop = pop_dist.get(category, 0)
                sample_prop = sample_dist.get(category, 0)
                bias = sample_prop - pop_prop
                relative_bias = (bias / pop_prop) * 100 if pop_prop > 0 else 0
                
                # Доверительный интервал для доли
                try:
                    n_successes = int(sample_prop * len(sample))
                    _, (ci_lower, ci_upper) = confidence_interval_proportion(n_successes, len(sample))
                    contains_true = ci_lower <= pop_prop <= ci_upper
                except:
                    ci_lower = ci_upper = np.nan
                    contains_true = False
                
                results.append({
                    'Variable': f"{var}_{category}",
                    'Type': 'Categorical',
                    'Population_Value': round(pop_prop, 3),
                    'Sample_Value': round(sample_prop, 3),
                    'Bias': round(bias, 3),
                    'Relative_Bias_%': round(relative_bias, 2),
                    'CI_Lower': round(ci_lower, 3),
                    'CI_Upper': round(ci_upper, 3),
                    'Contains_True': contains_true
                })
    
    analysis_df = pd.DataFrame(results)
    
    if len(analysis_df) > 0:
        print("📊 Анализ репрезентативности выборки:")
        print("="*80)
        
        # Показываем только самые важные метрики
        for var_type in ['Numeric', 'Categorical']:
            type_data = analysis_df[analysis_df['Type'] == var_type]
            if len(type_data) > 0:
                print(f"\n📈 {var_type} переменные:")
                for _, row in type_data.iterrows():
                    status = "✅" if row['Contains_True'] else "❌"
                    print(f"  {status} {row['Variable']:20} | "
                          f"Смещение: {row['Relative_Bias_%']:>6.1f}% | "
                          f"ДИ покрывает: {row['Contains_True']}")
    
    return analysis_df

# Функции-помощники для работы с критическими значениями
def get_z_critical(confidence: float) -> float:
    """Возвращает z-критическое значение для заданного уровня доверия"""
    alpha = 1 - confidence
    return stats.norm.ppf(1 - alpha/2)

def get_t_critical(confidence: float, df: int) -> float:
    """Возвращает t-критическое значение для заданного уровня доверия и степеней свободы"""
    alpha = 1 - confidence
    return stats.t.ppf(1 - alpha/2, df)

# Пример использования модуля
if __name__ == "__main__":
    print("🚀 Модуль для выборочного анализа загружен!")
    print("\n📚 Доступные функции:")
    print("="*50)
    
    functions = [
        "load_population() - загрузка данных",
        "create_random_sample() - случайная выборка", 
        "create_stratified_sample() - стратифицированная выборка",
        "create_systematic_sample() - систематическая выборка",
        "calculate_sample_statistics() - статистики выборки",
        "confidence_interval_mean() - ДИ для среднего",
        "confidence_interval_proportion() - ДИ для доли",
        "sample_size_for_mean() - размер выборки для среднего",
        "sample_size_for_proportion() - размер выборки для доли",
        "compare_sampling_methods() - сравнение методов выборки",  
        "simulate_confidence_intervals() - симуляция ДИ",
        "analyze_sample_representativeness() - анализ репрезентативности"
    ]
    
    for func in functions:
        print(f"  📝 {func}")
    
    print(f"\n💡 Пример использования:")
    print("="*30)
    print("population = load_population()")
    print("sample = create_random_sample(population, 500)")
    print("mean, ci = confidence_interval_mean(sample['annual_spend'])")
    print("print(f'Среднее: {mean:.0f}, ДИ: [{ci[0]:.0f}; {ci[1]:.0f}]')")
    
    # Демонстрация работы с тестовыми данными
    try:
        population = load_population()
        if population is not None:
            print(f"\n✅ Тестовая загрузка данных успешна!")
            print(f"📊 Размер генеральной совокупности: {len(population)}")
            
            # Создаем небольшую выборку для демонстрации
            sample = create_random_sample(population, 100, seed=42)
            stats_dict = calculate_sample_statistics(sample)
            
            print(f"\n📈 Пример статистик выборки (n=100):")
            for var, stats in stats_dict.items():
                if isinstance(stats, dict) and 'mean' in stats:
                    print(f"  {var}: среднее = {stats['mean']:.1f}, σ = {stats['std']:.1f}")
                    
    except Exception as e:
        print(f"❌ Ошибка в демонстрации: {str(e)}")
        print("💡 Убедитесь что файл customer_population.csv находится в папке files/")