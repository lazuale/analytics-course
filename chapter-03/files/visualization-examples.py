# Примеры кода визуализаций для Главы 3

"""
Этот файл содержит вспомогательные функции и шаблоны для создания различных типов графиков,
используемых в Главе 3: визуализация для начинающих.
Используйте в Jupyter Notebook или Python-скриптах.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

sns.set_style("whitegrid")


def plot_bar_chart(data, x_col, y_col, title="Столбчатая диаграмма", color='steelblue'):
    """Создаёт простую столбчатую диаграмму"""
    plt.figure(figsize=(8, 5))
    sns.barplot(x=x_col, y=y_col, data=data, color=color)
    plt.title(title)
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def plot_line_chart(data, x_col, y_cols, title="Линейный график", palette='tab10'):
    """Создаёт линейный график для нескольких показателей"""
    plt.figure(figsize=(10, 6))
    data.plot(x=x_col, y=y_cols, marker='o', colormap=palette)
    plt.title(title)
    plt.xlabel(x_col)
    plt.ylabel('Значение')
    plt.legend(title='Показатели', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def plot_scatter(data, x_col, y_col, size_col=None, title="Точечная диаграмма", hue=None):
    """Создаёт точечную диаграмму, опционально с размером и цветовым кодом"""
    plt.figure(figsize=(8, 6))
    sns.scatterplot(x=x_col, y=y_col, size=size_col, hue=hue, data=data, palette='viridis', alpha=0.7)
    plt.title(title)
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    if size_col:
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()


def plot_heatmap(pivot_data, title="Тепловая карта", cmap='YlOrRd'):
    """Создаёт тепловую карту на основе сводной таблицы"""
    plt.figure(figsize=(10, 6))
    sns.heatmap(pivot_data, annot=True, fmt='d', cmap=cmap, cbar_kws={'label': 'Значение'})
    plt.title(title)
    plt.xlabel('Час')
    plt.ylabel('День')
    plt.tight_layout()
    plt.show()