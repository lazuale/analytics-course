# 📝 Практические задания для главы 18

📖 [Вернуться к теории](../README.md) | 📁 [Учебные файлы](../files/README.md) | ✅ [Чек-лист](../checklist.md)

## 🎯 Обзор заданий

В этой главе вы выполните **5 практических заданий** возрастающей сложности:

1. **🌤️ Базовое API** — получение данных о погоде  
2. **💱 Валютный мониторинг** — отслеживание курсов валют
3. **📊 Анализ API данных** — исследование и визуализация
4. **🔄 Автоматизация сбора** — планировщик для регулярного получения данных
5. **🚀 Продвинутая система** — полноценная система мониторинга с базой данных

**⏱️ Общее время выполнения:** 6-8 часов  
**🎯 Результат:** Рабочая система автоматического сбора и анализа данных через API

---

## 📋 Задание 1: Первое знакомство с API

**🎯 Цель:** Научиться делать простые API запросы и обрабатывать ответы

**🛠️ Инструменты:** Python, requests, pandas

**⏱️ Время:** 45 минут

### Что нужно сделать:

#### 1️⃣ Получение данных о погоде

Используя **OpenWeatherMap API**, получите данные о погоде для 5 российских городов:

```python
import requests
import pandas as pd
import json
from datetime import datetime

def get_weather_for_city(city_name, api_key):
    """
    Получите данные о погоде для одного города
    Верните словарь с ключевыми показателями
    """
    # ВАШ КОД ЗДЕСЬ
    pass

# Список городов для анализа
cities = ["Moscow", "Saint Petersburg", "Novosibirsk", "Yekaterinburg", "Nizhny Novgorod"]

# Получите API ключ на https://openweathermap.org/api (бесплатно)
api_key = "YOUR_API_KEY_HERE"  # Замените на реальный ключ

# Соберите данные по всем городам
weather_data = []
for city in cities:
    try:
        data = get_weather_for_city(city, api_key)
        weather_data.append(data)
        print(f"✅ Получены данные для {city}")
    except Exception as e:
        print(f"❌ Ошибка для {city}: {e}")
```

#### 2️⃣ Анализ полученных данных

```python
# Преобразуйте данные в DataFrame
weather_df = pd.DataFrame(weather_data)

# Выполните базовый анализ:
print("🌡️ Самый теплый город:")
print(weather_df.loc[weather_df['temperature'].idxmax()])

print("\n💨 Самый ветреный город:")
print(weather_df.loc[weather_df['wind_speed'].idxmax()])

print("\n💧 Самая высокая влажность:")
print(weather_df.loc[weather_df['humidity'].idxmax()])
```

#### 3️⃣ Сохранение результатов

```python
# Сохраните данные в CSV с временной меткой
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"weather_data_{timestamp}.csv"
weather_df.to_csv(filename, index=False, encoding='utf-8')
print(f"📄 Данные сохранены в {filename}")
```

### ✅ Ожидаемый результат:

- CSV файл с данными о погоде в 5 городах
- Вывод в консоль с анализом (самый теплый/ветренный/влажный город)  
- Работающий код без ошибок

---

## 📋 Задание 2: Мониторинг валютных курсов

**🎯 Цель:** Создать систему отслеживания изменений валютных курсов

**🛠️ Инструменты:** Python, requests, matplotlib

**⏱️ Время:** 60 минут

### Что нужно сделать:

#### 1️⃣ Создание функции получения курсов

```python
import matplotlib.pyplot as plt
import time

def get_exchange_rates(base_currency="USD"):
    """
    Получите актуальные курсы валют
    Используйте API: https://api.exchangerate-api.com/v4/latest/USD
    """
    # ВАШ КОД ЗДЕСЬ
    pass

def track_currency_changes(currencies_to_track, hours_to_monitor=2):
    """
    Отслеживайте изменения курсов в режиме реального времени
    
    currencies_to_track: список валют для отслеживания ['RUB', 'EUR', 'GBP']
    hours_to_monitor: сколько часов мониторить (для тестирования используйте 0.1)
    """
    
    tracking_data = {currency: {'rates': [], 'timestamps': []} 
                    for currency in currencies_to_track}
    
    # Мониторинг курсов каждые 5 минут
    end_time = time.time() + hours_to_monitor * 3600
    
    while time.time() < end_time:
        try:
            rates = get_exchange_rates("USD")
            current_time = datetime.now()
            
            for currency in currencies_to_track:
                if currency in rates:
                    tracking_data[currency]['rates'].append(rates[currency])
                    tracking_data[currency]['timestamps'].append(current_time)
            
            print(f"📊 {current_time.strftime('%H:%M:%S')} - Данные обновлены")
            
            # Ждем 5 минут (для тестирования - 30 секунд)
            time.sleep(30)  # Измените на 300 для реального использования
            
        except Exception as e:
            print(f"❌ Ошибка: {e}")
            time.sleep(30)
    
    return tracking_data
```

#### 2️⃣ Визуализация изменений курсов

```python
def plot_currency_trends(tracking_data):
    """Создайте графики изменения курсов"""
    
    plt.figure(figsize=(15, 8))
    
    for i, (currency, data) in enumerate(tracking_data.items()):
        plt.subplot(2, 2, i+1)
        plt.plot(data['timestamps'], data['rates'], marker='o', linewidth=2)
        plt.title(f'💱 Курс {currency}/USD')
        plt.xlabel('Время')
        plt.ylabel('Курс')
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3)
        
        # Добавьте аннотацию с изменением
        if len(data['rates']) > 1:
            change = data['rates'][-1] - data['rates'][0]
            change_pct = (change / data['rates'][0]) * 100
            plt.text(0.02, 0.98, f'Изменение: {change_pct:+.2f}%', 
                    transform=plt.gca().transAxes, verticalalignment='top',
                    bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    plt.tight_layout()
    plt.savefig('currency_trends.png', dpi=300, bbox_inches='tight')
    plt.show()

# Запуск мониторинга
currencies = ['RUB', 'EUR', 'GBP', 'JPY']
tracking_results = track_currency_changes(currencies, hours_to_monitor=0.1)
plot_currency_trends(tracking_results)
```

#### 3️⃣ Анализ и алерты

```python
def analyze_currency_changes(tracking_data, alert_threshold=0.5):
    """Анализ изменений и создание алертов"""
    
    analysis_results = {}
    
    for currency, data in tracking_data.items():
        if len(data['rates']) < 2:
            continue
            
        start_rate = data['rates'][0]
        end_rate = data['rates'][-1]
        max_rate = max(data['rates'])
        min_rate = min(data['rates'])
        
        change_pct = ((end_rate - start_rate) / start_rate) * 100
        volatility = ((max_rate - min_rate) / start_rate) * 100
        
        analysis_results[currency] = {
            'start_rate': start_rate,
            'end_rate': end_rate,
            'change_percent': change_pct,
            'volatility': volatility,
            'max_rate': max_rate,
            'min_rate': min_rate
        }
        
        # Создаем алерт при значительном изменении
        if abs(change_pct) > alert_threshold:
            direction = "📈 вырос" if change_pct > 0 else "📉 упал"
            print(f"🚨 АЛЕРТ: {currency} {direction} на {abs(change_pct):.2f}%!")
    
    return analysis_results

# Анализ результатов
analysis = analyze_currency_changes(tracking_results, alert_threshold=0.1)

# Создайте отчет
print("\n📊 ОТЧЕТ ПО ВАЛЮТНЫМ КУРСАМ:")
print("=" * 50)
for currency, stats in analysis.items():
    print(f"\n💰 {currency}:")
    print(f"   Начальный курс: {stats['start_rate']:.4f}")
    print(f"   Конечный курс: {stats['end_rate']:.4f}")
    print(f"   Изменение: {stats['change_percent']:+.2f}%")
    print(f"   Волатильность: {stats['volatility']:.2f}%")
```

### ✅ Ожидаемый результат:

- График изменения курсов 4 валют
- Анализ с процентными изменениями
- Система алертов при значительных колебаниях

---

## 📋 Задание 3: Комплексный анализ API данных

**🎯 Цель:** Объединить данные из разных API и провести аналитическое исследование

**🛠️ Инструменты:** Python, requests, pandas, seaborn

**⏱️ Время:** 90 минут

### Что нужно сделать:

#### 1️⃣ Сбор данных из множественных источников

```python
import seaborn as sns
from datetime import datetime, timedelta

def collect_multi_source_data():
    """
    Соберите данные из разных API источников
    """
    
    collected_data = {}
    
    # 1. Погодные данные для крупных городов
    print("🌤️ Собираем погодные данные...")
    weather_api_key = "YOUR_WEATHER_API_KEY"
    major_cities = ["Moscow", "London", "New York", "Tokyo", "Sydney"]
    
    weather_data = []
    for city in major_cities:
        # ВАШ КОД для получения погоды
        pass
    
    collected_data['weather'] = pd.DataFrame(weather_data)
    
    # 2. Валютные курсы
    print("💱 Собираем валютные данные...")
    rates = get_exchange_rates("USD")
    major_currencies = ['RUB', 'EUR', 'GBP', 'JPY', 'CNY', 'CAD', 'AUD']
    
    currency_data = []
    for currency in major_currencies:
        if currency in rates:
            currency_data.append({
                'currency': currency,
                'rate': rates[currency],
                'collected_at': datetime.now()
            })
    
    collected_data['currencies'] = pd.DataFrame(currency_data)
    
    # 3. Тестовые пользовательские данные (JSONPlaceholder)
    print("👥 Собираем данные пользователей...")
    users_response = requests.get('https://jsonplaceholder.typicode.com/users')
    posts_response = requests.get('https://jsonplaceholder.typicode.com/posts')
    
    if users_response.status_code == 200 and posts_response.status_code == 200:
        users_df = pd.DataFrame(users_response.json())
        posts_df = pd.DataFrame(posts_response.json())
        
        # Анализ активности пользователей
        user_activity = posts_df.groupby('userId').agg({
            'id': 'count',
            'title': lambda x: x.str.len().mean(),
            'body': lambda x: x.str.len().mean()
        }).round(2)
        
        user_activity.columns = ['posts_count', 'avg_title_length', 'avg_body_length']
        collected_data['user_activity'] = user_activity.reset_index()
    
    return collected_data

# Сбор всех данных
all_data = collect_multi_source_data()
```

#### 2️⃣ Создание комплексного анализа

```python
def create_comprehensive_analysis(data_dict):
    """Создайте комплексный анализ всех собранных данных"""
    
    # Создаем фигуру для множественных графиков
    fig, axes = plt.subplots(2, 3, figsize=(20, 12))
    fig.suptitle('🔍 КОМПЛЕКСНЫЙ АНАЛИЗ API ДАННЫХ', fontsize=16, fontweight='bold')
    
    # 1. Анализ температур по городам
    if 'weather' in data_dict and not data_dict['weather'].empty:
        weather_df = data_dict['weather']
        
        ax1 = axes[0, 0]
        weather_df.plot(x='city', y='temperature', kind='bar', ax=ax1, color='skyblue')
        ax1.set_title('🌡️ Температура по городам')
        ax1.set_ylabel('Температура (°C)')
        ax1.tick_params(axis='x', rotation=45)
    
    # 2. Валютные курсы (топ-6 по значению)
    if 'currencies' in data_dict and not data_dict['currencies'].empty:
        currency_df = data_dict['currencies'].nlargest(6, 'rate')
        
        ax2 = axes[0, 1]
        bars = ax2.bar(currency_df['currency'], currency_df['rate'], color='lightgreen')
        ax2.set_title('💰 Топ валют по курсу к USD')
        ax2.set_ylabel('Курс')
        
        # Добавим значения на столбцы
        for bar, value in zip(bars, currency_df['rate']):
            ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
                    f'{value:.2f}', ha='center', va='bottom')
    
    # 3. Анализ активности пользователей
    if 'user_activity' in data_dict:
        activity_df = data_dict['user_activity']
        
        ax3 = axes[0, 2]
        ax3.scatter(activity_df['posts_count'], activity_df['avg_body_length'], 
                   alpha=0.7, color='coral')
        ax3.set_xlabel('Количество постов')
        ax3.set_ylabel('Средняя длина поста')
        ax3.set_title('📝 Активность vs Качество контента')
        
        # Добавим линию тренда
        z = np.polyfit(activity_df['posts_count'], activity_df['avg_body_length'], 1)
        p = np.poly1d(z)
        ax3.plot(activity_df['posts_count'], p(activity_df['posts_count']), 
                "r--", alpha=0.8)
    
    # 4. Распределение температур (если есть данные)
    if 'weather' in data_dict and not data_dict['weather'].empty:
        ax4 = axes[1, 0]
        ax4.hist(weather_df['temperature'], bins=10, alpha=0.7, color='orange', edgecolor='black')
        ax4.set_title('📊 Распределение температур')
        ax4.set_xlabel('Температура (°C)')
        ax4.set_ylabel('Частота')
    
    # 5. Корреляционная матрица пользовательской активности
    if 'user_activity' in data_dict:
        ax5 = axes[1, 1]
        numeric_columns = activity_df.select_dtypes(include=[np.number]).columns
        correlation_matrix = activity_df[numeric_columns].corr()
        
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0,
                   square=True, ax=ax5, cbar_kws={'shrink': 0.8})
        ax5.set_title('🔗 Корреляции активности')
    
    # 6. Сводная таблица ключевых метрик
    ax6 = axes[1, 2]
    ax6.axis('off')
    
    summary_text = "📋 КЛЮЧЕВЫЕ МЕТРИКИ:\n\n"
    
    if 'weather' in data_dict and not data_dict['weather'].empty:
        avg_temp = weather_df['temperature'].mean()
        summary_text += f"🌡️ Средняя температура: {avg_temp:.1f}°C\n"
        summary_text += f"🏙️ Городов проанализировано: {len(weather_df)}\n\n"
    
    if 'currencies' in data_dict:
        currency_count = len(currency_df)
        max_rate = currency_df['rate'].max()
        summary_text += f"💱 Валют проанализировано: {currency_count}\n"
        summary_text += f"💰 Максимальный курс: {max_rate:.2f}\n\n"
    
    if 'user_activity' in data_dict:
        total_posts = activity_df['posts_count'].sum()
        avg_posts = activity_df['posts_count'].mean()
        summary_text += f"📝 Всего постов: {total_posts}\n"
        summary_text += f"📊 Среднее постов на юзера: {avg_posts:.1f}\n"
    
    summary_text += f"\n🕒 Анализ выполнен: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    
    ax6.text(0.1, 0.9, summary_text, transform=ax6.transAxes, fontsize=11,
            verticalalignment='top', bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
    
    plt.tight_layout()
    plt.savefig('comprehensive_api_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    return fig

# Выполнение анализа
analysis_figure = create_comprehensive_analysis(all_data)
```

#### 3️⃣ Создание отчета с выводами

```python
def generate_insights_report(data_dict):
    """Генерация отчета с инсайтами"""
    
    report = []
    report.append("🔍 ОТЧЕТ ПО КОМПЛЕКСНОМУ АНАЛИЗУ API ДАННЫХ")
    report.append("=" * 60)
    report.append(f"📅 Дата анализа: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("")
    
    # Анализ погодных данных
    if 'weather' in data_dict and not data_dict['weather'].empty:
        weather_df = data_dict['weather']
        
        hottest_city = weather_df.loc[weather_df['temperature'].idxmax()]
        coldest_city = weather_df.loc[weather_df['temperature'].idxmin()]
        
        report.append("🌤️ ПОГОДНЫЙ АНАЛИЗ:")
        report.append(f"   🔥 Самый теплый город: {hottest_city['city']} ({hottest_city['temperature']:.1f}°C)")
        report.append(f"   🧊 Самый холодный город: {coldest_city['city']} ({coldest_city['temperature']:.1f}°C)")
        report.append(f"   📊 Средняя температура: {weather_df['temperature'].mean():.1f}°C")
        report.append("")
    
    # Анализ валютных данных
    if 'currencies' in data_dict and not data_dict['currencies'].empty:
        currency_df = data_dict['currencies']
        
        strongest = currency_df.loc[currency_df['rate'].idxmax()]
        weakest = currency_df.loc[currency_df['rate'].idxmin()]
        
        report.append("💱 ВАЛЮТНЫЙ АНАЛИЗ:")
        report.append(f"   💪 Самая сильная валюта: {strongest['currency']} ({strongest['rate']:.4f} за $1)")
        report.append(f"   📉 Самая слабая валюта: {weakest['currency']} ({weakest['rate']:.4f} за $1)")
        report.append("")
    
    # Анализ пользовательской активности
    if 'user_activity' in data_dict:
        activity_df = data_dict['user_activity']
        
        most_active = activity_df.loc[activity_df['posts_count'].idxmax()]
        highest_quality = activity_df.loc[activity_df['avg_body_length'].idxmax()]
        
        report.append("👥 АНАЛИЗ ПОЛЬЗОВАТЕЛЬСКОЙ АКТИВНОСТИ:")
        report.append(f"   🏆 Самый активный пользователь: ID {most_active['userId']} ({most_active['posts_count']} постов)")
        report.append(f"   📝 Самые качественные посты: ID {highest_quality['userId']} ({highest_quality['avg_body_length']:.0f} симв/пост)")
        report.append(f"   📊 Средняя активность: {activity_df['posts_count'].mean():.1f} постов на пользователя")
        report.append("")
    
    # Бизнес-инсайты
    report.append("💡 БИЗНЕС-ИНСАЙТЫ И РЕКОМЕНДАЦИИ:")
    report.append("   🎯 API интеграция позволяет получать актуальные данные из разных источников")
    report.append("   🔄 Автоматизация сбора данных экономит время и повышает точность анализа")
    report.append("   📊 Комплексный анализ выявляет скрытые закономерности между разными метриками")
    report.append("   🚀 Регулярный мониторинг через API позволяет быстро реагировать на изменения")
    
    # Сохраняем отчет
    report_text = "\n".join(report)
    with open('api_analysis_report.txt', 'w', encoding='utf-8') as f:
        f.write(report_text)
    
    print(report_text)
    print(f"\n📄 Отчет сохранен в файл: api_analysis_report.txt")
    
    return report_text

# Генерация отчета
insights_report = generate_insights_report(all_data)
```

### ✅ Ожидаемый результат:

- Комплексный график с 6 видами анализа
- Подробный текстовый отчет с инсайтами
- Файлы: `comprehensive_api_analysis.png`, `api_analysis_report.txt`

---

## 📋 Задание 4: Автоматизация сбора данных

**🎯 Цель:** Создать систему автоматического сбора данных по расписанию

**🛠️ Инструменты:** Python, schedule, SQLite

**⏱️ Время:** 120 минут

### Что нужно сделать:

#### 1️⃣ Создание базы данных для хранения

```python
import sqlite3
import schedule
import time
from datetime import datetime, timedelta

def setup_database():
    """Создание SQLite базы для хранения API данных"""
    
    conn = sqlite3.connect('api_data.db')
    cursor = conn.cursor()
    
    # Таблица для погодных данных
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS weather_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT NOT NULL,
            temperature REAL,
            humidity INTEGER,
            pressure REAL,
            description TEXT,
            wind_speed REAL,
            collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Таблица для валютных курсов
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS currency_rates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            currency TEXT NOT NULL,
            rate REAL NOT NULL,
            base_currency TEXT DEFAULT 'USD',
            collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Таблица для логов сбора
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS collection_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data_type TEXT NOT NULL,
            status TEXT NOT NULL,
            records_count INTEGER,
            error_message TEXT,
            collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ База данных настроена")

def save_weather_to_db(weather_data):
    """Сохранение погодных данных в базу"""
    
    conn = sqlite3.connect('api_data.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO weather_data 
            (city, temperature, humidity, pressure, description, wind_speed)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            weather_data['city'],
            weather_data['temperature'],
            weather_data['humidity'],
            weather_data['pressure'],
            weather_data['description'],
            weather_data['wind_speed']
        ))
        
        conn.commit()
        return True
        
    except Exception as e:
        print(f"❌ Ошибка сохранения погоды: {e}")
        return False
    finally:
        conn.close()

def save_currencies_to_db(currency_data):
    """Сохранение валютных данных в базу"""
    
    conn = sqlite3.connect('api_data.db')
    cursor = conn.cursor()
    
    try:
        # Сохраняем все валюты одной транзакцией
        currency_records = [
            (currency, rate, 'USD') 
            for currency, rate in currency_data.items()
        ]
        
        cursor.executemany('''
            INSERT INTO currency_rates (currency, rate, base_currency)
            VALUES (?, ?, ?)
        ''', currency_records)
        
        conn.commit()
        return len(currency_records)
        
    except Exception as e:
        print(f"❌ Ошибка сохранения валют: {e}")
        return 0
    finally:
        conn.close()

# Настройка базы данных
setup_database()
```

#### 2️⃣ Создание автоматизированного сборщика

```python
class AutomatedDataCollector:
    """Автоматизированный сборщик данных из API"""
    
    def __init__(self, weather_api_key):
        self.weather_api_key = weather_api_key
        self.cities = ["Moscow", "Saint Petersburg", "Novosibirsk", "Yekaterinburg"]
        self.currencies = ['RUB', 'EUR', 'GBP', 'JPY', 'CNY']
        
    def log_collection(self, data_type, status, records_count=0, error_message=None):
        """Логирование результатов сбора"""
        
        conn = sqlite3.connect('api_data.db')
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO collection_logs 
                (data_type, status, records_count, error_message)
                VALUES (?, ?, ?, ?)
            ''', (data_type, status, records_count, error_message))
            
            conn.commit()
        except Exception as e:
            print(f"❌ Ошибка логирования: {e}")
        finally:
            conn.close()
    
    def collect_weather_data(self):
        """Сбор погодных данных для всех городов"""
        
        print(f"🌤️ {datetime.now().strftime('%H:%M:%S')} - Начинаем сбор погодных данных...")
        
        collected_count = 0
        errors = []
        
        for city in self.cities:
            try:
                weather_data = get_weather_for_city(city, self.weather_api_key)
                if save_weather_to_db(weather_data):
                    collected_count += 1
                    print(f"   ✅ {city}: {weather_data['temperature']:.1f}°C")
                else:
                    errors.append(f"Ошибка сохранения для {city}")
                    
                time.sleep(1)  # Пауза между запросами
                
            except Exception as e:
                error_msg = f"Ошибка для {city}: {e}"
                errors.append(error_msg)
                print(f"   ❌ {error_msg}")
        
        # Логирование результатов
        status = "SUCCESS" if collected_count > 0 else "FAILED"
        error_text = "; ".join(errors) if errors else None
        
        self.log_collection("weather", status, collected_count, error_text)
        print(f"🌤️ Погода: собрано {collected_count}/{len(self.cities)} городов")
        
        return collected_count
    
    def collect_currency_data(self):
        """Сбор данных о валютных курсах"""
        
        print(f"💱 {datetime.now().strftime('%H:%M:%S')} - Начинаем сбор валютных данных...")
        
        try:
            rates = get_exchange_rates("USD")
            
            # Фильтруем только нужные валюты
            filtered_rates = {currency: rates[currency] 
                            for currency in self.currencies 
                            if currency in rates}
            
            saved_count = save_currencies_to_db(filtered_rates)
            
            if saved_count > 0:
                self.log_collection("currency", "SUCCESS", saved_count)
                print(f"   ✅ Сохранено {saved_count} валютных курсов")
                
                # Выводим топ-3 курса
                sorted_rates = sorted(filtered_rates.items(), key=lambda x: x[1], reverse=True)
                for currency, rate in sorted_rates[:3]:
                    print(f"      💰 {currency}: {rate:.4f}")
            else:
                self.log_collection("currency", "FAILED", 0, "Не удалось сохранить данные")
                
            return saved_count
            
        except Exception as e:
            error_msg = f"Ошибка сбора валют: {e}"
            self.log_collection("currency", "FAILED", 0, error_msg)
            print(f"   ❌ {error_msg}")
            return 0
    
    def daily_collection_job(self):
        """Ежедневное задание сбора данных"""
        
        print(f"\n🚀 ЕЖЕДНЕВНЫЙ СБОР ДАННЫХ - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
        
        # Сбор погодных данных
        weather_count = self.collect_weather_data()
        
        # Пауза между типами данных
        time.sleep(2)
        
        # Сбор валютных данных
        currency_count = self.collect_currency_data()
        
        # Итоговая статистика
        total_records = weather_count + currency_count
        print(f"\n📊 ИТОГО СОБРАНО: {total_records} записей")
        print(f"   🌤️ Погода: {weather_count}")
        print(f"   💱 Валюты: {currency_count}")
        print("=" * 70)
        
        return total_records
    
    def hourly_currency_job(self):
        """Почасовое обновление валютных курсов"""
        
        print(f"\n🔄 ПОЧАСОВОЕ ОБНОВЛЕНИЕ ВАЛЮТ - {datetime.now().strftime('%H:%M:%S')}")
        currency_count = self.collect_currency_data()
        return currency_count

# Создание сборщика
collector = AutomatedDataCollector("YOUR_WEATHER_API_KEY")
```

#### 3️⃣ Настройка расписания и мониторинга

```python
def setup_collection_schedule(collector):
    """Настройка расписания автоматического сбора"""
    
    # Ежедневный полный сбор в 9:00
    schedule.every().day.at("09:00").do(collector.daily_collection_job)
    
    # Почасовое обновление валют в рабочее время
    for hour in range(9, 18):  # С 9 до 18 часов
        schedule.every().day.at(f"{hour:02d}:00").do(collector.hourly_currency_job)
    
    # Для тестирования - каждые 2 минуты
    schedule.every(2).minutes.do(collector.hourly_currency_job)
    
    print("⏰ Расписание настроено:")
    print("   🌅 Ежедневный полный сбор: 09:00")
    print("   🔄 Почасовое обновление валют: 09:00-17:00")
    print("   🧪 Тестовое обновление: каждые 2 минуты")

def get_collection_statistics():
    """Получение статистики сбора данных"""
    
    conn = sqlite3.connect('api_data.db')
    
    try:
        # Статистика по логам
        logs_query = '''
            SELECT 
                data_type,
                COUNT(*) as total_collections,
                SUM(CASE WHEN status = 'SUCCESS' THEN 1 ELSE 0 END) as successful,
                SUM(CASE WHEN status = 'SUCCESS' THEN records_count ELSE 0 END) as total_records,
                MAX(collected_at) as last_collection
            FROM collection_logs
            GROUP BY data_type
        '''
        
        logs_df = pd.read_sql(logs_query, conn)
        
        # Последние записи
        weather_query = '''
            SELECT COUNT(*) as count, MAX(collected_at) as latest
            FROM weather_data
            WHERE date(collected_at) = date('now')
        '''
        
        currency_query = '''
            SELECT COUNT(*) as count, MAX(collected_at) as latest
            FROM currency_rates
            WHERE date(collected_at) = date('now')
        '''
        
        weather_today = pd.read_sql(weather_query, conn)
        currency_today = pd.read_sql(currency_query, conn)
        
        # Печатаем статистику
        print("\n📊 СТАТИСТИКА СБОРА ДАННЫХ:")
        print("=" * 50)
        print(logs_df.to_string(index=False))
        
        print(f"\n📅 ДАННЫЕ ЗА СЕГОДНЯ:")
        print(f"   🌤️ Погодные записи: {weather_today['count'].iloc[0]}")
        print(f"   💱 Валютные записи: {currency_today['count'].iloc[0]}")
        
        return logs_df
        
    except Exception as e:
        print(f"❌ Ошибка получения статистики: {e}")
        return None
    finally:
        conn.close()

def run_automated_collection(duration_minutes=10):
    """Запуск автоматизированной системы сбора"""
    
    print(f"🚀 ЗАПУСК АВТОМАТИЗИРОВАННОЙ СИСТЕМЫ СБОРА ДАННЫХ")
    print(f"⏱️ Продолжительность тестирования: {duration_minutes} минут")
    print("=" * 70)
    
    # Настраиваем расписание
    setup_collection_schedule(collector)
    
    # Первоначальный сбор
    print("\n🎬 Выполняем первоначальный сбор данных...")
    collector.daily_collection_job()
    
    # Основной цикл
    start_time = time.time()
    end_time = start_time + (duration_minutes * 60)
    
    print(f"\n🔄 Начинаем автоматический режим...")
    
    while time.time() < end_time:
        schedule.run_pending()
        time.sleep(30)  # Проверяем каждые 30 секунд
        
        # Показываем статистику каждые 5 минут
        if int((time.time() - start_time) / 60) % 5 == 0:
            get_collection_statistics()
    
    print(f"\n🏁 АВТОМАТИЧЕСКИЙ СБОР ЗАВЕРШЕН")
    
    # Финальная статистика
    final_stats = get_collection_statistics()
    
    return final_stats

# Запуск автоматизированной системы (тестирование на 10 минут)
final_statistics = run_automated_collection(duration_minutes=10)
```

### ✅ Ожидаемый результат:

- База данных SQLite с тремя таблицами и реальными данными
- Система автоматического сбора по расписанию  
- Логирование всех операций и статистика работы
- Файл `api_data.db` с накопленными данными

---

## 📋 Задание 5: Продвинутая система мониторинга (Capstone Project)

**🎯 Цель:** Создать полноценную систему мониторинга с алертами и веб-дашбордом

**🛠️ Инструменты:** Python, FastAPI, HTML/CSS, SQLite

**⏱️ Время:** 180 минут

### Что нужно сделать:

#### 1️⃣ Создание системы алертов

```python
import smtplib
from email.mime.text import MimeText
from email.mime.multipart import MimeMultipart

class AlertSystem:
    """Система уведомлений и алертов"""
    
    def __init__(self):
        self.alert_rules = {
            'temperature': {'min': -30, 'max': 45},
            'currency_change': {'threshold': 5.0},  # 5% изменение
            'data_freshness': {'max_hours': 2}  # Данные старше 2 часов
        }
        self.alerts_sent = []
    
    def check_weather_alerts(self):
        """Проверка погодных алертов"""
        
        conn = sqlite3.connect('api_data.db')
        
        # Получаем последние данные по каждому городу
        query = '''
            SELECT city, temperature, collected_at
            FROM weather_data w1
            WHERE collected_at = (
                SELECT MAX(collected_at) 
                FROM weather_data w2 
                WHERE w2.city = w1.city
            )
        '''
        
        weather_df = pd.read_sql(query, conn)
        conn.close()
        
        alerts = []
        
        for _, row in weather_df.iterrows():
            temp = row['temperature']
            city = row['city']
            
            if temp < self.alert_rules['temperature']['min']:
                alerts.append({
                    'type': 'temperature',
                    'severity': 'critical',
                    'message': f"🥶 КРИТИЧЕСКИ НИЗКАЯ ТЕМПЕРАТУРА в {city}: {temp:.1f}°C",
                    'city': city,
                    'value': temp
                })
            elif temp > self.alert_rules['temperature']['max']:
                alerts.append({
                    'type': 'temperature', 
                    'severity': 'critical',
                    'message': f"🔥 КРИТИЧЕСКИ ВЫСОКАЯ ТЕМПЕРАТУРА в {city}: {temp:.1f}°C",
                    'city': city,
                    'value': temp
                })
        
        return alerts
    
    def check_currency_alerts(self):
        """Проверка алертов по валютам"""
        
        conn = sqlite3.connect('api_data.db')
        
        # Получаем изменение курсов за последние 24 часа
        query = '''
            SELECT 
                currency,
                rate as current_rate,
                LAG(rate) OVER (PARTITION BY currency ORDER BY collected_at) as previous_rate,
                collected_at
            FROM currency_rates
            WHERE datetime(collected_at) > datetime('now', '-24 hours')
            ORDER BY currency, collected_at DESC
        '''
        
        rates_df = pd.read_sql(query, conn)
        conn.close()
        
        alerts = []
        
        for currency in rates_df['currency'].unique():
            currency_data = rates_df[rates_df['currency'] == currency]
            
            if len(currency_data) >= 2:
                current = currency_data['current_rate'].iloc[0]
                previous = currency_data['previous_rate'].iloc[0]
                
                if pd.notna(previous) and previous > 0:
                    change_pct = ((current - previous) / previous) * 100
                    
                    if abs(change_pct) >= self.alert_rules['currency_change']['threshold']:
                        direction = "📈 вырос" if change_pct > 0 else "📉 упал"
                        alerts.append({
                            'type': 'currency',
                            'severity': 'warning',
                            'message': f"💱 {currency} {direction} на {abs(change_pct):.2f}%",
                            'currency': currency,
                            'change': change_pct,
                            'current_rate': current
                        })
        
        return alerts
    
    def send_telegram_alert(self, alerts):
        """Отправка алертов в Telegram (заглушка)"""
        
        if not alerts:
            return
        
        message = "🚨 СИСТЕМА АЛЕРТОВ\n\n"
        for alert in alerts:
            message += f"{alert['message']}\n"
        
        print(f"📱 Telegram Alert:")
        print(message)
        print("-" * 40)
        
        # Здесь был бы код отправки в реальный Telegram
        # bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        # chat_id = os.getenv('TELEGRAM_CHAT_ID')
        # requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage", 
        #               json={'chat_id': chat_id, 'text': message})
    
    def run_alert_check(self):
        """Запуск проверки всех алертов"""
        
        print(f"🔍 {datetime.now().strftime('%H:%M:%S')} - Проверяем алерты...")
        
        all_alerts = []
        
        # Проверяем погодные алерты
        weather_alerts = self.check_weather_alerts()
        all_alerts.extend(weather_alerts)
        
        # Проверяем валютные алерты
        currency_alerts = self.check_currency_alerts()
        all_alerts.extend(currency_alerts)
        
        if all_alerts:
            print(f"⚠️ Найдено {len(all_alerts)} алертов:")
            for alert in all_alerts:
                print(f"   {alert['message']}")
            
            self.send_telegram_alert(all_alerts)
            self.alerts_sent.extend(all_alerts)
        else:
            print("✅ Все показатели в норме")
        
        return all_alerts

# Создание системы алертов
alert_system = AlertSystem()
```

#### 2️⃣ Создание веб-дашборда

```python
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn
import json
from threading import Thread

app = FastAPI(title="API Data Monitor", version="1.0.0")
templates = Jinja2Templates(directory="templates")

def get_dashboard_data():
    """Получение данных для дашборда"""
    
    conn = sqlite3.connect('api_data.db')
    
    try:
        # Последние погодные данные
        weather_query = '''
            SELECT city, temperature, humidity, description, collected_at
            FROM weather_data w1
            WHERE collected_at = (
                SELECT MAX(collected_at) 
                FROM weather_data w2 
                WHERE w2.city = w1.city
            )
        '''
        weather_df = pd.read_sql(weather_query, conn)
        
        # Последние валютные курсы
        currency_query = '''
            SELECT currency, rate, collected_at
            FROM currency_rates c1
            WHERE collected_at = (
                SELECT MAX(collected_at)
                FROM currency_rates c2
                WHERE c2.currency = c1.currency
            )
            ORDER BY rate DESC
        '''
        currency_df = pd.read_sql(currency_query, conn)
        
        # Статистика сбора за последние 7 дней
        stats_query = '''
            SELECT 
                date(collected_at) as date,
                data_type,
                COUNT(*) as collections,
                SUM(records_count) as total_records
            FROM collection_logs
            WHERE datetime(collected_at) > datetime('now', '-7 days')
            GROUP BY date(collected_at), data_type
            ORDER BY date DESC
        '''
        stats_df = pd.read_sql(stats_query, conn)
        
        return {
            'weather': weather_df.to_dict('records'),
            'currencies': currency_df.to_dict('records'),
            'stats': stats_df.to_dict('records'),
            'last_update': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
    finally:
        conn.close()

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Главная страница дашборда"""
    
    data = get_dashboard_data()
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "data": data
    })

@app.get("/api/data")
async def api_data():
    """API endpoint для получения данных"""
    return get_dashboard_data()

@app.get("/api/alerts")
async def get_alerts():
    """API endpoint для получения алертов"""
    alerts = alert_system.run_alert_check()
    return {"alerts": alerts, "count": len(alerts)}

# Создание HTML шаблона дашборда
dashboard_html = '''
<!DOCTYPE html>
<html>
<head>
    <title>📊 API Data Monitor</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { 
            font-family: Arial, sans-serif; 
            margin: 0; 
            padding: 20px; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
        }
        .container { 
            max-width: 1200px; 
            margin: 0 auto; 
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }
        h1 { 
            text-align: center; 
            color: #4a5568; 
            margin-bottom: 30px;
            font-size: 2.5em;
        }
        .grid { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); 
            gap: 20px; 
            margin-bottom: 30px;
        }
        .card { 
            background: #f7fafc; 
            border-radius: 10px; 
            padding: 20px; 
            border-left: 5px solid #4299e1;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .card h3 { 
            margin-top: 0; 
            color: #2d3748; 
            border-bottom: 2px solid #e2e8f0;
            padding-bottom: 10px;
        }
        .weather-item, .currency-item { 
            display: flex; 
            justify-content: space-between; 
            padding: 10px 0; 
            border-bottom: 1px solid #e2e8f0;
        }
        .weather-item:last-child, .currency-item:last-child { 
            border-bottom: none; 
        }
        .temperature { 
            font-weight: bold; 
            color: #e53e3e; 
        }
        .currency { 
            font-weight: bold; 
            color: #38a169; 
        }
        .last-update { 
            text-align: center; 
            color: #718096; 
            font-style: italic; 
            margin-top: 20px;
        }
        .status-indicator {
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 8px;
        }
        .status-ok { background-color: #48bb78; }
        .status-warning { background-color: #ed8936; }
        .status-error { background-color: #f56565; }
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 API Data Monitor Dashboard</h1>
        
        <div class="grid">
            <div class="card">
                <h3>🌤️ Текущая погода</h3>
                {% for weather in data.weather %}
                <div class="weather-item">
                    <span>{{ weather.city }}</span>
                    <span class="temperature">{{ "%.1f"|format(weather.temperature) }}°C</span>
                </div>
                {% endfor %}
            </div>
            
            <div class="card">
                <h3>💱 Валютные курсы (USD)</h3>
                {% for currency in data.currencies %}
                <div class="currency-item">
                    <span>{{ currency.currency }}</span>
                    <span class="currency">{{ "%.4f"|format(currency.rate) }}</span>
                </div>
                {% endfor %}
            </div>
            
            <div class="card">
                <h3>📈 Статистика сбора</h3>
                {% for stat in data.stats %}
                <div class="weather-item">
                    <span>{{ stat.data_type }}</span>
                    <span>{{ stat.total_records }} записей</span>
                </div>
                {% endfor %}
            </div>
        </div>
        
        <div class="last-update">
            <span class="status-indicator status-ok"></span>
            Последнее обновление: {{ data.last_update }}
        </div>
    </div>
    
    <script>
        // Автообновление каждые 60 секунд
        setTimeout(function() {
            location.reload();
        }, 60000);
    </script>
</body>
</html>
'''

# Создание директории templates и сохранение HTML
import os
os.makedirs("templates", exist_ok=True)
with open("templates/dashboard.html", "w", encoding="utf-8") as f:
    f.write(dashboard_html)

print("✅ HTML шаблон дашборда создан")
```

#### 3️⃣ Запуск полной системы мониторинга

```python
def run_full_monitoring_system():
    """Запуск полной системы мониторинга"""
    
    print("🚀 ЗАПУСК ПОЛНОЙ СИСТЕМЫ МОНИТОРИНГА")
    print("=" * 60)
    
    # 1. Настройка всех компонентов
    setup_database()
    
    # 2. Создание сборщика данных
    collector = AutomatedDataCollector("YOUR_WEATHER_API_KEY")
    
    # 3. Первоначальный сбор данных
    print("\n📊 Выполняем первоначальный сбор данных...")
    collector.daily_collection_job()
    
    # 4. Настройка расписания
    # Каждые 5 минут для демонстрации
    schedule.every(5).minutes.do(collector.hourly_currency_job)
    schedule.every(10).minutes.do(collector.collect_weather_data)
    schedule.every(3).minutes.do(alert_system.run_alert_check)
    
    print("\n⚠️ Настройка алертов...")
    # Тестовый алерт с низким порогом
    alert_system.alert_rules['currency_change']['threshold'] = 0.1  # 0.1% для демо
    
    def run_scheduler():
        """Функция для запуска планировщика в отдельном потоке"""
        while True:
            schedule.run_pending()
            time.sleep(30)
    
    def run_web_server():
        """Функция для запуска веб-сервера"""
        uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
    
    # 5. Запуск планировщика в отдельном потоке
    scheduler_thread = Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()
    
    print("\n🌐 Запуск веб-дашборда на http://127.0.0.1:8000")
    print("📱 Система алертов активна")
    print("🔄 Автоматический сбор данных каждые 5-10 минут")
    print("\n" + "=" * 60)
    print("💡 Откройте браузер и перейдите на http://127.0.0.1:8000")
    print("💡 Нажмите Ctrl+C для остановки системы")
    print("=" * 60)
    
    # 6. Запуск веб-сервера (блокирующая операция)
    try:
        run_web_server()
    except KeyboardInterrupt:
        print("\n🛑 Система мониторинга остановлена пользователем")
    except Exception as e:
        print(f"\n❌ Ошибка системы: {e}")
    
    print("🏁 Полная система мониторинга завершена")

# Демо запуск (закомментируйте для реального использования)
print("🎬 ДЕМОНСТРАЦИЯ: Создание всех компонентов системы...")

# Создание демо данных
setup_database()
collector = AutomatedDataCollector("demo-key")
print("✅ Сборщик данных создан")

print("✅ Система алертов создана")

print("✅ Веб-дашборд настроен")

print("\n🚀 Все компоненты системы мониторинга готовы!")
print("💡 Для запуска полной системы используйте:")
print("   run_full_monitoring_system()")
```

### ✅ Ожидаемый результат:

- **Полноценная система мониторинга** с автоматическим сбором данных
- **Веб-дашборд** на http://127.0.0.1:8000 с актуальными данными
- **Система алертов** с проверкой аномалий и уведомлениями
- **База данных** с накопленной историей данных
- **Логирование** всех операций и ошибок

---

## 💡 Рекомендации по выполнению

### 📋 Общие советы:

1. **🔑 API ключи:** Получите бесплатные ключи на соответствующих сайтах
2. **⏰ Тестирование:** Используйте короткие интервалы для быстрого тестирования
3. **💾 Данные:** Сохраняйте все промежуточные результаты
4. **🐛 Отладка:** Добавляйте подробные print() для отслеживания процесса

### 🔧 Технические требования:

```bash
# Установка необходимых библиотек
pip install requests pandas matplotlib seaborn schedule sqlite3 fastapi uvicorn jinja2 python-dotenv
```

### 📁 Структура файлов после выполнения:

```
chapter-18-results/
├── weather_data_20250904_160000.csv
├── currency_trends.png
├── comprehensive_api_analysis.png
├── api_analysis_report.txt
├── api_data.db
├── templates/
│   └── dashboard.html
└── .env (с вашими API ключами)
```

### ❓ Часто задаваемые вопросы:

**Q: Где получить API ключи?**
A: OpenWeatherMap (бесплатно 1000 запросов/день), ExchangeRate-API (бесплатно), JSONPlaceholder (без ключей)

**Q: Задание 5 не запускается?**  
A: Проверьте установку FastAPI и Uvicorn, создайте папку templates/

**Q: База данных не создается?**
A: Убедитесь, что у вас есть права на запись в текущую папку

---

- 🔙 [Предыдущая глава: Глава 17 - Классификация и регрессия в машинном обучении](../chapter-17/README.md)
- 🔜 [Следующая глава: Глава 19 - SQL: основные запросы, агрегаты, GROUP BY](../chapter-19/README.md)

---

- 📢 Присоединяйтесь к чату курса: https://t.me/analytics_course_chat
- 📢 Канал курса: https://t.me/analytics_course_channel