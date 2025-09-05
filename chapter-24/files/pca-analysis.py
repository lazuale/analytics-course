"""
🔍 PCA Analysis Template
Шаблон для анализа главных компонент (Principal Component Analysis)

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
import warnings
warnings.filterwarnings('ignore')

# Настройка стиля графиков
plt.style.use('default')
sns.set_palette("husl")

class PCAAnalyzer:
    """
    Класс для проведения анализа главных компонент
    """
    
    def __init__(self):
        self.data = None
        self.features = None
        self.features_scaled = None
        self.pca_model = None
        self.components = None
        self.feature_names = None
        
    def load_and_preprocess_data(self, file_path, id_column='customer_id'):
        """
        Загружает и предобрабатывает данные для PCA
        
        Parameters:
        -----------
        file_path : str
            Путь к CSV файлу
        id_column : str
            Название колонки с идентификаторами
        """
        print("📊 Загрузка данных...")
        
        # Загружаем данные с правильными разделителями
        self.data = pd.read_csv(file_path, sep=';', decimal=',')
        print(f"✅ Загружено {len(self.data)} записей с {len(self.data.columns)} переменными")
        
        # Выделяем числовые переменные (исключаем ID)
        self.features = self.data.drop(columns=[id_column])
        self.feature_names = list(self.features.columns)
        
        # Проверяем данные
        print("\n🔍 Проверка данных:")
        print(f"Пропущенные значения: {self.features.isnull().sum().sum()}")
        print(f"Дублированные строки: {self.features.duplicated().sum()}")
        
        # Базовая статистика
        print("\n📈 Описательная статистика:")
        print(self.features.describe().round(2))
        
        return self.features
    
    def standardize_features(self):
        """
        Стандартизирует признаки (обязательно для PCA!)
        """
        print("\n⚖️ Стандартизация данных...")
        
        scaler = StandardScaler()
        self.features_scaled = scaler.fit_transform(self.features)
        
        print("✅ Данные стандартизированы (среднее=0, стандартное отклонение=1)")
        
        # Проверяем стандартизацию
        scaled_df = pd.DataFrame(self.features_scaled, columns=self.feature_names)
        print(f"Проверка: среднее = {scaled_df.mean().mean():.6f}")
        print(f"Проверка: стд. отклонение = {scaled_df.std().mean():.6f}")
        
        return self.features_scaled
    
    def perform_pca(self, n_components=None, variance_threshold=0.85):
        """
        Выполняет анализ главных компонент
        
        Parameters:
        -----------
        n_components : int or None
            Количество компонент (если None, определяется автоматически)
        variance_threshold : float
            Порог объясненной изменчивости для автоматического выбора
        """
        print("\n🔍 Анализ главных компонент...")
        
        if n_components is None:
            # Сначала фиттим полную PCA для определения количества компонент
            pca_full = PCA()
            pca_full.fit(self.features_scaled)
            
            # Находим количество компонент для заданного порога
            cumsum = np.cumsum(pca_full.explained_variance_ratio_)
            n_components = np.argmax(cumsum >= variance_threshold) + 1
            
            print(f"🎯 Для {variance_threshold:.0%} изменчивости нужно {n_components} компонент")
        
        # Применяем PCA с выбранным количеством компонент
        self.pca_model = PCA(n_components=n_components)
        self.components = self.pca_model.fit_transform(self.features_scaled)
        
        print(f"✅ PCA выполнен: {n_components} компонент")
        print(f"📊 Объясненная изменчивость: {self.pca_model.explained_variance_ratio_.sum():.1%}")
        
        return self.components
    
    def plot_scree(self, save_path=None):
        """
        Строит scree plot для выбора количества компонент
        """
        # Получаем полную PCA для scree plot
        pca_full = PCA()
        pca_full.fit(self.features_scaled)
        
        plt.figure(figsize=(12, 6))
        
        # Scree plot
        plt.subplot(1, 2, 1)
        plt.plot(range(1, len(pca_full.explained_variance_ratio_) + 1), 
                pca_full.explained_variance_ratio_, 'bo-', linewidth=2, markersize=8)
        plt.title('🔍 Scree Plot: Изменчивость по компонентам', fontsize=14, fontweight='bold')
        plt.xlabel('Номер компоненты')
        plt.ylabel('Объясненная изменчивость')
        plt.grid(True, alpha=0.3)
        
        # Кумулятивная изменчивость
        plt.subplot(1, 2, 2)
        cumsum = np.cumsum(pca_full.explained_variance_ratio_)
        plt.plot(range(1, len(cumsum) + 1), cumsum, 'ro-', linewidth=2, markersize=8)
        plt.axhline(y=0.8, color='orange', linestyle='--', label='80%')
        plt.axhline(y=0.85, color='red', linestyle='--', label='85%')
        plt.axhline(y=0.9, color='darkred', linestyle='--', label='90%')
        plt.title('📈 Кумулятивная изменчивость', fontsize=14, fontweight='bold')
        plt.xlabel('Номер компоненты')
        plt.ylabel('Кумулятивная изменчивость')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()
    
    def analyze_loadings(self, top_n=3):
        """
        Анализирует нагрузки переменных на компоненты
        
        Parameters:
        -----------
        top_n : int
            Количество топ переменных для каждой компоненты
        """
        print("\n📋 Анализ нагрузок компонент:")
        
        # Создаем DataFrame с нагрузками
        loadings_df = pd.DataFrame(
            self.pca_model.components_.T,
            columns=[f'PC{i+1}' for i in range(self.pca_model.n_components_)],
            index=self.feature_names
        )
        
        for i in range(self.pca_model.n_components_):
            pc_name = f'PC{i+1}'
            variance_explained = self.pca_model.explained_variance_ratio_[i]
            
            print(f"\n🎯 {pc_name} (объясняет {variance_explained:.1%} изменчивости):")
            
            # Топ положительных нагрузок
            top_positive = loadings_df[pc_name].nlargest(top_n)
            print(f"  ⬆️ Положительные нагрузки:")
            for var, loading in top_positive.items():
                print(f"     {var}: {loading:.3f}")
            
            # Топ отрицательных нагрузок
            top_negative = loadings_df[pc_name].nsmallest(top_n)
            print(f"  ⬇️ Отрицательные нагрузки:")
            for var, loading in top_negative.items():
                print(f"     {var}: {loading:.3f}")
        
        return loadings_df


def main():
    """
    Основная функция для демонстрации использования PCAAnalyzer
    """
    print("🚀 Запуск анализа главных компонент")
    print("="*50)
    
    # Создаем анализатор
    analyzer = PCAAnalyzer()
    
    # Загружаем данные
    analyzer.load_and_preprocess_data('customers_data.csv')
    
    # Стандартизируем
    analyzer.standardize_features()
    
    # Строим scree plot
    analyzer.plot_scree()
    
    # Выполняем PCA
    analyzer.perform_pca(variance_threshold=0.85)
    
    # Анализируем нагрузки
    loadings = analyzer.analyze_loadings()
    
    print("\n🎉 Анализ завершен!")
    return analyzer


if __name__ == "__main__":
    analyzer = main()