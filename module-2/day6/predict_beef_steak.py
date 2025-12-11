#!/usr/bin/env python3
"""
Add a new dish "Beef Steak" and predict its healthiness using the trained model.
Display the probability distribution as a histogram.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
import re

def extract_numeric_price(price_str):
    """Extract numeric price from price string."""
    if pd.isna(price_str):
        return None
    
    numbers = re.findall(r'\d+\.?\d*', str(price_str))
    if numbers:
        prices = [float(num) for num in numbers]
        return sum(prices) / len(prices)
    return None

def predict_beef_steak_healthiness():
    """Add new Beef Steak dish and predict its healthiness."""
    
    # Load the original dataset
    df = pd.read_csv('zeughauskeller-cogs.csv')
    print(f"📊 Original dataset: {len(df)} dishes")
    
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
    
    # Train the best model (Logistic Regression) on all original data
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_original)
    
    model = LogisticRegression(random_state=42, max_iter=1000)
    model.fit(X_scaled, y_original)
    
    print(f"✅ Model trained on {len(X_original)} dishes")
    
    # Create new Beef Steak dish
    beef_steak = {
        'Dish Name': 'Beef Steak',
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
        'Estimated dish weight (kg)': 0.4,  # Reasonable estimate for steak
        'Price (CHF)': 45,  # Estimate based on high meat cost
        'Total COGS Estimated (CHF)': 15.25,  # Sum of COGS components
        'Healthiness': None  # To be predicted
    }
    
    # Calculate derived features
    beef_steak['Price_Numeric'] = beef_steak['Price (CHF)']
    
    print(f"\n🥩 NEW DISH ADDED: {beef_steak['Dish Name']}")
    print(f"   Meat COGS: {beef_steak['COGS_Meat/Sausage (CHF)']} CHF")
    print(f"   Vegetables COGS: {beef_steak['COGS_Vegetables (CHF)']} CHF")
    print(f"   Total COGS: {beef_steak['Total COGS Estimated (CHF)']} CHF")
    print(f"   Estimated Price: {beef_steak['Price_Numeric']} CHF")
    
    # Prepare features for prediction
    beef_steak_features = []
    for col in feature_columns:
        beef_steak_features.append(beef_steak[col])
    
    # Transform using the same scaler
    beef_steak_features = np.array(beef_steak_features).reshape(1, -1)
    beef_steak_scaled = scaler.transform(beef_steak_features)
    
    # Make prediction
    predicted_healthiness = model.predict(beef_steak_scaled)[0]
    healthiness_probabilities = model.predict_proba(beef_steak_scaled)[0]
    
    print(f"\n🎯 PREDICTION RESULTS:")
    print(f"   Predicted Healthiness: {predicted_healthiness}")
    print(f"   Confidence: {healthiness_probabilities[predicted_healthiness-1]:.1%}")
    
    # Get all possible healthiness levels
    healthiness_levels = sorted(y_original.unique())
    
    print(f"\n📊 PROBABILITY DISTRIBUTION:")
    for i, level in enumerate(healthiness_levels):
        prob = healthiness_probabilities[i]
        bar = "█" * int(prob * 50)  # Visual bar
        print(f"   Healthiness {level}: {prob:.3f} ({prob:.1%}) {bar}")
    
    # Create histogram visualization
    plt.figure(figsize=(10, 6))
    
    colors = ['#FF6B6B', '#FFA07A', '#FFD700', '#98FB98', '#87CEEB']
    bars = plt.bar(healthiness_levels, healthiness_probabilities, 
                   color=colors[:len(healthiness_levels)], 
                   alpha=0.8, edgecolor='black', linewidth=1.5)
    
    # Add percentage labels on bars
    for i, (level, prob) in enumerate(zip(healthiness_levels, healthiness_probabilities)):
        plt.text(level, prob + 0.01, f'{prob:.1%}', 
                ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    # Highlight the predicted class
    predicted_idx = list(healthiness_levels).index(predicted_healthiness)
    bars[predicted_idx].set_color('#FF4444')
    bars[predicted_idx].set_alpha(1.0)
    bars[predicted_idx].set_linewidth(3)
    
    plt.xlabel('Healthiness Level', fontsize=12, fontweight='bold')
    plt.ylabel('Probability', fontsize=12, fontweight='bold')
    plt.title(f'Predicted Healthiness Distribution for "Beef Steak"\nPredicted Level: {predicted_healthiness} (Confidence: {healthiness_probabilities[predicted_idx]:.1%})', 
              fontsize=14, fontweight='bold')
    
    plt.xticks(healthiness_levels)
    plt.ylim(0, max(healthiness_probabilities) * 1.2)
    plt.grid(True, alpha=0.3, axis='y')
    
    # Add legend
    healthiness_descriptions = {
        1: 'Very Unhealthy',
        2: 'Unhealthy', 
        3: 'Moderate',
        4: 'Healthy',
        5: 'Very Healthy'
    }
    
    legend_text = []
    for level in healthiness_levels:
        description = healthiness_descriptions.get(level, f'Level {level}')
        legend_text.append(f'Level {level}: {description}')
    
    plt.figtext(0.02, 0.02, '\n'.join(legend_text), fontsize=9, 
                bbox=dict(boxstyle='round,pad=0.5', facecolor='lightgray', alpha=0.8))
    
    # Add dish details
    dish_info = f"""Beef Steak Characteristics:
• Meat COGS: {beef_steak['COGS_Meat/Sausage (CHF)']} CHF
• Vegetables: {beef_steak['COGS_Vegetables (CHF)']} CHF  
• Total COGS: {beef_steak['Total COGS Estimated (CHF)']} CHF
• Est. Price: {beef_steak['Price_Numeric']} CHF"""
    
    plt.figtext(0.98, 0.98, dish_info, fontsize=9, ha='right', va='top',
                bbox=dict(boxstyle='round,pad=0.5', facecolor='lightyellow', alpha=0.8))
    
    plt.tight_layout()
    plt.savefig('beef_steak_healthiness_prediction.png', dpi=300, bbox_inches='tight')
    print(f"\n✅ Visualization saved to: beef_steak_healthiness_prediction.png")
    
    # Compare with similar dishes in dataset
    print(f"\n📋 COMPARISON WITH SIMILAR DISHES:")
    print("-" * 60)
    
    # Find dishes with similar characteristics
    meat_dishes = df[df['COGS_Meat/Sausage (CHF)'] > 10.0].copy()
    if len(meat_dishes) > 0:
        print(f"High-meat dishes (>10 CHF meat cost) in dataset:")
        for _, dish in meat_dishes.iterrows():
            dish_name = dish['Dish Name']
            meat_cost = dish['COGS_Meat/Sausage (CHF)']
            healthiness = dish['Healthiness']
            price = dish.get('Price_Numeric', 'N/A')
            print(f"  • {dish_name}: Meat={meat_cost} CHF, Health={healthiness}, Price={price} CHF")
    
    # Statistical context
    print(f"\n📈 STATISTICAL CONTEXT:")
    print("-" * 40)
    print(f"Beef Steak meat cost (15.0 CHF):")
    meat_costs = df['COGS_Meat/Sausage (CHF)']
    percentile = (meat_costs < 15.0).mean() * 100
    print(f"  • Higher than {percentile:.1f}% of dishes in dataset")
    print(f"  • Dataset range: {meat_costs.min():.1f} - {meat_costs.max():.1f} CHF")
    print(f"  • Dataset mean: {meat_costs.mean():.1f} CHF")
    
    # Business interpretation
    print(f"\n💡 BUSINESS INTERPRETATION:")
    print("-" * 40)
    if predicted_healthiness <= 2:
        interpretation = "UNHEALTHY - High meat content with minimal vegetables"
    elif predicted_healthiness == 3:
        interpretation = "MODERATE - Balanced but meat-heavy preparation"
    else:
        interpretation = "HEALTHY - Despite high meat cost, preparation may be lean"
        
    print(f"Prediction: {interpretation}")
    print(f"Confidence level: {healthiness_probabilities[predicted_idx]:.1%}")
    
    if healthiness_probabilities[predicted_idx] < 0.5:
        print("⚠️  Low confidence - consider additional features for better prediction")
    else:
        print("✅ Reasonable confidence in prediction")
    
    return {
        'dish': beef_steak,
        'predicted_healthiness': predicted_healthiness,
        'probabilities': healthiness_probabilities,
        'healthiness_levels': healthiness_levels,
        'confidence': healthiness_probabilities[predicted_idx]
    }

if __name__ == "__main__":
    results = predict_beef_steak_healthiness()