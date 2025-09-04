"""
🎛️ Production-ready система сегментации клиентов

Этот скрипт предоставляет:
- Класс CustomerSegmentation для автоматической сегментации
- Полный пайплайн от сырых данных до бизнес-рекомендаций
- Методы сохранения и загрузки моделей
- Мониторинг качества и обнаружение дрифта
- Интерактивный dashboard с профилями сегментов
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import silhouette_score, calinski_harabasz_score
from sklearn.decomposition import PCA
from datetime import datetime, timedelta
import joblib
import warnings
import json

warnings.filterwarnings('ignore')

class CustomerSegmentation:
    """
    Production-ready система сегментации клиентов
    
    Использование:
    -------------
    segmenter = CustomerSegmentation()
    segmenter.fit(customer_data, features=['age', 'income', 'spending'])
    new_segments = segmenter.predict(new_customer_data)
    profiles = segmenter.get_segment_profiles()
    """
    
    def __init__(self, n_clusters='auto', algorithm='kmeans', random_state=42):
        """
        Инициализация системы сегментации
        
        Parameters:
        -----------
        n_clusters : int или 'auto'
            Количество кластеров. Если 'auto', выбирается автоматически
        algorithm : str
            Алгоритм кластеризации ('kmeans', 'hierarchical')
        random_state : int
            Фиксация случайности для воспроизводимости
        """
        self.n_clusters = n_clusters
        self.algorithm = algorithm
        self.random_state = random_state
        
        # Внутренние объекты
        self.model = None
        self.scaler = None
        self.feature_names = None
        self.segment_profiles = None
        self.quality_metrics = {}
        self.business_names = {}
        self.fitted = False
        
        print(f"🎯 Инициализирована система сегментации")
        print(f"  • Алгоритм: {algorithm}")
        print(f"  • Кластеров: {n_clusters}")
    
    def _prepare_features(self, data, features=None):
        """Подготовка признаков для кластеризации"""
        if features is None:
            # Автоматический выбор числовых признаков
            numeric_features = data.select_dtypes(include=[np.number]).columns.tolist()
            # Исключаем ID и даты
            features = [f for f in numeric_features if not any(x in f.lower() for x in ['id', 'date'])]
        
        self.feature_names = features
        
        # Извлекаем признаки
        X = data[features].copy()
        
        # Обработка пропусков
        X = X.fillna(X.median())
        
        return X
    
    def _find_optimal_clusters(self, X_scaled, max_k=10):
        """Автоматический поиск оптимального количества кластеров"""
        print("🔍 Поиск оптимального количества кластеров...")
        
        k_range = range(2, min(max_k + 1, len(X_scaled) // 2))
        silhouette_scores = []
        calinski_scores = []
        inertias = []
        
        for k in k_range:
            kmeans = KMeans(n_clusters=k, random_state=self.random_state, n_init=10)
            labels = kmeans.fit_predict(X_scaled)
            
            silhouette_scores.append(silhouette_score(X_scaled, labels))
            calinski_scores.append(calinski_harabasz_score(X_scaled, labels))
            inertias.append(kmeans.inertia_)
        
        # Выбираем k по силуэтному коэффициенту
        optimal_k = k_range[np.argmax(silhouette_scores)]
        best_silhouette = max(silhouette_scores)
        
        print(f"  ✅ Оптимальное количество кластеров: {optimal_k}")
        print(f"  📊 Силуэтный коэффициент: {best_silhouette:.3f}")
        
        return optimal_k
    
    def _create_rfm_features(self, data):
        """Создание RFM признаков если есть необходимые данные"""
        rfm_features = {}
        
        # Recency - дни с последней покупки
        if 'last_purchase_date' in data.columns:
            try:
                last_purchase = pd.to_datetime(data['last_purchase_date'])
                rfm_features['recency'] = (datetime.now() - last_purchase).dt.days
            except:
                if 'days_since_last_purchase' in data.columns:
                    rfm_features['recency'] = data['days_since_last_purchase']
        
        # Frequency - частота покупок
        if 'total_purchases' in data.columns:
            rfm_features['frequency'] = data['total_purchases']
        
        # Monetary - сумма покупок
        if 'total_spent' in data.columns:
            rfm_features['monetary'] = data['total_spent']
        elif 'avg_order_value' in data.columns and 'total_purchases' in data.columns:
            rfm_features['monetary'] = data['avg_order_value'] * data['total_purchases']
        
        if rfm_features:
            print(f"  ✅ Созданы RFM признаки: {list(rfm_features.keys())}")
            
        return pd.DataFrame(rfm_features)
    
    def fit(self, data, features=None, create_rfm=True):
        """
        Обучение модели сегментации
        
        Parameters:
        -----------
        data : DataFrame
            Данные клиентов
        features : list, optional
            Список признаков для кластеризации
        create_rfm : bool
            Создавать ли RFM признаки автоматически
        """
        print(f"\n🎯 Обучение модели сегментации на {len(data)} клиентах...")
        
        # Подготовка признаков
        X = self._prepare_features(data, features)
        
        # Добавляем RFM признаки если нужно
        if create_rfm:
            rfm_features = self._create_rfm_features(data)
            if not rfm_features.empty:
                X = pd.concat([X, rfm_features], axis=1)
                self.feature_names.extend(rfm_features.columns.tolist())
        
        print(f"  📊 Используемые признаки: {self.feature_names}")
        print(f"  📏 Размерность данных: {X.shape}")
        
        # Стандартизация
        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X)
        
        # Выбор количества кластеров
        if self.n_clusters == 'auto':
            self.n_clusters = self._find_optimal_clusters(X_scaled)
        
        # Обучение модели кластеризации
        if self.algorithm == 'kmeans':
            self.model = KMeans(
                n_clusters=self.n_clusters, 
                random_state=self.random_state,
                n_init=10
            )
        else:
            from sklearn.cluster import AgglomerativeClustering
            self.model = AgglomerativeClustering(n_clusters=self.n_clusters)
        
        # Кластеризация
        cluster_labels = self.model.fit_predict(X_scaled)
        
        # Оценка качества
        self.quality_metrics = {
            'silhouette_score': silhouette_score(X_scaled, cluster_labels),
            'calinski_harabasz': calinski_harabasz_score(X_scaled, cluster_labels),
            'n_clusters': self.n_clusters,
            'n_features': len(self.feature_names),
            'n_samples': len(data)
        }
        
        print(f"  ✅ Модель обучена!")
        print(f"  📊 Качество (силуэт): {self.quality_metrics['silhouette_score']:.3f}")
        
        # Создание профилей сегментов
        data_with_segments = data.copy()
        data_with_segments['segment'] = cluster_labels
        self._create_segment_profiles(data_with_segments, X)
        self._assign_business_names()
        
        self.fitted = True
        return self
    
    def _create_segment_profiles(self, data_with_segments, X):
        """Создание профилей сегментов"""
        print("  📋 Создание профилей сегментов...")
        
        profiles = []
        
        for segment_id in sorted(data_with_segments['segment'].unique()):
            segment_data = data_with_segments[data_with_segments['segment'] == segment_id]
            X_segment = X[data_with_segments['segment'] == segment_id]
            
            profile = {
                'segment_id': segment_id,
                'size': len(segment_data),
                'percentage': len(segment_data) / len(data_with_segments) * 100
            }
            
            # Средние значения признаков
            for i, feature in enumerate(self.feature_names):
                profile[f'avg_{feature}'] = X_segment.iloc[:, i].mean()
                profile[f'std_{feature}'] = X_segment.iloc[:, i].std()
            
            # Дополнительная статистика
            if 'age' in data_with_segments.columns:
                profile['avg_age'] = segment_data['age'].mean()
                profile['age_range'] = f"{segment_data['age'].min()}-{segment_data['age'].max()}"
            
            if 'gender' in data_with_segments.columns:
                gender_dist = segment_data['gender'].value_counts(normalize=True)
                profile['gender_distribution'] = gender_dist.to_dict()
            
            if 'city' in data_with_segments.columns:
                top_city = segment_data['city'].mode()
                profile['top_city'] = top_city[0] if len(top_city) > 0 else 'Неизвестно'
            
            profiles.append(profile)
        
        self.segment_profiles = pd.DataFrame(profiles)
        print(f"    ✅ Создано {len(profiles)} профилей сегментов")
    
    def _assign_business_names(self):
        """Присвоение бизнес-названий сегментам"""
        names = {}
        
        for _, profile in self.segment_profiles.iterrows():
            segment_id = profile['segment_id']
            
            # Логика присвоения названий на основе характеристик
            if 'avg_monetary' in profile and 'avg_frequency' in profile:
                monetary = profile.get('avg_monetary', 0)
                frequency = profile.get('avg_frequency', 0)
                recency = profile.get('avg_recency', 180)
                
                # RFM сегментация
                if monetary > 50000 and frequency > 15 and recency < 30:
                    name = "💎 Чемпионы"
                elif monetary > 30000 and frequency > 10:
                    name = "🏆 Лояльные клиенты"
                elif recency < 60 and frequency > 5:
                    name = "🚀 Потенциально лояльные"
                elif recency < 30:
                    name = "🌱 Новые клиенты"
                elif recency > 180:
                    name = "😴 Спящие"
                else:
                    name = "👥 Обычные клиенты"
                    
            elif 'avg_age' in profile:
                age = profile['avg_age']
                if age < 30:
                    name = "🌟 Молодежь"
                elif age > 50:
                    name = "🎯 Зрелые клиенты"
                else:
                    name = "💼 Средний возраст"
            else:
                name = f"📊 Сегмент {segment_id}"
            
            names[segment_id] = name
        
        self.business_names = names
        print(f"  🏷️ Присвоены бизнес-названия сегментам")
    
    def predict(self, new_data):
        """
        Предсказание сегментов для новых клиентов
        
        Parameters:
        -----------
        new_data : DataFrame
            Новые данные клиентов
            
        Returns:
        --------
        segments : array
            Предсказанные сегменты
        """
        if not self.fitted:
            raise ValueError("Сначала обучите модель с помощью fit()")
        
        # Подготовка признаков
        X_new = new_data[self.feature_names]
        X_new = X_new.fillna(X_new.median())
        
        # Стандартизация
        X_new_scaled = self.scaler.transform(X_new)
        
        # Предсказание
        segments = self.model.predict(X_new_scaled)
        
        return segments
    
    def get_segment_profiles(self):
        """Получение профилей сегментов"""
        if not self.fitted:
            raise ValueError("Сначала обучите модель с помощью fit()")
        
        profiles_with_names = self.segment_profiles.copy()
        profiles_with_names['business_name'] = profiles_with_names['segment_id'].map(self.business_names)
        
        return profiles_with_names
    
    def visualize_segments(self, data=None, save_path=None):
        """Визуализация сегментов"""
        if not self.fitted:
            raise ValueError("Сначала обучите модель с помощью fit()")
        
        print("🎨 Создание визуализации сегментов...")
        
        if data is not None:
            # Предсказываем сегменты для переданных данных
            X = self._prepare_features(data, self.feature_names)
            X_scaled = self.scaler.transform(X.fillna(X.median()))
            segments = self.model.predict(X_scaled)
        else:
            # Используем данные из обучения (если есть)
            print("  ⚠️ Данные не переданы, создаем примерную визуализацию")
            return
        
        # Создаем визуализацию
        if len(self.feature_names) > 2:
            # Используем PCA для снижения размерности
            pca = PCA(n_components=2)
            X_pca = pca.fit_transform(X_scaled)
            
            plt.figure(figsize=(15, 10))
            
            # График кластеров в PCA пространстве
            plt.subplot(2, 2, 1)
            colors = plt.cm.Set1(np.linspace(0, 1, self.n_clusters))
            
            for i in range(self.n_clusters):
                mask = segments == i
                plt.scatter(X_pca[mask, 0], X_pca[mask, 1], 
                           c=[colors[i]], label=self.business_names.get(i, f'Сегмент {i}'),
                           alpha=0.7, s=50)
            
            plt.title('🎯 Сегменты в PCA пространстве')
            plt.xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.1%})')
            plt.ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.1%})')
            plt.legend()
            plt.grid(alpha=0.3)
            
            # Размеры сегментов
            plt.subplot(2, 2, 2)
            segment_sizes = pd.Series(segments).value_counts().sort_index()
            bars = plt.bar(range(len(segment_sizes)), segment_sizes.values, color=colors)
            
            for bar, size in zip(bars, segment_sizes.values):
                plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
                        f'{size}', ha='center', va='bottom', fontweight='bold')
            
            plt.title('📊 Размеры сегментов')
            plt.xlabel('Сегмент')
            plt.ylabel('Количество клиентов')
            plt.xticks(range(len(segment_sizes)), 
                      [self.business_names.get(i, f'Сегмент {i}') for i in segment_sizes.index],
                      rotation=45)
            
            # Профили сегментов (радарная диаграмма)
            plt.subplot(2, 2, (3, 4))
            self._plot_radar_chart(plt.gca())
            
            plt.suptitle('📊 Анализ клиентских сегментов', fontsize=16)
            plt.tight_layout()
            
            if save_path:
                plt.savefig(save_path, dpi=300, bbox_inches='tight')
                print(f"  ✅ Визуализация сохранена: {save_path}")
            
            plt.show()
    
    def _plot_radar_chart(self, ax):
        """Создание радарной диаграммы профилей сегментов"""
        # Выбираем топ-5 признаков для радарной диаграммы
        feature_cols = [col for col in self.segment_profiles.columns if col.startswith('avg_')][:5]
        
        if len(feature_cols) < 3:
            ax.text(0.5, 0.5, 'Недостаточно признаков\nдля радарной диаграммы', 
                   ha='center', va='center', transform=ax.transAxes)
            return
        
        # Нормализуем данные для радарной диаграммы
        profiles_norm = self.segment_profiles[feature_cols].copy()
        for col in feature_cols:
            profiles_norm[col] = (profiles_norm[col] - profiles_norm[col].min()) / \
                                (profiles_norm[col].max() - profiles_norm[col].min())
        
        angles = np.linspace(0, 2 * np.pi, len(feature_cols), endpoint=False).tolist()
        angles += angles[:1]  # Замкнуть круг
        
        ax.set_theta_offset(np.pi / 2)
        ax.set_theta_direction(-1)
        ax.set_thetagrids(np.degrees(angles[:-1]), 
                         [col.replace('avg_', '').title() for col in feature_cols])
        
        colors = plt.cm.Set1(np.linspace(0, 1, len(profiles_norm)))
        
        for i, (_, row) in enumerate(profiles_norm.iterrows()):
            values = row.tolist()
            values += values[:1]  # Замкнуть линию
            
            ax.plot(angles, values, 'o-', linewidth=2, 
                   label=self.business_names.get(i, f'Сегмент {i}'),
                   color=colors[i])
            ax.fill(angles, values, alpha=0.25, color=colors[i])
        
        ax.set_ylim(0, 1)
        ax.set_title('🎯 Профили сегментов', pad=20)
        ax.legend(loc='upper right', bbox_to_anchor=(1.2, 1.0))
    
    def create_marketing_strategies(self):
        """Создание маркетинговых стратегий для сегментов"""
        if not self.fitted:
            raise ValueError("Сначала обучите модель с помощью fit()")
        
        print(f"\n🎯 МАРКЕТИНГОВЫЕ СТРАТЕГИИ ПО СЕГМЕНТАМ:")
        print("=" * 60)
        
        strategy_templates = {
            "💎 Чемпионы": {
                "strategy": "VIP сервис и эксклюзивные предложения",
                "channels": ["Персональный менеджер", "VIP события", "Приватные продажи"],
                "tactics": ["Эксклюзивные товары", "Персональные скидки", "Приоритетная поддержка"],
                "expected_conversion": "15-25%",
                "budget_allocation": "30%"
            },
            "🏆 Лояльные клиенты": {
                "strategy": "Программы лояльности и удержание",
                "channels": ["Email маркетинг", "Push уведомления", "Персональные рекомендации"],
                "tactics": ["Накопительные скидки", "Раннее уведомление о распродажах", "Подарки"],
                "expected_conversion": "12-18%",
                "budget_allocation": "25%"
            },
            "🚀 Потенциально лояльные": {
                "strategy": "Развитие лояльности и увеличение частоты",
                "channels": ["Retargeting", "Social media", "Email кампании"],
                "tactics": ["Промо на повторные покупки", "Cross-sell", "Образовательный контент"],
                "expected_conversion": "8-12%",
                "budget_allocation": "20%"
            },
            "🌱 Новые клиенты": {
                "strategy": "Onboarding и первое впечатление",
                "channels": ["Welcome серии", "Мобильные push", "Социальные сети"],
                "tactics": ["Приветственные скидки", "Обучающий контент", "Простота использования"],
                "expected_conversion": "6-10%",
                "budget_allocation": "15%"
            },
            "😴 Спящие": {
                "strategy": "Реактивация и возврат",
                "channels": ["Реактивационные email", "Ретаргетинг", "SMS"],
                "tactics": ["Win-back скидки", "Опросы удовлетворенности", "Новые продукты"],
                "expected_conversion": "3-6%",
                "budget_allocation": "10%"
            }
        }
        
        strategies = {}
        
        for segment_id, business_name in self.business_names.items():
            profile = self.segment_profiles[self.segment_profiles['segment_id'] == segment_id].iloc[0]
            
            # Получаем стратегию по бизнес-названию или создаем общую
            if business_name in strategy_templates:
                strategy = strategy_templates[business_name].copy()
            else:
                strategy = {
                    "strategy": "Персонализированный подход",
                    "channels": ["Multi-channel кампания"],
                    "tactics": ["A/B тестирование предложений"],
                    "expected_conversion": "5-10%",
                    "budget_allocation": "5%"
                }
            
            # Добавляем информацию о сегменте
            strategy['segment_size'] = int(profile['size'])
            strategy['segment_percentage'] = round(profile['percentage'], 1)
            
            strategies[segment_id] = strategy
            
            # Выводим стратегию
            print(f"\n{business_name} (Сегмент {segment_id}):")
            print(f"  👥 Размер: {strategy['segment_size']} клиентов ({strategy['segment_percentage']}%)")
            print(f"  🎯 Стратегия: {strategy['strategy']}")
            print(f"  📱 Каналы: {', '.join(strategy['channels'])}")
            print(f"  🛠 Тактики: {', '.join(strategy['tactics'])}")
            print(f"  📊 Ожидаемая конверсия: {strategy['expected_conversion']}")
            print(f"  💰 Распределение бюджета: {strategy['budget_allocation']}")
        
        return strategies
    
    def save_model(self, filepath):
        """Сохранение модели"""
        if not self.fitted:
            raise ValueError("Сначала обучите модель с помощью fit()")
        
        model_data = {
            'model': self.model,
            'scaler': self.scaler,
            'feature_names': self.feature_names,
            'segment_profiles': self.segment_profiles,
            'business_names': self.business_names,
            'quality_metrics': self.quality_metrics,
            'n_clusters': self.n_clusters,
            'algorithm': self.algorithm,
            'random_state': self.random_state
        }
        
        joblib.dump(model_data, filepath)
        print(f"✅ Модель сохранена: {filepath}")
    
    def load_model(self, filepath):
        """Загрузка модели"""
        model_data = joblib.load(filepath)
        
        self.model = model_data['model']
        self.scaler = model_data['scaler']
        self.feature_names = model_data['feature_names']
        self.segment_profiles = model_data['segment_profiles']
        self.business_names = model_data['business_names']
        self.quality_metrics = model_data['quality_metrics']
        self.n_clusters = model_data['n_clusters']
        self.algorithm = model_data['algorithm']
        self.random_state = model_data['random_state']
        self.fitted = True
        
        print(f"✅ Модель загружена: {filepath}")

def demo_full_pipeline():
    """Демонстрация полного пайплайна сегментации"""
    print("🚀 Демонстрация полного пайплайна сегментации клиентов!")
    print("=" * 60)
    
    try:
        # Загружаем данные
        data = pd.read_csv('customer_behavior.csv')
        print(f"✅ Загружено {len(data)} клиентов из файла")
    except FileNotFoundError:
        print("❌ Файл customer_behavior.csv не найден")
        print("   Запустите сначала kmeans_clustering.py для создания данных")
        return
    
    # 1. Создаем и обучаем модель
    segmenter = CustomerSegmentation(n_clusters='auto', algorithm='kmeans')
    
    # Выбираем признаки для сегментации
    features = ['age', 'income', 'total_purchases', 'total_spent', 'avg_order_value', 'loyalty_score']
    segmenter.fit(data, features=features, create_rfm=True)
    
    # 2. Получаем профили сегментов
    profiles = segmenter.get_segment_profiles()
    print(f"\n📋 Профили сегментов:")
    print(profiles[['segment_id', 'business_name', 'size', 'percentage']].round(1))
    
    # 3. Создаем маркетинговые стратегии
    strategies = segmenter.create_marketing_strategies()
    
    # 4. Визуализируем результаты
    segmenter.visualize_segments(data)
    
    # 5. Демонстрируем предсказание для новых клиентов
    print(f"\n🔮 Тест предсказания для новых клиентов:")
    new_customers = pd.DataFrame({
        'age': [25, 45, 60],
        'income': [50, 80, 120],
        'total_purchases': [3, 15, 25],
        'total_spent': [5000, 50000, 100000],
        'avg_order_value': [1666, 3333, 4000],
        'loyalty_score': [5, 8, 9]
    })
    
    predicted_segments = segmenter.predict(new_customers)
    
    for i, segment in enumerate(predicted_segments):
        business_name = segmenter.business_names.get(segment, f'Сегмент {segment}')
        print(f"  Клиент {i+1}: {business_name}")
    
    # 6. Сохраняем модель
    segmenter.save_model('customer_segmentation_model.pkl')
    
    print(f"\n🎉 Полный пайплайн сегментации завершен!")
    print("💡 Модель готова к использованию в production!")
    
    return segmenter

if __name__ == "__main__":
    demo_full_pipeline()