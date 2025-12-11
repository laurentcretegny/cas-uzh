#!/usr/bin/env python3
"""
Analyze the correlation between healthiness and cost in the combined restaurant dataset.
Generate four distinct visualizations with different chart types.
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import re
from collections import Counter

def extract_numeric_price(price_str):
    """Extract numeric price from price string."""
    if pd.isna(price_str):
        return None
    
    # Extract all numbers from the price string
    numbers = re.findall(r'\d+\.?\d*', str(price_str))
    if numbers:
        # If there are multiple prices (like "14.00 CHF (Klein) / 18.00 CHF (Groß)"), take the average
        prices = [float(num) for num in numbers]
        return sum(prices) / len(prices)
    return None

def calculate_healthiness_score(ingredients, dish_name, dish_category):
    """Calculate healthiness score based on ingredients and dish characteristics."""
    if pd.isna(ingredients):
        ingredients = ""
    
    ingredients_lower = ingredients.lower()
    dish_lower = dish_name.lower()
    category_lower = dish_category.lower()
    
    score = 50  # Base score
    
    # Positive health factors (+points)
    positive_ingredients = {
        'salad': 15, 'mixed salad': 15, 'green salad': 15, 'rucola': 10, 'arugula': 10,
        'tomatoes': 8, 'cherry tomatoes': 8, 'vegetables': 12, 'seasonal ingredients': 10,
        'herbs': 8, 'basilikum': 5, 'oregano': 5, 'garlic': 5, 'knoblauch': 5,
        'chicken': 10, 'poulet': 10, 'veal': 8, 'perch': 12, 'fish': 12,
        'olive oil': 8, 'potatoes': 6, 'boiled potatoes': 8
    }
    
    # Negative health factors (-points)
    negative_ingredients = {
        'cream': -8, 'rahm': -8, 'mascarpone': -10, 'gorgonzola': -6,
        'bacon': -12, 'speck': -12, 'sausage': -10, 'bratwurst': -10, 'salsiccia': -10,
        'fried': -8, 'deep fried': -12, 'butter': -6,
        'bbq sauce': -5, 'barbecue sauce': -5, 'curry sauce': -5,
        'french fries': -10, 'burger': -8, 'tartare': -5
    }
    
    # Category-based adjustments
    category_adjustments = {
        'salad': 15, 'insalate': 15, 'fresh salads': 15, 'light dishes': 12,
        'soup': 8, 'homemade soups': 10,
        'pizza': -5, 'pizze': -5, 'dessert': -15, 'dolci': -15
    }
    
    # Apply positive factors
    for ingredient, points in positive_ingredients.items():
        if ingredient in ingredients_lower or ingredient in dish_lower:
            score += points
    
    # Apply negative factors
    for ingredient, points in negative_ingredients.items():
        if ingredient in ingredients_lower or ingredient in dish_lower:
            score += points
    
    # Apply category adjustments
    for category, points in category_adjustments.items():
        if category in category_lower:
            score += points
    
    # Special dish type penalties/bonuses
    if 'pizza' in dish_lower:
        score -= 5
    if 'dessert' in category_lower or 'tiramisu' in dish_lower:
        score -= 20
    if 'salad' in dish_lower:
        score += 10
    if 'soup' in dish_lower or 'broth' in dish_lower:
        score += 8
    
    # Ensure score is within reasonable bounds
    return max(0, min(100, score))

def create_healthiness_cost_visualizations():
    """Create four distinct visualizations correlating healthiness and cost."""
    
    # Load the combined dataset
    df = pd.read_csv('combined_restaurant_menus.csv')
    
    # Extract numeric prices
    df['Price_Numeric'] = df['Price'].apply(extract_numeric_price)
    
    # Calculate healthiness scores
    df['Healthiness_Score'] = df.apply(
        lambda row: calculate_healthiness_score(
            row['Ingredients'], 
            row['Dish'], 
            row['Dish Category']
        ), axis=1
    )
    
    # Remove rows with missing price data
    df_clean = df.dropna(subset=['Price_Numeric'])
    
    # Create healthiness categories
    df_clean['Healthiness_Category'] = pd.cut(
        df_clean['Healthiness_Score'],
        bins=[0, 35, 55, 75, 100],
        labels=['Low', 'Medium', 'High', 'Very High'],
        include_lowest=True
    )
    
    # Set up the plotting style
    plt.style.use('default')
    sns.set_palette("husl")
    
    # Create figure with 4 subplots
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Healthiness vs Cost Analysis - Restaurant Dataset', fontsize=16, fontweight='bold')
    
    # 1. Scatter Plot with Regression Line
    sns.scatterplot(data=df_clean, x='Healthiness_Score', y='Price_Numeric', 
                    hue='Restaurant', s=100, alpha=0.7, ax=ax1)
    sns.regplot(data=df_clean, x='Healthiness_Score', y='Price_Numeric', 
                scatter=False, color='red', ax=ax1)
    ax1.set_title('Scatter Plot: Healthiness vs Price', fontweight='bold')
    ax1.set_xlabel('Healthiness Score (0-100)')
    ax1.set_ylabel('Price (CHF)')
    ax1.legend(title='Restaurant', bbox_to_anchor=(1.05, 1), loc='upper left')
    
    # 2. Box Plot by Healthiness Categories
    sns.boxplot(data=df_clean, x='Healthiness_Category', y='Price_Numeric', ax=ax2)
    sns.stripplot(data=df_clean, x='Healthiness_Category', y='Price_Numeric', 
                  color='red', alpha=0.6, ax=ax2)
    ax2.set_title('Box Plot: Price Distribution by Healthiness Category', fontweight='bold')
    ax2.set_xlabel('Healthiness Category')
    ax2.set_ylabel('Price (CHF)')
    
    # 3. Violin Plot with Split by Restaurant
    sns.violinplot(data=df_clean, x='Healthiness_Category', y='Price_Numeric', 
                   hue='Restaurant', split=True, ax=ax3)
    ax3.set_title('Violin Plot: Price vs Healthiness by Restaurant', fontweight='bold')
    ax3.set_xlabel('Healthiness Category')
    ax3.set_ylabel('Price (CHF)')
    ax3.legend(title='Restaurant', bbox_to_anchor=(1.05, 1), loc='upper left')
    
    # 4. Heatmap of Average Prices
    # Create price ranges for better visualization
    df_clean['Price_Range'] = pd.cut(
        df_clean['Price_Numeric'],
        bins=[0, 15, 25, 35, 100],
        labels=['Low (≤15)', 'Medium (15-25)', 'High (25-35)', 'Premium (>35)'],
        include_lowest=True
    )
    
    # Create crosstab for heatmap
    heatmap_data = pd.crosstab(df_clean['Healthiness_Category'], df_clean['Price_Range'])
    sns.heatmap(heatmap_data, annot=True, fmt='d', cmap='YlOrRd', ax=ax4)
    ax4.set_title('Heatmap: Dish Count by Healthiness and Price Range', fontweight='bold')
    ax4.set_xlabel('Price Range (CHF)')
    ax4.set_ylabel('Healthiness Category')
    
    plt.tight_layout()
    plt.savefig('healthiness_cost_correlation_analysis.png', dpi=300, bbox_inches='tight')
    print("✅ Four correlation visualizations saved to: healthiness_cost_correlation_analysis.png")
    
    # Print statistical summary
    print("\n" + "="*80)
    print("HEALTHINESS vs COST CORRELATION ANALYSIS")
    print("="*80)
    
    # Calculate correlation coefficient
    correlation = df_clean['Healthiness_Score'].corr(df_clean['Price_Numeric'])
    print(f"📊 Pearson Correlation Coefficient: {correlation:.3f}")
    
    if correlation > 0.3:
        correlation_strength = "Strong Positive"
    elif correlation > 0.1:
        correlation_strength = "Moderate Positive"
    elif correlation > -0.1:
        correlation_strength = "Weak/No"
    elif correlation > -0.3:
        correlation_strength = "Moderate Negative"
    else:
        correlation_strength = "Strong Negative"
    
    print(f"🔍 Correlation Strength: {correlation_strength}")
    
    # Summary statistics by healthiness category
    print("\n📈 AVERAGE PRICE BY HEALTHINESS CATEGORY:")
    print("-" * 50)
    summary = df_clean.groupby('Healthiness_Category')['Price_Numeric'].agg(['count', 'mean', 'std']).round(2)
    summary.columns = ['Count', 'Avg Price (CHF)', 'Std Dev']
    print(summary.to_string())
    
    # Restaurant comparison
    print("\n🏪 AVERAGE HEALTHINESS AND PRICE BY RESTAURANT:")
    print("-" * 60)
    restaurant_summary = df_clean.groupby('Restaurant').agg({
        'Healthiness_Score': ['mean', 'std'],
        'Price_Numeric': ['mean', 'std']
    }).round(2)
    restaurant_summary.columns = ['Avg Healthiness', 'Health Std', 'Avg Price (CHF)', 'Price Std']
    print(restaurant_summary.to_string())
    
    # Show some examples
    print("\n🍽️  EXAMPLES BY HEALTHINESS CATEGORY:")
    print("-" * 70)
    for category in df_clean['Healthiness_Category'].unique():
        if pd.notna(category):
            example = df_clean[df_clean['Healthiness_Category'] == category].iloc[0]
            print(f"{category} Healthiness: {example['Dish']} ({example['Healthiness_Score']}/100, {example['Price_Numeric']:.1f} CHF)")
    
    return df_clean

if __name__ == "__main__":
    dataset = create_healthiness_cost_visualizations()