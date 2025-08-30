# Установка и настройка программного обеспечения

## 📋 Требуемое ПО и минимальные версии

- **Microsoft Excel** — версия 2016 или новее  
- **Power BI Desktop** — последняя стабильная версия для Windows
- **Anaconda (Python 3)** — включает Jupyter Notebook
- **Git** — для управления версиями и публикации на GitHub
- **Текстовый редактор** — VS Code, Notepad++ или аналогичный

## 🖥 Установка ПО на Windows

### 1. Microsoft Excel
- Приобретите или активируйте подписку Microsoft 365
- Установите Excel через установщик Microsoft Office

### 2. Power BI Desktop
1. Откройте Microsoft Store (Windows)
2. Найдите **Power BI Desktop**
3. Нажмите **Установить**
4. После установки запустите программу и войдите в аккаунт (опционально)

### 3. Anaconda (Python 3)
1. Перейдите на сайт: https://www.anaconda.com/products/distribution
2. Выберите **Download** → **Windows** → **Python 3.x**
3. Запустите скачанный установщик
4. Отметьте опцию "Add Anaconda to my PATH environment variable"
5. Завершите установку
6. Запустите **Anaconda Navigator** и убедитесь, что **Jupyter Notebook** открывается

### 4. Git и GitHub
1. Перейдите на сайт: https://git-scm.com/
2. Скачайте **Git for Windows**
3. Запустите установщик, оставляя настройки по умолчанию
4. Проверьте установку в терминале:  
   ```bash
   git --version
   ```
5. Создайте аккаунт на https://github.com/
6. Настройте SSH-ключи или используйте HTTPS для клонирования

## 🖥 Установка ПО на MacOS/Linux

### 1. Microsoft Excel
- MacOS: Установите через App Store или Microsoft 365
- Linux: Используйте LibreOffice Calc (частично совместим)

### 2. Power BI Desktop
- MacOS/Linux: используйте **Power BI Online** через браузер или запустите через виртуальную машину

### 3. Anaconda (Python 3)
1. Скачайте установщик для MacOS/Linux с сайта Anaconda
2. Выполните в терминале:
   ```bash
   bash Anaconda3-*.sh
   ```
3. Добавьте Anaconda в PATH и активируйте:
   ```bash
   source ~/.bashrc
   conda init
   ```

### 4. Git
- MacOS: `brew install git` (если установлен Homebrew)
- Linux: `sudo apt-get install git` (Ubuntu/Debian) или `sudo yum install git` (RHEL/CentOS)

## 📂 Проверка установок

| Программа         | Команда для проверки         | Ожидаемый ответ          |
|-------------------|------------------------------|--------------------------|
| Excel             | —                            | Открытие приложения      |
| Power BI Desktop  | —                            | Открытие приложения      |
| conda             | `conda --version`            | `conda x.x.x`            |
| python            | `python --version`           | `Python 3.x.x`           |
| jupyter notebook  | `jupyter notebook --version` | `jupyter core x.x.x`     |
| git               | `git --version`              | `git version x.x.x`      |

---

**Теперь ваше окружение готово к прохождению курса!**

> Если возникают проблемы, создайте Issue в репозитории с описанием вашей системы и ошибки.