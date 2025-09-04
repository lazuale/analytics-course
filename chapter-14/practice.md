# 📝 Практические задания для главы 14

📖 [Вернуться к теории](../README.md) | 📁 [Учебные файлы](../files/README.md) | ✅ [Чек-лист](../checklist.md)

**🎯 Цель:** Стать настоящим "доктором данных" — научиться лечить "больные" данные и превращать их в полезную информацию!

## 🏥 Задание 1: "Доктор данных" — лечим грязные данные

**🎬 Ваша роль:** Вы — новый аналитик в интернет-магазине. Вам дали "грязные" данные с кучей проблем. Нужно их вылечить!

**📋 Что нужно сделать:**
1. Загрузить данные и провести "диагностику"
2. Найти все проблемы в данных
3. Вылечить данные пошагово
4. Создать отчет о проделанной работе

**📁 Используемые файлы:** `files/messy_ecommerce_data.csv`, `files/data-cleaning-template.py`

### 🚀 **Шаг 1: Подготовка рабочего места**

**💻 Создайте новую папку для проекта и откройте Python:**

```python
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt

print("🏥 Добро пожаловать в клинику данных!")
print("Сегодня мы будем лечить больные данные e-commerce магазина")
```

### 🔍 **Шаг 2: Загрузка и диагностика пациента**

```python
# Загружаем "больного пациента"
try:
    df = pd.read_csv('files/messy_ecommerce_data.csv')
    print(f"✅ Пациент загружен: {len(df)} записей")
except FileNotFoundError:
    print("❌ Файл не найден! Убедитесь, что messy_ecommerce_data.csv в папке files/")
    exit()

# Первичный осмотр пациента
print(f"\n🔍 ПЕРВИЧНАЯ ДИАГНОСТИКА")
print("=" * 30)
print(f"📏 Размер: {df.shape[0]} строк, {df.shape[1]} столбцов")
print(f"📋 Столбцы: {list(df.columns)}")

# Показываем первые строки (как снимок)
print(f"\n📸 Снимок состояния пациента:")
print(df.head())

# Ищем симптомы болезни
print(f"\n🩺 ПОИСК СИМПТОМОВ:")
print(f"❌ Пропущенные значения: {df.isnull().sum().sum()}")
print(f"🔄 Дубликаты: {df.duplicated().sum()}")
print(f"📊 Типы данных:")
for col, dtype in df.dtypes.items():
    print(f"   {col}: {dtype}")
```

### 🧹 **Шаг 3: Лечение — этап за этапом**

**Лечение 1: Удаляем дубликаты**
```python
print(f"\n💊 ЛЕЧЕНИЕ 1: Удаление дубликатов")
print("-" * 35)

дубликаты_до = df.duplicated().sum()
print(f"🔍 Найдено дубликатов: {дубликаты_до}")

# Удаляем полные дубликаты
df = df.drop_duplicates()

# Удаляем дубликаты по ID заказа (оставляем последний)
if 'order_id' in df.columns:
    дубликаты_id_до = df.duplicated(subset=['order_id']).sum()
    df = df.drop_duplicates(subset=['order_id'], keep='last')
    print(f"🧹 Удалено дубликатов по order_id: {дубликаты_id_до}")

строк_удалено = дубликаты_до - df.duplicated().sum()
print(f"✅ Удалено строк: {строк_удалено}")
print(f"📊 Осталось строк: {len(df)}")
```

**Лечение 2: Исправляем форматы данных**
```python
print(f"\n💊 ЛЕЧЕНИЕ 2: Исправление форматов")
print("-" * 32)

# Лечим цены (убираем символы валют)
if 'price' in df.columns:
    print("🔧 Лечим столбец 'price'...")
    
    # Показываем проблемы
    print(f"   Примеры проблемных цен: {df['price'].head().tolist()}")
    
    # Создаем функцию лечения цен
    def лечить_цену(цена):
        if pd.isna(цена) or цена == '':
            return np.nan
        
        # Преобразуем в строку и чистим
        цена_str = str(цена)
        цена_str = цена_str.replace('$', '').replace('₽', '').replace(' USD', '')
        цена_str = цена_str.replace(',', '.').replace(' ', '')
        
        # Убираем все кроме цифр, точек и минусов
        import re
        цена_str = re.sub(r'[^\d.\-]', '', цена_str)
        
        try:
            return float(цена_str)
        except:
            return np.nan
    
    # Применяем лечение
    df['price'] = df['price'].apply(лечить_цену)
    успешных_цен = df['price'].notna().sum()
    print(f"   ✅ Вылечено цен: {успешных_цен}")

# Лечим даты
if 'order_date' in df.columns:
    print("🔧 Лечим столбец 'order_date'...")
    
    # Применяем лечение дат
    df['order_date'] = pd.to_datetime(df['order_date'], 
                                     infer_datetime_format=True, 
                                     errors='coerce')
    успешных_дат = df['order_date'].notna().sum()
    print(f"   ✅ Вылечено дат: {успешных_дат}")

# Лечим количества
if 'quantity' in df.columns:
    print("🔧 Лечим столбец 'quantity'...")
    
    # Преобразуем в числа
    df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce')
    
    # Убираем отрицательные количества (это ошибки)
    отрицательных = (df['quantity'] < 0).sum()
    df = df[df['quantity'] >= 0]
    print(f"   🗑️ Удалено отрицательных количеств: {отрицательных}")
```

**Лечение 3: Заполняем пропуски**
```python
print(f"\n💊 ЛЕЧЕНИЕ 3: Заполнение пропусков")
print("-" * 30)

# Анализируем пропуски по столбцам
пропуски = df.isnull().sum()
print("🔍 Пропуски по столбцам:")
for столбец, количество in пропуски[пропуски > 0].items():
    процент = (количество / len(df)) * 100
    print(f"   {столбец}: {количество} ({процент:.1f}%)")

# Лечим пропуски в именах клиентов
if 'customer_name' in df.columns:
    пустых_имен = df['customer_name'].isnull().sum()
    df = df.dropna(subset=['customer_name'])  # Удаляем строки без имени клиента
    print(f"🗑️ Удалено строк без имени клиента: {пустых_имен}")

# Лечим пропуски в ценах (заполняем средней ценой по категории)
if 'price' in df.columns and 'category' in df.columns:
    средние_цены = df.groupby('category')['price'].median()
    
    def заполнить_цену(row):
        if pd.isna(row['price']) and not pd.isna(row['category']):
            return средние_цены.get(row['category'], df['price'].median())
        return row['price']
    
    заполнено_цен = df['price'].isnull().sum()
    df['price'] = df.apply(заполнить_цену, axis=1)
    print(f"💊 Заполнено пропусков в ценах: {заполнено_цен}")

# Лечим пропуски в адресах
if 'shipping_address' in df.columns:
    df['shipping_address'] = df['shipping_address'].fillna('Не указан')
    print(f"💊 Заполнены пропуски в адресах")
```

**Лечение 4: Стандартизация текста**
```python
print(f"\n💊 ЛЕЧЕНИЕ 4: Стандартизация текста")
print("-" * 32)

# Лечим названия категорий
if 'category' in df.columns:
    print("🔧 Стандартизируем категории...")
    
    # Показываем проблемы
    уникальные_категории = df['category'].unique()
    print(f"   Было категорий: {len(уникальные_категории)}")
    print(f"   Примеры: {уникальные_категории[:5]}")
    
    # Стандартизируем
    df['category'] = df['category'].str.strip().str.title()
    
    # Исправляем типичные опечатки
    замены_категорий = {
        'Electronics': 'Electronics',
        'Electronic': 'Electronics', 
        'Elektronics': 'Electronics',
        'Clothing': 'Clothing',
        'Clothes': 'Clothing',
        'Home Garden': 'Home & Garden',
        'Home & Garden': 'Home & Garden'
    }
    
    df['category'] = df['category'].replace(замены_категорий)
    
    стало_категорий = df['category'].nunique()
    print(f"   ✅ Стало категорий: {стало_категорий}")

# Лечим имена клиентов
if 'customer_name' in df.columns:
    print("🔧 Стандартизируем имена клиентов...")
    
    # Убираем лишние пробелы и приводим к единому формату
    df['customer_name'] = df['customer_name'].str.strip().str.title()
    print(f"   ✅ Стандартизированы имена клиентов")
```

### 📊 **Шаг 4: Контрольный осмотр после лечения**

```python
print(f"\n🩺 КОНТРОЛЬНЫЙ ОСМОТР ПОСЛЕ ЛЕЧЕНИЯ")
print("=" * 40)

print(f"📏 Финальный размер: {df.shape[0]} строк, {df.shape[1]} столбцов")
print(f"❌ Оставшиеся пропуски: {df.isnull().sum().sum()}")
print(f"🔄 Оставшиеся дубликаты: {df.duplicated().sum()}")

# Проверяем качество данных
проблемы = []

if 'price' in df.columns:
    отрицательных_цен = (df['price'] < 0).sum()
    if отрицательных_цен > 0:
        проблемы.append(f"Отрицательные цены: {отрицательных_цен}")

if 'quantity' in df.columns:
    нулевых_количеств = (df['quantity'] == 0).sum()
    if нулевых_количеств > 0:
        проблемы.append(f"Нулевые количества: {нулевых_количеств}")

if проблемы:
    print(f"⚠️ Обнаруженные проблемы:")
    for проблема in проблемы:
        print(f"   • {проблема}")
else:
    print(f"✅ Пациент полностью здоров!")

# Сохраняем вылеченные данные
df.to_csv('cleaned_ecommerce_data.csv', index=False, encoding='utf-8-sig')
print(f"\n💾 Вылеченные данные сохранены: cleaned_ecommerce_data.csv")
```

**❓ Контрольные вопросы:**
1. Сколько строк данных было до и после лечения?
2. Какие типы проблем были самыми частыми?
3. Можно ли было предотвратить эти проблемы на этапе сбора данных?

---

## 🔍 Задание 2: "Детектив данных" — ищем закономерности

**🎬 Ваша роль:** Вы детектив, который должен найти скрытые закономерности в данных продаж. Кто лучший клиент? Какой товар приносит больше прибыли?

**📋 Что нужно сделать:**
1. Загрузить очищенные данные из предыдущего задания
2. Провести детективное расследование с помощью группировок
3. Найти интересные закономерности
4. Создать досье на каждую находку

**📁 Используемые файлы:** Результат предыдущего задания `cleaned_ecommerce_data.csv`

### 🕵️ **Шаг 1: Подготовка детективного расследования**

```python
print("🕵️ Детективное агентство 'Pandas Холмс'")
print("Дело: Поиск закономерностей в данных e-commerce")
print("=" * 50)

# Загружаем вылеченные данные
df = pd.read_csv('cleaned_ecommerce_data.csv')

# Готовим данные для расследования
df['order_date'] = pd.to_datetime(df['order_date'])
df['месяц'] = df['order_date'].dt.month
df['день_недели'] = df['order_date'].dt.day_name()
df['выручка'] = df['price'] * df['quantity']

print(f"📊 База доказательств: {len(df)} записей")
print(f"📅 Период расследования: {df['order_date'].min()} - {df['order_date'].max()}")
print(f"💰 Общая выручка: {df['выручка'].sum():,.2f}")
```

### 🔍 **Шаг 2: Расследование клиентов**

```python
print(f"\n🔍 РАССЛЕДОВАНИЕ 1: Профилирование клиентов")
print("-" * 42)

# Создаем досье на каждого клиента
досье_клиентов = df.groupby('customer_name').agg({
    'выручка': ['sum', 'count', 'mean'],
    'quantity': 'sum',
    'order_date': ['min', 'max']
}).round(2)

# Упрощаем названия столбцов
досье_клиентов.columns = ['общая_выручка', 'количество_заказов', 'средний_чек', 'общее_количество', 'первый_заказ', 'последний_заказ']

# Сортируем по выручке
досье_клиентов = досье_клиентов.sort_values('общая_выручка', ascending=False)

print("🏆 ТОП-5 КЛИЕНТОВ ПО ВЫРУЧКЕ:")
for i, (клиент, данные) in enumerate(досье_клиентов.head().iterrows(), 1):
    print(f"{i}. {клиент}")
    print(f"   💰 Общая выручка: {данные['общая_выручка']:,.2f}")
    print(f"   🛒 Количество заказов: {данные['количество_заказов']}")
    print(f"   💳 Средний чек: {данные['средний_чек']:,.2f}")
    print()

# Сегментируем клиентов
def определить_класс_клиента(row):
    if row['общая_выручка'] > 20000 and row['количество_заказов'] > 5:
        return 'VIP 👑'
    elif row['общая_выручка'] > 10000:
        return 'Ценный 💎'
    elif row['количество_заказов'] > 3:
        return 'Активный ⚡'
    else:
        return 'Обычный 👤'

досье_клиентов['класс'] = досье_клиентов.apply(определить_класс_клиента, axis=1)

print("📊 РАСПРЕДЕЛЕНИЕ КЛИЕНТОВ ПО КЛАССАМ:")
распределение = досье_клиентов['класс'].value_counts()
for класс, количество in распределение.items():
    процент = (количество / len(досье_клиентов)) * 100
    print(f"   {класс}: {количество} клиентов ({процент:.1f}%)")
```

### 🛍️ **Шаг 3: Расследование товаров**

```python
print(f"\n🔍 РАССЛЕДОВАНИЕ 2: Анализ товарного портфеля")
print("-" * 45)

# Анализируем товары по категориям
анализ_категорий = df.groupby('category').agg({
    'выручка': ['sum', 'mean', 'count'],
    'quantity': 'sum',
    'price': 'mean'
}).round(2)

анализ_категорий.columns = ['общая_выручка', 'средняя_выручка_заказа', 'количество_заказов', 'общее_количество', 'средняя_цена']

print("📦 АНАЛИЗ ПО КАТЕГОРИЯМ ТОВАРОВ:")
for категория, данные in анализ_категорий.iterrows():
    доля_выручки = (данные['общая_выручка'] / df['выручка'].sum()) * 100
    print(f"\n🏷️ {категория}:")
    print(f"   💰 Общая выручка: {данные['общая_выручка']:,.2f} ({доля_выручки:.1f}%)")
    print(f"   🛒 Количество заказов: {данные['количество_заказов']}")
    print(f"   📦 Среднее количество в заказе: {данные['общее_количество']/данные['количество_заказов']:.1f}")
    print(f"   💳 Средняя цена: {данные['средняя_цена']:,.2f}")

# Ищем самые популярные товары
популярные_товары = df.groupby('product').agg({
    'quantity': 'sum',
    'выручка': 'sum'
}).sort_values('выручка', ascending=False)

print(f"\n🎯 ТОП-5 ТОВАРОВ ПО ВЫРУЧКЕ:")
for i, (товар, данные) in enumerate(популярные_товары.head().iterrows(), 1):
    print(f"{i}. {товар}")
    print(f"   💰 Выручка: {данные['выручка']:,.2f}")
    print(f"   📦 Продано штук: {данные['quantity']}")
```

### 📅 **Шаг 4: Временное расследование**

```python
print(f"\n🔍 РАССЛЕДОВАНИЕ 3: Временные закономерности")
print("-" * 42)

# Анализируем продажи по месяцам
продажи_по_месяцам = df.groupby('месяц').agg({
    'выручка': 'sum',
    'quantity': 'sum',
    'customer_name': 'nunique'
}).round(2)

продажи_по_месяцам.columns = ['выручка', 'количество', 'уникальных_клиентов']

print("📅 СЕЗОННОСТЬ ПРОДАЖ:")
месяцы = ['', 'Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн', 
          'Июл', 'Авг', 'Сен', 'Окт', 'Ноя', 'Дек']

for месяц_номер, данные in продажи_по_месяцам.iterrows():
    месяц_название = месяцы[месяц_номер]
    доля = (данные['выручка'] / продажи_по_месяцам['выручка'].sum()) * 100
    print(f"{месяц_название}: {данные['выручка']:,.2f} ({доля:.1f}%) - {данные['уникальных_клиентов']} клиентов")

# Находим лучший и худший месяцы
лучший_месяц = продажи_по_месяцам['выручка'].idxmax()
худший_месяц = продажи_по_месяцам['выручка'].idxmin()

print(f"\n🏆 Лучший месяц: {месяцы[лучший_месяц]} ({продажи_по_месяцам.loc[лучший_месяц, 'выручка']:,.2f})")
print(f"📉 Худший месяц: {месяцы[худший_месяц]} ({продажи_по_месяцам.loc[худший_месяц, 'выручка']:,.2f})")

# Анализируем дни недели
продажи_по_дням = df.groupby('день_недели')['выручка'].sum().sort_values(ascending=False)

print(f"\n📊 ПРОДАЖИ ПО ДНЯМ НЕДЕЛИ:")
for день, выручка in продажи_по_дням.items():
    доля = (выручка / продажи_по_дням.sum()) * 100
    print(f"{день}: {выручка:,.2f} ({доля:.1f}%)")

лучший_день = продажи_по_дням.index[0]
print(f"\n🎯 Самый прибыльный день: {лучший_день}")
```

### 📊 **Шаг 5: Составляем детективный отчет**

```python
print(f"\n📋 ДЕТЕКТИВНЫЙ ОТЧЕТ")
print("=" * 20)

# Находки расследования
находки = []

# Находка 1: VIP клиенты
vip_клиенты = len(досье_клиентов[досье_клиентов['класс'] == 'VIP 👑'])
vip_выручка = досье_клиентов[досье_клиентов['класс'] == 'VIP 👑']['общая_выручка'].sum()
vip_доля = (vip_выручка / df['выручка'].sum()) * 100

if vip_доля > 40:
    находки.append(f"🔍 НАХОДКА: {vip_клиенты} VIP клиентов ({vip_клиенты/len(досье_клиентов)*100:.1f}%) дают {vip_доля:.1f}% выручки!")

# Находка 2: Лидирующая категория
лидер_категория = анализ_категорий['общая_выручка'].idxmax()
лидер_доля = (анализ_категорий.loc[лидер_категория, 'общая_выручка'] / df['выручка'].sum()) * 100

if лидер_доля > 30:
    находки.append(f"🔍 НАХОДКА: Категория '{лидер_категория}' доминирует с {лидер_доля:.1f}% от общей выручки!")

# Находка 3: Сезонность
разброс_месяцев = (продажи_по_месяцам['выручка'].max() - продажи_по_месяцам['выручка'].min()) / продажи_по_месяцам['выручка'].mean()

if разброс_месяцев > 0.5:
    находки.append(f"🔍 НАХОДКА: Выраженная сезонность! Разброс продаж по месяцам {разброс_месяцев:.1f}x")

# Выводим находки
print("🕵️ КЛЮЧЕВЫЕ НАХОДКИ РАССЛЕДОВАНИЯ:")
for i, находка in enumerate(находки, 1):
    print(f"{i}. {находка}")

if not находки:
    print("🤔 Явных закономерностей не обнаружено. Данные распределены равномерно.")

# Рекомендации
print(f"\n💡 РЕКОМЕНДАЦИИ ДЛЯ БИЗНЕСА:")
print("1. 👑 Сосредоточьтесь на удержании VIP клиентов")
print("2. 📦 Развивайте лидирующие категории товаров")
print("3. 📅 Планируйте маркетинг с учетом сезонности")
print("4. 🎯 Изучите причины успеха в лучшие дни недели")

# Сохраняем досье клиентов
досье_клиентов.to_csv('customer_profiles.csv', encoding='utf-8-sig')
print(f"\n💾 Досье клиентов сохранено: customer_profiles.csv")
```

**❓ Детективные вопросы:**
1. Кто ваш самый ценный клиент и почему?
2. Какая категория товаров имеет наибольший потенциал?
3. В какие дни недели стоит проводить акции?

---

## 🤝 Задание 3: "Переговорщик данных" — объединяем источники

**🎬 Ваша роль:** Вы дипломат, который должен "подружить" данные из разных источников. У вас есть основные данные продаж и большой датасет для сравнения.

**📋 Что нужно сделать:**
1. Загрузить данные из разных источников
2. Изучить структуру каждого источника
3. Найти общие "ключи" для объединения
4. Создать единую сводную таблицу
5. Получить новые инсайты из объединенных данных

**📁 Используемые файлы:** `files/large_dataset_sample.csv`, результаты предыдущих заданий

### 🤝 **Шаг 1: Знакомство с "переговорщиками"**

```python
print("🤝 Дипломатическая миссия: Объединение данных")
print("=" * 45)

# Загружаем данных из разных источников
print("📥 Загружаем участников переговоров...")

# Участник 1: Наши очищенные данные (малые)
try:
    df_small = pd.read_csv('cleaned_ecommerce_data.csv')
    print(f"🛒 Очищенные данные: {len(df_small)} записей")
    print(f"   Столбцы: {list(df_small.columns)}")
except:
    print("⚠️ Не найден файл очищенных данных, создаем образец...")
    df_small = pd.DataFrame({
        'customer_name': ['John Smith', 'Mary Davis', 'Alice Brown'],
        'product': ['iPhone 14', 'Samsung Galaxy', 'MacBook Pro'],
        'category': ['Electronics', 'Electronics', 'Electronics'],
        'price': [999, 899, 1299],
        'quantity': [1, 2, 1]
    })

# Участник 2: Большой международный датасет
try:
    df_big = pd.read_csv('files/large_dataset_sample.csv')
    print(f"🌍 Большой датасет: {len(df_big)} записей")
    print(f"   Столбцы: {list(df_big.columns)}")
except FileNotFoundError:
    print("❌ Файл large_dataset_sample.csv не найден в папке files/")
    exit()

# Готовим данные для объединения
df_small['source'] = 'Local Store'
df_big['source'] = 'Global Network'

print(f"\n📊 Размеры данных:")
print(f"   Локальные данные: {len(df_small):,} записей")
print(f"   Глобальные данные: {len(df_big):,} записей")
```

### 🔍 **Шаг 2: Подготовка к переговорам**

```python
print(f"\n🔍 ПОДГОТОВКА К ПЕРЕГОВОРАМ")
print("-" * 25)

# Изучаем общие поля для объединения
print("🔑 Анализ схожих полей:")

# Приводим к общему виду столбцы
if 'customer_name' in df_small.columns and 'customer_id' in df_big.columns:
    print("   Клиенты: customer_name (локал) vs customer_id (глобал)")

if 'product' in df_small.columns and 'product_name' in df_big.columns:
    print("   Товары: product (локал) vs product_name (глобал)")

if 'category' in df_small.columns and 'category' in df_big.columns:
    print("   ✅ Общее поле: category")

# Стандартизируем структуру для объединения
df_small_std = df_small.copy()
df_big_std = df_big.copy()

# Приводим названия столбцов к единому виду
if 'product_name' in df_big_std.columns:
    df_big_std = df_big_std.rename(columns={'product_name': 'product'})

if 'final_price' in df_big_std.columns:
    df_big_std = df_big_std.rename(columns={'final_price': 'total_amount'})

# Добавляем вычисляемые поля для анализа
df_small_std['total_amount'] = df_small_std['price'] * df_small_std['quantity']
df_small_std['region'] = 'Local Region'
df_small_std['country'] = 'Local Country'

print(f"\n📊 Подготовленные структуры:")
print("Локальные данные:", list(df_small_std.columns))
print("Глобальные данные:", list(df_big_std.columns))
```

### 🤝 **Шаг 3: Объединение по категориям товаров**

```python
print(f"\n🤝 ПЕРЕГОВОРЫ 1: Объединение по категориям")
print("-" * 40)

# Сравнительный анализ по категориям
local_categories = df_small_std.groupby('category').agg({
    'total_amount': ['sum', 'mean', 'count'],
    'quantity': 'sum'
}).round(2)

local_categories.columns = ['local_revenue', 'local_avg_order', 'local_orders', 'local_quantity']
local_categories['source'] = 'Local'

# Глобальная статистика по категориям
if 'category' in df_big_std.columns:
    global_categories = df_big_std.groupby('category').agg({
        'total_amount': ['sum', 'mean', 'count'],
        'quantity': 'sum'
    }).round(2)
    
    global_categories.columns = ['global_revenue', 'global_avg_order', 'global_orders', 'global_quantity']
    global_categories['source'] = 'Global'
    
    # Объединяем статистики
    combined_categories = pd.merge(
        local_categories.reset_index(),
        global_categories.reset_index(),
        on='category',
        how='outer',
        suffixes=('_local', '_global')
    )
    
    print("📊 Сравнение категорий (локал vs глобал):")
    print(combined_categories[['category', 'local_revenue', 'global_revenue', 'local_avg_order', 'global_avg_order']])
    
    # Находим различия
    print(f"\n🔍 КЛЮЧЕВЫЕ РАЗЛИЧИЯ:")
    for _, row in combined_categories.iterrows():
        if not pd.isna(row['local_revenue']) and not pd.isna(row['global_revenue']):
            local_rev = row['local_revenue']
            global_rev = row['global_revenue']
            if global_rev > 0:
                ratio = local_rev / (global_rev / len(df_big_std) * len(df_small_std))  # Нормализуем по размеру
                print(f"   {row['category']}: локальная vs глобальная эффективность = {ratio:.2f}x")
```

### 📈 **Шаг 4: Географический анализ**

```python
print(f"\n🤝 ПЕРЕГОВОРЫ 2: Географическое сравнение")
print("-" * 43)

# Анализ по регионам (используем данные из большого датасета)
if 'region' in df_big_std.columns and 'country' in df_big_std.columns:
    
    regional_performance = df_big_std.groupby(['region', 'country']).agg({
        'total_amount': ['sum', 'mean', 'count'],
        'customer_id': 'nunique'
    }).round(2)
    
    regional_performance.columns = ['total_revenue', 'avg_order', 'orders_count', 'unique_customers']
    regional_performance = regional_performance.reset_index()
    
    print("🌍 ТОП-5 СТРАН ПО ВЫРУЧКЕ:")
    top_countries = regional_performance.nlargest(5, 'total_revenue')
    for _, row in top_countries.iterrows():
        print(f"   {row['country']} ({row['region']}): ${row['total_revenue']:,.2f}")
        print(f"      Средний чек: ${row['avg_order']:,.2f}, Клиентов: {row['unique_customers']}")
    
    # Региональная статистика
    print(f"\n📊 СТАТИСТИКА ПО РЕГИОНАМ:")
    regional_summary = regional_performance.groupby('region').agg({
        'total_revenue': 'sum',
        'orders_count': 'sum',
        'unique_customers': 'sum'
    }).sort_values('total_revenue', ascending=False)
    
    for region, data in regional_summary.iterrows():
        avg_revenue_per_customer = data['total_revenue'] / data['unique_customers']
        print(f"   {region}:")
        print(f"      💰 Выручка: ${data['total_revenue']:,.2f}")
        print(f"      👥 Клиентов: {data['unique_customers']:,}")
        print(f"      💳 Выручка на клиента: ${avg_revenue_per_customer:,.2f}")
```

### 🎯 **Шаг 5: Объединенная сводная таблица**

```python
print(f"\n🎯 ФИНАЛЬНЫЕ ПЕРЕГОВОРЫ: Создание сводной таблицы")
print("=" * 50)

# Создаем общие поля для всех данных
df_small_final = df_small_std[['category', 'total_amount', 'quantity', 'source']].copy()
df_big_final = df_big_std[['category', 'total_amount', 'quantity', 'source']].copy()

# Объединяем все данные
unified_data = pd.concat([df_small_final, df_big_final], ignore_index=True)

print(f"📊 Объединенный датасет: {len(unified_data):,} записей")

# Создаем мега-сводную таблицу
mega_pivot = pd.pivot_table(
    unified_data,
    values=['total_amount', 'quantity'],
    index='category',
    columns='source',
    aggfunc='sum',
    fill_value=0,
    margins=True
)

print(f"\n📋 МЕГА-СВОДНАЯ ТАБЛИЦА:")
print(mega_pivot)

# Анализ эффективности по источникам
source_comparison = unified_data.groupby(['category', 'source']).agg({
    'total_amount': ['sum', 'mean'],
    'quantity': 'sum'
}).round(2)

print(f"\n💡 КЛЮЧЕВЫЕ ИНСАЙТЫ ПЕРЕГОВОРОВ:")

# Находим самые прибыльные категории в каждом источнике
for source in unified_data['source'].unique():
    source_data = unified_data[unified_data['source'] == source]
    top_category = source_data.groupby('category')['total_amount'].sum().idxmax()
    top_revenue = source_data.groupby('category')['total_amount'].sum().max()
    print(f"🏆 {source}: Лидер категория '{top_category}' (${top_revenue:,.2f})")

# Сохраняем объединенные данные
unified_data.to_csv('unified_analysis.csv', index=False, encoding='utf-8-sig')
mega_pivot.to_csv('mega_pivot_table.csv', encoding='utf-8-sig')

print(f"\n💾 Результаты переговоров сохранены:")
print("   - unified_analysis.csv")
print("   - mega_pivot_table.csv")
print("✅ Дипломатическая миссия завершена успешно!")
```

**❓ Дипломатические вопросы:**
1. Какие новые инсайты появились после объединения данных?
2. Какие различия между локальным и глобальным рынками наиболее значимы?
3. Стоит ли менять стратегию на основе глобальных трендов?

---

## 🗄️ Задание 4: "IT-архитектор" — строим мост с базой данных

**🎬 Ваша роль:** Вы IT-архитектор, который должен построить мост между миром Python и миром баз данных. Нужно научиться загружать данные из БД и сохранять результаты обратно.

**📋 Что нужно сделать:**
1. Подключиться к базе данных SQLite
2. Изучить структуру базы данных
3. Загрузить данные с помощью SQL запросов
4. Обработать данные в Pandas
5. Сохранить результаты обратно в базу

**📁 Используемые файлы:** `files/sample_database.db`, `files/sql-connection-example.py`

### 🏗️ **Шаг 1: Строительство моста**

```python
import sqlite3
import pandas as pd
from datetime import datetime

print("🏗️ IT-Архитектурное бюро 'Pandas & SQL'")
print("Проект: Мост между Python и базой данных")
print("=" * 50)

# Подключаемся к базе данных
try:
    conn = sqlite3.connect('files/sample_database.db')
    print("✅ Соединение с базой данных установлено")
except Exception as e:
    print(f"❌ Ошибка подключения: {e}")
    print("Убедитесь, что файл sample_database.db в папке files/")
    exit()

# Изучаем архитектуру базы данных
print(f"\n🏛️ ИЗУЧЕНИЕ АРХИТЕКТУРЫ БАЗЫ ДАННЫХ")
print("-" * 35)

# Получаем список таблиц
tables_query = "SELECT name FROM sqlite_master WHERE type='table';"
tables = pd.read_sql_query(tables_query, conn)

print("📋 Доступные таблицы:")
for table in tables['name']:
    print(f"   📊 {table}")
    
    # Получаем структуру каждой таблицы
    structure_query = f"PRAGMA table_info({table});"
    structure = pd.read_sql_query(structure_query, conn)
    
    print("      Столбцы:")
    for _, col in structure.iterrows():
        print(f"         • {col['name']} ({col['type']})")
    
    # Считаем количество записей
    count_query = f"SELECT COUNT(*) as count FROM {table};"
    count = pd.read_sql_query(count_query, conn)
    print(f"      Записей: {count['count'].iloc[0]:,}")
    print()
```

### 📥 **Шаг 2: Загрузка данных по частям**

```python
print(f"\n📥 ЗАГРУЗКА ДАННЫХ ИЗ БАЗЫ")
print("-" * 25)

# Загружаем клиентов
клиенты_query = """
SELECT 
    customer_id,
    customer_name,
    city,
    country,
    customer_segment,
    total_spent,
    registration_date
FROM customers
ORDER BY total_spent DESC
"""

df_customers = pd.read_sql_query(клиенты_query, conn)
print(f"👥 Загружено клиентов: {len(df_customers)}")
print("Топ-3 клиента по тратам:")
print(df_customers[['customer_name', 'total_spent', 'customer_segment']].head(3))

# Загружаем заказы с JOIN'ами
заказы_query = """
SELECT 
    o.order_id,
    o.customer_id,
    c.customer_name,
    c.city,
    c.country,
    o.order_date,
    o.total_amount,
    o.status
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
WHERE o.status IN ('Completed', 'Shipped')
ORDER BY o.order_date DESC
"""

df_orders = pd.read_sql_query(заказы_query, conn)
print(f"\n🛒 Загружено заказов: {len(df_orders)}")
print("Последние 3 заказа:")
print(df_orders[['customer_name', 'order_date', 'total_amount', 'status']].head(3))

# Загружаем детали заказов с товарами
детали_query = """
SELECT 
    oi.order_id,
    oi.product_id,
    p.product_name,
    p.supplier,
    c.category_name,
    oi.quantity,
    oi.unit_price,
    oi.total_price,
    p.unit_cost,
    (oi.total_price - (oi.quantity * p.unit_cost)) as profit
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
JOIN categories c ON p.category_id = c.category_id
ORDER BY oi.total_price DESC
"""

df_order_items = pd.read_sql_query(детали_query, conn)
print(f"\n📦 Загружено позиций заказов: {len(df_order_items)}")
print("Топ-3 позиции по выручке:")
print(df_order_items[['product_name', 'quantity', 'total_price', 'profit']].head(3))
```

### 🔄 **Шаг 3: Обработка данных в Pandas**

```python
print(f"\n🔄 ОБРАБОТКА ДАННЫХ В PANDAS")
print("-" * 28)

# Преобразуем даты
df_orders['order_date'] = pd.to_datetime(df_orders['order_date'])
df_customers['registration_date'] = pd.to_datetime(df_customers['registration_date'])

# Добавляем временные компоненты
df_orders['год'] = df_orders['order_date'].dt.year
df_orders['месяц'] = df_orders['order_date'].dt.month
df_orders['квартал'] = df_orders['order_date'].dt.quarter
df_orders['день_недели'] = df_orders['order_date'].dt.day_name()

print("📅 Добавлены временные компоненты к заказам")

# Создаем комплексную аналитику клиентов
print(f"\n📊 СОЗДАНИЕ КОМПЛЕКСНОЙ АНАЛИТИКИ")
print("-" * 32)

customer_analytics = df_orders.groupby(['customer_id', 'customer_name', 'city', 'country']).agg({
    'order_id': 'count',
    'total_amount': ['sum', 'mean'],
    'order_date': ['min', 'max']
}).round(2)

# Упрощаем названия столбцов
customer_analytics.columns = ['orders_count', 'total_revenue', 'avg_order_value', 'first_order', 'last_order']
customer_analytics = customer_analytics.reset_index()

# Добавляем дополнительные метрики
customer_analytics['customer_lifetime_days'] = (
    customer_analytics['last_order'] - customer_analytics['first_order']
).dt.days

# Избегаем деления на ноль
customer_analytics['orders_per_month'] = customer_analytics['orders_count'] / np.maximum(
    customer_analytics['customer_lifetime_days'] / 30.44, 1
)

# RFM анализ
def calculate_rfm_score(row):
    """Рассчитываем RFM оценку клиента"""
    recency = (datetime.now() - row['last_order']).days
    frequency = row['orders_count']
    monetary = row['total_revenue']
    
    # Простая система оценок от 1 до 5
    r_score = 5 if recency <= 30 else 4 if recency <= 90 else 3 if recency <= 180 else 2 if recency <= 365 else 1
    f_score = 5 if frequency >= 5 else 4 if frequency >= 3 else 3 if frequency >= 2 else 2 if frequency > 1 else 1
    m_score = 5 if monetary >= 5000 else 4 if monetary >= 2000 else 3 if monetary >= 1000 else 2 if monetary >= 500 else 1
    
    return f"{r_score}{f_score}{m_score}"

customer_analytics['rfm_score'] = customer_analytics.apply(calculate_rfm_score, axis=1)

# Сегментируем клиентов
def categorize_customer(rfm):
    """Категоризируем клиентов по RFM"""
    if rfm in ['555', '554', '544', '545', '454', '455', '445']:
        return 'Champions 🏆'
    elif rfm in ['543', '444', '435', '355', '354', '345', '344', '335']:
        return 'Loyal Customers 💎'
    elif rfm in ['512', '511', '422', '421', '412', '411']:
        return 'New Customers 🌟'
    elif rfm in ['155', '154', '144', '214', '215', '115', '114']:
        return 'At Risk ⚠️'
    else:
        return 'Others 👤'

customer_analytics['customer_category'] = customer_analytics['rfm_score'].apply(categorize_customer)

print("✅ RFM анализ и сегментация клиентов завершены")

# Показываем результаты
print(f"\n📊 Результаты сегментации:")
segmentation = customer_analytics['customer_category'].value_counts()
for category, count in segmentation.items():
    avg_revenue = customer_analytics[customer_analytics['customer_category'] == category]['total_revenue'].mean()
    print(f"   {category}: {count} клиентов (средняя выручка: ${avg_revenue:,.2f})")
```

### 📊 **Шаг 4: Продвинутая аналитика товаров**

```python
print(f"\n📦 АНАЛИЗ ТОВАРНОГО ПОРТФЕЛЯ")
print("-" * 25)

# Объединяем данные о товарах с заказами для полного анализа
product_analysis = df_order_items.groupby(['product_name', 'category_name', 'supplier']).agg({
    'quantity': 'sum',
    'total_price': 'sum',
    'profit': 'sum',
    'order_id': 'count'
}).round(2)

product_analysis.columns = ['total_quantity', 'total_revenue', 'total_profit', 'times_ordered']
product_analysis = product_analysis.reset_index()

# Добавляем метрики эффективности
product_analysis['profit_margin'] = (product_analysis['total_profit'] / product_analysis['total_revenue'] * 100).round(1)
product_analysis['avg_order_size'] = (product_analysis['total_quantity'] / product_analysis['times_ordered']).round(1)

print("🏆 ТОП-5 ТОВАРОВ ПО ПРИБЫЛИ:")
top_products = product_analysis.nlargest(5, 'total_profit')
for _, product in top_products.iterrows():
    print(f"   {product['product_name']} ({product['category_name']})")
    print(f"      Прибыль: ${product['total_profit']:,.2f}")
    print(f"      Маржа: {product['profit_margin']}%")
    print(f"      Заказов: {product['times_ordered']}")
    print()

# Анализ по категориям
category_analysis = product_analysis.groupby('category_name').agg({
    'total_revenue': 'sum',
    'total_profit': 'sum',
    'times_ordered': 'sum'
}).round(2)

category_analysis['category_margin'] = (category_analysis['total_profit'] / category_analysis['total_revenue'] * 100).round(1)

print("📊 АНАЛИЗ ПО КАТЕГОРИЯМ:")
for category, data in category_analysis.iterrows():
    print(f"   {category}:")
    print(f"      Выручка: ${data['total_revenue']:,.2f}")
    print(f"      Прибыль: ${data['total_profit']:,.2f}")
    print(f"      Маржа: {data['category_margin']}%")
```

### 📤 **Шаг 5: Сохранение результатов в базу данных**

```python
print(f"\n📤 СОХРАНЕНИЕ РЕЗУЛЬТАТОВ В БАЗУ ДАННЫХ")
print("-" * 38)

try:
    # Сохраняем аналитику клиентов
    customer_analytics.to_sql('customer_analytics', conn, if_exists='replace', index=False)
    print("✅ Сохранена таблица customer_analytics")
    
    # Сохраняем анализ товаров
    product_analysis.to_sql('product_analytics', conn, if_exists='replace', index=False)
    print("✅ Сохранена таблица product_analytics")
    
    # Сохраняем анализ по категориям
    category_analysis.reset_index().to_sql('category_analytics', conn, if_exists='replace', index=False)
    print("✅ Сохранена таблица category_analytics")
    
    # Проверяем, что данные сохранились
    verification_query = """
    SELECT name, 
           (SELECT COUNT(*) FROM customer_analytics) as customer_count,
           (SELECT COUNT(*) FROM product_analytics) as product_count,
           (SELECT COUNT(*) FROM category_analytics) as category_count
    FROM sqlite_master 
    WHERE type='table' AND name LIKE '%analytics%'
    """
    
    verification = pd.read_sql_query(verification_query, conn)
    print(f"\n📊 Проверка сохраненных данных:")
    for _, row in verification.iterrows():
        print(f"   customer_analytics: {row['customer_count']} записей")
        print(f"   product_analytics: {row['product_count']} записей")  
        print(f"   category_analytics: {row['category_count']} записей")
        break
    
except Exception as e:
    print(f"❌ Ошибка при сохранении: {e}")

# Создаем исполнительный дашборд в виде SQL представления
dashboard_query = """
CREATE VIEW IF NOT EXISTS executive_dashboard AS
SELECT 
    'Total Revenue' as metric,
    printf('$%.2f', SUM(o.total_amount)) as value
FROM orders o
WHERE o.status IN ('Completed', 'Shipped')

UNION ALL

SELECT 
    'Total Customers' as metric,
    CAST(COUNT(DISTINCT c.customer_id) AS TEXT) as value
FROM customers c

UNION ALL

SELECT 
    'Average Order Value' as metric,
    printf('$%.2f', AVG(o.total_amount)) as value
FROM orders o
WHERE o.status IN ('Completed', 'Shipped')

UNION ALL

SELECT 
    'Total Orders' as metric,
    CAST(COUNT(*) AS TEXT) as value
FROM orders o
WHERE o.status IN ('Completed', 'Shipped')
"""

try:
    conn.execute(dashboard_query)
    conn.commit()
    
    dashboard = pd.read_sql_query("SELECT * FROM executive_dashboard", conn)
    print(f"\n📊 ИСПОЛНИТЕЛЬНЫЙ ДАШБОРД:")
    for _, row in dashboard.iterrows():
        print(f"   {row['metric']}: {row['value']}")
    
    print("✅ Создано SQL представление executive_dashboard")
    
except Exception as e:
    print(f"⚠️ Не удалось создать дашборд: {e}")

# Закрываем соединение
conn.close()
print(f"\n🔒 Соединение с базой данных закрыто")
print("✅ IT-архитектурный проект завершен успешно!")
```

**❓ Архитектурные вопросы:**
1. Какие преимущества дает объединение SQL и Pandas?
2. Когда лучше использовать SQL, а когда Pandas?
3. Как можно автоматизировать этот процесс для ежедневной работы?

---

## 📊 Задание 5: "Директор по аналитике" — создаем исполнительный дашборд

**🎬 Ваша роль:** Вы директор по аналитике. Нужно создать комплексный отчет для совета директоров с ключевыми показателями, трендами и рекомендациями.

**📋 Что нужно сделать:**
1. Объединить все данные из предыдущих заданий
2. Создать систему KPI
3. Найти тренды и закономерности
4. Подготовить исполнительное резюме
5. Дать стратегические рекомендации

**📁 Используемые файлы:** Результаты всех предыдущих заданий

### 📊 **Шаг 1: Подготовка аналитической платформы**

```python
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

print("📊 Аналитический центр 'Executive Dashboard'")
print("Подготовка отчета для совета директоров")
print("=" * 50)

# Загружаем все доступные данные
datasets = {}

files_to_load = [
    ('cleaned_ecommerce_data.csv', 'cleaned_local'),
    ('customer_profiles.csv', 'customer_profiles'),
    ('unified_analysis.csv', 'unified'),
    ('files/large_dataset_sample.csv', 'global')
]

for filename, key in files_to_load:
    try:
        datasets[key] = pd.read_csv(filename)
        print(f"✅ Загружен {key}: {len(datasets[key]):,} записей")
    except FileNotFoundError:
        print(f"⚠️ Файл {filename} не найден")

# Выбираем основной датасет для анализа
if 'global' in datasets:
    df_main = datasets['global'].copy()
    source_name = "Глобальные данные"
elif 'unified' in datasets:
    df_main = datasets['unified'].copy()
    source_name = "Объединенные данные"
elif 'cleaned_local' in datasets:
    df_main = datasets['cleaned_local'].copy()
    source_name = "Локальные данные"
else:
    print("❌ Нет доступных данных для анализа")
    exit()

print(f"\n🎯 Основной датасет: {source_name}")
print(f"📊 Размер: {len(df_main):,} записей, {len(df_main.columns)} столбцов")

# Подготовка данных для анализа
if 'order_date' in df_main.columns:
    df_main['order_date'] = pd.to_datetime(df_main['order_date'], errors='coerce')

# Определяем поле с суммой заказа
amount_column = None
for col in ['final_price', 'total_amount', 'price']:
    if col in df_main.columns:
        amount_column = col
        break

if amount_column:
    df_main['revenue'] = df_main[amount_column]
    if 'quantity' in df_main.columns:
        df_main['revenue'] = df_main[amount_column] * df_main['quantity']
else:
    print("⚠️ Не найдено поле с суммой заказа, создаем тестовое")
    df_main['revenue'] = np.random.uniform(100, 2000, len(df_main))

print(f"💰 Общая выручка в анализе: ${df_main['revenue'].sum():,.2f}")
```

### 📈 **Шаг 2: Создание системы KPI**

```python
print(f"\n📈 КЛЮЧЕВЫЕ ПОКАЗАТЕЛИ ЭФФЕКТИВНОСТИ (KPI)")
print("=" * 45)

# Основные KPI
kpi = {}

# Финансовые KPI
kpi['общая_выручка'] = df_main['revenue'].sum()
kpi['средний_чек'] = df_main['revenue'].mean()
kpi['количество_заказов'] = len(df_main)

# Клиентские KPI
customer_column = None
for col in ['customer_id', 'customer_name']:
    if col in df_main.columns:
        customer_column = col
        break

if customer_column:
    kpi['количество_клиентов'] = df_main[customer_column].nunique()
    kpi['выручка_на_клиента'] = kpi['общая_выручка'] / kpi['количество_клиентов']
    kpi['заказов_на_клиента'] = kpi['количество_заказов'] / kpi['количество_клиентов']

# Товарные KPI
if 'category' in df_main.columns:
    kpi['количество_категорий'] = df_main['category'].nunique()

if 'product' in df_main.columns or 'product_name' in df_main.columns:
    product_col = 'product' if 'product' in df_main.columns else 'product_name'
    kpi['количество_товаров'] = df_main[product_col].nunique()

# Географические KPI
if 'region' in df_main.columns:
    kpi['количество_регионов'] = df_main['region'].nunique()

if 'country' in df_main.columns:
    kpi['количество_стран'] = df_main['country'].nunique()

# Выводим KPI
print("💼 ФИНАНСОВЫЕ ПОКАЗАТЕЛИ:")
print(f"   💰 Общая выручка: ${kpi['общая_выручка']:,.2f}")
print(f"   💳 Средний чек: ${kpi['средний_чек']:,.2f}")
print(f"   🛒 Общее количество заказов: {kpi['количество_заказов']:,}")

if customer_column:
    print(f"\n👥 КЛИЕНТСКИЕ ПОКАЗАТЕЛИ:")
    print(f"   👤 Уникальных клиентов: {kpi['количество_клиентов']:,}")
    print(f"   💰 Выручка на клиента: ${kpi['выручка_на_клиента']:,.2f}")
    print(f"   📈 Заказов на клиента: {kpi['заказов_на_клиента']:.1f}")

print(f"\n📦 ТОВАРНЫЕ ПОКАЗАТЕЛИ:")
if 'количество_категорий' in kpi:
    print(f"   🏷️ Категорий товаров: {kpi['количество_категорий']}")
if 'количество_товаров' in kpi:
    print(f"   📦 Уникальных товаров: {kpi['количество_товаров']}")

if 'количество_регионов' in kpi:
    print(f"\n🌍 ГЕОГРАФИЧЕСКИЕ ПОКАЗАТЕЛИ:")
    print(f"   🗺️ Регионов: {kpi['количество_регионов']}")
    if 'количество_стран' in kpi:
        print(f"   🏁 Стран: {kpi['количество_стран']}")
```

### 📊 **Шаг 3: Временной анализ и тренды**

```python
print(f"\n📊 АНАЛИЗ ТРЕНДОВ И ВРЕМЕННЫХ ПАТТЕРНОВ")
print("=" * 40)

if 'order_date' in df_main.columns and df_main['order_date'].notna().sum() > 100:
    
    # Готовим временные компоненты
    df_temp = df_main[df_main['order_date'].notna()].copy()
    df_temp['year'] = df_temp['order_date'].dt.year
    df_temp['month'] = df_temp['order_date'].dt.month
    df_temp['quarter'] = df_temp['order_date'].dt.quarter
    df_temp['day_of_week'] = df_temp['order_date'].dt.day_name()
    
    # Анализ по годам
    if df_temp['year'].nunique() > 1:
        yearly_trends = df_temp.groupby('year').agg({
            'revenue': ['sum', 'mean', 'count'],
            customer_column: 'nunique' if customer_column else lambda x: len(x)
        }).round(2)
        
        yearly_trends.columns = ['total_revenue', 'avg_order', 'orders_count', 'unique_customers']
        
        print("📅 ТРЕНДЫ ПО ГОДАМ:")
        for year, data in yearly_trends.iterrows():
            print(f"   {year}: ${data['total_revenue']:,.2f} выручка, {data['orders_count']:,} заказов")
        
        # Рассчитываем рост год к году
        if len(yearly_trends) >= 2:
            years = sorted(yearly_trends.index)
            current_year = years[-1]
            previous_year = years[-2]
            
            revenue_growth = ((yearly_trends.loc[current_year, 'total_revenue'] - 
                             yearly_trends.loc[previous_year, 'total_revenue']) / 
                             yearly_trends.loc[previous_year, 'total_revenue']) * 100
            
            print(f"\n📈 Рост выручки {previous_year} → {current_year}: {revenue_growth:+.1f}%")
    
    # Сезонный анализ
    seasonal_analysis = df_temp.groupby('month').agg({
        'revenue': ['sum', 'mean'],
        'order_date': 'count'
    }).round(2)
    
    seasonal_analysis.columns = ['monthly_revenue', 'avg_monthly_order', 'orders_count']
    
    months = ['', 'Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн',
              'Июл', 'Авг', 'Сен', 'Окт', 'Ноя', 'Дек']
    
    print(f"\n📊 СЕЗОННОСТЬ ПРОДАЖ:")
    for month_num, data in seasonal_analysis.iterrows():
        month_name = months[month_num] if month_num <= 12 else f"М{month_num}"
        share = (data['monthly_revenue'] / seasonal_analysis['monthly_revenue'].sum()) * 100
        print(f"   {month_name}: ${data['monthly_revenue']:,.2f} ({share:.1f}%)")
    
    # Находим пики и спады
    best_month = seasonal_analysis['monthly_revenue'].idxmax()
    worst_month = seasonal_analysis['monthly_revenue'].idxmin()
    
    print(f"\n🏆 Лучший месяц: {months[best_month]} (${seasonal_analysis.loc[best_month, 'monthly_revenue']:,.2f})")
    print(f"📉 Худший месяц: {months[worst_month]} (${seasonal_analysis.loc[worst_month, 'monthly_revenue']:,.2f})")
    
    # Анализ по дням недели
    weekday_analysis = df_temp.groupby('day_of_week')['revenue'].sum().sort_values(ascending=False)
    
    print(f"\n📊 ПРОДАЖИ ПО ДНЯМ НЕДЕЛИ:")
    for day, revenue in weekday_analysis.items():
        share = (revenue / weekday_analysis.sum()) * 100
        print(f"   {day}: ${revenue:,.2f} ({share:.1f}%)")

else:
    print("⚠️ Недостаточно данных для временного анализа")
```

### 🎯 **Шаг 4: Сегментационный анализ**

```python
print(f"\n🎯 СЕГМЕНТАЦИОННЫЙ АНАЛИЗ")
print("=" * 25)

# Географическая сегментация
if 'region' in df_main.columns and 'country' in df_main.columns:
    print("🌍 ГЕОГРАФИЧЕСКИЙ АНАЛИЗ:")
    
    geo_analysis = df_main.groupby(['region', 'country']).agg({
        'revenue': ['sum', 'mean', 'count'],
        customer_column: 'nunique' if customer_column else lambda x: len(x)
    }).round(2)
    
    geo_analysis.columns = ['total_revenue', 'avg_order', 'orders_count', 'unique_customers']
    geo_analysis = geo_analysis.reset_index().sort_values('total_revenue', ascending=False)
    
    print("\n🏆 ТОП-5 СТРАН ПО ВЫРУЧКЕ:")
    for i, (_, row) in enumerate(geo_analysis.head().iterrows(), 1):
        share = (row['total_revenue'] / df_main['revenue'].sum()) * 100
        efficiency = row['total_revenue'] / row['unique_customers'] if row['unique_customers'] > 0 else 0
        
        print(f"{i}. {row['country']} ({row['region']})")
        print(f"   💰 Выручка: ${row['total_revenue']:,.2f} ({share:.1f}%)")
        print(f"   👥 Клиентов: {row['unique_customers']:,}")
        print(f"   📊 Выручка/клиент: ${efficiency:,.2f}")
        print()

# Товарная сегментация
if 'category' in df_main.columns:
    print("📦 АНАЛИЗ ПО КАТЕГОРИЯМ ТОВАРОВ:")
    
    category_analysis = df_main.groupby('category').agg({
        'revenue': ['sum', 'mean', 'count'],
        'quantity': 'sum' if 'quantity' in df_main.columns else lambda x: len(x)
    }).round(2)
    
    category_analysis.columns = ['total_revenue', 'avg_order', 'orders_count', 'total_quantity']
    category_analysis = category_analysis.sort_values('total_revenue', ascending=False)
    
    for category, data in category_analysis.iterrows():
        share = (data['total_revenue'] / df_main['revenue'].sum()) * 100
        print(f"\n🏷️ {category}:")
        print(f"   💰 Выручка: ${data['total_revenue']:,.2f} ({share:.1f}%)")
        print(f"   🛒 Заказов: {data['orders_count']:,}")
        print(f"   📦 Единиц продано: {data['total_quantity']:,}")
        print(f"   💳 Средний чек: ${data['avg_order']:,.2f}")

# Клиентская сегментация (если есть профили клиентов)
if 'customer_profiles' in datasets:
    profiles = datasets['customer_profiles']
    
    if 'класс' in profiles.columns:
        print(f"\n👥 СЕГМЕНТАЦИЯ КЛИЕНТОВ:")
        
        client_segments = profiles['класс'].value_counts()
        total_revenue_profiles = profiles['общая_выручка'].sum()
        
        for segment, count in client_segments.items():
            segment_revenue = profiles[profiles['класс'] == segment]['общая_выручка'].sum()
            share = (segment_revenue / total_revenue_profiles) * 100
            avg_revenue = segment_revenue / count
            
            print(f"   {segment}:")
            print(f"      Клиентов: {count} ({count/len(profiles)*100:.1f}%)")
            print(f"      Выручка: ${segment_revenue:,.2f} ({share:.1f}%)")
            print(f"      Средняя выручка/клиент: ${avg_revenue:,.2f}")
```

### 📋 **Шаг 5: Исполнительное резюме и рекомендации**

```python
print(f"\n📋 ИСПОЛНИТЕЛЬНОЕ РЕЗЮМЕ")
print("=" * 25)

# Создаем сводку ключевых метрик
executive_summary = {
    'Финансовые показатели': {
        'Общая выручка': f"${kpi['общая_выручка']:,.2f}",
        'Средний чек': f"${kpi['средний_чек']:,.2f}",
        'Количество заказов': f"{kpi['количество_заказов']:,}"
    }
}

if customer_column:
    executive_summary['Клиентские показатели'] = {
        'Всего клиентов': f"{kpi['количество_клиентов']:,}",
        'Выручка на клиента': f"${kpi['выручка_на_клиента']:,.2f}",
        'Заказов на клиента': f"{kpi['заказов_на_клиента']:.1f}"
    }

# Выводим резюме
for category, metrics in executive_summary.items():
    print(f"\n📊 {category.upper()}:")
    for metric, value in metrics.items():
        print(f"   • {metric}: {value}")

# Ключевые находки
print(f"\n🔍 КЛЮЧЕВЫЕ НАХОДКИ:")

findings = []

# Находка 1: Географическая концентрация
if 'region' in df_main.columns:
    top_region_revenue = df_main.groupby('region')['revenue'].sum().max()
    total_revenue = df_main['revenue'].sum()
    concentration = (top_region_revenue / total_revenue) * 100
    
    if concentration > 40:
        top_region = df_main.groupby('region')['revenue'].sum().idxmax()
        findings.append(f"🌍 Высокая географическая концентрация: {top_region} дает {concentration:.1f}% выручки")

# Находка 2: Товарная концентрация  
if 'category' in df_main.columns:
    top_category_revenue = df_main.groupby('category')['revenue'].sum().max()
    category_concentration = (top_category_revenue / total_revenue) * 100
    
    if category_concentration > 30:
        top_category = df_main.groupby('category')['revenue'].sum().idxmax()
        findings.append(f"📦 Доминирование категории: {top_category} составляет {category_concentration:.1f}% выручки")

# Находка 3: Сезонность
if 'order_date' in df_main.columns and df_main['order_date'].notna().sum() > 100:
    df_temp = df_main[df_main['order_date'].notna()].copy()
    monthly_revenues = df_temp.groupby(df_temp['order_date'].dt.month)['revenue'].sum()
    
    if len(monthly_revenues) >= 3:
        seasonality_ratio = monthly_revenues.max() / monthly_revenues.min()
        if seasonality_ratio > 1.5:
            findings.append(f"📅 Выраженная сезонность: разброс продаж по месяцам {seasonality_ratio:.1f}x")

# Выводим находки
for i, finding in enumerate(findings, 1):
    print(f"{i}. {finding}")

if not findings:
    print("📊 Бизнес показывает сбалансированное развитие без критических концентраций")

# Стратегические рекомендации
print(f"\n💡 СТРАТЕГИЧЕСКИЕ РЕКОМЕНДАЦИИ:")

recommendations = [
    "📈 Развивайте лидирующие сегменты с высокой маржинальностью",
    "🌍 Диверсифицируйте географическое присутствие для снижения рисков",
    "👥 Внедрите программы лояльности для удержания ключевых клиентов",
    "📦 Оптимизируйте товарный портфель на основе анализа прибыльности",
    "📅 Планируйте запасы и маркетинг с учетом сезонных колебаний",
    "📊 Автоматизируйте сбор и анализ данных для оперативного принятия решений"
]

for i, rec in enumerate(recommendations, 1):
    print(f"{i}. {rec}")

# Создаем финальный дашборд
dashboard_data = []

for category, metrics in executive_summary.items():
    for metric, value in metrics.items():
        dashboard_data.append({
            'Category': category,
            'Metric': metric,
            'Value': value,
            'Report_Date': datetime.now().strftime('%Y-%m-%d')
        })

dashboard_df = pd.DataFrame(dashboard_data)

# Сохраняем исполнительный отчет
dashboard_df.to_csv('executive_dashboard.csv', index=False, encoding='utf-8-sig')

# Создаем текстовый отчет
report_text = f"""
ИСПОЛНИТЕЛЬНЫЙ ОТЧЕТ ПО АНАЛИТИКЕ ДАННЫХ
Дата: {datetime.now().strftime('%d.%m.%Y %H:%M')}
Источник: {source_name}

КЛЮЧЕВЫЕ ПОКАЗАТЕЛИ:
• Общая выручка: ${kpi['общая_выручка']:,.2f}
• Средний чек: ${kpi['средний_чек']:,.2f}
• Количество заказов: {kpi['количество_заказов']:,}
"""

if customer_column:
    report_text += f"""• Клиентов: {kpi['количество_клиентов']:,}
• Выручка на клиента: ${kpi['выручка_на_клиента']:,.2f}
"""

report_text += f"""
КЛЮЧЕВЫЕ НАХОДКИ:
"""

for i, finding in enumerate(findings, 1):
    report_text += f"{i}. {finding}\n"

report_text += f"""
РЕКОМЕНДАЦИИ:
"""

for i, rec in enumerate(recommendations, 1):
    report_text += f"{i}. {rec}\n"

with open('executive_report.txt', 'w', encoding='utf-8') as f:
    f.write(report_text)

print(f"\n💾 ОТЧЕТЫ СОХРАНЕНЫ:")
print("   • executive_dashboard.csv - Табличный дашборд")
print("   • executive_report.txt - Текстовый отчет")

print(f"\n🎉 Аналитический отчет для совета директоров готов!")
print("✅ Все задания главы 14 успешно выполнены!")
```

**❓ Стратегические вопросы:**
1. Какие ключевые риски вы выявили для бизнеса?
2. Какие возможности роста имеют наибольший потенциал?
3. Какие метрики следует отслеживать ежедневно для оперативного управления?

---

- 🔙 [Предыдущая глава: Глава 13 - Основы DAX: вычисляемые столбцы и меры](../chapter-13/README.md)
- 🔜 [Следующая глава: Глава 15 - Визуализация в Python: Matplotlib и Seaborn](../chapter-15/README.md)

---

- 📢 Присоединяйтесь к чату курса: [https://t.me/analytics_course_chat](https://t.me/analytics_course_chat)
- 📢 Канал курса: [https://t.me/analytics_course_channel](https://t.me/analytics_course_channel)