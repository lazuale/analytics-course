"""
🚀 Comprehensive Multivariate Analysis
Комплексный мультивариантный анализ: PCA + Факторный анализ + Бизнес-инсайты

Автор: Analytics Course
Глава: 24 - Мультивариантный анализ
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA, FactorAnalysis
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import warnings
warnings.filterwarnings('ignore')

# Настройка стиля
plt.style.use('default')
sns.set_palette("husl")

class ComprehensiveAnalyzer:
    """
    Комплексный анализатор для полного цикла мультивариантного анализа
    """
    
    def __init__(self):
        self.products_data = None
        self.sales_data = None
        self.merged_data = None
        self.features = None
        self.features_scaled = None
        self.pca_model = None
        self.fa_model = None
        self.pca_components = None
        self.clusters = None
        self.feature_names = None
        
    def load_and_merge_data(self, products_file='products_analysis.csv', 
                           sales_file='sales_data.csv'):
        """
        Загружает и объединяет данные о товарах и продажах
        """
        print("📊 Загрузка и объединение данных...")
        
        # Загружаем данные
        self.products_data = pd.read_csv(products_file, sep=';', decimal=',')
        self.sales_data = pd.read_csv(sales_file, sep=';', decimal=',')
        
        print(f"✅ Товары: {len(self.products_data)} записей")
        print(f"✅ Продажи: {len(self.sales_data)} записей")
        
        # Объединяем данные
        self.merged_data = self.products_data.merge(
            self.sales_data, on='product_id', how='inner'
        )
        
        print(f"🔗 Объединено: {len(self.merged_data)} записей")
        
        return self.merged_data
    
    def feature_engineering(self):
        """
        Создает производные метрики для анализа
        """
        print("\n🔧 Инжиниринг признаков...")
        
        # Создаем производные метрики
        self.merged_data['profit_margin'] = (
            (self.merged_data['price'] - self.merged_data['cost']) / 
            self.merged_data['price']
        )
        
        self.merged_data['sales_velocity'] = (
            self.merged_data['units_sold'] / self.merged_data['days_in_catalog']
        )
        
        self.merged_data['revenue_per_day'] = (
            self.merged_data['revenue'] / self.merged_data['days_in_catalog']
        )
        
        self.merged_data['marketing_efficiency'] = (
            self.merged_data['revenue'] / self.merged_data['marketing_spend']
        )
        
        self.merged_data['review_density'] = (
            self.merged_data['review_count'] / self.merged_data['days_in_catalog']
        )
        
        # Логарифмируем сильно скошенные переменные
        self.merged_data['log_price'] = np.log(self.merged_data['price'])
        self.merged_data['log_units_sold'] = np.log(self.merged_data['units_sold'] + 1)
        
        print("✅ Создано новых признаков:")
        new_features = ['profit_margin', 'sales_velocity', 'revenue_per_day', 
                       'marketing_efficiency', 'review_density', 'log_price', 'log_units_sold']
        for feature in new_features:
            print(f"   • {feature}")
        
        return self.merged_data
    
    def prepare_analysis_features(self):
        """
        Подготавливает признаки для мультивариантного анализа
        """
        print("\n📋 Подготовка признаков для анализа...")
        
        # Выбираем количественные признаки для анализа
        analysis_features = [
            'log_price', 'profit_margin', 'log_units_sold', 'sales_velocity',
            'return_rate', 'rating', 'review_density', 'category_popularity',
            'seasonal_factor', 'competition_level', 'revenue_per_day',
            'marketing_efficiency', 'conversion_rate'
        ]
        
        # Проверяем наличие всех признаков
        available_features = [f for f in analysis_features if f in self.merged_data.columns]
        print(f"📊 Используемые признаки ({len(available_features)}):")
        for feature in available_features:
            print(f"   • {feature}")
        
        self.features = self.merged_data[available_features]
        self.feature_names = available_features
        
        # Проверяем качество данных
        print(f"\n🔍 Качество данных:")
        print(f"   Пропущенные значения: {self.features.isnull().sum().sum()}")
        print(f"   Бесконечные значения: {np.isinf(self.features.values).sum()}")
        
        # Заполняем пропуски медианой
        if self.features.isnull().sum().sum() > 0:
            self.features = self.features.fillna(self.features.median())
            print("   ✅ Пропуски заполнены медианными значениями")
        
        return self.features
    
    def standardize_data(self):
        """
        Стандартизирует данные
        """
        print("\n⚖️ Стандартизация данных...")
        
        scaler = StandardScaler()
        self.features_scaled = scaler.fit_transform(self.features)
        
        print("✅ Данные стандартизированы")
        return self.features_scaled
    
    def perform_comprehensive_pca(self, variance_threshold=0.85):
        """
        Выполняет комплексный анализ PCA
        """
        print("\n🔍 Комплексный анализ главных компонент...")
        
        # Определяем оптимальное количество компонент
        pca_full = PCA()
        pca_full.fit(self.features_scaled)
        
        cumsum = np.cumsum(pca_full.explained_variance_ratio_)
        n_components = np.argmax(cumsum >= variance_threshold) + 1
        
        print(f"🎯 Для {variance_threshold:.0%} изменчивости нужно {n_components} компонент")
        
        # Применяем PCA
        self.pca_model = PCA(n_components=n_components)
        self.pca_components = self.pca_model.fit_transform(self.features_scaled)
        
        # Анализируем результаты
        print(f"\n📊 Результаты PCA:")
        print(f"   Компонент: {self.pca_model.n_components_}")
        print(f"   Объясненная изменчивость: {self.pca_model.explained_variance_ratio_.sum():.1%}")
        
        # Интерпретируем главные компоненты
        self._interpret_pca_components()
        
        return self.pca_components
    
    def _interpret_pca_components(self, top_n=3):
        """
        Интерпретирует главные компоненты
        """
        print("\n🎯 Интерпретация главных компонент:")
        
        loadings = self.pca_model.components_.T
        
        for i in range(self.pca_model.n_components_):
            variance = self.pca_model.explained_variance_ratio_[i]
            print(f"\n📊 PC{i+1} (объясняет {variance:.1%} изменчивости):")
            
            # Находим переменные с наибольшими нагрузками
            component_loadings = loadings[:, i]
            abs_loadings = np.abs(component_loadings)
            top_indices = np.argsort(abs_loadings)[-top_n:][::-1]
            
            print("   Ключевые переменные:")
            for idx in top_indices:
                feature = self.feature_names[idx]
                loading = component_loadings[idx]
                direction = "⬆️" if loading > 0 else "⬇️"
                print(f"     {direction} {feature}: {loading:.3f}")
            
            # Предлагаем интерпретацию
            interpretation = self._suggest_component_interpretation(
                [self.feature_names[idx] for idx in top_indices],
                [component_loadings[idx] for idx in top_indices]
            )
            print(f"   💡 Возможная интерпретация: {interpretation}")
    
    def _suggest_component_interpretation(self, top_features, top_loadings):
        """
        Предлагает интерпретацию компоненты на основе топ-переменных
        """
        # Анализируем доминирующие темы
        themes = {
            'price': ['log_price', 'profit_margin'],
            'performance': ['log_units_sold', 'sales_velocity', 'revenue_per_day'],
            'quality': ['rating', 'return_rate', 'review_density'],
            'market': ['competition_level', 'category_popularity', 'seasonal_factor'],
            'efficiency': ['marketing_efficiency', 'conversion_rate']
        }
        
        theme_scores = {}
        for theme, keywords in themes.items():
            score = 0
            for feature, loading in zip(top_features, top_loadings):
                for keyword in keywords:
                    if keyword in feature:
                        score += abs(loading)
            theme_scores[theme] = score
        
        # Находим доминирующую тему
        if theme_scores:
            dominant_theme = max(theme_scores, key=theme_scores.get)
            interpretations = {
                'price': '"Ценовое позиционирование"',
                'performance': '"Коммерческая эффективность"',
                'quality': '"Качество и восприятие"',
                'market': '"Рыночные условия"',
                'efficiency': '"Операционная эффективность"'
            }
            return interpretations.get(dominant_theme, '"Смешанный фактор"')
        else:
            return '"Требует дополнительного анализа"'
    
    def perform_clustering_analysis(self, max_clusters=8):
        """
        Выполняет кластерный анализ в пространстве главных компонент
        """
        print("\n👥 Кластерный анализ...")
        
        # Определяем оптимальное количество кластеров
        silhouette_scores = []
        K_range = range(2, max_clusters + 1)
        
        for k in K_range:
            kmeans = KMeans(n_clusters=k, random_state=42)
            cluster_labels = kmeans.fit_predict(self.pca_components)
            silhouette_avg = silhouette_score(self.pca_components, cluster_labels)
            silhouette_scores.append(silhouette_avg)
        
        # Находим оптимальное количество кластеров
        optimal_k = K_range[np.argmax(silhouette_scores)]
        best_score = max(silhouette_scores)
        
        print(f"🎯 Оптимальное количество кластеров: {optimal_k}")
        print(f"📊 Silhouette score: {best_score:.3f}")
        
        # Применяем кластеризацию
        kmeans = KMeans(n_clusters=optimal_k, random_state=42)
        self.clusters = kmeans.fit_predict(self.pca_components)
        
        # Анализируем кластеры
        self._analyze_clusters()
        
        return self.clusters
    
    def _analyze_clusters(self):
        """
        Анализирует профили кластеров
        """
        print("\n📊 Профили кластеров:")
        
        # Добавляем кластеры к исходным данным
        analysis_data = self.merged_data.copy()
        analysis_data['cluster'] = self.clusters
        
        # Анализируем ключевые метрики по кластерам
        key_metrics = ['price', 'units_sold', 'revenue', 'profit_margin', 
                      'rating', 'return_rate', 'category_popularity']
        
        cluster_profiles = analysis_data.groupby('cluster')[key_metrics].agg({
            'price': ['mean', 'median'],
            'units_sold': ['mean', 'median'],
            'revenue': ['mean', 'median'],
            'profit_margin': ['mean'],
            'rating': ['mean'],
            'return_rate': ['mean'],
            'category_popularity': ['mean']
        }).round(2)
        
        print(cluster_profiles)
        
        # Размеры кластеров
        cluster_sizes = analysis_data['cluster'].value_counts().sort_index()
        print(f"\n📊 Размеры кластеров:")
        for cluster, size in cluster_sizes.items():
            percentage = size / len(analysis_data) * 100
            print(f"   Кластер {cluster}: {size} товаров ({percentage:.1f}%)")
        
        return cluster_profiles
    
    def generate_business_insights(self):
        """
        Генерирует бизнес-инсайты на основе анализа
        """
        print("\n" + "="*60)
        print("💡 БИЗНЕС-ИНСАЙТЫ И РЕКОМЕНДАЦИИ")
        print("="*60)
        
        # Анализ по кластерам
        analysis_data = self.merged_data.copy()
        analysis_data['cluster'] = self.clusters
        
        # Находим самые прибыльные кластеры
        cluster_revenue = analysis_data.groupby('cluster')['revenue'].sum()
        cluster_profit = analysis_data.groupby('cluster').apply(
            lambda x: ((x['price'] - x['cost']) * x['units_sold']).sum()
        )
        
        top_revenue_cluster = cluster_revenue.idxmax()
        top_profit_cluster = cluster_profit.idxmax()
        
        print(f"🏆 Топ-кластер по выручке: Кластер {top_revenue_cluster}")
        print(f"💰 Топ-кластер по прибыли: Кластер {top_profit_cluster}")
        
        # Анализ проблемных областей
        low_performers = analysis_data[
            (analysis_data['sales_velocity'] < analysis_data['sales_velocity'].quantile(0.25)) |
            (analysis_data['profit_margin'] < analysis_data['profit_margin'].quantile(0.25))
        ]
        
        print(f"\n⚠️ Проблемные товары: {len(low_performers)} ({len(low_performers)/len(analysis_data)*100:.1f}%)")
        
        # Рекомендации по кластерам
        print("\n🎯 Рекомендации по кластерам:")
        
        for cluster in sorted(analysis_data['cluster'].unique()):
            cluster_data = analysis_data[analysis_data['cluster'] == cluster]
            avg_profit = cluster_data['profit_margin'].mean()
            avg_sales = cluster_data['sales_velocity'].mean()
            avg_rating = cluster_data['rating'].mean()
            
            print(f"\n📊 Кластер {cluster}:")
            print(f"   Товаров: {len(cluster_data)}")
            print(f"   Средняя прибыльность: {avg_profit:.1%}")
            print(f"   Средняя скорость продаж: {avg_sales:.2f}")
            print(f"   Средний рейтинг: {avg_rating:.1f}")
            
            # Стратегические рекомендации
            if avg_profit > 0.3 and avg_sales > analysis_data['sales_velocity'].median():
                print("   🚀 Стратегия: Масштабирование (звёзды категории)")
            elif avg_profit > 0.3 and avg_sales <= analysis_data['sales_velocity'].median():
                print("   📈 Стратегия: Маркетинговое продвижение (скрытые жемчужины)")
            elif avg_profit <= 0.3 and avg_sales > analysis_data['sales_velocity'].median():
                print("   💡 Стратегия: Оптимизация затрат (популярные, но малоприбыльные)")
            else:
                print("   ⚠️ Стратегия: Пересмотр ассортимента (кандидаты на исключение)")
    
    def create_executive_summary(self):
        """
        Создает executive summary для руководства
        """
        print("\n" + "="*60)
        print("📊 EXECUTIVE SUMMARY")
        print("="*60)
        
        # Основные цифры
        total_products = len(self.merged_data)
        total_revenue = self.merged_data['revenue'].sum()
        avg_profit_margin = self.merged_data['profit_margin'].mean()
        
        print(f"📋 Ключевые показатели:")
        print(f"   • Проанализировано товаров: {total_products:,}")
        print(f"   • Общая выручка: {total_revenue:,.0f} руб.")
        print(f"   • Средняя маржинальность: {avg_profit_margin:.1%}")
        
        # Результаты анализа
        print(f"\n🔍 Результаты мультивариантного анализа:")
        print(f"   • Выделено главных компонент: {self.pca_model.n_components_}")
        print(f"   • Объясненная изменчивость: {self.pca_model.explained_variance_ratio_.sum():.1%}")
        print(f"   • Количество сегментов: {len(np.unique(self.clusters))}")
        
        # Топ-инсайты
        print(f"\n💡 Ключевые инсайты:")
        print(f"   1. Ассортимент можно эффективно описать {self.pca_model.n_components_} ключевыми факторами")
        print(f"   2. Товары естественным образом группируются в {len(np.unique(self.clusters))} сегмента")
        print(f"   3. Каждый сегмент требует индивидуальной стратегии управления")
        
        # Приоритеты действий
        print(f"\n🎯 Приоритетные действия:")
        print(f"   1. Масштабировать высокоприбыльные сегменты")
        print(f"   2. Оптимизировать маркетинг низкорентабельных товаров")
        print(f"   3. Пересмотреть ассортимент проблемных категорий")
        
        return {
            'total_products': total_products,
            'total_revenue': total_revenue,
            'avg_profit_margin': avg_profit_margin,
            'n_components': self.pca_model.n_components_,
            'explained_variance': self.pca_model.explained_variance_ratio_.sum(),
            'n_clusters': len(np.unique(self.clusters))
        }
    
    def create_comprehensive_visualization(self):
        """
        Создает комплексную визуализацию результатов
        """
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        
        # 1. Scree plot
        ax1 = axes[0, 0]
        pca_full = PCA()
        pca_full.fit(self.features_scaled)
        explained_var = pca_full.explained_variance_ratio_
        
        ax1.plot(range(1, len(explained_var) + 1), explained_var, 'bo-')
        ax1.set_title('🔍 Scree Plot')
        ax1.set_xlabel('Компонента')
        ax1.set_ylabel('Изменчивость')
        ax1.grid(True, alpha=0.3)
        
        # 2. Кластеры в пространстве PC1-PC2
        ax2 = axes[0, 1]
        scatter = ax2.scatter(self.pca_components[:, 0], self.pca_components[:, 1], 
                            c=self.clusters, cmap='viridis', alpha=0.7)
        ax2.set_title('👥 Кластеры (PC1 vs PC2)')
        ax2.set_xlabel(f'PC1 ({self.pca_model.explained_variance_ratio_[0]:.1%})')
        ax2.set_ylabel(f'PC2 ({self.pca_model.explained_variance_ratio_[1]:.1%})')
        plt.colorbar(scatter, ax=ax2)
        
        # 3. Распределение по кластерам
        ax3 = axes[0, 2]
        cluster_counts = pd.Series(self.clusters).value_counts().sort_index()
        ax3.bar(cluster_counts.index, cluster_counts.values, color='skyblue', alpha=0.7)
        ax3.set_title('📊 Размеры кластеров')
        ax3.set_xlabel('Кластер')
        ax3.set_ylabel('Количество товаров')
        
        # 4. Heatmap нагрузок
        ax4 = axes[1, 0]
        loadings = self.pca_model.components_.T
        n_comp_show = min(4, self.pca_model.n_components_)
        
        im = ax4.imshow(loadings[:, :n_comp_show], cmap='RdBu_r', aspect='auto')
        ax4.set_title('🔥 Матрица нагрузок')
        ax4.set_xlabel('Главные компоненты')
        ax4.set_ylabel('Переменные')
        ax4.set_xticks(range(n_comp_show))
        ax4.set_xticklabels([f'PC{i+1}' for i in range(n_comp_show)])
        ax4.set_yticks(range(len(self.feature_names)))
        ax4.set_yticklabels(self.feature_names, fontsize=8)
        plt.colorbar(im, ax=ax4)
        
        # 5. Выручка по кластерам
        ax5 = axes[1, 1]
        analysis_data = self.merged_data.copy()
        analysis_data['cluster'] = self.clusters
        revenue_by_cluster = analysis_data.groupby('cluster')['revenue'].sum()
        
        ax5.bar(revenue_by_cluster.index, revenue_by_cluster.values, 
               color='lightcoral', alpha=0.7)
        ax5.set_title('💰 Выручка по кластерам')
        ax5.set_xlabel('Кластер')
        ax5.set_ylabel('Выручка (руб.)')
        ax5.ticklabel_format(style='scientific', axis='y', scilimits=(0,0))
        
        # 6. Маржинальность по кластерам
        ax6 = axes[1, 2]
        margin_by_cluster = analysis_data.groupby('cluster')['profit_margin'].mean()
        
        colors = ['red' if x < 0.2 else 'orange' if x < 0.3 else 'green' 
                 for x in margin_by_cluster.values]
        ax6.bar(margin_by_cluster.index, margin_by_cluster.values, 
               color=colors, alpha=0.7)
        ax6.set_title('📈 Маржинальность по кластерам')
        ax6.set_xlabel('Кластер')
        ax6.set_ylabel('Средняя маржинальность')
        ax6.axhline(y=0.2, color='red', linestyle='--', alpha=0.5, label='20%')
        ax6.axhline(y=0.3, color='orange', linestyle='--', alpha=0.5, label='30%')
        
        plt.tight_layout()
        plt.show()


def main():
    """
    Основная функция для запуска комплексного анализа
    """
    print("🚀 Запуск комплексного мультивариантного анализа")
    print("="*60)
    
    # Создаем анализатор
    analyzer = ComprehensiveAnalyzer()
    
    # Загружаем и объединяем данные
    analyzer.load_and_merge_data()
    
    # Инжиниринг признаков
    analyzer.feature_engineering()
    
    # Подготавливаем данные для анализа
    analyzer.prepare_analysis_features()
    
    # Стандартизируем данные
    analyzer.standardize_data()
    
    # Выполняем PCA
    analyzer.perform_comprehensive_pca()
    
    # Кластерный анализ
    analyzer.perform_clustering_analysis()
    
    # Создаем визуализацию
    analyzer.create_comprehensive_visualization()
    
    # Генерируем бизнес-инсайты
    analyzer.generate_business_insights()
    
    # Executive summary
    summary = analyzer.create_executive_summary()
    
    print("\n🎉 Комплексный анализ завершен!")
    
    return analyzer, summary


if __name__ == "__main__":
    analyzer, summary = main()