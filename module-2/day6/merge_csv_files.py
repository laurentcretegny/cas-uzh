#!/usr/bin/env python3
"""
Merge the two restaurant CSV files into a single combined file.
"""
import pandas as pd

def merge_restaurant_csvs():
    """Merge La Fonte and Zeughauskeller CSV files into one combined file."""
    
    # Read both CSV files
    la_fonte_df = pd.read_csv('la_fonte_menu_dishes.csv')
    zeughauskeller_df = pd.read_csv('zeughauskeller_menu_dishes.csv')
    
    # Combine the DataFrames
    combined_df = pd.concat([la_fonte_df, zeughauskeller_df], ignore_index=True)
    
    # Save the merged file
    output_file = 'combined_restaurant_menus.csv'
    combined_df.to_csv(output_file, index=False)
    
    print(f"✅ Successfully merged restaurant menu files!")
    print(f"📄 Output file: {output_file}")
    print(f"📊 Total dishes: {len(combined_df)}")
    print(f"🍽️  La Fonte dishes: {len(la_fonte_df)}")
    print(f"🍽️  Zeughauskeller dishes: {len(zeughauskeller_df)}")
    
    # Show summary by restaurant
    print("\n" + "="*60)
    print("COMBINED MENU SUMMARY")
    print("="*60)
    restaurant_counts = combined_df['Restaurant'].value_counts()
    for restaurant, count in restaurant_counts.items():
        print(f"{restaurant}: {count} dishes")
    
    # Show first few rows as preview
    print("\n" + "="*60)
    print("PREVIEW OF MERGED DATA")
    print("="*60)
    print(combined_df.head(3).to_string(index=False))
    print("...")
    print(combined_df.tail(3).to_string(index=False))
    
    return output_file

if __name__ == "__main__":
    merge_restaurant_csvs()