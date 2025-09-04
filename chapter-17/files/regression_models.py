"""
📈 Регрессионные модели в машинном обучении

Этот скрипт демонстрирует:
- Линейную регрессию с интерпретацией коэффициентов
- Полиномиальную регрессию для нелинейных зависимостей
- Регуляризацию (Ridge, Lasso) для борьбы с переобучением
- Random Forest для регрессии
- Анализ остатков и диагностику моделей
- Бизнес-применение для прогнозирования цен
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.pipeline import Pipeline
import warnings

warnings.filterwarnings('ignore')

print("📈 Изучаем регрессионные модели в машинном обучении!")
print("=" * 55)

# Настройка визуализации
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10
sns.set_style("whitegrid")

def generate_real_estate_data():
    """Генерируем данные недвижимости для демонстрации регрессии"""
    np.random.seed(42)
    n_properties = 1000
    
    print("🏠 Генерируем данные рынка недвижимости...")
    
    # Создаем данные с реалистичными закономерностями
    data = {}
    
    # Базовые характеристики
    data['total_area'] = np.random.gamma(3, 20)  # площадь в кв.м
    data['total_area'] = np.clip(data['total_area'], 30, 250)
    
    # Комнаты зависят от площади
    data['rooms'] = np.where(
        data['total_area'] < 40, 1,
        np.where(data['total_area'] < 60, 2,
                np.where(data['total_area'] < 100, 3, 4))
    )
    
    # Этаж
    data['floor'] = np.random.randint(1, 26, n_properties)
    data['total_floors'] = data['floor'] + np.random.randint(0, 15)
    data['total_floors'] = np.clip(data['total_floors'], data['floor'], 30)
    
    # Год постройки
    data['year_built'] = np.random.randint(1960, 2024, n_properties)
    
    # Район влияет на цену
    districts = ['Центр', 'Спальный район', 'Новостройки', 'Окраина']
    district_multipliers = [2.0, 1.0, 1.3, 0.7]
    data['district'] = np.random.choice(districts, n_properties)
    
    # Расстояние до центра
    district_distances = {'Центр': 3, 'Спальный район': 15, 'Новостройки': 25, 'Окраина': 35}
    data['center_distance'] = [district_distances[d] + np.random.normal(0, 5) for d in data['district']]
    data['center_distance'] = np.clip(data['center_distance'], 1, 50)
    
    # Метро (не везде есть)
    data['has_metro'] = np.random.choice([True, False], n_properties, p=[0.6, 0.4])
    data['metro_distance'] = np.where(
        data['has_metro'],
        np.random.gamma(2, 0.5),  # км до метро
        np.nan
    )
    
    # Состояние и удобства
    data['renovation_quality'] = np.random.choice(['Без ремонта', 'Косметический', 'Евроремонт'], 
                                                 n_properties, p=[0.3, 0.5, 0.2])
    renovation_multipliers = {'Без ремонта': 0.85, 'Косметический': 1.0, 'Евроремонт': 1.2}
    
    data['has_balcony'] = np.random.choice([True, False], n_properties, p=[0.7, 0.3])
    data['has_parking'] = np.random.choice([True, False], n_properties, p=[0.4, 0.6])
    
    # Экология и инфраструктура
    data['school_rating'] = np.random.gamma(2, 2)
    data['school_rating'] = np.clip(data['school_rating'], 1, 10)
    
    data['park_distance'] = np.random.exponential(2)  # км до парка
    data['noise_level'] = np.random.gamma(2, 2)  # уровень шума
    data['noise_level'] = np.clip(data['noise_level'], 1, 10)
    
    # Рассчитываем цену на основе всех факторов
    base_price_per_sqm = 100000  # базовая цена за кв.м
    
    price_per_sqm = base_price_per_sqm
    
    # Влияние района
    for i in range(n_properties):
        district = data['district'][i]
        district_idx = districts.index(district)
        price_per_sqm_i = base_price_per_sqm * district_multipliers[district_idx]
        
        # Влияние площади (больше площадь -> дешевле за кв.м)
        area_factor = max(0.7, 1 - (data['total_area'][i] - 60) / 500)
        price_per_sqm_i *= area_factor
        
        # Влияние этажа (первый и последний дешевле)
        floor = data['floor'][i]
        total_floors = data['total_floors'][i]
        if floor == 1 or floor == total_floors:
            floor_factor = 0.95
        else:
            floor_factor = 1.0
        price_per_sqm_i *= floor_factor
        
        # Влияние года постройки
        age = 2024 - data['year_built'][i]
        age_factor = max(0.6, 1 - age / 200)  # старые дома дешевле
        price_per_sqm_i *= age_factor
        
        # Влияние ремонта
        renovation = data['renovation_quality'][i]
        price_per_sqm_i *= renovation_multipliers[renovation]
        
        # Влияние расстояния до центра
        distance_factor = max(0.5, 1 - data['center_distance'][i] / 100)
        price_per_sqm_i *= distance_factor
        
        # Влияние метро
        if data['has_metro'][i] and not np.isnan(data['metro_distance'][i]):
            metro_factor = max(0.8, 1 - data['metro_distance'][i] / 10)
            price_per_sqm_i *= metro_factor
        elif not data['has_metro'][i]:
            price_per_sqm_i *= 0.85  # нет метро вообще
        
        # Влияние удобств
        if data['has_balcony'][i]:
            price_per_sqm_i *= 1.05
        if data['has_parking'][i]:
            price_per_sqm_i *= 1.1
        
        # Влияние инфраструктуры
        school_factor = 0.9 + data['school_rating'][i] / 50
        price_per_sqm_i *= school_factor
        
        park_factor = max(0.9, 1 - data['park_distance'][i] / 20)
        price_per_sqm_i *= park_factor
        
        noise_factor = max(0.8, 1 - (data['noise_level'][i] - 5) / 20)
        price_per_sqm_i *= noise_factor
        
        # Итоговая цена
        total_price = price_per_sqm_i * data['total_area'][i]
        
        # Добавляем случайность
        total_price *= np.random.normal(1, 0.15)
        
        # Сохраняем
        if i == 0:
            data['price'] = [max(1000000, total_price)]
        else:
            data['price'].append(max(1000000, total_price))
    
    # Конвертируем в DataFrame
    df = pd.DataFrame(data)
    
    # Округляем цены
    df['price'] = df['price'].round(-3)  # округляем до тысяч
    
    print(f"✅ Создано {len(df)} объектов недвижимости")
    print(f"📊 Цены от {df['price'].min():,.0f} до {df['price'].max():,.0f} руб.")
    print(f"📈 Средняя цена: {df['price'].mean():,.0f} руб.")
    print(f"📏 Средняя площадь: {df['total_area'].mean():.1f} кв.м")
    
    return df

def explore_real_estate_data(data):
    """Исследовательский анализ данных недвижимости"""
    print("\n🔍 Исследовательский анализ рынка недвижимости:")
    print("=" * 50)
    
    # Базовая статистика
    print("📊 Описательная статистика:")
    print(data[['total_area', 'rooms', 'year_built', 'center_distance', 'price']].describe())
    
    # Корреляция с ценой
    numeric_columns = data.select_dtypes(include=[np.number]).columns
    correlations = data[numeric_columns].corr()['price'].abs().sort_values(ascending=False)
    
    print(f"\n🎯 Корреляция с ценой:")
    for col, corr in correlations.items():
        if col != 'price':
            print(f"  {col}: {corr:.3f}")
    
    # Визуализация
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.suptitle('🏠 Анализ рынка недвижимости', fontsize=16)
    
    # Распределение цен
    axes[0,0].hist(data['price'] / 1e6, bins=30, alpha=0.7, edgecolor='black')
    axes[0,0].set_title('📊 Распределение цен')
    axes[0,0].set_xlabel('Цена (млн руб.)')
    axes[0,0].set_ylabel('Количество')
    
    # Цена vs площадь
    axes[0,1].scatter(data['total_area'], data['price'] / 1e6, alpha=0.6)
    axes[0,1].set_title('📈 Площадь vs Цена')
    axes[0,1].set_xlabel('Площадь (кв.м)')
    axes[0,1].set_ylabel('Цена (млн руб.)')
    
    # Цены по районам
    district_prices = data.groupby('district')['price'].mean() / 1e6
    district_prices.plot(kind='bar', ax=axes[0,2])
    axes[0,2].set_title('🏙️ Средние цены по районам')
    axes[0,2].set_ylabel('Цена (млн руб.)')
    axes[0,2].tick_params(axis='x', rotation=45)
    
    # Влияние года постройки
    data['age'] = 2024 - data['year_built']
    axes[1,0].scatter(data['age'], data['price'] / 1e6, alpha=0.6)
    axes[1,0].set_title('🏗️ Возраст vs Цена')
    axes[1,0].set_xlabel('Возраст дома (лет)')
    axes[1,0].set_ylabel('Цена (млн руб.)')
    
    # Влияние расстояния до центра
    axes[1,1].scatter(data['center_distance'], data['price'] / 1e6, alpha=0.6)
    axes[1,1].set_title('🎯 Расстояние до центра vs Цена')
    axes[1,1].set_xlabel('Расстояние до центра (км)')
    axes[1,1].set_ylabel('Цена (млн руб.)')
    
    # Корреляционная матрица
    important_features = ['total_area', 'rooms', 'floor', 'year_built', 
                         'center_distance', 'school_rating', 'price']
    correlation_matrix = data[important_features].corr()
    
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0, ax=axes[1,2])
    axes[1,2].set_title('🔥 Корреляционная матрица')
    
    plt.tight_layout()
    plt.show()

def prepare_regression_data(data):
    """Подготовка данных для регрессионного анализа"""
    print("\n🔧 Подготовка данных для регрессионного анализа:")
    print("=" * 50)
    
    # Создаем копию
    df = data.copy()
    
    # Feature engineering
    print("✨ Создание новых признаков...")
    df['age'] = 2024 - df['year_built']
    df['price_per_sqm'] = df['price'] / df['total_area']
    df['floor_ratio'] = df['floor'] / df['total_floors']
    
    # Логарифмические трансформации
    df['log_total_area'] = np.log(df['total_area'])
    df['log_center_distance'] = np.log(df['center_distance'] + 1)
    
    # Категориальные признаки
    df['is_new_building'] = (df['age'] <= 5).astype(int)
    df['is_center'] = (df['district'] == 'Центр').astype(int)
    df['is_first_or_last_floor'] = ((df['floor'] == 1) | 
                                   (df['floor'] == df['total_floors'])).astype(int)
    
    # One-hot encoding для района
    district_dummies = pd.get_dummies(df['district'], prefix='district')
    df = pd.concat([df, district_dummies], axis=1)
    
    # One-hot encoding для ремонта
    renovation_dummies = pd.get_dummies(df['renovation_quality'], prefix='renovation')
    df = pd.concat([df, renovation_dummies], axis=1)
    
    # Обработка пропусков в metro_distance
    df['metro_distance'] = df['metro_distance'].fillna(df['metro_distance'].median())
    df['has_metro_numeric'] = df['has_metro'].astype(int)
    
    # Выбираем признаки для модели
    feature_columns = [
        'total_area', 'rooms', 'floor', 'total_floors', 'age',
        'center_distance', 'metro_distance', 'school_rating',
        'park_distance', 'noise_level', 'floor_ratio',
        'has_balcony', 'has_parking', 'has_metro_numeric',
        'is_new_building', 'is_center', 'is_first_or_last_floor'
    ] + list(district_dummies.columns) + list(renovation_dummies.columns)
    
    # Преобразуем булевы признаки в числовые
    boolean_columns = ['has_balcony', 'has_parking']
    for col in boolean_columns:
        df[col] = df[col].astype(int)
    
    X = df[feature_columns]
    y = df['price']
    
    print(f"📊 Итоговые признаки для модели: {len(X.columns)}")
    print(f"   Числовые признаки: {len([col for col in X.columns if not col.startswith(('district_', 'renovation_'))])}")
    print(f"   Категориальные (район): {len([col for col in X.columns if col.startswith('district_')])}")
    print(f"   Категориальные (ремонт): {len([col for col in X.columns if col.startswith('renovation_')])}")
    
    return X, y, feature_columns

def train_regression_models(X, y, feature_names):
    """Обучение различных регрессионных моделей"""
    print("\n📈 Обучение регрессионных моделей:")
    print("=" * 35)
    
    # Разделение данных
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    print(f"📊 Разделение данных:")
    print(f"  Обучающая выборка: {len(X_train)} объектов")
    print(f"  Тестовая выборка: {len(X_test)} объектов")
    print(f"  Средняя цена в train: {y_train.mean():,.0f} руб.")
    print(f"  Средняя цена в test: {y_test.mean():,.0f} руб.")
    
    # Масштабирование для некоторых моделей
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    models = {}
    results = {}
    
    # 1. Линейная регрессия
    print(f"\n📏 Обучение линейной регрессии...")
    linear_reg = LinearRegression()
    linear_reg.fit(X_train, y_train)
    models['Линейная регрессия'] = (linear_reg, X_train, X_test)
    
    # 2. Полиномиальная регрессия (степень 2)
    print(f"🌊 Обучение полиномиальной регрессии...")
    poly_pipeline = Pipeline([
        ('poly', PolynomialFeatures(degree=2, interaction_only=True, include_bias=False)),
        ('scaler', StandardScaler()),
        ('linear', LinearRegression())
    ])
    poly_pipeline.fit(X_train, y_train)
    models['Полиномиальная регрессия'] = (poly_pipeline, X_train, X_test)
    
    # 3. Ridge регрессия (L2 регуляризация)
    print(f"🏔️ Обучение Ridge регрессии...")
    ridge = Ridge(alpha=1000.0)
    ridge.fit(X_train_scaled, y_train)
    models['Ridge регрессия'] = (ridge, X_train_scaled, X_test_scaled)
    
    # 4. Lasso регрессия (L1 регуляризация)
    print(f"🎯 Обучение Lasso регрессии...")
    lasso = Lasso(alpha=10000.0)
    lasso.fit(X_train_scaled, y_train)
    models['Lasso регрессия'] = (lasso, X_train_scaled, X_test_scaled)
    
    # 5. Random Forest
    print(f"🌲 Обучение Random Forest...")
    rf_reg = RandomForestRegressor(
        n_estimators=100,
        max_depth=15,
        min_samples_split=5,
        random_state=42,
        n_jobs=-1
    )
    rf_reg.fit(X_train, y_train)
    models['Random Forest'] = (rf_reg, X_train, X_test)
    
    # Оценка моделей
    print(f"\n📊 Оценка качества моделей:")
    print("-" * 90)
    print(f"{'Модель':<25} {'R²':<8} {'RMSE':<15} {'MAE':<15} {'MAPE (%)':<10}")
    print("-" * 90)
    
    for name, (model, X_tr, X_te) in models.items():
        # Предсказания
        y_pred = model.predict(X_te)
        
        # Метрики
        r2 = r2_score(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        mae = mean_absolute_error(y_test, y_pred)
        mape = np.mean(np.abs((y_test - y_pred) / y_test)) * 100
        
        results[name] = {
            'model': model,
            'y_pred': y_pred,
            'r2': r2,
            'rmse': rmse,
            'mae': mae,
            'mape': mape
        }
        
        print(f"{name:<25} {r2:<8.3f} {rmse:<15,.0f} {mae:<15,.0f} {mape:<10.1f}")
    
    return models, results, X_train, X_test, y_train, y_test, scaler, feature_names

def visualize_regression_results(models, results, X_test, y_test, feature_names):
    """Визуализация результатов регрессионных моделей"""
    print(f"\n🎨 Визуализация результатов регрессии:")
    
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.suptitle('📈 Сравнение регрессионных моделей', fontsize=16)
    
    # 1. Сравнение метрик
    metrics_df = pd.DataFrame({
        name: [res['r2'], res['rmse']/1e6, res['mae']/1e6, res['mape']]
        for name, res in results.items()
    }, index=['R²', 'RMSE (млн)', 'MAE (млн)', 'MAPE (%)'])
    
    metrics_df.plot(kind='bar', ax=axes[0,0])
    axes[0,0].set_title('📊 Сравнение метрик')
    axes[0,0].set_ylabel('Значение метрики')
    axes[0,0].legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    axes[0,0].tick_params(axis='x', rotation=45)
    
    # 2-4. Предсказания vs реальные значения для топ-3 моделей
    best_models = sorted(results.keys(), key=lambda x: results[x]['r2'], reverse=True)[:3]
    
    for i, model_name in enumerate(best_models):
        ax = axes[0, i+1] if i < 2 else axes[1, 0]
        
        y_pred = results[model_name]['y_pred']
        r2 = results[model_name]['r2']
        
        ax.scatter(y_test/1e6, y_pred/1e6, alpha=0.6)
        
        # Линия идеального предсказания
        min_val, max_val = min(y_test.min(), y_pred.min())/1e6, max(y_test.max(), y_pred.max())/1e6
        ax.plot([min_val, max_val], [min_val, max_val], 'r--', lw=2)
        
        ax.set_xlabel('Реальная цена (млн руб.)')
        ax.set_ylabel('Предсказанная цена (млн руб.)')
        ax.set_title(f'{model_name}\nR² = {r2:.3f}')
        ax.grid(True, alpha=0.3)
    
    # 5. Остатки для лучшей модели
    best_model_name = best_models[0]
    best_pred = results[best_model_name]['y_pred']
    residuals = y_test - best_pred
    
    axes[1,1].scatter(best_pred/1e6, residuals/1e6, alpha=0.6)
    axes[1,1].axhline(y=0, color='r', linestyle='--')
    axes[1,1].set_xlabel('Предсказанная цена (млн руб.)')
    axes[1,1].set_ylabel('Остатки (млн руб.)')
    axes[1,1].set_title(f'📊 Остатки ({best_model_name})')
    axes[1,1].grid(True, alpha=0.3)
    
    # 6. Q-Q plot остатков
    from scipy import stats
    stats.probplot(residuals, dist="norm", plot=axes[1,2])
    axes[1,2].set_title(f'📈 Q-Q plot остатков\n({best_model_name})')
    
    plt.tight_layout()
    plt.show()

def analyze_feature_importance_regression(models, feature_names):
    """Анализ важности признаков для регрессионных моделей"""
    print(f"\n🎯 Анализ важности признаков в регрессии:")
    print("=" * 45)
    
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    
    # Линейная регрессия - коэффициенты
    linear_model = models['Линейная регрессия'][0]
    linear_coef = pd.DataFrame({
        'feature': feature_names,
        'coefficient': linear_model.coef_,
        'abs_coefficient': np.abs(linear_model.coef_)
    }).sort_values('abs_coefficient', ascending=True)
    
    # Топ-10 коэффициентов по модулю
    top_coef = linear_coef.tail(10)
    bars = axes[0].barh(range(len(top_coef)), top_coef['coefficient'])
    
    # Раскрашиваем положительные и отрицательные коэффициенты
    for i, bar in enumerate(bars):
        if top_coef.iloc[i]['coefficient'] > 0:
            bar.set_color('green')
        else:
            bar.set_color('red')
    
    axes[0].set_yticks(range(len(top_coef)))
    axes[0].set_yticklabels(top_coef['feature'])
    axes[0].set_title('📊 Коэффициенты линейной регрессии\n(топ-10 по модулю)')
    axes[0].set_xlabel('Коэффициент')
    
    # Lasso регрессия - отобранные признаки
    lasso_model = models['Lasso регрессия'][0]
    lasso_coef = pd.DataFrame({
        'feature': feature_names,
        'coefficient': lasso_model.coef_
    })
    # Убираем признаки с нулевыми коэффициентами
    lasso_selected = lasso_coef[lasso_coef['coefficient'] != 0].copy()
    lasso_selected['abs_coefficient'] = np.abs(lasso_selected['coefficient'])
    lasso_selected = lasso_selected.sort_values('abs_coefficient', ascending=True)
    
    if len(lasso_selected) > 0:
        top_lasso = lasso_selected.tail(10)
        bars = axes[1].barh(range(len(top_lasso)), top_lasso['coefficient'])
        
        for i, bar in enumerate(bars):
            if top_lasso.iloc[i]['coefficient'] > 0:
                bar.set_color('green')
            else:
                bar.set_color('red')
        
        axes[1].set_yticks(range(len(top_lasso)))
        axes[1].set_yticklabels(top_lasso['feature'])
        axes[1].set_title(f'🎯 Lasso: отобранные признаки\n({len(lasso_selected)} из {len(feature_names)})')
        axes[1].set_xlabel('Коэффициент')
    
    # Random Forest - важность признаков
    rf_model = models['Random Forest'][0]
    rf_importance = pd.DataFrame({
        'feature': feature_names,
        'importance': rf_model.feature_importances_
    }).sort_values('importance', ascending=True)
    
    rf_importance.tail(10).plot(x='feature', y='importance', kind='barh', 
                               ax=axes[2], color='darkgreen')
    axes[2].set_title('🌲 Random Forest\nважность признаков')
    axes[2].set_xlabel('Важность')
    
    plt.tight_layout()
    plt.show()
    
    # Выводим интерпретацию
    print(f"💡 Интерпретация важных признаков:")
    print(f"\n📊 Линейная регрессия (топ-5):")
    for _, row in linear_coef.tail(5).iterrows():
        effect = "увеличивает" if row['coefficient'] > 0 else "уменьшает"
        print(f"  {row['feature']}: {effect} цену на {abs(row['coefficient']):,.0f} руб.")
    
    if len(lasso_selected) > 0:
        print(f"\n🎯 Lasso отобрал {len(lasso_selected)} из {len(feature_names)} признаков")
        print(f"   Это помогает избежать переобучения и улучшить интерпретируемость")
    
    print(f"\n🌲 Random Forest (топ-3):")
    for _, row in rf_importance.tail(3).iterrows():
        print(f"  {row['feature']}: важность {row['importance']:.3f}")

def cross_validation_regression(models, X, y):
    """Кросс-валидация регрессионных моделей"""
    print(f"\n🔄 Кросс-валидация регрессионных моделей:")
    print("=" * 45)
    
    cv_results = {}
    scaler = StandardScaler()
    
    for name, (model, _, _) in models.items():
        print(f"Тестируем {name}...")
        
        if name in ['Ridge регрессия', 'Lasso регрессия']:
            # Для регуляризованных моделей нужно масштабирование
            # Создаем пайплайн для правильной кросс-валидации
            pipeline = Pipeline([
                ('scaler', StandardScaler()),
                ('model', model)
            ])
            cv_scores = cross_val_score(pipeline, X, y, cv=5, scoring='r2')
        else:
            cv_scores = cross_val_score(model, X, y, cv=5, scoring='r2')
        
        cv_results[name] = cv_scores
        
        print(f"  R² по фолдам: {cv_scores}")
        print(f"  Среднее R²: {cv_scores.mean():.3f} ± {cv_scores.std():.3f}")
        print(f"  Диапазон: [{cv_scores.min():.3f}, {cv_scores.max():.3f}]")
        print()
    
    # Визуализация
    plt.figure(figsize=(12, 6))
    cv_data = [scores for scores in cv_results.values()]
    box_plot = plt.boxplot(cv_data, labels=list(cv_results.keys()), patch_artist=True)
    
    # Раскрашиваем боксы
    colors = plt.cm.Set3(np.linspace(0, 1, len(cv_data)))
    for patch, color in zip(box_plot['boxes'], colors):
        patch.set_facecolor(color)
    
    plt.title('📊 Распределение R² по кросс-валидации')
    plt.ylabel('R²')
    plt.xticks(rotation=45)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

def business_case_real_estate(results, models, feature_names):
    """Бизнес-применение для оценки недвижимости"""
    print(f"\n💼 Бизнес-кейс: Автоматическая оценка недвижимости")
    print("=" * 55)
    
    # Выбираем лучшую модель
    best_model_name = max(results.keys(), key=lambda x: results[x]['r2'])
    best_result = results[best_model_name]
    best_model = best_result['model']
    
    print(f"🏆 Лучшая модель: {best_model_name}")
    print(f"   R² = {best_result['r2']:.3f}")
    print(f"   RMSE = {best_result['rmse']:,.0f} руб.")
    print(f"   MAE = {best_result['mae']:,.0f} руб.")
    print(f"   MAPE = {best_result['mape']:.1f}%")
    
    print(f"\n💡 Бизнес-интерпретация:")
    print(f"   • Модель объясняет {best_result['r2']*100:.0f}% дисперсии цен")
    print(f"   • Средняя ошибка оценки: ±{best_result['mae']:,.0f} руб.")
    print(f"   • Относительная ошибка: ±{best_result['mape']:.1f}%")
    
    if best_result['mape'] < 15:
        quality = "Отличное"
    elif best_result['mape'] < 25:
        quality = "Хорошее"
    else:
        quality = "Требует улучшения"
    
    print(f"   • Качество модели: {quality}")
    
    print(f"\n🎯 Применение в бизнесе:")
    
    # Оценка экономического эффекта
    avg_price = 8_000_000  # средняя цена квартиры
    manual_evaluation_cost = 5000  # стоимость ручной оценки
    model_evaluation_cost = 100   # стоимость автоматической оценки
    
    accuracy_threshold = 0.15  # приемлемая точность ±15%
    
    if best_result['mape'] <= accuracy_threshold * 100:
        automation_potential = 80  # можно автоматизировать 80% оценок
        print(f"   • Можно автоматизировать {automation_potential}% оценок")
        print(f"   • Экономия на каждой оценке: {manual_evaluation_cost - model_evaluation_cost:,} руб.")
        
        monthly_evaluations = 1000
        monthly_savings = monthly_evaluations * automation_potential/100 * (manual_evaluation_cost - model_evaluation_cost)
        annual_savings = monthly_savings * 12
        
        print(f"   • При {monthly_evaluations:,} оценок в месяц:")
        print(f"     - Месячная экономия: {monthly_savings:,.0f} руб.")
        print(f"     - Годовая экономия: {annual_savings:,.0f} руб.")
    
    # Рекомендации по улучшению
    print(f"\n🔧 Рекомендации по улучшению модели:")
    
    if best_result['r2'] < 0.8:
        print(f"   • Собрать дополнительные данные: транспортная доступность, криминогенность")
        print(f"   • Добавить данные о ремонте и планировке")
        print(f"   • Учесть сезонность рынка")
    
    if best_result['mape'] > 20:
        print(f"   • Сегментировать рынок по ценовым категориям")
        print(f"   • Создать отдельные модели для разных районов")
        print(f"   • Применить ансамблевые методы")
    
    print(f"   • Регулярно переобучать модель (рекомендуется каждые 3 месяца)")
    print(f"   • Мониторить drift в данных")

def create_price_prediction_system(best_model, scaler, feature_names):
    """Создает систему предсказания цен"""
    print(f"\n🔮 Система предсказания цен на недвижимость:")
    print("=" * 50)
    
    def predict_apartment_price(apartment_data):
        """
        Предсказывает цену квартиры
        
        apartment_data: dict с характеристиками квартиры
        """
        # Создаем DataFrame
        df = pd.DataFrame([apartment_data])
        
        # Добавляем недостающие признаки
        all_features = set(feature_names)
        current_features = set(df.columns)
        missing_features = all_features - current_features
        
        # Заполняем пропущенные признаки нулями (для one-hot encoded)
        for feature in missing_features:
            df[feature] = 0
        
        # Убеждаемся что порядок признаков правильный
        X_new = df[feature_names]
        
        # Предсказание
        if scaler is not None:
            X_new_scaled = scaler.transform(X_new)
            predicted_price = best_model.predict(X_new_scaled)[0]
        else:
            predicted_price = best_model.predict(X_new)[0]
        
        return max(0, predicted_price)
    
    # Демонстрация системы
    print(f"🧪 Тестируем систему предсказания:")
    
    test_apartments = [
        {
            "total_area": 65, "rooms": 2, "floor": 5, "total_floors": 16,
            "age": 10, "center_distance": 12, "metro_distance": 0.8,
            "school_rating": 7, "park_distance": 1.5, "noise_level": 4,
            "floor_ratio": 5/16, "has_balcony": 1, "has_parking": 0,
            "has_metro_numeric": 1, "is_new_building": 0, "is_center": 0,
            "is_first_or_last_floor": 0,
            "district_Спальный район": 1, "district_Центр": 0, "district_Новостройки": 0, "district_Окраина": 0,
            "renovation_Косметический": 1, "renovation_Без ремонта": 0, "renovation_Евроремонт": 0
        },
        {
            "total_area": 85, "rooms": 3, "floor": 3, "total_floors": 5,
            "age": 25, "center_distance": 5, "metro_distance": 0.3,
            "school_rating": 9, "park_distance": 0.5, "noise_level": 6,
            "floor_ratio": 3/5, "has_balcony": 1, "has_parking": 1,
            "has_metro_numeric": 1, "is_new_building": 0, "is_center": 1,
            "is_first_or_last_floor": 0,
            "district_Центр": 1, "district_Спальный район": 0, "district_Новостройки": 0, "district_Окраина": 0,
            "renovation_Евроремонт": 1, "renovation_Косметический": 0, "renovation_Без ремонта": 0
        }
    ]
    
    for i, apartment in enumerate(test_apartments, 1):
        predicted_price = predict_apartment_price(apartment)
        print(f"\n   Квартира {i}:")
        print(f"     • {apartment['rooms']}-комн, {apartment['total_area']} кв.м, {apartment['floor']}/{apartment['total_floors']} этаж")
        print(f"     • Возраст: {apartment['age']} лет, до центра: {apartment['center_distance']} км")
        print(f"     • Предсказанная цена: {predicted_price:,.0f} руб.")
        print(f"     • Цена за кв.м: {predicted_price/apartment['total_area']:,.0f} руб/кв.м")
    
    return predict_apartment_price

def main():
    """Основная функция демонстрации регрессии"""
    print("🚀 Запуск демонстрации регрессионных моделей!")
    
    # 1. Генерируем и исследуем данные
    data = generate_real_estate_data()
    explore_real_estate_data(data)
    
    # 2. Подготавливаем данные
    X, y, feature_names = prepare_regression_data(data)
    
    # 3. Обучаем модели
    models, results, X_train, X_test, y_train, y_test, scaler, _ = train_regression_models(X, y, feature_names)
    
    # 4. Визуализируем результаты
    visualize_regression_results(models, results, X_test, y_test, feature_names)
    
    # 5. Анализируем важность признаков
    analyze_feature_importance_regression(models, feature_names)
    
    # 6. Кросс-валидация
    cross_validation_regression(models, X, y)
    
    # 7. Бизнес-применение
    business_case_real_estate(results, models, feature_names)
    
    # 8. Создаем систему предсказания
    best_model_name = max(results.keys(), key=lambda x: results[x]['r2'])
    best_model = results[best_model_name]['model']
    best_scaler = scaler if 'Ridge' in best_model_name or 'Lasso' in best_model_name else None
    
    predict_func = create_price_prediction_system(best_model, best_scaler, feature_names)
    
    print(f"\n🎉 Демонстрация регрессионных моделей завершена!")
    print("📚 Следующий шаг: изучите model_evaluation.py")
    print("💡 Совет: экспериментируйте с feature engineering и регуляризацией!")
    
    return models, results, predict_func

if __name__ == "__main__":
    models, results, predict_function = main()