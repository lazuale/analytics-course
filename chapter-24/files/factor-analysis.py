"""
🧩 Factor Analysis Template
Шаблон для факторного анализа (Factor Analysis)

Автор: Analytics Course
Глава: 24 - Мультивариантный анализ
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import FactorAnalysis
from factor_analyzer import FactorAnalyzer
from factor_analyzer.factor_analyzer import calculate_bartlett_sphericity, calculate_kmo
import warnings
warnings.filterwarnings('ignore')

# Настройка стиля графиков
plt.style.use('default')
sns.set_palette("viridis")

class FactorAnalysisToolkit:
    """
    Комплексный инструментарий для факторного анализа
    """
    
    def __init__(self):
        self.data = None
        self.features = None
        self.fa_model = None
        self.loadings = None
        self.feature_names = None
        self.n_factors = None
        
    def load_data(self, file_path, id_column='employee_id'):
        """
        Загружает данные для факторного анализа
        
        Parameters:
        -----------
        file_path : str
            Путь к CSV файлу
        id_column : str
            Название колонки с идентификаторами
        """
        print("📊 Загрузка данных для факторного анализа...")
        
        # Загружаем данные
        self.data = pd.read_csv(file_path, sep=';', decimal=',')
        print(f"✅ Загружено {len(self.data)} записей с {len(self.data.columns)} переменными")
        
        # Выделяем числовые переменные
        self.features = self.data.drop(columns=[id_column])
        self.feature_names = list(self.features.columns)
        
        # Базовая информация
        print(f"📋 Переменные для анализа: {len(self.feature_names)}")
        print(f"🔍 Пропущенные значения: {self.features.isnull().sum().sum()}")
        
        return self.features
    
    def check_data_adequacy(self):
        """
        Проверяет пригодность данных для факторного анализа
        """
        print("\n🔍 Проверка пригодности данных для факторного анализа...")
        
        # Тест Бартлетта на сферичность
        chi_square_value, p_value = calculate_bartlett_sphericity(self.features)
        print(f"\n📊 Тест Бартлетта на сферичность:")
        print(f"   χ² = {chi_square_value:.2f}")
        print(f"   p-value = {p_value:.6f}")
        
        if p_value < 0.05:
            print("   ✅ Данные подходят для факторного анализа (p < 0.05)")
        else:
            print("   ❌ Данные НЕ подходят для факторного анализа (p >= 0.05)")
        
        # Критерий КМО (Kaiser-Meyer-Olkin)
        kmo_all, kmo_model = calculate_kmo(self.features)
        print(f"\n🎯 Критерий КМО:")
        print(f"   Общий КМО = {kmo_model:.3f}")
        
        if kmo_model >= 0.8:
            print("   🏆 Отличная пригодность (КМО >= 0.8)")
        elif kmo_model >= 0.7:
            print("   ✅ Хорошая пригодность (КМО >= 0.7)")
        elif kmo_model >= 0.6:
            print("   ⚠️ Средняя пригодность (КМО >= 0.6)")
        elif kmo_model >= 0.5:
            print("   ❌ Плохая пригодность (КМО >= 0.5)")
        else:
            print("   💀 Неприемлемая пригодность (КМО < 0.5)")
        
        # КМО для отдельных переменных
        print("\n📋 КМО для отдельных переменных:")
        for i, var in enumerate(self.feature_names):
            kmo_var = kmo_all[i]
            status = "✅" if kmo_var >= 0.5 else "❌"
            print(f"   {status} {var}: {kmo_var:.3f}")
        
        return chi_square_value, p_value, kmo_model
    
    def determine_n_factors(self, max_factors=None):
        """
        Определяет оптимальное количество факторов
        """
        print("\n🎯 Определение количества факторов...")
        
        if max_factors is None:
            max_factors = min(len(self.feature_names), len(self.features) // 5)
        
        # Создаем факторный анализатор без вращения
        fa = FactorAnalyzer(rotation=None)
        fa.fit(self.features)
        
        # Получаем собственные значения
        eigenvalues, v = fa.get_eigenvalues()
        
        # Правило Кайзера (eigenvalue > 1)
        kaiser_n = np.sum(eigenvalues > 1)
        print(f"📊 Правило Кайзера (eigenvalue > 1): {kaiser_n} факторов")
        
        # Scree plot
        plt.figure(figsize=(10, 6))
        plt.plot(range(1, len(eigenvalues) + 1), eigenvalues, 'bo-', linewidth=2, markersize=8)
        plt.axhline(y=1, color='red', linestyle='--', linewidth=2, label='Eigenvalue = 1')
        plt.title('🧩 Scree Plot для факторного анализа', fontsize=14, fontweight='bold')
        plt.xlabel('Номер фактора')
        plt.ylabel('Собственное значение')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()
        
        # Процент объясненной дисперсии
        print("\n📈 Объясненная дисперсия по факторам:")
        cumulative = 0
        for i, ev in enumerate(eigenvalues[:min(10, len(eigenvalues))]):
            variance_explained = ev / len(self.feature_names) * 100
            cumulative += variance_explained
            print(f"   Фактор {i+1}: {variance_explained:.1f}% (накопленная: {cumulative:.1f}%)")
        
        self.n_factors = kaiser_n
        return kaiser_n, eigenvalues
    
    def perform_factor_analysis(self, n_factors=None, rotation='varimax'):
        """
        Выполняет факторный анализ с вращением
        
        Parameters:
        -----------
        n_factors : int
            Количество факторов
        rotation : str
            Тип вращения ('varimax', 'promax', 'oblimin', None)
        """
        if n_factors is None:
            n_factors = self.n_factors
        
        print(f"\n🧩 Факторный анализ с {n_factors} факторами (вращение: {rotation})...")
        
        # Создаем и обучаем модель
        self.fa_model = FactorAnalyzer(n_factors=n_factors, rotation=rotation)
        self.fa_model.fit(self.features)
        
        # Получаем матрицу нагрузок
        self.loadings = self.fa_model.loadings_
        
        print(f"✅ Факторный анализ завершен")
        
        # Анализ качества
        communalities = self.fa_model.get_communalities()
        uniquenesses = 1 - communalities
        
        print(f"\n📊 Качество факторного решения:")
        print(f"   Средняя общность: {np.mean(communalities):.3f}")
        print(f"   Средняя уникальность: {np.mean(uniquenesses):.3f}")
        
        return self.loadings
    
    def plot_factor_loadings(self, save_path=None):
        """
        Визуализирует матрицу факторных нагрузок
        """
        loadings_df = pd.DataFrame(
            self.loadings,
            index=self.feature_names,
            columns=[f'Фактор {i+1}' for i in range(self.loadings.shape[1])]
        )
        
        plt.figure(figsize=(12, 8))
        sns.heatmap(loadings_df, annot=True, cmap='RdBu_r', center=0,
                   fmt='.2f', square=True, linewidths=0.5,
                   cbar_kws={'label': 'Факторная нагрузка'})
        plt.title('🔥 Матрица факторных нагрузок', fontsize=14, fontweight='bold')
        plt.xlabel('Факторы')
        plt.ylabel('Переменные')
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()
        
        return loadings_df
    
    def interpret_factors(self, threshold=0.3):
        """
        Интерпретирует факторы на основе нагрузок
        
        Parameters:
        -----------
        threshold : float
            Минимальное значение нагрузки для интерпретации
        """
        print(f"\n🎯 Интерпретация факторов (порог нагрузки: {threshold}):")
        
        loadings_df = pd.DataFrame(
            self.loadings,
            index=self.feature_names,
            columns=[f'Фактор {i+1}' for i in range(self.loadings.shape[1])]
        )
        
        for i in range(self.loadings.shape[1]):
            factor_name = f'Фактор {i+1}'
            print(f"\n🧩 {factor_name}:")
            
            # Переменные с высокими нагрузками
            high_loadings = loadings_df[factor_name][abs(loadings_df[factor_name]) >= threshold]
            high_loadings = high_loadings.sort_values(key=abs, ascending=False)
            
            if len(high_loadings) > 0:
                print(f"   📊 Переменные с высокими нагрузками:")
                for var, loading in high_loadings.items():
                    direction = "⬆️" if loading > 0 else "⬇️"
                    print(f"     {direction} {var}: {loading:.3f}")
                
                # Предложение интерпретации
                print(f"   💡 Возможная интерпретация:")
                self._suggest_interpretation(high_loadings, factor_name)
            else:
                print(f"   ⚠️ Нет переменных с нагрузкой выше {threshold}")
        
        return loadings_df
    
    def _suggest_interpretation(self, high_loadings, factor_name):
        """
        Предлагает интерпретацию фактора на основе переменных
        """
        variables = high_loadings.index.tolist()
        
        # Словарь ключевых слов для интерпретации
        interpretations = {
            'salary': 'Материальная мотивация',
            'bonus': 'Материальная мотивация', 
            'pay': 'Материальная мотивация',
            'team': 'Социальный климат',
            'manager': 'Социальный климат',
            'culture': 'Социальный климат',
            'relation': 'Социальный климат',
            'career': 'Развитие и рост',
            'growth': 'Развитие и рост',
            'training': 'Развитие и рост',
            'innovation': 'Развитие и рост',
            'work': 'Условия работы',
            'environment': 'Условия работы',
            'balance': 'Условия работы',
            'stress': 'Условия работы'
        }
        
        # Подсчитываем вхождения ключевых слов
        counts = {}
        for var in variables:
            var_lower = var.lower()
            for keyword, interpretation in interpretations.items():
                if keyword in var_lower:
                    counts[interpretation] = counts.get(interpretation, 0) + 1
        
        if counts:
            most_likely = max(counts, key=counts.get)
            print(f"     🎯 Вероятная интерпретация: '{most_likely}'")
        else:
            print(f"     🤔 Требует дополнительного анализа предметной области")
    
    def analyze_communalities(self):
        """
        Анализирует общности переменных
        """
        communalities = self.fa_model.get_communalities()
        
        print("\n📊 Анализ общностей (communalities):")
        comm_df = pd.DataFrame({
            'Переменная': self.feature_names,
            'Общность': communalities,
            'Уникальность': 1 - communalities
        }).sort_values('Общность', ascending=False)
        
        print(comm_df.round(3).to_string(index=False))
        
        # Выделяем проблемные переменные
        low_comm = comm_df[comm_df['Общность'] < 0.4]
        if len(low_comm) > 0:
            print("\n⚠️ Переменные с низкой общностью (< 0.4):")
            for _, row in low_comm.iterrows():
                print(f"   {row['Переменная']}: {row['Общность']:.3f}")
            print("   💡 Рассмотрите исключение этих переменных или увеличение количества факторов")
        
        return comm_df
    
    def create_factor_scores(self):
        """
        Вычисляет факторные оценки для каждого наблюдения
        """
        factor_scores = self.fa_model.transform(self.features)
        
        # Создаем DataFrame с факторными оценками
        scores_df = pd.DataFrame(
            factor_scores,
            columns=[f'Фактор_{i+1}' for i in range(factor_scores.shape[1])]
        )
        
        # Добавляем исходный ID
        if hasattr(self, 'data'):
            id_column = self.data.columns[0]  # Предполагаем, что первая колонка - ID
            scores_df[id_column] = self.data[id_column].values
        
        print(f"\n📊 Факторные оценки вычислены для {len(scores_df)} наблюдений")
        print("📋 Статистика факторных оценок:")
        print(scores_df.describe().round(3))
        
        return scores_df
    
    def generate_report(self):
        """
        Генерирует итоговый отчет по факторному анализу
        """
        print("\n" + "="*60)
        print("🧩 ИТОГОВЫЙ ОТЧЕТ ПО ФАКТОРНОМУ АНАЛИЗУ")
        print("="*60)
        
        print(f"📋 Исходные данные: {len(self.data)} наблюдений, {len(self.feature_names)} переменных")
        print(f"🎯 Количество факторов: {self.fa_model.n_factors}")
        
        # Качество модели
        communalities = self.fa_model.get_communalities()
        mean_communality = np.mean(communalities)
        
        print(f"\n📊 Качество факторного решения:")
        print(f"   Средняя общность: {mean_communality:.3f}")
        
        if mean_communality >= 0.6:
            print("   ✅ Отличное качество факторного решения")
        elif mean_communality >= 0.4:
            print("   ⚠️ Приемлемое качество факторного решения")
        else:
            print("   ❌ Низкое качество факторного решения")
        
        # Объясненная дисперсия
        eigenvalues, _ = self.fa_model.get_eigenvalues()
        total_variance = np.sum(eigenvalues[:self.fa_model.n_factors])
        variance_explained = total_variance / len(self.feature_names) * 100
        
        print(f"\n📈 Объясненная дисперсия: {variance_explained:.1f}%")
        
        print("\n💡 Рекомендации:")
        if mean_communality >= 0.6 and variance_explained >= 60:
            print("   🏆 Отличный результат! Факторное решение можно использовать")
        elif mean_communality >= 0.4 and variance_explained >= 40:
            print("   ✅ Хороший результат с возможностью улучшения")
        else:
            print("   🔄 Рассмотрите изменение количества факторов или переменных")


def main():
    """
    Демонстрация использования факторного анализа
    """
    print("🧩 Запуск факторного анализа")
    print("="*50)
    
    # Создаем анализатор
    analyzer = FactorAnalysisToolkit()
    
    # Загружаем данные
    analyzer.load_data('employee_satisfaction.csv')
    
    # Проверяем пригодность данных
    analyzer.check_data_adequacy()
    
    # Определяем количество факторов
    analyzer.determine_n_factors()
    
    # Выполняем факторный анализ
    analyzer.perform_factor_analysis(rotation='varimax')
    
    # Визуализируем нагрузки
    loadings_df = analyzer.plot_factor_loadings()
    
    # Интерпретируем факторы
    analyzer.interpret_factors(threshold=0.3)
    
    # Анализируем общности
    analyzer.analyze_communalities()
    
    # Вычисляем факторные оценки
    factor_scores = analyzer.create_factor_scores()
    
    # Генерируем отчет
    analyzer.generate_report()
    
    print("\n🎉 Факторный анализ завершен!")
    return analyzer, factor_scores


if __name__ == "__main__":
    analyzer, scores = main()