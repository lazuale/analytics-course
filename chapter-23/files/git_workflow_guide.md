# 🔧 Git Workflow Guide — Руководство по работе с Git для аналитических проектов

## 🎯 Цель документа

Это руководство описывает лучшие практики использования Git и GitHub для управления аналитическими проектами, включая обработку данных, Jupyter notebooks, Power BI отчеты и код на Python/SQL.

---

## 📁 Стандартная структура аналитического проекта

### 🏗️ Рекомендуемая структура папок

```
📁 analytics-project/
├── 📄 README.md                     # Описание проекта  
├── 📋 requirements.txt               # Python зависимости
├── ⚙️ config.yaml                    # Конфигурация
├── 🚫 .gitignore                     # Исключения из Git
├── 📊 data/                          # Данные (осторожно с приватными!)
│   ├── 📥 raw/                       # Исходные данные
│   ├── 🔧 processed/                 # Обработанные данные
│   └── 🌐 external/                  # Внешние источники
├── 📓 notebooks/                     # Jupyter notebooks
│   ├── 🔍 01_exploratory/            # Исследовательский анализ
│   ├── 📊 02_modeling/               # Моделирование и анализ
│   └── 📈 03_reporting/              # Финальные отчеты
├── 🐍 src/                           # Исходный код
│   ├── 🔧 data_processing/           
│   │   ├── __init__.py
│   │   ├── extract.py                # ETL операции
│   │   ├── transform.py              # Трансформации
│   │   └── load.py                   # Загрузка данных
│   ├── 📊 analysis/
│   │   ├── __init__.py
│   │   ├── statistics.py             # Статистические функции
│   │   ├── segmentation.py           # Сегментация
│   │   └── forecasting.py            # Прогнозирование
│   ├── 📈 visualization/
│   │   ├── __init__.py
│   │   ├── charts.py                 # Функции создания графиков
│   │   └── dashboards.py             # Дашборд компоненты
│   └── 🛠️ utils/
│       ├── __init__.py
│       ├── config.py                 # Работа с конфигурацией
│       ├── logger.py                 # Логирование
│       └── helpers.py                # Вспомогательные функции
├── 📊 reports/                       # Готовые отчеты
│   ├── 📄 powerbi/                   # Power BI файлы
│   │   ├── main_dashboard.pbix
│   │   └── executive_report.pbix
│   ├── 🖼️ figures/                   # Графики и изображения
│   │   ├── trend_analysis.png
│   │   └── segmentation_chart.png
│   └── 📋 documents/                 # Текстовые отчеты
│       ├── executive_summary.pdf
│       └── technical_appendix.docx
├── 🧪 tests/                         # Тесты
│   ├── test_data_processing.py
│   ├── test_analysis.py
│   └── test_visualization.py
├── 📜 sql/                           # SQL скрипты
│   ├── 01_create_tables.sql
│   ├── 02_data_quality_checks.sql
│   └── 03_analysis_queries.sql
└── 🔧 scripts/                       # Вспомогательные скрипты
    ├── setup.py                      # Установка окружения
    ├── run_analysis.py               # Запуск анализа
    └── deploy.sh                     # Деплой отчетов
```

---

## 🔧 Настройка Git репозитория

### 1️⃣ Инициализация проекта

```bash
# Создание и инициализация репозитория
mkdir my-analytics-project
cd my-analytics-project
git init

# Настройка пользователя (если не настроено глобально)
git config user.name "Your Name"
git config user.email "your.email@company.com"

# Создание основной структуры
mkdir -p data/{raw,processed,external}
mkdir -p notebooks/{01_exploratory,02_modeling,03_reporting}
mkdir -p src/{data_processing,analysis,visualization,utils}
mkdir -p reports/{powerbi,figures,documents}
mkdir -p tests sql scripts

# Создание основных файлов
touch README.md .gitignore requirements.txt config.yaml
```

### 2️⃣ Создание .gitignore для аналитических проектов

```gitignore
# ==========================================
# ДАННЫЕ И КОНФИДЕНЦИАЛЬНАЯ ИНФОРМАЦИЯ
# ==========================================

# Исходные данные (могут содержать персональную информацию)
data/raw/
!data/raw/.gitkeep
!data/raw/sample_*.csv

# Большие файлы с данными
*.parquet
*.pkl
*.h5
*.hdf5
data/processed/*.csv
data/processed/*.xlsx

# Базы данных
*.db
*.sqlite
*.sqlite3

# Конфиденциальные файлы
.env
.secrets
credentials.json
config_production.yaml
api_keys.txt

# ==========================================
# PYTHON
# ==========================================

# Байт-код Python
__pycache__/
*.py[cod]
*$py.class
*.so

# Виртуальные окружения
.venv/
env/
ENV/
venv/

# Jupyter Notebook checkpoints
.ipynb_checkpoints/

# Pytest кэш
.pytest_cache/
.coverage
htmlcov/

# ==========================================
# POWER BI И MICROSOFT OFFICE
# ==========================================

# Временные файлы Power BI
*.tmp
~$*.pbix
~$*.pbit

# Backup файлы Power BI
*.pbix.backup*

# Excel временные файлы
~$*.xlsx
~$*.xls
~$*.docx
~$*.pptx

# ==========================================
# СИСТЕМНЫЕ И IDE ФАЙЛЫ
# ==========================================

# Windows
Thumbs.db
Desktop.ini
$RECYCLE.BIN/

# macOS  
.DS_Store
.AppleDouble
.LSOverride

# VS Code
.vscode/
!.vscode/settings.json
!.vscode/launch.json

# PyCharm
.idea/

# ==========================================
# ЛОГИ И ВРЕМЕННЫЕ ФАЙЛЫ
# ==========================================

# Файлы логов
*.log
logs/
log_*.txt

# Временные файлы анализа
temp/
tmp/
scratch/

# Кэш библиотек
.cache/

# ==========================================
# ОТЧЕТЫ И БОЛЬШИЕ ФАЙЛЫ
# ==========================================

# Большие графики (кроме образцов)
reports/figures/*.png
reports/figures/*.jpg
reports/figures/*.pdf
!reports/figures/sample_*.png

# Большие отчеты
reports/documents/*.pdf
!reports/documents/template.pdf

# ==========================================
# СПЕЦИФИЧНЫЕ ДЛЯ ПРОЕКТА ИСКЛЮЧЕНИЯ
# ==========================================

# Добавьте сюда специфичные для вашего проекта исключения
```

---

## 🔄 Git Flow для аналитических проектов

### 📊 Адаптированная модель ветвления

```
📈 main (производственная версия)
├── 🚧 develop (текущая разработка)
│   ├── 🔬 feature/customer-segmentation
│   ├── 📊 feature/sales-dashboard  
│   ├── 🔍 feature/churn-analysis
│   └── 📈 feature/forecasting-model
├── 🐛 hotfix/critical-bug-fix
└── 📦 release/v1.2.0
```

### 🌲 Описание веток

**📈 main (master)**
- Стабильная, готовая к production версия
- Только проверенные и протестированные результаты
- Тегируется версиями (v1.0.0, v1.1.0, etc.)

**🚧 develop**  
- Интеграционная ветка для новой разработки
- Содержит последние завершенные feature
- Регулярно тестируется и валидируется

**🔬 feature/**
- Ветки для конкретных аналитических задач
- Именование: `feature/task-description`
- Примеры: `feature/customer-churn-model`, `feature/revenue-dashboard`

**🐛 hotfix/**
- Срочные исправления в production
- Именование: `hotfix/issue-description`
- Сливаются в main и develop одновременно

**📦 release/**
- Подготовка к релизу новой версии
- Финальные проверки и документирование
- Именование: `release/v1.2.0`

---

## 💬 Стандарты коммитов

### 🏷️ Формат сообщений коммитов

```
<type>(<scope>): <subject>

<body>

<footer>
```

### 📝 Типы коммитов

```bash
✨ feat: новая функциональность или анализ
🐛 fix: исправление ошибок в коде или данных  
📊 data: обновление или добавление данных
📈 viz: изменения в visualizations
📚 docs: обновление документации
🔧 config: изменения конфигурации
🚀 perf: улучшение производительности
♻️  refactor: рефакторинг без изменения функциональности
🧪 test: добавление или изменение тестов
🎨 style: форматирование кода (не влияет на логику)
```

### 💡 Примеры качественных коммитов

```bash
# Хорошие примеры
✨ feat(segmentation): добавить k-means кластеризацию клиентов
📊 data: обновить данные продаж за Q4 2024
📈 viz: улучшить дашборд KPI с новыми метриками
🐛 fix(sql): исправить JOIN для корректного расчета LTV
📚 docs: добавить описание методологии сегментации

# Плохие примеры  
❌ "fix stuff"
❌ "update"
❌ "работает" 
❌ "final version"
❌ "commit"
```

---

## 🤝 Процесс совместной работы

### 1️⃣ Создание feature ветки

```bash
# Переключение на develop и обновление
git checkout develop
git pull origin develop

# Создание новой feature ветки
git checkout -b feature/customer-lifetime-value

# Работа над задачей...
git add .
git commit -m "✨ feat(ltv): добавить расчет customer lifetime value"

# Отправка в удаленный репозиторий
git push -u origin feature/customer-lifetime-value
```

### 2️⃣ Pull Request процесс

**📋 Шаблон описания Pull Request:**

```markdown
## 📊 Описание изменений
Краткое описание выполненной аналитической задачи

## 🎯 Бизнес-цель
Какую бизнес-проблему решает этот анализ

## 📈 Результаты
- Ключевой инсайт 1
- Ключевой инсайт 2  
- Ключевой инсайт 3

## 🔧 Технические изменения
- [ ] Новые данные добавлены
- [ ] Новые функции анализа
- [ ] Обновлены визуализации
- [ ] Документация обновлена

## 🧪 Валидация
- [ ] Данные проверены на качество
- [ ] Расчеты верифицированы  
- [ ] Код протестирован
- [ ] Notebook выполняется без ошибок

## 📋 Чек-лист для ревью
- [ ] Код читаем и документирован
- [ ] Методология корректна
- [ ] Результаты интерпретированы правильно
- [ ] Нет конфиденциальных данных в коммитах
```

### 3️⃣ Code Review для аналитики

**🔍 Что проверять в аналитическом коде:**

```markdown
📊 Данные:
- Корректность источников данных
- Обработка пропусков и выбросов
- Фильтрация и очистка данных
- Период анализа и актуальность

📈 Методология:
- Правильность статистических методов
- Валидация предположений
- Интерпретация результатов
- Учет ограничений и bias

💻 Технический код:
- Читаемость и документирование
- Производительность запросов/кода
- Воспроизводимость результатов
- Обработка ошибок

📚 Документация:
- Описание методологии
- Интерпретация результатов  
- Рекомендации для бизнеса
- Ограничения и риски
```

---

## 📚 Документирование

### 📄 Структура README.md

```markdown
# 📊 Название проекта

## 🎯 Цель анализа
Четкое описание бизнес-задачи которую решает проект

## 📊 Данные
### Источники
- **CRM система**: клиентские данные
- **DWH**: транзакционные данные  
- **Web-analytics**: поведенческие данные

### Период анализа
📅 2022-01-01 до 2024-12-31

### Ограничения
⚠️ Данные могут содержать дубликаты до 2023 года
⚠️ Некоторые метрики недоступны для периода до 2022

## 🛠️ Технологический стек
- **Python 3.9+**: основной язык анализа
- **pandas, numpy**: обработка данных
- **scikit-learn**: машинное обучение
- **matplotlib, plotly**: визуализация
- **Power BI**: интерактивные дашборды
- **SQL**: работа с базами данных

## 🚀 Как запустить анализ

### Установка зависимостей
```bash
pip install -r requirements.txt
```

### Подготовка данных
```bash
python scripts/extract_data.py
python scripts/clean_data.py
```

### Запуск анализа  
```bash
jupyter notebook notebooks/01_exploratory/main_analysis.ipynb
```

## 📈 Ключевые результаты
1. **Сегментация клиентов**: выделено 4 основных сегмента
2. **Churn prediction**: модель с точностью 87%
3. **LTV модель**: прогноз доходности клиентов

## 📊 Структура репозитория
```
├── data/           # Данные (не включены в Git)
├── notebooks/      # Jupyter notebooks  
├── src/           # Исходный код
├── reports/       # Готовые отчеты
└── tests/         # Тесты
```

## 👥 Команда
- **Data Scientist**: Имя Фамилия (@username)
- **Business Analyst**: Имя Фамилия (@username)
- **Product Owner**: Имя Фамилия (@username)

## 📄 Лицензия
MIT License
```

---

## ⚙️ Автоматизация и CI/CD

### 🤖 GitHub Actions для аналитики

```yaml
# .github/workflows/analytics-ci.yml
name: Analytics CI

on:
  push:
    branches: [develop, main]
  pull_request:
    branches: [develop, main]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'
        
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        
    - name: Lint code with flake8
      run: |
        flake8 src/ --max-line-length=88
        
    - name: Run tests
      run: |
        pytest tests/
        
    - name: Check notebooks
      run: |
        jupyter nbconvert --execute --to notebook --inplace notebooks/**/*.ipynb
        
    - name: Validate data schemas
      run: |
        python scripts/validate_schemas.py
```

### 📊 Автоматическая валидация данных

```python
# scripts/validate_schemas.py
"""
Скрипт для валидации схем данных
"""

import pandas as pd
import pandera as pa
from pathlib import Path

def validate_sales_data():
    """Валидация данных продаж"""
    
    schema = pa.DataFrameSchema({
        "date": pa.Column(pa.DateTime),
        "customer_id": pa.Column(pa.Int, checks=[
            pa.Check.greater_than(0)
        ]),
        "amount": pa.Column(pa.Float, checks=[
            pa.Check.greater_than_or_equal_to(0)
        ]),
        "product_id": pa.Column(pa.String, nullable=False)
    })
    
    # Валидация файлов
    data_files = Path("data/processed").glob("sales_*.csv")
    
    for file_path in data_files:
        df = pd.read_csv(file_path)
        try:
            schema.validate(df)
            print(f"✅ {file_path.name} валидация прошла успешно")
        except pa.errors.SchemaError as e:
            print(f"❌ {file_path.name} ошибка валидации: {e}")
            raise

if __name__ == "__main__":
    validate_sales_data()
```

---

## 🔐 Безопасность и конфиденциальность

### 🛡️ Защита конфиденциальных данных

```bash
# Установка git-crypt для шифрования чувствительных файлов
git-crypt init

# Создание .gitattributes для шифрования
echo "credentials.json filter=git-crypt diff=git-crypt" >> .gitattributes
echo "config_production.yaml filter=git-crypt diff=git-crypt" >> .gitattributes

# Добавление ключа для команды
git-crypt add-gpg-user user@example.com
```

### 🔍 Проверка на утечки данных

```python
# scripts/check_data_leaks.py
"""
Проверка коммитов на наличие конфиденциальных данных
"""

import re
import os
from pathlib import Path

def check_for_sensitive_data(file_path):
    """Проверка файла на конфиденциальные данные"""
    
    sensitive_patterns = [
        r'\b\d{4}-\d{4}-\d{4}-\d{4}\b',  # Номера карт
        r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',  # Email
        r'\b\+7\d{10}\b',  # Телефоны РФ
        r'password\s*=\s*["\'][^"\']+["\']',  # Пароли
        r'api_key\s*=\s*["\'][^"\']+["\']',  # API ключи
    ]
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        for pattern in sensitive_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                print(f"⚠️  Найдены подозрительные данные в {file_path}:")
                for match in matches[:3]:  # Показать первые 3
                    print(f"   {match}")
                return True
                
    except UnicodeDecodeError:
        # Бинарный файл, пропускаем
        pass
        
    return False

# Проверка всех файлов в репозитории
for file_path in Path('.').rglob('*'):
    if file_path.is_file() and not str(file_path).startswith('.git'):
        check_for_sensitive_data(file_path)
```

---

## 📋 Чек-лист для аналитического проекта

### ✅ Перед началом проекта

- [ ] Репозиторий инициализирован с правильной структурой
- [ ] .gitignore настроен для аналитических файлов
- [ ] README.md содержит описание проекта и данных
- [ ] requirements.txt создан с зависимостями
- [ ] Настроены ветки main, develop
- [ ] Команда добавлена в репозиторий с правильными правами

### ✅ Во время разработки

- [ ] Feature ветка создана для каждой задачи
- [ ] Коммиты имеют описательные сообщения с префиксами
- [ ] Конфиденциальные данные не попадают в коммиты
- [ ] Код документирован и читаем
- [ ] Notebooks выполняются без ошибок
- [ ] Результаты валидированы и интерпретированы

### ✅ Перед слиянием

- [ ] Pull Request содержит подробное описание
- [ ] Code review проведен другим аналитиком
- [ ] Все тесты проходят
- [ ] Документация обновлена
- [ ] Методология описана
- [ ] Ограничения и риски указаны

---

## 🚀 Продвинутые техники

### 🔄 Автоматическое обновление отчетов

```python
# scripts/auto_refresh_reports.py
"""
Автоматическое обновление Power BI отчетов при изменении данных
"""

import requests
import json
from datetime import datetime

def refresh_powerbi_dataset(dataset_id, access_token):
    """Обновление датасета в Power BI"""
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    url = f'https://api.powerbi.com/v1.0/myorg/datasets/{dataset_id}/refreshes'
    
    response = requests.post(url, headers=headers)
    
    if response.status_code == 202:
        print(f"✅ Обновление датасета {dataset_id} запущено")
    else:
        print(f"❌ Ошибка обновления: {response.text}")

# Использование в GitHub Actions
if __name__ == "__main__":
    dataset_id = os.getenv('POWERBI_DATASET_ID')
    access_token = os.getenv('POWERBI_ACCESS_TOKEN')
    
    if dataset_id and access_token:
        refresh_powerbi_dataset(dataset_id, access_token)
```

### 📊 Версионирование данных с DVC

```bash
# Установка DVC для версионирования больших датасетов
pip install dvc

# Инициализация DVC в проекте
dvc init

# Добавление больших файлов под версионирование DVC
dvc add data/raw/large_dataset.csv

# Commit метаданных DVC в Git
git add data/raw/large_dataset.csv.dvc .gitignore
git commit -m "📊 data: добавить большой датасет под DVC контроль"

# Настройка удаленного хранилища для данных
dvc remote add -d myremote s3://my-bucket/dvcstore
dvc push
```

---

## 🎓 Заключение

Этот Git workflow обеспечивает:

- **🔐 Безопасность**: защиту конфиденциальных данных
- **🤝 Сотрудничество**: эффективную совместную работу аналитиков
- **📊 Качество**: валидацию результатов и code review
- **🚀 Автоматизацию**: CI/CD для аналитических процессов
- **📚 Документирование**: полную трассировку изменений и методологии

Следуя этим практикам, вы сможете создавать надежные, масштабируемые и воспроизводимые аналитические проекты.

---

**💡 Помните**: Git в аналитике — это не только код, но и методология, данные и результаты. Относитесь к версионированию как к части научного процесса!