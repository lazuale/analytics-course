# 🎯 Глава 16: Кластеризация и сегментация — находим скрытые группы в данных!

## 🎯 Что вы изучите

После изучения этой главы вы сможете:

- 🔍 **Находить скрытые группы** в данных без заранее известных меток
- 🎯 **Сегментировать клиентов** для персонализированного маркетинга
- 🤖 **Использовать алгоритмы k-means и иерархическую кластеризацию** в scikit-learn
- 📊 **Оценивать качество** кластеризации и выбирать оптимальное количество групп
- 💼 **Применять результаты** для принятия бизнес-решений и стратегий

## 🌟 Кластеризация простыми словами

**Кластеризация** — это как умный сортировщик, который смотрит на кучу разных объектов и автоматически раскладывает их по группам, основываясь на их сходстве.

### 🎭 **Метафора: Кластеризация как организация вечеринки**

Представьте, что вы организуете большую вечеринку и хотите рассадить гостей за столики так, чтобы людям было интересно общаться:

- 🎯 **Кластеризация** — это процесс группировки гостей
- 👥 **Кластеры** — это столики с похожими людьми
- 📏 **Расстояние** — это степень сходства между людьми
- 🎪 **Центроид** — это "душа компании" за каждым столиком
- 🔄 **Алгоритм** — это ваша стратегия рассаживания

### 💼 **Зачем это нужно аналитику в 2025:**

**Без кластеризации:**
```
"У нас 50,000 клиентов. Всем отправим одинаковое предложение!"
Результат: 😴 2% конверсия
```

**С кластеризацией:**
```python
# Находим 5 групп клиентов
clusters = KMeans(n_clusters=5)
customer_segments = clusters.fit_predict(customer_data)
# Персонализированные предложения для каждой группы
```
Результат: 🚀 15% конверсия

## 🧠 Основы кластеризации

### 🎯 **Что такое неконтролируемое обучение**

**Контролируемое обучение** (главы 17-18):
- У нас есть правильные ответы ("это спам", "это не спам")
- Учим модель предсказывать известные категории

**Неконтролируемое обучение** (эта глава):
- У нас НЕТ правильных ответов
- Ищем скрытые закономерности и группы
- Данные сами "рассказывают" свою структуру

### 📊 **Типы кластеризации**

#### 🎯 **Жесткая кластеризация**
Каждый объект принадлежит только одному кластеру
```
Клиент Иван → Кластер "VIP" (100%)
Клиент Мария → Кластер "Экономные" (100%)
```

#### 🌊 **Мягкая кластеризация**  
Каждый объект может частично принадлежать разным кластерам
```
Клиент Петр → 70% "VIP" + 30% "Средний класс"
```

## 🎯 K-means кластеризация — самый популярный алгоритм

### 🌟 **Как работает k-means**

**Простая аналогия:** Представьте, что вы ищете лучшие места для открытия кофеен в городе.

1. **🎯 Выбираете количество кофеен** (параметр k)
2. **📍 Случайно размещаете их** на карте города  
3. **👥 Каждый житель идет в ближайшую** кофейню
4. **🏠 Кофейни "переезжают"** в центр своих клиентов
5. **🔄 Повторяете** пока кофейни не найдут идеальные места

### 🔧 **K-means на практике**

```python
from sklearn.cluster import KMeans
import pandas as pd
import numpy as np

# Загружаем данные клиентов
customers = pd.read_csv('customers.csv')

# Выбираем признаки для кластеризации
features = ['возраст', 'доход', 'частота_покупок']
X = customers[features]

# Создаем модель k-means
kmeans = KMeans(
    n_clusters=4,        # Количество кластеров
    random_state=42,     # Для воспроизводимости
    n_init=10           # Количество инициализаций
)

# Находим кластеры
cluster_labels = kmeans.fit_predict(X)

# Добавляем результаты к данным
customers['кластер'] = cluster_labels

print("🎉 Клиенты разделены на группы!")
print(customers['кластер'].value_counts())
```

### 🎯 **Выбор оптимального количества кластеров**

#### 📈 **Метод локтя (Elbow Method)**

**Идея:** Ищем "локоть" на графике — точку, где добавление кластера не сильно улучшает результат.

```python
from sklearn.metrics import silhouette_score

# Тестируем разное количество кластеров
inertias = []
silhouette_scores = []
k_range = range(2, 11)

for k in k_range:
    kmeans = KMeans(n_clusters=k, random_state=42)
    cluster_labels = kmeans.fit_predict(X)
    
    # Внутрикластерная дисперсия (чем меньше, тем лучше)
    inertias.append(kmeans.inertia_)
    
    # Силуэтный коэффициент (чем больше, тем лучше)
    silhouette_scores.append(silhouette_score(X, cluster_labels))

# Строим график для выбора k
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.plot(k_range, inertias, 'bo-')
plt.title('📈 Метод локтя')
plt.xlabel('Количество кластеров (k)')
plt.ylabel('Внутрикластерная дисперсия')

plt.subplot(1, 2, 2)
plt.plot(k_range, silhouette_scores, 'ro-')
plt.title('📊 Силуэтный анализ')
plt.xlabel('Количество кластеров (k)')
plt.ylabel('Силуэтный коэффициент')

plt.show()
```

#### 🎯 **Силуэтный анализ**

**Силуэтный коэффициент** показывает, насколько хорошо объект вписывается в свой кластер:
- **+1** — объект идеально вписывается в свой кластер
- **0** — объект находится на границе кластеров  
- **-1** — объект попал не в тот кластер

### ⚖️ **Преимущества и недостатки k-means**

#### ✅ **Преимущества:**
- 🚀 **Быстрый** — работает с большими данными
- 🎯 **Простой** — легко понять и реализовать
- 📊 **Эффективный** — хорошо находит сферические кластеры
- 💼 **Популярный** — много готовых реализаций

#### ❌ **Недостатки:**
- 🎯 **Нужно заранее знать k** — количество кластеров
- ⭕ **Только круглые кластеры** — плохо работает с вытянутыми группами
- 📏 **Чувствителен к масштабу** — нужна нормализация данных
- 🎲 **Случайная инициализация** — результат может отличаться

## 🌳 Иерархическая кластеризация — строим дерево групп

### 🌟 **Как работает иерархическая кластеризация**

**Аналогия:** Представьте семейное дерево, но наоборот — от отдельных людей к большим семьям.

#### 🔗 **Агломеративная кластеризация (снизу вверх):**

1. **👤 Каждый объект** — отдельный кластер
2. **🤝 Находим двух самых похожих** "соседей"
3. **👥 Объединяем их** в один кластер  
4. **🔄 Повторяем** пока не останется один большой кластер
5. **✂️ "Разрезаем" дерево** на нужном уровне

```python
from sklearn.cluster import AgglomerativeClustering
from scipy.cluster.hierarchy import dendrogram, linkage
import matplotlib.pyplot as plt

# Создаем иерархические кластеры
hierarchical = AgglomerativeClustering(
    n_clusters=4,           # Количество финальных кластеров
    linkage='ward'          # Метод объединения
)

cluster_labels = hierarchical.fit_predict(X)

# Строим дендрограмму (дерево кластеров)
linkage_matrix = linkage(X, method='ward')

plt.figure(figsize=(12, 8))
dendrogram(linkage_matrix, 
           truncate_mode='lastp',  # Показать только последние p кластеров
           p=12,                   # Количество листьев
           leaf_rotation=90,       # Поворот подписей
           leaf_font_size=10)

plt.title('🌳 Дендрограмма - дерево кластеров')
plt.xlabel('Номер кластера или размер')
plt.ylabel('Расстояние объединения')
plt.show()
```

### 🔗 **Методы объединения кластеров**

#### 🎯 **Ward (минимум дисперсии)**
- Объединяет кластеры так, чтобы минимально увеличить внутреннюю дисперсию
- **Лучший выбор** для большинства задач

#### 📏 **Complete (полная связь)**
- Расстояние = максимальное расстояние между элементами кластеров
- Создает **компактные** кластеры

#### 🔗 **Average (средняя связь)**
- Расстояние = среднее расстояние между всеми парами элементов
- **Компромиссный** вариант

#### ⚡ **Single (одиночная связь)**
- Расстояние = минимальное расстояние между ближайшими элементами
- Склонен к **цепному эффекту**

### ⚖️ **Преимущества и недостатки иерархической кластеризации**

#### ✅ **Преимущества:**
- 🌳 **Показывает структуру** данных в виде дерева
- 🎯 **Не нужно заранее знать количество** кластеров
- 📊 **Детерминирован** — всегда одинаковый результат
- 🔍 **Можно анализировать** на разных уровнях детализации

#### ❌ **Недостатки:**
- 🐌 **Медленный** — плохо работает с большими данными O(n³)
- 🚫 **Нельзя исправить ошибки** — если объединили неправильно, не разъединишь
- 💾 **Много памяти** — нужно хранить матрицу расстояний
- 🎯 **Сложно автоматизировать** выбор финального количества кластеров

## 📊 Практические применения кластеризации

### 👥 **Сегментация клиентов**

**Цель:** Разделить клиентов на группы для персонализированного маркетинга.

```python
# Признаки для сегментации клиентов
customer_features = [
    'возраст',
    'доход', 
    'частота_покупок',
    'средний_чек',
    'время_с_последней_покупки',
    'количество_категорий'
]

# RFM анализ (Recency, Frequency, Monetary)
customers['R'] = (datetime.now() - customers['последняя_покупка']).dt.days
customers['F'] = customers['количество_покупок'] 
customers['M'] = customers['общая_сумма_покупок']

# Нормализация данных (важно для k-means!)
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_scaled = scaler.fit_transform(customers[['R', 'F', 'M']])

# Кластеризация
kmeans = KMeans(n_clusters=5, random_state=42)
customers['сегмент'] = kmeans.fit_predict(X_scaled)

# Интерпретация сегментов
segment_analysis = customers.groupby('сегмент').agg({
    'R': 'mean',
    'F': 'mean', 
    'M': 'mean',
    'возраст': 'mean',
    'доход': 'mean'
}).round(2)

print("📊 Характеристики сегментов:")
print(segment_analysis)
```

### 🛍️ **Товарные рекомендации**

**Цель:** Группировать товары для перекрестных продаж и рекомендаций.

```python
# Матрица "клиент-товар" 
customer_product_matrix = purchases.pivot_table(
    index='клиент_id', 
    columns='товар', 
    values='количество', 
    fill_value=0
)

# Кластеризуем товары по покупательскому поведению
product_clusters = KMeans(n_clusters=8, random_state=42)
product_segments = product_clusters.fit_predict(customer_product_matrix.T)

# Товары в одном кластере покупают одни и те же клиенты
products_df = pd.DataFrame({
    'товар': customer_product_matrix.columns,
    'кластер': product_segments
})

print("🛍️ Группы товаров для рекомендаций:")
for cluster in range(8):
    cluster_products = products_df[products_df['кластер'] == cluster]['товар'].tolist()
    print(f"Кластер {cluster}: {cluster_products[:5]}...")  # Показываем первые 5
```

### 🗺️ **Географическая сегментация**

**Цель:** Найти регионы со схожим поведением для оптимизации логистики.

```python
# Группируем по регионам и считаем характеристики
region_features = sales.groupby('регион').agg({
    'выручка': 'mean',
    'количество_заказов': 'sum',
    'средний_чек': 'mean',
    'скидка': 'mean'
}).reset_index()

# Кластеризация регионов
region_clusters = KMeans(n_clusters=3, random_state=42)
region_features['кластер'] = region_clusters.fit_predict(
    region_features[['выручка', 'количество_заказов', 'средний_чек', 'скидка']]
)

print("🗺️ Региональные кластеры:")
print(region_features.groupby('кластер')['регион'].apply(list))
```

## 📏 Подготовка данных для кластеризации

### 🔧 **Нормализация и стандартизация**

**Проблема:** Различные масштабы признаков искажают расстояния.

```python
from sklearn.preprocessing import StandardScaler, MinMaxScaler

# Исходные данные
data = pd.DataFrame({
    'возраст': [25, 35, 45, 55],      # от 0 до 100
    'доход': [30000, 60000, 90000, 120000],  # от 0 до 500000
    'покупки': [2, 5, 8, 12]          # от 0 до 50
})

print("📊 Исходные данные:")
print(data)

# Стандартизация (среднее=0, стд.отклонение=1)
scaler = StandardScaler()
data_standardized = scaler.fit_transform(data)

print("\n📏 После стандартизации:")
print(pd.DataFrame(data_standardized, columns=data.columns))

# Нормализация (от 0 до 1)
minmax_scaler = MinMaxScaler()
data_normalized = minmax_scaler.fit_transform(data)

print("\n🎯 После нормализации:")
print(pd.DataFrame(data_normalized, columns=data.columns))
```

### 🧹 **Обработка категориальных переменных**

```python
from sklearn.preprocessing import LabelEncoder, OneHotEncoder

# Категориальные данные
customers = pd.DataFrame({
    'пол': ['М', 'Ж', 'М', 'Ж'],
    'город': ['Москва', 'СПб', 'Москва', 'Казань'],
    'доход': [50000, 60000, 55000, 45000]
})

# Способ 1: Label Encoding (для порядковых переменных)
le = LabelEncoder()
customers['пол_encoded'] = le.fit_transform(customers['пол'])

# Способ 2: One-Hot Encoding (для номинальных переменных)
city_encoded = pd.get_dummies(customers['город'], prefix='город')
customers_encoded = pd.concat([customers, city_encoded], axis=1)

print("🔄 Обработанные данные:")
print(customers_encoded)
```

## 📊 Оценка качества кластеризации

### 🎯 **Внутренние метрики (не нужны истинные метки)**

#### 📏 **Силуэтный коэффициент**
```python
from sklearn.metrics import silhouette_score, silhouette_samples

# Общий силуэтный коэффициент
silhouette_avg = silhouette_score(X, cluster_labels)
print(f"Средний силуэтный коэффициент: {silhouette_avg:.3f}")

# Силуэтный коэффициент для каждого объекта
sample_silhouette_values = silhouette_samples(X, cluster_labels)

# Анализ по кластерам
for i in range(n_clusters):
    cluster_silhouettes = sample_silhouette_values[cluster_labels == i]
    print(f"Кластер {i}: силуэт = {cluster_silhouettes.mean():.3f}")
```

#### 🎯 **Calinski-Harabasz индекс**
```python
from sklearn.metrics import calinski_harabasz_score

ch_score = calinski_harabasz_score(X, cluster_labels)
print(f"Calinski-Harabasz индекс: {ch_score:.2f}")
# Чем больше, тем лучше разделение кластеров
```

#### 📊 **Davies-Bouldin индекс**
```python
from sklearn.metrics import davies_bouldin_score

db_score = davies_bouldin_score(X, cluster_labels)
print(f"Davies-Bouldin индекс: {db_score:.3f}")
# Чем меньше, тем лучше разделение кластеров
```

### 🎨 **Визуализация результатов кластеризации**

```python
import matplotlib.pyplot as plt
import seaborn as sns

# Двумерная визуализация (если признаков больше 2, используем PCA)
from sklearn.decomposition import PCA

if X.shape[1] > 2:
    # Сжимаем до 2D для визуализации
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X)
    print(f"PCA объясняет {pca.explained_variance_ratio_.sum():.1%} дисперсии")
else:
    X_pca = X

# Визуализация кластеров
plt.figure(figsize=(12, 8))

# Раскрашиваем точки по кластерам
colors = plt.cm.Set1(np.linspace(0, 1, len(np.unique(cluster_labels))))

for i, color in enumerate(colors):
    mask = cluster_labels == i
    plt.scatter(X_pca[mask, 0], X_pca[mask, 1], 
               c=[color], label=f'Кластер {i}', alpha=0.7)

# Добавляем центроиды (для k-means)
if hasattr(kmeans, 'cluster_centers_'):
    centers_pca = pca.transform(kmeans.cluster_centers_) if X.shape[1] > 2 else kmeans.cluster_centers_
    plt.scatter(centers_pca[:, 0], centers_pca[:, 1],
               c='black', marker='x', s=300, linewidths=3, label='Центроиды')

plt.title('🎯 Результаты кластеризации')
plt.xlabel('Первая главная компонента' if X.shape[1] > 2 else 'Признак 1')
plt.ylabel('Вторая главная компонента' if X.shape[1] > 2 else 'Признак 2')
plt.legend()
plt.grid(alpha=0.3)
plt.show()
```

## 💼 Бизнес-интерпретация результатов

### 🎯 **Профилирование кластеров**

```python
def profile_clusters(data, cluster_column='кластер'):
    """Создает профили кластеров для бизнес-интерпретации"""
    
    profiles = []
    
    for cluster_id in data[cluster_column].unique():
        cluster_data = data[data[cluster_column] == cluster_id]
        
        profile = {
            'Кластер': cluster_id,
            'Размер': len(cluster_data),
            'Доля': f"{len(cluster_data) / len(data) * 100:.1f}%"
        }
        
        # Средние значения числовых признаков
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            if col != cluster_column:
                profile[f'Средний {col}'] = cluster_data[col].mean()
        
        # Моды категориальных признаков  
        categorical_cols = data.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            if col != cluster_column:
                mode_value = cluster_data[col].mode()
                if len(mode_value) > 0:
                    profile[f'Типичный {col}'] = mode_value[0]
        
        profiles.append(profile)
    
    return pd.DataFrame(profiles)

# Создаем профили кластеров
cluster_profiles = profile_clusters(customers)
print("📊 Профили кластеров клиентов:")
print(cluster_profiles)
```

### 🏷️ **Присвоение бизнес-названий кластерам**

```python
# На основе анализа профилей присваиваем понятные названия
cluster_names = {
    0: 'Молодые активные',
    1: 'Премиум клиенты', 
    2: 'Экономные покупатели',
    3: 'Редкие крупные покупки',
    4: 'Средний класс'
}

customers['сегмент_название'] = customers['кластер'].map(cluster_names)

# Создаем рекомендации для каждого сегмента
segment_strategies = {
    'Молодые активные': 'Акции на трендовые товары, соцсети',
    'Премиум клиенты': 'VIP программа, персональный менеджер',  
    'Экономные покупатели': 'Скидки, программа лояльности',
    'Редкие крупные покупки': 'Напоминания, сезонные предложения',
    'Средний класс': 'Стандартные акции, email-рассылка'
}

print("🎯 Стратегии работы с сегментами:")
for segment, strategy in segment_strategies.items():
    count = (customers['сегмент_название'] == segment).sum()
    print(f"{segment} ({count} клиентов): {strategy}")
```

## 🚀 Готовые шаблоны для копирования

### 🎯 **Полный пайплайн сегментации клиентов**

```python
def customer_segmentation_pipeline(data, features, n_clusters=5):
    """
    Полный пайплайн сегментации клиентов
    
    Parameters:
    -----------
    data : DataFrame
        Данные клиентов
    features : list
        Список признаков для кластеризации
    n_clusters : int
        Количество кластеров
    
    Returns:
    --------
    data_with_clusters : DataFrame
        Исходные данные с добавленными кластерами
    model : KMeans
        Обученная модель для новых данных
    """
    
    from sklearn.cluster import KMeans
    from sklearn.preprocessing import StandardScaler
    from sklearn.metrics import silhouette_score
    
    # 1. Подготовка данных
    X = data[features].copy()
    
    # Обработка пропусков
    X = X.fillna(X.median())
    
    # Стандартизация
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # 2. Кластеризация
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    cluster_labels = kmeans.fit_predict(X_scaled)
    
    # 3. Оценка качества
    silhouette = silhouette_score(X_scaled, cluster_labels)
    print(f"✅ Кластеризация завершена!")
    print(f"📊 Силуэтный коэффициент: {silhouette:.3f}")
    print(f"🎯 Найдено кластеров: {n_clusters}")
    
    # 4. Добавляем результаты
    result_data = data.copy()
    result_data['кластер'] = cluster_labels
    
    # 5. Профилирование
    print("\n📋 Размеры кластеров:")
    print(pd.Series(cluster_labels).value_counts().sort_index())
    
    return result_data, kmeans, scaler

# Пример использования
segmented_customers, model, scaler = customer_segmentation_pipeline(
    data=customers,
    features=['возраст', 'доход', 'частота_покупок', 'средний_чек'],
    n_clusters=5
)
```

### 📊 **Функция для выбора оптимального количества кластеров**

```python
def find_optimal_clusters(data, features, max_k=10):
    """Находит оптимальное количество кластеров"""
    
    from sklearn.cluster import KMeans
    from sklearn.preprocessing import StandardScaler
    from sklearn.metrics import silhouette_score
    import matplotlib.pyplot as plt
    
    # Подготовка данных
    X = data[features]
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Тестируем разное количество кластеров
    k_range = range(2, max_k + 1)
    inertias = []
    silhouette_scores = []
    
    for k in k_range:
        kmeans = KMeans(n_clusters=k, random_state=42)
        cluster_labels = kmeans.fit_predict(X_scaled)
        
        inertias.append(kmeans.inertia_)
        silhouette_scores.append(silhouette_score(X_scaled, cluster_labels))
    
    # Визуализация результатов
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
    
    # График локтя
    ax1.plot(k_range, inertias, 'bo-')
    ax1.set_title('📈 Метод локтя')
    ax1.set_xlabel('Количество кластеров (k)')
    ax1.set_ylabel('Внутрикластерная дисперсия')
    ax1.grid(alpha=0.3)
    
    # Силуэтный анализ
    ax2.plot(k_range, silhouette_scores, 'ro-')
    ax2.set_title('📊 Силуэтный анализ')
    ax2.set_xlabel('Количество кластеров (k)')
    ax2.set_ylabel('Силуэтный коэффициент')
    ax2.grid(alpha=0.3)
    
    # Находим оптимальное k
    best_k = k_range[np.argmax(silhouette_scores)]
    
    plt.tight_layout()
    plt.show()
    
    print(f"🎯 Рекомендуемое количество кластеров: {best_k}")
    print(f"📊 Силуэтный коэффициент: {max(silhouette_scores):.3f}")
    
    return best_k, silhouette_scores

# Использование
optimal_k, scores = find_optimal_clusters(
    data=customers,
    features=['возраст', 'доход', 'частота_покупок'],
    max_k=10
)
```

## ⚠️ Важные моменты и ошибки

### ❌ **Частые ошибки новичков:**

1. **🔍 Забывают нормализовать данные**
   ```python
   # ❌ Неправильно
   kmeans.fit(raw_data)
   
   # ✅ Правильно
   scaler = StandardScaler()
   scaled_data = scaler.fit_transform(raw_data)
   kmeans.fit(scaled_data)
   ```

2. **🎯 Не анализируют результаты**
   ```python
   # ❌ Просто получили кластеры
   clusters = kmeans.fit_predict(X)
   
   # ✅ Анализируют и интерпретируют
   clusters = kmeans.fit_predict(X)
   silhouette = silhouette_score(X, clusters)
   print(f"Качество кластеризации: {silhouette}")
   
   # Профилирование кластеров
   for i in range(n_clusters):
       print(f"Кластер {i}: {np.sum(clusters == i)} объектов")
   ```

3. **📊 Используют неподходящие признаки**
   ```python
   # ❌ Включают ID и другие нерелевантные признаки
   features = ['client_id', 'registration_date', 'age', 'income']
   
   # ✅ Только релевантные для сегментации признаки
   features = ['age', 'income', 'purchase_frequency', 'avg_order_value']
   ```

### 💡 **Лучшие практики:**

1. **🔍 Исследуйте данные перед кластеризацией**
2. **📏 Всегда нормализуйте числовые признаки**
3. **🎯 Пробуйте разные алгоритмы и параметры**
4. **📊 Оценивайте качество несколькими метриками**
5. **💼 Интерпретируйте результаты с бизнес-точки зрения**
6. **🔄 Валидируйте результаты на новых данных**

## 🚀 Что дальше?

После освоения этой главы вы умеете:

✅ **Находить скрытые группы** в данных без учителя  
✅ **Использовать k-means и иерархическую кластеризацию** для разных задач  
✅ **Выбирать оптимальное количество кластеров** с помощью различных метрик  
✅ **Интерпретировать результаты** и применять их в бизнесе  
✅ **Создавать персонализированные стратегии** для разных сегментов клиентов

**Следующий шаг:** Научиться предсказывать конкретные значения с помощью контролируемого обучения!

## 🛠 Инструкции

Теперь переходите к практическим заданиям — вас ждут 5 увлекательных проектов по кластеризации реальных бизнес-данных:

- 📝 [Перейти к практическим заданиям](practice.md)
- ✅ [Перейти к чек-листу](checklist.md)
- 📁 [Посмотреть учебные файлы](files/README.md)

---

- 🔙 [Предыдущая глава: Глава 15 - Визуализация в Python: Matplotlib и Seaborn](../chapter-15/README.md)
- 🔜 [Следующая глава: Глава 17 - Классификация и регрессия в машинном обучении](../chapter-17/README.md)

---

- 📢 Присоединяйтесь к чату курса: https://t.me/analytics_course_chat
- 📢 Канал курса: https://t.me/analytics_course_channel