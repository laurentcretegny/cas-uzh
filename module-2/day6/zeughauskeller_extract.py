#!/usr/bin/env python3
"""
Extract 15 dishes from Zeughauskeller menu with balanced sampling
"""

import pandas as pd
import re

def extract_zeughauskeller_dishes():
    """Extract and structure 15 dishes from the Zeughauskeller menu with balanced sampling"""
    
    # Restaurant information
    restaurant_name = "Zeughauskeller Zurich"
    
    # Define dishes with balanced sampling across categories
    dishes = [
        # Homemade Soups (2 dishes)
        {
            "Restaurant": restaurant_name,
            "ID": "S001",
            "Dish": "Beef broth with finely shredded crepe",
            "Dish Category": "Homemade Soups",
            "Ingredients": "Beef broth, finely shredded crepe",
            "Price": "8.00 CHF"
        },
        {
            "Restaurant": restaurant_name,
            "ID": "S002",
            "Dish": "Seasonal soup",
            "Dish Category": "Homemade Soups",
            "Ingredients": "Seasonal ingredients",
            "Price": "9.00 CHF"
        },
        
        # Fresh Salads (1 dish)
        {
            "Restaurant": restaurant_name,
            "ID": "SA001",
            "Dish": "Mixed salad",
            "Dish Category": "Fresh Salads",
            "Ingredients": "Mixed green salad",
            "Price": "9.50 CHF"
        },
        
        # Cold Platters (2 dishes)
        {
            "Restaurant": restaurant_name,
            "ID": "CP001",
            "Dish": "Beefsteak Tartare",
            "Dish Category": "Cold Platters",
            "Ingredients": "Raw beef tartare (mild or spicy), salad garnish, toast, butter",
            "Price": "32.00 CHF (regular portion)"
        },
        {
            "Restaurant": restaurant_name,
            "ID": "CP002",
            "Dish": "Sliced air-dried mountain ham and beef with Swiss Gruyère",
            "Dish Category": "Cold Platters",
            "Ingredients": "Air-dried mountain ham, air-dried mountain beef, shaved Swiss Gruyère cheese",
            "Price": "24.50 CHF"
        },
        
        # Specialities of the House (4 dishes)
        {
            "Restaurant": restaurant_name,
            "ID": "SH001",
            "Dish": "Kalbsgeschnetzeltes nach Zürcher Art",
            "Dish Category": "Specialities of the House",
            "Ingredients": "Panfried sliced veal, mushrooms, creamy white-wine sauce",
            "Price": "36.50 CHF"
        },
        {
            "Restaurant": restaurant_name,
            "ID": "SH002",
            "Dish": "Mayor's sword",
            "Dish Category": "Specialities of the House",
            "Ingredients": "400g marinated baby-beef steaks, mixed salad, Rösti or French fries, curry-garlic and barbecue sauce",
            "Price": "88.00 CHF (for 2 persons)"
        },
        {
            "Restaurant": restaurant_name,
            "ID": "SH003",
            "Dish": "Whole pork shank",
            "Dish Category": "Specialities of the House",
            "Ingredients": "Marinated pork shank with herbs, oven-roasted, dark draught beer, fresh potato salad",
            "Price": "33.00 CHF"
        },
        {
            "Restaurant": restaurant_name,
            "ID": "SH004",
            "Dish": "Deep fried perch fillets",
            "Dish Category": "Specialities of the House",
            "Ingredients": "Perch fillets, boiled potatoes, tartar sauce",
            "Price": "31.00 CHF"
        },
        
        # Our Sausage Favourites (3 dishes)
        {
            "Restaurant": restaurant_name,
            "ID": "SF001",
            "Dish": "The original Kalbsbratwurst",
            "Dish Category": "Our Sausage Favourites",
            "Ingredients": "Pan fried veal sausage (made in Zurich), onion sauce, homemade potato salad",
            "Price": "20.00 CHF"
        },
        {
            "Restaurant": restaurant_name,
            "ID": "SF002",
            "Dish": "Zwingli sausage",
            "Dish Category": "Our Sausage Favourites",
            "Ingredients": "Grilled pork sausage with herbs and pistachio pieces (recipe from 1519), onion sauce, homemade potato salad",
            "Price": "22.00 CHF"
        },
        {
            "Restaurant": restaurant_name,
            "ID": "SF003",
            "Dish": "Vaudois Saucisson",
            "Dish Category": "Our Sausage Favourites",
            "Ingredients": "Smoked pork sausage with bacon, white wine, traditional spice mixture, sauerkraut, boiled potatoes",
            "Price": "29.00 CHF"
        },
        
        # Always a good choice (2 dishes)
        {
            "Restaurant": restaurant_name,
            "ID": "AG001",
            "Dish": "Älplermagronen",
            "Dish Category": "Always a good choice",
            "Ingredients": "Alpine Macaroni (Swiss specialty), potato cubes, onions, cream sauce",
            "Price": "21.50 CHF"
        },
        {
            "Restaurant": restaurant_name,
            "ID": "AG002",
            "Dish": "Zeughauskeller-Burger",
            "Dish Category": "Always a good choice",
            "Ingredients": "2x 120g beef burgers (100% beef), coleslaw, fried onions, bacon, BBQ-sauce, French fries",
            "Price": "28.00 CHF"
        },
        
        # Light dishes (1 dish)
        {
            "Restaurant": restaurant_name,
            "ID": "LD001",
            "Dish": "Tender chicken breast",
            "Dish Category": "Light dishes",
            "Ingredients": "Swiss Gourmet chicken (crumbed and crispy or grilled), green salad",
            "Price": "28.00 CHF"
        }
    ]
    
    # Create DataFrame
    df = pd.DataFrame(dishes)
    
    return df

def main():
    """Main function to extract dishes and display results"""
    
    print("=" * 80)
    print("ZEUGHAUSKELLER ZURICH - MENU DISHES EXTRACTION")
    print("=" * 80)
    print()
    
    # Extract dishes
    menu_df = extract_zeughauskeller_dishes()
    
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
    pd.set_option('display.max_colwidth', 60)
    
    print(menu_df.to_string(index=False))
    
    # Save to CSV
    output_file = "/workspaces/cas-uzh/module-2/day6/zeughauskeller_menu_dishes.csv"
    menu_df.to_csv(output_file, index=False, encoding='utf-8')
    print(f"\nData saved to: {output_file}")
    
    print()
    print("BALANCED SAMPLING APPROACH:")
    print("-" * 40)
    print("• Selected 15 dishes across 6 different categories")
    print("• Specialities of the House: 4 dishes (26.7%)")
    print("• Our Sausage Favourites: 3 dishes (20%)")
    print("• Always a good choice: 2 dishes (13.3%)")
    print("• Homemade Soups: 2 dishes (13.3%)")
    print("• Cold Platters: 2 dishes (13.3%)")
    print("• Fresh Salads: 1 dish (6.7%)")
    print("• Light dishes: 1 dish (6.7%)")
    print()
    print("• Price range: 8.00 CHF - 88.00 CHF")
    print("• Variety includes traditional Swiss, German, and international dishes")
    print("• Features both hearty traditional fare and lighter options")

if __name__ == "__main__":
    main()