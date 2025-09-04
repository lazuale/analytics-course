# 📝 Практические задания для главы 10

📖 [Вернуться к теории](../README.md) | 📁 [Учебные файлы](../files/README.md) | ✅ [Чек-лист](../checklist.md)

## 👥 Задание 1: Базовый когортный анализ

**Описание:**  
Изучите основы когортного анализа и научитесь строить таблицы retention для понимания поведения клиентов во времени.

**Что нужно сделать:**

### A. Создание когорт по месяцу регистрации
1. Работайте с файлом `files/user_transactions.csv` — данные о транзакциях пользователей за 2 года
2. **Определение первой активности в Excel:**
   ```excel
   # Первый месяц активности каждого пользователя
   =ТЕКСТ(МИН(ЕСЛИ($A$2:$A$1000=A2;$B$2:$B$1000));"ГГГГ-ММ")
   ```
3. **Расчет периода от первой активности:**
   ```excel
   # Номер месяца от первой транзакции
   =(ГОД(B2)-ГОД(E2))*12+МЕСЯЦ(B2)-МЕСЯЦ(E2)
   ```

### B. Построение retention таблицы
1. **Создание сводной таблицы:**
   - Строки: Когорта (месяц первой активности)
   - Столбцы: Период (0, 1, 2, 3... месяцев)
   - Значения: Количество уникальных пользователей
      
2. **Расчет retention rates:**
   ```excel
   # Retention = Активные пользователи в периоде / Размер когорты
   =C2/$B$2  # Где B2 - размер когорты (период 0)
   ```

### C. Python реализация
```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Загрузка данных
df = pd.read_csv('files/user_transactions.csv', sep=';')
df['transaction_date'] = pd.to_datetime(df['transaction_date'])

# Определение когорт
df['order_period'] = df['transaction_date'].dt.to_period('M')
df['cohort_group'] = df.groupby('user_id')['transaction_date'].transform('min').dt.to_period('M')

# Расчет номера периода
df['period_number'] = (df['order_period'] - df['cohort_group']).apply(lambda x: x.n)

# Создание когортной таблицы
cohort_data = df.groupby(['cohort_group', 'period_number'])['user_id'].nunique().reset_index()
cohort_table = cohort_data.pivot(index='cohort_group', columns='period_number', values='user_id')

# Размеры когорт
cohort_sizes = cohort_table.iloc[:,0]

# Retention rates
retention_table = cohort_table.divide(cohort_sizes, axis=0)

# Визуализация
plt.figure(figsize=(15, 8))
sns.heatmap(retention_table, annot=True, fmt='.1%', cmap='YlOrRd')
plt.title('Retention Rates по когортам')
plt.ylabel('Когорта')
plt.xlabel('Период')
plt.show()
```

**Анализ результатов:**
- Какие когорты показывают лучший retention?
- Как меняется retention с течением времени?
- В какой период происходит наибольший отток?
- Есть ли сезонные паттерны в retention?

**Ожидаемый результат:**  
Когортная таблица с retention rates и анализом поведения когорт.

---

## 💰 Задание 2: LTV анализ и revenue-когорты

**Описание:**  
Углубите анализ когорт, рассчитав revenue-метрики и пожизненную ценность клиентов.

**Что нужно сделать:**

### A. Revenue по когортам
1. Используйте тот же файл `files/user_transactions.csv`
2. **Выручка на пользователя:**
   ```python
   # Revenue таблица
   revenue_data = df.groupby(['cohort_group', 'period_number'])['transaction_amount'].sum().reset_index()
   revenue_table = revenue_data.pivot(index='cohort_group', columns='period_number', values='transaction_amount')
   
   # Revenue per user
   revenue_per_user = revenue_table.divide(cohort_sizes, axis=0)
   
   # Кумулятивная выручка на пользователя
   cumulative_revenue = revenue_per_user.cumsum(axis=1)
   ```

### B. LTV прогнозирование
1. **Простое LTV:**
   ```python
   # Экстраполяция на основе трендов
   def calculate_ltv(cohort_revenue, periods_to_extrapolate=12):
       # Находим тренд последних N периодов
       recent_periods = cohort_revenue.dropna().tail(6)
       if len(recent_periods) < 3:
           return cohort_revenue.sum()
       
       # Простая экстраполяция на основе среднего
       avg_monthly_revenue = recent_periods.mean()
       extrapolated_revenue = avg_monthly_revenue * periods_to_extrapolate
       
       return cohort_revenue.sum() + extrapolated_revenue
   
   # LTV для каждой когорты
   ltv_by_cohort = cumulative_revenue.apply(calculate_ltv, axis=1)
   ```

2. **Сравнительный анализ когорт:**
   - Ранжируйте когорты по LTV
   - Выявите факторы успешных когорт
   - Рассчитайте payback period для каждой когорты

**Ожидаемый результат:**  
LTV анализ с прогнозами выручки и рекомендациями по каналам.

---

## 🎯 Задание 3: RFM-анализ и сегментация

**Описание:**  
Проведите RFM-анализ клиентов для создания персонализированных маркетинговых стратегий.

**Что нужно сделать:**

### A. Расчет RFM метрик
1. Работайте с файлом `files/customer_database.csv` — полная база клиентов
2. **Recency, Frequency, Monetary:**
   ```python
   from datetime import datetime
   
   # Опорная дата (например, сегодня)
   current_date = df['last_purchase_date'].max() + pd.Timedelta(days=1)
   
   # Расчет RFM
   rfm = df.groupby('customer_id').agg({
       'last_purchase_date': lambda x: (current_date - x.max()).days,
       'purchase_count': 'sum',
       'total_amount': 'sum'
   })
   
   rfm.columns = ['recency', 'frequency', 'monetary']
   ```

3. **Квинтильное разбиение:**
   ```python
   # Разбивка на 5 групп (квинтилей)
   rfm['r_score'] = pd.qcut(rfm['recency'], 5, labels=[5,4,3,2,1])  # Меньше дней = лучше
   rfm['f_score'] = pd.qcut(rfm['frequency'].rank(method='first'), 5, labels=[1,2,3,4,5])
   rfm['m_score'] = pd.qcut(rfm['monetary'], 5, labels=[1,2,3,4,5])
   
   # RFM строка
   rfm['rfm_score'] = rfm['r_score'].astype(str) + rfm['f_score'].astype(str) + rfm['m_score'].astype(str)
   ```

### B. Создание клиентских сегментов
1. **Правила сегментации:**
   ```python
   def segment_customers(row):
       if row['rfm_score'] in ['555', '554', '544', '545', '454', '455', '445']:
           return 'Чемпионы'
       elif row['rfm_score'] in ['543', '444', '435', '355', '434', '343', '344']:
           return 'Лояльные клиенты'
       elif row['rfm_score'] in ['512', '511', '422', '421', '412', '411']:
           return 'Потенциально лояльные'
       elif row['rfm_score'] in ['512', '411', '311', '211', '413', '414']:
           return 'Новые клиенты'
       elif row['rfm_score'] in ['155', '254', '144', '214', '215', '115']:
           return 'Нуждающиеся во внимании'
       elif row['rfm_score'] in ['155', '144', '214', '215', '135', '125']:
           return 'Спящие'
       elif row['rfm_score'] in ['124', '123', '133', '142', '134']:
           return 'Рискуем потерять'
       else:
           return 'Потерянные'
   
   rfm['segment'] = rfm.apply(segment_customers, axis=1)
   ```

2. **Стратегии для каждого сегмента:**
   - Чемпионы: VIP программы и эксклюзивные предложения
   - Лояльные клиенты: Программы лояльности и перекрестные продажи
   - Потенциально лояльные: Персонализированные предложения
   - Новые клиенты: Приветственные кампании
   - Нуждающиеся во внимании: Реактивация специальными предложениями
   - Спящие: Win-back кампании с большими скидками
   - Рискуем потерять: Срочные меры удержания
   - Потерянные: Минимальные автоматические усилия

**Ожидаемый результат:**  
RFM сегментация со стратегиями для каждого сегмента и планом действий.

---

## 🔍 Задание 4: Кластеризация клиентов

**Описание:**  
Примените методы машинного обучения для автоматической сегментации клиентов без предварительных предположений.

**Что нужно сделать:**

### A. K-means кластеризация
1. Используйте файл `files/customer_features.csv` с расширенными характеристиками клиентов
2. **Подготовка данных:**
   ```python
   from sklearn.preprocessing import StandardScaler
   from sklearn.cluster import KMeans
   from sklearn.metrics import silhouette_score
   
   # Выбор признаков для кластеризации
   features = ['recency', 'frequency', 'monetary', 'avg_transaction_amount', 
              'avg_days_between_purchases', 'customer_lifetime_days']
   
   X = df[features].copy()
   X = X.fillna(X.median())  # Обработка пропущенных значений
   
   # Стандартизация
   scaler = StandardScaler()
   X_scaled = scaler.fit_transform(X)
   ```

3. **Определение оптимального количества кластеров:**
   ```python
   # Метод локтя и силуэтный анализ
   inertias = []
   silhouette_scores = []
   K = range(2, 11)
   
   for k in K:
       kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
       kmeans.fit(X_scaled)
       inertias.append(kmeans.inertia_)
       silhouette_scores.append(silhouette_score(X_scaled, kmeans.labels_))
   
   # Выбор оптимального k
   optimal_k = K[np.argmax(silhouette_scores)]
   ```

### B. Иерархическая кластеризация
1. **Построение дендрограммы:**
   ```python
   from scipy.cluster.hierarchy import dendrogram, linkage
   
   # Иерархическая кластеризация
   linkage_matrix = linkage(X_scaled[:1000], method='ward')  # Выборка для скорости
   
   # Дендрограмма
   plt.figure(figsize=(15, 8))
   dendrogram(linkage_matrix, truncate_mode='level', p=10)
   plt.title('Дендрограмма иерархической кластеризации')
   plt.show()
   ```

### C. Анализ полученных кластеров
1. **Характеристики кластеров:**
   ```python
   # Финальная кластеризация
   kmeans_final = KMeans(n_clusters=optimal_k, random_state=42)
   df['cluster'] = kmeans_final.fit_predict(X_scaled)
   
   # Анализ кластеров
   cluster_analysis = df.groupby('cluster')[features].agg(['mean', 'std', 'count']).round(2)
   ```

2. **Интерпретация и именование кластеров:**
   - Определите характеристики каждого кластера
   - Дайте понятные бизнес-названия сегментам
   - Создайте профили типичных клиентов

**Ожидаемый результат:**  
Кластерный анализ с характеристиками автоматически найденных сегментов.

---

## 🚀 Задание 5: Интегрированная система сегментации

**Описание:**  
Создайте комплексную систему сегментации, объединяющую когортный анализ, RFM и кластеризацию для эффективного управления клиентами.

**Что нужно сделать:**

### Бизнес-кейс: CRM система нового поколения
E-commerce компания хочет создать автоматизированную систему управления клиентами, которая:
- Автоматически сегментирует новых клиентов
- Отслеживает движение клиентов между сегментами
- Предлагает персонализированные маркетинговые действия
- Прогнозирует LTV и churn риски

### Этап 1: Мультиметодная сегментация
1. Используйте файл `files/integrated_customer_data.csv`
2. **Сравнение подходов:**
   ```python
   # Объединение результатов разных методов
   customer_segments = pd.DataFrame({
       'customer_id': df['customer_id'],
       'rfm_segment': df['rfm_segment'],
       'cluster_segment': df['cluster'],
       'cohort': df['cohort_month'],
       'cohort_performance': df['cohort_retention_rate']
   })
   
   # Создание мета-сегментов
   def create_meta_segment(row):
       if row['rfm_segment'] in ['Чемпионы', 'Лояльные клиенты'] and row['cluster_segment'] in [0, 1]:
           return 'Премиум клиенты'
       elif row['rfm_segment'] in ['Новые клиенты', 'Потенциально лояльные']:
           return 'Развивающиеся клиенты'
       elif row['rfm_segment'] in ['Спящие', 'Рискуем потерять']:
           return 'Клиенты риска'
       else:
           return 'Стандартные клиенты'
   
   customer_segments['meta_segment'] = customer_segments.apply(create_meta_segment, axis=1)
   ```

### Этап 2: Предиктивная модель
1. **Модель прогнозирования churn:**
   ```python
   from sklearn.ensemble import RandomForestClassifier
   from sklearn.model_selection import train_test_split
   
   # Подготовка признаков для модели churn
   churn_features = [
       'recency', 'frequency', 'monetary',
       'avg_days_between_purchases', 'customer_lifetime_days',
       'seasonal_concentration', 'price_sensitivity'
   ]
   
   # Целевая переменная: не было покупок последние 90 дней
   df['is_churned'] = (df['recency'] > 90).astype(int)
   
   X = df[churn_features]
   y = df['is_churned']
   
   X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
   
   # Обучение модели
   churn_model = RandomForestClassifier(n_estimators=100, random_state=42)
   churn_model.fit(X_train, y_train)
   
   # Вероятности churn для всех клиентов
   df['churn_probability'] = churn_model.predict_proba(X)[:, 1]
   ```

### Этап 3: Автоматизированные рекомендации
1. **Система рекомендаций:**
   ```python
   def generate_marketing_actions(customer_row):
       """Генерация персонализированных маркетинговых действий"""
       actions = []
       
       # На основе мета-сегмента
       segment = customer_row['meta_segment']
       churn_risk = customer_row['churn_probability']
       ltv = customer_row['predicted_ltv']
       
       if segment == 'Премиум клиенты':
           actions.extend(['VIP программа', 'Персональный менеджер'])
       elif segment == 'Развивающиеся клиенты':
           actions.extend(['Онбординг программа', 'Образовательный контент'])
       elif segment == 'Клиенты риска':
           actions.extend(['Win-back кампания', 'Персональная скидка'])
       
       # На основе риска оттока
       if churn_risk > 0.7:
           actions.append('СРОЧНО: Личный контакт менеджера')
       elif churn_risk > 0.4:
           actions.append('Профилактическая кампания')
       
       return '; '.join(actions)
   
   df['recommended_actions'] = df.apply(generate_marketing_actions, axis=1)
   ```

### Этап 4: Дашборд и мониторинг
1. **Создайте исполнительный дашборд:**
   - KPI по сегментам (размер, LTV, churn rate)
   - Тренды миграции между сегментами
   - Прогнозы выручки по сегментам
   - Приоритетные действия на этой неделе

2. **Автоматические алерты:**
   - Высокий риск оттока у ценных клиентов
   - Необычные изменения в размерах сегментов
   - Снижение retention в ключевых когортах

**Ожидаемый результат:**  
Интегрированная CRM система с автоматической сегментацией, прогнозами и рекомендациями.

---

## 💡 Методические рекомендации

### 👥 Когортный анализ:
- **Начинайте с месячных когорт** — наиболее популярный и понятный интервал
- **Анализируйте первые 6-12 периодов** — достаточно для понимания паттернов
- **Ищите внешние причины** — связывайте изменения retention с бизнес-событиями
- **Сравнивайте каналы привлечения** — разные источники дают разное качество клиентов

### 🎯 RFM сегментация:
- **Адаптируйте под бизнес** — B2B и B2C требуют разных подходов
- **Регулярно пересчитывайте** — сегменты должны быть актуальными
- **Фокусируйтесь на действиях** — каждый сегмент должен иметь стратегию
- **Тестируйте подходы** — проверяйте эффективность разных стратегий

### 🔍 Кластеризация:
- **Выбирайте релевантные признаки** — больше переменных ≠ лучше результат
- **Стандартизируйте данные** — разные шкалы могут исказить результат
- **Интерпретируйте кластеры** — каждая группа должна иметь бизнес-смысл
- **Валидируйте результаты** — проверяйте стабильность на новых данных

---

- 🔙 [Предыдущая глава: Глава 9 - Временные ряды и анализ трендов](../chapter-09/README.md)  
- 🔜 [Следующая глава: Глава 11 - Power BI — создание дашбордов](../chapter-11/README.md)

---

- 📢 Присоединяйтесь к чату курса: [https://t.me/analytics_course_chat](https://t.me/analytics_course_chat)
- 📢 Канал курса: [https://t.me/analytics_course_channel](https://t.me/analytics_course_channel)