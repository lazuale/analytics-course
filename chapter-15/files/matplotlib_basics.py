"""
📊 Основы работы с Matplotlib - ваш первый шаг в мир визуализации!

Этот скрипт демонстрирует базовые возможности Matplotlib:
- Создание простых графиков
- Настройка оформления
- Работа с субплотами
- Сохранение в различных форматах
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

print("🎨 Изучаем основы Matplotlib!")
print("=" * 50)

# Настройка matplotlib для лучшего отображения
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 11
plt.rcParams['axes.grid'] = True
plt.rcParams['grid.alpha'] = 0.3

def demo_basic_plot():
    """Демонстрация создания базового графика"""
    print("\n📈 1. Создаем базовый линейный график")
    
    # Создаем тестовые данные
    x = np.linspace(0, 10, 100)
    y = np.sin(x)
    
    plt.figure(figsize=(10, 6))
    plt.plot(x, y, 'b-', linewidth=2, label='sin(x)')
    plt.plot(x, np.cos(x), 'r--', linewidth=2, label='cos(x)')
    
    # Настройка оформления
    plt.title('📈 Мой первый график в Matplotlib', fontsize=14, pad=20)
    plt.xlabel('X значения')
    plt.ylabel('Y значения')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Показываем график
    plt.tight_layout()
    plt.show()
    
    print("✅ Базовый график создан!")

def demo_business_chart():
    """Создание бизнес-графика с реальными данными"""
    print("\n💼 2. Создаем график продаж (бизнес-пример)")
    
    # Генерируем данные продаж
    months = ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн', 
              'Июл', 'Авг', 'Сен', 'Окт', 'Ноя', 'Дек']
    sales_2023 = [150, 180, 220, 240, 280, 260, 290, 310, 285, 340, 380, 420]
    sales_2024 = [180, 210, 250, 280, 320, 300, 340, 370, 350, 400, 450, 500]
    
    plt.figure(figsize=(12, 7))
    
    # Создаем столбчатую диаграмму
    x = np.arange(len(months))
    width = 0.35
    
    bars1 = plt.bar(x - width/2, sales_2023, width, label='2023 год', 
                    color='#1f77b4', alpha=0.8)
    bars2 = plt.bar(x + width/2, sales_2024, width, label='2024 год', 
                    color='#ff7f0e', alpha=0.8)
    
    # Добавляем значения на столбцы
    for bar in bars1:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 5,
                f'{height}К', ha='center', va='bottom')
    
    for bar in bars2:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 5,
                f'{height}К', ha='center', va='bottom')
    
    # Настройка оформления
    plt.title('📊 Сравнение продаж по месяцам', fontsize=16, pad=20)
    plt.xlabel('Месяц')
    plt.ylabel('Продажи, тыс. руб.')
    plt.xticks(x, months)
    plt.legend()
    plt.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.show()
    
    print("✅ Бизнес-график готов!")

def demo_subplots():
    """Демонстрация работы с несколькими графиками"""
    print("\n🎛️ 3. Создаем панель из нескольких графиков")
    
    # Генерируем тестовые данные
    x = np.linspace(0, 10, 100)
    
    # Создаем фигуру с субплотами
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('🎨 Галерея различных типов графиков', fontsize=16)
    
    # График 1: Линейный
    ax1.plot(x, np.sin(x), 'b-', linewidth=2)
    ax1.set_title('📈 Линейный график')
    ax1.grid(True, alpha=0.3)
    
    # График 2: Столбчатый
    categories = ['A', 'B', 'C', 'D', 'E']
    values = [23, 45, 56, 78, 32]
    ax2.bar(categories, values, color=['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#ff99cc'])
    ax2.set_title('📊 Столбчатая диаграмма')
    
    # График 3: Рассеивание  
    np.random.seed(42)
    x_scatter = np.random.randn(100)
    y_scatter = 2 * x_scatter + np.random.randn(100)
    ax3.scatter(x_scatter, y_scatter, alpha=0.7, color='green')
    ax3.set_title('💫 Диаграмма рассеивания')
    ax3.grid(True, alpha=0.3)
    
    # График 4: Круговая диаграмма
    sizes = [30, 25, 20, 15, 10]
    labels = ['Категория A', 'Категория B', 'Категория C', 'Категория D', 'Категория E']
    colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#ff99cc']
    ax4.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    ax4.set_title('🥧 Круговая диаграмма')
    
    plt.tight_layout()
    plt.show()
    
    print("✅ Панель графиков создана!")

def demo_styling():
    """Демонстрация различных стилей оформления"""
    print("\n🎨 4. Экспериментируем со стилями")
    
    # Данные для демонстрации
    x = np.linspace(0, 10, 50)
    y1 = np.sin(x)
    y2 = np.cos(x)
    
    # Различные стили matplotlib
    styles = ['default', 'seaborn-v0_8', 'ggplot', 'bmh']
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('🎨 Галерея стилей Matplotlib', fontsize=16)
    
    for i, style in enumerate(styles):
        ax = axes[i//2, i%2]
        
        with plt.style.context(style):
            ax.plot(x, y1, linewidth=2, label='sin(x)')
            ax.plot(x, y2, linewidth=2, label='cos(x)')
            ax.set_title(f'Стиль: {style}')
            ax.legend()
            ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()
    
    print("✅ Галерея стилей готова!")

def demo_save_formats():
    """Демонстрация сохранения в различных форматах"""
    print("\n💾 5. Сохраняем графики в разных форматах")
    
    # Создаем красивый график для сохранения
    plt.figure(figsize=(12, 8))
    
    x = np.linspace(0, 4*np.pi, 100)
    y = np.sin(x) * np.exp(-x/10)
    
    plt.plot(x, y, 'b-', linewidth=3, label='Затухающая синусоида')
    plt.fill_between(x, 0, y, alpha=0.3, color='blue')
    
    plt.title('📈 График для демонстрации сохранения', fontsize=16, pad=20)
    plt.xlabel('X значения')
    plt.ylabel('Y значения')
    plt.legend(fontsize=12)
    plt.grid(True, alpha=0.3)
    
    # Сохраняем в разных форматах
    formats = {
        'PNG': {'dpi': 300, 'bbox_inches': 'tight'},
        'PDF': {'bbox_inches': 'tight'},
        'SVG': {'bbox_inches': 'tight'}
    }
    
    for format_name, kwargs in formats.items():
        filename = f'demo_graph.{format_name.lower()}'
        plt.savefig(filename, **kwargs)
        print(f"  ✅ Сохранено: {filename}")
    
    plt.show()
    print("✅ Все форматы сохранены!")

def create_professional_template():
    """Шаблон профессионального графика"""
    print("\n🏆 6. Создаем профессиональный шаблон")
    
    # Настройка профессионального стиля
    plt.style.use('seaborn-v0_8-whitegrid')
    
    # Корпоративные цвета
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
    
    # Данные для демонстрации
    quarters = ['Q1 2023', 'Q2 2023', 'Q3 2023', 'Q4 2023', 'Q1 2024']
    revenue = [1200, 1350, 1180, 1650, 1420]
    profit = [180, 220, 150, 280, 240]
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Создаем комбинированный график
    x = np.arange(len(quarters))
    width = 0.35
    
    bars = ax.bar(x, revenue, width, label='Выручка', color=colors[0], alpha=0.8)
    line = ax.plot(x, profit, color=colors[1], marker='o', linewidth=3, 
                   markersize=8, label='Прибыль')
    
    # Добавляем значения на столбцы
    for i, (bar, profit_val) in enumerate(zip(bars, profit)):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 20,
                f'{height}М', ha='center', va='bottom', fontweight='bold')
        ax.text(i, profit_val + 30, f'{profit_val}М', ha='center', 
                va='bottom', fontweight='bold', color=colors[1])
    
    # Профессиональное оформление
    ax.set_title('📊 Финансовые показатели компании', 
                fontsize=18, fontweight='bold', pad=30)
    ax.set_xlabel('Квартал', fontsize=12)
    ax.set_ylabel('Млн рублей', fontsize=12)
    ax.set_xticks(x)
    ax.set_xticklabels(quarters)
    
    # Настройка легенды
    ax.legend(loc='upper left', fontsize=12, frameon=True, shadow=True)
    
    # Добавляем сетку
    ax.grid(True, alpha=0.3, linestyle='-', linewidth=0.5)
    ax.set_axisbelow(True)
    
    # Убираем верхнюю и правую рамки
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    plt.tight_layout()
    plt.show()
    
    print("✅ Профессиональный шаблон готов!")

# Запускаем все демонстрации
if __name__ == "__main__":
    print("🚀 Начинаем изучение Matplotlib!")
    
    demo_basic_plot()
    demo_business_chart() 
    demo_subplots()
    demo_styling()
    demo_save_formats()
    create_professional_template()
    
    print("\n🎉 Поздравляем! Вы изучили основы Matplotlib!")
    print("📚 Следующий шаг: изучите seaborn_statistical.py")
    print("💡 Совет: экспериментируйте с параметрами графиков!")