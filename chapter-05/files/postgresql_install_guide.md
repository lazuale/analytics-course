# 🛠 Руководство по установке PostgreSQL

## 📋 Системные требования

- **Операционная система:** Windows 10/11, macOS 10.15+, Linux (Ubuntu 18.04+)
- **Оперативная память:** минимум 2 GB, рекомендуется 4 GB+
- **Дисковое пространство:** минимум 1 GB свободного места
- **Права администратора** для установки

---

## 🖥 Установка на Windows

### Шаг 1: Загрузка установщика
1. Перейдите на официальный сайт: https://www.postgresql.org/download/windows/
2. Нажмите "Download the installer"
3. Выберите PostgreSQL 15 или новее для Windows x86-64
4. Скачайте файл (размер ~300 MB)

### Шаг 2: Запуск установки
1. **Запустите скачанный .exe файл** от имени администратора
2. **Выберите компоненты для установки:**
   - ✅ PostgreSQL Server (основной сервер)
   - ✅ pgAdmin 4 (графический интерфейс)
   - ✅ Stack Builder (дополнительные модули)
   - ✅ Command Line Tools (инструменты командной строки)

### Шаг 3: Настройка параметров
1. **Каталог установки:** оставьте по умолчанию `C:\Program Files\PostgreSQL\15`
2. **Каталог данных:** оставьте по умолчанию
3. **Пароль суперпользователя:** 
   - Придумайте надежный пароль для пользователя `postgres`
   - ⚠️ **ЗАПИШИТЕ ПАРОЛЬ** — он понадобится для подключения
4. **Порт:** оставьте стандартный `5432`
5. **Локаль:** выберите `Russian, Russia` или оставьте `C`

### Шаг 4: Завершение установки
1. Дождитесь завершения установки (5-10 минут)
2. Запустите Stack Builder для установки дополнительных модулей (опционально)
3. После установки в меню Пуск появятся:
   - **pgAdmin 4** — графический интерфейс
   - **SQL Shell (psql)** — командная строка

### Шаг 5: Проверка установки
1. **Откройте pgAdmin 4**
2. При первом запуске установите мастер-пароль для pgAdmin
3. В левой панели найдите "Servers" → "PostgreSQL 15"
4. Введите пароль пользователя postgres
5. Если подключение успешно — установка завершена!

---

## 🍎 Установка на macOS

### Вариант 1: Homebrew (рекомендуется)

1. **Установите Homebrew** (если еще не установлен):
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. **Установите PostgreSQL:**
   ```bash
   brew install postgresql@15
   ```

3. **Запустите службу PostgreSQL:**
   ```bash
   brew services start postgresql@15
   ```

4. **Создайте базу данных:**
   ```bash
   createdb postgres
   ```

5. **Подключитесь к PostgreSQL:**
   ```bash
   psql postgres
   ```

### Вариант 2: Postgres.app

1. Скачайте Postgres.app с https://postgresapp.com/
2. Перетащите приложение в папку Applications
3. Запустите Postgres.app
4. Нажмите "Initialize" для создания нового сервера
5. Сервер будет доступен на порту 5432

### Установка pgAdmin для macOS

1. Скачайте pgAdmin с https://www.pgadmin.org/download/pgadmin-4-macos/
2. Установите .dmg файл
3. Запустите pgAdmin и настройте подключение к серверу

---

## 🐧 Установка на Linux (Ubuntu/Debian)

### Шаг 1: Обновление системы
```bash
sudo apt update
sudo apt upgrade -y
```

### Шаг 2: Установка PostgreSQL
```bash
# Установка PostgreSQL и дополнительных пакетов
sudo apt install postgresql postgresql-contrib postgresql-client -y
```

### Шаг 3: Запуск и настройка
```bash
# Запуск службы PostgreSQL
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Проверка статуса
sudo systemctl status postgresql
```

### Шаг 4: Настройка пользователя
```bash
# Переключение на пользователя postgres
sudo -u postgres psql

# В psql выполните:
ALTER USER postgres PASSWORD 'your_password';
\q
```

### Шаг 5: Установка pgAdmin (опционально)
```bash
# Добавление репозитория pgAdmin
curl -fsSL https://www.pgadmin.org/static/packages_pgadmin_org.pub | sudo gpg --dearmor -o /usr/share/keyrings/packages-pgadmin-org.gpg

# Установка pgAdmin
sudo apt install pgadmin4-web -y

# Настройка веб-интерфейса
sudo /usr/pgadmin4/bin/setup-web.sh
```

---

## 🔧 Первоначальная настройка

### Подключение через psql (командная строка)

**Windows:**
```cmd
# Откройте "SQL Shell (psql)" из меню Пуск
# Или в командной строке:
"C:\Program Files\PostgreSQL\15\bin\psql.exe" -U postgres -h localhost
```

**macOS/Linux:**
```bash
psql -U postgres -h localhost
```

### Основные команды psql

```sql
-- Просмотр версии PostgreSQL
SELECT version();

-- Список баз данных
\l

-- Подключение к базе данных
\c database_name

-- Список таблиц в текущей БД
\dt

-- Описание структуры таблицы
\d table_name

-- Выход из psql
\q

-- Справка по командам
\help
\?
```

### Создание учебной базы данных

```sql
-- Создание базы данных для курса
CREATE DATABASE analytics_course;

-- Подключение к базе
\c analytics_course;

-- Проверка подключения
SELECT current_database(), current_user;
```

---

## 🔐 Настройка безопасности

### Изменение настроек аутентификации

**Файл pg_hba.conf** контролирует доступ к базе данных:

**Расположение файла:**
- Windows: `C:\Program Files\PostgreSQL\15\data\pg_hba.conf`
- macOS (Homebrew): `/usr/local/var/postgres/pg_hba.conf`
- Linux: `/etc/postgresql/15/main/pg_hba.conf`

**Базовая настройка для обучения:**
```
# TYPE  DATABASE        USER            ADDRESS                 METHOD
local   all             postgres                                md5
host    all             postgres        127.0.0.1/32           md5
host    all             postgres        ::1/128                md5
```

⚠️ **После изменения pg_hba.conf перезапустите PostgreSQL**

### Создание пользователя для обучения

```sql
-- Создание пользователя student
CREATE USER student WITH PASSWORD 'student123';

-- Предоставление прав на базу analytics_course
GRANT ALL PRIVILEGES ON DATABASE analytics_course TO student;

-- Предоставление прав на схему public
\c analytics_course;
GRANT ALL ON SCHEMA public TO student;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO student;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO student;
```

---

## 🆘 Решение типичных проблем

### Проблема 1: "could not connect to server"

**Причины и решения:**
- **Служба не запущена:**
  - Windows: Службы → PostgreSQL → Запустить
  - macOS: `brew services start postgresql@15`
  - Linux: `sudo systemctl start postgresql`

- **Неправильный порт:** Проверьте порт 5432 в настройках
- **Файерволл:** Добавьте исключение для порта 5432

### Проблема 2: "password authentication failed"

**Решения:**
- Проверьте правильность пароля пользователя postgres
- Убедитесь, что в pg_hba.conf настроена аутентификация md5
- Перезапустите PostgreSQL после изменения настроек

### Проблема 3: pgAdmin не подключается

**Решения:**
- Проверьте, что PostgreSQL запущен
- В pgAdmin проверьте настройки подключения:
  - Host: localhost или 127.0.0.1
  - Port: 5432
  - Username: postgres
  - Database: postgres

### Проблема 4: Ошибки с правами доступа в Linux

**Решения:**
```bash
# Сброс прав для пользователя postgres
sudo -u postgres psql -c "ALTER USER postgres PASSWORD 'newpassword';"

# Проверка статуса службы
sudo systemctl status postgresql

# Перезапуск службы
sudo systemctl restart postgresql
```

---

## 📊 Инструменты для работы с PostgreSQL

### pgAdmin 4 (рекомендуется для начинающих)
- **Графический интерфейс** для управления базами данных
- **Визуальный конструктор** запросов
- **Мониторинг производительности**
- **Резервное копирование и восстановление**

### psql (командная строка)
- **Быстрый доступ** к базе данных
- **Выполнение скриптов** из файлов
- **Автоматизация** задач
- **Минимальное потребление ресурсов**

### DBeaver (альтернатива)
- **Универсальный клиент** для разных СУБД
- **Продвинутые возможности** редактирования
- **Встроенный редактор ER-диаграмм**
- Скачать: https://dbeaver.io/

---

## ✅ Проверка готовности к работе

### Контрольный список:
- [ ] PostgreSQL установлен и запущен
- [ ] pgAdmin успешно подключается к серверу
- [ ] Создана учебная база данных `analytics_course`
- [ ] Выполняются базовые SQL команды
- [ ] Известен пароль пользователя postgres

### Тестовый запрос:
```sql
-- Выполните этот запрос для проверки работоспособности
SELECT 
    'PostgreSQL готов к работе!' as message,
    version() as version,
    current_database() as database,
    current_user as user,
    now() as current_time;
```

Если запрос выполнился успешно — **вы готовы к изучению главы 5!**

---

## 🔗 Полезные ссылки

- **Официальная документация:** https://www.postgresql.org/docs/
- **Учебник по SQL:** https://www.w3schools.com/sql/
- **PostgreSQL Wiki:** https://wiki.postgresql.org/
- **Сообщество на GitHub:** https://github.com/postgres/postgres
- **Русскоязычная документация:** https://postgrespro.ru/docs/

---

📢 **Если возникли проблемы с установкой — обратитесь в Telegram чат курса!**
[@analytics_course_chat](https://t.me/analytics_course_chat)
