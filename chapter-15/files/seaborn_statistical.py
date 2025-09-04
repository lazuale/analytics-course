"""
🎨 Статистические визуализации с Seaborn - делаем данные красивыми!

Этот скрипт демонстрирует возможности Seaborn:
- Распределения и гистограммы
- Корреляционные матрицы
- Категориальные данные
- Парные графики
- Стилизация и цветовые палитры
"""

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

print("🌈 Изучаем статистические графики с Seaborn!")
print("=" * 55)

# Настройка Seaborn для красивых графиков
sns.set_style("whitegrid")
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (10, 6)

def generate_sample_data():
    """Генерация примера данных для демонстрации"""
    np.random.seed(42)
    
    n_samples = 500
    data = {
        'возраст': np.random.normal(35, 12, n_samples).astype(int),
        'доход': np.random.lognormal(10.5, 0.5, n_samples),
        'удовлетворенность': np.random.normal(7, 1.5, n_samples),
        'количество_покупок': np.random.poisson(8, n_samples),
    }
    
    # Добавляем категориальные переменные
    data['пол'] = np.random.choice(['М', 'Ж'], n_samples)
    data['сегмент'] = np.random.choice(['VIP', 'Обычный', 'Новый'], n_samples, p=[0.2, 0.6, 0.2])
    data['город'] = np.random.choice(['Москва', 'СПб', 'Екатеринбург', 'Казань'], n_samples)
    
    # Создаем взаимосвязи в данных
    data['доход'] = data['доход'] + (data['возраст'] - 25) * 500
    data['доход'] = np.where(data['пол'] == 'М', data['доход'] * 1.2, data['доход'])
    data['удовлетворенность'] = np.clip(data['удовлетворенность'], 1, 10)
    data['возраст'] = np.clip(data['возраст'], 18, 75)
    
    return pd.DataFrame(data)

def demo_distributions(data):
    """Демонстрация графиков распределений"""
    print("\n📊 1. Исследуем распределения данных")
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('📊 Анализ распределений клиентов', fontsize=16, y=0.98)
    
    # Гистограмма с плотностью
    sns.histplot(data=data, x='возраст', kde=True, bins=25, ax=axes[0,0])
    axes[0,0].set_title('📈 Распределение возраста')
    axes[0,0].set_xlabel('Возраст, лет')
    
    # Ящики с усами по сегментам
    sns.boxplot(data=data, x='сегмент', y='доход', ax=axes[0,1])
    axes[0,1].set_title('📦 Доходы по сегментам клиентов')
    axes[0,1].set_ylabel('Доход, тыс. руб.')
    
    # Violin plot - красивое распределение
    sns.violinplot(data=data, x='пол', y='удовлетворенность', ax=axes[1,0])
    axes[1,0].set_title('🎻 Удовлетворенность по полу')
    axes[1,0].set_ylabel('Удовлетворенность (1-10)')
    
    # Совокупное распределение
    sns.ecdfplot(data=data, x='количество_покупок', ax=axes[1,1])
    axes[1,1].set_title('📈 Кумулятивное распределение покупок')
    axes[1,1].set_xlabel('Количество покупок')
    
    plt.tight_layout()
    plt.show()
    
    print("✅ Распределения изучены!")

def demo_correlations(data):
    """Демонстрация корреляционных графиков"""
    print("\n🔗 2. Ищем связи в данных")
    
    # Выбираем числовые столбцы для анализа
    numeric_cols = ['возраст', 'доход', 'удовлетворенность', 'количество_покупок']
    correlation_data = data[numeric_cols]
    
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    fig.suptitle('🔍 Поиск взаимосвязей в данных', fontsize=16)
    
    # Корреляционная матрица
    correlation_matrix = correlation_data.corr()
    sns.heatmap(correlation_matrix, 
                annot=True,           # Показываем значения
                cmap='RdYlBu_r',     # Красиво-синяя палитра
                center=0,            # Центр на нуле
                square=True,         # Квадратные ячейки
                fmt='.2f',           # Формат чисел
                ax=axes[0])
    axes[0].set_title('🔥 Тепловая карта корреляций')
    
    # Диаграмма рассеивания с группировкой
    sns.scatterplot(data=data, x='возраст', y='доход', 
                    hue='сегмент', size='удовлетворенность',
                    sizes=(50, 200), alpha=0.7, ax=axes[1])
    axes[1].set_title('💫 Возраст vs Доход (по сегментам)')
    axes[1].set_xlabel('Возраст, лет')
    axes[1].set_ylabel('Доход, тыс. руб.')
    
    plt.tight_layout()
    plt.show()
    
    print("✅ Корреляции найдены!")

def demo_categorical_data(data):
    """Демонстрация работы с категориальными данными"""
    print("\n📋 3. Анализируем категориальные данные")
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('📋 Анализ категориальных переменных', fontsize=16, y=0.98)
    
    # Подсчет по категориям
    sns.countplot(data=data, x='город', ax=axes[0,0])
    axes[0,0].set_title('🏙️ Распределение клиентов по городам')
    axes[0,0].tick_params(axis='x', rotation=45)
    
    # Средние значения по категориям
    sns.barplot(data=data, x='сегмент', y='доход', ax=axes[0,1])
    axes[0,1].set_title('💰 Средний доход по сегментам')
    axes[0,1].set_ylabel('Средний доход, тыс. руб.')
    
    # Point plot для трендов
    sns.pointplot(data=data, x='город', y='удовлетворенность', 
                  hue='сегмент', ax=axes[1,0])
    axes[1,0].set_title('📈 Удовлетворенность: город × сегмент')
    axes[1,0].tick_params(axis='x', rotation=45)
    axes[1,0].legend(title='Сегмент', bbox_to_anchor=(1.05, 1), loc='upper left')
    
    # Swarm plot для детального просмотра
    sns.swarmplot(data=data.sample(100), x='пол', y='количество_покупок', 
                  hue='сегмент', ax=axes[1,1])
    axes[1,1].set_title('🐝 Детальный анализ покупок')
    axes[1,1].set_ylabel('Количество покупок')
    
    plt.tight_layout()
    plt.show()
    
    print("✅ Категориальные данные проанализированы!")

def demo_pairplot(data):
    """Демонстрация парных графиков"""
    print("\n🔍 4. Исследуем все связи сразу")
    
    # Выбираем подмножество данных для парного анализа
    sample_data = data.sample(200)  # Меньше точек для лучшей читаемости
    numeric_cols = ['возраст', 'доход', 'удовлетворенность', 'количество_покупок']
    
    # Создаем парные графики
    g = sns.pairplot(sample_data[numeric_cols + ['сегмент']], 
                     hue='сегмент',
                     diag_kind='kde',      # Плотности на диагонали
                     corner=True)          # Только нижний треугольник
    
    g.fig.suptitle('🔍 Исследование всех связей между переменными', 
                   y=1.02, fontsize=14)
    
    plt.show()
    
    print("✅ Все связи исследованы!")

def demo_style_gallery():
    """Демонстрация различных стилей Seaborn"""
    print("\n🎨 5. Галерея стилей Seaborn")
    
    # Создаем тестовые данные
    tips = sns.load_dataset("tips")
    
    # Различные стили Seaborn
    styles = ['darkgrid', 'whitegrid', 'dark', 'white', 'ticks']
    
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.suptitle('🎨 Галерея стилей Seaborn', fontsize=16)
    
    for i, style in enumerate(styles):
        row, col = i // 3, i % 3
        ax = axes[row, col]
        
        with sns.axes_style(style):
            sns.scatterplot(data=tips, x="total_bill", y="tip", 
                           hue="time", ax=ax)
            ax.set_title(f'Стиль: {style}')
    
    # Последний график - сравнение палитр
    ax = axes[1, 2]
    palettes = ['husl', 'Set2', 'viridis']
    for i, palette in enumerate(palettes):
        with sns.color_palette(palette):
            sns.scatterplot(data=tips.sample(50), x="total_bill", y="tip", 
                           label=f'Палитра {palette}', ax=ax)
    ax.set_title('Сравнение палитр')
    ax.legend()
    
    plt.tight_layout()
    plt.show()
    
    print("✅ Галерея стилей готова!")

def demo_advanced_plots(data):
    """Демонстрация продвинутых графиков"""
    print("\n🚀 6. Продвинутые техники визуализации")
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('🚀 Продвинутые статистические графики', fontsize=16, y=0.98)
    
    # Регрессионный анализ
    sns.regplot(data=data, x='возраст', y='доход', 
                scatter_kws={'alpha': 0.6}, ax=axes[0,0])
    axes[0,0].set_title('📈 Регрессионный анализ')
    axes[0,0].set_xlabel('Возраст, лет')
    axes[0,0].set_ylabel('Доход, тыс. руб.')
    
    # Совместное распределение
    sns.jointplot(data=data.sample(300), x='возраст', y='доход', 
                  kind='hex', height=6)
    plt.suptitle('🔍 Совместное распределение')
    
    # FacetGrid для множественного анализа
    sample_data = data.sample(200)
    g = sns.FacetGrid(sample_data, col='сегмент', hue='пол', height=4)
    g.map(sns.scatterplot, 'возраст', 'доход', alpha=0.7)
    g.add_legend(title='Пол')
    g.fig.suptitle('📊 Анализ по группам', y=1.02)
    
    plt.show()
    
    print("✅ Продвинутые графики освоены!")

# Функция для создания красивого отчета
def create_statistical_report(data):
    """Создание полного статистического отчета"""
    print("\n📋 7. Создаем итоговый статистический отчет")
    
    # Настройка профессионального стиля
    sns.set_style("whitegrid")
    sns.set_palette("Set2")
    
    # Создаем большую фигуру для отчета
    fig = plt.figure(figsize=(20, 16))
    fig.suptitle('📊 Полный статистический отчет по клиентам', 
                 fontsize=20, y=0.98)
    
    # 1. Основные распределения
    ax1 = plt.subplot(4, 3, 1)
    sns.histplot(data=data, x='возраст', kde=True, bins=20)
    plt.title('Возрастное распределение')
    
    ax2 = plt.subplot(4, 3, 2)
    sns.boxplot(data=data, x='сегмент', y='доход')
    plt.title('Доходы по сегментам')
    
    ax3 = plt.subplot(4, 3, 3)
    sns.countplot(data=data, x='город')
    plt.title('География клиентов')
    plt.xticks(rotation=45)
    
    # 2. Корреляционный анализ
    ax4 = plt.subplot(4, 3, (4, 6))  # Занимает 3 позиции
    numeric_cols = ['возраст', 'доход', 'удовлетворенность', 'количество_покупок']
    correlation_matrix = data[numeric_cols].corr()
    sns.heatmap(correlation_matrix, annot=True, cmap='RdYlBu_r', 
                center=0, square=True, fmt='.2f')
    plt.title('Корреляционная матрица')
    
    # 3. Детальный анализ по сегментам
    ax7 = plt.subplot(4, 3, 7)
    sns.violinplot(data=data, x='сегмент', y='удовлетворенность')
    plt.title('Удовлетворенность по сегментам')
    
    ax8 = plt.subplot(4, 3, 8)
    sns.barplot(data=data, x='пол', y='количество_покупок', hue='сегмент')
    plt.title('Активность покупок')
    
    ax9 = plt.subplot(4, 3, 9)
    pivot_data = data.pivot_table(values='доход', 
                                  index='город', 
                                  columns='сегмент', 
                                  aggfunc='mean')
    sns.heatmap(pivot_data, annot=True, fmt='.0f', cmap='YlOrRd')
    plt.title('Средние доходы: город × сегмент')
    
    # 4. Ключевые инсайты
    ax10 = plt.subplot(4, 3, (10, 12))
    ax10.axis('off')
    
    # Вычисляем статистики для инсайтов
    avg_age = data['возраст'].mean()
    avg_income = data['доход'].mean()
    vip_income = data[data['сегмент'] == 'VIP']['доход'].mean()
    regular_income = data[data['сегмент'] == 'Обычный']['доход'].mean()
    top_city = data['город'].value_counts().index[0]
    
    insights_text = f"""
    📊 КЛЮЧЕВЫЕ ИНСАЙТЫ:
    
    👥 Профиль клиентов:
    • Средний возраст: {avg_age:.0f} лет
    • Средний доход: {avg_income:,.0f} тыс. руб.
    • Самый популярный город: {top_city}
    
    💰 Сегментация:
    • VIP клиенты: {vip_income:,.0f} тыс. руб. (средний доход)
    • Обычные клиенты: {regular_income:,.0f} тыс. руб.
    • Разница в доходах: {((vip_income/regular_income - 1)*100):.0f}%
    
    🔍 Корреляции:
    • Возраст ↔ Доход: {data['возраст'].corr(data['доход']):.2f}
    • Доход ↔ Покупки: {data['доход'].corr(data['количество_покупок']):.2f}
    • Покупки ↔ Удовлетворенность: {data['количество_покупок'].corr(data['удовлетворенность']):.2f}
    
    📈 Рекомендации:
    • Фокус на VIP сегмент в {top_city}
    • Программы лояльности для молодых клиентов
    • Персонализация по доходам
    """
    
    ax10.text(0.05, 0.95, insights_text, transform=ax10.transAxes, 
              fontsize=11, verticalalignment='top',
              bbox=dict(boxstyle="round,pad=1", facecolor='lightblue', alpha=0.7))
    
    plt.tight_layout()
    plt.show()
    
    print("✅ Статистический отчет готов!")

# Основная функция для запуска всех демонстраций
def main():
    """Запуск всех демонстраций Seaborn"""
    print("🚀 Начинаем изучение Seaborn!")
    
    # Генерируем данные для анализа
    data = generate_sample_data()
    print(f"✅ Сгенерировано {len(data)} записей клиентов для анализа")
    
    # Запускаем все демонстрации
    demo_distributions(data)
    demo_correlations(data)
    demo_categorical_data(data)
    demo_pairplot(data)
    demo_style_gallery()
    demo_advanced_plots(data)
    create_statistical_report(data)
    
    print("\n🎉 Поздравляем! Вы освоили статистическую визуализацию!")
    print("📚 Следующий шаг: изучите dashboard_template.py")
    print("💡 Совет: используйте Seaborn для быстрого исследования данных!")

if __name__ == "__main__":
    main()