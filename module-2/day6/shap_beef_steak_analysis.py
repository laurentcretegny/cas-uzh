#!/usr/bin/env python3
"""
Compute SHAP feature contributions for the Beef Steak healthiness prediction
and visualize with a color-coded bar chart.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
import shap
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

def compute_shap_beef_steak():
    """Compute SHAP values for Beef Steak healthiness prediction."""
    
    # Load the original dataset
    df = pd.read_csv('zeughauskeller-cogs.csv')
    print(f"📊 Loading dataset: {len(df)} dishes")
    
    # Extract numeric price
    df['Price_Numeric'] = df['Price (CHF)'].apply(extract_numeric_price)
    
    # Select features
    cogs_columns = [col for col in df.columns if col.startswith('COGS_')]
    feature_columns = cogs_columns + ['Estimated dish weight (kg)', 'Price_Numeric', 'Total COGS Estimated (CHF)']
    
    # Prepare original data
    X_original = df[feature_columns].copy()
    y_original = df['Healthiness'].copy()
    
    # Handle missing values
    X_original = X_original.fillna(0)
    y_original = y_original.fillna(y_original.median())
    
    # Train the model
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_original)
    
    model = LogisticRegression(random_state=42, max_iter=1000)
    model.fit(X_scaled, y_original)
    
    print(f"✅ Model trained successfully")
    
    # Create new Beef Steak dish
    beef_steak = {
        'COGS_Meat/Sausage (CHF)': 15.0,
        'COGS_Cheese (CHF)': 0.0,
        'COGS_Mushrooms (CHF)': 0.0,
        'COGS_Potatoes (CHF)': 0.0,
        'COGS_Pasta/Noodles (CHF)': 0.0,
        'COGS_Bread/Toast (CHF)': 0.0,
        'COGS_Salad Greens (CHF)': 0.0,
        'COGS_Rice (CHF)': 0.0,
        'COGS_Sauce (CHF)': 0.0,
        'COGS_Vegetables (CHF)': 0.25,
        'Estimated dish weight (kg)': 0.4,
        'Price_Numeric': 45,
        'Total COGS Estimated (CHF)': 15.25,
    }
    
    # Prepare features for prediction
    beef_steak_features = []
    for col in feature_columns:
        beef_steak_features.append(beef_steak[col])
    
    beef_steak_features = np.array(beef_steak_features).reshape(1, -1)
    beef_steak_scaled = scaler.transform(beef_steak_features)
    
    # Make prediction
    predicted_healthiness = model.predict(beef_steak_scaled)[0]
    healthiness_probabilities = model.predict_proba(beef_steak_scaled)[0]
    
    print(f"🎯 Prediction: Healthiness Level {predicted_healthiness}")
    print(f"📊 Confidence: {healthiness_probabilities[predicted_healthiness-1]:.1%}")
    
    # Initialize SHAP explainer
    print(f"🔍 Computing SHAP values...")
    explainer = shap.LinearExplainer(model, X_scaled)
    
    # Get SHAP values for the beef steak
    shap_values = explainer.shap_values(beef_steak_scaled)
    
    print(f"   SHAP values type: {type(shap_values)}")
    if isinstance(shap_values, list):
        print(f"   Number of classes: {len(shap_values)}")
        print(f"   Shape per class: {shap_values[0].shape}")
    else:
        print(f"   SHAP values shape: {shap_values.shape}")
    
    # For multiclass logistic regression, we need SHAP values for the predicted class
    predicted_class_idx = predicted_healthiness - 1  # Convert to 0-indexed
    
    # Get SHAP values for predicted class
    if isinstance(shap_values, list):
        # Multi-class case: shap_values is list of arrays
        shap_values_predicted = shap_values[predicted_class_idx][0]  # First sample
        base_value = explainer.expected_value[predicted_class_idx]
    else:
        # Binary case or single output
        if shap_values.ndim == 3:  # (n_samples, n_features, n_classes)
            shap_values_predicted = shap_values[0, :, predicted_class_idx]
        elif shap_values.ndim == 2:  # (n_samples, n_features)
            shap_values_predicted = shap_values[0, :]
        else:
            shap_values_predicted = shap_values
            
        if hasattr(explainer.expected_value, '__len__') and len(explainer.expected_value) > 1:
            base_value = explainer.expected_value[predicted_class_idx]
        else:
            base_value = explainer.expected_value
    
    print(f"📈 SHAP analysis complete")
    print(f"   SHAP values shape: {shap_values_predicted.shape}")
    print(f"   Base value: {base_value}")
    print(f"   Sum of SHAP values: {shap_values_predicted.sum():.3f}")
    print(f"   Prediction logic: {base_value} + {shap_values_predicted.sum():.3f} = {base_value + shap_values_predicted.sum():.3f}")
    
    # Ensure shap_values_predicted is 1D
    if shap_values_predicted.ndim > 1:
        shap_values_predicted = shap_values_predicted.flatten()
    
    # Ensure beef_steak_features is 1D for DataFrame
    beef_steak_features_1d = beef_steak_features.flatten()
    
    # Create feature names for display
    feature_names_display = []
    for col in feature_columns:
        name = col.replace('COGS_', '').replace(' (CHF)', '').replace(' (kg)', '')
        if 'Price_Numeric' in col:
            name = 'Price'
        elif 'Total COGS' in col:
            name = 'Total COGS'
        elif 'Estimated dish weight' in col:
            name = 'Dish Weight'
        feature_names_display.append(name)
    
    # Create DataFrame for easier manipulation
    shap_df = pd.DataFrame({
        'Feature': feature_names_display,
        'SHAP_Value': shap_values_predicted,
        'Feature_Value': beef_steak_features_1d
    })
    
    # Sort by absolute SHAP value for better visualization
    shap_df['Abs_SHAP'] = np.abs(shap_df['SHAP_Value'])
    shap_df = shap_df.sort_values('Abs_SHAP', ascending=True)
    
    # Create the bar chart
    plt.figure(figsize=(12, 8))
    
    # Color mapping: blue for positive, red for negative
    colors = ['red' if val < 0 else 'blue' for val in shap_df['SHAP_Value']]
    
    # Create horizontal bar chart
    bars = plt.barh(range(len(shap_df)), shap_df['SHAP_Value'], 
                    color=colors, alpha=0.7, edgecolor='black', linewidth=0.8)
    
    # Customize the plot
    plt.yticks(range(len(shap_df)), shap_df['Feature'])
    plt.xlabel('SHAP Value (Impact on Prediction)', fontsize=12, fontweight='bold')
    plt.ylabel('Features', fontsize=12, fontweight='bold')
    plt.title(f'SHAP Feature Contributions: Beef Steak → Healthiness Level {predicted_healthiness}\n'
              f'Base Value: {base_value:.3f}, Prediction: {base_value + shap_values_predicted.sum():.3f}',
              fontsize=14, fontweight='bold')
    
    # Add value labels on bars
    for i, (bar, shap_val, feature_val) in enumerate(zip(bars, shap_df['SHAP_Value'], shap_df['Feature_Value'])):
        # Position text based on bar direction
        x_pos = shap_val + (0.01 if shap_val >= 0 else -0.01)
        ha = 'left' if shap_val >= 0 else 'right'
        
        plt.text(x_pos, i, f'{shap_val:.3f}', 
                ha=ha, va='center', fontsize=9, fontweight='bold')
        
        # Add feature value in parentheses
        feature_name = shap_df['Feature'].iloc[i]
        if feature_val != 0:  # Only show non-zero values
            plt.text(-0.5, i, f'({feature_val:.2f})', 
                    ha='right', va='center', fontsize=8, style='italic', color='gray')
    
    # Add vertical line at x=0
    plt.axvline(x=0, color='black', linestyle='-', linewidth=1)
    
    # Add legend
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor='blue', alpha=0.7, label='Positive Impact (→ Higher Health)'),
                      Patch(facecolor='red', alpha=0.7, label='Negative Impact (→ Lower Health)')]
    plt.legend(handles=legend_elements, loc='lower right')
    
    # Add grid for better readability
    plt.grid(True, alpha=0.3, axis='x')
    
    # Add explanation text
    explanation = f"""SHAP Interpretation:
• Base Value: Expected healthiness score across all dishes
• Blue bars: Features pushing toward higher healthiness
• Red bars: Features pushing toward lower healthiness  
• Sum of all contributions + base = final prediction"""
    
    plt.figtext(0.02, 0.02, explanation, fontsize=9,
                bbox=dict(boxstyle='round,pad=0.5', facecolor='lightblue', alpha=0.8))
    
    plt.tight_layout()
    plt.savefig('beef_steak_shap_analysis.png', dpi=300, bbox_inches='tight')
    print(f"✅ SHAP visualization saved to: beef_steak_shap_analysis.png")
    
    # Detailed SHAP analysis
    print(f"\n" + "="*70)
    print("DETAILED SHAP FEATURE CONTRIBUTION ANALYSIS")
    print("="*70)
    
    print(f"\n🎯 PREDICTION BREAKDOWN:")
    print(f"   Base value (expected): {base_value:.3f}")
    print(f"   Total SHAP contribution: {shap_values_predicted.sum():.3f}")
    print(f"   Final prediction: {base_value + shap_values_predicted.sum():.3f}")
    print(f"   Predicted class: {predicted_healthiness}")
    
    # Sort by SHAP value magnitude for analysis
    shap_analysis = shap_df.sort_values('SHAP_Value', ascending=False)
    
    print(f"\n📊 TOP POSITIVE CONTRIBUTORS (Pushing toward healthier):")
    print("-" * 60)
    positive_contribs = shap_analysis[shap_analysis['SHAP_Value'] > 0]
    if len(positive_contribs) > 0:
        for _, row in positive_contribs.iterrows():
            feature = row['Feature']
            shap_val = row['SHAP_Value']
            feature_val = row['Feature_Value']
            print(f"  {feature:<20} | SHAP: +{shap_val:.3f} | Value: {feature_val:.2f}")
    else:
        print("  No positive contributors found")
    
    print(f"\n📉 TOP NEGATIVE CONTRIBUTORS (Pushing toward unhealthier):")
    print("-" * 60)
    negative_contribs = shap_analysis[shap_analysis['SHAP_Value'] < 0]
    if len(negative_contribs) > 0:
        for _, row in negative_contribs.iterrows():
            feature = row['Feature']
            shap_val = row['SHAP_Value']
            feature_val = row['Feature_Value']
            print(f"  {feature:<20} | SHAP: {shap_val:.3f} | Value: {feature_val:.2f}")
    else:
        print("  No negative contributors found")
    
    # Feature importance ranking
    print(f"\n🏆 FEATURE IMPORTANCE RANKING (by absolute SHAP value):")
    print("-" * 60)
    importance_ranking = shap_df.sort_values('Abs_SHAP', ascending=False)
    for rank, (_, row) in enumerate(importance_ranking.iterrows(), 1):
        feature = row['Feature']
        shap_val = row['SHAP_Value']
        abs_shap = row['Abs_SHAP']
        direction = "↗️" if shap_val > 0 else "↘️"
        print(f"  {rank:2d}. {feature:<20} | {direction} {abs_shap:.3f} | ({shap_val:+.3f})")
    
    # Business insights
    print(f"\n💡 BUSINESS INSIGHTS:")
    print("-" * 30)
    
    # Find the most influential features
    top_negative = negative_contribs.head(1)
    top_positive = positive_contribs.head(1) if len(positive_contribs) > 0 else None
    
    if len(top_negative) > 0:
        worst_feature = top_negative.iloc[0]
        print(f"🔴 Main health detractor: {worst_feature['Feature']} (SHAP: {worst_feature['SHAP_Value']:.3f})")
        
    if top_positive is not None and len(top_positive) > 0:
        best_feature = top_positive.iloc[0]
        print(f"🔵 Main health contributor: {best_feature['Feature']} (SHAP: {best_feature['SHAP_Value']:.3f})")
    else:
        print(f"🔵 No positive health contributors - all features push toward unhealthier classification")
    
    # Actionable recommendations
    print(f"\n📋 ACTIONABLE RECOMMENDATIONS:")
    print("-" * 40)
    
    # Look for zero-value features that could be improved
    zero_features = shap_df[(shap_df['Feature_Value'] == 0) & (shap_df['SHAP_Value'] < 0)]
    if len(zero_features) > 0:
        print("To improve healthiness score:")
        for _, row in zero_features.head(3).iterrows():
            feature = row['Feature']
            if 'Vegetables' in feature or 'Salad' in feature:
                print(f"  • Add {feature.lower()} - currently zero, could boost health score")
    
    # Look at high-impact negative features
    high_impact_negative = negative_contribs.head(2)
    if len(high_impact_negative) > 0:
        print("Current health detractors:")
        for _, row in high_impact_negative.iterrows():
            feature = row['Feature']
            feature_val = row['Feature_Value']
            if 'Meat' in feature and feature_val > 10:
                print(f"  • Reduce {feature.lower()} portion ({feature_val:.1f} CHF is premium level)")
    
    return {
        'shap_values': shap_values_predicted,
        'base_value': base_value,
        'features': feature_names_display,
        'feature_values': beef_steak_features[0],
        'prediction': predicted_healthiness,
        'shap_dataframe': shap_df
    }

if __name__ == "__main__":
    results = compute_shap_beef_steak()