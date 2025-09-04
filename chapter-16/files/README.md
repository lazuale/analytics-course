# 📁 Учебные файлы для главы 16

Эта папка содержит все необходимые материалы для освоения кластеризации и сегментации данных в Python.

## 🎯 Содержимое папки

### 📊 Файлы с данными

#### 👥 `customer_behavior.csv` (142 KB)
**Назначение:** Данные клиентов для сегментации и RFM анализа  
**Размер:** 2,000 записей клиентов интернет-магазина  
**Содержимое:**
- `customer_id` — уникальный ID клиента
- `age` — возраст (18-75 лет)
- `income` — месячный доход (тыс. руб.)
- `gender` — пол (М/Ж)
- `city` — город проживания
- `registration_date` — дата регистрации
- `last_purchase_date` — дата последней покупки
- `total_purchases` — общее количество покупок
- `total_spent` — общая потраченная сумма (руб.)
- `avg_order_value` — средний чек (руб.)
- `days_since_last_purchase` — дней с последней покупки
- `favorite_category` — предпочитаемая категория товаров
- `payment_method` — способ оплаты
- `loyalty_score` — индекс лояльности (1-10)

**Использование:** 
- Задание 1: K-means сегментация клиентов
- Задание 4: Оценка качества кластеризации
- Задание 5: Production решение для сегментации

#### 🛍️ `product_analytics.csv` (87 KB)
**Назначение:** Характеристики товаров для товарной кластеризации  
**Размер:** 500 товаров различных категорий  
**Содержимое:**
- `product_id` — уникальный ID товара
- `product_name` — название товара
- `category` — категория (Электроника, Одежда, Дом, Спорт, Книги)
- `subcategory` — подкатегория
- `price` — цена (руб.)
- `rating` — средний рейтинг (1-5)
- `review_count` — количество отзывов
- `sales_volume` — объем продаж за месяц
- `return_rate` — процент возвратов
- `brand` — бренд товара
- `weight` — вес (кг)
- `dimensions` — габариты
- `discount_frequency` — частота участия в акциях
- `seasonality_index` — сезонность (1-10)
- `profit_margin` — маржинальность (%)

**Использование:**
- Задание 2: Иерархическая кластеризация товаров
- Создание рекомендательных систем
- Анализ товарного портфеля

#### 🗺️ `regional_data.csv` (23 KB)
**Назначение:** Экономические показатели регионов России для географической сегментации  
**Размер:** 85 регионов РФ  
**Содержимое:**
- `region_code` — код региона
- `region_name` — название региона
- `federal_district` — федеральный округ
- `population` — население (тыс. чел.)
- `gdp_per_capita` — ВРП на душу населения (тыс. руб.)
- `average_income` — средние доходы населения (руб.)
- `unemployment_rate` — уровень безработицы (%)
- `internet_penetration` — проникновение интернета (%)
- `retail_turnover` — оборот розничной торговли (млн руб.)
- `investment_volume` — объем инвестиций (млн руб.)
- `education_index` — индекс образования (1-10)
- `urbanization_rate` — уровень урбанизации (%)
- `distance_from_moscow` — расстояние от Москвы (км)

**Использование:**
- Задание 3: Географическая сегментация регионов
- Анализ региональных рынков
- Планирование экспансии бизнеса

#### 📈 `customer_transactions.csv` (256 KB)
**Назначение:** Детальные транзакции клиентов для продвинутой аналитики  
**Размер:** 15,000 транзакций  
**Содержимое:**
- `transaction_id` — ID транзакции
- `customer_id` — ID клиента (связь с customer_behavior.csv)
- `transaction_date` — дата и время транзакции
- `product_id` — ID товара (связь с product_analytics.csv)
- `quantity` — количество
- `unit_price` — цена за единицу
- `total_amount` — общая сумма
- `discount_applied` — примененная скидка (руб.)
- `channel` — канал продаж (Online, Store, Mobile)
- `session_duration` — длительность сессии (мин.)
- `payment_method` — способ оплаты
- `delivery_method` — способ доставки

**Использование:**
- Создание матриц клиент-товар для кластеризации
- Анализ паттернов покупательского поведения
- Market basket analysis

### 🐍 Python скрипты

#### 🎯 `kmeans_clustering.py` (15.4 KB)
**Назначение:** Полное введение в K-means кластеризацию  
**Содержимое:**
- Базовые примеры K-means с синтетическими данными
- Функции для выбора оптимального количества кластеров
- Методы оценки качества (силуэтный анализ, метод локтя)
- Визуализация результатов кластеризации
- Обработка реальных данных клиентов

```python
# Пример содержимого
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score

def find_optimal_clusters(data, max_k=10):
    """Находит оптимальное количество кластеров"""
    inertias = []
    silhouette_scores = []
    
    for k in range(2, max_k + 1):
        kmeans = KMeans(n_clusters=k, random_state=42)
        clusters = kmeans.fit_predict(data)
        
        inertias.append(kmeans.inertia_)
        silhouette_scores.append(silhouette_score(data, clusters))
    
    return inertias, silhouette_scores
```

#### 🌳 `hierarchical_clustering.py` (12.8 KB)
**Назначение:** Иерархическая кластеризация и дендрограммы  
**Содержимое:**
- Агломеративная кластеризация с разными методами объединения
- Построение и интерпретация дендрограмм
- Сравнение методов ward, complete, average, single
- Применение к товарным данным
- Создание рекомендательных систем

```python
# Пример содержимого
from sklearn.cluster import AgglomerativeClustering
from scipy.cluster.hierarchy import dendrogram, linkage
import matplotlib.pyplot as plt

def plot_dendrogram(data, method='ward', title='Дендрограмма'):
    """Строит дендрограмму для данных"""
    linkage_matrix = linkage(data, method=method)
    
    plt.figure(figsize=(12, 8))
    dendrogram(linkage_matrix, truncate_mode='lastp', p=15)
    plt.title(f'{title} (метод: {method})')
    plt.show()
    
    return linkage_matrix
```

#### 📊 `clustering_evaluation.py` (18.2 KB)
**Назначение:** Комплексная оценка качества кластеризации  
**Содержимое:**
- Все основные метрики качества кластеризации
- Силуэтный анализ с детальными диаграммами
- Сравнение различных алгоритмов (K-means, DBSCAN, GMM)
- Анализ стабильности кластеризации
- Автоматические отчеты по качеству

```python
def comprehensive_clustering_evaluation(data, cluster_labels):
    """Комплексная оценка качества кластеризации"""
    from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score
    
    metrics = {
        'silhouette_score': silhouette_score(data, cluster_labels),
        'calinski_harabasz': calinski_harabasz_score(data, cluster_labels),
        'davies_bouldin': davies_bouldin_score(data, cluster_labels),
        'n_clusters': len(np.unique(cluster_labels))
    }
    
    return metrics
```

#### 🎛️ `customer_segmentation_pipeline.py` (24.7 KB)
**Назначение:** Production-ready решение для сегментации клиентов  
**Содержимое:**
- Класс CustomerSegmentation для автоматической сегментации
- Полный пайплайн от сырых данных до бизнес-рекомендаций
- Методы сохранения и загрузки моделей
- Мониторинг качества и drift detection
- Интерактивный dashboard с профилями сегментов

```python
class CustomerSegmentation:
    """Production-ready система сегментации клиентов"""
    
    def __init__(self, n_clusters='auto', algorithm='kmeans'):
        self.n_clusters = n_clusters
        self.algorithm = algorithm
        self.model = None
        self.scaler = None
        self.feature_names = None
        self.segment_profiles = None
    
    def fit(self, data, features):
        """Обучение модели сегментации"""
        # Полная реализация пайплайна
        pass
    
    def predict(self, new_data):
        """Сегментация новых клиентов"""
        pass
    
    def get_segment_profiles(self):
        """Получение профилей сегментов"""
        pass
```

#### 🗺️ `geographic_clustering.py` (11.6 KB)
**Назначение:** Специализированные методы для географической кластеризации  
**Содержимое:**
- Кластеризация регионов по экономическим показателям
- Учет географических ограничений в кластеризации
- Визуализация результатов на карте России
- Анализ региональных кластеров для бизнеса
- Рекомендации по региональной экспансии

```python
def geographic_clustering_with_constraints(regional_data, n_clusters=5):
    """Кластеризация регионов с учетом географических ограничений"""
    from sklearn.cluster import AgglomerativeClustering
    
    # Создание матрицы связности на основе соседства регионов
    connectivity_matrix = create_regional_connectivity(regional_data)
    
    clustering = AgglomerativeClustering(
        n_clusters=n_clusters,
        connectivity=connectivity_matrix,
        linkage='ward'
    )
    
    return clustering.fit_predict(regional_data)
```

#### 🔬 `advanced_clustering.py` (19.3 KB)
**Назначение:** Продвинутые техники кластеризации  
**Содержимое:**
- DBSCAN для кластеризации на основе плотности
- Gaussian Mixture Models для мягкой кластеризации
- Spectral Clustering для сложных форм кластеров
- Ensemble кластеризация (комбинирование алгоритмов)
- Кластеризация временных рядов

```python
def ensemble_clustering(data, algorithms=['kmeans', 'gmm', 'spectral']):
    """Ensemble кластеризация с комбинированием результатов"""
    from sklearn.cluster import KMeans, SpectralClustering
    from sklearn.mixture import GaussianMixture
    
    results = {}
    
    for algo in algorithms:
        if algo == 'kmeans':
            model = KMeans(n_clusters=5, random_state=42)
        elif algo == 'gmm':
            model = GaussianMixture(n_components=5, random_state=42)
        # ... другие алгоритмы
        
        results[algo] = model.fit_predict(data)
    
    # Комбинирование результатов
    return combine_clustering_results(results)
```

## 🚀 Как использовать файлы

### 📋 Последовательность работы:

1. **🎯 Начните с теории** — прочитайте README.md главы 16
2. **🐍 Изучите K-means** — запустите `kmeans_clustering.py`
3. **🌳 Освойте иерархическую кластеризацию** — изучите `hierarchical_clustering.py`
4. **💻 Переходите к практике** — откройте practice.md
5. **📁 Используйте данные по заданиям:**
   - Задание 1: `customer_behavior.csv` + `kmeans_clustering.py`
   - Задание 2: `product_analytics.csv` + `hierarchical_clustering.py`
   - Задание 3: `regional_data.csv` + `geographic_clustering.py`
   - Задание 4: все файлы + `clustering_evaluation.py`
   - Задание 5: `customer_segmentation_pipeline.py`

### 💡 Советы по работе:

**🔧 Для установки зависимостей:**
```bash
# Основные библиотеки для кластеризации
pip install scikit-learn pandas numpy matplotlib seaborn

# Для работы с дендрограммами
pip install scipy

# Для продвинутых алгоритмов
pip install hdbscan umap-learn

# Для интерактивных визуализаций
pip install plotly bokeh

# Для работы с картами (опционально)
pip install geopandas folium
```

**📂 Структура рабочей папки:**
```
chapter-16/
├── files/              # ← эта папка
│   ├── customer_behavior.csv
│   ├── product_analytics.csv
│   ├── regional_data.csv
│   ├── customer_transactions.csv
│   ├── kmeans_clustering.py
│   ├── hierarchical_clustering.py
│   ├── clustering_evaluation.py
│   ├── customer_segmentation_pipeline.py
│   ├── geographic_clustering.py
│   └── advanced_clustering.py
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
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA

# Настройка отображения
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 11
sns.set_style("whitegrid")

# Отключение предупреждений
import warnings
warnings.filterwarnings('ignore')
```

## ⚠️ Важные заметки

### 🎯 О данных:
- Все данные реалистичные, но синтетические для обучения
- CSV файлы в кодировке UTF-8 с разделителем ","
- Данные содержат взаимосвязи для реалистичной кластеризации
- Включены выбросы и аномалии для отработки их обработки

### 🔐 Безопасность:
- Никаких реальных персональных или коммерческих данных
- Все данные полностью анонимны и синтетические
- Безопасно для использования в учебных и коммерческих проектах

### 🚀 Производительность:
- Размеры данных оптимизированы для обучения (до 2K записей)
- Все алгоритмы выполняются за разумное время (<30 сек)
- Включены оптимизированные версии для больших данных

### 📊 Особенности данных:

#### **Customer_behavior.csv:**
- RFM сегменты: от "Чемпионы" до "Спящие"
- Реалистичные корреляции между признаками
- Различные возрастные и доходные группы
- 5-7 естественных кластеров клиентов

#### **Product_analytics.csv:**
- Товары из 5 основных категорий
- Реалистичные зависимости цена-качество-популярность
- Сезонные и трендовые товары
- 6-8 товарных кластеров разной природы

#### **Regional_data.csv:**
- Актуальные экономические показатели регионов РФ
- Географическая логика в данных (соседние регионы похожи)
- 4-6 кластеров регионов по развитию
- Учтены федеральные округа и расстояния

## 🆘 Помощь и решение проблем

**Если кластеры получаются странными:**
```python
# Проверьте масштабирование данных
scaler = StandardScaler()
data_scaled = scaler.fit_transform(data)

# Исследуйте выбросы
Q1 = data.quantile(0.25)
Q3 = data.quantile(0.75)
IQR = Q3 - Q1
outliers = data[(data < (Q1 - 1.5 * IQR)) | (data > (Q3 + 1.5 * IQR)).any(axis=1)]
print(f"Найдено выбросов: {len(outliers)}")
```

**Если алгоритм работает медленно:**
```python
# Для больших данных используйте MiniBatchKMeans
from sklearn.cluster import MiniBatchKMeans

mini_kmeans = MiniBatchKMeans(n_clusters=5, random_state=42, batch_size=100)
clusters = mini_kmeans.fit_predict(data)
```

**Если результаты нестабильны:**
```python
# Увеличьте количество инициализаций
kmeans = KMeans(n_clusters=5, n_init=20, random_state=42)

# Или проверьте стабильность
def check_stability(data, n_runs=10):
    results = []
    for i in range(n_runs):
        kmeans = KMeans(n_clusters=5, random_state=i)
        clusters = kmeans.fit_predict(data)
        results.append(clusters)
    return results
```

**Если нет интерпретации результатов:**
```python
# Создайте профили кластеров
def create_cluster_profiles(data, clusters):
    profiles = []
    for cluster_id in np.unique(clusters):
        mask = clusters == cluster_id
        cluster_data = data[mask]
        
        profile = {
            'cluster': cluster_id,
            'size': len(cluster_data),
            'percentage': len(cluster_data) / len(data) * 100
        }
        
        for col in data.columns:
            profile[f'avg_{col}'] = cluster_data[col].mean()
            
        profiles.append(profile)
    
    return pd.DataFrame(profiles)
```

**💪 Готовы найти скрытые группы в ваших данных? Начинайте с практических заданий!**

---

📖 [Вернуться к теории](../README.md) | 📝 [Перейти к практике](../practice.md) | ✅ [Перейти к чек-листу](../checklist.md)

---

- 🔙 [Предыдущая глава: Глава 15 - Визуализация в Python: Matplotlib и Seaborn](../chapter-15/README.md)
- 🔜 [Следующая глава: Глава 17 - Классификация и регрессия в машинном обучении](../chapter-17/README.md)

---

- 📢 Присоединяйтесь к чату курса: https://t.me/analytics_course_chat
- 📢 Канал курса: https://t.me/analytics_course_channel