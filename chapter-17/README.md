# 🤖 Глава 17: Классификация и регрессия — машинное обучение с учителем!

## 🎯 Что вы изучите

После изучения этой главы вы сможете:

- 🧠 **Строить модели машинного обучения** для предсказания категорий и числовых значений
- 📊 **Использовать алгоритмы классификации** (логистическая регрессия, деревья решений, случайный лес)
- 📈 **Создавать регрессионные модели** для прогнозирования цен, продаж, доходов
- ⚖️ **Оценивать качество моделей** с помощью правильных метрик (accuracy, F1, MSE, R²)
- 🎯 **Настраивать гиперпараметры** и избегать переобучения
- 💼 **Применять ML в бизнесе** для автоматизации решений и прогнозов

## 🌟 Контролируемое обучение простыми словами

**Контролируемое обучение** — это как обучение ребенка по учебнику с ответами. У нас есть множество примеров с правильными ответами, и мы учим компьютер находить закономерности.

### 🎭 **Метафора: Машинное обучение как подготовка к экзамену**

Представьте, что вы готовите студента к экзамену:

- 📚 **Обучающие данные** — это учебник с примерами и ответами
- 🧠 **Модель** — это студент, который учится
- 🎯 **Алгоритм** — это метод обучения (зубрежка, понимание, практика)
- 📝 **Тестирование** — это пробный экзамен для проверки знаний
- ✅ **Предсказание** — это ответы на реальном экзамене
- 📊 **Метрики качества** — это оценка за экзамен

### 💼 **Зачем это нужно аналитику в 2025:**

**Классификация — предсказываем категории:**
```python
# Будет ли клиент покупать? (Да/Нет)
# Какая категория товара продается лучше? (A/B/C)
# Является ли email спамом? (Спам/Не спам)
```

**Регрессия — предсказываем числа:**
```python
# Какая будет цена на товар завтра?
# Сколько продаж ожидать в следующем месяце?
# Какой доход принесет клиент за год?
```

## 🧠 Основы контролируемого обучения

### 📊 **Типы задач машинного обучения**

#### 🎯 **Классификация — предсказание категорий**
- **Бинарная классификация:** Да/Нет, Спам/Не спам, Купит/Не купит
- **Многоклассовая:** Категория товара (A/B/C/D), Сегмент клиента, Источник трафика

#### 📈 **Регрессия — предсказание числовых значений**
- **Цены:** Стоимость недвижимости, курс акций
- **Количества:** Продажи, посетители, конверсия
- **Временные ряды:** Прогноз на будущие периоды

### 🎓 **Процесс машинного обучения**

```python
# 1. Подготовка данных
X = data[['возраст', 'доход', 'пол']]  # Признаки (features)
y = data['купит_товар']                # Целевая переменная (target)

# 2. Разделение на обучение и тест
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# 3. Обучение модели
from sklearn.linear_model import LogisticRegression
model = LogisticRegression()
model.fit(X_train, y_train)

# 4. Предсказания
predictions = model.predict(X_test)

# 5. Оценка качества
from sklearn.metrics import accuracy_score
accuracy = accuracy_score(y_test, predictions)
print(f"Точность модели: {accuracy:.2%}")
```

## 🎯 Классификация — предсказание категорий

### 🧮 **Логистическая регрессия — фундамент классификации**

**Принцип:** Вместо прямой линии строим S-образную кривую (сигмоиду), которая дает вероятности от 0 до 1.

```python
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

# Пример: Будет ли клиент покупать?
features = ['возраст', 'доход', 'количество_посещений']
X = customers[features]
y = customers['купил_товар']  # 0 или 1

# Обучаем модель
log_reg = LogisticRegression(random_state=42)
log_reg.fit(X_train, y_train)

# Получаем вероятности
probabilities = log_reg.predict_proba(X_test)[:, 1]  # Вероятность класса "1"
predictions = log_reg.predict(X_test)

print("📊 Результаты логистической регрессии:")
print(f"Точность: {accuracy_score(y_test, predictions):.2%}")
print("\nДетальный отчет:")
print(classification_report(y_test, predictions))
```

**⚖️ Преимущества:**
- 🚀 Быстрая и простая
- 📊 Дает вероятности, а не только классы  
- 🔍 Легко интерпретировать коэффициенты
- 📈 Хорошо работает с линейно разделимыми данными

**❌ Недостатки:**
- 📏 Предполагает линейную связь между признаками и логарифмом отношения шансов
- 🚫 Плохо работает с сильно нелинейными зависимостями
- 📊 Чувствительна к выбросам

### 🌳 **Деревья решений — понятная логика**

**Принцип:** Строим дерево вопросов типа "если-то", как блок-схему принятия решений.

```python
from sklearn.tree import DecisionTreeClassifier, plot_tree
import matplotlib.pyplot as plt

# Обучаем дерево решений
tree = DecisionTreeClassifier(
    max_depth=5,        # Максимальная глубина дерева
    min_samples_split=20,  # Минимум образцов для разбиения
    random_state=42
)

tree.fit(X_train, y_train)

# Визуализируем дерево
plt.figure(figsize=(20, 10))
plot_tree(tree, feature_names=features, 
          class_names=['Не купит', 'Купит'],
          filled=True, rounded=True)
plt.title('🌳 Дерево решений для предсказания покупок')
plt.show()

# Важность признаков
feature_importance = pd.DataFrame({
    'feature': features,
    'importance': tree.feature_importances_
}).sort_values('importance', ascending=False)

print("🎯 Важность признаков:")
print(feature_importance)
```

**⚖️ Преимущества:**
- 🧠 Очень легко интерпретировать
- 🔧 Не требует предобработки данных
- 🌿 Автоматически выбирает важные признаки
- 📊 Работает с любыми типами данных

**❌ Недостатки:**
- 🎲 Склонность к переобучению
- 🔄 Нестабильность (малые изменения данных → разные деревья)
- 📊 Может создавать слишком сложные правила

### 🌲 **Случайный лес — мудрость толпы**

**Принцип:** Строим много разных деревьев и усредняем их решения. Каждое дерево видит только часть данных и признаков.

```python
from sklearn.ensemble import RandomForestClassifier

# Создаем случайный лес
rf = RandomForestClassifier(
    n_estimators=100,     # Количество деревьев
    max_depth=10,         # Глубина каждого дерева
    min_samples_split=5,
    random_state=42,
    n_jobs=-1            # Используем все ядра процессора
)

rf.fit(X_train, y_train)

# Предсказания
rf_predictions = rf.predict(X_test)
rf_probabilities = rf.predict_proba(X_test)[:, 1]

print("🌲 Результаты случайного леса:")
print(f"Точность: {accuracy_score(y_test, rf_predictions):.2%}")

# Важность признаков (более надежная, чем у одного дерева)
feature_importance_rf = pd.DataFrame({
    'feature': features,
    'importance': rf.feature_importances_
}).sort_values('importance', ascending=False)

print("\n🎯 Важность признаков (Random Forest):")
print(feature_importance_rf)
```

**⚖️ Преимущества:**
- 🎯 Очень высокая точность
- 🛡️ Устойчивость к переобучению
- 📊 Надежная оценка важности признаков
- 🔧 Мало требует настройки гиперпараметров

**❌ Недостатки:**
- 📦 Менее интерпретируем, чем одно дерево
- 💻 Требует больше памяти и времени
- 🎯 Может переобучаться на очень зашумленных данных

## 📈 Регрессия — предсказание чисел

### 📏 **Линейная регрессия — основа прогнозирования**

**Принцип:** Ищем прямую линию, которая лучше всего проходит через облако точек.

```python
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

# Пример: Прогнозирование цены недвижимости
features = ['площадь', 'этаж', 'год_постройки', 'расстояние_до_центра']
X = houses[features]
y = houses['цена']

# Обучаем линейную регрессию
lin_reg = LinearRegression()
lin_reg.fit(X_train, y_train)

# Предсказания
predictions = lin_reg.predict(X_test)

# Оценка качества
mse = mean_squared_error(y_test, predictions)
r2 = r2_score(y_test, predictions)

print("📈 Результаты линейной регрессии:")
print(f"R² (коэффициент детерминации): {r2:.3f}")
print(f"Среднеквадратичная ошибка: {mse:,.0f}")
print(f"Средняя абсолютная ошибка: {np.mean(np.abs(y_test - predictions)):,.0f}")

# Коэффициенты модели
coefficients = pd.DataFrame({
    'feature': features,
    'coefficient': lin_reg.coef_,
    'abs_coefficient': np.abs(lin_reg.coef_)
}).sort_values('abs_coefficient', ascending=False)

print("\n📊 Влияние признаков на цену:")
for _, row in coefficients.iterrows():
    print(f"  {row['feature']}: {row['coefficient']:+,.0f} руб.")
```

**Интерпретация коэффициентов:**
- **Площадь: +50,000** → каждый кв.м добавляет 50,000 рублей к цене
- **Этаж: -2,000** → каждый этаж выше уменьшает цену на 2,000 рублей

### 🌊 **Полиномиальная регрессия — гибкие кривые**

**Принцип:** Создаем новые признаки как степени исходных (x², x³) для описания нелинейных зависимостей.

```python
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import Pipeline

# Создаем полиномиальную модель
poly_pipeline = Pipeline([
    ('poly', PolynomialFeatures(degree=2, include_bias=False)),
    ('linear', LinearRegression())
])

# Обучаем
poly_pipeline.fit(X_train, y_train)
poly_predictions = poly_pipeline.predict(X_test)

# Сравниваем с линейной моделью
poly_r2 = r2_score(y_test, poly_predictions)
print(f"📈 Линейная регрессия R²: {r2:.3f}")
print(f"🌊 Полиномиальная регрессия R²: {poly_r2:.3f}")

# Визуализация (для одного признака)
if len(features) == 1:
    plt.figure(figsize=(12, 6))
    
    # Исходные данные
    plt.scatter(X_test, y_test, alpha=0.6, label='Реальные данные')
    
    # Линейная модель
    plt.plot(X_test, predictions, 'r-', label='Линейная регрессия')
    
    # Полиномиальная модель
    sorted_idx = np.argsort(X_test.values.ravel())
    plt.plot(X_test.values.ravel()[sorted_idx], poly_predictions[sorted_idx], 
             'g-', label='Полиномиальная регрессия')
    
    plt.xlabel(features[0])
    plt.ylabel('Цена')
    plt.legend()
    plt.title('📊 Сравнение моделей регрессии')
    plt.show()
```

### 🌲 **Случайный лес для регрессии**

```python
from sklearn.ensemble import RandomForestRegressor

# Random Forest для регрессии
rf_reg = RandomForestRegressor(
    n_estimators=100,
    max_depth=15,
    min_samples_split=5,
    random_state=42
)

rf_reg.fit(X_train, y_train)
rf_predictions = rf_reg.predict(X_test)

rf_r2 = r2_score(y_test, rf_predictions)
rf_mse = mean_squared_error(y_test, rf_predictions)

print(f"🌲 Random Forest R²: {rf_r2:.3f}")
print(f"🌲 Random Forest MSE: {rf_mse:,.0f}")
```

## ⚖️ Оценка качества моделей

### 📊 **Метрики для классификации**

#### 🎯 **Основные метрики**

```python
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

# Матрица ошибок
conf_matrix = confusion_matrix(y_test, predictions)
print("🔍 Матрица ошибок:")
print(f"{'':>15} {'Предсказано':>20}")
print(f"{'Реально':>10} {'Не купит':>10} {'Купит':>10}")
print(f"{'Не купит':>10} {conf_matrix[0,0]:>10} {conf_matrix[0,1]:>10}")
print(f"{'Купит':>10} {conf_matrix[1,0]:>10} {conf_matrix[1,1]:>10}")

# Основные метрики
accuracy = accuracy_score(y_test, predictions)
precision = precision_score(y_test, predictions)
recall = recall_score(y_test, predictions)
f1 = f1_score(y_test, predictions)

print(f"\n📊 Метрики качества:")
print(f"  🎯 Accuracy (точность): {accuracy:.2%}")
print(f"  🔍 Precision (точность положительных): {precision:.2%}")
print(f"  📈 Recall (полнота): {recall:.2%}")
print(f"  ⚖️ F1-score (гармоническое среднее): {f1:.2%}")
```

**Когда что использовать:**

- **🎯 Accuracy** — общая точность, когда классы сбалансированы
- **🔍 Precision** — важно избежать ложных срабатываний (антиспам, медицинская диагностика)
- **📈 Recall** — важно найти все положительные случаи (поиск мошенничества)
- **⚖️ F1-score** — компромисс между precision и recall

#### 📈 **ROC-кривая и AUC**

```python
from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt

# Получаем вероятности вместо классов
y_proba = model.predict_proba(X_test)[:, 1]

# Строим ROC-кривую
fpr, tpr, thresholds = roc_curve(y_test, y_proba)
roc_auc = auc(fpr, tpr)

plt.figure(figsize=(10, 8))
plt.plot(fpr, tpr, color='darkorange', lw=2, 
         label=f'ROC кривая (AUC = {roc_auc:.2f})')
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('📈 ROC Кривая')
plt.legend(loc="lower right")
plt.show()

print(f"📊 AUC-ROC: {roc_auc:.3f}")
if roc_auc > 0.9:
    print("  🏆 Отличное качество!")
elif roc_auc > 0.8:
    print("  ✅ Хорошее качество")
elif roc_auc > 0.7:
    print("  📊 Приемлемое качество")
else:
    print("  ⚠️ Модель требует улучшения")
```

### 📈 **Метрики для регрессии**

```python
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# Основные метрики регрессии
mse = mean_squared_error(y_test, predictions)
mae = mean_absolute_error(y_test, predictions)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, predictions)

print(f"📊 Метрики качества регрессии:")
print(f"  📏 R² (коэффициент детерминации): {r2:.3f}")
print(f"  📊 MSE (среднеквадратичная ошибка): {mse:,.0f}")
print(f"  📈 RMSE (корень из MSE): {rmse:,.0f}")
print(f"  📉 MAE (средняя абсолютная ошибка): {mae:,.0f}")

# Интерпретация R²
if r2 > 0.9:
    print("  🏆 Отличная модель!")
elif r2 > 0.7:
    print("  ✅ Хорошая модель")
elif r2 > 0.5:
    print("  📊 Приемлемая модель")
else:
    print("  ⚠️ Модель объясняет мало дисперсии")

# Визуализация предсказаний vs реальных значений
plt.figure(figsize=(10, 8))
plt.scatter(y_test, predictions, alpha=0.6)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
plt.xlabel('Реальные значения')
plt.ylabel('Предсказанные значения')
plt.title(f'📊 Предсказания vs Реальность (R² = {r2:.3f})')
plt.show()
```

## 🔄 Кросс-валидация и настройка гиперпараметров

### 📊 **K-fold кросс-валидация**

**Проблема:** Если тестировать модель только на одном разбиении данных, результат может быть случайным.

**Решение:** Разделяем данные на K частей, обучаемся на K-1 частях, тестируем на оставшейся. Повторяем K раз.

```python
from sklearn.model_selection import cross_val_score, StratifiedKFold

# K-fold кросс-валидация
cv_scores = cross_val_score(
    model, X, y, 
    cv=5,           # 5-fold
    scoring='accuracy'
)

print(f"📊 Результаты кросс-валидации:")
print(f"  Точность по фолдам: {cv_scores}")
print(f"  Средняя точность: {cv_scores.mean():.3f} ± {cv_scores.std():.3f}")
```

### 🔧 **Подбор гиперпараметров**

```python
from sklearn.model_selection import GridSearchCV

# Определяем сетку гиперпараметров для Random Forest
param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [5, 10, 15, None],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

# Поиск по сетке с кросс-валидацией
grid_search = GridSearchCV(
    RandomForestClassifier(random_state=42),
    param_grid,
    cv=5,
    scoring='f1',
    n_jobs=-1,
    verbose=1
)

print("🔧 Поиск оптимальных гиперпараметров...")
grid_search.fit(X_train, y_train)

print(f"✅ Лучшие параметры: {grid_search.best_params_}")
print(f"📊 Лучшее качество: {grid_search.best_score_:.3f}")

# Используем лучшую модель
best_model = grid_search.best_estimator_
```

## 📊 Обработка признаков (Feature Engineering)

### 🔧 **Подготовка данных**

```python
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# Пример данных
data = pd.DataFrame({
    'возраст': [25, 35, 45, 55],
    'доход': [30000, 80000, 120000, 60000],
    'город': ['Москва', 'СПб', 'Москва', 'Казань'],
    'образование': ['Высшее', 'Среднее', 'Высшее', 'Среднее']
})

# Разделяем на числовые и категориальные признаки
numeric_features = ['возраст', 'доход']
categorical_features = ['город', 'образование']

# Создаем препроцессор
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numeric_features),
        ('cat', OneHotEncoder(drop='first', sparse=False), categorical_features)
    ]
)

# Создаем полный пайплайн
pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('classifier', LogisticRegression())
])

# Теперь можем обучать сразу на сырых данных
pipeline.fit(X_train, y_train)
predictions = pipeline.predict(X_test)
```

### 🎯 **Создание новых признаков**

```python
def create_features(data):
    """Создание новых признаков для улучшения модели"""
    
    # Копируем исходные данные
    features = data.copy()
    
    # Взаимодействия признаков
    features['доход_на_возраст'] = features['доход'] / features['возраст']
    
    # Группировки
    features['возрастная_группа'] = pd.cut(
        features['возраст'], 
        bins=[0, 30, 50, 100], 
        labels=['Молодые', 'Средние', 'Зрелые']
    )
    
    # Логарифмы для скошенных распределений
    features['log_доход'] = np.log1p(features['доход'])
    
    # Категориальные признаки из числовых
    features['высокий_доход'] = (features['доход'] > features['доход'].median()).astype(int)
    
    # Временные признаки (если есть даты)
    if 'дата_регистрации' in features.columns:
        features['дата_регистрации'] = pd.to_datetime(features['дата_регистрации'])
        features['дни_с_регистрации'] = (datetime.now() - features['дата_регистрации']).dt.days
        features['месяц_регистрации'] = features['дата_регистрации'].dt.month
        features['день_недели_регистрации'] = features['дата_регистрации'].dt.dayofweek
    
    return features

# Применяем feature engineering
X_enhanced = create_features(X)
print(f"🎯 Создано {len(X_enhanced.columns)} признаков из {len(X.columns)}")
```

## 💼 Бизнес-применения машинного обучения

### 🛒 **Предсказание покупок (классификация)**

```python
# Модель для предсказания покупок
def build_purchase_prediction_model(customer_data):
    """
    Строит модель для предсказания вероятности покупки
    """
    
    # Подготовка данных
    features = [
        'возраст', 'доход', 'пол_encoded', 'город_encoded',
        'дни_с_последней_покупки', 'количество_прошлых_покупок',
        'средний_чек', 'любимая_категория_encoded'
    ]
    
    X = customer_data[features]
    y = customer_data['купит_в_следующем_месяце']
    
    # Разделение данных
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Обучение модели
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Оценка качества
    predictions = model.predict(X_test)
    probabilities = model.predict_proba(X_test)[:, 1]
    
    print("🛒 Модель предсказания покупок:")
    print(f"  🎯 Точность: {accuracy_score(y_test, predictions):.2%}")
    print(f"  📊 F1-score: {f1_score(y_test, predictions):.3f}")
    
    # Важность признаков
    feature_importance = pd.DataFrame({
        'feature': features,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print(f"\n🎯 Важность признаков:")
    for _, row in feature_importance.head().iterrows():
        print(f"  {row['feature']}: {row['importance']:.3f}")
    
    return model, feature_importance

# Применение для маркетинга
def create_marketing_campaign(model, customers, campaign_budget=100000):
    """
    Создает персонализированную маркетинговую кампанию
    """
    
    # Предсказываем вероятности покупки
    probabilities = model.predict_proba(customers[features])[:, 1]
    
    # Добавляем к данным клиентов
    customers_with_proba = customers.copy()
    customers_with_proba['вероятность_покупки'] = probabilities
    
    # Сортируем по убыванию вероятности
    customers_with_proba = customers_with_proba.sort_values('вероятность_покупки', ascending=False)
    
    # Расчет ROI для каждого клиента
    customers_with_proba['ожидаемая_прибыль'] = (
        customers_with_proba['вероятность_покупки'] * 
        customers_with_proba['средний_чек'] * 0.2  # 20% маржа
    )
    
    # Стоимость маркетингового контакта
    cost_per_contact = 50
    customers_with_proba['roi'] = (
        customers_with_proba['ожидаемая_прибыль'] / cost_per_contact
    )
    
    # Выбираем клиентов с ROI > 1
    profitable_customers = customers_with_proba[customers_with_proba['roi'] > 1]
    
    # Учитываем бюджет
    num_contacts = min(len(profitable_customers), campaign_budget // cost_per_contact)
    campaign_customers = profitable_customers.head(num_contacts)
    
    print(f"📈 Рекомендации для кампании:")
    print(f"  🎯 Связаться с {num_contacts:,} клиентами")
    print(f"  💰 Бюджет: {num_contacts * cost_per_contact:,} руб.")
    print(f"  📊 Ожидаемый доход: {campaign_customers['ожидаемая_прибыль'].sum():,.0f} руб.")
    print(f"  🚀 Ожидаемый ROI: {campaign_customers['ожидаемая_прибыль'].sum() / (num_contacts * cost_per_contact):.1f}x")
    
    return campaign_customers
```

### 📈 **Прогнозирование продаж (регрессия)**

```python
def build_sales_forecasting_model(sales_data):
    """
    Строит модель для прогнозирования продаж
    """
    
    # Feature engineering для временных рядов
    sales_data['дата'] = pd.to_datetime(sales_data['дата'])
    sales_data['год'] = sales_data['дата'].dt.year
    sales_data['месяц'] = sales_data['дата'].dt.month
    sales_data['день_недели'] = sales_data['дата'].dt.dayofweek
    sales_data['квартал'] = sales_data['дата'].dt.quarter
    sales_data['день_года'] = sales_data['дата'].dt.dayofyear
    
    # Скользящие средние для тренда
    sales_data['продажи_7дней'] = sales_data['продажи'].rolling(7).mean()
    sales_data['продажи_30дней'] = sales_data['продажи'].rolling(30).mean()
    
    # Лаги (продажи в прошлые периоды)
    sales_data['продажи_вчера'] = sales_data['продажи'].shift(1)
    sales_data['продажи_неделю_назад'] = sales_data['продажи'].shift(7)
    
    # Удаляем строки с NaN после создания лагов
    sales_data = sales_data.dropna()
    
    features = [
        'месяц', 'день_недели', 'квартал', 'день_года',
        'продажи_7дней', 'продажи_30дней', 
        'продажи_вчера', 'продажи_неделю_назад',
        'цена', 'маркетинговые_расходы', 'количество_конкурентов'
    ]
    
    X = sales_data[features]
    y = sales_data['продажи']
    
    # Разделение по времени (важно для временных рядов!)
    split_date = sales_data['дата'].quantile(0.8)
    train_mask = sales_data['дата'] <= split_date
    
    X_train, X_test = X[train_mask], X[~train_mask]
    y_train, y_test = y[train_mask], y[~train_mask]
    
    # Обучение модели
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Предсказания
    predictions = model.predict(X_test)
    
    # Оценка качества
    r2 = r2_score(y_test, predictions)
    mae = mean_absolute_error(y_test, predictions)
    
    print("📈 Модель прогнозирования продаж:")
    print(f"  📊 R² коэффициент: {r2:.3f}")
    print(f"  📏 Средняя ошибка: {mae:,.0f} единиц")
    print(f"  📈 Средняя ошибка в %: {(mae / y_test.mean()) * 100:.1f}%")
    
    return model, features
```

## ⚠️ Важные моменты и частые ошибки

### ❌ **Частые ошибки новичков:**

1. **🔍 Утечка данных (Data Leakage)**
   ```python
   # ❌ Неправильно - используем будущую информацию
   data['средний_чек_за_год'] = data.groupby('клиент_id')['чек'].transform('mean')
   
   # ✅ Правильно - используем только прошлую информацию
   data['средний_чек_до_даты'] = data.groupby('клиент_id')['чек'].expanding().mean()
   ```

2. **📊 Неправильное разделение данных**
   ```python
   # ❌ Неправильно - для временных рядов
   train_test_split(X, y, test_size=0.2, random_state=42)
   
   # ✅ Правильно - хронологическое разделение
   split_date = data['дата'].quantile(0.8)
   train_data = data[data['дата'] <= split_date]
   test_data = data[data['дата'] > split_date]
   ```

3. **🎯 Неправильная метрика для несбалансированных классов**
   ```python
   # ❌ Если 95% клиентов не покупают, accuracy = 95% ничего не значит
   print(f"Accuracy: {accuracy_score(y_test, predictions)}")
   
   # ✅ Используем F1-score или AUC-ROC
   print(f"F1-score: {f1_score(y_test, predictions)}")
   print(f"AUC-ROC: {roc_auc_score(y_test, probabilities)}")
   ```

### 💡 **Лучшие практики:**

1. **🔍 Всегда анализируйте данные перед моделированием**
2. **📊 Используйте кросс-валидацию для надежной оценки**
3. **🎯 Выбирайте метрики в соответствии с бизнес-задачей**
4. **🔧 Создавайте pipeline для воспроизводимости**
5. **📈 Мониторьте производительность модели в production**
6. **💼 Всегда интерпретируйте результаты с бизнес-точки зрения**

## 🚀 Готовые шаблоны для копирования

### 🎯 **Полный пайплайн классификации**

```python
def classification_pipeline(data, target_column, test_size=0.2):
    """
    Полный пайплайн для задач классификации
    """
    from sklearn.model_selection import train_test_split
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.metrics import classification_report, confusion_matrix
    from sklearn.model_selection import cross_val_score
    
    # Подготовка данных
    X = data.drop(columns=[target_column])
    y = data[target_column]
    
    # Разделение
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=42, stratify=y
    )
    
    # Модель
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    
    # Обучение
    model.fit(X_train, y_train)
    
    # Предсказания
    predictions = model.predict(X_test)
    probabilities = model.predict_proba(X_test)[:, 1]
    
    # Оценка
    print("📊 Результаты классификации:")
    print(classification_report(y_test, predictions))
    
    # Кросс-валидация
    cv_scores = cross_val_score(model, X, y, cv=5, scoring='f1')
    print(f"\n🔄 Кросс-валидация F1: {cv_scores.mean():.3f} ± {cv_scores.std():.3f}")
    
    return model, X_test, y_test, predictions, probabilities

# Использование
model, X_test, y_test, pred, proba = classification_pipeline(data, 'купит_товар')
```

### 📈 **Полный пайплайн регрессии**

```python
def regression_pipeline(data, target_column, test_size=0.2):
    """
    Полный пайплайн для задач регрессии
    """
    from sklearn.model_selection import train_test_split
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
    
    # Подготовка данных
    X = data.drop(columns=[target_column])
    y = data[target_column]
    
    # Разделение
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=42
    )
    
    # Модель
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    
    # Обучение
    model.fit(X_train, y_train)
    
    # Предсказания
    predictions = model.predict(X_test)
    
    # Оценка
    r2 = r2_score(y_test, predictions)
    mse = mean_squared_error(y_test, predictions)
    mae = mean_absolute_error(y_test, predictions)
    
    print("📈 Результаты регрессии:")
    print(f"  R² коэффициент: {r2:.3f}")
    print(f"  MSE: {mse:,.0f}")
    print(f"  MAE: {mae:,.0f}")
    print(f"  RMSE: {np.sqrt(mse):,.0f}")
    
    return model, X_test, y_test, predictions

# Использование  
model, X_test, y_test, predictions = regression_pipeline(data, 'цена')
```

## 🚀 Что дальше?

После освоения этой главы вы умеете:

✅ **Строить модели классификации** для предсказания категорий  
✅ **Создавать регрессионные модели** для прогнозирования числовых значений  
✅ **Оценивать качество моделей** с помощью правильных метрик  
✅ **Избегать переобучения** с помощью кросс-валидации  
✅ **Применять ML в бизнесе** для автоматизации решений

**Следующий шаг:** Изучить продвинутые техники машинного обучения и deep learning!

## 🛠 Инструкции

Теперь переходите к практическим заданиям — вас ждут 5 проектов по созданию реальных ML-моделей:

- 📝 [Перейти к практическим заданиям](practice.md)
- ✅ [Перейти к чек-листу](checklist.md)
- 📁 [Посмотреть учебные файлы](files/README.md)

---

- 🔙 [Предыдущая глава: Глава 16 - Кластеризация и сегментация](../chapter-16/README.md)
- 🔜 [Следующая глава: Глава 18 - Продвинутые техники машинного обучения](../chapter-18/README.md)

---

- 📢 Присоединяйтесь к чату курса: https://t.me/analytics_course_chat
- 📢 Канал курса: https://t.me/analytics_course_channel