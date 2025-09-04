# 📝 Практические задания для главы 9

📖 [Вернуться к теории](../README.md) | 📁 [Учебные файлы](../files/README.md) | ✅ [Чек-лист](../checklist.md)

## 📈 Задание 1: Анализ компонентов временного ряда

**Описание:**  
Научитесь выявлять и анализировать основные компоненты временного ряда: тренд, сезонность и случайные колебания.

**Что нужно сделать:**
1. Работайте с файлом [`files/monthly_sales.csv`](files/monthly_sales.csv) - данные о продажах магазина за 5 лет

### A. Визуальный анализ временного ряда
   - Постройте график продаж по времени в Excel
   - Определите визуально: есть ли тренд? сезонность? цикличность?
   - Выделите периоды роста и спада

### B. Выделение тренда методом скользящих средних
   1. **Простая скользящая средняя:**
      ```excel
      =СРЗНАЧ(СМЕЩ(B2;-5;0;12;1))  # 12-месячная скользящая средняя
      ```
      
   2. **Центрированная скользящая средняя:**
      - Рассчитайте 12-месячную скользящую среднюю
      - Центрируйте ее для удаления сезонности
      
   3. **Сравнение разных периодов:**
      - 3-месячная, 6-месячная, 12-месячная
      - Как изменяется сглаживание при увеличении окна?

### C. Python реализация
```python
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose

# Загрузка данных
df = pd.read_csv('monthly_sales.csv', sep=';', decimal=',', parse_dates=['date'])
df = df.set_index('date')

# Декомпозиция временного ряда
decomposition = seasonal_decompose(df['sales'], model='multiplicative', period=12)

# Визуализация компонентов
fig, axes = plt.subplots(4, 1, figsize=(12, 10))
decomposition.observed.plot(ax=axes[0], title='Исходные данные')
decomposition.trend.plot(ax=axes[1], title='Тренд')
decomposition.seasonal.plot(ax=axes[2], title='Сезонность')
decomposition.resid.plot(ax=axes[3], title='Остатки')
plt.tight_layout()
plt.show()
```

2. **Анализ сезонности:**
   - Рассчитайте сезонные индексы для каждого месяца
   - В какие месяцы продажи максимальные/минимальные?
   - Постройте график средних продаж по месяцам

3. **Анализ остатков:**
   - Есть ли в остатках еще какие-то паттерны?
   - Проверьте остатки на нормальность
   - Найдите выбросы и аномальные периоды

**Ожидаемый результат:**  
Анализ компонентов `time_series_decomposition.xlsx` с выделением тренда, сезонности и интерпретацией.

---

## 📊 Задание 2: Методы сглаживания и простейшие прогнозы

**Описание:**  
Изучите различные методы сглаживания временных рядов и научитесь делать простые прогнозы.

**Что нужно сделать:**
1. Используйте файл [`files/daily_visitors.csv`](files/daily_visitors.csv) - ежедневная посещаемость сайта

### A. Простые скользящие средние
   1. **Различные окна сглаживания:**
      - 7-дневная (недельная)
      - 30-дневная (месячная)
      - 90-дневная (квартальная)
      
   2. **Сравнение качества сглаживания:**
      - Какое окно лучше сглаживает шум?
      - Какое лучше сохраняет тренды?
      - Влияние размера окна на задержку сигнала

### B. Взвешенные скользящие средние
   ```excel
   # Линейные веса (больший вес последним наблюдениям)
   =(B10*1 + B9*2 + B8*3 + B7*4 + B6*5 + B5*6 + B4*7)/28
   
   # Экспоненциальные веса
   =α*B10 + (1-α)*C9  где α = 0.3
   ```

### C. Экспоненциальное сглаживание
```python
# Простое экспоненциальное сглаживание
from statsmodels.tsa.holtwinters import SimpleExpSmoothing

model = SimpleExpSmoothing(ts)
fitted_model = model.fit(smoothing_level=0.3)

# Прогноз на 30 дней вперед
forecast = fitted_model.forecast(steps=30)

# Подбор оптимального параметра сглаживания
alphas = [0.1, 0.3, 0.5, 0.7, 0.9]
mse_scores = []

for alpha in alphas:
    model = SimpleExpSmoothing(ts).fit(smoothing_level=alpha)
    mse = ((ts - model.fittedvalues)**2).mean()
    mse_scores.append(mse)
    
optimal_alpha = alphas[np.argmin(mse_scores)]
```

2. **Прогнозирование:**
   - Разделите данные на обучающую (80%) и тестовую (20%) выборки
   - Постройте прогнозы каждым методом
   - Сравните точность прогнозов по MAE и RMSE

3. **Обработка аномалий:**
   - Найдите выбросы в данных (выходные, праздники, сбои)
   - Как выбросы влияют на прогнозы?
   - Примените робастные методы сглаживания

**Ожидаемый результат:**  
Сравнение методов сглаживания `smoothing_methods_comparison.xlsx` с оценкой точности прогнозов.

---

## 🔍 Задание 3: Продвинутое экспоненциальное сглаживание

**Описание:**  
Примените методы Холта и Холта-Винтерса для временных рядов с трендом и сезонностью.

**Что нужно сделать:**
1. Работайте с файлом [`files/quarterly_revenue.csv`](files/quarterly_revenue.csv) - квартальная выручка компании

### A. Метод Холта (двойное экспоненциальное сглаживание)
   **Для рядов с трендом, но без сезонности**

```python
from statsmodels.tsa.holtwinters import ExponentialSmoothing

# Модель Холта
model_holt = ExponentialSmoothing(ts, trend='add')
fitted_holt = model_holt.fit()

# Прогноз на 8 кварталов (2 года)
forecast_holt = fitted_holt.forecast(steps=8)

# Анализ параметров
print(f"Уровень (alpha): {fitted_holt.params['smoothing_level']:.3f}")
print(f"Тренд (beta): {fitted_holt.params['smoothing_trend']:.3f}")
```

### B. Метод Холта-Винтерса (тройное экспоненциальное сглаживание)
   **Для рядов с трендом и сезонностью**

```python
# Аддитивная сезонность
model_add = ExponentialSmoothing(ts, trend='add', seasonal='add', seasonal_periods=4)
fitted_add = model_add.fit()

# Мультипликативная сезонность  
model_mult = ExponentialSmoothing(ts, trend='add', seasonal='mul', seasonal_periods=4)
fitted_mult = model_mult.fit()

# Сравнение моделей
print(f"AIC аддитивной: {fitted_add.aic:.2f}")
print(f"AIC мультипликативной: {fitted_mult.aic:.2f}")
```

2. **Выбор типа сезонности:**
   - Постройте графики остатков для обеих моделей
   - Какая модель лучше подходит для ваших данных?
   - Как интерпретировать аддитивную vs мультипликативную сезонность?

3. **Анализ точности:**
   - Сравните прогнозы методов Холта и Холта-Винтерса
   - Рассчитайте MAPE, MAE, RMSE на тестовой выборке
   - Постройте доверительные интервалы для прогнозов

### C. Практическое применение
4. **Создайте автоматическую систему прогнозирования:**
   ```python
   def auto_forecast(data, periods=4):
       """Автоматический выбор лучшей модели и прогноз"""
       models = {
           'Simple': SimpleExpSmoothing(data),
           'Holt': ExponentialSmoothing(data, trend='add'),
           'HoltWinters_add': ExponentialSmoothing(data, trend='add', seasonal='add', seasonal_periods=4),
           'HoltWinters_mult': ExponentialSmoothing(data, trend='add', seasonal='mul', seasonal_periods=4)
       }
       
       best_aic = float('inf')
       best_model = None
       
       for name, model in models.items():
           try:
               fitted = model.fit()
               if fitted.aic < best_aic:
                   best_aic = fitted.aic
                   best_model = (name, fitted)
           except:
               continue
       
       forecast = best_model[1].forecast(steps=periods)
       return best_model[0], forecast
   ```

**Ожидаемый результат:**  
Модели экспоненциального сглаживания `exponential_smoothing_models.xlsx` с автоматическим выбором лучшей модели.

---

## 📈 Задание 4: Анализ трендов и структурных изменений

**Описание:**  
Научитесь выявлять изменения в трендах и структурные сдвиги во временных рядах.

**Что нужно сделать:**
1. Используйте файл [`files/stock_price.csv`](files/stock_price.csv) - цены акций за несколько лет

### A. Анализ различных типов трендов
   1. **Линейный тренд:**
      ```python
      from scipy import stats
      
      # Простая линейная регрессия по времени
      x = np.arange(len(ts))
      slope, intercept, r_value, p_value, std_err = stats.linregress(x, ts.values)
      
      trend_line = intercept + slope * x
      print(f"Тренд: {slope:.2f} руб./день (R²={r_value**2:.3f})")
      ```

   2. **Полиномиальный тренд:**
      ```python
      # Полином 2-й степени
      coeffs = np.polyfit(x, ts.values, deg=2)
      poly_trend = np.polyval(coeffs, x)
      
      # Сравнение с линейным трендом
      from sklearn.metrics import r2_score
      linear_r2 = r2_score(ts.values, trend_line)
      poly_r2 = r2_score(ts.values, poly_trend)
      ```

   3. **Экспоненциальный тренд:**
      ```python
      # Линеаризация через логарифм
      log_ts = np.log(ts)
      slope_log, intercept_log, _, _, _ = stats.linregress(x, log_ts)
      exp_trend = np.exp(intercept_log + slope_log * x)
      ```

### B. Выявление структурных изменений
   2. **Точки структурных сдвигов:**
      ```python
      import ruptures as rpt
      
      # Поиск точек изменения тренда
      model = "l2"  # Изменения в среднем
      algo = rpt.Pelt(model=model).fit(ts.values)
      change_points = algo.predict(pen=10)
      
      # Визуализация точек сдвига
      plt.figure(figsize=(12, 6))
      plt.plot(ts)
      for cp in change_points[:-1]:
          plt.axvline(ts.index[cp], color='red', linestyle='--', alpha=0.7)
      plt.title('Структурные изменения во временном ряду')
      ```

   3. **Анализ волатильности:**
      - Рассчитайте скользящее стандартное отклонение
      - Найдите периоды повышенной и пониженной волатильности
      - Связаны ли изменения волатильности с внешними событиями?

### C. Бизнес-интерпретация
   4. **Связь с внешними событиями:**
      - Отметьте на графике важные события (запуск продукта, кризис, и т.д.)
      - Как события влияют на тренд и волатильность?
      - Можно ли предсказать структурные изменения?

   5. **Прогнозирование с учетом структурных изменений:**
      - Постройте прогноз только на последнем стабильном периоде
      - Сравните с прогнозом по всем данным
      - Какой подход дает более точные результаты?

**Ожидаемый результат:**  
Анализ трендов `trend_analysis.xlsx` с выявлением структурных изменений и их бизнес-интерпретацией.

---

## 🎯 Задание 5: Комплексный анализ веб-аналитики

**Описание:**  
Проведите полный анализ временных рядов веб-аналитики с множественными метриками и построением дашборда.

**Что нужно сделать:**

### Бизнес-кейс: Анализ эффективности сайта
Интернет-магазин хочет понять динамику ключевых метрик и построить систему прогнозирования трафика.

1. **Данные:** файл [`files/web_analytics.csv`](files/web_analytics.csv) содержит:
   - Ежедневные визиты
   - Конверсию в покупки
   - Выручку
   - Источники трафика
   - События (реклама, праздники, акции)

### Этап 1: Исследовательский анализ
2. **Многомерный анализ временных рядов:**
   ```python
   # Корреляционный анализ метрик во времени
   metrics = ['visits', 'conversion_rate', 'revenue', 'avg_order_value']
   correlation_over_time = []
   
   for i in range(30, len(df)):
       window_data = df[metrics].iloc[i-30:i]
       corr_matrix = window_data.corr()
       correlation_over_time.append(corr_matrix.iloc[0, 1])  # visits vs conversion
   
   plt.plot(correlation_over_time)
   plt.title('Динамика корреляции визитов и конверсии')
   ```

3. **Анализ источников трафика:**
   - Декомпозиция каждого источника отдельно
   - Какие источники наиболее стабильны/волатильны?
   - Сезонные паттерны по источникам

### Этап 2: Влияние внешних событий
4. **Event Study анализ:**
   ```python
   def analyze_event_impact(ts, event_date, window_before=7, window_after=7):
       """Анализ влияния события на временной ряд"""
       event_idx = ts.index.get_loc(event_date)
       
       before = ts.iloc[event_idx-window_before:event_idx].mean()
       after = ts.iloc[event_idx:event_idx+window_after].mean()
       
       impact = (after - before) / before * 100
       return impact
   
   # Анализ влияния рекламных кампаний
   campaign_dates = ['2023-03-15', '2023-07-20', '2023-11-25']
   for date in campaign_dates:
       impact = analyze_event_impact(df['visits'], date)
       print(f"Влияние кампании {date}: {impact:.1f}%")
   ```

5. **Сезонные эффекты:**
   - Внутринедельная сезонность (будни vs выходные)
   - Месячная сезонность (зарплатная)
   - Годовая сезонность (праздники, каникулы)

### Этап 3: Прогнозирование
6. **Ансамбль моделей:**
   ```python
   from sklearn.ensemble import VotingRegressor
   from sklearn.linear_model import LinearRegression
   
   # Подготовка признаков
   def create_features(ts):
       df_features = pd.DataFrame(index=ts.index)
       
       # Лаговые переменные
       for lag in [1, 7, 30]:
           df_features[f'lag_{lag}'] = ts.shift(lag)
       
       # Скользящие средние
       df_features['ma_7'] = ts.rolling(7).mean()
       df_features['ma_30'] = ts.rolling(30).mean()
       
       # Временные признаки
       df_features['day_of_week'] = ts.index.dayofweek
       df_features['month'] = ts.index.month
       df_features['is_weekend'] = (ts.index.dayofweek >= 5).astype(int)
       
       return df_features
   
   # Объединение статистических и ML подходов
   exp_smoothing_forecast = fitted_model.forecast(30)
   
   features = create_features(df['visits']).dropna()
   ml_model = LinearRegression()
   ml_model.fit(features[:-30], df['visits'][features.index[:-30]])
   ml_forecast = ml_model.predict(features[-30:])
   
   # Взвешенный ансамбль
   ensemble_forecast = 0.6 * exp_smoothing_forecast + 0.4 * ml_forecast
   ```

### Этап 4: Дашборд и мониторинг
7. **Создайте систему мониторинга:**
   - KPI дашборд с ключевыми метриками
   - Автоматические алерты при аномальных значениях
   - Сравнение фактических данных с прогнозами

8. **Бизнес-рекомендации:**
   - Оптимальное время для запуска рекламных кампаний
   - Прогноз нагрузки на сайт для планирования ресурсов
   - Ожидаемая выручка на следующий квартал
   - Риски и возможности на основе трендов

### Этап 5: Автоматизация
9. **Создайте автоматическую систему:**
   ```python
   class WebAnalyticsForecaster:
       def __init__(self):
           self.models = {}
           self.is_fitted = False
       
       def fit(self, data):
           """Обучение всех моделей"""
           for metric in ['visits', 'conversion_rate', 'revenue']:
               # Выбор лучшей модели для каждой метрики
               best_model = self._select_best_model(data[metric])
               self.models[metric] = best_model
           
           self.is_fitted = True
       
       def forecast(self, periods=30):
           """Прогноз на заданный период"""
           forecasts = {}
           for metric, model in self.models.items():
               forecasts[metric] = model.forecast(periods)
           
           return pd.DataFrame(forecasts)
       
       def detect_anomalies(self, data):
           """Выявление аномалий в реальном времени"""
           # Реализация алгоритма выявления аномалий
           pass
   
   # Использование
   forecaster = WebAnalyticsForecaster()
   forecaster.fit(df)
   future_forecast = forecaster.forecast(30)
   ```

**Ожидаемый результат:**  
Комплексная система анализа `web_analytics_dashboard.xlsx` с прогнозами, алертами и бизнес-рекомендациями.

---

## 💡 Методические рекомендации

### 📈 Выбор метода сглаживания:
```
Характер данных → Рекомендуемый метод
├─ Без тренда и сезонности → Простое экспоненциальное сглаживание
├─ Есть тренд, нет сезонности → Метод Холта
├─ Есть тренд и сезонность → Метод Холта-Винтерса
└─ Сложные паттерны → ARIMA или машинное обучение
```

### 📊 Параметры сглаживания:
- **α (уровень) = 0.1-0.3** — медленная адаптация, хорошо для стабильных рядов
- **α = 0.7-0.9** — быстрая адаптация, хорошо для изменчивых рядов
- **β (тренд) обычно < α** — тренд изменяется медленнее уровня
- **γ (сезонность) = 0.1-0.3** — сезонные паттерны стабильны

### 🎯 Оценка качества прогнозов:
```excel
MAE = СРЗНАЧ(ABS(Фактические - Прогноз))
RMSE = КОРЕНЬ(СРЗНАЧ((Фактические - Прогноз)^2))
MAPE = СРЗНАЧ(ABS((Фактические - Прогноз)/Фактические)) * 100%
```

### ❓ Решение проблем:

#### Нестационарность:
- Удалите тренд через разности: ΔY(t) = Y(t) - Y(t-1)
- Примените логарифмическую трансформацию для стабилизации дисперсии
- Используйте сезонные разности для устранения сезонности

#### Выбросы и аномалии:
- Используйте робастные методы (медианное сглаживание)
- Предварительно очистите данные от выбросов
- Примените адаптивные методы с переменными параметрами

#### Структурные изменения:
- Используйте только недавние данные для прогноза
- Примените методы с забыванием (экспоненциальное сглаживание)
- Мониторьте качество прогнозов и переобучайте модели

---

- 🔙 [Предыдущая глава: Глава 8 - Корреляция и регрессия](../chapter-08/README.md)
- 🔜 [Следующая глава: Глава 10 - Когортный анализ и кластеризация](../chapter-10/README.md)

---

- 📢 Присоединяйтесь к чату курса: [https://t.me/analytics_course_chat](https://t.me/analytics_course_chat)
- 📢 Канал курса: [https://t.me/analytics_course_channel](https://t.me/analytics_course_channel)