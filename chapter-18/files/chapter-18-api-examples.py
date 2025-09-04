#!/usr/bin/env python3
"""
🔗 Готовые примеры работы с популярными API

Этот файл содержит готовые функции и классы для работы с различными API.
Используйте эти примеры как шаблоны для ваших проектов.

Требуемые библиотеки:
pip install requests pandas python-dotenv

Автор: Analytics Course (github.com/lazuale/analytics-course)
Глава: 18 - Работа с API
"""

import requests
import pandas as pd
import json
import time
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from typing import Dict, List, Optional, Any

# Загружаем переменные окружения
load_dotenv()

print("🚀 API Examples для главы 18")
print("=" * 50)

# ========================================
# 🌤️ РАБОТА С OPENWEATHERMAP API
# ========================================

class WeatherAPI:
    """Класс для работы с OpenWeatherMap API"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "http://api.openweathermap.org/data/2.5"
        
    def get_current_weather(self, city: str, units: str = "metric") -> Dict:
        """
        Получение текущей погоды для города
        
        Args:
            city: Название города (например, "Moscow" или "London")
            units: Единицы измерения ("metric", "imperial", "kelvin")
        
        Returns:
            Словарь с данными о погоде
        """
        
        url = f"{self.base_url}/weather"
        params = {
            'q': city,
            'appid': self.api_key,
            'units': units,
            'lang': 'ru'  # Описания на русском языке
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()  # Вызовет исключение при HTTP ошибке
            
            data = response.json()
            
            # Извлекаем и структурируем данные
            weather_data = {
                'city': data['name'],
                'country': data['sys']['country'],
                'temperature': round(data['main']['temp'], 1),
                'feels_like': round(data['main']['feels_like'], 1),
                'humidity': data['main']['humidity'],
                'pressure': data['main']['pressure'],
                'description': data['weather'][0]['description'],
                'main': data['weather'][0]['main'],
                'wind_speed': data.get('wind', {}).get('speed', 0),
                'wind_direction': data.get('wind', {}).get('deg', 0),
                'cloudiness': data['clouds']['all'],
                'visibility': data.get('visibility', 0) / 1000,  # км
                'sunrise': datetime.fromtimestamp(data['sys']['sunrise']),
                'sunset': datetime.fromtimestamp(data['sys']['sunset']),
                'collected_at': datetime.now()
            }
            
            return weather_data
            
        except requests.exceptions.HTTPError as e:
            if response.status_code == 401:
                raise ValueError("🔐 Неверный API ключ OpenWeatherMap")
            elif response.status_code == 404:
                raise ValueError(f"🔍 Город '{city}' не найден")
            else:
                raise ValueError(f"❌ HTTP ошибка: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            raise ValueError(f"🌐 Ошибка сети: {e}")
    
    def get_multiple_cities(self, cities: List[str]) -> pd.DataFrame:
        """
        Получение погоды для нескольких городов
        
        Args:
            cities: Список названий городов
            
        Returns:
            DataFrame с погодными данными
        """
        
        weather_data = []
        
        for city in cities:
            try:
                data = self.get_current_weather(city)
                weather_data.append(data)
                print(f"✅ {city}: {data['temperature']}°C, {data['description']}")
                time.sleep(1)  # Пауза между запросами
                
            except Exception as e:
                print(f"❌ Ошибка для {city}: {e}")
                # Добавляем пустую запись с ошибкой
                weather_data.append({
                    'city': city,
                    'error': str(e),
                    'collected_at': datetime.now()
                })
        
        return pd.DataFrame(weather_data)

# ========================================
# 💱 РАБОТА С ВАЛЮТНЫМИ API
# ========================================

class CurrencyAPI:
    """Класс для работы с валютными курсами"""
    
    def __init__(self):
        self.base_url = "https://api.exchangerate-api.com/v4/latest"
        
    def get_exchange_rates(self, base_currency: str = "USD") -> Dict:
        """
        Получение текущих курсов валют
        
        Args:
            base_currency: Базовая валюта (USD, EUR, RUB и т.д.)
            
        Returns:
            Словарь с курсами валют
        """
        
        url = f"{self.base_url}/{base_currency}"
        
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            return {
                'base': data['base'],
                'date': data['date'],
                'rates': data['rates'],
                'collected_at': datetime.now()
            }
            
        except requests.exceptions.RequestException as e:
            raise ValueError(f"❌ Ошибка получения курсов валют: {e}")
    
    def get_specific_rates(self, base: str, target_currencies: List[str]) -> pd.DataFrame:
        """
        Получение курсов для определенных валют
        
        Args:
            base: Базовая валюта
            target_currencies: Список целевых валют
            
        Returns:
            DataFrame с курсами
        """
        
        rates_data = self.get_exchange_rates(base)
        
        filtered_rates = []
        for currency in target_currencies:
            if currency in rates_data['rates']:
                filtered_rates.append({
                    'currency': currency,
                    'rate': rates_data['rates'][currency],
                    'base': rates_data['base'],
                    'date': rates_data['date'],
                    'collected_at': rates_data['collected_at']
                })
            else:
                print(f"⚠️ Валюта {currency} не найдена")
        
        return pd.DataFrame(filtered_rates)
    
    def calculate_conversion(self, amount: float, from_currency: str, 
                           to_currency: str) -> Dict:
        """
        Конвертация валют
        
        Args:
            amount: Сумма для конвертации
            from_currency: Исходная валюта
            to_currency: Целевая валюта
            
        Returns:
            Словарь с результатом конвертации
        """
        
        rates = self.get_exchange_rates(from_currency)
        
        if to_currency not in rates['rates']:
            raise ValueError(f"Валюта {to_currency} не поддерживается")
        
        converted_amount = amount * rates['rates'][to_currency]
        
        return {
            'original_amount': amount,
            'original_currency': from_currency,
            'converted_amount': round(converted_amount, 2),
            'target_currency': to_currency,
            'exchange_rate': rates['rates'][to_currency],
            'conversion_date': rates['date']
        }

# ========================================
# 👥 РАБОТА С JSONPLACEHOLDER API
# ========================================

class JSONPlaceholderAPI:
    """Класс для работы с JSONPlaceholder API (тестовые данные)"""
    
    def __init__(self):
        self.base_url = "https://jsonplaceholder.typicode.com"
    
    def get_users(self) -> pd.DataFrame:
        """Получение списка пользователей"""
        
        url = f"{self.base_url}/users"
        
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            users_data = response.json()
            
            # Извлекаем основные поля
            processed_users = []
            for user in users_data:
                processed_users.append({
                    'id': user['id'],
                    'name': user['name'],
                    'username': user['username'],
                    'email': user['email'],
                    'city': user['address']['city'],
                    'zipcode': user['address']['zipcode'],
                    'lat': float(user['address']['geo']['lat']),
                    'lng': float(user['address']['geo']['lng']),
                    'phone': user['phone'],
                    'website': user['website'],
                    'company_name': user['company']['name']
                })
            
            return pd.DataFrame(processed_users)
            
        except requests.exceptions.RequestException as e:
            raise ValueError(f"❌ Ошибка получения пользователей: {e}")
    
    def get_posts(self) -> pd.DataFrame:
        """Получение списка постов"""
        
        url = f"{self.base_url}/posts"
        
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            posts_data = response.json()
            posts_df = pd.DataFrame(posts_data)
            
            # Добавляем статистики
            posts_df['title_length'] = posts_df['title'].str.len()
            posts_df['body_length'] = posts_df['body'].str.len()
            
            return posts_df
            
        except requests.exceptions.RequestException as e:
            raise ValueError(f"❌ Ошибка получения постов: {e}")
    
    def analyze_user_activity(self) -> pd.DataFrame:
        """Анализ активности пользователей"""
        
        users_df = self.get_users()
        posts_df = self.get_posts()
        
        # Анализ активности по пользователям
        activity_stats = posts_df.groupby('userId').agg({
            'id': 'count',
            'title_length': 'mean',
            'body_length': 'mean'
        }).round(2)
        
        activity_stats.columns = ['posts_count', 'avg_title_length', 'avg_body_length']
        
        # Объединяем с данными пользователей
        result = users_df.merge(
            activity_stats, 
            left_on='id', 
            right_index=True, 
            how='left'
        )
        
        # Заполняем пропуски нулями
        result[['posts_count', 'avg_title_length', 'avg_body_length']] = \
            result[['posts_count', 'avg_title_length', 'avg_body_length']].fillna(0)
        
        return result.sort_values('posts_count', ascending=False)

# ========================================
# 🔧 УНИВЕРСАЛЬНЫЙ API КЛИЕНТ
# ========================================

class UniversalAPIClient:
    """Универсальный клиент для работы с любыми REST API"""
    
    def __init__(self, base_url: str, api_key: Optional[str] = None, 
                 auth_type: str = 'bearer', timeout: int = 30):
        """
        Инициализация клиента
        
        Args:
            base_url: Базовый URL API
            api_key: API ключ для аутентификации
            auth_type: Тип аутентификации ('bearer', 'api_key', 'query')
            timeout: Таймаут запросов в секундах
        """
        
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.timeout = timeout
        
        # Настраиваем сессию
        self.session = requests.Session()
        
        # Настраиваем аутентификацию
        if api_key:
            if auth_type == 'bearer':
                self.session.headers['Authorization'] = f'Bearer {api_key}'
            elif auth_type == 'api_key':
                self.session.headers['X-API-Key'] = api_key
            elif auth_type == 'query':
                self.default_params = {'api_key': api_key}
                
        # Настраиваем общие заголовки
        self.session.headers.update({
            'User-Agent': 'Python-Analytics-Client/1.0',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        })
    
    def make_request(self, method: str, endpoint: str, 
                    params: Optional[Dict] = None, 
                    data: Optional[Dict] = None,
                    max_retries: int = 3) -> Dict:
        """
        Универсальный метод для API запросов с retry логикой
        
        Args:
            method: HTTP метод ('GET', 'POST', 'PUT', 'DELETE')
            endpoint: API endpoint
            params: Параметры запроса
            data: Данные для POST/PUT запросов
            max_retries: Максимальное количество повторов
            
        Returns:
            Словарь с ответом API
        """
        
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        # Добавляем API ключ в параметры если нужно
        if hasattr(self, 'default_params'):
            params = {**(params or {}), **self.default_params}
        
        last_exception = None
        
        for attempt in range(max_retries):
            try:
                response = self.session.request(
                    method=method,
                    url=url,
                    params=params,
                    json=data,
                    timeout=self.timeout
                )
                
                # Обрабатываем статус коды
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 401:
                    raise ValueError("🔐 Ошибка авторизации - проверьте API ключ")
                elif response.status_code == 404:
                    raise ValueError("🔍 Ресурс не найден")
                elif response.status_code == 429:
                    retry_after = int(response.headers.get('Retry-After', 60))
                    if attempt < max_retries - 1:
                        print(f"⏳ Rate limit. Ждем {retry_after} сек...")
                        time.sleep(retry_after)
                        continue
                    else:
                        raise ValueError("🚫 Превышен лимит запросов API")
                elif response.status_code >= 500:
                    if attempt < max_retries - 1:
                        wait_time = 2 ** attempt  # Экспоненциальная задержка
                        print(f"🔧 Ошибка сервера. Ждем {wait_time} сек...")
                        time.sleep(wait_time)
                        continue
                    else:
                        raise ValueError(f"🔥 Ошибка сервера: {response.status_code}")
                else:
                    response.raise_for_status()
                    
            except requests.exceptions.Timeout:
                last_exception = f"⏰ Таймаут запроса (>{self.timeout}s)"
                if attempt < max_retries - 1:
                    print(f"{last_exception}. Повтор...")
                    time.sleep(2)
                    
            except requests.exceptions.RequestException as e:
                last_exception = f"🌐 Ошибка сети: {e}"
                if attempt < max_retries - 1:
                    print(f"{last_exception}. Повтор...")
                    time.sleep(2)
        
        raise Exception(f"❌ Не удалось выполнить запрос после {max_retries} попыток. "
                       f"Последняя ошибка: {last_exception}")
    
    def get(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        """GET запрос"""
        return self.make_request('GET', endpoint, params=params)
    
    def post(self, endpoint: str, data: Optional[Dict] = None) -> Dict:
        """POST запрос"""
        return self.make_request('POST', endpoint, data=data)
    
    def put(self, endpoint: str, data: Optional[Dict] = None) -> Dict:
        """PUT запрос"""
        return self.make_request('PUT', endpoint, data=data)
    
    def delete(self, endpoint: str) -> Dict:
        """DELETE запрос"""
        return self.make_request('DELETE', endpoint)

# ========================================
# 📊 ДЕМОНСТРАЦИОННЫЕ ПРИМЕРЫ
# ========================================

def demo_weather_api():
    """Демонстрация работы с погодным API"""
    
    print("\n🌤️ ДЕМОНСТРАЦИЯ WEATHER API")
    print("-" * 40)
    
    # Получаем API ключ из переменных окружения
    api_key = os.getenv('WEATHER_API_KEY')
    
    if not api_key:
        print("⚠️ API ключ для OpenWeatherMap не найден в переменных окружения")
        print("💡 Создайте .env файл и добавьте: WEATHER_API_KEY=your_key_here")
        return
    
    try:
        weather = WeatherAPI(api_key)
        
        # Получаем погоду для одного города
        print("📍 Получаем погоду для Москвы...")
        moscow_weather = weather.get_current_weather("Moscow")
        print(f"✅ Москва: {moscow_weather['temperature']}°C, {moscow_weather['description']}")
        
        # Получаем погоду для нескольких городов
        print("\n📍 Получаем погоду для нескольких городов...")
        cities = ["Moscow", "Saint Petersburg", "Novosibirsk", "London", "New York"]
        weather_df = weather.get_multiple_cities(cities)
        
        # Анализируем данные
        if not weather_df.empty and 'temperature' in weather_df.columns:
            valid_data = weather_df.dropna(subset=['temperature'])
            if not valid_data.empty:
                print(f"\n📊 АНАЛИЗ ПОГОДЫ:")
                print(f"   🌡️  Самый теплый город: {valid_data.loc[valid_data['temperature'].idxmax(), 'city']} "
                      f"({valid_data['temperature'].max()}°C)")
                print(f"   🧊 Самый холодный город: {valid_data.loc[valid_data['temperature'].idxmin(), 'city']} "
                      f"({valid_data['temperature'].min()}°C)")
                print(f"   📊 Средняя температура: {valid_data['temperature'].mean():.1f}°C")
        
    except Exception as e:
        print(f"❌ Ошибка демонстрации Weather API: {e}")

def demo_currency_api():
    """Демонстрация работы с валютным API"""
    
    print("\n💱 ДЕМОНСТРАЦИЯ CURRENCY API")
    print("-" * 40)
    
    try:
        currency = CurrencyAPI()
        
        # Получаем курсы основных валют к доллару
        print("💰 Получаем курсы валют к USD...")
        target_currencies = ['RUB', 'EUR', 'GBP', 'JPY', 'CNY']
        rates_df = currency.get_specific_rates('USD', target_currencies)
        
        print("📊 ТЕКУЩИЕ КУРСЫ:")
        for _, row in rates_df.iterrows():
            print(f"   💸 1 USD = {row['rate']:.4f} {row['currency']}")
        
        # Конвертация валют
        print("\n🔄 Примеры конвертации:")
        conversions = [
            (100, 'USD', 'RUB'),
            (1000, 'EUR', 'USD'),
            (50000, 'RUB', 'EUR')
        ]
        
        for amount, from_curr, to_curr in conversions:
            try:
                conversion = currency.calculate_conversion(amount, from_curr, to_curr)
                print(f"   💱 {conversion['original_amount']} {conversion['original_currency']} = "
                      f"{conversion['converted_amount']} {conversion['target_currency']}")
            except Exception as e:
                print(f"   ❌ Ошибка конвертации {from_curr}→{to_curr}: {e}")
        
    except Exception as e:
        print(f"❌ Ошибка демонстрации Currency API: {e}")

def demo_jsonplaceholder_api():
    """Демонстрация работы с JSONPlaceholder API"""
    
    print("\n👥 ДЕМОНСТРАЦИЯ JSONPLACEHOLDER API")
    print("-" * 40)
    
    try:
        api = JSONPlaceholderAPI()
        
        # Получаем и анализируем пользователей
        print("📊 Анализируем активность пользователей...")
        activity_df = api.analyze_user_activity()
        
        print("🏆 ТОП-5 САМЫХ АКТИВНЫХ ПОЛЬЗОВАТЕЛЕЙ:")
        top_users = activity_df.head()
        for _, user in top_users.iterrows():
            print(f"   👤 {user['name']} (@{user['username']}): "
                  f"{user['posts_count']} постов")
        
        # Статистика
        print(f"\n📈 СТАТИСТИКА:")
        print(f"   👥 Всего пользователей: {len(activity_df)}")
        print(f"   📝 Общее количество постов: {activity_df['posts_count'].sum()}")
        print(f"   📊 Средняя активность: {activity_df['posts_count'].mean():.1f} постов/пользователь")
        print(f"   📏 Средняя длина поста: {activity_df['avg_body_length'].mean():.0f} символов")
        
    except Exception as e:
        print(f"❌ Ошибка демонстрации JSONPlaceholder API: {e}")

def demo_universal_client():
    """Демонстрация универсального API клиента"""
    
    print("\n🔧 ДЕМОНСТРАЦИЯ УНИВЕРСАЛЬНОГО КЛИЕНТА")
    print("-" * 40)
    
    try:
        # Создаем клиент для JSONPlaceholder API
        client = UniversalAPIClient("https://jsonplaceholder.typicode.com")
        
        print("📊 Получаем данные через универсальный клиент...")
        
        # Получаем пользователей
        users = client.get("users")
        print(f"✅ Получено пользователей: {len(users)}")
        
        # Получаем посты
        posts = client.get("posts")
        print(f"✅ Получено постов: {len(posts)}")
        
        # Получаем комментарии с параметрами
        comments = client.get("comments", params={"postId": 1})
        print(f"✅ Получено комментариев для поста 1: {len(comments)}")
        
        print("🎉 Универсальный клиент работает корректно!")
        
    except Exception as e:
        print(f"❌ Ошибка демонстрации Universal Client: {e}")

# ========================================
# 🚀 ГЛАВНАЯ ФУНКЦИЯ
# ========================================

def main():
    """Главная функция для запуска всех демонстраций"""
    
    print("🎬 ЗАПУСК ДЕМОНСТРАЦИЙ API EXAMPLES")
    print("=" * 60)
    
    # Проверяем наличие .env файла
    if not os.path.exists('.env'):
        print("⚠️ Файл .env не найден.")
        print("💡 Создайте .env файл по образцу .env.example для работы с API ключами")
        print()
    
    # Запускаем демонстрации
    demo_weather_api()
    demo_currency_api()
    demo_jsonplaceholder_api() 
    demo_universal_client()
    
    print("\n" + "=" * 60)
    print("🎉 ВСЕ ДЕМОНСТРАЦИИ ЗАВЕРШЕНЫ!")
    print("💡 Используйте классы из этого файла в ваших проектах")
    print("📖 Подробнее в practice.md и README.md")
    print("=" * 60)

if __name__ == "__main__":
    main()