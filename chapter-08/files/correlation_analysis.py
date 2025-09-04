"""
Скрипт для корреляционного и регрессионного анализа

Этот скрипт содержит готовые функции для проведения корреляционного анализа,
построения регрессионных моделей и их валидации.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from scipy.stats import pearsonr
import warnings
warnings.filterwarnings('ignore')

# Настройка отображения
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['figure.figsize'] = (12, 8)
plt.style.use('default')

def load_business_data(filename: str) -> pd.DataFrame:
    """
    Загружает бизнес-данные с правильной обработкой русского формата
    
    Параметры:
    ----------
    filename : str
        Имя CSV файла
        
    Возвращает:
    ----------
    pd.DataFrame
        Загруженные и обработанные данные
    """
    try:
        # Загружаем с русскими настройками
        df = pd.read_csv(filename, sep=';', decimal='.', encoding='utf-8')
        
        print(f"✅ Данные загружены: {filename}")
        print(f"📊 Размер: {df.shape[0]} строк, {df.shape[1]} столбцов")
        print(f"📋 Столбцы: {list(df.columns)}")
        
        return df
        
    except FileNotFoundError:
        print(f"❌ Файл {filename} не найден")
        return pd.DataFrame()
    except Exception as e:
        print(f"❌ Ошибка загрузки: {e}")
        return pd.DataFrame()

def create_correlation_matrix(df: pd.DataFrame, figsize: tuple = (10, 8)) -> None:
    """
    Создает красивую тепловую карту корреляций
    
    Параметры:
    ----------
    df : pd.DataFrame
        DataFrame с числовыми данными
    figsize : tuple
        Размер графика
    """
    
    # Выбираем только числовые столбцы
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    if len(numeric_cols) < 2:
        print("❌ Недостаточно числовых столбцов для корреляционного анализа")
        return
    
    # Рассчитываем корреляции
    corr_matrix = df[numeric_cols].corr()
    
    # Создаем тепловую карту
    plt.figure(figsize=figsize)
    
    # Создаем маску для верхнего треугольника (убираем дублирование)
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
    
    # Рисуем тепловую карту
    sns.heatmap(
        corr_matrix, 
        mask=mask,
        annot=True, 
        cmap='RdYlBu_r',
        center=0,
        fmt='.2f',
        square=True,
        cbar_kws={'label': 'Коэффициент корреляции'}
    )
    
    plt.title('🔗 Карта корреляций между показателями', fontsize=16, pad=20)
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.show()
    
    # Выводим топ корреляций
    print("\n🏆 ТОП-5 САМЫХ СИЛЬНЫХ СВЯЗЕЙ:")
    print("=" * 50)
    
    # Получаем все пары корреляций
    correlations = []
    for i in range(len(corr_matrix.columns)):
        for j in range(i+1, len(corr_matrix.columns)):
            var1 = corr_matrix.columns[i]
            var2 = corr_matrix.columns[j]
            corr_val = corr_matrix.iloc[i, j]
            correlations.append((var1, var2, corr_val))
    
    # Сортируем по убыванию абсолютного значения
    correlations.sort(key=lambda x: abs(x[2]), reverse=True)
    
    for i, (var1, var2, corr_val) in enumerate(correlations[:5], 1):
        direction = "📈 Положительная" if corr_val > 0 else "📉 Отрицательная"
        strength = "🔥 Сильная" if abs(corr_val) > 0.7 else ("⚡ Средняя" if abs(corr_val) > 0.3 else "💨 Слабая")
        print(f"{i}. {var1} ↔ {var2}")
        print(f"   {direction} связь: {corr_val:.3f} ({strength})")
        print()

def simple_regression_analysis(df: pd.DataFrame, x_col: str, y_col: str) -> dict:
    """
    Выполняет простой регрессионный анализ между двумя переменными
    
    Параметры:
    ----------
    df : pd.DataFrame
        Данные для анализа
    x_col : str
        Название независимой переменной (X)
    y_col : str
        Название зависимой переменной (Y)
        
    Возвращает:
    ----------
    dict
        Результаты регрессионного анализа
    """
    
    if x_col not in df.columns or y_col not in df.columns:
        print(f"❌ Столбцы {x_col} или {y_col} не найдены")
        return {}
    
    # Подготавливаем данные
    X = df[[x_col]].values
    y = df[y_col].values
    
    # Убираем пропущенные значения
    mask = ~(np.isnan(X.flatten()) | np.isnan(y))
    X = X[mask]
    y = y[mask]
    
    if len(X) < 3:
        print("❌ Недостаточно данных для регрессии")
        return {}
    
    # Строим модель
    model = LinearRegression()
    model.fit(X, y)
    
    # Делаем предсказания
    y_pred = model.predict(X)
    
    # Рассчитываем метрики
    r2 = r2_score(y, y_pred)
    correlation, p_value = pearsonr(X.flatten(), y)
    mae = mean_absolute_error(y, y_pred)
    rmse = np.sqrt(mean_squared_error(y, y_pred))
    
    results = {
        'coefficient': model.coef_[0],
        'intercept': model.intercept_,
        'r_squared': r2,
        'correlation': correlation,
        'p_value': p_value,
        'mae': mae,
        'rmse': rmse,
        'n_observations': len(X)
    }
    
    # Выводим результаты
    print("📊 РЕЗУЛЬТАТЫ ПРОСТОЙ РЕГРЕССИИ")
    print("=" * 40)
    print(f"📈 Модель: {y_col} = {model.intercept_:.2f} + {model.coef_[0]:.3f} × {x_col}")
    print()
    print("📋 Интерпретация коэффициентов:")
    print(f"• Базовый уровень: {model.intercept_:.2f}")
    print(f"• Эффект {x_col}: {model.coef_[0]:.3f}")
    if model.coef_[0] > 0:
        print(f"  → При увеличении {x_col} на 1 ед., {y_col} растет на {model.coef_[0]:.3f}")
    else:
        print(f"  → При увеличении {x_col} на 1 ед., {y_col} падает на {abs(model.coef_[0]):.3f}")
    print()
    print("📊 Качество модели:")
    print(f"• R² = {r2:.3f} (модель объясняет {r2*100:.1f}% вариации)")
    print(f"• Корреляция = {correlation:.3f}")
    print(f"• P-value = {p_value:.6f} ({'значимо' if p_value < 0.05 else 'НЕ значимо'})")
    print(f"• Средняя ошибка = {mae:.2f}")
    
    # Строим график
    plt.figure(figsize=(12, 5))
    
    # График рассеяния с линией регрессии
    plt.subplot(1, 2, 1)
    plt.scatter(X, y, alpha=0.6, color='steelblue', s=50)
    plt.plot(X, y_pred, color='red', linewidth=2, label=f'y = {model.intercept_:.1f} + {model.coef_[0]:.2f}x')
    plt.xlabel(x_col, fontsize=12)
    plt.ylabel(y_col, fontsize=12)
    plt.title(f'📈 Регрессионная модель\nR² = {r2:.3f}', fontsize=14)
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # График остатков
    residuals = y - y_pred
    plt.subplot(1, 2, 2)
    plt.scatter(y_pred, residuals, alpha=0.6, color='orange', s=50)
    plt.axhline(y=0, color='red', linestyle='--', linewidth=2)
    plt.xlabel('Предсказанные значения', fontsize=12)
    plt.ylabel('Остатки', fontsize=12)
    plt.title('🔍 Анализ остатков', fontsize=14)
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()
    
    return results

def multiple_regression_analysis(df: pd.DataFrame, target_col: str, feature_cols: list) -> dict:
    """
    Выполняет множественный регрессионный анализ
    
    Параметры:
    ----------
    df : pd.DataFrame
        Данные для анализа
    target_col : str
        Целевая переменная (Y)
    feature_cols : list
        Список независимых переменных (X)
        
    Возвращает:
    ----------
    dict
        Результаты множественной регрессии
    """
    
    # Проверяем наличие столбцов
    missing_cols = [col for col in feature_cols + [target_col] if col not in df.columns]
    if missing_cols:
        print(f"❌ Отсутствующие столбцы: {missing_cols}")
        return {}
    
    # Подготавливаем данные
    X = df[feature_cols].values
    y = df[target_col].values
    
    # Убираем строки с пропущенными значениями
    mask = ~(np.isnan(X).any(axis=1) | np.isnan(y))
    X = X[mask]
    y = y[mask]
    
    if len(X) < len(feature_cols) + 2:
        print("❌ Недостаточно данных для множественной регрессии")
        return {}
    
    # Строим модель
    model = LinearRegression()
    model.fit(X, y)
    
    # Делаем предсказания
    y_pred = model.predict(X)
    
    # Рассчитываем метрики
    r2 = r2_score(y, y_pred)
    mae = mean_absolute_error(y, y_pred)
    rmse = np.sqrt(mean_squared_error(y, y_pred))
    
    results = {
        'coefficients': dict(zip(feature_cols, model.coef_)),
        'intercept': model.intercept_,
        'r_squared': r2,
        'mae': mae,
        'rmse': rmse,
        'n_observations': len(X),
        'n_features': len(feature_cols)
    }
    
    # Выводим результаты
    print("📊 РЕЗУЛЬТАТЫ МНОЖЕСТВЕННОЙ РЕГРЕССИИ")
    print("=" * 45)
    
    # Формула модели
    formula_parts = [f"{model.intercept_:.2f}"]
    for feature, coef in zip(feature_cols, model.coef_):
        if coef >= 0:
            formula_parts.append(f"+ {coef:.3f}×{feature}")
        else:
            formula_parts.append(f"- {abs(coef):.3f}×{feature}")
    
    formula = f"{target_col} = " + " ".join(formula_parts)
    print(f"📈 Модель: {formula}")
    print()
    
    print("📋 Интерпретация коэффициентов:")
    print(f"• Константа: {model.intercept_:.2f} (базовый уровень)")
    
    for feature, coef in zip(feature_cols, model.coef_):
        direction = "увеличивается" if coef > 0 else "уменьшается"
        print(f"• {feature}: {coef:.3f}")
        print(f"  → При росте на 1 ед., {target_col} {direction} на {abs(coef):.3f}")
    print()
    
    print("📊 Качество модели:")
    print(f"• R² = {r2:.3f} (объясняет {r2*100:.1f}% вариации)")
    print(f"• Средняя ошибка = {mae:.2f}")
    print(f"• Наблюдений: {len(X)}")
    
    # График важности факторов
    plt.figure(figsize=(12, 6))
    
    # Важность факторов (по абсолютным значениям коэффициентов)
    plt.subplot(1, 2, 1)
    importances = np.abs(model.coef_)
    indices = np.argsort(importances)[::-1]
    
    colors = ['green' if coef > 0 else 'red' for coef in model.coef_[indices]]
    plt.bar(range(len(importances)), importances[indices], color=colors, alpha=0.7)
    plt.xlabel('Факторы')
    plt.ylabel('Важность (|коэффициент|)')
    plt.title('📊 Важность факторов')
    plt.xticks(range(len(feature_cols)), [feature_cols[i] for i in indices], rotation=45, ha='right')
    plt.grid(True, alpha=0.3)
    
    # График остатков vs предсказанные значения
    plt.subplot(1, 2, 2)
    residuals = y - y_pred
    plt.scatter(y_pred, residuals, alpha=0.6, color='purple', s=50)
    plt.axhline(y=0, color='red', linestyle='--', linewidth=2)
    plt.xlabel('Предсказанные значения')
    plt.ylabel('Остатки')
    plt.title('🔍 Анализ остатков')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()
    
    return results

def polynomial_regression_analysis(df: pd.DataFrame, x_col: str, y_col: str, degree: int = 2) -> dict:
    """
    Выполняет полиномиальную регрессию для нелинейных зависимостей
    
    Параметры:
    ----------
    df : pd.DataFrame
        Данные для анализа
    x_col : str
        Независимая переменная
    y_col : str
        Зависимая переменная
    degree : int
        Степень полинома (по умолчанию 2 - квадратичная)
        
    Возвращает:
    ----------
    dict
        Результаты полиномиальной регрессии
    """
    
    if x_col not in df.columns or y_col not in df.columns:
        print(f"❌ Столбцы {x_col} или {y_col} не найдены")
        return {}
    
    # Подготавливаем данные
    X = df[x_col].values.reshape(-1, 1)
    y = df[y_col].values
    
    # Убираем пропущенные значения
    mask = ~(np.isnan(X.flatten()) | np.isnan(y))
    X = X[mask]
    y = y[mask]
    
    # Создаем полиномиальные признаки
    poly_features = PolynomialFeatures(degree=degree)
    X_poly = poly_features.fit_transform(X)
    
    # Строим модели
    linear_model = LinearRegression()
    linear_model.fit(X, y)
    linear_pred = linear_model.predict(X)
    linear_r2 = r2_score(y, linear_pred)
    
    poly_model = LinearRegression()
    poly_model.fit(X_poly, y)
    poly_pred = poly_model.predict(X_poly)
    poly_r2 = r2_score(y, poly_pred)
    
    results = {
        'linear_r2': linear_r2,
        'polynomial_r2': poly_r2,
        'improvement': poly_r2 - linear_r2,
        'polynomial_coefficients': poly_model.coef_,
        'polynomial_intercept': poly_model.intercept_,
        'degree': degree,
        'better_model': 'polynomial' if poly_r2 > linear_r2 else 'linear'
    }
    
    # Выводим результаты
    print("📊 СРАВНЕНИЕ ЛИНЕЙНОЙ И ПОЛИНОМИАЛЬНОЙ МОДЕЛЕЙ")
    print("=" * 55)
    print(f"📈 Линейная модель R² = {linear_r2:.3f}")
    print(f"📈 Полиномиальная модель (степень {degree}) R² = {poly_r2:.3f}")
    print(f"🎯 Улучшение = {poly_r2 - linear_r2:.3f}")
    print()
    
    if poly_r2 > linear_r2 + 0.05:  # Значимое улучшение
        print("✅ Полиномиальная модель значительно лучше!")
        print("💡 В данных есть нелинейная зависимость")
    elif poly_r2 > linear_r2:
        print("⚡ Небольшое улучшение от полиномиальной модели")
        print("💡 Возможно, есть слабая нелинейность")
    else:
        print("❌ Линейная модель работает лучше")
        print("💡 Зависимость линейная")
    
    # График сравнения
    plt.figure(figsize=(15, 5))
    
    # Сортируем для красивой кривой
    sort_idx = np.argsort(X.flatten())
    X_sorted = X[sort_idx]
    y_sorted = y[sort_idx]
    X_poly_sorted = X_poly[sort_idx]
    linear_pred_sorted = linear_pred[sort_idx]
    poly_pred_sorted = poly_pred[sort_idx]
    
    # Линейная модель
    plt.subplot(1, 3, 1)
    plt.scatter(X, y, alpha=0.6, color='steelblue', s=50)
    plt.plot(X_sorted, linear_pred_sorted, color='red', linewidth=2, label=f'Linear (R²={linear_r2:.3f})')
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.title('📈 Линейная модель')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Полиномиальная модель
    plt.subplot(1, 3, 2)
    plt.scatter(X, y, alpha=0.6, color='steelblue', s=50)
    plt.plot(X_sorted, poly_pred_sorted, color='green', linewidth=2, label=f'Polynomial (R²={poly_r2:.3f})')
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.title(f'📈 Полиномиальная модель (степень {degree})')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Сравнение остатков
    plt.subplot(1, 3, 3)
    linear_residuals = y - linear_pred
    poly_residuals = y - poly_pred
    
    plt.scatter(linear_pred, linear_residuals, alpha=0.6, color='red', s=30, label='Линейная')
    plt.scatter(poly_pred, poly_residuals, alpha=0.6, color='green', s=30, label='Полиномиальная')
    plt.axhline(y=0, color='black', linestyle='--', linewidth=1)
    plt.xlabel('Предсказанные значения')
    plt.ylabel('Остатки')
    plt.title('🔍 Сравнение остатков')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()
    
    return results

def business_roi_calculator(model_results: dict, cost_per_unit: float, revenue_per_unit: float) -> dict:
    """
    Рассчитывает ROI и бизнес-эффект на основе модели регрессии
    
    Параметры:
    ----------
    model_results : dict
        Результаты регрессионного анализа
    cost_per_unit : float
        Стоимость единицы независимой переменной
    revenue_per_unit : float
        Выручка с единицы зависимой переменной
        
    Возвращает:
    ----------
    dict
        Расчеты ROI и бизнес-эффекта
    """
    
    if 'coefficient' not in model_results:
        print("❌ Некорректные результаты модели")
        return {}
    
    coefficient = model_results['coefficient']
    r_squared = model_results['r_squared']
    
    # Расчеты ROI
    revenue_increase = coefficient * revenue_per_unit
    roi_percent = (revenue_increase / cost_per_unit - 1) * 100 if cost_per_unit > 0 else 0
    payback_units = cost_per_unit / revenue_increase if revenue_increase > 0 else float('inf')
    
    results = {
        'coefficient': coefficient,
        'cost_per_unit': cost_per_unit,
        'revenue_per_unit': revenue_per_unit,
        'revenue_increase': revenue_increase,
        'roi_percent': roi_percent,
        'payback_units': payback_units,
        'model_reliability': r_squared
    }
    
    # Выводим результаты
    print("💰 РАСЧЕТ БИЗНЕС-ЭФФЕКТА И ROI")
    print("=" * 35)
    print(f"📊 Коэффициент модели: {coefficient:.3f}")
    print(f"💸 Затраты на единицу: {cost_per_unit:.2f} руб")
    print(f"💵 Выручка с единицы результата: {revenue_per_unit:.2f} руб")
    print()
    print("🎯 Бизнес-эффект:")
    print(f"• Рост результата на единицу затрат: {coefficient:.3f}")
    print(f"• Дополнительная выручка: {revenue_increase:.2f} руб")
    print(f"• ROI: {roi_percent:.1f}%")
    
    if roi_percent > 0:
        print(f"• ✅ Окупаемость: {payback_units:.1f} единиц")
        if roi_percent >= 100:
            print("🚀 ОТЛИЧНАЯ инвестиция!")
        elif roi_percent >= 50:
            print("✅ Хорошая инвестиция")
        elif roi_percent >= 20:
            print("⚡ Приемлемая инвестиция")
        else:
            print("⚠️ Низкая доходность")
    else:
        print("❌ Убыточная инвестиция")
    
    print(f"\n🎯 Надежность прогноза: {r_squared*100:.1f}% (R²)")
    
    return results

def validate_model(df: pd.DataFrame, target_col: str, feature_cols: list, test_size: float = 0.3) -> dict:
    """
    Валидирует модель на тестовых данных
    
    Параметры:
    ----------
    df : pd.DataFrame
        Полный набор данных
    target_col : str
        Целевая переменная
    feature_cols : list
        Список независимых переменных
    test_size : float
        Доля тестовых данных (по умолчанию 30%)
        
    Возвращает:
    ----------
    dict
        Результаты валидации
    """
    
    # Подготавливаем данные
    X = df[feature_cols].values
    y = df[target_col].values
    
    # Убираем пропущенные значения
    mask = ~(np.isnan(X).any(axis=1) | np.isnan(y))
    X = X[mask]
    y = y[mask]
    
    # Разделяем на обучение и тест
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=42
    )
    
    # Обучаем модель
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # Предсказания
    y_train_pred = model.predict(X_train)
    y_test_pred = model.predict(X_test)
    
    # Метрики
    train_r2 = r2_score(y_train, y_train_pred)
    test_r2 = r2_score(y_test, y_test_pred)
    train_mae = mean_absolute_error(y_train, y_train_pred)
    test_mae = mean_absolute_error(y_test, y_test_pred)
    
    results = {
        'train_r2': train_r2,
        'test_r2': test_r2,
        'train_mae': train_mae,
        'test_mae': test_mae,
        'overfitting': train_r2 - test_r2,
        'train_size': len(X_train),
        'test_size': len(X_test)
    }
    
    # Анализ результатов
    print("🧪 ВАЛИДАЦИЯ МОДЕЛИ НА ТЕСТОВЫХ ДАННЫХ")
    print("=" * 45)
    print(f"📊 Обучающая выборка: {len(X_train)} наблюдений")
    print(f"📊 Тестовая выборка: {len(X_test)} наблюдений")
    print()
    print("📈 Качество модели:")
    print(f"• R² на обучении: {train_r2:.3f}")
    print(f"• R² на тесте: {test_r2:.3f}")
    print(f"• Средняя ошибка на обучении: {train_mae:.2f}")
    print(f"• Средняя ошибка на тесте: {test_mae:.2f}")
    print()
    
    # Диагностика переобучения
    overfitting = train_r2 - test_r2
    print("🔍 Диагностика переобучения:")
    print(f"• Разница R²: {overfitting:.3f}")
    
    if overfitting < 0.05:
        print("✅ Модель стабильна, переобучения нет")
    elif overfitting < 0.15:
        print("⚠️ Небольшое переобучение, модель приемлема")
    else:
        print("❌ Сильное переобучение, упростите модель")
    
    # График сравнения
    plt.figure(figsize=(12, 5))
    
    plt.subplot(1, 2, 1)
    plt.scatter(y_train_pred, y_train, alpha=0.6, color='blue', label=f'Обучение (R²={train_r2:.3f})')
    plt.scatter(y_test_pred, y_test, alpha=0.6, color='red', label=f'Тест (R²={test_r2:.3f})')
    
    # Линия идеального предсказания
    min_val = min(min(y_train), min(y_test))
    max_val = max(max(y_train), max(y_test))
    plt.plot([min_val, max_val], [min_val, max_val], 'k--', alpha=0.8, linewidth=2)
    
    plt.xlabel('Предсказанные значения')
    plt.ylabel('Реальные значения')
    plt.title('🎯 Качество предсказаний')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Распределение ошибок
    plt.subplot(1, 2, 2)
    train_residuals = y_train - y_train_pred
    test_residuals = y_test - y_test_pred
    
    plt.hist(train_residuals, bins=20, alpha=0.7, color='blue', label='Обучение')
    plt.hist(test_residuals, bins=20, alpha=0.7, color='red', label='Тест')
    plt.xlabel('Ошибки предсказания')
    plt.ylabel('Частота')
    plt.title('📊 Распределение ошибок')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()
    
    return results

# Демонстрация использования
if __name__ == "__main__":
    print("🚀 ДЕМОНСТРАЦИЯ КОРРЕЛЯЦИОННОГО И РЕГРЕССИОННОГО АНАЛИЗА")
    print("=" * 60)
    
    # Пример 1: Загрузка и корреляционный анализ
    print("\n1️⃣ КОРРЕЛЯЦИОННЫЙ АНАЛИЗ")
    print("-" * 30)
    
    # Пробуем загрузить business_metrics.csv
    df_business = load_business_data('business_metrics.csv')
    
    if not df_business.empty:
        print("\n🔗 Строим карту корреляций...")
        create_correlation_matrix(df_business)
    
    # Пример 2: Простая регрессия
    print("\n2️⃣ ПРОСТАЯ РЕГРЕССИЯ")
    print("-" * 25)
    
    # Пробуем загрузить advertising_sales.csv
    df_ads = load_business_data('advertising_sales.csv')
    
    if not df_ads.empty and 'advertising_budget' in df_ads.columns and 'sales' in df_ads.columns:
        print("\n📈 Анализ связи реклама → продажи...")
        results = simple_regression_analysis(df_ads, 'advertising_budget', 'sales')
        
        if results:
            # Расчет ROI для рекламы
            print("\n💰 Расчет ROI рекламы...")
            roi_results = business_roi_calculator(results, cost_per_unit=1000, revenue_per_unit=1000)
    
    # Пример 3: Множественная регрессия
    print("\n3️⃣ МНОЖЕСТВЕННАЯ РЕГРЕССИЯ")
    print("-" * 30)
    
    df_multiple = load_business_data('multiple_factors.csv')
    
    if not df_multiple.empty:
        feature_columns = ['advertising_budget', 'num_promotions', 'seasonal_index', 'competitor_activity']
        available_features = [col for col in feature_columns if col in df_multiple.columns]
        
        if len(available_features) >= 2 and 'sales' in df_multiple.columns:
            print(f"\n📊 Анализ влияния факторов: {available_features}")
            multiple_results = multiple_regression_analysis(df_multiple, 'sales', available_features)
            
            if multiple_results:
                print("\n🧪 Валидация модели...")
                validation_results = validate_model(df_multiple, 'sales', available_features)
    
    # Пример 4: Нелинейные зависимости
    print("\n4️⃣ НЕЛИНЕЙНЫЕ ЗАВИСИМОСТИ")
    print("-" * 35)
    
    df_nonlinear = load_business_data('nonlinear_data.csv')
    
    if not df_nonlinear.empty and 'price' in df_nonlinear.columns and 'demand' in df_nonlinear.columns:
        print("\n🔄 Анализ нелинейной связи цена → спрос...")
        poly_results = polynomial_regression_analysis(df_nonlinear, 'price', 'demand', degree=2)
    
    print("\n🎉 Демонстрация завершена!")
    print("💡 Используйте функции из этого скрипта для анализа своих данных")