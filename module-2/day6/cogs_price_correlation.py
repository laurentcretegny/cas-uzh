#!/usr/bin/env python3
"""
Create a correlation matrix showing Price vs each COGS attribute
with scatter plots, fitted lines, and R squared values in a 2x5 layout.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import re

def extract_numeric_price(price_str):
    """Extract numeric price from price string."""
    if pd.isna(price_str):
        return None
    
    # Extract all numbers from the price string
    numbers = re.findall(r'\d+\.?\d*', str(price_str))
    if numbers:
        prices = [float(num) for num in numbers]
        return sum(prices) / len(prices)  # Average if multiple prices
    return None

def create_cogs_price_correlation_matrix():
    """Create correlation matrix of Price vs. each COGS attribute."""
    
    # Load the data
    df = pd.read_csv('zeughauskeller-cogs.csv')
    
    # Extract numeric price
    df['Price_Numeric'] = df['Price (CHF)'].apply(extract_numeric_price)
    
    # Select COGS attributes
    cogs_columns = [col for col in df.columns if col.startswith('COGS_')]
    print(f"📊 Analyzing correlation for {len(cogs_columns)} COGS attributes with Price")
    
    # Remove rows with missing price data
    df_clean = df.dropna(subset=['Price_Numeric'])
    
    # Create the 2x5 subplot layout
    fig, axes = plt.subplots(2, 5, figsize=(20, 10))
    fig.suptitle('Price vs. COGS Attributes Correlation Analysis\nZeughauskeller Restaurant', 
                 fontsize=16, fontweight='bold', y=0.95)
    
    # Flatten axes array for easier iteration
    axes_flat = axes.flatten()
    
    # Store correlation results
    correlation_results = []
    
    # Create scatter plots for each COGS attribute
    for i, cogs_col in enumerate(cogs_columns):
        ax = axes_flat[i]
        
        # Get data
        x = df_clean[cogs_col]
        y = df_clean['Price_Numeric']
        
        # Create scatter plot
        ax.scatter(x, y, alpha=0.7, s=60, edgecolors='black', linewidth=0.5, color='steelblue')
        
        # Calculate correlation and fit line
        if len(x) > 1 and x.std() > 0:  # Check if there's variation in x
            # Fit linear regression
            X_reshaped = x.values.reshape(-1, 1)
            lr = LinearRegression()
            lr.fit(X_reshaped, y)
            y_pred = lr.predict(X_reshaped)
            
            # Calculate R²
            r2 = r2_score(y, y_pred)
            
            # Plot fitted line
            sorted_indices = np.argsort(x)
            ax.plot(x.iloc[sorted_indices], y_pred[sorted_indices], 
                   color='red', linewidth=2, alpha=0.8)
            
            # Calculate Pearson correlation coefficient
            pearson_r = np.corrcoef(x, y)[0, 1]
            
        else:
            r2 = 0
            pearson_r = 0
        
        # Store results
        correlation_results.append({
            'COGS_Attribute': cogs_col,
            'R_squared': r2,
            'Pearson_r': pearson_r,
            'Mean_COGS': x.mean(),
            'Max_COGS': x.max()
        })
        
        # Customize subplot
        cogs_name = cogs_col.replace('COGS_', '').replace(' (CHF)', '')
        ax.set_xlabel(f'{cogs_name} (CHF)', fontsize=10)
        ax.set_ylabel('Price (CHF)', fontsize=10)
        ax.set_title(f'{cogs_name}\nR² = {r2:.3f}', fontsize=11, fontweight='bold')
        ax.grid(True, alpha=0.3)
        
        # Add R² text box
        ax.text(0.05, 0.95, f'R² = {r2:.3f}', transform=ax.transAxes,
                bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7),
                fontsize=9, fontweight='bold')
        
        # Set consistent y-axis for all subplots
        ax.set_ylim(0, df_clean['Price_Numeric'].max() * 1.05)
    
    plt.tight_layout()
    plt.subplots_adjust(top=0.9)
    plt.savefig('cogs_price_correlation_matrix.png', dpi=300, bbox_inches='tight')
    print(f"\n✅ Correlation matrix saved to: cogs_price_correlation_matrix.png")
    
    # Print detailed correlation analysis
    print(f"\n" + "="*80)
    print("PRICE vs. COGS CORRELATION ANALYSIS RESULTS")
    print("="*80)
    
    # Sort by R² value for ranking
    correlation_df = pd.DataFrame(correlation_results)
    correlation_df = correlation_df.sort_values('R_squared', ascending=False)
    
    print(f"\n🏆 CORRELATION STRENGTH RANKING (by R²):")
    print("-" * 60)
    
    for i, row in correlation_df.iterrows():
        cogs_name = row['COGS_Attribute'].replace('COGS_', '').replace(' (CHF)', '')
        r2 = row['R_squared']
        pearson_r = row['Pearson_r']
        
        # Interpret correlation strength
        if r2 > 0.7:
            strength = "Very Strong"
        elif r2 > 0.5:
            strength = "Strong"
        elif r2 > 0.3:
            strength = "Moderate"
        elif r2 > 0.1:
            strength = "Weak"
        else:
            strength = "Very Weak"
        
        print(f"{len(correlation_df) - list(correlation_df.index).index(i):2d}. {cogs_name:<20} | "
              f"R² = {r2:.3f} | r = {pearson_r:+.3f} | {strength}")
    
    # Statistical summary
    print(f"\n📊 STATISTICAL SUMMARY:")
    print("-" * 40)
    print(f"Highest R²: {correlation_df['R_squared'].max():.3f} ({correlation_df.iloc[0]['COGS_Attribute'].replace('COGS_', '').replace(' (CHF)', '')})")
    print(f"Lowest R²:  {correlation_df['R_squared'].min():.3f} ({correlation_df.iloc[-1]['COGS_Attribute'].replace('COGS_', '').replace(' (CHF)', '')})")
    print(f"Mean R²:    {correlation_df['R_squared'].mean():.3f}")
    print(f"Median R²:  {correlation_df['R_squared'].median():.3f}")
    
    # Business insights
    print(f"\n💡 BUSINESS INSIGHTS:")
    print("-" * 30)
    
    strong_predictors = correlation_df[correlation_df['R_squared'] > 0.3]
    if len(strong_predictors) > 0:
        print(f"🎯 Strong price predictors ({len(strong_predictors)} attributes):")
        for _, row in strong_predictors.iterrows():
            cogs_name = row['COGS_Attribute'].replace('COGS_', '').replace(' (CHF)', '')
            print(f"   • {cogs_name} (R² = {row['R_squared']:.3f})")
    else:
        print("🎯 No strong individual price predictors found")
    
    weak_predictors = correlation_df[correlation_df['R_squared'] < 0.1]
    if len(weak_predictors) > 0:
        print(f"\n🔍 Weak price predictors ({len(weak_predictors)} attributes):")
        for _, row in weak_predictors.iterrows():
            cogs_name = row['COGS_Attribute'].replace('COGS_', '').replace(' (CHF)', '')
            print(f"   • {cogs_name} (R² = {row['R_squared']:.3f})")
    
    # Cost distribution analysis
    print(f"\n📈 COST DISTRIBUTION PATTERNS:")
    print("-" * 40)
    for _, row in correlation_df.head(5).iterrows():  # Top 5 predictors
        cogs_name = row['COGS_Attribute'].replace('COGS_', '').replace(' (CHF)', '')
        mean_cost = row['Mean_COGS']
        max_cost = row['Max_COGS']
        if mean_cost > 0:
            print(f"{cogs_name}: Avg {mean_cost:.2f} CHF, Max {max_cost:.2f} CHF")
    
    # Save detailed results
    correlation_df.to_csv('cogs_price_correlation_results.csv', index=False)
    print(f"\n✅ Detailed correlation results saved to: cogs_price_correlation_results.csv")
    
    return correlation_df

if __name__ == "__main__":
    results = create_cogs_price_correlation_matrix()