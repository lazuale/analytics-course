# 📊 Глава 15: Визуализация в Python — превращаем данные в истории!

## 🎯 Что вы изучите

После изучения этой главы вы сможете:

- 🎨 **Создавать профессиональные графики** с помощью Matplotlib и Seaborn
- 📊 **Рассказывать истории данными** через эффективную визуализацию
- 🔍 **Находить закономерности** в данных с помощью статистических графиков
- 🎭 **Настраивать стиль и оформление** для презентаций и отчетов
- 📱 **Создавать интерактивные дашборды** прямо в Python

## 🌟 Python визуализация простыми словами

**Визуализация в Python** — это как иметь личную студию дизайна прямо в коде. Вы берете сухие цифры и превращаете их в красивые, понятные истории.

### 🎭 **Метафора: Python визуализация как киностудия**

Представьте, что вы режиссер фильма о ваших данных:

- 📊 **Matplotlib** — это ваша съемочная команда (камеры, свет, звук)
- 🎨 **Seaborn** — это талантливый художник по костюмам (делает все красиво)
- 📈 **Pandas** — это сценарист (готовит данные к съемкам)
- 🎬 **Ваш код** — это режиссерский сценарий (как все должно выглядеть)

### 💼 **Зачем это нужно аналитику в 2025:**

**Без визуализации:**
```
"Продажи выросли на 23.4% по сравнению с прошлым кварталом"
Реакция руководства: 😴 "Ну и что?"
```

**С визуализацией:**
```python
# Красивый график роста с трендами
plt.figure(figsize=(12, 6))
sns.lineplot(data=sales_data, x='month', y='revenue')
plt.title('🚀 Взрывной рост продаж!')
```
Реакция руководства: 🤩 "Вау! Расскажите подробнее!"

## 🎨 Знакомимся с инструментами

### 📊 **Matplotlib — универсальный солдат**

**Matplotlib** — это швейцарский нож визуализации. Может все, но иногда требует усилий.

**Философия:** "Дайте мне контроль над каждым пикселем!"

```python
import matplotlib.pyplot as plt
import numpy as np

# Простейший график
x = [1, 2, 3, 4, 5]
y = [2, 4, 6, 8, 10]

plt.plot(x, y)
plt.title('Мой первый график! 📈')
plt.xlabel('Время')
plt.ylabel('Продажи')
plt.show()
```

**Когда использовать:**
- ✅ Нужен полный контроль над внешним видом
- ✅ Создаете уникальные типы графиков
- ✅ Интегрируете в веб-приложения
- ✅ Сохраняете в различные форматы

### 🎨 **Seaborn — стилист и дизайнер**

**Seaborn** — это Matplotlib, который окончил школу дизайна. Красиво по умолчанию!

**Философия:** "Зачем настраивать цвета, когда они уже идеальные?"

```python
import seaborn as sns
import pandas as pd

# Тот же график, но красивый
sns.set_style("whitegrid")
df = pd.DataFrame({'время': x, 'продажи': y})

plt.figure(figsize=(10, 6))
sns.lineplot(data=df, x='время', y='продажи', marker='o')
plt.title('Продажи растут! 🚀', size=16)
plt.show()
```

**Когда использовать:**
- ✅ Нужно быстро и красиво
- ✅ Статистические графики (распределения, корреляции)
- ✅ Презентации и отчеты
- ✅ Исследовательский анализ данных

## 📈 Основные типы графиков

### 📊 **Линейные графики — показываем динамику**

**Лучше всего для:** временных рядов, трендов, динамики

```python
# Продажи по месяцам — классика жанра
plt.figure(figsize=(12, 6))
sns.lineplot(data=sales_df, x='месяц', y='выручка', 
             marker='o', linewidth=2.5)
plt.title('📈 Динамика продаж по месяцам', size=14)
plt.ylabel('Выручка, млн руб.')
plt.xticks(rotation=45)
plt.grid(alpha=0.3)
plt.show()
```

**💡 Профессиональные секреты:**
- Используйте `marker='o'` для точек на линии
- `linewidth=2.5` делает линию заметнее
- `alpha=0.3` для полупрозрачности элементов

### 📊 **Столбчатые диаграммы — сравниваем категории**

**Лучше всего для:** сравнения по категориям, рейтингов, структуры

```python
# Продажи по регионам
plt.figure(figsize=(10, 6))
sns.barplot(data=sales_df, x='регион', y='выручка', 
            palette='viridis')
plt.title('💰 Выручка по регионам', size=14)
plt.ylabel('Выручка, млн руб.')
plt.xticks(rotation=45)

# Добавляем значения на столбцы
for i, v in enumerate(sales_by_region):
    plt.text(i, v + 0.1, f'{v:.1f}М', ha='center')

plt.show()
```

### 🥧 **Круговые диаграммы — показываем доли**

**Лучше всего для:** структуры, долей от целого (максимум 5-6 категорий)

```python
# Доли продаж по категориям товаров
categories = ['Электроника', 'Одежда', 'Книги', 'Спорт', 'Дом']
values = [35, 25, 15, 15, 10]

plt.figure(figsize=(8, 8))
colors = sns.color_palette('Set2')

plt.pie(values, labels=categories, colors=colors, 
        autopct='%1.1f%%', startangle=90)
plt.title('🛍️ Структура продаж по категориям', size=14)
plt.show()
```

### 📊 **Диаграммы рассеивания — ищем связи**

**Лучше всего для:** корреляций, выбросов, зависимостей

```python
# Связь между рекламным бюджетом и продажами
plt.figure(figsize=(10, 6))
sns.scatterplot(data=marketing_df, x='реклама_бюджет', y='продажи',
                size='размер_города', hue='регион', 
                sizes=(50, 200), alpha=0.7)
plt.title('💰 Реклама vs Продажи', size=14)
plt.xlabel('Рекламный бюджет, тыс. руб.')
plt.ylabel('Продажи, млн руб.')
plt.show()
```

## 🎨 Магия Seaborn — статистические графики

### 📊 **Распределения — понимаем природу данных**

```python
# Распределение доходов клиентов
plt.figure(figsize=(12, 8))

# Гистограмма + кривая плотности
plt.subplot(2, 2, 1)
sns.histplot(data=customers_df, x='доход', kde=True, bins=30)
plt.title('📊 Распределение доходов')

# Ящик с усами
plt.subplot(2, 2, 2)  
sns.boxplot(data=customers_df, y='доход')
plt.title('📦 Выбросы в доходах')

# По категориям
plt.subplot(2, 2, 3)
sns.violinplot(data=customers_df, x='сегмент', y='доход')
plt.title('🎻 Доходы по сегментам')

# Совокупное распределение
plt.subplot(2, 2, 4)
sns.ecdfplot(data=customers_df, x='доход')
plt.title('📈 Кумулятивное распределение')

plt.tight_layout()
plt.show()
```

### 🔗 **Корреляционные матрицы — находим связи**

```python
# Тепловая карта корреляций
numeric_columns = ['продажи', 'реклама', 'цена', 'скидка', 'рейтинг']
correlation_matrix = df[numeric_columns].corr()

plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, 
            annot=True,           # Показывать значения
            cmap='RdYlBu_r',     # Красиво-синяя палитра
            center=0,            # Центр на нуле
            square=True,         # Квадратные ячейки
            fmt='.2f')           # Формат чисел

plt.title('🔥 Тепловая карта корреляций', size=14)
plt.show()
```

### 📊 **Парные графики — исследуем все связи сразу**

```python
# Исследуем связи между всеми переменными
g = sns.pairplot(data=sales_df[numeric_columns], 
                 diag_kind='kde',    # Плотности на диагонали
                 corner=True)        # Только нижний треугольник

g.fig.suptitle('🔍 Исследование всех связей', y=1.02, size=16)
plt.show()
```

## 🎭 Настройка стилей и оформления

### 🎨 **Готовые стили Seaborn**

```python
# Доступные стили
styles = ['darkgrid', 'whitegrid', 'dark', 'white', 'ticks']

fig, axes = plt.subplots(2, 3, figsize=(15, 10))
fig.suptitle('🎨 Галерея стилей Seaborn', size=16)

for i, style in enumerate(styles):
    sns.set_style(style)
    ax = axes[i//3, i%3]
    
    sns.lineplot(data=sample_data, x='x', y='y', ax=ax)
    ax.set_title(f'Стиль: {style}')

# Последний график — без стиля
sns.reset_orig()
ax = axes[1, 2]
sns.lineplot(data=sample_data, x='x', y='y', ax=ax) 
ax.set_title('Без стиля (matplotlib)')

plt.tight_layout()
plt.show()
```

### 🌈 **Работа с цветовыми палитрами**

```python
# Палитры для категориальных данных
palettes = ['Set1', 'Set2', 'Dark2', 'tab10', 'husl', 'viridis']

fig, axes = plt.subplots(2, 3, figsize=(15, 10))
fig.suptitle('🌈 Галерея цветовых палитр', size=16)

for i, palette in enumerate(palettes):
    ax = axes[i//3, i%3]
    
    sns.barplot(data=category_sales, x='категория', y='продажи',
                palette=palette, ax=ax)
    ax.set_title(f'Палитра: {palette}')
    ax.tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.show()
```

### 🎯 **Создание фирменного стиля**

```python
# Ваш корпоративный стиль
def setup_corporate_style():
    """Настройка фирменного стиля компании"""
    
    # Корпоративные цвета
    corporate_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
    
    # Настройки matplotlib
    plt.rcParams.update({
        'font.size': 12,
        'font.family': 'DejaVu Sans',
        'axes.titlesize': 14,
        'axes.labelsize': 12,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'legend.fontsize': 10,
        'figure.titlesize': 16,
        'axes.grid': True,
        'grid.alpha': 0.3
    })
    
    # Устанавливаем палитру
    sns.set_palette(corporate_colors)
    sns.set_style("whitegrid")
    
    return corporate_colors

# Используем фирменный стиль
colors = setup_corporate_style()

plt.figure(figsize=(12, 6))
sns.barplot(data=sales_data, x='месяц', y='выручка')
plt.title('📊 Ежемесячная выручка компании', pad=20)
plt.ylabel('Выручка, млн руб.')
plt.show()
```

## 📊 Создание дашбордов в Python

### 🎛️ **Многопанельные дашборды**

```python
def create_sales_dashboard(sales_df):
    """Создаем полноценный дашборд продаж"""
    
    # Настройка фигуры
    fig = plt.figure(figsize=(20, 12))
    fig.suptitle('📊 Дашборд продаж компании', size=20, y=0.98)
    
    # 1. Динамика продаж (большой график)
    ax1 = plt.subplot(3, 4, (1, 4))  # Занимает 4 позиции
    monthly_sales = sales_df.groupby('месяц')['выручка'].sum()
    sns.lineplot(x=monthly_sales.index, y=monthly_sales.values, 
                 marker='o', linewidth=3, ax=ax1)
    ax1.set_title('📈 Динамика продаж по месяцам', size=14)
    ax1.set_ylabel('Выручка, млн руб.')
    
    # 2. Топ товары
    ax2 = plt.subplot(3, 4, 5)
    top_products = sales_df.groupby('товар')['выручка'].sum().nlargest(5)
    sns.barplot(y=top_products.index, x=top_products.values, ax=ax2)
    ax2.set_title('🏆 Топ-5 товаров')
    
    # 3. Продажи по регионам  
    ax3 = plt.subplot(3, 4, 6)
    region_sales = sales_df.groupby('регион')['выручка'].sum()
    ax3.pie(region_sales.values, labels=region_sales.index, autopct='%1.1f%%')
    ax3.set_title('🗺️ Продажи по регионам')
    
    # 4. Распределение чеков
    ax4 = plt.subplot(3, 4, 7)
    sns.histplot(data=sales_df, x='сумма_чека', bins=30, ax=ax4)
    ax4.set_title('💰 Распределение чеков')
    
    # 5. Корреляция цена-количество
    ax5 = plt.subplot(3, 4, 8)
    sns.scatterplot(data=sales_df, x='цена', y='количество', 
                    alpha=0.6, ax=ax5)
    ax5.set_title('💱 Цена vs Количество')
    
    # 6. KPI метрики (текстовые)
    ax6 = plt.subplot(3, 4, (9, 12))
    ax6.axis('off')
    
    # Вычисляем KPI
    total_revenue = sales_df['выручка'].sum()
    avg_check = sales_df['сумма_чека'].mean()
    total_orders = len(sales_df)
    customers = sales_df['клиент'].nunique()
    
    kpi_text = f"""
    📊 КЛЮЧЕВЫЕ ПОКАЗАТЕЛИ
    
    💰 Общая выручка: {total_revenue:,.0f} млн руб.
    🛒 Средний чек: {avg_check:,.0f} руб.
    📦 Всего заказов: {total_orders:,}
    👥 Уникальных клиентов: {customers:,}
    
    📈 Средняя выручка на клиента: {total_revenue/customers:,.0f} руб.
    🔄 Повторных покупок: {((total_orders-customers)/customers*100):.1f}%
    """
    
    ax6.text(0.1, 0.5, kpi_text, fontsize=12, va='center',
             bbox=dict(boxstyle="round,pad=1", facecolor='lightblue', alpha=0.7))
    
    plt.tight_layout()
    return fig

# Создаем дашборд
dashboard = create_sales_dashboard(sales_df)
plt.show()
```

## 📱 Интерактивные визуализации

### ⚡ **Plotly — интерактивность в браузере**

```python
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Интерактивный график продаж
fig = px.line(sales_df, x='дата', y='выручка', 
              title='📈 Интерактивная динамика продаж',
              hover_data=['количество_заказов', 'средний_чек'])

# Добавляем аннотации для важных событий
fig.add_annotation(x='2024-11-01', y=sales_df.loc[sales_df['дата']=='2024-11-01', 'выручка'].iloc[0],
                   text="🚀 Черная пятница!",
                   showarrow=True, arrowhead=2)

fig.show()

# Интерактивная карта продаж по регионам
fig_map = px.choropleth(region_data, 
                        locations='регион_код',
                        color='выручка',
                        hover_name='регион',
                        color_continuous_scale='Blues',
                        title='🗺️ География продаж')
fig_map.show()
```

## 🔄 Интеграция с Pandas

### 📊 **Встроенные возможности Pandas**

```python
# Pandas умеет рисовать графики сам!
sales_df.set_index('дата')['выручка'].plot(kind='line', 
                                           figsize=(12, 6),
                                           title='📈 Быстрый график из Pandas')

# Несколько графиков одновременно
sales_df.groupby('регион')['выручка'].sum().plot(kind='bar',
                                                  color=sns.color_palette('Set2'))
plt.title('📊 Продажи по регионам')
plt.ylabel('Выручка, млн руб.')
plt.xticks(rotation=45)
plt.show()

# Корреляционная матрица из Pandas
numeric_cols = sales_df.select_dtypes(include=[np.number]).columns
correlation_matrix = sales_df[numeric_cols].corr()

# Красивая тепловая карта
plt.figure(figsize=(10, 8))
mask = np.triu(np.ones_like(correlation_matrix, dtype=bool))
sns.heatmap(correlation_matrix, mask=mask, annot=True, 
            cmap='RdYlBu_r', center=0)
plt.title('🔥 Корреляции между показателями')
plt.show()
```

## 💾 Сохранение и экспорт графиков

### 📁 **Различные форматы для разных целей**

```python
# Создаем красивый график для сохранения
plt.figure(figsize=(12, 8))
sns.set_style("whitegrid")
sns.lineplot(data=sales_df, x='месяц', y='выручка', marker='o', linewidth=3)
plt.title('📈 Динамика продаж — готово для презентации', size=16, pad=20)
plt.ylabel('Выручка, млн руб.', size=12)
plt.xlabel('Месяц', size=12)

# Сохраняем в разных форматах
plt.savefig('sales_chart_presentation.png', dpi=300, bbox_inches='tight')  # Для презентаций
plt.savefig('sales_chart_print.pdf', bbox_inches='tight')                  # Для печати  
plt.savefig('sales_chart_web.svg', bbox_inches='tight')                    # Для веба

print("✅ Графики сохранены в форматах PNG, PDF и SVG")
plt.show()
```

## 🎯 Готовые шаблоны для копирования

### 📊 **Универсальный шаблон для бизнес-отчета**

```python
def create_business_report(data, title="Бизнес-отчет"):
    """
    Универсальный шаблон для создания бизнес-отчета
    
    Parameters:
    -----------
    data : DataFrame
        Данные для анализа
    title : str
        Заголовок отчета
    """
    
    # Настройка стиля
    sns.set_style("whitegrid")
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
    sns.set_palette(colors)
    
    # Создаем фигуру
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle(f'📊 {title}', size=18, y=0.95)
    
    # График 1: Основная метрика по времени
    sns.lineplot(data=data, x='период', y='основная_метрика', 
                 marker='o', linewidth=2.5, ax=axes[0,0])
    axes[0,0].set_title('📈 Динамика основного показателя')
    
    # График 2: Сравнение по категориям
    sns.barplot(data=data, x='категория', y='значение', ax=axes[0,1])
    axes[0,1].set_title('📊 Сравнение по категориям')
    axes[0,1].tick_params(axis='x', rotation=45)
    
    # График 3: Распределение
    sns.histplot(data=data, x='распределение', bins=20, ax=axes[1,0])
    axes[1,0].set_title('📈 Распределение значений')
    
    # График 4: Корреляция
    sns.scatterplot(data=data, x='x_переменная', y='y_переменная', 
                    alpha=0.7, ax=axes[1,1])
    axes[1,1].set_title('💫 Взаимосвязь переменных')
    
    plt.tight_layout()
    return fig

# Пример использования
# report = create_business_report(your_data, "Анализ продаж Q3 2024")
# report.savefig('business_report.png', dpi=300, bbox_inches='tight')
```

## ✅ Лучшие практики и советы

### 🎯 **Что делает график профессиональным:**

1. **📏 Правильные пропорции**
   ```python
   # Золотое сечение для графиков
   plt.figure(figsize=(12, 7.4))  # Соотношение 1.6:1
   ```

2. **🎨 Осознанный выбор цветов**
   ```python
   # Используйте не более 5-7 цветов
   # Цветослепые должны различать ваши графики
   colors = sns.color_palette("colorblind", n_colors=5)
   ```

3. **📝 Понятные подписи**
   ```python
   plt.title('📈 Рост продаж на 23% за квартал', size=14)
   plt.ylabel('Выручка, млн руб.')  # Всегда указывайте единицы!
   ```

4. **🔍 Фокус на главном**
   ```python
   # Убираем лишние элементы
   sns.despine()  # Убирает верхнюю и правую рамки
   plt.grid(alpha=0.3)  # Полупрозрачная сетка
   ```

### ❌ **Чего избегать:**

- 🚫 **3D графиков без необходимости** — они искажают восприятие
- 🚫 **Слишком много цветов** — максимум 7 категорий на одном графике  
- 🚫 **Мелкого шрифта** — минимум 10pt для осей, 12pt для заголовков
- 🚫 **Неподписанных осей** — всегда указывайте, что измеряете
- 🚫 **Обрезанных Y-осей** — начинайте с нуля, если нет веских причин

## 🚀 Что дальше?

После освоения этой главы вы умеете:

✅ **Создавать профессиональные графики** с Matplotlib и Seaborn  
✅ **Настраивать стили и цвета** под корпоративный дизайн  
✅ **Строить статистические визуализации** для исследования данных  
✅ **Создавать интерактивные дашборды** прямо в Python  
✅ **Рассказывать истории данными** через эффективную визуализацию

**Следующий шаг:** Научиться автоматически находить закономерности в данных с помощью машинного обучения!

## 🛠 Инструкции

Теперь переходите к практическим заданиям — вас ждут 5 увлекательных проектов по визуализации реальных бизнес-данных:

- 📝 [Перейти к практическим заданиям](practice.md)
- ✅ [Перейти к чек-листу](checklist.md)
- 📁 [Посмотреть учебные файлы](files/README.md)
---

- 🔙 [Предыдущая глава: Глава 14 - Pandas в Python: загрузка и очистка данных](../chapter-14/README.md)
- 🔜 [Следующая глава: Глава 16 - Кластеризация и сегментация: k-means и иерархическая](../chapter-16/README.md)

---

- 📢 Присоединяйтесь к чату курса: https://t.me/analytics_course_chat
- 📢 Канал курса: https://t.me/analytics_course_channel