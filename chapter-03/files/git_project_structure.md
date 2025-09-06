# 🚀 Шаблон структуры Git-репозитория для аналитических проектов

## 📁 Рекомендуемая структура каталогов

```
analytics-project-name/
├── README.md                    # Главное описание проекта
├── CHANGELOG.md                 # История изменений
├── .gitignore                  # Исключения для Git
├── requirements.txt            # Зависимости Python (если есть)
│
├── 📁 data/                    # Данные (НЕ в Git, только в Git LFS)
│   ├── raw/                    # Исходные данные
│   ├── processed/              # Обработанные данные
│   ├── external/               # Внешние источники
│   └── temp/                   # Временные файлы (в .gitignore)
│
├── 📁 models/                  # Аналитические модели
│   ├── power-pivot/           # Power Pivot файлы (.xlsx)
│   ├── pivot-tables/          # Сводные таблицы
│   ├── dax-measures/          # DAX-формулы (.txt)
│   └── excel-workbooks/       # Excel файлы с анализом
│
├── 📁 reports/                # Готовые отчеты и дашборды
│   ├── weekly/                # Еженедельные отчеты
│   ├── monthly/               # Месячные отчеты
│   ├── quarterly/             # Квартальные отчеты
│   ├── dashboards/            # Интерактивные дашборды
│   └── presentations/         # Презентации для руководства
│
├── 📁 scripts/                # Скрипты автоматизации
│   ├── data-prep/             # Подготовка данных (.py, .sql)
│   ├── etl/                   # ETL процессы
│   ├── automation/            # Автоматизация отчетов (.bat, .ps1)
│   └── utilities/             # Вспомогательные скрипты
│
├── 📁 docs/                   # Документация проекта
│   ├── business-logic/        # Описание бизнес-логики
│   ├── technical/             # Техническая документация
│   ├── user-guides/           # Руководства пользователя
│   ├── data-dictionary/       # Словарь данных
│   └── images/                # Схемы и диаграммы
│
├── 📁 config/                 # Файлы конфигурации
│   ├── connections/           # Подключения к источникам
│   ├── parameters/            # Параметры отчетов
│   └── settings/              # Настройки приложений
│
└── 📁 tests/                  # Тесты и проверки
    ├── data-quality/          # Тесты качества данных
    ├── model-validation/      # Валидация моделей
    └── report-tests/          # Тесты отчетов
```

---

## ⚠️ .gitignore для аналитических проектов

### 📝 Создайте файл `.gitignore` со следующим содержимым:

```gitignore
# ============================================
# EXCEL И OFFICE ФАЙЛЫ
# ============================================

# Временные файлы Excel
~$*.xlsx
~$*.xls
~$*.xlsm
*.tmp
*.temp

# Резервные копии Excel
*.xlk
~*.xlsx
~*.xls

# Power BI временные файлы
*.pbix.tmp
~AutoRecover.*.pbix

# ============================================
# ДАННЫЕ (БОЛЬШИЕ ФАЙЛЫ)
# ============================================

# CSV файлы с данными (больше 50MB)
data/raw/*.csv
data/processed/*.csv
*.csv

# Excel файлы с большими данными
data/raw/*.xlsx
data/processed/*.xlsx

# Архивы данных
*.zip
*.rar
*.7z
*.gz

# ============================================
# КОНФИДЕНЦИАЛЬНАЯ ИНФОРМАЦИЯ
# ============================================

# Файлы с паролями и подключениями
config/passwords.txt
config/connection_strings.txt
secrets/
*.env
.env*

# Персональные настройки
personal-settings/
my-config/

# ============================================
# СИСТЕМНЫЕ И ВРЕМЕННЫЕ ФАЙЛЫ
# ============================================

# Windows
Thumbs.db
ehthumbs.db
Desktop.ini
$RECYCLE.BIN/

# macOS
.DS_Store
.AppleDouble
.LSOverride

# Временные папки
temp/
tmp/
cache/

# Логи
*.log
logs/

# ============================================
# PYTHON И СКРИПТЫ (ЕСЛИ ИСПОЛЬЗУЮТСЯ)
# ============================================

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/

# Jupyter Notebook
.ipynb_checkpoints

# ============================================
# БЭКАПЫ И СТАРЫЕ ВЕРСИИ
# ============================================

# Автоматические бэкапы
backup/
backups/
*_backup.*
*_old.*
*_archive.*

# Старые версии файлов
v1/
version_*/
archived/
```

---

## 📋 Naming Conventions (правила именования)

### 📁 **Папки и каталоги:**
- Используйте **дефисы** для разделения слов: `sales-analysis`, `customer-reports`
- **Не используйте пробелы** и специальные символы
- Используйте **английские названия** для технических папок
- **Русские названия** допустимы для бизнес-папок: `отчеты-продажи`

### 📄 **Файлы Excel (.xlsx):**
```
Формат: [тип]-[предмет]-[период]-[версия]
Примеры:
- dashboard-sales-2024-v2.xlsx
- report-monthly-dec2024-final.xlsx
- model-customers-q4-2024.xlsx
- analysis-products-abc-v3.xlsx
```

### 📊 **Отчеты по периодам:**
```
weekly-sales-2024-w15.xlsx    (15 неделя 2024)
monthly-revenue-2024-03.xlsx  (март 2024)
quarterly-analysis-2024-q2.xlsx (2 квартал 2024)
annual-summary-2024.xlsx      (годовой отчет)
```

### 💾 **Файлы данных (.csv):**
```
Формат: [источник]-[тип]-[дата]
Примеры:
- crm-sales-20241215.csv
- website-traffic-202412.csv
- inventory-stock-2024-q4.csv
```

### 📈 **DAX и формулы (.txt):**
```
dax-measures-sales.txt
dax-time-intelligence.txt
excel-formulas-financial.txt
```

---

## 🔄 Git Workflow для аналитических проектов

### 🌟 **Основная ветка (main):**
- Содержит **стабильные версии** отчетов и моделей
- **Только проверенный код** и файлы
- Обязательная **проверка коллегами** перед слиянием

### 🛠 **Ветки разработки:**
```bash
# Создание ветки для нового отчета
git checkout -b feature/sales-dashboard-2024

# Создание ветки для исправления ошибок
git checkout -b bugfix/pivot-table-calculation

# Экспериментальные работы
git checkout -b experiment/new-dax-measures
```

### 📝 **Правила коммитов:**

#### 🏷 **Префиксы коммитов:**
```
feat:     Новая функциональность (новый отчет, дашборд)
fix:      Исправление ошибки в расчетах или формулах
update:   Обновление существующих отчетов
data:     Обновление данных или источников
docs:     Изменения в документации
config:   Изменения в конфигурации
refactor: Реструктуризация без изменения функций
```

#### ✅ **Примеры хороших коммитов:**
```bash
git commit -m "feat: добавлен дашборд продаж по регионам"
git commit -m "fix: исправлена формула расчета маржинальности"
git commit -m "update: обновлены данные продаж за декабрь 2024"
git commit -m "docs: добавлено описание DAX-мер"
git commit -m "data: загружены новые справочники клиентов"
```

#### ❌ **Плохие примеры коммитов:**
```bash
git commit -m "изменения"                    # Слишком общий
git commit -m "исправил файл"               # Не указано что именно
git commit -m "final version"               # На английском без деталей
git commit -m "работает!"                   # Не описывает изменения
```

---

## 🏗 Жизненный цикл аналитического проекта

### 🎯 **1. Инициализация проекта:**
```bash
# Создание нового репозитория
mkdir retail-analytics-2024
cd retail-analytics-2024
git init

# Создание структуры каталогов
mkdir -p data/{raw,processed,external,temp}
mkdir -p models/{power-pivot,pivot-tables,dax-measures}
mkdir -p reports/{weekly,monthly,dashboards}
mkdir -p scripts/{data-prep,etl,automation}
mkdir -p docs/{business-logic,technical,user-guides}

# Создание базовых файлов
touch README.md CHANGELOG.md .gitignore
touch docs/project-overview.md

# Первый коммит
git add .
git commit -m "feat: инициализация структуры проекта"
```

### 📊 **2. Разработка аналитической модели:**
```bash
# Создание ветки для модели
git checkout -b feature/sales-model-powerpivot

# Добавление файлов модели
# [работа в Excel/Power Pivot]

# Коммит с описанием модели
git add models/power-pivot/sales-model-v1.xlsx
git commit -m "feat: создана многотабличная модель продаж с DAX-мерами"

# Добавление документации
git add docs/business-logic/sales-model-description.md
git commit -m "docs: описание бизнес-логики модели продаж"
```

### 📈 **3. Создание отчетов:**
```bash
# Ветка для еженедельного отчета
git checkout -b feature/weekly-sales-report

# Добавление отчета
git add reports/weekly/sales-report-template.xlsx
git commit -m "feat: шаблон еженедельного отчета по продажам"

# Автоматизация
git add scripts/automation/weekly-report-update.py
git commit -m "feat: скрипт автоматического обновления данных"
```

### 🔄 **4. Итерации и улучшения:**
```bash
# Исправление ошибок
git checkout -b bugfix/margin-calculation
# [исправление формул]
git commit -m "fix: исправлен расчет маржинальности в DAX-мерах"

# Добавление новых метрик
git checkout -b feature/customer-ltv-analysis
# [добавление анализа LTV]
git commit -m "feat: добавлен анализ жизненной ценности клиентов"
```

### 🚀 **5. Релиз и деплой:**
```bash
# Слияние в main
git checkout main
git merge feature/sales-model-powerpivot
git merge feature/weekly-sales-report

# Создание релиза
git tag -a v1.0 -m "Релиз 1.0: основная модель продаж и еженедельные отчеты"
git push origin v1.0

# Обновление changelog
echo "## v1.0 (2024-12-15)\n- Создана модель продаж\n- Добавлен еженедельный отчет" >> CHANGELOG.md
git add CHANGELOG.md
git commit -m "docs: обновлен CHANGELOG для релиза v1.0"
```

---

## 👥 Командная работа над аналитическими проектами

### 🔀 **Распределение ролей:**

#### 👨‍💼 **Ведущий аналитик:**
- Создает архитектуру проекта
- Проверяет merge requests
- Управляет релизами
- Отвечает за качество моделей

#### 📊 **Аналитики данных:**
- Разрабатывают отчеты и дашборды
- Создают DAX-меры и формулы
- Документируют бизнес-логику
- Тестируют расчеты

#### 🛠 **Инженеры данных:**
- Создают ETL-скрипты
- Настраивают автоматизацию
- Поддерживают подключения к данным
- Оптимизируют производительность

### 🔄 **Process командной работы:**

```bash
# 1. Получение последней версии
git checkout main
git pull origin main

# 2. Создание ветки для задачи
git checkout -b feature/quarterly-analysis

# 3. Работа над задачей
# [разработка отчета]

# 4. Промежуточные коммиты
git add .
git commit -m "feat: добавлена базовая структура квартального отчета"

# 5. Обновление с main (если нужно)
git checkout main
git pull origin main
git checkout feature/quarterly-analysis
git merge main

# 6. Финальный коммит
git add .
git commit -m "feat: завершен квартальный анализ с трендами"

# 7. Push ветки
git push origin feature/quarterly-analysis

# 8. Создание Pull/Merge Request
# [через интерфейс GitLab/GitHub/Bitbucket]

# 9. Code Review и слияние
# [ведущий аналитик проверяет и одобряет]

# 10. Удаление ветки после слияния
git checkout main
git pull origin main
git branch -d feature/quarterly-analysis
```

---

## 📊 Управление версиями Excel файлов

### 💡 **Особенности работы с Excel в Git:**

#### ✅ **Что хорошо работает:**
- **Небольшие файлы** (до 10 MB) отлично трекаются
- **Шаблоны отчетов** без данных
- **Файлы с формулами и макросами**
- **Дашборды с подключениями** к внешним источникам

#### ❌ **Что работает плохо:**
- **Файлы с большими объемами данных** (более 50 MB)
- **Часто изменяющиеся рабочие книги**
- **Файлы с включенными исходными данными**

### 🛠 **Best Practices для Excel файлов:**

#### 📋 **1. Разделение шаблонов и данных:**
```
models/
├── templates/              # Шаблоны без данных (в Git)
│   ├── sales-template.xlsx
│   └── dashboard-template.xlsx
├── working/               # Рабочие файлы с данными (в .gitignore)
│   ├── sales-december.xlsx
│   └── dashboard-current.xlsx
└── final/                 # Финальные отчеты (в Git, если <10MB)
    ├── report-q4-2024.xlsx
    └── annual-summary.xlsx
```

#### 🔗 **2. Использование внешних подключений:**
- Подключайтесь к CSV файлам через Power Query
- Используйте базы данных вместо встроенных данных
- Храните данные отдельно от логики отчетов

#### 📝 **3. Комментарии к коммитам Excel файлов:**
```bash
# Хорошие комментарии для Excel
git commit -m "feat: добавлена сводная таблица по регионам в sales-template.xlsx"
git commit -m "fix: исправлена формула ВПР на строке 45 в dashboard-template.xlsx"
git commit -m "update: обновлена структура отчета - добавлен лист 'Тренды'"
```

---

## 🔧 Автоматизация и DevOps

### 🤖 **Автоматическое обновление отчетов:**

#### 📝 **Пример batch-скрипта (Windows):**
```batch
@echo off
REM Обновление еженедельного отчета продаж

echo Начало обновления отчетов...
cd /d "C:\Analytics\retail-analytics-2024"

echo Получение последних изменений из Git...
git pull origin main

echo Обновление данных...
python scripts/data-prep/update_sales_data.py

echo Обновление Excel отчетов...
python scripts/automation/refresh_excel_reports.py

echo Создание коммита с обновлениями...
git add reports/weekly/
git commit -m "data: автоматическое обновление еженедельных отчетов %DATE%"
git push origin main

echo Отчеты успешно обновлены!
pause
```

#### 🐍 **Пример Python скрипта:**
```python
"""
Автоматизация обновления Excel отчетов
"""
import os
import subprocess
from datetime import datetime
import win32com.client as win32

def update_excel_file(file_path):
    """Обновление внешних подключений в Excel файле"""
    xl = win32.Dispatch("Excel.Application")
    xl.Visible = False
    
    wb = xl.Workbooks.Open(file_path)
    wb.RefreshAll()
    wb.Save()
    wb.Close()
    xl.Quit()
    
    print(f"Обновлен файл: {file_path}")

def git_commit_changes():
    """Коммит изменений в Git"""
    date_str = datetime.now().strftime("%Y-%m-%d")
    subprocess.run([
        "git", "add", "reports/"
    ])
    subprocess.run([
        "git", "commit", "-m", f"data: автоматическое обновление отчетов {date_str}"
    ])
    subprocess.run([
        "git", "push", "origin", "main"
    ])

if __name__ == "__main__":
    # Список файлов для обновления
    files_to_update = [
        "reports/weekly/sales-report.xlsx",
        "reports/monthly/revenue-dashboard.xlsx"
    ]
    
    for file_path in files_to_update:
        if os.path.exists(file_path):
            update_excel_file(file_path)
    
    git_commit_changes()
    print("Все отчеты успешно обновлены и зафиксированы в Git!")
```

---

## 📚 Шаблоны README для проектов

### 📄 **Базовый шаблон README.md:**

```markdown
# 📊 Проект "Название проекта"

## 🎯 Описание проекта
Краткое описание целей и задач аналитического проекта.

## 📋 Содержимое репозитория
- **models/** — Аналитические модели и сводные таблицы
- **reports/** — Готовые отчеты и дашборды  
- **scripts/** — Скрипты автоматизации
- **docs/** — Документация проекта

## 🛠 Требования к системе
- Excel 2019+ с Power Pivot
- Python 3.8+ (для скриптов автоматизации)
- Git 2.30+

## 🚀 Быстрый старт
1. Склонируйте репозиторий: `git clone [url]`
2. Откройте Excel файлы из папки `models/`
3. Обновите подключения к данным
4. Запустите обновление через скрипты

## 👥 Команда проекта
- **Ведущий аналитик:** Имя Фамилия
- **Аналитики:** Список участников
- **Дата создания:** ДД.ММ.ГГГГ

## 📞 Контакты
- Email: analytics@company.com
- Telegram: @analytics_team
```

---

## 🎯 Заключение

Правильная организация Git-репозитория для аналитических проектов:

### ✅ **Обеспечивает:**
- **Надежное версионирование** критических отчетов и моделей
- **Эффективную командную работу** без конфликтов файлов
- **Автоматизацию процессов** обновления и развертывания
- **Полную документированность** бизнес-логики и технических решений

### 🎯 **Повышает качество работы:**
- Снижает риски потери данных и откатов изменений
- Ускоряет разработку через переиспользование компонентов
- Улучшает прозрачность аналитических процессов
- Упрощает onboarding новых членов команды

**Следование этим принципам сделает ваши аналитические проекты профессиональными, надежными и масштабируемыми!**

---

📖 [Вернуться к описанию файлов](README.md) | 📝 [Перейти к практике](../practice.md)

---

📢 Присоединяйтесь к чату курса: [@analytics_course_chat](https://t.me/analytics_course_chat)
📢 Канал курса: [@analytics_course_channel](https://t.me/analytics_course_channel)