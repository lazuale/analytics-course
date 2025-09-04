"""
🎯 Основы классификации в машинном обучении

Этот скрипт демонстрирует:
- Логистическую регрессию, деревья решений, случайный лес
- Правильную подготовку данных для ML
- Оценку качества моделей классификации
- Интерпретацию результатов для бизнеса
- Визуализацию границ решений
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import (accuracy_score, precision_score, recall_score, 
                           f1_score, confusion_matrix, classification_report,
                           roc_curve, roc_auc_score, precision_recall_curve)
import warnings

warnings.filterwarnings('ignore')

print("🎯 Изучаем основы классификации в машинном обучении!")
print("=" * 60)

# Настройка визуализации
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10
sns.set_style("whitegrid")

def generate_sample_data():
    """Генерируем примерные данные клиентов для демонстрации классификации"""
    np.random.seed(42)
    n_customers = 1000
    
    print("🔧 Генерируем данные клиентов интернет-магазина...")
    
    # Создаем реалистичные данные с закономерностями
    data = {}
    
    # Демографические данные
    data['age'] = np.random.normal(35, 12, n_customers).astype(int)
    data['age'] = np.clip(data['age'], 18, 70)
    
    data['income'] = np.random.lognormal(11, 0.5, n_customers)  # log-normal распределение
    data['income'] = np.clip(data['income'], 20000, 500000)
    
    data['gender'] = np.random.choice(['M', 'F'], n_customers)
    
    # Поведенческие данные (зависят от демографии)
    data['days_since_registration'] = np.random.exponential(180, n_customers).astype(int)
    data['total_sessions'] = np.random.poisson(data['age'] / 3, n_customers)
    data['avg_session_duration'] = np.random.exponential(15, n_customers)  # минуты
    
    # Покупательское поведение
    data['total_spent'] = (
        data['income'] * 0.001 * np.random.uniform(0.5, 1.5, n_customers) +
        data['total_sessions'] * np.random.uniform(100, 500, n_customers)
    )
    
    data['number_of_purchases'] = np.random.poisson(
        np.clip(data['total_sessions'] / 5, 0, 20), n_customers
    )
    
    # Создаем целевую переменную на основе логичных закономерностей
    purchase_probability = (
        0.1 +  # базовая вероятность
        (data['income'] - np.min(data['income'])) / (np.max(data['income']) - np.min(data['income'])) * 0.3 +  # доход
        (data['total_sessions'] / np.max(data['total_sessions'])) * 0.2 +  # активность
        (data['total_spent'] / np.max(data['total_spent'])) * 0.3 +  # история трат
        np.random.normal(0, 0.1, n_customers)  # случайность
    )
    
    purchase_probability = np.clip(purchase_probability, 0, 1)
    data['will_purchase'] = np.random.binomial(1, purchase_probability, n_customers)
    
    # Конвертируем в DataFrame
    df = pd.DataFrame(data)
    
    # Добавляем категориальную переменную
    df['customer_type'] = pd.cut(df['total_spent'], 
                               bins=[0, 50000, 150000, np.inf], 
                               labels=['Bronze', 'Silver', 'Gold'])
    
    print(f"✅ Создано {len(df)} записей клиентов")
    print(f"📊 Распределение целевой переменной:")
    print(df['will_purchase'].value_counts())
    print(f"   Доля положительных случаев: {df['will_purchase'].mean():.1%}")
    
    return df

def explore_data(data):
    """Исследовательский анализ данных"""
    print("\n🔍 Исследовательский анализ данных:")
    print("=" * 40)
    
    # Базовая информация
    print(f"📏 Размерность данных: {data.shape}")
    print(f"📊 Типы данных:")
    print(data.dtypes)
    
    # Пропущенные значения
    missing = data.isnull().sum()
    if missing.sum() > 0:
        print(f"\n⚠️ Пропущенные значения:")
        print(missing[missing > 0])
    else:
        print(f"\n✅ Пропущенных значений нет")
    
    # Корреляция с целевой переменной
    numeric_columns = data.select_dtypes(include=[np.number]).columns
    correlations = data[numeric_columns].corr()['will_purchase'].abs().sort_values(ascending=False)
    
    print(f"\n🎯 Корреляция с целевой переменной:")
    for col, corr in correlations.items():
        if col != 'will_purchase':
            print(f"  {col}: {corr:.3f}")
    
    # Визуализация
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    # Распределение целевой переменной
    data['will_purchase'].value_counts().plot(kind='bar', ax=axes[0,0])
    axes[0,0].set_title('📊 Распределение целевой переменной')
    axes[0,0].set_xlabel('Будет покупать')
    axes[0,0].set_ylabel('Количество')
    
    # Корреляционная матрица
    sns.heatmap(data[numeric_columns].corr(), annot=True, cmap='coolwarm', 
                center=0, ax=axes[0,1])
    axes[0,1].set_title('🔥 Корреляционная матрица')
    
    # Распределение важных признаков
    data.boxplot(column='income', by='will_purchase', ax=axes[1,0])
    axes[1,0].set_title('💰 Доход vs Покупки')
    axes[1,0].set_xlabel('Будет покупать')
    axes[1,0].set_ylabel('Доход')
    
    data.boxplot(column='total_spent', by='will_purchase', ax=axes[1,1])
    axes[1,1].set_title('💳 История трат vs Покупки')
    axes[1,1].set_xlabel('Будет покупать')
    axes[1,1].set_ylabel('Потрачено ранее')
    
    plt.tight_layout()
    plt.show()

def prepare_data_for_ml(data):
    """Подготовка данных для машинного обучения"""
    print("\n🔧 Подготовка данных для машинного обучения:")
    print("=" * 45)
    
    # Создаем копию данных
    df = data.copy()
    
    # Feature engineering
    print("✨ Создание новых признаков...")
    df['spending_rate'] = df['total_spent'] / (df['days_since_registration'] + 1)
    df['session_value'] = df['total_spent'] / (df['total_sessions'] + 1)
    df['purchase_frequency'] = df['number_of_purchases'] / (df['total_sessions'] + 1)
    df['high_income'] = (df['income'] > df['income'].median()).astype(int)
    
    # Обработка категориальных переменных
    print("🏷️ Кодирование категориальных переменных...")
    le_gender = LabelEncoder()
    df['gender_encoded'] = le_gender.fit_transform(df['gender'])
    
    # One-hot encoding для customer_type
    customer_type_dummies = pd.get_dummies(df['customer_type'], prefix='type')
    df = pd.concat([df, customer_type_dummies], axis=1)
    
    # Выбираем признаки для модели
    feature_columns = [
        'age', 'income', 'days_since_registration', 'total_sessions',
        'avg_session_duration', 'total_spent', 'number_of_purchases',
        'spending_rate', 'session_value', 'purchase_frequency', 'high_income',
        'gender_encoded'
    ] + list(customer_type_dummies.columns)
    
    X = df[feature_columns]
    y = df['will_purchase']
    
    print(f"📊 Итоговые признаки для модели: {len(X.columns)}")
    print(f"   {list(X.columns)}")
    
    return X, y, feature_columns

def train_classification_models(X, y, feature_names):
    """Обучение различных моделей классификации"""
    print("\n🤖 Обучение моделей классификации:")
    print("=" * 40)
    
    # Разделение данных
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"📊 Разделение данных:")
    print(f"  Обучающая выборка: {len(X_train)} образцов")
    print(f"  Тестовая выборка: {len(X_test)} образцов")
    print(f"  Доля положительных в train: {y_train.mean():.1%}")
    print(f"  Доля положительных в test: {y_test.mean():.1%}")
    
    # Масштабирование данных (нужно для логистической регрессии)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Словарь для хранения моделей
    models = {}
    results = {}
    
    # 1. Логистическая регрессия
    print(f"\n🎯 Обучение логистической регрессии...")
    log_reg = LogisticRegression(random_state=42, max_iter=1000)
    log_reg.fit(X_train_scaled, y_train)
    models['Логистическая регрессия'] = (log_reg, X_train_scaled, X_test_scaled)
    
    # 2. Дерево решений
    print(f"🌳 Обучение дерева решений...")
    tree = DecisionTreeClassifier(
        max_depth=10, 
        min_samples_split=20, 
        random_state=42
    )
    tree.fit(X_train, y_train)
    models['Дерево решений'] = (tree, X_train, X_test)
    
    # 3. Случайный лес
    print(f"🌲 Обучение случайного леса...")
    rf = RandomForestClassifier(
        n_estimators=100, 
        max_depth=15,
        min_samples_split=10,
        random_state=42,
        n_jobs=-1
    )
    rf.fit(X_train, y_train)
    models['Случайный лес'] = (rf, X_train, X_test)
    
    # Оценка моделей
    print(f"\n📊 Оценка качества моделей:")
    print("-" * 80)
    print(f"{'Модель':<20} {'Accuracy':<10} {'Precision':<11} {'Recall':<8} {'F1':<8} {'AUC-ROC':<8}")
    print("-" * 80)
    
    for name, (model, X_tr, X_te) in models.items():
        # Предсказания
        y_pred = model.predict(X_te)
        y_proba = model.predict_proba(X_te)[:, 1]
        
        # Метрики
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        auc_roc = roc_auc_score(y_test, y_proba)
        
        results[name] = {
            'model': model,
            'y_pred': y_pred,
            'y_proba': y_proba,
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1': f1,
            'auc_roc': auc_roc
        }
        
        print(f"{name:<20} {accuracy:<10.3f} {precision:<11.3f} {recall:<8.3f} {f1:<8.3f} {auc_roc:<8.3f}")
    
    return models, results, X_train, X_test, y_train, y_test, scaler, feature_names

def visualize_model_results(models, results, X_test, y_test, feature_names):
    """Визуализация результатов моделей"""
    print(f"\n🎨 Визуализация результатов моделей:")
    
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.suptitle('📊 Сравнение моделей классификации', fontsize=16)
    
    # 1. Сравнение метрик
    metrics_df = pd.DataFrame({
        name: [res['accuracy'], res['precision'], res['recall'], res['f1'], res['auc_roc']]
        for name, res in results.items()
    }, index=['Accuracy', 'Precision', 'Recall', 'F1', 'AUC-ROC'])
    
    metrics_df.plot(kind='bar', ax=axes[0,0])
    axes[0,0].set_title('📊 Сравнение метрик')
    axes[0,0].set_ylabel('Значение метрики')
    axes[0,0].legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    axes[0,0].tick_params(axis='x', rotation=45)
    
    # 2. ROC-кривые
    for name, res in results.items():
        fpr, tpr, _ = roc_curve(y_test, res['y_proba'])
        axes[0,1].plot(fpr, tpr, label=f"{name} (AUC={res['auc_roc']:.3f})")
    
    axes[0,1].plot([0, 1], [0, 1], 'k--', label='Случайный классификатор')
    axes[0,1].set_xlabel('False Positive Rate')
    axes[0,1].set_ylabel('True Positive Rate')
    axes[0,1].set_title('📈 ROC-кривые')
    axes[0,1].legend()
    axes[0,1].grid(True, alpha=0.3)
    
    # 3. Precision-Recall кривые
    for name, res in results.items():
        precision, recall, _ = precision_recall_curve(y_test, res['y_proba'])
        axes[0,2].plot(recall, precision, label=f"{name}")
    
    axes[0,2].set_xlabel('Recall')
    axes[0,2].set_ylabel('Precision')
    axes[0,2].set_title('🎯 Precision-Recall кривые')
    axes[0,2].legend()
    axes[0,2].grid(True, alpha=0.3)
    
    # 4. Confusion matrices
    model_names = list(results.keys())
    for i, name in enumerate(model_names):
        if i >= 3:  # Показываем только первые 3
            break
        
        cm = confusion_matrix(y_test, results[name]['y_pred'])
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[1,i])
        axes[1,i].set_title(f'🔍 Матрица ошибок\n{name}')
        axes[1,i].set_xlabel('Предсказано')
        axes[1,i].set_ylabel('Реально')
    
    plt.tight_layout()
    plt.show()

def analyze_feature_importance(models, feature_names):
    """Анализ важности признаков"""
    print(f"\n🎯 Анализ важности признаков:")
    print("=" * 35)
    
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    
    # Логистическая регрессия - коэффициенты
    log_reg_model = models['Логистическая регрессия'][0]
    coefficients = pd.DataFrame({
        'feature': feature_names,
        'coefficient': log_reg_model.coef_[0],
        'abs_coefficient': np.abs(log_reg_model.coef_[0])
    }).sort_values('abs_coefficient', ascending=True)
    
    coefficients.tail(10).plot(x='feature', y='coefficient', kind='barh', ax=axes[0])
    axes[0].set_title('📊 Коэффициенты логистической регрессии\n(топ-10 по модулю)')
    axes[0].set_xlabel('Коэффициент')
    
    # Дерево решений - важность признаков
    tree_model = models['Дерево решений'][0]
    tree_importance = pd.DataFrame({
        'feature': feature_names,
        'importance': tree_model.feature_importances_
    }).sort_values('importance', ascending=True)
    
    tree_importance.tail(10).plot(x='feature', y='importance', kind='barh', ax=axes[1])
    axes[1].set_title('🌳 Важность признаков\n(дерево решений)')
    axes[1].set_xlabel('Важность')
    
    # Случайный лес - важность признаков
    rf_model = models['Случайный лес'][0]
    rf_importance = pd.DataFrame({
        'feature': feature_names,
        'importance': rf_model.feature_importances_
    }).sort_values('importance', ascending=True)
    
    rf_importance.tail(10).plot(x='feature', y='importance', kind='barh', ax=axes[2])
    axes[2].set_title('🌲 Важность признаков\n(случайный лес)')
    axes[2].set_xlabel('Важность')
    
    plt.tight_layout()
    plt.show()
    
    # Выводим топ-5 признаков для каждой модели
    print(f"🏆 Топ-5 важных признаков по моделям:")
    print(f"\n📊 Логистическая регрессия (по модулю коэффициента):")
    for _, row in coefficients.tail(5).iterrows():
        print(f"  {row['feature']}: {row['coefficient']:+.3f}")
    
    print(f"\n🌳 Дерево решений:")
    for _, row in tree_importance.tail(5).iterrows():
        print(f"  {row['feature']}: {row['importance']:.3f}")
    
    print(f"\n🌲 Случайный лес:")
    for _, row in rf_importance.tail(5).iterrows():
        print(f"  {row['feature']}: {row['importance']:.3f}")

def visualize_decision_tree(models, feature_names):
    """Визуализация дерева решений"""
    print(f"\n🌳 Визуализация дерева решений:")
    
    tree_model = models['Дерево решений'][0]
    
    plt.figure(figsize=(20, 12))
    plot_tree(tree_model, 
              feature_names=feature_names,
              class_names=['Не купит', 'Купит'],
              filled=True,
              rounded=True,
              fontsize=10,
              max_depth=3)  # Показываем только верхние 3 уровня
    plt.title('🌳 Структура дерева решений (первые 3 уровня)', fontsize=16)
    plt.show()

def cross_validation_analysis(models, X, y):
    """Анализ устойчивости моделей с помощью кросс-валидации"""
    print(f"\n🔄 Кросс-валидация моделей:")
    print("=" * 30)
    
    cv_results = {}
    
    for name, (model, X_data, _) in models.items():
        if 'Логистическая' in name:
            # Для логистической регрессии используем масштабированные данные
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            cv_scores = cross_val_score(model, X_scaled, y, cv=5, scoring='f1')
        else:
            cv_scores = cross_val_score(model, X, y, cv=5, scoring='f1')
        
        cv_results[name] = cv_scores
        
        print(f"{name}:")
        print(f"  F1-scores по фолдам: {cv_scores}")
        print(f"  Среднее F1: {cv_scores.mean():.3f} ± {cv_scores.std():.3f}")
        print(f"  Диапазон: [{cv_scores.min():.3f}, {cv_scores.max():.3f}]")
        print()
    
    # Визуализация результатов CV
    plt.figure(figsize=(12, 6))
    cv_data = [scores for scores in cv_results.values()]
    plt.boxplot(cv_data, labels=list(cv_results.keys()))
    plt.title('📊 Распределение F1-score по кросс-валидации')
    plt.ylabel('F1-score')
    plt.xticks(rotation=45)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

def business_interpretation(results, models, feature_names):
    """Бизнес-интерпретация результатов"""
    print(f"\n💼 Бизнес-интерпретация результатов:")
    print("=" * 40)
    
    # Выбираем лучшую модель по F1-score
    best_model_name = max(results.keys(), key=lambda x: results[x]['f1'])
    best_result = results[best_model_name]
    
    print(f"🏆 Лучшая модель: {best_model_name}")
    print(f"   F1-score: {best_result['f1']:.3f}")
    print(f"   Точность (Accuracy): {best_result['accuracy']:.3f}")
    print(f"   Precision: {best_result['precision']:.3f}")
    print(f"   Recall: {best_result['recall']:.3f}")
    
    print(f"\n💡 Бизнес-интерпретация:")
    print(f"   • Из 100 клиентов, которых модель предсказывает как покупателей,")
    print(f"     реально купят {best_result['precision']*100:.0f} клиентов")
    print(f"   • Модель найдет {best_result['recall']*100:.0f}% от всех потенциальных покупателей")
    print(f"   • Общая точность предсказаний: {best_result['accuracy']*100:.0f}%")
    
    # Рекомендации для маркетинга
    print(f"\n🎯 Рекомендации для маркетинговой кампании:")
    
    # Анализ важности признаков лучшей модели
    if 'Случайный лес' in best_model_name or 'Дерево' in best_model_name:
        model = models[best_model_name][0]
        importance = pd.DataFrame({
            'feature': feature_names,
            'importance': model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        print(f"   📊 Ключевые факторы для покупки (по {best_model_name}):")
        for _, row in importance.head(3).iterrows():
            feature = row['feature']
            imp = row['importance']
            print(f"   • {feature}: важность {imp:.3f}")
    
    print(f"\n💰 Экономический эффект:")
    print(f"   • При стоимости маркетингового контакта 100 руб. и среднем чеке 5000 руб:")
    print(f"   • ROI от таргетинга: {(best_result['precision'] * 5000 - 100) / 100 * 100:.0f}%")
    print(f"   • Рекомендуется связываться только с клиентами, для которых")
    print(f"     вероятность покупки > {1 - best_result['precision']:.2f}")

def create_prediction_function(best_model, scaler, feature_names):
    """Создает функцию для предсказания новых клиентов"""
    print(f"\n🔮 Создание функции предсказания:")
    print("=" * 35)
    
    def predict_customer_purchase(customer_data):
        """
        Предсказывает вероятность покупки для нового клиента
        
        customer_data: dict с характеристиками клиента
        """
        # Создаем DataFrame с одной строкой
        df = pd.DataFrame([customer_data])
        
        # Feature engineering (те же преобразования что и при обучении)
        if 'spending_rate' not in df.columns:
            df['spending_rate'] = df['total_spent'] / (df['days_since_registration'] + 1)
        if 'session_value' not in df.columns:
            df['session_value'] = df['total_spent'] / (df['total_sessions'] + 1)
        if 'purchase_frequency' not in df.columns:
            df['purchase_frequency'] = df['number_of_purchases'] / (df['total_sessions'] + 1)
        
        # Выбираем нужные признаки
        X_new = df[feature_names]
        
        # Предсказание
        if scaler is not None:
            X_new_scaled = scaler.transform(X_new)
            probability = best_model.predict_proba(X_new_scaled)[0, 1]
        else:
            probability = best_model.predict_proba(X_new)[0, 1]
        
        return probability
    
    # Демонстрация функции
    print(f"🧪 Тестируем функцию предсказания:")
    
    test_customers = [
        {
            'age': 30, 'income': 80000, 'days_since_registration': 365,
            'total_sessions': 50, 'avg_session_duration': 20, 'total_spent': 25000,
            'number_of_purchases': 8, 'high_income': 1, 'gender_encoded': 1,
            'type_Bronze': 0, 'type_Silver': 1, 'type_Gold': 0
        },
        {
            'age': 55, 'income': 150000, 'days_since_registration': 180,
            'total_sessions': 120, 'avg_session_duration': 25, 'total_spent': 80000,
            'number_of_purchases': 15, 'high_income': 1, 'gender_encoded': 0,
            'type_Bronze': 0, 'type_Silver': 0, 'type_Gold': 1
        }
    ]
    
    for i, customer in enumerate(test_customers, 1):
        prob = predict_customer_purchase(customer)
        print(f"   Клиент {i}: вероятность покупки = {prob:.1%}")
        recommendation = "Отправить предложение" if prob > 0.5 else "Не отправлять"
        print(f"   Рекомендация: {recommendation}")
        print()
    
    return predict_customer_purchase

def main():
    """Основная функция демонстрации классификации"""
    print("🚀 Запуск демонстрации классификации в машинном обучении!")
    
    # 1. Генерируем и исследуем данные
    data = generate_sample_data()
    explore_data(data)
    
    # 2. Подготавливаем данные для ML
    X, y, feature_names = prepare_data_for_ml(data)
    
    # 3. Обучаем модели
    models, results, X_train, X_test, y_train, y_test, scaler, _ = train_classification_models(X, y, feature_names)
    
    # 4. Визуализируем результаты
    visualize_model_results(models, results, X_test, y_test, feature_names)
    
    # 5. Анализируем важность признаков
    analyze_feature_importance(models, feature_names)
    
    # 6. Визуализируем дерево решений
    visualize_decision_tree(models, feature_names)
    
    # 7. Кросс-валидация
    cross_validation_analysis(models, X, y)
    
    # 8. Бизнес-интерпретация
    business_interpretation(results, models, feature_names)
    
    # 9. Создаем функцию предсказания
    best_model_name = max(results.keys(), key=lambda x: results[x]['f1'])
    best_model = models[best_model_name][0]
    best_scaler = scaler if 'Логистическая' in best_model_name else None
    
    predict_func = create_prediction_function(best_model, best_scaler, feature_names)
    
    print(f"\n🎉 Демонстрация классификации завершена!")
    print("📚 Следующий шаг: изучите regression_models.py")
    print("💡 Совет: экспериментируйте с разными алгоритмами и гиперпараметрами!")
    
    return models, results, predict_func

if __name__ == "__main__":
    models, results, predict_function = main()