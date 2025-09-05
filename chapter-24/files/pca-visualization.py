"""
📊 PCA Visualization Template
Продвинутые визуализации для анализа главных компонент

Автор: Analytics Course
Глава: 24 - Мультивариантный анализ
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Настройка стиля
plt.style.use('default')
sns.set_palette("husl")

class PCAVisualizer:
    """
    Класс для создания продвинутых визуализаций PCA
    """
    
    def __init__(self, pca_model, components, feature_names, original_data=None):
        """
        Parameters:
        -----------
        pca_model : sklearn.decomposition.PCA
            Обученная модель PCA
        components : np.array
            Главные компоненты (результат transform)
        feature_names : list
            Названия исходных переменных
        original_data : pd.DataFrame
            Исходные данные (опционально)
        """
        self.pca_model = pca_model
        self.components = components
        self.feature_names = feature_names
        self.original_data = original_data
        self.loadings = pca_model.components_.T
        
    def create_biplot(self, pc1=0, pc2=1, save_path=None, figsize=(12, 8)):
        """
        Создает biplot - одновременное отображение объектов и переменных
        
        Parameters:
        -----------
        pc1, pc2 : int
            Номера компонент для отображения (0-indexed)
        """
        fig, ax = plt.subplots(figsize=figsize)
        
        # Настройки для масштабирования стрелок
        scale_factor = 3
        
        # Отображаем объекты (точки)
        scatter = ax.scatter(self.components[:, pc1], self.components[:, pc2], 
                           alpha=0.6, s=50, c='steelblue', edgecolors='white', linewidth=0.5)
        
        # Отображаем переменные (стрелки)
        for i, feature in enumerate(self.feature_names):
            # Координаты стрелки
            x_coord = self.loadings[i, pc1] * scale_factor
            y_coord = self.loadings[i, pc2] * scale_factor
            
            # Рисуем стрелку
            ax.arrow(0, 0, x_coord, y_coord, 
                    head_width=0.1, head_length=0.1, 
                    fc='red', ec='red', alpha=0.8, linewidth=2)
            
            # Подписываем переменную
            ax.text(x_coord * 1.1, y_coord * 1.1, feature, 
                   fontsize=10, ha='center', va='center',
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))
        
        # Настройка осей
        variance_pc1 = self.pca_model.explained_variance_ratio_[pc1]
        variance_pc2 = self.pca_model.explained_variance_ratio_[pc2]
        
        ax.set_xlabel(f'PC{pc1+1} ({variance_pc1:.1%} изменчивости)', fontsize=12, fontweight='bold')
        ax.set_ylabel(f'PC{pc2+1} ({variance_pc2:.1%} изменчивости)', fontsize=12, fontweight='bold')
        ax.set_title(f'📊 Biplot: PC{pc1+1} vs PC{pc2+1}', fontsize=14, fontweight='bold')
        
        # Добавляем сетку и центральные линии
        ax.grid(True, alpha=0.3)
        ax.axhline(y=0, color='black', linestyle='-', alpha=0.3)
        ax.axvline(x=0, color='black', linestyle='-', alpha=0.3)
        
        # Делаем оси равными для правильного отображения
        ax.set_aspect('equal', adjustable='box')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()
    
    def plot_clusters_in_pc_space(self, clusters, pc1=0, pc2=1, save_path=None):
        """
        Отображает кластеры в пространстве главных компонент
        """
        plt.figure(figsize=(12, 8))
        
        # Цветовая палитра для кластеров
        unique_clusters = np.unique(clusters)
        colors = plt.cm.Set1(np.linspace(0, 1, len(unique_clusters)))
        
        # Отображаем каждый кластер отдельно
        for i, cluster in enumerate(unique_clusters):
            mask = clusters == cluster
            plt.scatter(self.components[mask, pc1], self.components[mask, pc2],
                       c=[colors[i]], label=f'Кластер {cluster}', 
                       alpha=0.7, s=60, edgecolors='white', linewidth=0.5)
        
        # Настройка графика
        variance_pc1 = self.pca_model.explained_variance_ratio_[pc1]
        variance_pc2 = self.pca_model.explained_variance_ratio_[pc2]
        
        plt.xlabel(f'PC{pc1+1} ({variance_pc1:.1%})', fontsize=12, fontweight='bold')
        plt.ylabel(f'PC{pc2+1} ({variance_pc2:.1%})', fontsize=12, fontweight='bold')
        plt.title('🎯 Кластеры в пространстве главных компонент', fontsize=14, fontweight='bold')
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()
    
    def plot_variable_contributions(self, component_num=0, top_n=10, save_path=None):
        """
        Отображает вклад переменных в главную компоненту
        """
        # Получаем вклады переменных (квадраты нагрузок)
        contributions = self.loadings[:, component_num] ** 2
        
        # Создаем DataFrame для удобства
        contrib_df = pd.DataFrame({
            'Variable': self.feature_names,
            'Contribution': contributions,
            'Loading': self.loadings[:, component_num]
        }).sort_values('Contribution', ascending=True)
        
        # Берем топ переменных
        top_contrib = contrib_df.tail(top_n)
        
        # Создаем горизонтальный барplot
        plt.figure(figsize=(10, 6))
        colors = ['red' if x < 0 else 'blue' for x in top_contrib['Loading']]
        
        bars = plt.barh(range(len(top_contrib)), top_contrib['Contribution'], 
                       color=colors, alpha=0.7, edgecolor='white', linewidth=1)
        
        # Настройка осей
        plt.yticks(range(len(top_contrib)), top_contrib['Variable'])
        plt.xlabel('Вклад в компоненту (квадрат нагрузки)', fontsize=12, fontweight='bold')
        plt.title(f'📊 Вклад переменных в PC{component_num+1}', fontsize=14, fontweight='bold')
        
        # Добавляем значения на бары
        for i, (bar, loading) in enumerate(zip(bars, top_contrib['Loading'])):
            width = bar.get_width()
            plt.text(width + 0.01, bar.get_y() + bar.get_height()/2, 
                    f'{loading:.3f}', ha='left', va='center', fontweight='bold')
        
        plt.grid(True, alpha=0.3, axis='x')
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()
        
        return top_contrib
    
    def create_enhanced_scree_plot(self, save_path=None):
        """
        Улучшенный scree plot с дополнительной информацией
        """
        explained_var = self.pca_model.explained_variance_ratio_
        cumulative_var = np.cumsum(explained_var)
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Основной scree plot
        components = range(1, len(explained_var) + 1)
        ax1.plot(components, explained_var, 'bo-', linewidth=2, markersize=8)
        ax1.set_title('🔍 Scree Plot', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Номер компоненты')
        ax1.set_ylabel('Объясненная изменчивость')
        ax1.grid(True, alpha=0.3)
        
        # Выделяем "локоть"
        if len(explained_var) >= 3:
            # Простой способ найти локоть - максимальная разность вторых производных
            second_derivatives = np.diff(explained_var, 2)
            if len(second_derivatives) > 0:
                elbow_point = np.argmax(second_derivatives) + 2
                ax1.axvline(x=elbow_point, color='red', linestyle='--', 
                           label=f'Возможный "локоть" (PC{elbow_point})')
                ax1.legend()
        
        # Кумулятивная изменчивость
        ax2.plot(components, cumulative_var, 'ro-', linewidth=2, markersize=8)
        ax2.axhline(y=0.8, color='orange', linestyle='--', label='80%')
        ax2.axhline(y=0.85, color='red', linestyle='--', label='85%')
        ax2.axhline(y=0.9, color='darkred', linestyle='--', label='90%')
        ax2.set_title('📈 Кумулятивная изменчивость', fontsize=14, fontweight='bold')
        ax2.set_xlabel('Номер компоненты')
        ax2.set_ylabel('Кумулятивная изменчивость')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()
    
    def create_interactive_biplot(self, pc1=0, pc2=1):
        """
        Создает интерактивный biplot с помощью Plotly
        """
        # Данные для точек
        df_points = pd.DataFrame({
            f'PC{pc1+1}': self.components[:, pc1],
            f'PC{pc2+1}': self.components[:, pc2],
            'index': range(len(self.components))
        })
        
        # Создаем фигуру
        fig = go.Figure()
        
        # Добавляем точки
        fig.add_trace(go.Scatter(
            x=df_points[f'PC{pc1+1}'],
            y=df_points[f'PC{pc2+1}'],
            mode='markers',
            marker=dict(size=8, color='steelblue', opacity=0.7),
            text=df_points['index'],
            hovertemplate=f'<b>Объект %{{text}}</b><br>PC{pc1+1}: %{{x:.3f}}<br>PC{pc2+1}: %{{y:.3f}}<extra></extra>',
            name='Объекты'
        ))
        
        # Добавляем стрелки переменных
        scale_factor = 3
        for i, feature in enumerate(self.feature_names):
            x_start, y_start = 0, 0
            x_end = self.loadings[i, pc1] * scale_factor
            y_end = self.loadings[i, pc2] * scale_factor
            
            # Стрелка
            fig.add_annotation(
                x=x_end, y=y_end,
                ax=x_start, ay=y_start,
                xref='x', yref='y',
                axref='x', ayref='y',
                arrowhead=2,
                arrowsize=1,
                arrowwidth=2,
                arrowcolor='red'
            )
            
            # Подпись
            fig.add_annotation(
                x=x_end * 1.1, y=y_end * 1.1,
                text=feature,
                showarrow=False,
                font=dict(color='red', size=10)
            )
        
        # Настройка осей
        variance_pc1 = self.pca_model.explained_variance_ratio_[pc1]
        variance_pc2 = self.pca_model.explained_variance_ratio_[pc2]
        
        fig.update_layout(
            title=f'📊 Интерактивный Biplot: PC{pc1+1} vs PC{pc2+1}',
            xaxis_title=f'PC{pc1+1} ({variance_pc1:.1%})',
            yaxis_title=f'PC{pc2+1} ({variance_pc2:.1%})',
            showlegend=False,
            width=800,
            height=600
        )
        
        # Добавляем сетку
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
        
        # Добавляем центральные линии
        fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)
        fig.add_vline(x=0, line_dash="dash", line_color="gray", opacity=0.5)
        
        fig.show()
        
        return fig
    
    def create_dashboard(self, clusters=None, save_path=None):
        """
        Создает комплексный дашборд с результатами PCA
        """
        fig = plt.figure(figsize=(16, 12))
        
        # 1. Scree plot
        ax1 = plt.subplot(2, 3, 1)
        explained_var = self.pca_model.explained_variance_ratio_
        plt.plot(range(1, len(explained_var) + 1), explained_var, 'bo-')
        plt.title('🔍 Scree Plot')
        plt.xlabel('Компонента')
        plt.ylabel('Изменчивость')
        plt.grid(True, alpha=0.3)
        
        # 2. Кумулятивная изменчивость
        ax2 = plt.subplot(2, 3, 2)
        cumulative = np.cumsum(explained_var)
        plt.plot(range(1, len(cumulative) + 1), cumulative, 'ro-')
        plt.axhline(y=0.8, color='orange', linestyle='--', alpha=0.7)
        plt.axhline(y=0.9, color='red', linestyle='--', alpha=0.7)
        plt.title('📈 Кумулятивная изменчивость')
        plt.xlabel('Компонента')
        plt.ylabel('Кумулятивная доля')
        plt.grid(True, alpha=0.3)
        
        # 3. Biplot
        ax3 = plt.subplot(2, 3, 3)
        if clusters is not None:
            colors = plt.cm.Set1(clusters)
            plt.scatter(self.components[:, 0], self.components[:, 1], c=colors, alpha=0.7)
        else:
            plt.scatter(self.components[:, 0], self.components[:, 1], alpha=0.7)
        
        # Добавляем векторы переменных (упрощенно)
        scale = 2
        for i, feature in enumerate(self.feature_names[:5]):  # Показываем только первые 5
            plt.arrow(0, 0, self.loadings[i, 0]*scale, self.loadings[i, 1]*scale,
                     color='red', alpha=0.7, head_width=0.05)
        
        plt.title('📊 Biplot (PC1 vs PC2)')
        plt.xlabel(f'PC1 ({explained_var[0]:.1%})')
        plt.ylabel(f'PC2 ({explained_var[1]:.1%})')
        plt.grid(True, alpha=0.3)
        
        # 4. Heatmap нагрузок (первые 4 компоненты)
        ax4 = plt.subplot(2, 3, 4)
        n_comp_to_show = min(4, self.pca_model.n_components_)
        loadings_subset = self.loadings[:, :n_comp_to_show]
        
        sns.heatmap(loadings_subset, 
                   xticklabels=[f'PC{i+1}' for i in range(n_comp_to_show)],
                   yticklabels=self.feature_names,
                   annot=True, fmt='.2f', cmap='RdBu_r', center=0)
        plt.title('🔥 Матрица нагрузок')
        
        # 5. Вклад переменных в PC1
        ax5 = plt.subplot(2, 3, 5)
        contributions = self.loadings[:, 0] ** 2
        sorted_idx = np.argsort(contributions)[-8:]  # Топ 8
        
        plt.barh(range(len(sorted_idx)), contributions[sorted_idx])
        plt.yticks(range(len(sorted_idx)), [self.feature_names[i] for i in sorted_idx])
        plt.title('📊 Вклад в PC1')
        plt.xlabel('Вклад')
        
        # 6. Статистика
        ax6 = plt.subplot(2, 3, 6)
        ax6.axis('off')
        
        # Текстовая информация
        info_text = f"""
        📊 Статистика PCA:
        
        • Компонент: {self.pca_model.n_components_}
        • Объясненная изменчивость: {explained_var.sum():.1%}
        • Исходных переменных: {len(self.feature_names)}
        • Наблюдений: {len(self.components)}
        
        🎯 Топ-3 компоненты:
        • PC1: {explained_var[0]:.1%}
        • PC2: {explained_var[1]:.1%}
        • PC3: {explained_var[2]:.1%}
        """
        
        ax6.text(0.1, 0.5, info_text, fontsize=11, verticalalignment='center',
                bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()


def demo_visualization():
    """
    Демонстрация возможностей визуализации PCA
    """
    print("🎨 Демонстрация визуализации PCA")
    print("="*40)
    
    # Загружаем данные
    data = pd.read_csv('customers_data.csv', sep=';', decimal=',')
    features = data.drop('customer_id', axis=1)
    
    # Стандартизируем
    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features)
    
    # Применяем PCA
    pca = PCA(n_components=4)
    components = pca.fit_transform(features_scaled)
    
    # Кластеризация
    kmeans = KMeans(n_clusters=4, random_state=42)
    clusters = kmeans.fit_predict(components)
    
    # Создаем визуализатор
    visualizer = PCAVisualizer(pca, components, features.columns, data)
    
    print("\n1. 📊 Создание biplot...")
    visualizer.create_biplot()
    
    print("\n2. 🎯 Отображение кластеров...")
    visualizer.plot_clusters_in_pc_space(clusters)
    
    print("\n3. 📊 Вклад переменных...")
    visualizer.plot_variable_contributions(component_num=0)
    
    print("\n4. 🔍 Улучшенный scree plot...")
    visualizer.create_enhanced_scree_plot()
    
    print("\n5. 📱 Интерактивный biplot...")
    visualizer.create_interactive_biplot()
    
    print("\n6. 📊 Комплексный дашборд...")
    visualizer.create_dashboard(clusters)
    
    print("\n🎉 Демонстрация завершена!")
    
    return visualizer


if __name__ == "__main__":
    visualizer = demo_visualization()