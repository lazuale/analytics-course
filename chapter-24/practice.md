# 💻 Глава 24: Практические задания — Мультивариантный анализ

📖 [Вернуться к теории](../README.md) | 📁 [Учебные файлы](../files/README.md) | ✅ [Чек-лист](../checklist.md)

---

## 🎯 Обзор практических заданий

В этой главе вы выполните **5 практических заданий**, которые покрывают все ключевые аспекты мультивариантного анализа:

1. **🔍 PCA для анализа клиентов** — снижение размерности реальных данных
2. **🧩 Факторный анализ удовлетворенности** — поиск скрытых факторов
3. **📊 Визуализация многомерных данных** — создание информативных графиков
4. **🎯 Интерпретация результатов** — извлечение бизнес-инсайтов
5. **🚀 Комплексный кейс** — полный цикл мультивариантного анализа

---

## 📝 Задание 1: PCA для анализа клиентов интернет-магазина

### 🎯 Цель
Применить анализ главных компонент для сегментации клиентов и снижения размерности данных.

### 📋 Описание задачи
У вас есть данные о 1000 клиентов интернет-магазина с 12 характеристиками поведения. Необходимо:
- Применить PCA для снижения размерности
- Определить оптимальное количество компонент
- Интерпретировать полученные главные компоненты

### 🗂 Файлы для работы
- `files/customers_data.csv` — данные о клиентах
- `files/pca_analysis.py` — шаблон для анализа

### 📊 Структура данных
```
customer_id,monthly_spending,orders_count,avg_order_value,session_duration,
page_views,return_rate,review_rating,mobile_usage,weekend_shopping,
loyalty_years,support_tickets,referrals_made
```

### 🛠 Пошаговые инструкции

#### Шаг 1: Подготовка данных
```python
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns

# Загрузить данные
df = pd.read_csv('customers_data.csv', sep=';', decimal=',')

# Проверить данные на пропуски и выбросы
print(df.info())
print(df.describe())
```

#### Шаг 2: Стандартизация
```python
# Выделить числовые переменные (исключить customer_id)
features = df.drop('customer_id', axis=1)

# Стандартизировать данные
scaler = StandardScaler()
features_scaled = scaler.fit_transform(features)
```

#### Шаг 3: Применение PCA
```python
# Создать PCA объект для всех компонент
pca_full = PCA()
pca_full.fit(features_scaled)

# Построить scree plot
plt.figure(figsize=(10, 6))
plt.plot(range(1, len(pca_full.explained_variance_ratio_) + 1), 
         pca_full.explained_variance_ratio_, 'bo-')
plt.title('🔍 Scree Plot: Объясненная изменчивость по компонентам')
plt.xlabel('Номер компоненты')
plt.ylabel('Объясненная изменчивость')
plt.grid(True, alpha=0.3)
plt.show()
```

#### Шаг 4: Выбор оптимального количества компонент
```python
# Найти количество компонент для 85% изменчивости
cumsum = np.cumsum(pca_full.explained_variance_ratio_)
n_components = np.argmax(cumsum >= 0.85) + 1
print(f"Для 85% изменчивости нужно {n_components} компонент")

# Применить PCA с выбранным количеством компонент
pca = PCA(n_components=n_components)
components = pca.fit_transform(features_scaled)
```

### ✅ Ожидаемый результат
- 📊 График scree plot с точкой "локтя"
- 🔢 Определение оптимального количества компонент (обычно 3-4)
- 📈 Таблица с объясненной изменчивостью по компонентам
- 🎯 Интерпретация первых 2-3 главных компонент

---

## 🧩 Задание 2: Факторный анализ удовлетворенности сотрудников

### 🎯 Цель
Провести факторный анализ для выявления скрытых факторов, влияющих на удовлетворенность сотрудников.

### 📋 Описание задачи
Проанализировать результаты опроса 500 сотрудников по 15 вопросам об удовлетворенности работой. Найти основные скрытые факторы, которые определяют ответы сотрудников.

### 🗂 Файлы для работы
- `files/employee_satisfaction.csv` — результаты опроса
- `files/factor_analysis.py` — шаблон для анализа

### 📊 Структура данных
```
employee_id,salary_satisfaction,bonus_fairness,workload_balance,
career_growth,training_opportunities,manager_support,team_relations,
work_environment,flexibility,recognition,job_security,
company_culture,innovation_support,stress_level,overall_satisfaction
```

### 🛠 Пошаговые инструкции

#### Шаг 1: Подготовка и проверка данных
```python
from sklearn.decomposition import FactorAnalysis
from factor_analyzer import FactorAnalyzer
from factor_analyzer.factor_analyzer import calculate_bartlett_sphericity
from factor_analyzer.factor_analyzer import calculate_kmo

# Загрузить данные
df = pd.read_csv('employee_satisfaction.csv', sep=';', decimal=',')
features = df.drop('employee_id', axis=1)

# Проверить адекватность выборки для факторного анализа
chi_square_value, p_value = calculate_bartlett_sphericity(features)
print(f"Тест Бартлетта: χ² = {chi_square_value:.2f}, p = {p_value:.4f}")

kmo_all, kmo_model = calculate_kmo(features)
print(f"Критерий КМО: {kmo_model:.3f}")
```

#### Шаг 2: Определение количества факторов
```python
# Построить scree plot для факторного анализа
fa = FactorAnalyzer(rotation=None)
fa.fit(features)

ev, v = fa.get_eigenvalues()
plt.figure(figsize=(10, 6))
plt.plot(range(1, len(ev) + 1), ev, 'bo-')
plt.axhline(y=1, color='r', linestyle='--', label='Eigenvalue = 1')
plt.title('🧩 Scree Plot для факторного анализа')
plt.xlabel('Номер фактора')
plt.ylabel('Собственное значение')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
```

#### Шаг 3: Факторный анализ с вращением
```python
# Провести факторный анализ с 3 факторами и вращением varimax
fa = FactorAnalyzer(n_factors=3, rotation='varimax')
fa.fit(features)

# Получить матрицу нагрузок
loadings = fa.loadings_
loadings_df = pd.DataFrame(loadings, 
                          index=features.columns,
                          columns=['Фактор 1', 'Фактор 2', 'Фактор 3'])

# Визуализировать нагрузки
plt.figure(figsize=(12, 8))
sns.heatmap(loadings_df, annot=True, cmap='RdBu_r', center=0,
            fmt='.2f', square=True)
plt.title('🔥 Матрица факторных нагрузок')
plt.tight_layout()
plt.show()
```

### ✅ Ожидаемый результат
- 📊 Scree plot с определением количества факторов
- 🔥 Heatmap матрицы факторных нагрузок
- 🎯 Интерпретация 3 основных факторов (например: "Материальная мотивация", "Социальный климат", "Развитие и рост")
- 📈 Доля объясненной изменчивости каждым фактором

---

## 📊 Задание 3: Визуализация результатов PCA

### 🎯 Цель
Создать информативные визуализации результатов PCA для презентации заинтересованным сторонам.

### 📋 Описание задачи
Используя результаты PCA из задания 1, создать комплект визуализаций, которые помогут бизнесу понять структуру клиентской базы.

### 🗂 Файлы для работы
- Результаты из задания 1
- `files/pca_visualization.py` — шаблоны графиков

### 🛠 Пошаговые инструкции

#### Шаг 1: Biplot для первых двух компонент
```python
def create_biplot(components, feature_names, pca_model):
    plt.figure(figsize=(12, 8))
    
    # Точки (клиенты) в пространстве компонент
    plt.scatter(components[:, 0], components[:, 1], alpha=0.6)
    
    # Векторы переменных
    for i, (feature, loading) in enumerate(zip(feature_names, pca_model.components_.T)):
        plt.arrow(0, 0, loading[0]*3, loading[1]*3, 
                 head_width=0.05, head_length=0.05, 
                 fc='red', ec='red', alpha=0.8)
        plt.text(loading[0]*3.2, loading[1]*3.2, feature, 
                fontsize=10, ha='center', va='center')
    
    plt.xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.1%} изменчивости)')
    plt.ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.1%} изменчивости)')
    plt.title('📊 Biplot: Клиенты и переменные в пространстве компонент')
    plt.grid(True, alpha=0.3)
    plt.show()

create_biplot(components, features.columns, pca)
```

#### Шаг 2: Кластеризация в пространстве компонент
```python
from sklearn.cluster import KMeans

# Кластеризация клиентов в пространстве компонент
kmeans = KMeans(n_clusters=4, random_state=42)
clusters = kmeans.fit_predict(components)

# Визуализация кластеров
plt.figure(figsize=(10, 8))
scatter = plt.scatter(components[:, 0], components[:, 1], 
                     c=clusters, cmap='viridis', alpha=0.7)
plt.colorbar(scatter, label='Кластер')
plt.xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.1%})')
plt.ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.1%})')
plt.title('🎯 Сегментация клиентов по главным компонентам')
plt.grid(True, alpha=0.3)
plt.show()
```

### ✅ Ожидаемый результат
- 📊 Biplot с клиентами и переменными
- 🎯 Визуализация кластеров клиентов
- 📈 График contribution of variables для каждой компоненты
- 🎨 Дашборд с ключевыми визуализациями

---

## 🎯 Задание 4: Интерпретация и бизнес-инсайты

### 🎯 Цель
Извлечь практические бизнес-инсайты из результатов мультивариантного анализа.

### 📋 Описание задачи
На основе результатов предыдущих заданий сформулировать конкретные рекомендации для бизнеса по работе с клиентами.

### 🛠 Пошаговые инструкции

#### Шаг 1: Анализ главных компонент
```python
# Проанализировать нагрузки переменных на компоненты
components_df = pd.DataFrame(
    pca.components_.T,
    columns=[f'PC{i+1}' for i in range(pca.n_components_)],
    index=features.columns
)

# Найти переменные с наибольшими нагрузками
for i in range(pca.n_components_):
    print(f"\n📊 Главная компонента {i+1}:")
    print(f"Объясняет {pca.explained_variance_ratio_[i]:.1%} изменчивости")
    
    # Топ-3 положительных нагрузки
    top_pos = components_df[f'PC{i+1}'].nlargest(3)
    print("Положительные нагрузки:", top_pos.to_dict())
    
    # Топ-3 отрицательных нагрузки
    top_neg = components_df[f'PC{i+1}'].nsmallest(3)
    print("Отрицательные нагрузки:", top_neg.to_dict())
```

#### Шаг 2: Профилирование кластеров
```python
# Добавить кластеры к исходным данным
df_with_clusters = df.copy()
df_with_clusters['cluster'] = clusters

# Профилировать каждый кластер
cluster_profiles = df_with_clusters.groupby('cluster').agg({
    'monthly_spending': ['mean', 'median'],
    'orders_count': ['mean', 'median'],
    'avg_order_value': ['mean', 'median'],
    'loyalty_years': ['mean', 'median'],
    'return_rate': ['mean', 'median']
}).round(2)

print("👥 Профили кластеров:")
print(cluster_profiles)
```

### ✅ Ожидаемый результат
- 📋 Интерпретация каждой главной компоненты
- 👥 Описание профилей кластеров клиентов
- 💡 Конкретные рекомендации по работе с каждым сегментом
- 📊 Презентационные слайды с выводами

---

## 🚀 Задание 5: Комплексный кейс — Анализ продуктовой линейки

### 🎯 Цель
Применить весь арсенал методов мультивариантного анализа для решения комплексной бизнес-задачи.

### 📋 Описание задачи
Компания производит 200 различных товаров и хочет оптимизировать продуктовую линейку. У вас есть данные о продажах, характеристиках товаров и клиентских предпочтениях.

### 🗂 Файлы для работы
- `files/products_analysis.csv` — данные о товарах
- `files/sales_data.csv` — данные о продажах
- `files/comprehensive_analysis.py` — шаблон полного анализа

### 🛠 Пошаговые инструкции

#### Шаг 1: Объединение и подготовка данных
```python
# Загрузить и объединить данные
products = pd.read_csv('products_analysis.csv', sep=';', decimal=',')
sales = pd.read_csv('sales_data.csv', sep=';', decimal=',')

# Объединить данные по product_id
full_data = products.merge(sales, on='product_id', how='inner')

# Создать производные метрики
full_data['profit_margin'] = (full_data['price'] - full_data['cost']) / full_data['price']
full_data['sales_velocity'] = full_data['units_sold'] / full_data['days_in_catalog']
```

#### Шаг 2: PCA для снижения размерности
```python
# Выбрать переменные для анализа
analysis_vars = [
    'price', 'cost', 'profit_margin', 'units_sold', 
    'sales_velocity', 'return_rate', 'rating',
    'category_popularity', 'seasonal_factor', 'competition_level'
]

# Применить PCA
features_scaled = StandardScaler().fit_transform(full_data[analysis_vars])
pca = PCA(n_components=0.9)  # 90% изменчивости
components = pca.fit_transform(features_scaled)
```

#### Шаг 3: Кластеризация и анализ групп товаров
```python
# Кластеризация товаров
from sklearn.cluster import KMeans
kmeans = KMeans(n_clusters=5, random_state=42)
clusters = kmeans.fit_predict(components)

# Анализ характеристик кластеров
full_data['cluster'] = clusters
cluster_analysis = full_data.groupby('cluster').agg({
    'price': ['mean', 'std'],
    'profit_margin': ['mean', 'std'],
    'units_sold': ['sum', 'mean'],
    'rating': 'mean',
    'return_rate': 'mean'
}).round(3)
```

### ✅ Ожидаемый результат
- 📊 Сегментация продуктовой линейки на 5 групп
- 💰 Анализ прибыльности каждой группы товаров
- 🎯 Рекомендации по оптимизации ассортимента
- 📈 План действий для каждого сегмента товаров
- 📋 Executive summary с ключевыми выводами

---

## ✅ Контрольные вопросы

После выполнения всех заданий ответьте на вопросы:

1. 🔍 **Какие главные компоненты** вы выделили и как их интерпретировали?
2. 🧩 **Какие скрытые факторы** обнаружил факторный анализ?
3. 📊 **Сколько процентов изменчивости** объясняют ваши компоненты/факторы?
4. 👥 **Какие сегменты клиентов** вы выделили и чем они отличаются?
5. 💡 **Какие практические рекомендации** можно дать бизнесу?

---

- 🔙 [Предыдущая глава: Глава 23: - Презентация результатов: storytelling, отчёты](../chapter-23/README.md)
- 🔜 [Следующая глава: Глава 25: Непараметрические тесты: Манна–Уитни, Крускала–Уоллиса](../chapter-25/README.md)

---

- 📢 Присоединяйтесь к чату курса: https://t.me/analytics_course_chat
- 📢 Канал курса: https://t.me/analytics_course_channel