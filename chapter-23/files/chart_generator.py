"""
📊 Автоматизированный генератор стандартных графиков
для аналитических презентаций согласно дизайн-системе
"""

import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple, Union
from datetime import datetime, timedelta
import yaml

class AnalyticsDesignSystem:
    """
    Класс с настройками корпоративной дизайн-системы для аналитики
    """
    
    def __init__(self, config_file: Optional[str] = None):
        """
        Инициализация дизайн-системы
        
        Args:
            config_file: Путь к YAML файлу с конфигурацией
        """
        if config_file:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            self.colors = config['visualization']['colors']
        else:
            # Стандартная палитра
            self.colors = {
                'primary': '#1E3A8A',     # Brand Blue
                'success': '#10B981',     # Success Green  
                'warning': '#F59E0B',     # Warning Yellow
                'danger': '#EF4444',      # Alert Red
                'info': '#8B5CF6',        # Info Purple
                'neutral': '#6B7280',     # Neutral Gray
                'background': '#FFFFFF'   # White Background
            }
        
        # Расширенная палитра для многокатегориальных данных
        self.color_palette = [
            self.colors['primary'],
            self.colors['success'], 
            self.colors['warning'],
            self.colors['danger'],
            self.colors['info'],
            '#06B6D4',  # Cyan
            '#84CC16',  # Lime
            '#F97316'   # Orange
        ]
        
        # Градации основного цвета
        self.blue_shades = [
            '#DBEAFE',  # Blue 100 (lightest)
            '#BFDBFE',  # Blue 200
            '#93C5FD',  # Blue 300  
            '#60A5FA',  # Blue 400
            '#3B82F6',  # Blue 500
            '#2563EB',  # Blue 600
            '#1D4ED8',  # Blue 700
            '#1E3A8A'   # Blue 800 (darkest)
        ]
        
        # Настройки шрифтов
        self.fonts = {
            'title': {'size': 16, 'weight': 'bold', 'family': 'Arial'},
            'subtitle': {'size': 14, 'weight': 'normal', 'family': 'Arial'},
            'axis_labels': {'size': 12, 'weight': 'normal', 'family': 'Arial'},
            'tick_labels': {'size': 10, 'weight': 'normal', 'family': 'Arial'},
            'kpi_large': {'size': 36, 'weight': 'bold', 'family': 'Arial Black'},
            'kpi_medium': {'size': 24, 'weight': 'bold', 'family': 'Arial'}
        }
        
        # Настройка matplotlib стиля
        self._setup_matplotlib_style()
    
    def _setup_matplotlib_style(self):
        """Настройка глобального стиля matplotlib"""
        plt.style.use('default')
        
        plt.rcParams.update({
            'figure.figsize': (12, 8),
            'figure.facecolor': self.colors['background'],
            'axes.facecolor': self.colors['background'],
            'axes.edgecolor': '#E5E7EB',
            'axes.labelcolor': '#374151',
            'text.color': '#374151',
            'xtick.color': '#374151',
            'ytick.color': '#374151',
            'grid.color': '#F3F4F6',
            'grid.alpha': 0.7,
            'font.size': 12,
            'font.family': 'sans-serif',
            'axes.spines.top': False,
            'axes.spines.right': False,
            'axes.grid': True,
            'axes.axisbelow': True
        })

class ChartGenerator:
    """Генератор стандартизированных графиков"""
    
    def __init__(self, design_system: Optional[AnalyticsDesignSystem] = None):
        """
        Инициализация генератора
        
        Args:
            design_system: Экземпляр дизайн-системы
        """
        self.ds = design_system or AnalyticsDesignSystem()
    
    def create_kpi_card(self, 
                       value: Union[int, float], 
                       title: str,
                       previous_value: Optional[Union[int, float]] = None,
                       format_type: str = 'number',
                       target_value: Optional[Union[int, float]] = None,
                       trend_data: Optional[List[float]] = None) -> go.Figure:
        """
        Создание интерактивной KPI карточки
        
        Args:
            value: Текущее значение метрики
            title: Название метрики
            previous_value: Предыдущее значение для сравнения
            format_type: Тип форматирования ('number', 'currency', 'percent')
            target_value: Целевое значение
            trend_data: Данные для мини-графика тренда
            
        Returns:
            go.Figure: Plotly график KPI карточки
        """
        
        fig = go.Figure()
        
        # Форматирование значения
        if format_type == 'currency':
            formatted_value = f"₽{value:,.0f}"
            formatted_previous = f"₽{previous_value:,.0f}" if previous_value else None
        elif format_type == 'percent':
            formatted_value = f"{value:.1f}%"
            formatted_previous = f"{previous_value:.1f}%" if previous_value else None
        else:
            formatted_value = f"{value:,.0f}"
            formatted_previous = f"{previous_value:,.0f}" if previous_value else None
        
        # Основное значение KPI
        fig.add_annotation(
            text=formatted_value,
            x=0.25, y=0.7,
            font=dict(
                size=self.ds.fonts['kpi_large']['size'],
                color=self.ds.colors['primary'],
                family=self.ds.fonts['kpi_large']['family']
            ),
            showarrow=False,
            xanchor='center'
        )
        
        # Название метрики
        fig.add_annotation(
            text=title,
            x=0.25, y=0.4,
            font=dict(
                size=self.ds.fonts['subtitle']['size'],
                color='#374151',
                family=self.ds.fonts['subtitle']['family']
            ),
            showarrow=False,
            xanchor='center'
        )
        
        # Сравнение с предыдущим периодом
        if previous_value is not None:
            change = value - previous_value
            change_pct = (change / previous_value) * 100 if previous_value != 0 else 0
            
            if change > 0:
                arrow = "▲"
                color = self.ds.colors['success']
            elif change < 0:
                arrow = "▼" 
                color = self.ds.colors['danger']
            else:
                arrow = "■"
                color = self.ds.colors['neutral']
            
            change_text = f"{arrow} {change_pct:+.1f}%"
            
            fig.add_annotation(
                text=change_text,
                x=0.25, y=0.2,
                font=dict(
                    size=self.ds.fonts['axis_labels']['size'],
                    color=color,
                    family=self.ds.fonts['axis_labels']['family']
                ),
                showarrow=False,
                xanchor='center'
            )
        
        # Мини-график тренда (если предоставлены данные)
        if trend_data and len(trend_data) > 1:
            x_trend = list(range(len(trend_data)))
            
            # Нормализация для отображения в правой части карточки
            y_min, y_max = min(trend_data), max(trend_data)
            y_range = y_max - y_min if y_max != y_min else 1
            y_normalized = [(y - y_min) / y_range * 0.6 + 0.2 for y in trend_data]
            x_normalized = [0.5 + (x / (len(trend_data) - 1)) * 0.45 for x in x_trend]
            
            fig.add_trace(go.Scatter(
                x=x_normalized,
                y=y_normalized,
                mode='lines',
                line=dict(
                    color=self.ds.colors['primary'],
                    width=2
                ),
                showlegend=False,
                hoverinfo='skip'
            ))
            
            # Заливка под линией
            fig.add_trace(go.Scatter(
                x=x_normalized + [x_normalized[-1], x_normalized[0]],
                y=y_normalized + [0.2, 0.2],
                fill='toself',
                fillcolor=f"rgba(30, 58, 138, 0.1)",
                line=dict(color='rgba(0,0,0,0)'),
                showlegend=False,
                hoverinfo='skip'
            ))
        
        # Целевое значение (индикатор прогресса)
        if target_value is not None:
            progress = min(value / target_value, 1.0) if target_value > 0 else 0
            
            # Полоса прогресса
            fig.add_shape(
                type="rect",
                x0=0.1, y0=0.05,
                x1=0.9, y1=0.1,
                fillcolor='#E5E7EB',
                line=dict(width=0)
            )
            
            fig.add_shape(
                type="rect", 
                x0=0.1, y0=0.05,
                x1=0.1 + progress * 0.8, y1=0.1,
                fillcolor=self.ds.colors['success'] if progress >= 1.0 else self.ds.colors['warning'],
                line=dict(width=0)
            )
            
            # Подпись цели
            fig.add_annotation(
                text=f"Цель: {target_value:,.0f} ({progress:.0%})",
                x=0.5, y=0.0,
                font=dict(size=10, color='#6B7280'),
                showarrow=False,
                xanchor='center'
            )
        
        # Настройки макета
        fig.update_layout(
            width=280, height=160,
            paper_bgcolor=self.ds.colors['background'],
            plot_bgcolor=self.ds.colors['background'],
            margin=dict(t=10, b=10, l=10, r=10),
            xaxis=dict(visible=False, range=[0, 1]),
            yaxis=dict(visible=False, range=[0, 1])
        )
        
        return fig
    
    def create_trend_chart(self, 
                          data: pd.DataFrame,
                          x_column: str,
                          y_column: str,
                          title: str,
                          y_axis_label: str = "",
                          show_trend_line: bool = True,
                          highlight_periods: Optional[List[Dict]] = None) -> go.Figure:
        """
        Создание графика трендов с дополнительными возможностями
        
        Args:
            data: DataFrame с данными
            x_column: Название колонки для оси X
            y_column: Название колонки для оси Y  
            title: Заголовок графика
            y_axis_label: Подпись оси Y
            show_trend_line: Показать линию тренда
            highlight_periods: Список периодов для выделения
            
        Returns:
            go.Figure: Plotly график
        """
        
        fig = go.Figure()
        
        # Основная линия данных
        fig.add_trace(go.Scatter(
            x=data[x_column],
            y=data[y_column],
            mode='lines+markers',
            line=dict(
                color=self.ds.colors['primary'],
                width=3
            ),
            marker=dict(
                color=self.ds.colors['primary'],
                size=6,
                symbol='circle'
            ),
            name='Факт',
            hovertemplate='<b>%{x}</b><br>%{y:,.0f}<extra></extra>'
        ))
        
        # Заливка под графиком
        fig.add_trace(go.Scatter(
            x=data[x_column],
            y=data[y_column],
            fill='tozeroy',
            fillcolor=f"rgba(30, 58, 138, 0.1)",
            line=dict(color='rgba(0,0,0,0)'),
            showlegend=False,
            hoverinfo='skip'
        ))
        
        # Линия тренда
        if show_trend_line and len(data) > 2:
            # Простая линейная регрессия
            x_numeric = range(len(data))
            y_values = data[y_column].values
            
            # Вычисление коэффициентов
            n = len(x_numeric)
            sum_x = sum(x_numeric)
            sum_y = sum(y_values)
            sum_xy = sum(x * y for x, y in zip(x_numeric, y_values))
            sum_x2 = sum(x * x for x in x_numeric)
            
            # Коэффициенты линейной регрессии
            slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x * sum_x)
            intercept = (sum_y - slope * sum_x) / n
            
            # Прогнозные значения
            trend_y = [slope * x + intercept for x in x_numeric]
            
            fig.add_trace(go.Scatter(
                x=data[x_column],
                y=trend_y,
                mode='lines',
                line=dict(
                    color=self.ds.colors['neutral'],
                    width=2,
                    dash='dash'
                ),
                name='Тренд',
                hovertemplate='<b>Тренд</b><br>%{y:,.0f}<extra></extra>'
            ))
        
        # Выделение специальных периодов
        if highlight_periods:
            for period in highlight_periods:
                start_date = period.get('start')
                end_date = period.get('end')
                color = period.get('color', self.ds.colors['warning'])
                label = period.get('label', 'Особый период')
                
                fig.add_vrect(
                    x0=start_date, x1=end_date,
                    fillcolor=color,
                    opacity=0.2,
                    line_width=0,
                    annotation_text=label,
                    annotation_position="top left"
                )
        
        # Настройки макета
        fig.update_layout(
            title=dict(
                text=title,
                font=dict(
                    size=self.ds.fonts['title']['size'],
                    color='#374151',
                    family=self.ds.fonts['title']['family']
                ),
                x=0.02
            ),
            paper_bgcolor=self.ds.colors['background'],
            plot_bgcolor=self.ds.colors['background'],
            font=dict(color='#374151', family='Arial'),
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right", 
                x=1
            ),
            margin=dict(t=80, b=60, l=80, r=40),
            height=400,
            hovermode='x unified'
        )
        
        # Настройки осей
        fig.update_xaxes(
            gridcolor='#F3F4F6',
            gridwidth=1,
            showline=True,
            linecolor='#E5E7EB',
            linewidth=1,
            title=dict(
                text=x_column,
                font=dict(size=self.ds.fonts['axis_labels']['size'])
            )
        )
        
        fig.update_yaxes(
            gridcolor='#F3F4F6', 
            gridwidth=1,
            showline=True,
            linecolor='#E5E7EB',
            linewidth=1,
            title=dict(
                text=y_axis_label or y_column,
                font=dict(size=self.ds.fonts['axis_labels']['size'])
            )
        )
        
        return fig
    
    def create_category_comparison(self,
                                 data: pd.DataFrame,
                                 category_column: str,
                                 value_column: str,
                                 title: str,
                                 sort_by_value: bool = True,
                                 max_categories: int = 10) -> go.Figure:
        """
        Создание графика сравнения категорий
        
        Args:
            data: DataFrame с данными
            category_column: Колонка с категориями
            value_column: Колонка со значениями
            title: Заголовок графика
            sort_by_value: Сортировать по значению
            max_categories: Максимальное количество категорий
            
        Returns:
            go.Figure: Plotly график
        """
        
        # Подготовка данных
        df = data.copy()
        
        if sort_by_value:
            df = df.sort_values(value_column, ascending=False)
        
        # Ограничение количества категорий
        if len(df) > max_categories:
            top_categories = df.head(max_categories - 1)
            others_value = df.tail(len(df) - max_categories + 1)[value_column].sum()
            others_row = pd.DataFrame({
                category_column: ['Прочие'],
                value_column: [others_value]
            })
            df = pd.concat([top_categories, others_row], ignore_index=True)
        
        # Выбор цветов
        colors = []
        for i, value in enumerate(df[value_column]):
            if i < len(self.ds.color_palette):
                colors.append(self.ds.color_palette[i])
            else:
                colors.append(self.ds.colors['neutral'])
        
        fig = go.Figure()
        
        # Столбчатая диаграмма
        fig.add_trace(go.Bar(
            x=df[category_column],
            y=df[value_column],
            marker=dict(
                color=colors,
                line=dict(color='rgba(0,0,0,0.1)', width=1)
            ),
            text=df[value_column],
            texttemplate='%{text:,.0f}',
            textposition='outside',
            textfont=dict(
                size=self.ds.fonts['axis_labels']['size'],
                color='#374151'
            ),
            hovertemplate='<b>%{x}</b><br>%{y:,.0f}<extra></extra>'
        ))
        
        # Настройки макета
        fig.update_layout(
            title=dict(
                text=title,
                font=dict(
                    size=self.ds.fonts['title']['size'],
                    color='#374151',
                    family=self.ds.fonts['title']['family']
                ),
                x=0.02
            ),
            paper_bgcolor=self.ds.colors['background'],
            plot_bgcolor=self.ds.colors['background'],
            font=dict(color='#374151', family='Arial'),
            showlegend=False,
            margin=dict(t=80, b=100, l=80, r=40),
            height=400
        )
        
        # Настройки осей
        fig.update_xaxes(
            gridcolor='#F3F4F6',
            showgrid=False,
            showline=True,
            linecolor='#E5E7EB',
            linewidth=1,
            tickangle=45 if len(df) > 5 else 0
        )
        
        fig.update_yaxes(
            gridcolor='#F3F4F6',
            gridwidth=1,
            showline=True,
            linecolor='#E5E7EB',
            linewidth=1,
            title=dict(
                text=value_column,
                font=dict(size=self.ds.fonts['axis_labels']['size'])
            )
        )
        
        return fig
    
    def create_dashboard_layout(self,
                              kpi_data: List[Dict],
                              trend_data: pd.DataFrame,
                              category_data: pd.DataFrame,
                              title: str = "Аналитический дашборд") -> go.Figure:
        """
        Создание компоновки дашборда с KPI, трендами и категориями
        
        Args:
            kpi_data: Список словарей с данными KPI
            trend_data: Данные для графика трендов
            category_data: Данные для сравнения категорий
            title: Заголовок дашборда
            
        Returns:
            go.Figure: Комплексный дашборд
        """
        
        # Создание субплотов
        fig = make_subplots(
            rows=3, cols=len(kpi_data),
            subplot_titles=[kpi['title'] for kpi in kpi_data] + ['Динамика', 'Сравнение категорий'],
            specs=[[{'type': 'indicator'}] * len(kpi_data),
                   [{'colspan': len(kpi_data), 'type': 'scatter'}, None] + [None] * (len(kpi_data) - 2),
                   [{'colspan': len(kpi_data), 'type': 'bar'}, None] + [None] * (len(kpi_data) - 2)],
            row_heights=[0.3, 0.35, 0.35],
            vertical_spacing=0.08
        )
        
        # Добавление KPI индикаторов
        for i, kpi in enumerate(kpi_data):
            delta_dict = {}
            if 'previous_value' in kpi and kpi['previous_value'] is not None:
                delta_dict = {
                    'reference': kpi['previous_value'],
                    'increasing': {'color': self.ds.colors['success']},
                    'decreasing': {'color': self.ds.colors['danger']},
                    'relative': True
                }
            
            fig.add_trace(go.Indicator(
                mode="number+delta",
                value=kpi['value'],
                title={'text': kpi['title']},
                number={'font': {'size': 36, 'color': self.ds.colors['primary']}},
                delta=delta_dict
            ), row=1, col=i+1)
        
        # График трендов
        fig.add_trace(go.Scatter(
            x=trend_data.iloc[:, 0],
            y=trend_data.iloc[:, 1],
            mode='lines+markers',
            line=dict(color=self.ds.colors['primary'], width=3),
            marker=dict(color=self.ds.colors['primary'], size=6),
            name='Тренд'
        ), row=2, col=1)
        
        # График категорий
        fig.add_trace(go.Bar(
            x=category_data.iloc[:, 0],
            y=category_data.iloc[:, 1],
            marker=dict(color=self.ds.color_palette[:len(category_data)]),
            name='Категории'
        ), row=3, col=1)
        
        # Общие настройки макета
        fig.update_layout(
            title=dict(
                text=title,
                font=dict(size=20, color='#374151', family='Arial'),
                x=0.5,
                xanchor='center'
            ),
            paper_bgcolor=self.ds.colors['background'],
            plot_bgcolor=self.ds.colors['background'],
            font=dict(color='#374151', family='Arial'),
            showlegend=False,
            height=800,
            margin=dict(t=100, b=60, l=60, r=60)
        )
        
        return fig

# Пример использования
def main():
    """Демонстрация возможностей генератора графиков"""
    
    print("📊 Демонстрация генератора стандартных графиков...")
    
    # Инициализация дизайн-системы с конфигурацией
    try:
        design_system = AnalyticsDesignSystem('config.yaml')
        print("✅ Дизайн-система загружена из config.yaml")
    except:
        design_system = AnalyticsDesignSystem()
        print("✅ Использована стандартная дизайн-система")
    
    chart_gen = ChartGenerator(design_system)
    
    # 1. KPI карточка
    print("📈 Создание KPI карточки...")
    
    kpi_fig = chart_gen.create_kpi_card(
        value=1234567,
        title="Общая выручка",
        previous_value=1100000,
        format_type='currency',
        target_value=1500000,
        trend_data=[950000, 1050000, 1100000, 1150000, 1234567]
    )
    
    kpi_fig.write_html("kpi_example.html")
    print("  Сохранено: kpi_example.html")
    
    # 2. График трендов
    print("📈 Создание графика трендов...")
    
    # Генерация данных для демонстрации
    dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='M')
    values = 100000 + np.cumsum(np.random.normal(5000, 10000, len(dates)))
    
    trend_data = pd.DataFrame({
        'Месяц': dates,
        'Выручка': values
    })
    
    # Выделение особых периодов
    highlight_periods = [
        {
            'start': '2024-11-01',
            'end': '2024-12-31', 
            'color': design_system.colors['success'],
            'label': 'Высокий сезон'
        }
    ]
    
    trend_fig = chart_gen.create_trend_chart(
        data=trend_data,
        x_column='Месяц',
        y_column='Выручка', 
        title="Динамика выручки по месяцам",
        y_axis_label="Выручка, руб",
        show_trend_line=True,
        highlight_periods=highlight_periods
    )
    
    trend_fig.write_html("trend_example.html")
    print("  Сохранено: trend_example.html")
    
    # 3. Сравнение категорий
    print("📊 Создание графика категорий...")
    
    category_data = pd.DataFrame({
        'Категория': ['Электроника', 'Одежда', 'Дом и сад', 'Спорт', 'Красота', 
                      'Книги', 'Игрушки', 'Авто', 'Здоровье', 'Прочее'],
        'Выручка': [450000, 380000, 280000, 250000, 180000, 
                   150000, 120000, 100000, 80000, 60000]
    })
    
    category_fig = chart_gen.create_category_comparison(
        data=category_data,
        category_column='Категория',
        value_column='Выручка',
        title="Выручка по категориям товаров",
        sort_by_value=True,
        max_categories=8
    )
    
    category_fig.write_html("categories_example.html")
    print("  Сохранено: categories_example.html")
    
    print(f"""
🎉 Демонстрация завершена!

📁 Созданные файлы:
- kpi_example.html — пример KPI карточки
- trend_example.html — график трендов с выделенными периодами  
- categories_example.html — сравнение категорий

🎨 Использованная дизайн-система:
- Корпоративные цвета: {design_system.colors['primary']}
- Стандартные шрифты и размеры
- Единообразные стили и отступы
""")

if __name__ == "__main__":
    main()