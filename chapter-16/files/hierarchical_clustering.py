"""
🌳 Иерархическая кластеризация - строим дерево групп данных!

Этот скрипт демонстрирует:
- Агломеративную кластеризацию  
- Построение и интерпретацию дендрограмм
- Различные методы объединения кластеров
- Сравнение с K-means
- Применение к товарным данным
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import AgglomerativeClustering, KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score, adjusted_rand_score
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
from scipy.spatial.distance import pdist
import warnings

warnings.filterwarnings('ignore')

print("🌳 Изучаем иерархическую кластеризацию!")
print("=" * 55)

# Настройка визуализации
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10
sns.set_style("whitegrid")

def generate_product_data():
    """Генерируем данные товаров для демонстрации иерархической кластеризации"""
    np.random.seed(42)
    n_products = 100
    
    # Создаем несколько естественных групп товаров
    product_groups = [
        {"name": "Премиум электроника", "size": 15, "price_mean": 50000, "rating_mean": 4.5, "reviews_mean": 200},
        {"name": "Массовая электроника", "size": 25, "price_mean": 15000, "rating_mean": 4.0, "reviews_mean": 150},
        {"name": "Дорогая одежда", "size": 10, "price_mean": 8000, "rating_mean": 4.2, "reviews_mean": 80},
        {"name": "Обычная одежда", "size": 20, "price_mean": 2000, "rating_mean": 3.8, "reviews_mean": 60},
        {"name": "Спорттовары", "size": 15, "price_mean": 5000, "rating_mean": 4.1, "reviews_mean": 90},
        {"name": "Книги", "size": 15, "price_mean": 800, "rating_mean": 4.3, "reviews_mean": 45}
    ]
    
    products_data = []
    product_id = 1
    
    for group in product_groups:
        for _ in range(group["size"]):
            # Генерируем характеристики товара с вариацией
            price = max(100, np.random.normal(group["price_mean"], group["price_mean"] * 0.3))
            rating = np.clip(np.random.normal(group["rating_mean"], 0.3), 1, 5)
            review_count = max(1, int(np.random.normal(group["reviews_mean"], 30)))
            
            # Продажи зависят от рейтинга и цены (обратная зависимость от цены)
            sales_base = (rating - 1) * 50 + (10000 / price) * 100
            sales_volume = max(1, int(np.random.normal(sales_base, 20)))
            
            # Процент возвратов обратно зависит от рейтинга
            return_rate = max(0, min(30, np.random.normal((5 - rating) * 5, 2)))
            
            # Маржинальность случайная но с тенденциями по группам
            if "Премиум" in group["name"]:
                profit_margin = np.random.normal(35, 8)
            elif "Книги" in group["name"]:
                profit_margin = np.random.normal(50, 10)
            else:
                profit_margin = np.random.normal(25, 6)
            
            profit_margin = np.clip(profit_margin, 5, 70)
            
            # Бренд зависит от группы
            if "электроника" in group["name"]:
                brand = np.random.choice(['Apple', 'Samsung', 'Xiaomi', 'Sony', 'LG'])
            elif "одежда" in group["name"]:
                brand = np.random.choice(['Nike', 'Adidas', 'Zara', 'H&M', 'Uniqlo'])
            elif "Спорт" in group["name"]:
                brand = np.random.choice(['Nike', 'Adidas', 'Puma', 'Reebok', 'Under Armour'])
            else:
                brand = np.random.choice(['NoName', 'Generic', 'Local', 'Import', 'Premium'])
            
            product = {
                'product_id': f'PROD_{product_id:05d}',
                'product_name': f'{group["name"]} товар {product_id}',
                'category': group["name"],
                'price': round(price, 2),
                'rating': round(rating, 1),
                'review_count': review_count,
                'sales_volume': sales_volume,
                'return_rate': round(return_rate, 1),
                'brand': brand,
                'profit_margin': round(profit_margin, 1),
                'true_group': group["name"]  # Истинная группа для проверки
            }
            
            products_data.append(product)
            product_id += 1
    
    return pd.DataFrame(products_data)

def plot_dendrogram_comparison(data, features, methods=['ward', 'complete', 'average', 'single']):
    """Сравнивает различные методы объединения через дендрограммы"""
    print("\n🌳 Сравнение методов объединения кластеров...")
    
    # Подготовка данных
    X = data[features]
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    fig, axes = plt.subplots(2, 2, figsize=(20, 15))
    fig.suptitle('🌳 Сравнение методов иерархической кластеризации', fontsize=16)
    
    axes = axes.ravel()
    
    for i, method in enumerate(methods):
        ax = axes[i]
        
        # Вычисляем матрицу связей
        linkage_matrix = linkage(X_scaled, method=method)
        
        # Строим дендрограмму
        dendrogram(linkage_matrix,
                  truncate_mode='lastp',  # Показать только последние p объединений
                  p=30,                   # Количество листьев
                  leaf_rotation=90,       # Поворот подписей
                  leaf_font_size=8,
                  ax=ax)
        
        ax.set_title(f'Метод: {method.upper()}', fontsize=14)
        ax.set_xlabel('Номер кластера или размер')
        ax.set_ylabel('Расстояние объединения')
        
        # Добавляем горизонтальную линию для разреза на 5 кластеров
        threshold = np.percentile(linkage_matrix[:, 2], 80)  # 80-й процентиль расстояний
        ax.axhline(y=threshold, color='red', linestyle='--', alpha=0.7, 
                  label=f'Порог для ~5 кластеров')
        ax.legend()
    
    plt.tight_layout()
    plt.show()
    
    return linkage_matrix

def perform_hierarchical_clustering(data, features, n_clusters=5, linkage_method='ward'):
    """Выполняет иерархическую кластеризацию"""
    print(f"\n🎯 Выполняем иерархическую кластеризацию...")
    print(f"  • Метод объединения: {linkage_method}")
    print(f"  • Количество кластеров: {n_clusters}")
    
    # Подготовка данных
    X = data[features]
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Обучаем модель
    hierarchical = AgglomerativeClustering(
        n_clusters=n_clusters,
        linkage=linkage_method
    )
    
    cluster_labels = hierarchical.fit_predict(X_scaled)
    
    # Добавляем результаты к данным
    data_with_clusters = data.copy()
    data_with_clusters['cluster'] = cluster_labels
    
    # Оценка качества
    silhouette = silhouette_score(X_scaled, cluster_labels)
    
    print(f"✅ Кластеризация завершена!")
    print(f"📊 Силуэтный коэффициент: {silhouette:.3f}")
    
    return data_with_clusters, hierarchical, X_scaled

def compare_clustering_methods(data, features, n_clusters=5):
    """Сравнивает иерархическую кластеризацию и K-means"""
    print(f"\n⚔️ Сравнение методов кластеризации...")
    
    # Подготовка данных
    X = data[features]
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Методы для сравнения
    methods = {
        'K-means': KMeans(n_clusters=n_clusters, random_state=42),
        'Иерархическая (ward)': AgglomerativeClustering(n_clusters=n_clusters, linkage='ward'),
        'Иерархическая (complete)': AgglomerativeClustering(n_clusters=n_clusters, linkage='complete'),
        'Иерархическая (average)': AgglomerativeClustering(n_clusters=n_clusters, linkage='average')
    }
    
    results = {}
    
    for method_name, model in methods.items():
        cluster_labels = model.fit_predict(X_scaled)
        silhouette = silhouette_score(X_scaled, cluster_labels)
        
        # Сравниваем с истинными группами (если есть)
        if 'true_group' in data.columns:
            # Кодируем истинные группы в числа для сравнения
            true_labels = pd.Categorical(data['true_group']).codes
            ari = adjusted_rand_score(true_labels, cluster_labels)
        else:
            ari = None
        
        results[method_name] = {
            'silhouette_score': silhouette,
            'adjusted_rand_index': ari,
            'cluster_labels': cluster_labels
        }
        
        print(f"  {method_name}:")
        print(f"    Силуэтный коэффициент: {silhouette:.3f}")
        if ari is not None:
            print(f"    Adjusted Rand Index: {ari:.3f}")
    
    # Визуализация сравнения
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('⚔️ Сравнение методов кластеризации', fontsize=16)
    
    axes = axes.ravel()
    colors = plt.cm.Set1(np.linspace(0, 1, n_clusters))
    
    for i, (method_name, result) in enumerate(results.items()):
        ax = axes[i]
        cluster_labels = result['cluster_labels']
        
        # Визуализируем первые два признака
        for cluster in range(n_clusters):
            mask = cluster_labels == cluster
            if np.any(mask):
                ax.scatter(X_scaled[mask, 0], X_scaled[mask, 1],
                          c=[colors[cluster]], label=f'Кластер {cluster}',
                          alpha=0.7, s=50)
        
        ax.set_title(f'{method_name}\nSilhouette: {result["silhouette_score"]:.3f}')
        ax.set_xlabel(f'{features[0]} (стандартизированный)')
        ax.set_ylabel(f'{features[1]} (стандартизированный)')
        ax.legend()
        ax.grid(alpha=0.3)
    
    plt.tight_layout()
    plt.show()
    
    return results

def analyze_hierarchical_clusters(data_with_clusters, features):
    """Анализирует профили кластеров из иерархической кластеризации"""
    print("\n📋 Анализ профилей кластеров:")
    print("=" * 50)
    
    # Создаем профили кластеров
    cluster_profiles = []
    
    for cluster_id in sorted(data_with_clusters['cluster'].unique()):
        cluster_data = data_with_clusters[data_with_clusters['cluster'] == cluster_id]
        
        profile = {
            'Кластер': cluster_id,
            'Размер': len(cluster_data),
            'Доля (%)': f"{len(cluster_data) / len(data_with_clusters) * 100:.1f}%"
        }
        
        # Средние значения числовых признаков
        for feature in features:
            profile[f'Средний {feature}'] = cluster_data[feature].mean()
        
        # Самые частые категориальные значения
        if 'brand' in cluster_data.columns:
            top_brand = cluster_data['brand'].mode()
            profile['Топ бренд'] = top_brand[0] if len(top_brand) > 0 else 'Нет данных'
        
        if 'true_group' in cluster_data.columns:
            top_group = cluster_data['true_group'].mode()
            profile['Основная группа'] = top_group[0] if len(top_group) > 0 else 'Смешанная'
        
        cluster_profiles.append(profile)
    
    profiles_df = pd.DataFrame(cluster_profiles)
    print(profiles_df.round(1))
    
    return profiles_df

def create_product_recommendations(data_with_clusters):
    """Создает рекомендации товаров на основе кластеров"""
    print(f"\n🛍️ СИСТЕМА ТОВАРНЫХ РЕКОМЕНДАЦИЙ:")
    print("=" * 50)
    
    recommendations = {}
    
    for cluster_id in sorted(data_with_clusters['cluster'].unique()):
        cluster_data = data_with_clusters[data_with_clusters['cluster'] == cluster_id]
        
        # Характеристики кластера
        avg_price = cluster_data['price'].mean()
        avg_rating = cluster_data['rating'].mean()
        avg_sales = cluster_data['sales_volume'].mean()
        top_brands = cluster_data['brand'].value_counts().head(3)
        
        # Стратегия для кластера
        if avg_price > 20000:
            strategy = "Премиум сегмент - акцент на качество и эксклюзивность"
        elif avg_rating > 4.2:
            strategy = "Высокий рейтинг - используйте социальные доказательства"
        elif avg_sales > 100:
            strategy = "Популярные товары - акцент на трендовость"
        else:
            strategy = "Нишевые товары - персонализированные предложения"
        
        recommendations[cluster_id] = {
            'размер': len(cluster_data),
            'средняя_цена': avg_price,
            'средний_рейтинг': avg_rating,
            'топ_бренды': top_brands.to_dict(),
            'стратегия': strategy,
            'товары': cluster_data[['product_name', 'price', 'rating']].head(3).to_dict('records')
        }
    
    # Выводим рекомендации
    for cluster_id, rec in recommendations.items():
        print(f"\n🎯 Кластер {cluster_id} ({rec['размер']} товаров):")
        print(f"  💰 Средняя цена: {rec['средняя_цена']:,.0f} руб.")
        print(f"  ⭐ Средний рейтинг: {rec['средний_рейтинг']:.1f}")
        print(f"  🏆 Топ бренды: {', '.join(rec['топ_бренды'].keys())}")
        print(f"  📈 Стратегия: {rec['стратегия']}")
        print(f"  🛍️ Примеры товаров:")
        for product in rec['товары']:
            print(f"    • {product['product_name']} - {product['price']:,.0f} руб. (★{product['rating']})")
    
    return recommendations

def demonstrate_dynamic_clustering(data, features):
    """Демонстрирует выбор количества кластеров через дендрограмму"""
    print(f"\n🔍 Динамический выбор количества кластеров...")
    
    # Подготовка данных
    X = data[features]
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Строим дендрограмму с возможностью выбора порога
    linkage_matrix = linkage(X_scaled, method='ward')
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 6))
    fig.suptitle('🔍 Выбор количества кластеров через дендрограмму', fontsize=14)
    
    # Полная дендрограмма
    dendrogram(linkage_matrix, ax=ax1, leaf_rotation=90, leaf_font_size=8)
    ax1.set_title('Полная дендрограмма')
    ax1.set_xlabel('Номер объекта')
    ax1.set_ylabel('Расстояние объединения')
    
    # Обрезанная дендрограмма
    dendrogram(linkage_matrix, truncate_mode='lastp', p=15, ax=ax2,
              leaf_rotation=90, leaf_font_size=10)
    ax2.set_title('Обрезанная дендрограмма (15 листьев)')
    ax2.set_xlabel('Кластер')
    ax2.set_ylabel('Расстояние объединения')
    
    # Добавляем линии для различных количеств кластеров
    distances = linkage_matrix[:, 2]
    for n_clusters, color in [(3, 'red'), (5, 'blue'), (7, 'green')]:
        threshold = distances[-(n_clusters-1)]
        ax2.axhline(y=threshold, color=color, linestyle='--', alpha=0.7,
                   label=f'{n_clusters} кластеров')
    
    ax2.legend()
    plt.tight_layout()
    plt.show()
    
    # Анализируем качество для разного количества кластеров
    print(f"\n📊 Качество кластеризации для разного количества групп:")
    
    cluster_range = range(2, 8)
    silhouette_scores = []
    
    for n_clusters in cluster_range:
        hierarchical = AgglomerativeClustering(n_clusters=n_clusters, linkage='ward')
        cluster_labels = hierarchical.fit_predict(X_scaled)
        silhouette = silhouette_score(X_scaled, cluster_labels)
        silhouette_scores.append(silhouette)
        
        print(f"  {n_clusters} кластеров: силуэтный коэффициент = {silhouette:.3f}")
    
    # График качества
    plt.figure(figsize=(10, 6))
    plt.plot(cluster_range, silhouette_scores, 'bo-', linewidth=2, markersize=8)
    plt.title('📊 Качество иерархической кластеризации')
    plt.xlabel('Количество кластеров')
    plt.ylabel('Силуэтный коэффициент')
    plt.grid(alpha=0.3)
    plt.show()
    
    optimal_k = cluster_range[np.argmax(silhouette_scores)]
    print(f"🎯 Рекомендуемое количество кластеров: {optimal_k}")
    
    return optimal_k

def main():
    """Основная функция демонстрации иерархической кластеризации"""
    print("🚀 Запуск демонстрации иерархической кластеризации!")
    
    # 1. Генерируем данные товаров
    data = generate_product_data()
    features = ['price', 'rating', 'review_count', 'sales_volume', 'return_rate', 'profit_margin']
    
    print(f"✅ Сгенерировано {len(data)} товаров для анализа")
    print(f"📊 Признаки для кластеризации: {', '.join(features)}")
    
    # 2. Сравниваем различные методы объединения
    linkage_matrix = plot_dendrogram_comparison(data, features)
    
    # 3. Выполняем иерархическую кластеризацию
    data_with_clusters, model, X_scaled = perform_hierarchical_clustering(data, features)
    
    # 4. Сравниваем с другими методами
    comparison_results = compare_clustering_methods(data, features)
    
    # 5. Анализируем профили кластеров
    profiles_df = analyze_hierarchical_clusters(data_with_clusters, features)
    
    # 6. Создаем товарные рекомендации
    recommendations = create_product_recommendations(data_with_clusters)
    
    # 7. Демонстрируем динамический выбор количества кластеров
    optimal_k = demonstrate_dynamic_clustering(data, features)
    
    print(f"\n🎉 Демонстрация иерархической кластеризации завершена!")
    print("📚 Следующий шаг: изучите clustering_evaluation.py")
    print("💡 Совет: иерархическая кластеризация лучше для понимания структуры данных!")
    
    return data_with_clusters, recommendations, comparison_results

if __name__ == "__main__":
    results = main()