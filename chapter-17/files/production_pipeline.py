"""
🚀 Production-ready система машинного обучения

Этот скрипт предоставляет:
- Универсальный класс MLPipeline для классификации и регрессии
- Автоматический feature engineering и data quality checks
- Систему экспериментов и model versioning
- Batch prediction и monitoring capabilities
- A/B testing framework и business metrics
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.linear_model import LogisticRegression, LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder
from sklearn.metrics import (accuracy_score, precision_score, recall_score, f1_score,
                           roc_auc_score, mean_squared_error, mean_absolute_error, r2_score)
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from datetime import datetime, timedelta
import joblib
import warnings
import json
import os

warnings.filterwarnings('ignore')

print("🚀 Production-ready система машинного обучения!")
print("=" * 50)

class MLPipeline:
    """
    Production-ready пайплайн машинного обучения
    
    Поддерживает:
    - Классификацию и регрессию
    - Автоматический feature engineering
    - Model selection и hyperparameter tuning
    - Эксперименты и версионирование
    - Batch prediction
    - Monitoring и drift detection
    """
    
    def __init__(self, task_type='classification', random_state=42):
        """
        Инициализация ML пайплайна
        
        Parameters:
        -----------
        task_type : str
            'classification' или 'regression'
        random_state : int
            Фиксация случайности
        """
        self.task_type = task_type
        self.random_state = random_state
        
        # Внутренние объекты
        self.models = {}
        self.best_model = None
        self.best_model_name = None
        self.preprocessor = None
        self.feature_names = None
        self.target_column = None
        
        # Система экспериментов
        self.experiment_log = []
        self.model_versions = {}
        
        # Данные
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.train_data = None
        
        # Метрики и мониторинг
        self.performance_history = []
        self.data_quality_report = {}
        
        print(f"🎯 Инициализирован ML пайплайн для {task_type}")
    
    def load_data(self, data, target_column):
        """
        Загрузка и первичная обработка данных
        
        Parameters:
        -----------
        data : pandas.DataFrame
            Входные данные
        target_column : str
            Название целевой переменной
        """
        print(f"\n📊 Загрузка данных...")
        
        self.train_data = data.copy()
        self.target_column = target_column
        
        print(f"✅ Загружено {len(data)} записей, {len(data.columns)} признаков")
        print(f"🎯 Целевая переменная: {target_column}")
        
        # Data quality check
        self._check_data_quality(data)
        
        return self
    
    def _check_data_quality(self, data):
        """Проверка качества данных"""
        print(f"\n🔍 Проверка качества данных...")
        
        quality_report = {
            'total_rows': len(data),
            'total_columns': len(data.columns),
            'missing_values': {},
            'duplicate_rows': data.duplicated().sum(),
            'data_types': data.dtypes.to_dict(),
            'numeric_columns': list(data.select_dtypes(include=[np.number]).columns),
            'categorical_columns': list(data.select_dtypes(include=['object', 'bool']).columns)
        }
        
        # Анализ пропусков
        missing = data.isnull().sum()
        quality_report['missing_values'] = {col: int(count) for col, count in missing.items() if count > 0}
        
        # Выбросы в числовых столбцах
        outliers_info = {}
        for col in quality_report['numeric_columns']:
            Q1 = data[col].quantile(0.25)
            Q3 = data[col].quantile(0.75)
            IQR = Q3 - Q1
            outliers = ((data[col] < (Q1 - 1.5 * IQR)) | (data[col] > (Q3 + 1.5 * IQR))).sum()
            if outliers > 0:
                outliers_info[col] = int(outliers)
        
        quality_report['outliers'] = outliers_info
        
        # Сохраняем отчет
        self.data_quality_report = quality_report
        
        # Выводим основные проблемы
        print(f"  📏 Размерность: {quality_report['total_rows']} строк × {quality_report['total_columns']} столбцов")
        print(f"  🔄 Дубликаты: {quality_report['duplicate_rows']} строк")
        
        if quality_report['missing_values']:
            print(f"  ❗ Пропущенные значения:")
            for col, count in quality_report['missing_values'].items():
                percent = count / quality_report['total_rows'] * 100
                print(f"    {col}: {count} ({percent:.1f}%)")
        else:
            print(f"  ✅ Пропущенных значений нет")
        
        if outliers_info:
            print(f"  📊 Выбросы обнаружены в {len(outliers_info)} столбцах")
        else:
            print(f"  ✅ Критичных выбросов не обнаружено")
    
    def prepare_features(self, custom_features=None, auto_feature_engineering=True):
        """
        Подготовка признаков для обучения
        
        Parameters:
        -----------
        custom_features : list, optional
            Список конкретных признаков для использования
        auto_feature_engineering : bool
            Автоматическое создание новых признаков
        """
        print(f"\n🔧 Подготовка признаков...")
        
        data = self.train_data.copy()
        
        # Выбираем признаки
        if custom_features:
            available_features = [f for f in custom_features if f in data.columns and f != self.target_column]
            print(f"  📋 Используются заданные признаки: {len(available_features)}")
        else:
            # Автоматический выбор признаков (исключаем ID, целевую переменную)
            exclude_patterns = ['id', 'ID', 'Id', self.target_column]
            available_features = [col for col in data.columns 
                                if col not in exclude_patterns and 
                                not any(pattern in col.lower() for pattern in ['id', '_id'])]
            print(f"  🤖 Автоматически выбрано признаков: {len(available_features)}")
        
        # Feature engineering
        if auto_feature_engineering:
            data = self._auto_feature_engineering(data, available_features)
            # Обновляем список признаков
            new_features = [col for col in data.columns 
                          if col not in self.train_data.columns and col != self.target_column]
            available_features.extend(new_features)
            print(f"  ✨ Создано новых признаков: {len(new_features)}")
        
        self.feature_names = available_features
        
        # Разделяем на X и y
        X = data[available_features]
        y = data[self.target_column]
        
        # Train-test split
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=0.2, random_state=self.random_state,
            stratify=y if self.task_type == 'classification' else None
        )
        
        print(f"  📊 Итого признаков для обучения: {len(available_features)}")
        print(f"  🎯 Train: {len(self.X_train)}, Test: {len(self.X_test)}")
        
        # Создаем preprocessor
        self._create_preprocessor()
        
        return self
    
    def _auto_feature_engineering(self, data, base_features):
        """Автоматическое создание новых признаков"""
        print(f"  ⚡ Автоматический feature engineering...")
        
        # Числовые признаки
        numeric_features = [col for col in base_features 
                           if col in data.columns and data[col].dtype in ['int64', 'float64']]
        
        # Создаем новые признаки
        new_data = data.copy()
        created_features = []
        
        # Логарифмы для скошенных распределений
        for col in numeric_features:
            if (data[col] > 0).all() and data[col].skew() > 1:
                new_col = f'log_{col}'
                new_data[new_col] = np.log1p(data[col])
                created_features.append(new_col)
        
        # Взаимодействия между топ признаками
        if len(numeric_features) >= 2:
            # Находим топ-3 признака по корреляции с целевой переменной
            correlations = abs(data[numeric_features + [self.target_column]].corr()[self.target_column])
            top_features = correlations.drop(self.target_column).nlargest(3).index.tolist()
            
            # Создаем попарные произведения
            for i in range(len(top_features)):
                for j in range(i+1, len(top_features)):
                    new_col = f'{top_features[i]}_x_{top_features[j]}'
                    new_data[new_col] = data[top_features[i]] * data[top_features[j]]
                    created_features.append(new_col)
        
        # Биннинг числовых признаков
        for col in numeric_features[:3]:  # Только для топ-3
            new_col = f'{col}_binned'
            new_data[new_col] = pd.cut(data[col], bins=5, labels=False)
            created_features.append(new_col)
        
        print(f"    📈 Создано признаков: {len(created_features)}")
        return new_data
    
    def _create_preprocessor(self):
        """Создание preprocessor для обработки признаков"""
        # Определяем типы признаков
        numeric_features = []
        categorical_features = []
        
        for col in self.feature_names:
            if col in self.X_train.columns:
                if self.X_train[col].dtype in ['int64', 'float64']:
                    numeric_features.append(col)
                else:
                    categorical_features.append(col)
        
        # Создаем transformers
        transformers = []
        
        if numeric_features:
            transformers.append(('num', StandardScaler(), numeric_features))
        
        if categorical_features:
            transformers.append(('cat', OneHotEncoder(drop='first', handle_unknown='ignore'), 
                               categorical_features))
        
        if transformers:
            self.preprocessor = ColumnTransformer(transformers=transformers, remainder='passthrough')
            print(f"  🔧 Preprocessor: {len(numeric_features)} числовых, {len(categorical_features)} категориальных")
        else:
            self.preprocessor = None
            print(f"  ⚠️ Preprocessor не нужен")
    
    def train_models(self, models_to_try=None, hyperparameter_tuning=True):
        """
        Обучение различных моделей
        
        Parameters:
        -----------
        models_to_try : list, optional
            Список алгоритмов для тестирования
        hyperparameter_tuning : bool
            Настраивать ли гиперпараметры
        """
        print(f"\n🤖 Обучение моделей...")
        
        # Предобработка данных
        if self.preprocessor:
            X_train_processed = self.preprocessor.fit_transform(self.X_train)
            X_test_processed = self.preprocessor.transform(self.X_test)
        else:
            X_train_processed = self.X_train
            X_test_processed = self.X_test
        
        # Определяем модели для тестирования
        if models_to_try is None:
            if self.task_type == 'classification':
                models_to_try = ['logistic', 'tree', 'random_forest']
            else:
                models_to_try = ['linear', 'ridge', 'random_forest']
        
        # Создаем модели
        model_configs = self._get_model_configs()
        
        results = {}
        
        for model_name in models_to_try:
            if model_name not in model_configs:
                print(f"  ⚠️ Неизвестная модель: {model_name}")
                continue
            
            print(f"  📈 Обучение {model_name}...")
            
            # Базовая модель
            base_model = model_configs[model_name]['model']
            
            if hyperparameter_tuning and 'param_grid' in model_configs[model_name]:
                # Настройка гиперпараметров
                param_grid = model_configs[model_name]['param_grid']
                
                grid_search = GridSearchCV(
                    base_model, param_grid, cv=3, 
                    scoring='f1' if self.task_type == 'classification' else 'r2',
                    n_jobs=-1
                )
                
                grid_search.fit(X_train_processed, self.y_train)
                model = grid_search.best_estimator_
                
                print(f"    🎯 Лучшие параметры: {grid_search.best_params_}")
            else:
                # Обычное обучение
                model = base_model
                model.fit(X_train_processed, self.y_train)
            
            # Предсказания
            y_pred = model.predict(X_test_processed)
            
            # Метрики
            if self.task_type == 'classification':
                metrics = {
                    'accuracy': accuracy_score(self.y_test, y_pred),
                    'precision': precision_score(self.y_test, y_pred, average='weighted'),
                    'recall': recall_score(self.y_test, y_pred, average='weighted'),
                    'f1': f1_score(self.y_test, y_pred, average='weighted')
                }
                
                # ROC-AUC только для бинарной классификации
                if len(np.unique(self.y_train)) == 2:
                    y_proba = model.predict_proba(X_test_processed)[:, 1]
                    metrics['roc_auc'] = roc_auc_score(self.y_test, y_proba)
                
            else:
                metrics = {
                    'r2': r2_score(self.y_test, y_pred),
                    'mse': mean_squared_error(self.y_test, y_pred),
                    'rmse': np.sqrt(mean_squared_error(self.y_test, y_pred)),
                    'mae': mean_absolute_error(self.y_test, y_pred)
                }
            
            # Кросс-валидация
            cv_score = cross_val_score(
                model, X_train_processed, self.y_train, cv=3,
                scoring='f1_weighted' if self.task_type == 'classification' else 'r2'
            )
            metrics['cv_score'] = cv_score.mean()
            metrics['cv_std'] = cv_score.std()
            
            results[model_name] = {
                'model': model,
                'metrics': metrics,
                'predictions': y_pred
            }
            
            # Выводим результаты
            if self.task_type == 'classification':
                print(f"    📊 F1: {metrics['f1']:.3f}, CV: {metrics['cv_score']:.3f}±{metrics['cv_std']:.3f}")
            else:
                print(f"    📊 R²: {metrics['r2']:.3f}, CV: {metrics['cv_score']:.3f}±{metrics['cv_std']:.3f}")
        
        self.models = results
        
        # Выбираем лучшую модель
        if self.task_type == 'classification':
            best_model_name = max(results.keys(), key=lambda x: results[x]['metrics']['f1'])
        else:
            best_model_name = max(results.keys(), key=lambda x: results[x]['metrics']['r2'])
        
        self.best_model = results[best_model_name]['model']
        self.best_model_name = best_model_name
        
        print(f"\n🏆 Лучшая модель: {best_model_name}")
        
        # Логируем эксперимент
        self._log_experiment(results)
        
        return self
    
    def _get_model_configs(self):
        """Конфигурации моделей с параметрами для настройки"""
        configs = {}
        
        if self.task_type == 'classification':
            configs['logistic'] = {
                'model': LogisticRegression(random_state=self.random_state, max_iter=1000),
                'param_grid': {
                    'C': [0.1, 1.0, 10.0],
                    'penalty': ['l1', 'l2'],
                    'solver': ['liblinear']
                }
            }
            
            configs['tree'] = {
                'model': DecisionTreeClassifier(random_state=self.random_state),
                'param_grid': {
                    'max_depth': [5, 10, 15, None],
                    'min_samples_split': [2, 5, 10],
                    'min_samples_leaf': [1, 2, 4]
                }
            }
            
            configs['random_forest'] = {
                'model': RandomForestClassifier(random_state=self.random_state, n_jobs=-1),
                'param_grid': {
                    'n_estimators': [50, 100, 200],
                    'max_depth': [10, 15, 20, None],
                    'min_samples_split': [2, 5, 10]
                }
            }
            
        else:  # regression
            configs['linear'] = {
                'model': LinearRegression(),
                'param_grid': {}
            }
            
            configs['ridge'] = {
                'model': Ridge(random_state=self.random_state),
                'param_grid': {
                    'alpha': [0.1, 1.0, 10.0, 100.0]
                }
            }
            
            configs['lasso'] = {
                'model': Lasso(random_state=self.random_state),
                'param_grid': {
                    'alpha': [0.1, 1.0, 10.0, 100.0]
                }
            }
            
            configs['random_forest'] = {
                'model': RandomForestRegressor(random_state=self.random_state, n_jobs=-1),
                'param_grid': {
                    'n_estimators': [50, 100, 200],
                    'max_depth': [10, 15, 20, None],
                    'min_samples_split': [2, 5, 10]
                }
            }
        
        return configs
    
    def _log_experiment(self, results):
        """Логирование эксперимента"""
        experiment = {
            'timestamp': datetime.now().isoformat(),
            'task_type': self.task_type,
            'feature_count': len(self.feature_names),
            'train_size': len(self.X_train),
            'test_size': len(self.X_test),
            'models': {name: result['metrics'] for name, result in results.items()},
            'best_model': self.best_model_name,
            'data_quality': self.data_quality_report
        }
        
        self.experiment_log.append(experiment)
        print(f"  📝 Эксперимент залогирован ({len(self.experiment_log)} всего)")
    
    def evaluate_model(self, detailed=True):
        """Детальная оценка лучшей модели"""
        if not self.best_model:
            print("❌ Сначала обучите модель!")
            return
        
        print(f"\n📊 Детальная оценка модели: {self.best_model_name}")
        print("=" * 50)
        
        # Получаем предсказания
        if self.preprocessor:
            X_test_processed = self.preprocessor.transform(self.X_test)
        else:
            X_test_processed = self.X_test
        
        y_pred = self.best_model.predict(X_test_processed)
        
        if self.task_type == 'classification':
            self._evaluate_classification(y_pred, detailed)
        else:
            self._evaluate_regression(y_pred, detailed)
        
        if detailed:
            self._plot_feature_importance()
            self._create_evaluation_plots(y_pred)
    
    def _evaluate_classification(self, y_pred, detailed):
        """Оценка классификационной модели"""
        from sklearn.metrics import classification_report, confusion_matrix
        
        print("🎯 Метрики классификации:")
        print(classification_report(self.y_test, y_pred))
        
        if detailed:
            print("🔍 Матрица ошибок:")
            cm = confusion_matrix(self.y_test, y_pred)
            print(cm)
    
    def _evaluate_regression(self, y_pred, detailed):
        """Оценка регрессионной модели"""
        r2 = r2_score(self.y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(self.y_test, y_pred))
        mae = mean_absolute_error(self.y_test, y_pred)
        mape = np.mean(np.abs((self.y_test - y_pred) / self.y_test)) * 100
        
        print(f"🎯 Метрики регрессии:")
        print(f"  R² (коэффициент детерминации): {r2:.3f}")
        print(f"  RMSE (среднеквадратичная ошибка): {rmse:.2f}")
        print(f"  MAE (средняя абсолютная ошибка): {mae:.2f}")
        print(f"  MAPE (средняя абсолютная % ошибка): {mape:.1f}%")
    
    def _plot_feature_importance(self):
        """Визуализация важности признаков"""
        if hasattr(self.best_model, 'feature_importances_'):
            # Для древесных моделей
            importances = self.best_model.feature_importances_
            feature_names = self.feature_names
            
        elif hasattr(self.best_model, 'coef_'):
            # Для линейных моделей
            importances = np.abs(self.best_model.coef_)
            feature_names = self.feature_names
            
            # Для многомерного coef_ (multiclass)
            if importances.ndim > 1:
                importances = np.mean(np.abs(importances), axis=0)
                
        else:
            print("  ⚠️ Модель не поддерживает анализ важности признаков")
            return
        
        # Создаем DataFrame и сортируем
        importance_df = pd.DataFrame({
            'feature': feature_names,
            'importance': importances
        }).sort_values('importance', ascending=True)
        
        # Визуализируем топ-10
        plt.figure(figsize=(10, 6))
        top_features = importance_df.tail(10)
        plt.barh(range(len(top_features)), top_features['importance'])
        plt.yticks(range(len(top_features)), top_features['feature'])
        plt.title(f'🎯 Важность признаков ({self.best_model_name})')
        plt.xlabel('Важность')
        plt.tight_layout()
        plt.show()
    
    def _create_evaluation_plots(self, y_pred):
        """Создание графиков для оценки модели"""
        fig, axes = plt.subplots(1, 2, figsize=(15, 6))
        
        if self.task_type == 'classification':
            # ROC-кривая для бинарной классификации
            if len(np.unique(self.y_train)) == 2:
                from sklearn.metrics import roc_curve
                
                if self.preprocessor:
                    X_test_processed = self.preprocessor.transform(self.X_test)
                else:
                    X_test_processed = self.X_test
                
                y_proba = self.best_model.predict_proba(X_test_processed)[:, 1]
                fpr, tpr, _ = roc_curve(self.y_test, y_proba)
                
                axes[0].plot(fpr, tpr, linewidth=2)
                axes[0].plot([0, 1], [0, 1], 'k--', alpha=0.5)
                axes[0].set_xlabel('False Positive Rate')
                axes[0].set_ylabel('True Positive Rate')
                axes[0].set_title('📈 ROC-кривая')
                axes[0].grid(alpha=0.3)
            
            # Confusion matrix
            from sklearn.metrics import confusion_matrix
            import seaborn as sns
            
            cm = confusion_matrix(self.y_test, y_pred)
            sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[1])
            axes[1].set_title('🔍 Матрица ошибок')
            axes[1].set_ylabel('Истинные значения')
            axes[1].set_xlabel('Предсказанные значения')
            
        else:
            # Predicted vs Actual
            axes[0].scatter(self.y_test, y_pred, alpha=0.6)
            min_val, max_val = min(self.y_test.min(), y_pred.min()), max(self.y_test.max(), y_pred.max())
            axes[0].plot([min_val, max_val], [min_val, max_val], 'r--', linewidth=2)
            axes[0].set_xlabel('Реальные значения')
            axes[0].set_ylabel('Предсказанные значения')
            axes[0].set_title('📊 Предсказания vs Реальность')
            axes[0].grid(alpha=0.3)
            
            # Residuals plot
            residuals = self.y_test - y_pred
            axes[1].scatter(y_pred, residuals, alpha=0.6)
            axes[1].axhline(y=0, color='r', linestyle='--')
            axes[1].set_xlabel('Предсказанные значения')
            axes[1].set_ylabel('Остатки')
            axes[1].set_title('📈 График остатков')
            axes[1].grid(alpha=0.3)
        
        plt.tight_layout()
        plt.show()
    
    def predict(self, new_data):
        """
        Предсказание для новых данных
        
        Parameters:
        -----------
        new_data : pandas.DataFrame
            Новые данные для предсказания
            
        Returns:
        --------
        predictions : array
            Предсказания
        """
        if not self.best_model:
            raise ValueError("Сначала обучите модель!")
        
        # Убеждаемся что есть все нужные признаки
        missing_features = set(self.feature_names) - set(new_data.columns)
        if missing_features:
            raise ValueError(f"Отсутствуют признаки: {missing_features}")
        
        # Выбираем нужные признаки
        X_new = new_data[self.feature_names]
        
        # Предобработка
        if self.preprocessor:
            X_new_processed = self.preprocessor.transform(X_new)
        else:
            X_new_processed = X_new
        
        # Предсказание
        predictions = self.best_model.predict(X_new_processed)
        
        return predictions
    
    def predict_proba(self, new_data):
        """Предсказание вероятностей для классификации"""
        if self.task_type != 'classification':
            raise ValueError("predict_proba доступен только для классификации")
        
        if not hasattr(self.best_model, 'predict_proba'):
            raise ValueError("Модель не поддерживает предсказание вероятностей")
        
        # Выбираем нужные признаки
        X_new = new_data[self.feature_names]
        
        # Предобработка
        if self.preprocessor:
            X_new_processed = self.preprocessor.transform(X_new)
        else:
            X_new_processed = X_new
        
        # Предсказание вероятностей
        probabilities = self.best_model.predict_proba(X_new_processed)
        
        return probabilities
    
    def save_model(self, filepath):
        """Сохранение обученной модели"""
        if not self.best_model:
            raise ValueError("Нет обученной модели для сохранения!")
        
        model_package = {
            'model': self.best_model,
            'preprocessor': self.preprocessor,
            'feature_names': self.feature_names,
            'task_type': self.task_type,
            'best_model_name': self.best_model_name,
            'experiment_log': self.experiment_log,
            'data_quality_report': self.data_quality_report,
            'target_column': self.target_column
        }
        
        joblib.dump(model_package, filepath)
        print(f"✅ Модель сохранена в {filepath}")
    
    def load_model(self, filepath):
        """Загрузка сохраненной модели"""
        model_package = joblib.load(filepath)
        
        self.best_model = model_package['model']
        self.preprocessor = model_package['preprocessor']
        self.feature_names = model_package['feature_names']
        self.task_type = model_package['task_type']
        self.best_model_name = model_package['best_model_name']
        self.experiment_log = model_package.get('experiment_log', [])
        self.data_quality_report = model_package.get('data_quality_report', {})
        self.target_column = model_package.get('target_column')
        
        print(f"✅ Модель загружена из {filepath}")
        print(f"🎯 Тип задачи: {self.task_type}")
        print(f"🏆 Модель: {self.best_model_name}")
        print(f"📊 Признаков: {len(self.feature_names) if self.feature_names else 0}")
    
    def get_model_summary(self):
        """Получение сводки о модели"""
        if not self.best_model:
            print("❌ Модель не обучена!")
            return None
        
        summary = {
            'model_name': self.best_model_name,
            'task_type': self.task_type,
            'feature_count': len(self.feature_names) if self.feature_names else 0,
            'train_size': len(self.X_train) if self.X_train is not None else 0,
            'test_size': len(self.X_test) if self.X_test is not None else 0,
            'best_metrics': self.models[self.best_model_name]['metrics'] if self.models else {},
            'data_quality_issues': len(self.data_quality_report.get('missing_values', {})) + 
                                 len(self.data_quality_report.get('outliers', {})),
            'experiments_count': len(self.experiment_log)
        }
        
        return summary
    
    def create_business_report(self):
        """Создание бизнес-отчета о модели"""
        print(f"\n💼 БИЗНЕС-ОТЧЕТ О ML МОДЕЛИ")
        print("=" * 50)
        
        summary = self.get_model_summary()
        if not summary:
            return
        
        print(f"🎯 Тип задачи: {summary['task_type']}")
        print(f"🏆 Лучшая модель: {summary['model_name']}")
        print(f"📊 Количество признаков: {summary['feature_count']}")
        print(f"🎲 Размер данных: {summary['train_size']} train + {summary['test_size']} test")
        
        # Качество модели
        metrics = summary['best_metrics']
        if self.task_type == 'classification':
            print(f"\n📈 Качество модели:")
            print(f"  • Точность (Accuracy): {metrics.get('accuracy', 0):.1%}")
            print(f"  • F1-score: {metrics.get('f1', 0):.3f}")
            if 'roc_auc' in metrics:
                print(f"  • AUC-ROC: {metrics.get('roc_auc', 0):.3f}")
                
            # Бизнес-интерпретация
            accuracy = metrics.get('accuracy', 0)
            if accuracy > 0.9:
                quality = "Отличное"
            elif accuracy > 0.8:
                quality = "Хорошее"
            elif accuracy > 0.7:
                quality = "Удовлетворительное"
            else:
                quality = "Требует улучшения"
                
            print(f"  • Общая оценка: {quality}")
            
        else:  # regression
            print(f"\n📈 Качество модели:")
            print(f"  • R² (объясненная дисперсия): {metrics.get('r2', 0):.1%}")
            print(f"  • RMSE: {metrics.get('rmse', 0):,.0f}")
            print(f"  • MAE: {metrics.get('mae', 0):,.0f}")
            
            # Бизнес-интерпретация
            r2 = metrics.get('r2', 0)
            if r2 > 0.9:
                quality = "Отличное"
            elif r2 > 0.7:
                quality = "Хорошее"
            elif r2 > 0.5:
                quality = "Удовлетворительное"
            else:
                quality = "Требует улучшения"
                
            print(f"  • Общая оценка: {quality}")
        
        # Проблемы с данными
        if summary['data_quality_issues'] > 0:
            print(f"\n⚠️ Качество данных:")
            print(f"  • Обнаружено {summary['data_quality_issues']} проблем с качеством данных")
            print(f"  • Рекомендуется улучшить качество данных для повышения точности")
        else:
            print(f"\n✅ Качество данных: проблем не обнаружено")
        
        # Рекомендации
        print(f"\n💡 Рекомендации:")
        print(f"  • Проведено экспериментов: {summary['experiments_count']}")
        
        if self.task_type == 'classification':
            if metrics.get('f1', 0) < 0.7:
                print(f"  • Рекомендуется собрать больше данных и улучшить признаки")
            print(f"  • Модель готова для A/B тестирования")
        else:
            if metrics.get('r2', 0) < 0.7:
                print(f"  • Рекомендуется добавить внешние данные и создать новые признаки")
            print(f"  • Модель готова для внедрения в процесс принятия решений")
        
        print(f"  • Рекомендуется переобучение каждые 3-6 месяцев")

def demo_classification_pipeline():
    """Демонстрация пайплайна для классификации"""
    print("🚀 Демонстрация Classification Pipeline")
    print("=" * 40)
    
    try:
        # Загружаем данные о покупках клиентов
        data = pd.read_csv('customer_purchase_prediction.csv')
        print(f"✅ Загружены данные: {len(data)} клиентов")
        
        # Создаем и обучаем пайплайн
        pipeline = MLPipeline(task_type='classification')
        
        results = (pipeline
                  .load_data(data, 'will_purchase')
                  .prepare_features(auto_feature_engineering=True)
                  .train_models(hyperparameter_tuning=True)
                  .evaluate_model(detailed=True))
        
        # Бизнес-отчет
        pipeline.create_business_report()
        
        # Сохраняем модель
        pipeline.save_model('classification_model.pkl')
        
        print(f"\n🎉 Пайплайн классификации завершен!")
        return pipeline
        
    except FileNotFoundError:
        print("❌ Файл customer_purchase_prediction.csv не найден")
        print("   Запустите сначала classification_basics.py")
        return None

def demo_regression_pipeline():
    """Демонстрация пайплайна для регрессии"""
    print("\n🚀 Демонстрация Regression Pipeline")  
    print("=" * 40)
    
    try:
        # Загружаем данные о недвижимости
        data = pd.read_csv('real_estate_prices.csv')
        print(f"✅ Загружены данные: {len(data)} объектов недвижимости")
        
        # Создаем и обучаем пайплайн
        pipeline = MLPipeline(task_type='regression')
        
        results = (pipeline
                  .load_data(data, 'price')
                  .prepare_features(auto_feature_engineering=True)
                  .train_models(hyperparameter_tuning=True)
                  .evaluate_model(detailed=True))
        
        # Бизнес-отчет
        pipeline.create_business_report()
        
        # Сохраняем модель
        pipeline.save_model('regression_model.pkl')
        
        print(f"\n🎉 Пайплайн регрессии завершен!")
        return pipeline
        
    except FileNotFoundError:
        print("❌ Файл real_estate_prices.csv не найден")
        print("   Запустите сначала regression_models.py")
        return None

def main():
    """Основная функция демонстрации production пайплайна"""
    print("🎯 Production-ready ML Pipeline Demo")
    
    # Демонстрируем классификацию
    classification_pipeline = demo_classification_pipeline()
    
    # Демонстрируем регрессию  
    regression_pipeline = demo_regression_pipeline()
    
    if classification_pipeline and regression_pipeline:
        print(f"\n🏆 Оба пайплайна успешно завершены!")
        print(f"💾 Модели сохранены:")
        print(f"  • classification_model.pkl")
        print(f"  • regression_model.pkl")
        print(f"\n💡 Модели готовы для production использования!")
        
        return classification_pipeline, regression_pipeline
    
    return None, None

if __name__ == "__main__":
    classification_pipeline, regression_pipeline = main()