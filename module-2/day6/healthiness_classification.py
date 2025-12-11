#!/usr/bin/env python3
"""
Create probabilistic classification models to predict the Healthiness attribute
using COGS and other dish features.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, roc_auc_score
from sklearn.metrics import roc_curve, auc
from sklearn.preprocessing import LabelBinarizer
import re
import warnings
warnings.filterwarnings('ignore')

def extract_numeric_price(price_str):
    """Extract numeric price from price string."""
    if pd.isna(price_str):
        return None
    
    numbers = re.findall(r'\d+\.?\d*', str(price_str))
    if numbers:
        prices = [float(num) for num in numbers]
        return sum(prices) / len(prices)
    return None

def create_healthiness_classification_model():
    """Create and evaluate probabilistic classification models for healthiness prediction."""
    
    # Load the data
    df = pd.read_csv('zeughauskeller-cogs.csv')
    print(f"📊 Dataset loaded: {len(df)} dishes")
    
    # Extract numeric price
    df['Price_Numeric'] = df['Price (CHF)'].apply(extract_numeric_price)
    
    # Select features - COGS attributes plus other numerical features
    cogs_columns = [col for col in df.columns if col.startswith('COGS_')]
    feature_columns = cogs_columns + ['Estimated dish weight (kg)', 'Price_Numeric', 'Total COGS Estimated (CHF)']
    
    # Prepare feature matrix and target variable
    X = df[feature_columns].copy()
    y = df['Healthiness'].copy()
    
    # Handle missing values
    X = X.fillna(0)
    y = y.fillna(y.median())
    
    print(f"🎯 Target variable distribution:")
    print(y.value_counts().sort_index())
    
    print(f"\n📈 Features used ({len(feature_columns)}):")
    for i, col in enumerate(feature_columns, 1):
        feature_name = col.replace('COGS_', '').replace(' (CHF)', '').replace(' (kg)', '')
        print(f"  {i:2d}. {feature_name}")
    
    # Standardize features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.3, random_state=42, stratify=y
    )
    
    print(f"\n🔄 Data split: {len(X_train)} training, {len(X_test)} testing samples")
    
    # Define models
    models = {
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
        'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000),
        'Naive Bayes': GaussianNB(),
        'SVM (RBF)': SVC(random_state=42, probability=True)
    }
    
    # Train and evaluate models
    results = {}
    
    print(f"\n" + "="*80)
    print("MODEL TRAINING AND EVALUATION")
    print("="*80)
    
    for name, model in models.items():
        print(f"\n🔍 Training {name}...")
        
        # Train model
        model.fit(X_train, y_train)
        
        # Predictions
        y_pred = model.predict(X_test)
        y_prob = model.predict_proba(X_test)
        
        # Calculate metrics
        accuracy = accuracy_score(y_test, y_pred)
        
        # Cross-validation
        cv_scores = cross_val_score(model, X_scaled, y, cv=5, scoring='accuracy')
        
        # Store results
        results[name] = {
            'model': model,
            'accuracy': accuracy,
            'cv_mean': cv_scores.mean(),
            'cv_std': cv_scores.std(),
            'y_pred': y_pred,
            'y_prob': y_prob,
            'classification_report': classification_report(y_test, y_pred, output_dict=True)
        }
        
        print(f"   Accuracy: {accuracy:.3f}")
        print(f"   CV Score: {cv_scores.mean():.3f} ± {cv_scores.std():.3f}")
    
    # Create comprehensive visualization
    fig = plt.figure(figsize=(16, 12))
    
    # Model comparison
    ax1 = plt.subplot(2, 3, 1)
    model_names = list(results.keys())
    accuracies = [results[name]['accuracy'] for name in model_names]
    cv_means = [results[name]['cv_mean'] for name in model_names]
    cv_stds = [results[name]['cv_std'] for name in model_names]
    
    x_pos = np.arange(len(model_names))
    bars = ax1.bar(x_pos, accuracies, alpha=0.7, color='steelblue', label='Test Accuracy')
    ax1.errorbar(x_pos, cv_means, yerr=cv_stds, fmt='ro', label='CV Mean ± Std')
    ax1.set_xlabel('Models')
    ax1.set_ylabel('Accuracy')
    ax1.set_title('Model Performance Comparison')
    ax1.set_xticks(x_pos)
    ax1.set_xticklabels(model_names, rotation=45, ha='right')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Add accuracy values on bars
    for i, (bar, acc) in enumerate(zip(bars, accuracies)):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                f'{acc:.3f}', ha='center', va='bottom', fontweight='bold')
    
    # Best model confusion matrix
    best_model_name = max(results.keys(), key=lambda k: results[k]['cv_mean'])
    best_model = results[best_model_name]
    
    ax2 = plt.subplot(2, 3, 2)
    cm = confusion_matrix(y_test, best_model['y_pred'])
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax2)
    ax2.set_title(f'Confusion Matrix\n{best_model_name}')
    ax2.set_xlabel('Predicted Healthiness')
    ax2.set_ylabel('True Healthiness')
    
    # Feature importance (for Random Forest)
    if 'Random Forest' in results:
        ax3 = plt.subplot(2, 3, 3)
        rf_model = results['Random Forest']['model']
        feature_importance = rf_model.feature_importances_
        feature_names_short = [col.replace('COGS_', '').replace(' (CHF)', '').replace(' (kg)', '') 
                              for col in feature_columns]
        
        # Sort by importance
        sorted_idx = np.argsort(feature_importance)[::-1][:10]  # Top 10
        
        ax3.barh(range(len(sorted_idx)), feature_importance[sorted_idx])
        ax3.set_yticks(range(len(sorted_idx)))
        ax3.set_yticklabels([feature_names_short[i] for i in sorted_idx])
        ax3.set_xlabel('Feature Importance')
        ax3.set_title('Top 10 Feature Importance\n(Random Forest)')
        ax3.grid(True, alpha=0.3)
    
    # Probability distributions for best model
    ax4 = plt.subplot(2, 3, 4)
    best_probs = best_model['y_prob']
    healthiness_classes = sorted(y.unique())
    
    for i, health_class in enumerate(healthiness_classes):
        mask = y_test == health_class
        if mask.sum() > 0:
            class_probs = best_probs[mask, i]
            ax4.hist(class_probs, alpha=0.6, label=f'Healthiness {health_class}', bins=10)
    
    ax4.set_xlabel('Predicted Probability')
    ax4.set_ylabel('Frequency')
    ax4.set_title(f'Probability Distributions\n{best_model_name}')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    
    # Prediction vs True values scatter
    ax5 = plt.subplot(2, 3, 5)
    ax5.scatter(y_test, best_model['y_pred'], alpha=0.6)
    ax5.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
    ax5.set_xlabel('True Healthiness')
    ax5.set_ylabel('Predicted Healthiness')
    ax5.set_title(f'Predictions vs True Values\n{best_model_name}')
    ax5.grid(True, alpha=0.3)
    
    # Cross-validation scores
    ax6 = plt.subplot(2, 3, 6)
    cv_data = []
    cv_labels = []
    for name in model_names:
        model = results[name]['model']
        cv_scores = cross_val_score(model, X_scaled, y, cv=5, scoring='accuracy')
        cv_data.append(cv_scores)
        cv_labels.append(name)
    
    ax6.boxplot(cv_data, labels=[name.replace(' ', '\n') for name in cv_labels])
    ax6.set_ylabel('CV Accuracy')
    ax6.set_title('Cross-Validation Score Distribution')
    ax6.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('healthiness_classification_analysis.png', dpi=300, bbox_inches='tight')
    print(f"\n✅ Classification analysis saved to: healthiness_classification_analysis.png")
    
    # Detailed results
    print(f"\n" + "="*80)
    print("DETAILED CLASSIFICATION RESULTS")
    print("="*80)
    
    print(f"\n🏆 BEST MODEL: {best_model_name}")
    print(f"   Test Accuracy: {best_model['accuracy']:.3f}")
    print(f"   CV Accuracy: {best_model['cv_mean']:.3f} ± {best_model['cv_std']:.3f}")
    
    print(f"\n📊 CLASSIFICATION REPORT (Best Model):")
    print("-" * 60)
    cr = best_model['classification_report']
    for class_label in sorted([k for k in cr.keys() if k.replace('.','').isdigit()]):
        precision = cr[class_label]['precision']
        recall = cr[class_label]['recall']
        f1 = cr[class_label]['f1-score']
        support = int(cr[class_label]['support'])
        print(f"Healthiness {class_label}: Precision={precision:.3f}, Recall={recall:.3f}, F1={f1:.3f} (n={support})")
    
    # Feature importance analysis
    if 'Random Forest' in results:
        print(f"\n🎯 TOP 10 FEATURE IMPORTANCE (Random Forest):")
        print("-" * 50)
        rf_model = results['Random Forest']['model']
        feature_importance = rf_model.feature_importances_
        
        # Create feature importance DataFrame
        importance_df = pd.DataFrame({
            'Feature': feature_columns,
            'Importance': feature_importance
        }).sort_values('Importance', ascending=False)
        
        for i, row in importance_df.head(10).iterrows():
            feature_name = row['Feature'].replace('COGS_', '').replace(' (CHF)', '').replace(' (kg)', '')
            print(f"{len(importance_df) - list(importance_df.index).index(i):2d}. {feature_name:<25} | {row['Importance']:.4f}")
    
    # Model comparison table
    print(f"\n📈 MODEL COMPARISON SUMMARY:")
    print("-" * 70)
    print(f"{'Model':<20} | {'Test Acc':<8} | {'CV Mean':<8} | {'CV Std':<8} | {'Rank'}")
    print("-" * 70)
    
    # Sort by CV mean for ranking
    sorted_models = sorted(results.items(), key=lambda x: x[1]['cv_mean'], reverse=True)
    
    for rank, (name, result) in enumerate(sorted_models, 1):
        print(f"{name:<20} | {result['accuracy']:<8.3f} | {result['cv_mean']:<8.3f} | {result['cv_std']:<8.3f} | {rank}")
    
    # Probability predictions for sample dishes
    print(f"\n🍽️  SAMPLE PREDICTIONS (Best Model - {best_model_name}):")
    print("-" * 80)
    
    # Get some sample predictions
    sample_indices = np.random.choice(len(X_test), min(5, len(X_test)), replace=False)
    
    for idx in sample_indices:
        true_health = y_test.iloc[idx]
        pred_health = best_model['y_pred'][idx]
        probs = best_model['y_prob'][idx]
        
        dish_idx = y_test.index[idx]
        dish_name = df.loc[dish_idx, 'Dish Name']
        
        print(f"\nDish: {dish_name}")
        print(f"True Healthiness: {true_health} | Predicted: {pred_health}")
        print("Probability distribution:")
        for i, health_class in enumerate(healthiness_classes):
            print(f"  Healthiness {health_class}: {probs[i]:.3f}")
    
    # Save results
    results_summary = pd.DataFrame({
        'Model': list(results.keys()),
        'Test_Accuracy': [results[name]['accuracy'] for name in results.keys()],
        'CV_Mean': [results[name]['cv_mean'] for name in results.keys()],
        'CV_Std': [results[name]['cv_std'] for name in results.keys()]
    })
    
    results_summary.to_csv('healthiness_classification_results.csv', index=False)
    print(f"\n✅ Results summary saved to: healthiness_classification_results.csv")
    
    return results, best_model_name

if __name__ == "__main__":
    results, best_model = create_healthiness_classification_model()