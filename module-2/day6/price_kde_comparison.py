#!/usr/bin/env python3
"""
Create a kernel density estimation (KDE) plot comparing dish price distributions
between Zeughauskeller (orange) and La Fonte (blue)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re

def extract_price_values(price_str):
    """Extract numeric price values from price strings"""
    if pd.isna(price_str):
        return np.nan
    
    # Extract all numbers from the price string
    numbers = re.findall(r'\d+\.?\d*', str(price_str))
    if not numbers:
        return np.nan
    
    # Convert to float and take the first (or average) price
    prices = [float(num) for num in numbers]
    
    # Handle special cases like ranges (Klein/Groß) or sharing dishes
    if len(prices) == 1:
        return prices[0]
    elif len(prices) == 2:
        # For dishes with two prices (like Klein/Groß), take the average
        return np.mean(prices)
    else:
        # For multiple prices, take the first one
        return prices[0]

def load_and_process_data():
    """Load both restaurant datasets and process price data"""
    
    # Load La Fonte data
    la_fonte_df = pd.read_csv('/workspaces/cas-uzh/module-2/day6/la_fonte_menu_dishes.csv')
    la_fonte_df['Restaurant_Clean'] = 'La Fonte'
    
    # Load Zeughauskeller data
    zeughaus_df = pd.read_csv('/workspaces/cas-uzh/module-2/day6/zeughauskeller_menu_dishes.csv')
    zeughaus_df['Restaurant_Clean'] = 'Zeughauskeller'
    
    # Combine datasets
    combined_df = pd.concat([la_fonte_df, zeughaus_df], ignore_index=True)
    
    # Extract numeric prices
    combined_df['Price_Numeric'] = combined_df['Price'].apply(extract_price_values)
    
    # Remove rows with missing or extreme prices (sharing dishes)
    combined_df = combined_df.dropna(subset=['Price_Numeric'])
    
    # Filter out extreme outliers (dishes for sharing)
    combined_df = combined_df[combined_df['Price_Numeric'] <= 50]  # Remove sharing dishes like Mayor's sword
    
    return combined_df

def create_kde_plot(data):
    """Create KDE plot comparing price distributions"""
    
    # Set style
    plt.style.use('default')
    sns.set_palette("husl")
    
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Separate data by restaurant
    la_fonte_prices = data[data['Restaurant_Clean'] == 'La Fonte']['Price_Numeric']
    zeughaus_prices = data[data['Restaurant_Clean'] == 'Zeughauskeller']['Price_Numeric']
    
    # Create KDE plots
    sns.kdeplot(data=la_fonte_prices, label='La Fonte', color='blue', alpha=0.7, linewidth=2.5)
    sns.kdeplot(data=zeughaus_prices, label='Zeughauskeller', color='orange', alpha=0.7, linewidth=2.5)
    
    # Customize plot
    ax.set_xlabel('Price (CHF)', fontsize=14, fontweight='bold')
    ax.set_ylabel('Density', fontsize=14, fontweight='bold')
    ax.set_title('Kernel Density Estimation (KDE)\nDish Price Distribution Comparison', 
                fontsize=16, fontweight='bold', pad=20)
    
    # Add legend
    ax.legend(fontsize=12, loc='upper right')
    
    # Add grid
    ax.grid(True, alpha=0.3, linestyle='--')
    
    # Set axis limits with some padding
    price_min = data['Price_Numeric'].min() - 2
    price_max = data['Price_Numeric'].max() + 2
    ax.set_xlim(price_min, price_max)
    
    # Add statistics annotations
    la_fonte_mean = la_fonte_prices.mean()
    la_fonte_std = la_fonte_prices.std()
    zeughaus_mean = zeughaus_prices.mean()
    zeughaus_std = zeughaus_prices.std()
    
    # Add text box with statistics
    stats_text = f"""Statistics:
La Fonte: μ = {la_fonte_mean:.1f} CHF, σ = {la_fonte_std:.1f} CHF (n={len(la_fonte_prices)})
Zeughauskeller: μ = {zeughaus_mean:.1f} CHF, σ = {zeughaus_std:.1f} CHF (n={len(zeughaus_prices)})"""
    
    ax.text(0.02, 0.98, stats_text, transform=ax.transAxes, fontsize=10, 
            verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    # Adjust layout
    plt.tight_layout()
    
    return fig

def create_detailed_analysis(data):
    """Create detailed statistical analysis"""
    
    print("=" * 70)
    print("RESTAURANT PRICE DISTRIBUTION ANALYSIS")
    print("=" * 70)
    print()
    
    # Separate data by restaurant
    la_fonte_data = data[data['Restaurant_Clean'] == 'La Fonte']
    zeughaus_data = data[data['Restaurant_Clean'] == 'Zeughauskeller']
    
    print("DATASET OVERVIEW:")
    print("-" * 30)
    print(f"La Fonte dishes analyzed: {len(la_fonte_data)}")
    print(f"Zeughauskeller dishes analyzed: {len(zeughaus_data)}")
    print(f"Total dishes: {len(data)}")
    print()
    
    print("PRICE STATISTICS:")
    print("-" * 30)
    
    # La Fonte statistics
    la_fonte_prices = la_fonte_data['Price_Numeric']
    print("La Fonte Restaurant:")
    print(f"  Mean price: {la_fonte_prices.mean():.2f} CHF")
    print(f"  Median price: {la_fonte_prices.median():.2f} CHF")
    print(f"  Standard deviation: {la_fonte_prices.std():.2f} CHF")
    print(f"  Min price: {la_fonte_prices.min():.2f} CHF")
    print(f"  Max price: {la_fonte_prices.max():.2f} CHF")
    print(f"  Price range: {la_fonte_prices.max() - la_fonte_prices.min():.2f} CHF")
    print()
    
    # Zeughauskeller statistics
    zeughaus_prices = zeughaus_data['Price_Numeric']
    print("Zeughauskeller:")
    print(f"  Mean price: {zeughaus_prices.mean():.2f} CHF")
    print(f"  Median price: {zeughaus_prices.median():.2f} CHF")
    print(f"  Standard deviation: {zeughaus_prices.std():.2f} CHF")
    print(f"  Min price: {zeughaus_prices.min():.2f} CHF")
    print(f"  Max price: {zeughaus_prices.max():.2f} CHF")
    print(f"  Price range: {zeughaus_prices.max() - zeughaus_prices.min():.2f} CHF")
    print()
    
    print("COMPARATIVE ANALYSIS:")
    print("-" * 30)
    mean_diff = zeughaus_prices.mean() - la_fonte_prices.mean()
    median_diff = zeughaus_prices.median() - la_fonte_prices.median()
    
    print(f"Mean price difference: {mean_diff:.2f} CHF")
    print(f"  ({'Higher' if mean_diff > 0 else 'Lower'} at {'Zeughauskeller' if mean_diff > 0 else 'La Fonte'})")
    print(f"Median price difference: {median_diff:.2f} CHF")
    print(f"  ({'Higher' if median_diff > 0 else 'Lower'} at {'Zeughauskeller' if median_diff > 0 else 'La Fonte'})")
    print()
    
    # Price categories
    print("PRICE CATEGORY BREAKDOWN:")
    print("-" * 30)
    
    def categorize_price(price):
        if price < 15:
            return "Budget (< 15 CHF)"
        elif price < 25:
            return "Moderate (15-25 CHF)"
        elif price < 35:
            return "Premium (25-35 CHF)"
        else:
            return "Luxury (> 35 CHF)"
    
    la_fonte_data['Price_Category'] = la_fonte_data['Price_Numeric'].apply(categorize_price)
    zeughaus_data['Price_Category'] = zeughaus_data['Price_Numeric'].apply(categorize_price)
    
    print("La Fonte:")
    la_fonte_cats = la_fonte_data['Price_Category'].value_counts()
    for cat, count in la_fonte_cats.items():
        print(f"  {cat}: {count} dishes ({count/len(la_fonte_data)*100:.1f}%)")
    
    print("\nZeughauskeller:")
    zeughaus_cats = zeughaus_data['Price_Category'].value_counts()
    for cat, count in zeughaus_cats.items():
        print(f"  {cat}: {count} dishes ({count/len(zeughaus_data)*100:.1f}%)")

def main():
    """Main function"""
    
    print("Loading and processing restaurant data...")
    data = load_and_process_data()
    
    print("Creating KDE plot...")
    fig = create_kde_plot(data)
    
    # Save plot
    output_path = '/workspaces/cas-uzh/module-2/day6/restaurant_price_kde_comparison.png'
    fig.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"KDE plot saved to: {output_path}")
    
    # Display plot
    plt.show()
    
    # Create detailed analysis
    create_detailed_analysis(data)
    
    print("\n" + "=" * 70)
    print("KDE PLOT INTERPRETATION:")
    print("=" * 70)
    print("• Blue curve (La Fonte): Italian restaurant price distribution")
    print("• Orange curve (Zeughauskeller): Swiss/German restaurant price distribution")
    print("• Higher peaks indicate more common price points")
    print("• Curve width indicates price variability")
    print("• Overlapping areas show similar pricing ranges")

if __name__ == "__main__":
    # Install required packages
    import subprocess
    import sys
    
    try:
        import matplotlib.pyplot as plt
        import seaborn as sns
    except ImportError:
        print("Installing required packages...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'matplotlib', 'seaborn'], check=True)
        import matplotlib.pyplot as plt
        import seaborn as sns
    
    main()