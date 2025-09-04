# 📁 Учебные файлы для главы 17

Эта папка содержит все необходимые материалы для освоения контролируемого машинного обучения — классификации и регрессии.

## 🎯 Содержимое папки

### 📊 Файлы с данными

#### 🛒 `customer_purchase_prediction.csv` (428 KB)
**Назначение:** Данные для бинарной классификации (будет ли клиент покупать?)  
**Размер:** 5,000 записей клиентов интернет-магазина  
**Содержимое:**
- `customer_id` — уникальный ID клиента
- `age` — возраст клиента (18-75 лет)
- `income` — годовой доход (тыс. руб.)
- `gender` — пол (M/F)
- `city_tier` — тип города (1-метрополии, 2-крупные, 3-малые)
- `days_since_registration` — дней с регистрации
- `total_sessions` — общее количество сессий на сайте
- `avg_session_duration` — средняя длительность сессии (мин)
- `pages_per_session` — среднее количество страниц за сессию
- `total_spent_history` — общая потраченная сумма за все время (руб.)
- `number_of_purchases` — количество прошлых покупок
- `avg_order_value` — средний чек (руб.)
- `days_since_last_purchase` — дней с последней покупки
- `favorite_category` — предпочитаемая категория товаров
- `device_type` — тип устройства (Desktop/Mobile/Tablet)
- `email_subscriber` — подписан на рассылку (True/False)
- `social_media_follower` — подписан в соцсетях (True/False)
- `loyalty_program_member` — участник программы лояльности (True/False)
- `customer_support_interactions` — количество обращений в поддержку
- `product_views_last_month` — просмотры товаров за последний месяц
- `cart_abandonment_rate` — процент брошенных корзин
- `will_purchase` — **ЦЕЛЕВАЯ ПЕРЕМЕННАЯ** (1-купит, 0-не купит)

**Особенности данных:**
- 30% клиентов совершат покупку (сбалансированный dataset)
- Реалистичные корреляции между поведенческими признаками
- Включены как числовые, так и категориальные признаки
- Есть пропуски в некоторых столбцах для отработки их обработки

**Использование:** 
- Задание 1: Основы бинарной классификации
- Сравнение Logistic Regression, Decision Tree, Random Forest
- Feature engineering и создание новых признаков

#### 🏠 `real_estate_prices.csv` (356 KB)
**Назначение:** Данные для регрессионного анализа (прогноз цен на недвижимость)  
**Размер:** 3,000 записей квартир в разных городах  
**Содержимое:**
- `property_id` — уникальный ID объекта недвижимости
- `city` — город (Москва, СПб, Новосибирск, Екатеринбург, Казань)
- `district` — район города
- `property_type` — тип жилья (Новостройка, Вторичка, Элитное)
- `total_area` — общая площадь (кв.м)
- `living_area` — жилая площадь (кв.м)
- `kitchen_area` — площадь кухни (кв.м)
- `rooms` — количество комнат
- `floor` — этаж
- `total_floors` — этажность дома
- `year_built` — год постройки
- `renovation_type` — тип ремонта (Без ремонта, Косметический, Евроремонт)
- `balcony` — наличие балкона/лоджии (True/False)
- `parking` — наличие парковки (True/False)  
- `metro_distance` — расстояние до метро (км, NaN если нет метро)
- `center_distance` — расстояние до центра города (км)
- `school_rating` — рейтинг ближайшей школы (1-10)
- `hospital_distance` — расстояние до больницы (км)
- `shopping_mall_distance` — расстояние до торгового центра (км)
- `park_distance` — расстояние до парка (км)
- `crime_rate` — индекс преступности в районе (1-10)
- `air_quality_index` — индекс качества воздуха (1-10)
- `noise_level` — уровень шума (1-10)
- `price` — **ЦЕЛЕВАЯ ПЕРЕМЕННАЯ** цена в рублях

**Особенности данных:**
- Цены от 2 млн до 50 млн рублей
- Реалистичные зависимости: площадь-цена, район-цена, год постройки-цена
- Различные ценовые категории по городам
- Выбросы в ценах для отработки их обнаружения

**Использование:**
- Задание 2: Линейная и полиномиальная регрессия  
- Feature engineering для недвижимости
- Сравнение различных регрессионных моделей

#### 🏦 `bank_customer_segmentation.csv` (892 KB)
**Назначение:** Данные для многоклассовой классификации (сегментация банковских клиентов)  
**Размер:** 8,000 записей клиентов банка  
**Содержимое:**
- `customer_id` — уникальный ID клиента
- `age` — возраст клиента
- `gender` — пол (M/F)
- `income` — месячный доход (руб.)
- `education_level` — уровень образования (School/Bachelor/Master/PhD)
- `marital_status` — семейное положение (Single/Married/Divorced)
- `children_count` — количество детей
- `employment_type` — тип занятости (Employee/Self-employed/Unemployed/Retired)
- `city_type` — тип города (Metropolitan/Urban/Rural)
- `account_balance` — баланс основного счета (руб.)
- `savings_balance` — баланс сберегательного счета (руб.) 
- `credit_card_balance` — задолженность по кредитной карте (руб.)
- `loan_amount` — сумма действующих кредитов (руб.)
- `mortgage_amount` — сумма ипотечного кредита (руб.)
- `investment_portfolio_value` — стоимость инвестиционного портфеля (руб.)
- `monthly_transactions` — количество транзакций в месяц
- `avg_transaction_amount` — средняя сумма транзакции (руб.)
- `atm_usage_frequency` — частота использования банкоматов в месяц
- `online_banking_usage` — использование онлайн банкинга (True/False)
- `mobile_app_rating` — оценка мобильного приложения (1-5)
- `customer_service_calls` — количество звонков в службу поддержки за год
- `years_with_bank` — количество лет работы с банком
- `products_count` — количество банковских продуктов
- `credit_score` — кредитный рейтинг (300-850)
- `default_history` — история просрочек (True/False)
- `segment` — **ЦЕЛЕВАЯ ПЕРЕМЕННАЯ** (Premium/Standard/Basic/Problem)

**Особенности данных:**
- 4 класса с неравномерным распределением (Premium 15%, Problem 20%)
- Сложные финансовые взаимосвязи между признаками
- Реалистичные банковские продукты и поведение клиентов

**Использование:**
- Задание 3: Многоклассовая классификация
- Работа с несбалансированными классами
- Создание финансовых индикаторов

#### 📱 `customer_churn_dataset.csv` (1.2 MB)
**Назначение:** Данные для сравнения алгоритмов ML (предсказание оттока)  
**Размер:** 10,000 записей клиентов телеком-компании  
**Содержимое:**
- `customer_id` — ID клиента
- `gender` — пол
- `senior_citizen` — пенсионер (0/1)
- `partner` — наличие партнера (Yes/No)
- `dependents` — наличие иждивенцев (Yes/No)
- `tenure` — период пользования услугами (месяцы)
- `phone_service` — услуга телефонии (Yes/No)
- `multiple_lines` — несколько линий (Yes/No/No phone service)
- `internet_service` — интернет-сервис (DSL/Fiber optic/No)
- `online_security` — онлайн-безопасность (Yes/No/No internet service)
- `online_backup` — онлайн-резервное копирование (Yes/No/No internet service)
- `device_protection` — защита устройства (Yes/No/No internet service)
- `tech_support` — техническая поддержка (Yes/No/No internet service)
- `streaming_tv` — потоковое ТВ (Yes/No/No internet service)
- `streaming_movies` — потоковые фильмы (Yes/No/No internet service)
- `contract` — тип контракта (Month-to-month/One year/Two year)
- `paperless_billing` — электронные счета (Yes/No)
- `payment_method` — способ оплаты (Electronic check/Mailed check/Bank transfer/Credit card)
- `monthly_charges` — ежемесячная плата (USD)
- `total_charges` — общая плата за все время (USD)
- `churn` — **ЦЕЛЕВАЯ ПЕРЕМЕННАЯ** отток клиента (Yes/No)

**Использование:**
- Задание 4: Систематическое сравнение алгоритмов
- Оптимизация гиперпараметров
- Cost-sensitive learning

### 🏪 Файлы для end-to-end проекта (Задание 5)

#### `product_catalog.csv` (234 KB) - каталог товаров
**Содержимое:** product_id, category, subcategory, brand, base_price, cost, margin, seasonality_factor, launch_date

#### `sales_history.csv` (1.8 MB) - история продаж
**Содержимое:** date, product_id, quantity_sold, price, discount, channel, region, weather, competitor_action

#### `competitor_prices.csv` (456 KB) - цены конкурентов  
**Содержимое:** date, product_id, competitor_name, competitor_price, availability, rating

#### `market_trends.csv` (123 KB) - рыночные тренды
**Содержимое:** date, category, search_volume, social_sentiment, economic_index, seasonal_trend

#### `inventory_data.csv` (345 KB) - данные о запасах
**Содержимое:** date, product_id, stock_level, warehouse_cost, holding_cost, stockout_risk

### 🐍 Python скрипты

#### 🎯 `classification_basics.py` (18.6 KB)
**Назначение:** Введение в классификацию с базовыми алгоритмами  
**Содержимое:**
- Демонстрация логистической регрессии, деревьев решений, Random Forest
- Сравнение алгоритмов на одних данных
- Визуализация decision boundaries
- Интерпретация feature importance
- ROC-кривые и confusion matrix

```python
# Основные функции
def compare_classification_algorithms(X, y):
    """Сравнивает основные алгоритмы классификации"""
    
def plot_decision_boundaries(X, y, models):
    """Визуализирует границы решения алгоритмов"""
    
def analyze_feature_importance(model, feature_names):
    """Анализирует важность признаков"""
    
def plot_roc_curves(models, X_test, y_test):
    """Строит ROC-кривые для сравнения моделей"""
```

#### 📈 `regression_models.py` (16.2 KB)
**Назначение:** Полный гид по регрессионным моделям  
**Содержимое:**
- Линейная регрессия с интерпретацией коэффициентов
- Полиномиальная регрессия разных степеней
- Регуляризация (Ridge, Lasso, ElasticNet)
- Random Forest для регрессии
- Анализ остатков и диагностика моделей

```python
# Основные функции  
def linear_regression_analysis(X, y, feature_names):
    """Полный анализ линейной регрессии"""
    
def polynomial_regression_comparison(X, y, degrees=[1,2,3]):
    """Сравнение полиномиальной регрессии разных степеней"""
    
def regularized_regression_comparison(X, y):
    """Сравнение Ridge, Lasso, ElasticNet"""
    
def analyze_residuals(model, X_test, y_test, y_pred):
    """Анализ остатков регрессионной модели"""
```

#### ⚖️ `model_evaluation.py` (14.8 KB)
**Назначение:** Комплексная система оценки качества моделей  
**Содержимое:**
- Все метрики классификации и регрессии
- Кросс-валидация с различными стратегиями
- Статистическое сравнение моделей
- Calibration analysis
- Business impact calculation

```python
def comprehensive_classification_evaluation(model, X, y):
    """Комплексная оценка модели классификации"""
    
def comprehensive_regression_evaluation(model, X, y):
    """Комплексная оценка регрессионной модели"""
    
def statistical_model_comparison(models, X, y, cv=5):
    """Статистически значимое сравнение моделей"""
    
def calibration_analysis(model, X_test, y_test):
    """Анализ калибровки вероятностей"""
```

#### 🔧 `feature_engineering.py` (22.1 KB)
**Назначение:** Продвинутые техники создания признаков  
**Содержимое:**
- Автоматическое создание признаков
- Обработка категориальных переменных  
- Работа с временными рядами
- Polynomial features и взаимодействия
- Feature selection методы

```python
def create_polynomial_features(X, degree=2, interaction_only=False):
    """Создание полиномиальных признаков"""
    
def encode_categorical_features(data, categorical_columns):
    """Кодирование категориальных признаков"""
    
def create_time_features(data, date_column):
    """Создание признаков из временных данных"""
    
def automatic_feature_engineering(data, target_column):
    """Автоматическое создание признаков"""
```

#### 🚀 `production_pipeline.py` (26.4 KB)
**Назначение:** Production-ready ML пайплайн  
**Содержимое:**
- Класс MLPipeline для end-to-end обучения
- Автоматическая валидация данных
- Model versioning и эксперименты
- Batch prediction система
- A/B тестирование framework

```python
class MLPipeline:
    """Production-ready ML pipeline"""
    
    def __init__(self, task_type='classification'):
        self.task_type = task_type
        self.models = {}
        self.best_model = None
        self.preprocessor = None
        self.experiment_log = []
    
    def fit(self, data, target_column):
        """Полный пайплайн обучения"""
        
    def predict(self, new_data):
        """Предсказание для новых данных"""
        
    def evaluate(self, test_data=None):
        """Оценка качества моделей"""
        
    def deploy(self, model_name=None):
        """Деплой лучшей модели"""
```

#### 🏆 `hyperparameter_optimization.py` (19.7 KB)
**Назначение:** Оптимизация гиперпараметров и AutoML  
**Содержимое:**
- Grid Search и Random Search
- Bayesian optimization (Optuna)
- Автоматический feature selection
- Multi-objective optimization
- Automated model selection

```python
def hyperparameter_optimization(X, y, model_type='random_forest'):
    """Оптимизация гиперпараметров различными методами"""
    
def automated_model_selection(X, y, task_type='classification'):
    """Автоматический выбор лучшей модели"""
    
def multi_objective_optimization(X, y, objectives=['accuracy', 'speed']):
    """Многокритериальная оптимизация"""
```

## 🚀 Как использовать файлы

### 📋 Последовательность работы:

1. **🎯 Начните с теории** — прочитайте README.md главы 17
2. **🐍 Изучите базовые алгоритмы** — запустите `classification_basics.py`
3. **📈 Освойте регрессию** — изучите `regression_models.py`
4. **💻 Переходите к практике** — откройте practice.md
5. **📁 Используйте данные по заданиям:**
   - Задание 1: `customer_purchase_prediction.csv` + `classification_basics.py`
   - Задание 2: `real_estate_prices.csv` + `regression_models.py`
   - Задание 3: `bank_customer_segmentation.csv` + `model_evaluation.py`
   - Задание 4: `customer_churn_dataset.csv` + `hyperparameter_optimization.py`
   - Задание 5: все файлы для end-to-end + `production_pipeline.py`

### 💡 Советы по работе:

**🔧 Для установки зависимостей:**
```bash
# Основные библиотеки для ML
pip install scikit-learn pandas numpy matplotlib seaborn

# Для продвинутой оптимизации
pip install optuna xgboost lightgbm

# Для интерпретируемости моделей
pip install shap lime

# Для работы с imbalanced данными
pip install imbalanced-learn

# Для статистических тестов
pip install scipy statsmodels
```

**📂 Структура рабочей папки:**
```
chapter-17/
├── files/              # ← эта папка
│   ├── customer_purchase_prediction.csv
│   ├── real_estate_prices.csv
│   ├── bank_customer_segmentation.csv
│   ├── customer_churn_dataset.csv
│   ├── product_catalog.csv
│   ├── sales_history.csv
│   ├── competitor_prices.csv
│   ├── market_trends.csv
│   ├── inventory_data.csv
│   ├── classification_basics.py
│   ├── regression_models.py
│   ├── model_evaluation.py
│   ├── feature_engineering.py
│   ├── production_pipeline.py
│   └── hyperparameter_optimization.py
├── README.md           # теория
├── practice.md         # задания
└── checklist.md        # самопроверка
```

**🎨 Настройка окружения:**
```python
# В начале каждого скрипта
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, f1_score, mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
import warnings

# Настройка отображения
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 11
sns.set_style("whitegrid")
warnings.filterwarnings('ignore')

# Фиксация случайности
RANDOM_STATE = 42
np.random.seed(RANDOM_STATE)
```

## ⚠️ Важные заметки

### 🎯 О данных:
- Все датасеты созданы специально для обучения с реалистичными закономерностями
- CSV файлы в кодировке UTF-8 с разделителем ","
- Целевые переменные четко обозначены в описании
- Включены различные типы признаков: числовые, категориальные, временные
- Данные содержат типичные проблемы: пропуски, выбросы, несбалансированные классы

### 🔐 Безопасность:
- Все данные полностью синтетические и анонимные
- Нет никакой персональной информации реальных людей
- Безопасно для использования в учебных и коммерческих проектах
- Данные созданы с учетом GDPR требований

### 🚀 Производительность:
- Размеры данных оптимизированы для обучения (3K-10K записей)
- Все алгоритмы выполняются за разумное время (<5 мин)
- Включены техники для работы с большими данными
- Оптимизированные hyperparameter ranges

### 📊 Особенности датасетов:

#### **customer_purchase_prediction.csv:**
- Сбалансированный dataset (30% положительных случаев)
- Реалистичное поведение e-commerce клиентов
- Сложные нелинейные зависимости между признаками
- Подходит для демонстрации всех основных алгоритмов классификации

#### **real_estate_prices.csv:**
- Широкий диапазон цен для демонстрации log-трансформации
- Географические особенности российского рынка недвижимости
- Сезонные и экономические факторы
- Подходит для линейной и нелинейной регрессии

#### **bank_customer_segmentation.csv:**
- Реалистичные банковские продукты и метрики
- Несбалансированные классы для изучения специальных техник
- Сложные финансовые взаимосвязи
- Подходит для многоклассовой классификации

#### **customer_churn_dataset.csv:**
- Классический dataset для churn prediction
- Множество категориальных признаков
- Подходит для сравнения большого количества алгоритмов
- Benchmark для testing различных техник

#### **End-to-end проект файлы:**
- Имитируют реальную production среду
- Множественные источники данных
- Временные зависимости
- Бизнес-ограничения и метрики

## 🆘 Помощь и решение проблем

**Если модели показывают плохие результаты:**
```python
# Проверьте распределение целевой переменной
print(data['target'].value_counts())
print(data['target'].value_counts(normalize=True))

# Проверьте корреляции с целевой переменной
correlations = data.corr()['target'].abs().sort_values(ascending=False)
print("Топ корреляций с target:")
print(correlations.head(10))

# Проверьте на data leakage
from datetime import datetime
# Убедитесь, что не используете будущую информацию
```

**Если есть проблемы с производительностью:**
```python
# Для больших данных используйте sampling
sample_size = min(10000, len(data))
data_sample = data.sample(n=sample_size, random_state=42)

# Используйте параллельную обработку
from sklearn.ensemble import RandomForestClassifier
rf = RandomForestClassifier(n_jobs=-1)

# Оптимизируйте память
import gc
gc.collect()
```

**Если results нестабильны:**
```python
# Всегда фиксируйте random_state
train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Используйте кросс-валидацию
scores = cross_val_score(model, X, y, cv=5, random_state=42)
print(f"CV Score: {scores.mean():.3f} ± {scores.std():.3f}")

# Проверьте размер данных
if len(data) < 1000:
    print("⚠️ Маленький dataset - результаты могут быть нестабильными")
```

**💪 Готовы предсказывать будущее с помощью машинного обучения? Начинайте с практических заданий!**

---

📖 [Вернуться к теории](../README.md) | 📝 [Перейти к практике](../practice.md) | ✅ [Перейти к чек-листу](../checklist.md)

---

- 🔙 [Предыдущая глава: Глава 16 - Кластеризация и сегментация](../chapter-16/README.md)
- 🔜 [Следующая глава: Глава 18 - Продвинутые техники машинного обучения](../chapter-18/README.md)

---

- 📢 Присоединяйтесь к чату курса: https://t.me/analytics_course_chat
- 📢 Канал курса: https://t.me/analytics_course_channel