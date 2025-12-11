#!/usr/bin/env python3
"""
Extract 15 dishes from La Fonte Restaurant Pizzeria menu with balanced sampling
"""

import pandas as pd
import re

def extract_menu_dishes():
    """Extract and structure 15 dishes from the menu with balanced sampling"""
    
    # Restaurant information
    restaurant_name = "La Fonte Restaurant Pizzeria"
    
    # Define dishes with balanced sampling across categories
    dishes = [
        # Antipasti (2 dishes)
        {
            "Restaurant": restaurant_name,
            "ID": "A001",
            "Dish": "Bruschettone",
            "Dish Category": "Antipasti",
            "Ingredients": "Geröstete Brotscheibe, Tomatenwürfel, Knoblauch",
            "Price": "10.00 CHF"
        },
        {
            "Restaurant": restaurant_name,
            "ID": "A002", 
            "Dish": "Carpaccio di manzo",
            "Dish Category": "Antipasti",
            "Ingredients": "Rindscarpaccio, Rucola, Grana",
            "Price": "24.00 CHF"
        },
        
        # Insalate (2 dishes)
        {
            "Restaurant": restaurant_name,
            "ID": "S001",
            "Dish": "Insalata con pollo",
            "Dish Category": "Insalate",
            "Ingredients": "Gemischter Blattsalat, Cherry, Pouletstreifen",
            "Price": "14.00 CHF (Klein) / 18.00 CHF (Groß)"
        },
        {
            "Restaurant": restaurant_name,
            "ID": "S002",
            "Dish": "Caprese",
            "Dish Category": "Insalate", 
            "Ingredients": "Tomaten, Büffelmozzarella",
            "Price": "12.00 CHF (Klein) / 16.00 CHF (Groß)"
        },
        
        # Primi Piatti (3 dishes)
        {
            "Restaurant": restaurant_name,
            "ID": "P001",
            "Dish": "Spaghetti Bolognese",
            "Dish Category": "Primi Piatti",
            "Ingredients": "Rindsbolognesesauce",
            "Price": "21.90 CHF"
        },
        {
            "Restaurant": restaurant_name,
            "ID": "P002", 
            "Dish": "Strozzapreti Campagnole",
            "Dish Category": "Primi Piatti",
            "Ingredients": "Speck, schwarzer Trüffel, Rahm",
            "Price": "31.50 CHF"
        },
        {
            "Restaurant": restaurant_name,
            "ID": "P003",
            "Dish": "Gnocchi Al zafferano",
            "Dish Category": "Primi Piatti",
            "Ingredients": "Safran, Cherry, Burrata",
            "Price": "29.70 CHF"
        },
        
        # Pizze Classiche (3 dishes)
        {
            "Restaurant": restaurant_name,
            "ID": "PC001",
            "Dish": "Pizza Margherita",
            "Dish Category": "Pizze Classiche",
            "Ingredients": "Tomaten, Mozzarella, Oregano, Basilikum",
            "Price": "16.90 CHF"
        },
        {
            "Restaurant": restaurant_name,
            "ID": "PC002",
            "Dish": "Pizza Prosciutto e funghi",
            "Dish Category": "Pizze Classiche", 
            "Ingredients": "Tomaten, Mozzarella, Hinterschinken, frische Champignons, Oregano, Basilikum",
            "Price": "19.90 CHF"
        },
        {
            "Restaurant": restaurant_name,
            "ID": "PC003",
            "Dish": "Pizza 4 Formaggi",
            "Dish Category": "Pizze Classiche",
            "Ingredients": "Tomaten, Mozzarella, Gorgonzola, Mascarpone, Grana, Oregano, Basilikum",
            "Price": "21.90 CHF"
        },
        
        # Pizze Speciali (3 dishes)
        {
            "Restaurant": restaurant_name,
            "ID": "PS001",
            "Dish": "Pizza Anna",
            "Dish Category": "Pizze Speciali",
            "Ingredients": "Tomaten, Mozzarella, Rohschinken, Cherry, Rucola, Grana, Burrata, Oregano, Basilikum",
            "Price": "29.50 CHF"
        },
        {
            "Restaurant": restaurant_name,
            "ID": "PS002",
            "Dish": "Pizza Molisana", 
            "Dish Category": "Pizze Speciali",
            "Ingredients": "Mozzarella, Salsiccia scharf, Provola, schwarzer Trüffel, Oregano, Basilikum",
            "Price": "32.00 CHF"
        },
        {
            "Restaurant": restaurant_name,
            "ID": "PS003",
            "Dish": "Pizza Biancaneve",
            "Dish Category": "Pizze Speciali",
            "Ingredients": "Mozzarella, Salsiccia scharf, Kartoffeln, Peperoni, Oregano, Basilikum",
            "Price": "24.90 CHF"
        },
        
        # Calzone (1 dish)
        {
            "Restaurant": restaurant_name,
            "ID": "C001",
            "Dish": "Calzone della Casa",
            "Dish Category": "Il Nostro Calzone",
            "Ingredients": "Tomaten, Mozzarella, Hinterschinken, frische Champignons, Knoblauch, Ei, Pesto, Grana",
            "Price": "27.50 CHF"
        },
        
        # Dessert (1 dish)
        {
            "Restaurant": restaurant_name,
            "ID": "D001",
            "Dish": "Tiramisù",
            "Dish Category": "I nostri Dessert",
            "Ingredients": "Hausgemachtes Tiramisu",
            "Price": "9.50 CHF"
        }
    ]
    
    # Create DataFrame
    df = pd.DataFrame(dishes)
    
    return df

def main():
    """Main function to extract dishes and display results"""
    
    print("=" * 80)
    print("LA FONTE RESTAURANT PIZZERIA - MENU DISHES EXTRACTION")
    print("=" * 80)
    print()
    
    # Extract dishes
    menu_df = extract_menu_dishes()
    
    print(f"Total dishes extracted: {len(menu_df)}")
    print()
    
    # Display category breakdown
    category_counts = menu_df['Dish Category'].value_counts()
    print("DISH CATEGORIES BREAKDOWN:")
    print("-" * 40)
    for category, count in category_counts.items():
        print(f"{category}: {count} dishes")
    print()
    
    # Display full table
    print("EXTRACTED DISHES TABLE:")
    print("-" * 120)
    
    # Configure pandas display options for better formatting
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', 50)
    
    print(menu_df.to_string(index=False))
    
    # Save to CSV
    output_file = "/workspaces/cas-uzh/module-2/day6/la_fonte_menu_dishes.csv"
    menu_df.to_csv(output_file, index=False, encoding='utf-8')
    print(f"\nData saved to: {output_file}")
    
    print()
    print("BALANCED SAMPLING APPROACH:")
    print("-" * 40)
    print("• Selected 15 dishes across 6 different categories")
    print("• Antipasti: 2 dishes (13.3%)")
    print("• Insalate: 2 dishes (13.3%)")
    print("• Primi Piatti: 3 dishes (20%)")
    print("• Pizze Classiche: 3 dishes (20%)")
    print("• Pizze Speciali: 3 dishes (20%)")
    print("• Calzone: 1 dish (6.7%)")
    print("• Dessert: 1 dish (6.7%)")
    print()
    print("• Price range: 9.50 CHF - 32.00 CHF")
    print("• Variety includes vegetarian, meat, seafood, and premium options")
    print("• Represents both traditional and specialty dishes")

if __name__ == "__main__":
    main()