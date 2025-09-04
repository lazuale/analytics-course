# 📝 Практические задания для главы 12

📖 [Вернуться к теории](../README.md) | 📁 [Учебные файлы](../files/README.md) | ✅ [Чек-лист](../checklist.md)

## 🗺️ Задание 1: Создание интерактивных карт в Power BI

**Описание:**  
Создайте географические визуализации для анализа продаж по регионам и странам мира.

**Что нужно сделать:**

### A. Подключение данных и подготовка
1. Загрузите данные из файла `files/world_sales_data.csv`
2. В Power Query Editor проверьте:
   - Типы данных для числовых полей (Продажи, Клиенты, Широта, Долгота)
   - Корректность географических названий
   - Отсутствие пустых значений в ключевых полях

### B. Создание карты с пузырьками (Bubble Map)
1. **Создайте визуализацию "Map":**
   - Location: Город, Страна
   - Size: Продажи
   - Color saturation: Средний_чек
   - Tooltips: все поля для детальной информации

2. **Настройте форматирование:**
   - Выберите подходящую цветовую схему (синие оттенки)
   - Настройте размеры пузырьков (минимум 10px, максимум 50px)
   - Добавьте заголовок "Продажи по городам мира"

### C. Создание заполненной карты (Filled Map)
1. **Создайте визуализацию "Filled Map":**
   - Location: Страна
   - Color saturation: SUM(Продажи)
   - Tooltips: Страна, Продажи, Количество городов

2. **Настройка цветов:**
   - Используйте зеленую цветовую схему
   - Настройте диапазоны: минимум (светло-зеленый), максимум (темно-зеленый)

### D. Интерактивный анализ
1. **Добавьте фильтры:**
   - Slicer по регионам
   - Slicer по категориям товаров
   - Date range slider (если добавите временные данные)

2. **Настройте перекрестную фильтрацию:**
   - Клик по стране на Filled Map фильтрует города на Bubble Map
   - Создайте таблицу топ-10 городов по продажам
   - Настройте синхронизацию всех элементов

**Ожидаемый результат:**  
Интерактивная страница с географическим анализом продаж по 8 странам и 22 городам мира.

---

## 📊 Задание 2: Построение воронки продаж и анализ конверсий

**Описание:**  
Создайте воронки продаж для анализа этапов покупки и выявления узких мест в конверсии.

**Что нужно сделать:**

### A. Подготовка данных воронки
1. Загрузите данные из файла `files/funnel_data.csv`
2. Проверьте структуру данных:
   - 5 этапов воронки от посетителей до покупки
   - 5 источников трафика
   - 6 месяцев данных (январь-июнь 2024)

### B. Создание базовой воронки
1. **Создайте визуализацию "Funnel":**
   - Group: Этап_название
   - Values: SUM(Количество)
   - Сортировка: по полю Порядок (по возрастанию)

2. **Проверьте правильный порядок этапов:**
   - Посетители сайта (самый широкий)
   - Просмотры товаров
   - Добавления в корзину
   - Переход к оплате
   - Успешная оплата (самый узкий)

### C. Расчет конверсий с помощью DAX
```dax
// Создайте эти меры в Power BI:

Конверсия к следующему этапу = 
VAR ТекущийЭтап = SELECTEDVALUE(funnel_data[Порядок])
VAR ТекущееКоличество = SUM(funnel_data[Количество])
VAR СледующееКоличество = 
    CALCULATE(
        SUM(funnel_data[Количество]),
        funnel_data[Порядок] = ТекущийЭтап + 1
    )
RETURN
    IF(
        ТекущийЭтап < 5,
        DIVIDE(СледующееКоличество, ТекущееКоличество, 0) * 100,
        BLANK()
    )

Общая конверсия = 
DIVIDE(
    CALCULATE(SUM(funnel_data[Количество]), funnel_data[Порядок] = 5),
    CALCULATE(SUM(funnel_data[Количество]), funnel_data[Порядок] = 1),
    0
) * 100

Потери на этапе = 
VAR ТекущееКоличество = SUM(funnel_data[Количество])
VAR ПредыдущееКоличество = 
    CALCULATE(
        SUM(funnel_data[Количество]),
        funnel_data[Порядок] = SELECTEDVALUE(funnel_data[Порядок]) - 1
    )
RETURN
    IF(
        SELECTEDVALUE(funnel_data[Порядок]) > 1,
        ПредыдущееКоличество - ТекущееКоличество,
        BLANK()
    )
```

### D. Сравнительный анализ источников
1. **Создайте матрицу (Matrix):**
   - Rows: Этап_название
   - Columns: Источник
   - Values: SUM(Количество), [Конверсия к следующему этапу]

2. **Добавьте условное форматирование:**
   - Background color для конверсии:
     - Красный: < 10%
     - Желтый: 10-20%
     - Зеленый: > 20%

### E. Дашборд узких мест
1. **Создайте KPI карточки:**
   - Общая конверсия (%)
   - Лучший источник трафика
   - Худший этап воронки
   - Общие потери клиентов

2. **Добавьте графики трендов:**
   - Line chart: конверсии по месяцам
   - Column chart: потери на каждом этапе
   - Воронки по источникам трафика

**Ожидаемый результат:**  
Интерактивный дашборд воронки с анализом 5 этапов по 5 источникам трафика за 6 месяцев.

---

## 📈 Задание 3: Executive KPI дашборд с индикаторами целей

**Описание:**  
Создайте профессиональный дашборд для руководства с ключевыми показателями и индикаторами выполнения планов.

**Что нужно сделать:**

### A. Подготовка KPI данных
1. Загрузите данные из файла `files/kpi_dashboard_data.csv`
2. Изучите структуру:
   - 18 месяцев данных (2023-01 до 2024-06)
   - 4 основных KPI: выручка, клиенты, средний чек, конверсия
   - Факт и план для каждого показателя

### B. Создание Gauge диаграмм
1. **Создайте 4 gauge диаграммы:**

**Gauge 1 - Выручка:**
- Value: SUM(Выручка) для последнего месяца
- Maximum value: SUM(Цель_выручки) * 1,2
- Target: SUM(Цель_выручки)
- Colors: 0-80% красный, 80-95% желтый, 95-100%+ зеленый

**Gauge 2 - Клиенты:**
- Value: SUM(Клиенты) для последнего месяца
- Maximum: SUM(Цель_клиентов) * 1,2
- Target: SUM(Цель_клиентов)

**Gauge 3 - Средний чек:**
- Value: AVERAGE(Средний_чек) для последнего месяца
- Maximum: AVERAGE(Цель_среднего_чека) * 1,3
- Target: AVERAGE(Цель_среднего_чека)

**Gauge 4 - Конверсия:**
- Value: AVERAGE(Конверсия) для последнего месяца
- Maximum: 5,0
- Target: AVERAGE(Цель_конверсии)

### C. KPI карточки с DAX индикаторами
```dax
// Создайте эти меры для карточек:

Выручка текущий месяц = 
CALCULATE(
    SUM(kpi_dashboard_data[Выручка]),
    LASTDATE(kpi_dashboard_data[Дата])
)

Статус выручки = 
VAR ТекущаяВыручка = [Выручка текущий месяц]
VAR ЦельВыручки = 
    CALCULATE(
        SUM(kpi_dashboard_data[Цель_выручки]),
        LASTDATE(kpi_dashboard_data[Дата])
    )
VAR ПроцентВыполнения = DIVIDE(ТекущаяВыручка, ЦельВыручки)
RETURN
    SWITCH(
        TRUE(),
        ПроцентВыполнения >= 1, "🟢 Цель достигнута",
        ПроцентВыполнения >= 0,9, "🟡 Близко к цели", 
        "🔴 Требует внимания"
    )

Тренд выручки MoM = 
VAR ТекущийМесяц = [Выручка текущий месяц]
VAR ПрошлыйМесяц = 
    CALCULATE(
        SUM(kpi_dashboard_data[Выручка]),
        DATEADD(kpi_dashboard_data[Дата], -1, MONTH)
    )
VAR ИзменениеПроцент = DIVIDE(ТекущийМесяц - ПрошлыйМесяц, ПрошлыйМесяц)
RETURN
    IF(
        ИзменениеПроцент > 0, 
        "📈 +" & FORMAT(ИзменениеПроцент, "0,1%"), 
        "📉 " & FORMAT(ИзменениеПроцент, "0,1%")
    )
```

### D. Комплексный executive дашборд
1. **Макет дашборда:**
   - Верхний ряд: 4 KPI карточки с большими числами
   - Средний ряд: 4 gauge диаграммы 2x2
   - Нижний ряд: тренды и детализация

2. **Тренды и сравнения:**
   - Line chart: выручка факт vs план по месяцам
   - Area chart: динамика всех KPI
   - Bar chart: выполнение планов по месяцам (%)

### E. Интерактивность и мобильная версия
1. **Фильтры и срезы:**
   - Date slicer для выбора периода
   - Кнопки быстрого выбора (последние 3, 6, 12 месяцев)

2. **Mobile layout:**
   - Создайте отдельную мобильную версию
   - Оставьте только самые важные KPI
   - Крупные элементы для сенсорного управления

**Ожидаемый результат:**  
Professional executive дашборд с 18 месяцами KPI данных, готовый для презентации руководству.

---

## 🎨 Задание 4: Кастомные визуализации из AppSource

**Описание:**  
Расширьте возможности Power BI с помощью кастомных визуализаций и создайте уникальные элементы дашборда.

**Что нужно сделать:**

### A. Установка кастомных визуализаций
1. **Откройте AppSource в Power BI:**
   - Нажмите иконку магазина в панели визуализаций
   - Или перейдите на appsource.microsoft.com

2. **Найдите и установите:**
   - "Bullet Chart" by OKViz
   - "Waterfall Chart" by MAQ Software
   - "Advanced Donut Visual"
   - "Multi KPI" by Akvelon

### B. Bullet Charts для департаментов
1. Загрузите данные из файла `files/custom_visuals_data.csv`
2. **Отфильтруйте данные:** Тип_метрики IN ("revenue", "customers", "percentage", "score")

3. **Создайте Bullet Chart:**
   - Category: Департамент
   - Value: Текущее_значение
   - Target: Целевое_значение
   - Minimum: Минимум_плохо
   - Satisfactory: Минимум_удовл
   - Good: Минимум_хорошо

4. **Настройте цвета:**
   - Плохо: #DC143C (красный)
   - Удовлетворительно: #DAA520 (желтый)
   - Хорошо: #2E8B57 (зеленый)

### C. Waterfall Chart анализа прибыли
1. **Отфильтруйте данные:** Тип_метрики = "waterfall"
2. **Создайте Waterfall Chart:**
   - Category: Статус (по порядку появления)
   - Value: Текущее_значение
   - Настройте типы столбцов:
     - "Начальная прибыль": Starting point
     - "Рост продаж", "Новые клиенты", "Экономия затрат": Increase
     - "Снижение цен", "Увеличение расходов": Decrease
     - "Итоговая прибыль": Total

3. **Форматирование:**
   - Зеленый для положительных изменений
   - Красный для отрицательных
   - Синий для начальной и итоговой точки

### D. Advanced Donut с детализацией
1. **Отфильтруйте данные:** Тип_метрики = "donut_chart"
2. **Создайте Advanced Donut Visual:**
   - Values: Текущее_значение
   - Category: Цвет_индикатора (категории товаров)
   - Details: Статус (кварталы)

3. **Настройте drill-down:**
   - Внешнее кольцо: категории товаров
   - Внутреннее кольцо: кварталы
   - Интерактивность с другими визуализациями

### E. Интеграция в единый дашборд
1. **Создайте 3 страницы:**
   - "Bullet Analysis": bullet charts по всем департаментам
   - "Waterfall Analysis": факторный анализ прибыли
   - "Product Performance": donut charts и тренды

2. **Навигация:**
   - Кнопки переключения между страницами
   - Bookmarks для разных представлений
   - Синхронизированные фильтры

**Ожидаемый результат:**  
Многостраничный дашборд с профессиональными кастомными визуализациями для анализа 8 департаментов.

---

## 🐍 Задание 5: Интеграция Python визуализаций

**Описание:**  
Дополните Power BI статистическими возможностями Python для создания продвинутых аналитических визуализаций.

**Что нужно сделать:**

### A. Настройка Python в Power BI
1. **Установите Python (если не установлен):**
   ```bash
   # Скачайте с python.org (версия 3.8+)
   # Установите с галочкой "Add Python to PATH"
   ```

2. **Установите библиотеки:**
   ```bash
   pip install pandas matplotlib seaborn numpy scipy
   ```

3. **Настройте Power BI:**
   - File → Options → Python scripting
   - Укажите путь к python.exe
   - Перезапустите Power BI Desktop

### B. Корреляционная матрица
1. Используйте данные из `world_sales_data.csv`
2. **Создайте Python visual:**

```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Подготовка данных для корреляции
numeric_cols = ['Продажи', 'Клиенты', 'Средний_чек', 'Широта', 'Долгота']
correlation_data = dataset[numeric_cols].corr()

# Создание тепловой карты
plt.figure(figsize=(10, 8))
mask = np.triu(np.ones_like(correlation_data, dtype=bool))

sns.heatmap(correlation_data, 
            annot=True,
            cmap='RdYlBu_r',
            center=0,
            square=True,
            mask=mask,
            linewidths=0.5,
            fmt='.3f')

plt.title('Корреляционная матрица продаж по регионам', 
          fontsize=16, fontweight='bold')
plt.tight_layout()
plt.show()
```

### C. Распределения KPI данных
1. Используйте данные из `kpi_dashboard_data.csv`
2. **Создайте статистический анализ:**

```python
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Создаем subplot сетку
fig, axes = plt.subplots(2, 2, figsize=(15, 10))
fig.suptitle('Анализ распределений KPI за 18 месяцев', fontsize=16)

# 1. Гистограмма выручки
ax1 = axes[0, 0]
revenue_data = dataset['Выручка'].dropna()
ax1.hist(revenue_data, bins=12, alpha=0.7, color='lightblue', edgecolor='black')
ax1.set_title('Распределение выручки')
ax1.set_xlabel('Выручка (руб)')
ax1.set_ylabel('Частота')
ax1.grid(True, alpha=0.3)

# 2. Box plot выполнения планов
ax2 = axes[0, 1]
performance_data = [
    dataset['Выполнение_выручки'],
    dataset['Выполнение_клиентов'],
    dataset['Выполнение_конверсии']
]
box_labels = ['Выручка', 'Клиенты', 'Конверсия']
box_plot = ax2.boxplot(performance_data, labels=box_labels, patch_artist=True)
colors = ['lightcoral', 'lightgreen', 'lightblue']
for patch, color in zip(box_plot['boxes'], colors):
    patch.set_facecolor(color)
ax2.set_title('Выполнение планов (%)')
ax2.axhline(y=100, color='red', linestyle='--', alpha=0.7)
ax2.grid(True, alpha=0.3)

# 3. Временные тренды
ax3 = axes[1, 0]
months = pd.to_datetime(dataset['Дата'])
ax3.plot(months, dataset['Выручка']/1000000, 'o-', linewidth=2, color='blue')
ax3.plot(months, dataset['Цель_выручки']/1000000, '--', linewidth=2, color='red')
ax3.set_title('Выручка vs План')
ax3.set_xlabel('Месяц')
ax3.set_ylabel('Выручка (млн руб)')
ax3.legend(['Факт', 'План'])
ax3.grid(True, alpha=0.3)

# 4. Scatter plot корреляции
ax4 = axes[1, 1]
scatter = ax4.scatter(dataset['Клиенты'], dataset['Выручка']/1000000, 
                     c=dataset['Конверсия'], cmap='viridis', alpha=0.7)
ax4.set_title('Клиенты vs Выручка')
ax4.set_xlabel('Количество клиентов')
ax4.set_ylabel('Выручка (млн руб)')
plt.colorbar(scatter, ax=ax4, label='Конверсия (%)')

plt.tight_layout()
plt.show()
```

### D. Прогнозирование тренда
```python
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import numpy as np

# Подготовка данных для прогноза
dataset['Дата'] = pd.to_datetime(dataset['Дата'])
dataset = dataset.sort_values('Дата').reset_index(drop=True)

# Модель прогнозирования
X = np.arange(len(dataset)).reshape(-1, 1)
y = dataset['Выручка'].values

# Полиномиальная регрессия
poly_features = PolynomialFeatures(degree=2)
X_poly = poly_features.fit_transform(X)
model = LinearRegression()
model.fit(X_poly, y)

# Прогноз на 6 месяцев
future_months = 6
future_X = np.arange(len(dataset), len(dataset) + future_months).reshape(-1, 1)
future_X_poly = poly_features.transform(future_X)
future_pred = model.predict(future_X_poly)

# Визуализация
plt.figure(figsize=(14, 8))
plt.plot(dataset['Дата'], dataset['Выручка'], 'o-', 
         linewidth=3, markersize=6, color='blue', label='Исторические данные')
plt.plot(dataset['Дата'], dataset['Цель_выручки'], '--', 
         linewidth=2, color='red', alpha=0.7, label='План')

# Тренд и прогноз
trend_pred = model.predict(X_poly)
plt.plot(dataset['Дата'], trend_pred, ':', 
         linewidth=2, color='green', alpha=0.7, label='Тренд')

# Будущие даты
last_date = dataset['Дата'].iloc[-1]
future_dates = pd.date_range(start=last_date + pd.DateOffset(months=1), 
                           periods=future_months, freq='MS')
plt.plot(future_dates, future_pred, 's-', 
         linewidth=3, markersize=8, color='purple', label='Прогноз')

plt.title('Прогноз выручки на 6 месяцев', fontsize=16, fontweight='bold')
plt.xlabel('Период')
plt.ylabel('Выручка (руб)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
```

### E. Интеграция Python в дашборд
1. **Создайте страницу "Python Analytics":**
   - Корреляционная матрица
   - Статистические распределения
   - Прогнозирование трендов

2. **Оптимизация производительности:**
   - Ограничьте объем данных для Python (используйте фильтры)
   - Добавьте кнопки для обновления Python скриптов
   - Настройте error handling

**Ожидаемый результат:**  
Интегрированный дашборд с Python аналитикой, включающий корреляции, статистические распределения и прогнозы.

---

## 🏆 Финальный проект: Мастер-дашборд главы 12

После выполнения всех 5 заданий создайте **комплексный дашборд** который объединяет все изученные техники:

### 📋 Структура финального проекта (5 страниц):

1. **🏠 Overview** — главная страница с общими KPI и навигацией
2. **🗺️ Geography** — географический анализ с картами
3. **📊 Conversion** — воронки продаж и конверсии
4. **📈 Performance** — executive KPI дашборд
5. **🔬 Analytics** — кастомные визуализации и Python анализ

### 🎯 Требования:
- Использовать все 4 CSV файла
- Минимум 15 различных типов визуализаций
- Интерактивная навигация между страницами
- Кастомные DAX меры (минимум 10)
- Минимум 3 кастомные визуализации из AppSource
- Минимум 2 Python визуализации
- Mobile-friendly версия главной страницы

### ✅ Критерии оценки:
- Все данные корректно импортированы и связаны
- Визуализации информативны и профессионально оформлены
- Интерактивность работает корректно
- DAX формулы дают правильные результаты
- Дизайн консистентный и удобный для пользователя
- Python интеграция функционирует без ошибок

---

- 🔙 [Предыдущая глава: Глава 11 - Power BI — создание дашбордов](../chapter-11/README.md)
- 🔜 [Следующая глава: Глава 13 - Основы DAX: вычисляемые столбцы и меры](../chapter-13/README.md)

---

- 📢 Присоединяйтесь к чату курса: [https://t.me/analytics_course_chat](https://t.me/analytics_course_chat)
- 📢 Канал курса: [https://t.me/analytics_course_channel](https://t.me/analytics_course_channel)