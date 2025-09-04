# 🔗 Глава 18: Работа с API — получение и автоматизация данных!

## 🎯 Что вы изучите

После изучения этой главы вы сможете:

* **🌐 Работать с REST API** для получения данных из внешних источников
* **🔐 Настраивать аутентификацию** и безопасно работать с API ключами  
* **🐍 Использовать Python** для автоматического получения данных через API
* **🔄 Автоматизировать процессы** сбора данных по расписанию
* **💾 Интегрировать API с SQL** для сохранения данных в базах
* **📊 Применять API в бизнесе** для создания актуальных дашбордов и отчетов

## 🌟 API простыми словами

**API (Application Programming Interface)** — это как "официант" между вашей программой и чужим сервисом. Представьте ресторан:

### 🍽️ Метафора ресторана:
* **👥 Вы** — аналитик, которому нужны данные
* **🍳 Кухня** — сервис с данными (Instagram, валютный сайт, погодный сервис)  
* **👨‍🍳 Повар** — база данных сервиса
* **🧾 Меню** — документация API (что можно заказать)
* **👨‍🍳 Официант** — само API (принимает ваш заказ, приносит данные)
* **💰 Чек** — API ключ (подтверждение, что вы можете заказывать)

Вы не можете зайти на кухню и взять данные сами — нужно заказать через официанта (API) по меню (документации).

### 💼 Зачем аналитику нужны API в 2025:

**Актуальные данные:**
```python
# Вместо ручного копирования каждый день
# Автоматически получаем свежие данные
current_exchange_rate = api.get_exchange_rate("USD", "RUB")
```

**Интеграция систем:**
```python
# Связываем разные платформы
crm_clients = salesforce_api.get_clients()
marketing_data = facebook_api.get_campaigns()
financial_data = accounting_api.get_revenue()
```

**Автоматизация отчетов:**
```python
# Дашборд обновляется сам каждое утро
def morning_report():
    weather = weather_api.get_forecast()
    sales = crm_api.get_yesterday_sales()  
    send_report_to_manager(weather, sales)
```

## 📚 Основы работы с API

### 🌐 Что такое REST API

**REST** (Representational State Transfer) — самый популярный стандарт API, работающий через HTTP запросы.

#### 🔤 Основные HTTP методы:
* **GET** — получить данные (как спросить "что у вас есть?")
* **POST** — отправить новые данные (как сделать заказ)
* **PUT** — обновить данные (как изменить заказ)
* **DELETE** — удалить данные (как отменить заказ)

#### 📋 Анатомия API запроса:

```python
import requests

# Структура запроса
response = requests.get(
    url="https://api.example.com/v1/users",    # Адрес API
    headers={                                   # Заголовки
        "Authorization": "Bearer your-token",
        "Content-Type": "application/json"
    },
    params={                                    # Параметры запроса  
        "page": 1,
        "limit": 100,
        "filter": "active"
    }
)

# Проверка успешности
if response.status_code == 200:
    data = response.json()  # Получаем данные
    print("✅ Данные получены успешно!")
else:
    print(f"❌ Ошибка: {response.status_code}")
```

### 🔐 Аутентификация и безопасность

#### 🗝️ Типы аутентификации:

**1. API Key (самый простой):**
```python
headers = {"X-API-Key": "your-secret-key"}
response = requests.get(url, headers=headers)
```

**2. Bearer Token (OAuth):**
```python
headers = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIs..."}
response = requests.get(url, headers=headers)
```

**3. Basic Authentication:**
```python
from requests.auth import HTTPBasicAuth
response = requests.get(url, auth=HTTPBasicAuth('username', 'password'))
```

#### 🛡️ Безопасность API ключей:

**❌ Неправильно — ключ в коде:**
```python
# НИКОГДА НЕ ДЕЛАЙТЕ ТАК!
api_key = "sk-1234567890abcdef"  # Все увидят ваш ключ
```

**✅ Правильно — ключ в переменных окружения:**
```python
import os
from dotenv import load_dotenv

load_dotenv()  # Загружаем .env файл
api_key = os.getenv('API_KEY')  # Безопасно получаем ключ

if not api_key:
    raise ValueError("❌ API ключ не найден в переменных окружения!")
```

**.env файл (НЕ коммитим в Git!):**
```
API_KEY=sk-1234567890abcdef
DATABASE_URL=postgresql://user:pass@localhost:5432/db
WEATHER_API_KEY=your-weather-key
```

### 🔧 Python библиотеки для работы с API

#### 📦 Основные библиотеки:

**requests — основа всего:**
```python
import requests
import json

# GET запрос
response = requests.get('https://api.github.com/users/octocat')
user_data = response.json()

# POST запрос с данными
payload = {"name": "John", "email": "john@example.com"}
response = requests.post('https://api.example.com/users', json=payload)
```

**requests-cache — кеширование запросов:**
```python
import requests_cache

# Кешируем запросы на 1 час (экономим API лимиты)
session = requests_cache.CachedSession(expire_after=3600)
response = session.get('https://api.expensive-service.com/data')
```

**httpx — асинхронные запросы:**
```python
import httpx
import asyncio

async def get_multiple_apis():
    async with httpx.AsyncClient() as client:
        tasks = [
            client.get('https://api.service1.com/data'),
            client.get('https://api.service2.com/data'),
            client.get('https://api.service3.com/data')
        ]
        responses = await asyncio.gather(*tasks)
    return [r.json() for r in responses]

# Получаем данные из 3 API одновременно!
```

#### 🔍 Обработка ответов API:

```python
def safe_api_request(url, max_retries=3):
    """Безопасный API запрос с повторными попытками"""
    
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=10)
            
            # Проверяем статус код
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 429:  # Rate limit
                wait_time = int(response.headers.get('Retry-After', 60))
                print(f"⏳ Превышен лимит. Ждем {wait_time} секунд...")
                time.sleep(wait_time)
                continue
            elif response.status_code == 401:
                raise ValueError("🔐 Ошибка аутентификации. Проверьте API ключ")
            elif response.status_code == 404:
                raise ValueError("🔍 Данные не найдены")
            else:
                print(f"⚠️ Неожиданный статус: {response.status_code}")
                
        except requests.exceptions.Timeout:
            print(f"⏰ Таймаут на попытке {attempt + 1}")
        except requests.exceptions.RequestException as e:
            print(f"🌐 Ошибка сети: {e}")
            
        if attempt < max_retries - 1:
            time.sleep(2 ** attempt)  # Экспоненциальная задержка
    
    raise Exception(f"❌ Не удалось получить данные после {max_retries} попыток")
```

### 📊 Популярные API для аналитики

#### 🌤️ OpenWeatherMap API (погода):

```python
import requests
import pandas as pd

def get_weather_data(city, api_key):
    """Получаем данные о погоде для анализа"""
    
    url = f"http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric',  # Цельсии
        'lang': 'ru'        # Русский язык
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        return {
            'city': data['name'],
            'temperature': data['main']['temp'],
            'humidity': data['main']['humidity'],
            'pressure': data['main']['pressure'],
            'description': data['weather'][0]['description'],
            'wind_speed': data['wind']['speed'],
            'timestamp': pd.Timestamp.now()
        }
    else:
        raise Exception(f"Ошибка API: {response.status_code}")

# Пример использования
weather = get_weather_data("Москва", "your-api-key")
print(f"🌡️ В Москве {weather['temperature']}°C, {weather['description']}")
```

#### 💱 Exchange Rates API (валютные курсы):

```python
def get_currency_rates(base_currency="USD"):
    """Получаем актуальные курсы валют"""
    
    url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Бросает исключение при ошибке
        
        data = response.json()
        
        # Создаем DataFrame для удобного анализа
        rates_df = pd.DataFrame([
            {'currency': currency, 'rate': rate, 'date': data['date']}
            for currency, rate in data['rates'].items()
        ])
        
        return rates_df
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка получения курсов валют: {e}")
        return None

# Анализ курсов
rates = get_currency_rates("USD")
print("💰 Топ-5 самых дорогих валют к доллару:")
print(rates.nlargest(5, 'rate')[['currency', 'rate']])
```

#### 📊 JSONPlaceholder API (тестовые данные):

```python
def get_user_posts_analysis():
    """Анализируем активность пользователей через API"""
    
    # Получаем пользователей и их посты
    users = requests.get('https://jsonplaceholder.typicode.com/users').json()
    posts = requests.get('https://jsonplaceholder.typicode.com/posts').json()
    
    # Преобразуем в DataFrame
    users_df = pd.DataFrame(users)
    posts_df = pd.DataFrame(posts)
    
    # Анализируем активность
    activity = posts_df.groupby('userId').agg({
        'id': 'count',
        'title': lambda x: x.str.len().mean(),
        'body': lambda x: x.str.len().mean()
    }).round(2)
    
    activity.columns = ['posts_count', 'avg_title_length', 'avg_body_length']
    
    # Объединяем с данными пользователей
    result = users_df[['id', 'name', 'email', 'company']].merge(
        activity, left_on='id', right_index=True
    )
    
    return result.sort_values('posts_count', ascending=False)

# Анализ активности пользователей
activity_report = get_user_posts_analysis()
print("📈 Самые активные пользователи:")
print(activity_report.head())
```

### 🔄 Автоматизация получения данных

#### ⏰ Планировщик задач с schedule:

```python
import schedule
import time
from datetime import datetime

def daily_data_collection():
    """Ежедневный сбор данных из API"""
    
    print(f"🔄 Начинаем сбор данных: {datetime.now()}")
    
    try:
        # Получаем данные из разных источников
        weather_data = get_weather_data("Москва", os.getenv('WEATHER_API_KEY'))
        currency_data = get_currency_rates("USD")
        
        # Сохраняем в базу данных
        save_to_database(weather_data, 'weather_daily')
        save_to_database(currency_data, 'currency_rates')
        
        print("✅ Данные успешно собраны и сохранены!")
        
    except Exception as e:
        print(f"❌ Ошибка сбора данных: {e}")
        send_alert_email(f"Ошибка в daily_data_collection: {e}")

# Настраиваем расписание
schedule.every().day.at("09:00").do(daily_data_collection)
schedule.every().hour.do(lambda: get_weather_data("Москва", api_key))
schedule.every(30).minutes.do(lambda: get_currency_rates("USD"))

# Запускаем планировщик
print("🚀 Планировщик запущен!")
while True:
    schedule.run_pending()
    time.sleep(60)  # Проверяем каждую минуту
```

#### 🏗️ Продвинутая автоматизация с классами:

```python
class APIDataCollector:
    """Универсальный сборщик данных из API"""
    
    def __init__(self, name, base_url, api_key=None):
        self.name = name
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.session = requests.Session()
        
        # Настройка сессии
        if api_key:
            self.session.headers.update({'Authorization': f'Bearer {api_key}'})
        
        self.session.headers.update({
            'User-Agent': 'DataAnalyticsBot/1.0',
            'Accept': 'application/json'
        })
        
    def get_data(self, endpoint, params=None, max_retries=3):
        """Получение данных с автоматическими повторами"""
        
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        for attempt in range(max_retries):
            try:
                response = self.session.get(url, params=params, timeout=30)
                
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 429:
                    wait_time = int(response.headers.get('Retry-After', 60))
                    print(f"⏳ Rate limit. Waiting {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    response.raise_for_status()
                    
            except requests.exceptions.RequestException as e:
                if attempt == max_retries - 1:
                    raise
                print(f"⚠️ Attempt {attempt + 1} failed: {e}")
                time.sleep(2 ** attempt)
    
    def collect_and_save(self, endpoint, table_name, params=None):
        """Получение данных и сохранение в БД"""
        
        try:
            data = self.get_data(endpoint, params)
            
            # Преобразуем в DataFrame
            if isinstance(data, list):
                df = pd.DataFrame(data)
            else:
                df = pd.DataFrame([data])
                
            # Добавляем метаданные
            df['collected_at'] = pd.Timestamp.now()
            df['source'] = self.name
            
            # Сохраняем в базу
            save_to_database(df, table_name)
            
            print(f"✅ {self.name}: {len(df)} записей сохранено в {table_name}")
            return df
            
        except Exception as e:
            print(f"❌ {self.name} error: {e}")
            raise

# Использование класса
weather_collector = APIDataCollector(
    name="OpenWeather",
    base_url="http://api.openweathermap.org/data/2.5",
    api_key=os.getenv('WEATHER_API_KEY')
)

# Автоматический сбор данных по городам
cities = ["Moscow", "Saint Petersburg", "Novosibirsk"]
for city in cities:
    weather_collector.collect_and_save(
        endpoint="weather",
        table_name="weather_data",
        params={"q": city, "units": "metric", "lang": "ru"}
    )
```

### 💾 Интеграция API с SQL базами данных

#### 🗄️ Сохранение API данных в PostgreSQL:

```python
import psycopg2
from sqlalchemy import create_engine
import pandas as pd

def setup_database_connection():
    """Настройка подключения к базе данных"""
    
    connection_string = os.getenv('DATABASE_URL', 
        'postgresql://username:password@localhost:5432/analytics_db')
    
    engine = create_engine(connection_string)
    return engine

def save_to_database(dataframe, table_name, if_exists='append'):
    """Сохранение DataFrame в базу данных"""
    
    engine = setup_database_connection()
    
    try:
        # Сохраняем данные
        dataframe.to_sql(
            name=table_name,
            con=engine,
            if_exists=if_exists,  # 'append', 'replace', 'fail'
            index=False,
            method='multi'  # Быстрая вставка
        )
        
        print(f"💾 Сохранено {len(dataframe)} записей в таблицу {table_name}")
        
    except Exception as e:
        print(f"❌ Ошибка сохранения в БД: {e}")
        raise
    finally:
        engine.dispose()

def create_api_data_tables():
    """Создание таблиц для хранения API данных"""
    
    engine = setup_database_connection()
    
    # SQL для создания таблиц
    tables_sql = """
    -- Таблица для погодных данных
    CREATE TABLE IF NOT EXISTS weather_data (
        id SERIAL PRIMARY KEY,
        city VARCHAR(100) NOT NULL,
        temperature DECIMAL(5,2),
        humidity INTEGER,
        pressure DECIMAL(7,2),
        description TEXT,
        wind_speed DECIMAL(5,2),
        collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        source VARCHAR(50)
    );
    
    -- Таблица для валютных курсов
    CREATE TABLE IF NOT EXISTS currency_rates (
        id SERIAL PRIMARY KEY,
        currency VARCHAR(10) NOT NULL,
        rate DECIMAL(15,6) NOT NULL,
        base_currency VARCHAR(10) DEFAULT 'USD',
        rate_date DATE,
        collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        source VARCHAR(50)
    );
    
    -- Индексы для быстрого поиска
    CREATE INDEX IF NOT EXISTS idx_weather_city_date 
    ON weather_data(city, collected_at);
    
    CREATE INDEX IF NOT EXISTS idx_currency_date 
    ON currency_rates(currency, rate_date);
    """
    
    try:
        with engine.connect() as connection:
            connection.execute(tables_sql)
            print("✅ Таблицы для API данных созданы")
            
    except Exception as e:
        print(f"❌ Ошибка создания таблиц: {e}")
    finally:
        engine.dispose()

# Пример полного цикла: API → Обработка → БД → Анализ
def complete_api_workflow():
    """Полный цикл работы с API данными"""
    
    # 1. Создаем таблицы
    create_api_data_tables()
    
    # 2. Получаем данные из API
    weather_data = get_weather_data("Москва", os.getenv('WEATHER_API_KEY'))
    currency_data = get_currency_rates("USD")
    
    # 3. Обрабатываем и сохраняем
    weather_df = pd.DataFrame([weather_data])
    save_to_database(weather_df, 'weather_data')
    save_to_database(currency_data, 'currency_rates')
    
    # 4. Анализируем сохраненные данные
    engine = setup_database_connection()
    
    analysis_query = """
    SELECT 
        city,
        AVG(temperature) as avg_temp,
        AVG(humidity) as avg_humidity,
        COUNT(*) as measurements_count,
        MAX(collected_at) as last_update
    FROM weather_data 
    WHERE collected_at >= CURRENT_DATE - INTERVAL '7 days'
    GROUP BY city
    ORDER BY avg_temp DESC;
    """
    
    analysis_result = pd.read_sql(analysis_query, engine)
    print("📊 Анализ погодных данных за неделю:")
    print(analysis_result)
    
    engine.dispose()
    return analysis_result
```

### 🏢 Бизнес-применения API

#### 📈 Создание актуального дашборда продаж:

```python
def create_sales_dashboard():
    """Создание дашборда с актуальными данными из CRM API"""
    
    # Получаем данные из разных API
    crm_data = get_crm_sales_data()  # Продажи из CRM
    weather_data = get_weather_data("Москва", weather_api_key)  # Погода
    currency_data = get_currency_rates("USD")  # Валютные курсы
    
    # Создаем сводную таблицу для дашборда
    dashboard_data = {
        'update_time': datetime.now(),
        'total_sales_today': crm_data['today_sales'],
        'sales_vs_yesterday': crm_data['sales_change_pct'],
        'weather_impact': calculate_weather_impact(weather_data, crm_data),
        'usd_rub_rate': currency_data[currency_data['currency'] == 'RUB']['rate'].iloc[0],
        'top_products': crm_data['top_products'][:5]
    }
    
    # Сохраняем для Power BI или другого BI инструмента
    dashboard_df = pd.DataFrame([dashboard_data])
    save_to_database(dashboard_df, 'daily_dashboard')
    
    return dashboard_data

def calculate_weather_impact(weather_data, sales_data):
    """Анализируем влияние погоды на продажи"""
    
    # Простая логика: плохая погода = больше онлайн продаж
    temp = weather_data['temperature']
    
    if temp < 0:
        return "Холод: +15% онлайн продаж"
    elif temp > 25:
        return "Жара: +10% напитков"
    elif 'дождь' in weather_data['description'].lower():
        return "Дождь: +20% доставки"
    else:
        return "Нормальная погода"
```

#### 🔔 Система мониторинга и алертов:

```python
def monitoring_system():
    """Система мониторинга важных показателей через API"""
    
    alerts = []
    
    try:
        # Проверяем курс доллара
        rates = get_currency_rates("USD")
        rub_rate = rates[rates['currency'] == 'RUB']['rate'].iloc[0]
        
        if rub_rate > 100:  # Доллар выше 100 рублей
            alerts.append(f"🚨 Курс доллара: {rub_rate:.2f} руб - критично высокий!")
        
        # Проверяем погоду
        weather = get_weather_data("Москва", os.getenv('WEATHER_API_KEY'))
        if weather['temperature'] < -20:
            alerts.append(f"🥶 Экстремальный холод в Москве: {weather['temperature']}°C")
        
        # Проверяем продажи (условно)
        # sales = get_sales_from_crm_api()
        # if sales['today'] < sales['yesterday'] * 0.7:  # Падение продаж на 30%
        #     alerts.append("📉 Критическое падение продаж!")
        
        # Отправляем алерты если есть
        if alerts:
            send_telegram_alert("\n".join(alerts))
            send_email_alert(alerts)
            
        print(f"✅ Мониторинг завершен. Алертов: {len(alerts)}")
        
    except Exception as e:
        send_telegram_alert(f"❌ Ошибка системы мониторинга: {e}")

def send_telegram_alert(message):
    """Отправка уведомлений в Telegram через Bot API"""
    
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    
    if bot_token and chat_id:
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        
        payload = {
            'chat_id': chat_id,
            'text': message,
            'parse_mode': 'HTML'
        }
        
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                print("📱 Уведомление отправлено в Telegram")
            else:
                print(f"❌ Ошибка отправки в Telegram: {response.status_code}")
        except Exception as e:
            print(f"❌ Ошибка Telegram API: {e}")
```

### ⚠️ Обработка ошибок и лимитов API

#### 🚦 Rate Limiting и управление лимитами:

```python
import time
from functools import wraps

def rate_limit(max_calls_per_minute=60):
    """Декоратор для ограничения частоты API вызовов"""
    
    min_interval = 60.0 / max_calls_per_minute
    last_called = [0.0]
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            left_to_wait = min_interval - elapsed
            
            if left_to_wait > 0:
                time.sleep(left_to_wait)
            
            ret = func(*args, **kwargs)
            last_called[0] = time.time()
            return ret
        return wrapper
    return decorator

class APIRateLimiter:
    """Умное управление лимитами API"""
    
    def __init__(self, max_requests_per_minute=60):
        self.max_requests = max_requests_per_minute
        self.requests = []
        
    def wait_if_needed(self):
        now = time.time()
        
        # Удаляем старые запросы (старше минуты)
        self.requests = [req_time for req_time in self.requests 
                        if now - req_time < 60]
        
        # Если достигли лимита, ждем
        if len(self.requests) >= self.max_requests:
            sleep_time = 60 - (now - self.requests[0]) + 1
            print(f"⏳ Достигнут лимит API. Ждем {sleep_time:.1f} сек...")
            time.sleep(sleep_time)
            
        # Записываем текущий запрос
        self.requests.append(now)

# Использование rate limiter
limiter = APIRateLimiter(max_requests_per_minute=100)

@rate_limit(max_calls_per_minute=50)
def get_limited_api_data(endpoint):
    """API запрос с автоматическим лимитированием"""
    limiter.wait_if_needed()
    return requests.get(endpoint)
```

#### 🔧 Универсальный обработчик ошибок:

```python
def robust_api_call(api_function, *args, max_retries=3, backoff_factor=1, **kwargs):
    """Универсальная функция для надежных API вызовов"""
    
    last_exception = None
    
    for attempt in range(max_retries):
        try:
            result = api_function(*args, **kwargs)
            
            # Логируем успешный запрос
            print(f"✅ API вызов успешен с {attempt + 1} попытки")
            return result
            
        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code
            
            if status_code == 401:
                print("🔐 Ошибка авторизации - проверьте API ключ")
                break  # Не повторяем при ошибке авторизации
            elif status_code == 404:
                print("🔍 Ресурс не найден")
                break  # Не повторяем для 404
            elif status_code == 429:
                retry_after = int(e.response.headers.get('Retry-After', 60))
                print(f"⏳ Rate limit. Ждем {retry_after} сек...")
                time.sleep(retry_after)
                continue
            elif status_code >= 500:
                print(f"🔧 Ошибка сервера {status_code}. Повтор...")
                last_exception = e
            else:
                print(f"❌ HTTP ошибка {status_code}")
                last_exception = e
                
        except requests.exceptions.Timeout as e:
            print(f"⏰ Таймаут на попытке {attempt + 1}")
            last_exception = e
            
        except requests.exceptions.ConnectionError as e:
            print(f"🌐 Ошибка соединения на попытке {attempt + 1}")
            last_exception = e
            
        except Exception as e:
            print(f"❌ Неизвестная ошибка: {e}")
            last_exception = e
        
        # Экспоненциальная задержка между попытками
        if attempt < max_retries - 1:
            sleep_time = backoff_factor * (2 ** attempt)
            print(f"⏸️ Ждем {sleep_time} сек перед следующей попыткой...")
            time.sleep(sleep_time)
    
    # Если все попытки неудачны
    raise Exception(f"❌ API вызов неудачен после {max_retries} попыток. "
                   f"Последняя ошибка: {last_exception}")

# Пример использования
def safe_weather_request(city):
    return robust_api_call(
        get_weather_data, 
        city, 
        os.getenv('WEATHER_API_KEY'),
        max_retries=5,
        backoff_factor=2
    )
```

### 🧪 Тестирование API интеграций

#### 🔬 Юнит-тесты для API функций:

```python
import unittest
from unittest.mock import Mock, patch
import json

class TestAPIFunctions(unittest.TestCase):
    """Тесты для функций работы с API"""
    
    def setUp(self):
        """Подготовка тестовых данных"""
        self.sample_weather_response = {
            'name': 'Moscow',
            'main': {'temp': 15.5, 'humidity': 65, 'pressure': 1013},
            'weather': [{'description': 'ясно'}],
            'wind': {'speed': 3.2}
        }
        
    @patch('requests.get')
    def test_get_weather_data_success(self, mock_get):
        """Тест успешного получения погодных данных"""
        
        # Настраиваем mock
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = self.sample_weather_response
        mock_get.return_value = mock_response
        
        # Тестируем функцию
        result = get_weather_data("Moscow", "test-api-key")
        
        # Проверяем результат
        self.assertEqual(result['city'], 'Moscow')
        self.assertEqual(result['temperature'], 15.5)
        self.assertIsNotNone(result['timestamp'])
        
        # Проверяем, что запрос был сделан правильно
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        self.assertIn('q=Moscow', str(kwargs.get('params', '')))
        
    @patch('requests.get')
    def test_get_weather_data_api_error(self, mock_get):
        """Тест обработки ошибки API"""
        
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        
        # Проверяем, что выбрасывается исключение
        with self.assertRaises(Exception) as context:
            get_weather_data("NonexistentCity", "test-api-key")
        
        self.assertIn("404", str(context.exception))

# Запуск тестов
if __name__ == '__main__':
    unittest.main()
```

### 📊 Готовые шаблоны для копирования

#### 🚀 Универсальный API клиент:

```python
class UniversalAPIClient:
    """Универсальный клиент для работы с любыми REST API"""
    
    def __init__(self, base_url, api_key=None, auth_type='bearer'):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.session = requests.Session()
        
        # Настраиваем аутентификацию
        if api_key:
            if auth_type == 'bearer':
                self.session.headers['Authorization'] = f'Bearer {api_key}'
            elif auth_type == 'api_key':
                self.session.headers['X-API-Key'] = api_key
            elif auth_type == 'query':
                self.default_params = {'api_key': api_key}
        
        self.session.headers.update({
            'User-Agent': 'Python-Analytics-Client/1.0',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        })
        
        self.rate_limiter = APIRateLimiter(max_requests_per_minute=60)
        
    def request(self, method, endpoint, params=None, data=None, **kwargs):
        """Универсальный метод для API запросов"""
        
        self.rate_limiter.wait_if_needed()
        
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        # Добавляем API ключ в параметры если нужно
        if hasattr(self, 'default_params'):
            params = {**(params or {}), **self.default_params}
        
        return robust_api_call(
            self.session.request,
            method, url,
            params=params,
            json=data,
            **kwargs
        )
    
    def get(self, endpoint, params=None, **kwargs):
        return self.request('GET', endpoint, params=params, **kwargs)
    
    def post(self, endpoint, data=None, **kwargs):
        return self.request('POST', endpoint, data=data, **kwargs)
    
    def put(self, endpoint, data=None, **kwargs):
        return self.request('PUT', endpoint, data=data, **kwargs)
    
    def delete(self, endpoint, **kwargs):
        return self.request('DELETE', endpoint, **kwargs)

# Использование универсального клиента
weather_client = UniversalAPIClient(
    base_url="http://api.openweathermap.org/data/2.5",
    api_key=os.getenv('WEATHER_API_KEY'),
    auth_type='query'
)

weather_data = weather_client.get('weather', params={'q': 'Moscow', 'units': 'metric'})
```

#### 📋 Готовый скрипт для ежедневного сбора данных:

```python
#!/usr/bin/env python3
"""
Скрипт для ежедневного автоматического сбора данных из API
Использование: python daily_api_collection.py
"""

import os
import sys
import logging
from datetime import datetime
import pandas as pd

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('api_collection.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

def main():
    """Главная функция сбора данных"""
    
    logger.info("🚀 Начинаем ежедневный сбор данных из API")
    
    collected_data = {}
    errors = []
    
    try:
        # 1. Погодные данные
        logger.info("🌤️ Собираем данные о погоде...")
        weather_data = collect_weather_data()
        collected_data['weather'] = weather_data
        logger.info(f"✅ Погода: {len(weather_data)} записей")
        
    except Exception as e:
        error_msg = f"❌ Ошибка сбора погодных данных: {e}"
        logger.error(error_msg)
        errors.append(error_msg)
    
    try:
        # 2. Валютные курсы
        logger.info("💱 Собираем валютные курсы...")
        currency_data = collect_currency_data()
        collected_data['currency'] = currency_data
        logger.info(f"✅ Валюты: {len(currency_data)} записей")
        
    except Exception as e:
        error_msg = f"❌ Ошибка сбора валютных данных: {e}"
        logger.error(error_msg)
        errors.append(error_msg)
    
    # 3. Сохранение данных
    if collected_data:
        try:
            save_collected_data(collected_data)
            logger.info("💾 Данные успешно сохранены в базу")
        except Exception as e:
            error_msg = f"❌ Ошибка сохранения данных: {e}"
            logger.error(error_msg)
            errors.append(error_msg)
    
    # 4. Отчет о результатах
    if errors:
        logger.warning(f"⚠️ Сбор завершен с {len(errors)} ошибками")
        send_error_notification(errors)
    else:
        logger.info("🎉 Сбор данных завершен успешно!")
    
    return len(errors) == 0

def collect_weather_data():
    """Сбор данных о погоде для основных городов"""
    
    cities = ["Moscow", "Saint Petersburg", "Novosibirsk", "Yekaterinburg"]
    weather_data = []
    
    for city in cities:
        try:
            data = get_weather_data(city, os.getenv('WEATHER_API_KEY'))
            weather_data.append(data)
            time.sleep(1)  # Пауза между запросами
            
        except Exception as e:
            logger.warning(f"⚠️ Не удалось получить погоду для {city}: {e}")
    
    return weather_data

def collect_currency_data():
    """Сбор данных о валютных курсах"""
    
    rates = get_currency_rates("USD")
    
    # Оставляем только основные валюты
    important_currencies = ['RUB', 'EUR', 'GBP', 'JPY', 'CNY']
    filtered_rates = rates[rates['currency'].isin(important_currencies)]
    
    return filtered_rates.to_dict('records')

def save_collected_data(data):
    """Сохранение собранных данных в базу"""
    
    engine = setup_database_connection()
    
    # Сохраняем каждый тип данных в свою таблицу
    for data_type, records in data.items():
        if records:
            df = pd.DataFrame(records)
            df['collection_date'] = datetime.now().date()
            
            save_to_database(df, f'{data_type}_daily')
            logger.info(f"💾 {data_type}: {len(df)} записей сохранено")

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
```

## 🛠 Инструкции

Теперь переходите к практическим заданиям и изучите работу с реальными API:

- 📝 [Перейти к практическим заданиям](practice.md)
- ✅ [Перейти к чек-листу](checklist.md)
- 📁 [Посмотреть учебные файлы](files/README.md)

---

- 🔙 [Предыдущая глава: Глава 17 - Классификация и регрессия в машинном обучении](../chapter-17/README.md)
- 🔜 [Следующая глава: Глава 19 - SQL: основные запросы, агрегаты, GROUP BY](../chapter-19/README.md)

---

- 📢 Присоединяйтесь к чату курса: https://t.me/analytics_course_chat
- 📢 Канал курса: https://t.me/analytics_course_channel