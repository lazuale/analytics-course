"""
🎯 K-means кластеризация - ваш первый шаг в неконтролируемое обучение!

Этот скрипт демонстрирует:
- Основы алгоритма K-means
- Выбор оптимального количества кластеров
- Визуализацию результатов
- Интерпретацию кластеров для бизнеса
- Сегментацию клиентов
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score
from sklearn.decomposition import PCA
import warnings

warnings.filterwarnings('ignore')

print("🎯 Изучаем K-means кластеризацию!")
print("=" * 50)

# Настройка визуализации
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10
sns.set_style("whitegrid")

def generate_sample_data():
    """Генерируем примерные данные клиентов для демонстрации"""
    np.random.seed(42)
    n_customers = 500
    
    # Создаем 4 естественных кластера клиентов
    clusters_data = []
    
    # Кластер 1: Молодые с низким доходом
    cluster1 = {
        'age': np.random.normal(25, 3, 125),
        'income': np.random.normal(40, 8, 125),
        'spending': np.random.normal(20, 5, 125)
    }
    clusters_data.append(cluster1)
    
    # Кластер 2: Средний возраст, средний доход  
    cluster2 = {
        'age': np.random.normal(40, 5, 125),
        'income': np.random.normal(70, 10, 125), 
        'spending': np.random.normal(45, 8, 125)
    }
    clusters_data.append(cluster2)
    
    # Кластер 3: Старше, высокий доход
    cluster3 = {
        'age': np.random.normal(55, 4, 125),
        'income': np.random.normal(100, 15, 125),
        'spending': np.random.normal(70, 10, 125)
    }
    clusters_data.append(cluster3)
    
    # Кластер 4: Молодые с высоким доходом (IT)
    cluster4 = {
        'age': np.random.normal(30, 4, 125),
        'income': np.random.normal(120, 20, 125),
        'spending': np.random.normal(80, 12, 125)
    }
    clusters_data.append(cluster4)
    
    # Объединяем все кластеры
    age = np.concatenate([cluster['age'] for cluster in clusters_data])
    income = np.concatenate([cluster['income'] for cluster in clusters_data])
    spending = np.concatenate([cluster['spending'] for cluster in clusters_data])
    
    # Создаем DataFrame
    data = pd.DataFrame({
        'age': np.clip(age, 18, 75),
        'income': np.clip(income, 20, 200),
        'spending': np.clip(spending, 5, 150),
        'true_cluster': np.repeat([0, 1, 2, 3], 125)  # Истинные кластеры для сравнения
    })
    
    return data

def visualize_data(data, title="Исходные данные"):
    """Визуализация данных в 3D пространстве"""
    fig = plt.figure(figsize=(15, 5))
    
    # 2D проекции
    ax1 = plt.subplot(1, 3, 1)
    plt.scatter(data['age'], data['income'], alpha=0.6, c='blue')
    plt.xlabel('Возраст')
    plt.ylabel('Доход (тыс. руб.)')
    plt.title('Возраст vs Доход')
    plt.grid(alpha=0.3)
    
    ax2 = plt.subplot(1, 3, 2)
    plt.scatter(data['age'], data['spending'], alpha=0.6, c='green')
    plt.xlabel('Возраст')
    plt.ylabel('Траты (тыс. руб.)')
    plt.title('Возраст vs Траты')
    plt.grid(alpha=0.3)
    
    ax3 = plt.subplot(1, 3, 3)
    plt.scatter(data['income'], data['spending'], alpha=0.6, c='red')
    plt.xlabel('Доход (тыс. руб.)')
    plt.ylabel('Траты (тыс. руб.)')
    plt.title('Доход vs Траты')
    plt.grid(alpha=0.3)
    
    plt.suptitle(title, fontsize=16)
    plt.tight_layout()
    plt.show()

def find_optimal_clusters(data, features, max_k=10):
    """Находит оптимальное количество кластеров"""
    print("\n🔍 Поиск оптимального количества кластеров...")
    
    # Подготовка данных
    X = data[features]
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Тестируем разное количество кластеров
    k_range = range(2, max_k + 1)
    inertias = []
    silhouette_scores = []
    calinski_scores = []
    davies_bouldin_scores = []
    
    for k in k_range:
        print(f"  Тестируем k={k}...")
        
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        cluster_labels = kmeans.fit_predict(X_scaled)
        
        # Собираем метрики
        inertias.append(kmeans.inertia_)
        silhouette_scores.append(silhouette_score(X_scaled, cluster_labels))
        calinski_scores.append(calinski_harabasz_score(X_scaled, cluster_labels))
        davies_bouldin_scores.append(davies_bouldin_score(X_scaled, cluster_labels))
    
    # Визуализация результатов
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('📊 Выбор оптимального количества кластеров', fontsize=16)
    
    # График локтя
    axes[0, 0].plot(k_range, inertias, 'bo-', linewidth=2, markersize=8)
    axes[0, 0].set_title('📈 Метод локтя (чем меньше, тем лучше)')
    axes[0, 0].set_xlabel('Количество кластеров (k)')
    axes[0, 0].set_ylabel('Inertia (внутрикластерная дисперсия)')
    axes[0, 0].grid(alpha=0.3)
    
    # Силуэтный анализ
    axes[0, 1].plot(k_range, silhouette_scores, 'ro-', linewidth=2, markersize=8)
    axes[0, 1].set_title('📊 Силуэтный коэффициент (чем больше, тем лучше)')
    axes[0, 1].set_xlabel('Количество кластеров (k)')
    axes[0, 1].set_ylabel('Силуэтный коэффициент')
    axes[0, 1].grid(alpha=0.3)
    
    # Calinski-Harabasz индекс
    axes[1, 0].plot(k_range, calinski_scores, 'go-', linewidth=2, markersize=8)
    axes[1, 0].set_title('🎯 Calinski-Harabasz индекс (чем больше, тем лучше)')
    axes[1, 0].set_xlabel('Количество кластеров (k)')
    axes[1, 0].set_ylabel('Calinski-Harabasz индекс')
    axes[1, 0].grid(alpha=0.3)
    
    # Davies-Bouldin индекс
    axes[1, 1].plot(k_range, davies_bouldin_scores, 'mo-', linewidth=2, markersize=8)
    axes[1, 1].set_title('📉 Davies-Bouldin индекс (чем меньше, тем лучше)')
    axes[1, 1].set_xlabel('Количество кластеров (k)')
    axes[1, 1].set_ylabel('Davies-Bouldin индекс')
    axes[1, 1].grid(alpha=0.3)
    
    plt.tight_layout()
    plt.show()
    
    # Рекомендация оптимального k
    best_k_silhouette = k_range[np.argmax(silhouette_scores)]
    best_k_calinski = k_range[np.argmax(calinski_scores)]
    best_k_davies = k_range[np.argmin(davies_bouldin_scores)]
    
    print(f"\n📊 Рекомендации по количеству кластеров:")
    print(f"  • По силуэтному коэффициенту: k = {best_k_silhouette} (score = {max(silhouette_scores):.3f})")
    print(f"  • По Calinski-Harabasz: k = {best_k_calinski} (score = {max(calinski_scores):.1f})")
    print(f"  • По Davies-Bouldin: k = {best_k_davies} (score = {min(davies_bouldin_scores):.3f})")
    
    return X_scaled, scaler, best_k_silhouette

def perform_kmeans_clustering(data, X_scaled, n_clusters=4):
    """Выполняет K-means кластеризацию"""
    print(f"\n🎯 Выполняем K-means кластеризацию с k={n_clusters}...")
    
    # Обучаем модель
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    cluster_labels = kmeans.fit_predict(X_scaled)
    
    # Добавляем метки кластеров к данным
    data_with_clusters = data.copy()
    data_with_clusters['cluster'] = cluster_labels
    
    # Оценка качества
    silhouette = silhouette_score(X_scaled, cluster_labels)
    calinski = calinski_harabasz_score(X_scaled, cluster_labels)
    davies_bouldin = davies_bouldin_score(X_scaled, cluster_labels)
    
    print(f"✅ Кластеризация завершена!")
    print(f"📊 Качество кластеризации:")
    print(f"  • Силуэтный коэффициент: {silhouette:.3f}")
    print(f"  • Calinski-Harabasz индекс: {calinski:.1f}")
    print(f"  • Davies-Bouldin индекс: {davies_bouldin:.3f}")
    print(f"  • Количество итераций: {kmeans.n_iter_}")
    
    return data_with_clusters, kmeans

def visualize_clusters(data_with_clusters, kmeans, X_scaled):
    """Визуализирует результаты кластеризации"""
    print("\n🎨 Визуализируем результаты кластеризации...")
    
    # Используем PCA для визуализации в 2D
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_scaled)
    
    # Получаем центроиды в PCA пространстве
    centers_pca = pca.transform(kmeans.cluster_centers_)
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('🎯 Результаты K-means кластеризации', fontsize=16)
    
    # График 1: PCA с кластерами
    colors = plt.cm.Set1(np.linspace(0, 1, len(np.unique(data_with_clusters['cluster']))))
    
    for i, color in enumerate(colors):
        mask = data_with_clusters['cluster'] == i
        axes[0, 0].scatter(X_pca[mask, 0], X_pca[mask, 1], 
                          c=[color], label=f'Кластер {i}', alpha=0.7, s=50)
    
    # Центроиды
    axes[0, 0].scatter(centers_pca[:, 0], centers_pca[:, 1],
                      c='black', marker='x', s=300, linewidths=3, label='Центроиды')
    
    axes[0, 0].set_title('📊 Кластеры в PCA пространстве')
    axes[0, 0].set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.1%} дисперсии)')
    axes[0, 0].set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.1%} дисперсии)')
    axes[0, 0].legend()
    axes[0, 0].grid(alpha=0.3)
    
    # График 2: Возраст vs Доход
    for i, color in enumerate(colors):
        mask = data_with_clusters['cluster'] == i
        axes[0, 1].scatter(data_with_clusters[mask]['age'], data_with_clusters[mask]['income'],
                          c=[color], label=f'Кластер {i}', alpha=0.7)
    
    axes[0, 1].set_title('👥 Кластеры: Возраст vs Доход')
    axes[0, 1].set_xlabel('Возраст')
    axes[0, 1].set_ylabel('Доход (тыс. руб.)')
    axes[0, 1].legend()
    axes[0, 1].grid(alpha=0.3)
    
    # График 3: Доход vs Траты
    for i, color in enumerate(colors):
        mask = data_with_clusters['cluster'] == i
        axes[1, 0].scatter(data_with_clusters[mask]['income'], data_with_clusters[mask]['spending'],
                          c=[color], label=f'Кластер {i}', alpha=0.7)
    
    axes[1, 0].set_title('💰 Кластеры: Доход vs Траты')
    axes[1, 0].set_xlabel('Доход (тыс. руб.)')
    axes[1, 0].set_ylabel('Траты (тыс. руб.)')
    axes[1, 0].legend()
    axes[1, 0].grid(alpha=0.3)
    
    # График 4: Размеры кластеров
    cluster_sizes = data_with_clusters['cluster'].value_counts().sort_index()
    bars = axes[1, 1].bar(range(len(cluster_sizes)), cluster_sizes.values,
                         color=colors[:len(cluster_sizes)], alpha=0.7)
    
    # Добавляем значения на столбцы
    for bar, size in zip(bars, cluster_sizes.values):
        height = bar.get_height()
        axes[1, 1].text(bar.get_x() + bar.get_width()/2., height + 5,
                        f'{size}', ha='center', va='bottom', fontweight='bold')
    
    axes[1, 1].set_title('📊 Размеры кластеров')
    axes[1, 1].set_xlabel('Номер кластера')
    axes[1, 1].set_ylabel('Количество клиентов')
    axes[1, 1].set_xticks(range(len(cluster_sizes)))
    axes[1, 1].grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.show()

def analyze_clusters(data_with_clusters):
    """Анализирует профили кластеров"""
    print("\n📋 Анализ профилей кластеров:")
    print("=" * 50)
    
    # Создаем профили кластеров
    features = ['age', 'income', 'spending']
    cluster_profiles = []
    
    for cluster_id in sorted(data_with_clusters['cluster'].unique()):
        cluster_data = data_with_clusters[data_with_clusters['cluster'] == cluster_id]
        
        profile = {
            'Кластер': cluster_id,
            'Размер': len(cluster_data),
            'Доля (%)': f"{len(cluster_data) / len(data_with_clusters) * 100:.1f}%"
        }
        
        for feature in features:
            profile[f'Средний {feature}'] = cluster_data[feature].mean()
            profile[f'Стд {feature}'] = cluster_data[feature].std()
        
        cluster_profiles.append(profile)
    
    profiles_df = pd.DataFrame(cluster_profiles)
    print(profiles_df.round(1))
    
    # Присваиваем бизнес-названия кластерам
    print(f"\n🏷️ Бизнес-интерпретация кластеров:")
    business_names = assign_business_names(profiles_df)
    
    for i, name in enumerate(business_names):
        size = profiles_df[profiles_df['Кластер'] == i]['Размер'].iloc[0]
        percentage = profiles_df[profiles_df['Кластер'] == i]['Доля (%)'].iloc[0]
        print(f"  Кластер {i}: '{name}' ({size} клиентов, {percentage})")
    
    return profiles_df, business_names

def assign_business_names(profiles_df):
    """Присваивает бизнес-названия кластерам на основе их характеристик"""
    names = []
    
    for _, profile in profiles_df.iterrows():
        avg_age = profile['Средний age']
        avg_income = profile['Средний income'] 
        avg_spending = profile['Средний spending']
        
        # Логика присвоения названий
        if avg_income > 90 and avg_spending > 60:
            name = "💎 VIP клиенты"
        elif avg_age < 35 and avg_income > 80:
            name = "🚀 Молодые профессионалы"
        elif avg_age > 50 and avg_income > 70:
            name = "🏆 Зрелые состоятельные"
        elif avg_spending < 30:
            name = "💰 Экономные покупатели"
        elif avg_age < 35:
            name = "🌱 Молодые начинающие"
        else:
            name = "👥 Средний класс"
        
        names.append(name)
    
    return names

def create_marketing_strategies(profiles_df, business_names):
    """Создает маркетинговые стратегии для каждого сегмента"""
    print(f"\n🎯 МАРКЕТИНГОВЫЕ СТРАТЕГИИ ПО СЕГМЕНТАМ:")
    print("=" * 60)
    
    strategies = {
        "💎 VIP клиенты": {
            "strategy": "Персональный сервис и эксклюзивные предложения",
            "channels": "Персональный менеджер, VIP-мероприятия",
            "offers": "Премиум товары, эксклюзивы, персональные скидки",
            "expected_conversion": "15-20%"
        },
        "🚀 Молодые профессионалы": {
            "strategy": "Удобство и инновации",
            "channels": "Мобильные приложения, социальные сети",
            "offers": "Технологичные товары, подписки, быстрая доставка",
            "expected_conversion": "8-12%"
        },
        "🏆 Зрелые состоятельные": {
            "strategy": "Качество и надежность",
            "channels": "Email, каталоги, личные консультации",
            "offers": "Качественные товары, гарантии, семейные предложения",
            "expected_conversion": "10-15%"
        },
        "💰 Экономные покупатели": {
            "strategy": "Акции и выгодные предложения",
            "channels": "SMS, промо-рассылки, соцсети",
            "offers": "Скидки, распродажи, программы лояльности",
            "expected_conversion": "5-8%"
        },
        "🌱 Молодые начинающие": {
            "strategy": "Доступность и образование",
            "channels": "Социальные сети, блоги, мессенджеры",
            "offers": "Доступные товары, рассрочка, обучающий контент",
            "expected_conversion": "6-10%"
        },
        "👥 Средний класс": {
            "strategy": "Универсальные предложения",
            "channels": "Email, интернет-реклама, магазины",
            "offers": "Стандартный ассортимент, умеренные скидки",
            "expected_conversion": "7-11%"
        }
    }
    
    for i, name in enumerate(business_names):
        if name in strategies:
            strategy = strategies[name]
            size = profiles_df[profiles_df['Кластер'] == i]['Размер'].iloc[0]
            
            print(f"\n{name} ({size} клиентов):")
            print(f"  📈 Стратегия: {strategy['strategy']}")
            print(f"  📱 Каналы: {strategy['channels']}")
            print(f"  🎁 Предложения: {strategy['offers']}")
            print(f"  📊 Ожидаемая конверсия: {strategy['expected_conversion']}")

def demonstrate_new_customer_prediction(kmeans, scaler):
    """Демонстрирует предсказание кластера для новых клиентов"""
    print(f"\n🔮 ПРЕДСКАЗАНИЕ СЕГМЕНТА ДЛЯ НОВЫХ КЛИЕНТОВ:")
    print("=" * 55)
    
    # Примеры новых клиентов
    new_customers = pd.DataFrame({
        'age': [28, 45, 60, 35],
        'income': [85, 65, 120, 45],
        'spending': [50, 40, 90, 25]
    })
    
    print("Новые клиенты для сегментации:")
    print(new_customers)
    
    # Предсказываем кластеры
    new_customers_scaled = scaler.transform(new_customers[['age', 'income', 'spending']])
    predicted_clusters = kmeans.predict(new_customers_scaled)
    
    print(f"\nПредсказанные сегменты:")
    for i, cluster in enumerate(predicted_clusters):
        customer_info = new_customers.iloc[i]
        print(f"  Клиент {i+1} (возраст: {customer_info['age']}, "
              f"доход: {customer_info['income']}, траты: {customer_info['spending']}) "
              f"→ Кластер {cluster}")

def main():
    """Основная функция демонстрации K-means"""
    print("🚀 Запуск демонстрации K-means кластеризации!")
    
    # 1. Генерируем данные
    data = generate_sample_data()
    print(f"✅ Сгенерировано {len(data)} записей клиентов")
    
    # 2. Визуализируем исходные данные
    visualize_data(data, "📊 Исходные данные клиентов")
    
    # 3. Находим оптимальное количество кластеров
    features = ['age', 'income', 'spending']
    X_scaled, scaler, optimal_k = find_optimal_clusters(data, features)
    
    # 4. Выполняем кластеризацию
    data_with_clusters, kmeans = perform_kmeans_clustering(data, X_scaled, optimal_k)
    
    # 5. Визуализируем результаты
    visualize_clusters(data_with_clusters, kmeans, X_scaled)
    
    # 6. Анализируем профили кластеров
    profiles_df, business_names = analyze_clusters(data_with_clusters)
    
    # 7. Создаем маркетинговые стратегии
    create_marketing_strategies(profiles_df, business_names)
    
    # 8. Демонстрируем предсказание для новых клиентов
    demonstrate_new_customer_prediction(kmeans, scaler)
    
    print(f"\n🎉 Демонстрация K-means завершена!")
    print("📚 Следующий шаг: изучите hierarchical_clustering.py")
    print("💡 Совет: экспериментируйте с разными количествами кластеров!")
    
    return data_with_clusters, kmeans, scaler

if __name__ == "__main__":
    results = main()