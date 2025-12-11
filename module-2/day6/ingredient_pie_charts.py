#!/usr/bin/env python3
"""
Create pie charts showing the proportion of dishes containing each ingredient
for Zeughauskeller and La Fonte restaurants
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re
from collections import Counter

def clean_and_extract_ingredients(ingredients_str):
    """Clean and extract individual ingredients from ingredient strings"""
    if pd.isna(ingredients_str):
        return []
    
    # Convert to lowercase for consistency
    ingredients_str = str(ingredients_str).lower()
    
    # Remove common non-ingredient words and punctuation
    ingredients_str = re.sub(r'[(),"]', '', ingredients_str)
    ingredients_str = re.sub(r'\b(served with|garnished with|made in|according to|recipe from|for|persons|specialty|hausgemacht|homemade|und|and|with|fresh|frisch)\b', '', ingredients_str)
    
    # Split by common separators
    ingredients = re.split(r'[,;]', ingredients_str)
    
    # Clean each ingredient
    cleaned_ingredients = []
    for ingredient in ingredients:
        ingredient = ingredient.strip()
        if len(ingredient) > 2 and ingredient not in ['chf', 'klein', 'groß', 'regular', 'portion', 'oder', 'or', 'also']:
            # Standardize common ingredient names
            ingredient = standardize_ingredient_name(ingredient)
            if ingredient:
                cleaned_ingredients.append(ingredient)
    
    return cleaned_ingredients

def standardize_ingredient_name(ingredient):
    """Standardize ingredient names for consistent counting"""
    
    ingredient = ingredient.strip().lower()
    
    # Dictionary for ingredient standardization
    standardization_map = {
        # Cheese variations
        'mozzarella': 'mozzarella',
        'büffelmozzarella': 'mozzarella',
        'buffalo mozzarella': 'mozzarella',
        'gorgonzola': 'gorgonzola', 
        'mascarpone': 'mascarpone',
        'grana': 'grana/parmesan',
        'parmesan': 'grana/parmesan',
        'gruyère': 'gruyère',
        'swiss gruyère cheese': 'gruyère',
        'swiss cheese': 'gruyère',
        'provola': 'provola',
        'burrata': 'burrata',
        
        # Tomato variations
        'tomaten': 'tomatoes',
        'tomatoes': 'tomatoes',
        'tomatensauce': 'tomatoes',
        'tomato sauce': 'tomatoes',
        'tomatenwürfel': 'tomatoes',
        'tomato cubes': 'tomatoes',
        'tomatenscheiben': 'tomatoes',
        'cherry': 'cherry tomatoes',
        'cherry tomatoes': 'cherry tomatoes',
        
        # Meat variations
        'hinterschinken': 'ham',
        'ham': 'ham',
        'prosciutto': 'ham',
        'rohschinken': 'prosciutto',
        'speck': 'bacon',
        'bacon': 'bacon',
        'salami scharf': 'spicy salami',
        'salami mild': 'mild salami',
        'salsiccia': 'sausage',
        'sausage': 'sausage',
        'veal': 'veal',
        'kalbsgeschnetzeltes': 'veal',
        'kalbs': 'veal',
        'beef': 'beef',
        'rindscarpaccio': 'beef carpaccio',
        'rinds': 'beef',
        'rind': 'beef',
        'pork': 'pork',
        'chicken': 'chicken',
        'poulet': 'chicken',
        'pouletstreifen': 'chicken',
        'swiss gourmet chicken': 'chicken',
        
        # Vegetables
        'rucola': 'arugula',
        'arugula': 'arugula',
        'spinat': 'spinach',
        'spinach': 'spinach',
        'zwiebeln': 'onions',
        'onions': 'onions',
        'knoblauch': 'garlic',
        'garlic': 'garlic',
        'champignons': 'mushrooms',
        'mushrooms': 'mushrooms',
        'frische champignons': 'mushrooms',
        'steinpilze': 'porcini mushrooms',
        'peperoni': 'peppers',
        'peppers': 'peppers',
        'zucchetti': 'zucchini',
        'zucchini': 'zucchini',
        'auberginen': 'eggplant',
        'eggplant': 'eggplant',
        
        # Herbs and seasonings
        'oregano': 'oregano',
        'basilikum': 'basil',
        'basil': 'basil',
        'peperoncino': 'chili',
        'chili': 'chili',
        'herbs': 'herbs',
        'kräuter': 'herbs',
        
        # Sauces and creams
        'rahm': 'cream',
        'cream': 'cream',
        'cream sauce': 'cream sauce',
        'creamy white-wine sauce': 'wine cream sauce',
        'onion sauce': 'onion sauce',
        'tartar sauce': 'tartar sauce',
        'rindsbolognesesauce': 'bolognese sauce',
        'bolognese sauce': 'bolognese sauce',
        
        # Carbs and sides
        'potato': 'potatoes',
        'potatoes': 'potatoes',
        'kartoffeln': 'potatoes',
        'potato salad': 'potato salad',
        'homemade potato salad': 'potato salad',
        'rösti': 'rösti',
        'french fries': 'french fries',
        'noodles': 'pasta',
        'pasta': 'pasta',
        'macaroni': 'pasta',
        'rice': 'rice',
        'bread': 'bread',
        'toast': 'toast',
        'butter': 'butter',
        
        # Salad ingredients
        'gemischter blattsalat': 'mixed salad',
        'mixed salad': 'mixed salad',
        'mixed green salad': 'mixed salad',
        'green salad': 'salad',
        'salad': 'salad',
        'salad garnish': 'salad',
        
        # Seafood
        'perch fillets': 'perch',
        'perch': 'perch',
        
        # Other
        'ei': 'egg',
        'egg': 'egg',
        'oliven': 'olives',
        'olives': 'olives',
        'safran': 'saffron',
        'saffron': 'saffron',
        'schwarzer trüffel': 'black truffle',
        'black truffle': 'black truffle',
        'wine': 'wine',
        'white wine': 'wine',
        'coleslaw': 'coleslaw',
        'bbq-sauce': 'bbq sauce',
        'fried onions': 'onions',
        'dark draught beer': 'beer',
        'seasonal ingredients': 'seasonal ingredients'
    }
    
    # Check for exact matches first
    for key, value in standardization_map.items():
        if key == ingredient or key in ingredient:
            return value
    
    # If no match found, return cleaned version if it's substantive
    if len(ingredient) > 2 and ingredient not in ['geröstete brotscheibe', 'boiled', 'pan fried', 'crumbed', 'crispy', 'grilled']:
        return ingredient
    
    return None

def analyze_ingredients(df, restaurant_name):
    """Analyze ingredient frequency for a restaurant"""
    
    all_ingredients = []
    
    for _, row in df.iterrows():
        ingredients = clean_and_extract_ingredients(row['Ingredients'])
        all_ingredients.extend(ingredients)
    
    # Count ingredient frequency
    ingredient_counts = Counter(all_ingredients)
    
    # Filter out very rare ingredients (appear in less than 2 dishes) for cleaner visualization
    min_frequency = 1  # Changed to 1 to show more ingredients
    filtered_counts = {k: v for k, v in ingredient_counts.items() if v >= min_frequency}
    
    # If too many ingredients, keep top 12 for readability
    if len(filtered_counts) > 12:
        sorted_items = sorted(filtered_counts.items(), key=lambda x: x[1], reverse=True)
        filtered_counts = dict(sorted_items[:12])
    
    return filtered_counts

def create_ingredient_pie_charts():
    """Create pie charts for both restaurants showing ingredient proportions"""
    
    # Load data
    la_fonte_df = pd.read_csv('/workspaces/cas-uzh/module-2/day6/la_fonte_menu_dishes.csv')
    zeughaus_df = pd.read_csv('/workspaces/cas-uzh/module-2/day6/zeughauskeller_menu_dishes.csv')
    
    # Analyze ingredients
    la_fonte_ingredients = analyze_ingredients(la_fonte_df, 'La Fonte')
    zeughaus_ingredients = analyze_ingredients(zeughaus_df, 'Zeughauskeller')
    
    # Create figure with subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))
    
    # Define colors for consistency
    colors_la_fonte = plt.cm.Set3(np.linspace(0, 1, len(la_fonte_ingredients)))
    colors_zeughaus = plt.cm.Pastel1(np.linspace(0, 1, len(zeughaus_ingredients)))
    
    # La Fonte pie chart
    if la_fonte_ingredients:
        ingredients_lf = list(la_fonte_ingredients.keys())
        counts_lf = list(la_fonte_ingredients.values())
        
        # Create pie chart
        wedges1, texts1, autotexts1 = ax1.pie(counts_lf, labels=ingredients_lf, colors=colors_la_fonte,
                                             autopct='%1.1f%%', startangle=90, 
                                             textprops={'fontsize': 9})
        
        # Beautify text
        for autotext in autotexts1:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
    
    ax1.set_title('La Fonte Restaurant\nIngredient Distribution', 
                  fontsize=16, fontweight='bold', pad=20)
    
    # Zeughauskeller pie chart
    if zeughaus_ingredients:
        ingredients_zh = list(zeughaus_ingredients.keys())
        counts_zh = list(zeughaus_ingredients.values())
        
        # Create pie chart
        wedges2, texts2, autotexts2 = ax2.pie(counts_zh, labels=ingredients_zh, colors=colors_zeughaus,
                                             autopct='%1.1f%%', startangle=90,
                                             textprops={'fontsize': 9})
        
        # Beautify text
        for autotext in autotexts2:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
    
    ax2.set_title('Zeughauskeller Zurich\nIngredient Distribution', 
                  fontsize=16, fontweight='bold', pad=20)
    
    # Overall title
    fig.suptitle('Restaurant Ingredient Analysis\nProportion of Dishes Containing Each Ingredient', 
                 fontsize=20, fontweight='bold', y=0.95)
    
    # Adjust layout
    plt.tight_layout()
    plt.subplots_adjust(top=0.85)
    
    return fig, la_fonte_ingredients, zeughaus_ingredients

def create_detailed_analysis(la_fonte_ingredients, zeughaus_ingredients):
    """Create detailed analysis of ingredients"""
    
    print("=" * 80)
    print("RESTAURANT INGREDIENT ANALYSIS")
    print("=" * 80)
    print()
    
    print("LA FONTE RESTAURANT:")
    print("-" * 40)
    print(f"Total unique ingredients: {len(la_fonte_ingredients)}")
    print("Top ingredients by frequency:")
    sorted_lf = sorted(la_fonte_ingredients.items(), key=lambda x: x[1], reverse=True)
    for ingredient, count in sorted_lf:
        percentage = (count / 15) * 100  # 15 total dishes
        print(f"  {ingredient}: {count} dishes ({percentage:.1f}%)")
    print()
    
    print("ZEUGHAUSKELLER ZURICH:")
    print("-" * 40)
    print(f"Total unique ingredients: {len(zeughaus_ingredients)}")
    print("Top ingredients by frequency:")
    sorted_zh = sorted(zeughaus_ingredients.items(), key=lambda x: x[1], reverse=True)
    for ingredient, count in sorted_zh:
        percentage = (count / 15) * 100  # 15 total dishes
        print(f"  {ingredient}: {count} dishes ({percentage:.1f}%)")
    print()
    
    # Compare common ingredients
    common_ingredients = set(la_fonte_ingredients.keys()) & set(zeughaus_ingredients.keys())
    if common_ingredients:
        print("COMMON INGREDIENTS:")
        print("-" * 40)
        for ingredient in sorted(common_ingredients):
            lf_count = la_fonte_ingredients[ingredient]
            zh_count = zeughaus_ingredients[ingredient]
            lf_pct = (lf_count / 15) * 100
            zh_pct = (zh_count / 15) * 100
            print(f"  {ingredient}:")
            print(f"    La Fonte: {lf_count} dishes ({lf_pct:.1f}%)")
            print(f"    Zeughauskeller: {zh_count} dishes ({zh_pct:.1f}%)")
    print()
    
    # Unique ingredients
    lf_unique = set(la_fonte_ingredients.keys()) - set(zeughaus_ingredients.keys())
    zh_unique = set(zeughaus_ingredients.keys()) - set(la_fonte_ingredients.keys())
    
    if lf_unique:
        print("LA FONTE UNIQUE INGREDIENTS:")
        print("-" * 40)
        for ingredient in sorted(lf_unique):
            count = la_fonte_ingredients[ingredient]
            percentage = (count / 15) * 100
            print(f"  {ingredient}: {count} dishes ({percentage:.1f}%)")
        print()
    
    if zh_unique:
        print("ZEUGHAUSKELLER UNIQUE INGREDIENTS:")
        print("-" * 40)
        for ingredient in sorted(zh_unique):
            count = zeughaus_ingredients[ingredient]
            percentage = (count / 15) * 100
            print(f"  {ingredient}: {count} dishes ({percentage:.1f}%)")

def main():
    """Main function"""
    
    print("Analyzing ingredient distributions...")
    
    # Create pie charts
    fig, la_fonte_ingredients, zeughaus_ingredients = create_ingredient_pie_charts()
    
    # Save the plot
    output_path = '/workspaces/cas-uzh/module-2/day6/restaurant_ingredient_pie_charts.png'
    fig.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"Ingredient pie charts saved to: {output_path}")
    
    # Display the plot
    plt.show()
    
    # Create detailed analysis
    create_detailed_analysis(la_fonte_ingredients, zeughaus_ingredients)
    
    print("\n" + "=" * 80)
    print("PIE CHART INTERPRETATION:")
    print("=" * 80)
    print("• Larger slices indicate ingredients used in more dishes")
    print("• Percentages show proportion of dishes containing each ingredient")
    print("• La Fonte shows Italian cuisine patterns (mozzarella, tomatoes, basil)")
    print("• Zeughauskeller shows Swiss/German patterns (potatoes, onions, traditional meats)")

if __name__ == "__main__":
    main()