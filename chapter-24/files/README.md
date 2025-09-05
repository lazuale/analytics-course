# 📁 Учебные материалы — Глава 24: Мультивариантный анализ

## 📋 Обзор содержимого папки

В этой папке собраны все файлы, необходимые для выполнения практических заданий по мультивариантному анализу: PCA и факторному анализу.

---

## 📊 Датасеты (CSV файлы)

### 🛒 `customers_data.csv` — Данные о клиентах интернет-магазина
**Описание**: Поведенческие данные 1000 клиентов для анализа PCA  
**Размер**: 1000 строк × 13 столбцов  
**Разделитель**: `;` (точка с запятой)  
**Десятичные дроби**: `,` (запятая)

**Структура данных**:
- `customer_id` — уникальный ID клиента
- `monthly_spending` — ежемесячные траты (рубли)
- `orders_count` — количество заказов в месяц
- `avg_order_value` — средний чек (рубли)
- `session_duration` — среднее время сессии (минуты)
- `page_views` — среднее количество просмотренных страниц
- `return_rate` — доля возвратов (от 0 до 1)
- `review_rating` — средняя оценка товаров (1-5)
- `mobile_usage` — доля мобильного трафика (от 0 до 1)
- `weekend_shopping` — доля покупок в выходные (от 0 до 1)
- `loyalty_years` — количество лет лояльности
- `support_tickets` — количество обращений в поддержку в месяц
- `referrals_made` — количество рефералов в месяц

**Применение**: Задание 1 (PCA анализ), Задание 3 (визуализация)

---

### 👥 `employee_satisfaction.csv` — Опрос удовлетворенности сотрудников
**Описание**: Результаты опроса 500 сотрудников по 15 аспектам работы  
**Размер**: 500 строк × 16 столбцов  
**Разделитель**: `;` (точка с запятой)  
**Десятичные дроби**: `,` (запятая)  
**Шкала оценок**: 1-7 (1 = совершенно не согласен, 7 = полностью согласен)

**Структура данных**:
- `employee_id` — уникальный ID сотрудника  
- `salary_satisfaction` — удовлетворенность зарплатой
- `bonus_fairness` — справедливость бонусной системы
- `workload_balance` — баланс рабочей нагрузки
- `career_growth` — возможности карьерного роста
- `training_opportunities` — возможности обучения
- `manager_support` — поддержка руководителя
- `team_relations` — отношения в команде
- `work_environment` — рабочая среда и условия
- `flexibility` — гибкость рабочего графика
- `recognition` — признание достижений
- `job_security` — стабильность работы
- `company_culture` — корпоративная культура
- `innovation_support` — поддержка инноваций
- `stress_level` — уровень стресса (обратная шкала)
- `overall_satisfaction` — общая удовлетворенность

**Применение**: Задание 2 (факторный анализ)

---

### 🛍 `products_analysis.csv` — Характеристики товаров
**Описание**: Данные о 200 товарах компании  
**Размер**: 200 строк × 11 столбцов  
**Разделитель**: `;` (точка с запятой)  
**Десятичные дроби**: `,` (запятая)

**Структура данных**:
- `product_id` — уникальный ID товара
- `category` — категория товара (текст)
- `price` — цена товара (рубли)
- `cost` — себестоимость (рубли)
- `rating` — средняя оценка товара (1-5)
- `review_count` — количество отзывов
- `return_rate` — доля возвратов (от 0 до 1)
- `category_popularity` — популярность категории (1-10)
- `seasonal_factor` — сезонный фактор (0.5-2.0)
- `competition_level` — уровень конкуренции (1-10)
- `days_in_catalog` — количество дней в каталоге

**Применение**: Задание 5 (комплексный анализ)

---

### 💰 `sales_data.csv` — Данные о продажах
**Описание**: Агрегированные данные о продажах товаров  
**Размер**: 200 строк × 5 столбцов  
**Разделитель**: `;` (точка с запятой)  
**Десятичные дроби**: `,` (запятая)

**Структура данных**:
- `product_id` — уникальный ID товара (связь с products_analysis.csv)
- `units_sold` — количество проданных единиц за период
- `revenue` — выручка за период (рубли)
- `marketing_spend` — расходы на маркетинг (рубли)
- `conversion_rate` — конверсия из просмотров в покупки (от 0 до 1)

**Применение**: Задание 5 (комплексный анализ)

---

## 🐍 Python скрипты

### 🔍 `pca_analysis.py` — Шаблон для анализа PCA
**Описание**: Готовый каркас для проведения анализа главных компонент  
**Функциональность**:
- Загрузка и предобработка данных
- Стандартизация переменных
- Применение PCA с разным количеством компонент
- Построение scree plot
- Анализ нагрузок компонент
- Сохранение результатов

**Ключевые функции**:
```python
def load_and_preprocess_data(file_path)
def standardize_features(data)
def perform_pca(data, n_components)
def plot_scree(pca_model)
def analyze_loadings(pca_model, feature_names)
```

---

### 🧩 `factor_analysis.py` — Шаблон факторного анализа
**Описание**: Комплексный инструмент для факторного анализа  
**Функциональность**:
- Проверка пригодности данных (тест Бартлетта, КМО)
- Определение количества факторов
- Факторный анализ с вращением
- Интерпретация результатов
- Визуализация матрицы нагрузок

**Ключевые функции**:
```python
def check_data_adequacy(data)
def determine_n_factors(data)
def perform_factor_analysis(data, n_factors, rotation)
def plot_factor_loadings(loadings_matrix)
def interpret_factors(loadings_matrix, threshold)
```

---

### 📊 `pca_visualization.py` — Визуализация результатов PCA
**Описание**: Набор функций для создания профессиональных графиков  
**Функциональность**:
- Biplot (объекты + переменные)
- Scree plot с улучшенным дизайном
- Contribution plot переменных
- Кластеризация в пространстве компонент
- Интерактивные графики

**Ключевые функции**:
```python
def create_biplot(components, loadings, feature_names)
def plot_enhanced_scree(explained_variance)
def plot_variable_contributions(loadings, component_num)
def plot_clusters_in_pc_space(components, clusters)
def create_interactive_biplot(components, loadings)
```

---

### 🚀 `comprehensive_analysis.py` — Комплексный анализ
**Описание**: Полный pipeline для мультивариантного анализа  
**Функциональность**:
- Объединение данных из нескольких источников
- Предварительный анализ и очистка
- Применение PCA и факторного анализа
- Кластеризация и сегментация
- Создание итогового отчета
- Бизнес-рекомендации

**Ключевые функции**:
```python
def merge_datasets(products_df, sales_df)
def comprehensive_pca_pipeline(data)
def comprehensive_factor_pipeline(data)
def cluster_analysis(components)
def generate_business_insights(clusters, original_data)
def create_executive_summary(results)
```

---

## 🎯 Рекомендации по использованию файлов

### 📋 Последовательность работы:
1. **Начните с `customers_data.csv`** и `pca_analysis.py` для освоения PCA
2. **Переходите к `employee_satisfaction.csv`** и `factor_analysis.py` для факторного анализа  
3. **Используйте `pca_visualization.py`** для создания качественных графиков
4. **Завершите `comprehensive_analysis.py`** с полными данными товаров и продаж

### 💡 Полезные советы:
- **📊 Всегда проверяйте данные** на пропуски и выбросы перед анализом
- **⚖️ Обязательно стандартизируйте** данные перед применением PCA
- **🎯 Начинайте с малого числа компонент** и постепенно увеличивайте
- **📝 Документируйте интерпретацию** каждой компоненты/фактора
- **🔄 Экспериментируйте с параметрами** для лучшего понимания методов

### 🚨 Частые ошибки:
- ❌ Забыли стандартизировать данные
- ❌ Неправильный разделитель в CSV (должен быть `;`)
- ❌ Неправильный десятичный разделитель (должна быть `,`)
- ❌ Слишком много компонент без экономического обоснования
- ❌ Игнорирование проверки адекватности данных для факторного анализа

---

## 🔧 Технические требования

### 📚 Необходимые библиотеки:
```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA, FactorAnalysis
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from factor_analyzer import FactorAnalyzer
from factor_analyzer.factor_analyzer import calculate_bartlett_sphericity, calculate_kmo
```

### 💻 Установка недостающих пакетов:
```bash
pip install factor_analyzer
pip install plotly  # для интерактивных графиков
```

---

- 🔙 [Предыдущая глава: Глава 23: - Презентация результатов: storytelling, отчёты](../chapter-23/README.md)
- 🔜 [Следующая глава: Глава 25: Непараметрические тесты: Манна–Уитни, Крускала–Уоллиса](../chapter-25/README.md)

---

- 📢 Присоединяйтесь к чату курса: https://t.me/analytics_course_chat
- 📢 Канал курса: https://t.me/analytics_course_channel