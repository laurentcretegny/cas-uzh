#!/usr/bin/env python3
"""
Perform PCA dimensionality reduction on COGS attributes and create a scatter plot
with non-overlapping dish name labels.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from adjustText import adjust_text
import seaborn as sns

def perform_pca_analysis():
    """Perform PCA on COGS attributes and create visualization."""
    
    # Load the data
    df = pd.read_csv('zeughauskeller-cogs.csv')
    
    # Select COGS attributes (columns starting with "COGS_")
    cogs_columns = [col for col in df.columns if col.startswith('COGS_')]
    print(f"📊 Found {len(cogs_columns)} COGS attributes:")
    for i, col in enumerate(cogs_columns, 1):
        print(f"  {i}. {col}")
    
    # Extract features and dish names
    X = df[cogs_columns].values
    dish_names = df['Dish Name'].values
    
    # Check for missing values
    if np.any(np.isnan(X)):
        print("⚠️  Warning: Found missing values, filling with 0...")
        X = np.nan_to_num(X, nan=0.0)
    
    print(f"\n📈 Dataset shape: {X.shape}")
    print(f"🍽️  Number of dishes: {len(dish_names)}")
    
    # Standardize the features (important for PCA)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Perform PCA
    pca = PCA(n_components=2, random_state=42)
    X_pca = pca.fit_transform(X_scaled)
    
    # Print PCA results
    print(f"\n🔍 PCA Results:")
    print(f"  Explained variance ratio:")
    print(f"    PC1: {pca.explained_variance_ratio_[0]:.3f} ({pca.explained_variance_ratio_[0]*100:.1f}%)")
    print(f"    PC2: {pca.explained_variance_ratio_[1]:.3f} ({pca.explained_variance_ratio_[1]*100:.1f}%)")
    print(f"    Total explained variance: {sum(pca.explained_variance_ratio_):.3f} ({sum(pca.explained_variance_ratio_)*100:.1f}%)")
    
    # Print component loadings (feature importance)
    print(f"\n📊 Feature loadings (PC1, PC2):")
    loadings = pca.components_.T
    for i, feature in enumerate(cogs_columns):
        print(f"  {feature.replace('COGS_', '')}: ({loadings[i,0]:.3f}, {loadings[i,1]:.3f})")
    
    # Create the visualization
    plt.figure(figsize=(14, 10))
    
    # Create scatter plot
    scatter = plt.scatter(X_pca[:, 0], X_pca[:, 1], 
                         c=range(len(dish_names)), 
                         cmap='tab20', 
                         alpha=0.7, 
                         s=60,
                         edgecolors='black',
                         linewidth=0.5)
    
    # Add labels with adjustment to avoid overlap
    texts = []
    for i, (x, y) in enumerate(X_pca):
        # Truncate long dish names for readability
        label = dish_names[i]
        if len(label) > 20:
            label = label[:20] + "..."
        
        text = plt.text(x, y, label, fontsize=8, ha='center', va='center',
                       bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.7))
        texts.append(text)
    
    # Adjust text positions to avoid overlap
    adjust_text(texts, 
                arrowprops=dict(arrowstyle='->', color='gray', lw=0.5, alpha=0.7),
                expand_points=(1.2, 1.2),
                expand_text=(1.1, 1.1))
    
    # Customize the plot
    plt.xlabel(f'PC1 ({pca.explained_variance_ratio_[0]*100:.1f}% variance)', fontsize=12, fontweight='bold')
    plt.ylabel(f'PC2 ({pca.explained_variance_ratio_[1]*100:.1f}% variance)', fontsize=12, fontweight='bold')
    plt.title('PCA Analysis: Zeughauskeller Dishes by COGS Attributes', fontsize=14, fontweight='bold')
    
    # Add grid for better readability
    plt.grid(True, alpha=0.3)
    
    # Add explanation text
    plt.figtext(0.02, 0.02, 
                f'Total explained variance: {sum(pca.explained_variance_ratio_)*100:.1f}%\n'
                f'Each point represents a dish positioned by its COGS cost structure',
                fontsize=9, style='italic')
    
    plt.tight_layout()
    plt.savefig('zeughauskeller_pca_analysis.png', dpi=300, bbox_inches='tight')
    print(f"\n✅ PCA visualization saved to: zeughauskeller_pca_analysis.png")
    
    # Additional analysis: identify extreme dishes
    print(f"\n🎯 Extreme dishes in PCA space:")
    
    # Find dishes at extremes of each PC
    pc1_max = np.argmax(X_pca[:, 0])
    pc1_min = np.argmin(X_pca[:, 0])
    pc2_max = np.argmax(X_pca[:, 1])
    pc2_min = np.argmin(X_pca[:, 1])
    
    print(f"  Highest PC1: {dish_names[pc1_max]} ({X_pca[pc1_max, 0]:.2f})")
    print(f"  Lowest PC1:  {dish_names[pc1_min]} ({X_pca[pc1_min, 0]:.2f})")
    print(f"  Highest PC2: {dish_names[pc2_max]} ({X_pca[pc2_max, 1]:.2f})")
    print(f"  Lowest PC2:  {dish_names[pc2_min]} ({X_pca[pc2_min, 1]:.2f})")
    
    # Create feature importance plot
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # PC1 loadings
    pc1_loadings = loadings[:, 0]
    feature_names_short = [name.replace('COGS_', '').replace(' (CHF)', '') for name in cogs_columns]
    
    bars1 = ax1.barh(range(len(feature_names_short)), pc1_loadings, 
                     color=['red' if x < 0 else 'blue' for x in pc1_loadings])
    ax1.set_yticks(range(len(feature_names_short)))
    ax1.set_yticklabels(feature_names_short)
    ax1.set_xlabel('Loading Strength')
    ax1.set_title(f'PC1 Feature Loadings ({pca.explained_variance_ratio_[0]*100:.1f}% variance)')
    ax1.grid(axis='x', alpha=0.3)
    
    # PC2 loadings
    pc2_loadings = loadings[:, 1]
    bars2 = ax2.barh(range(len(feature_names_short)), pc2_loadings,
                     color=['red' if x < 0 else 'blue' for x in pc2_loadings])
    ax2.set_yticks(range(len(feature_names_short)))
    ax2.set_yticklabels(feature_names_short)
    ax2.set_xlabel('Loading Strength')
    ax2.set_title(f'PC2 Feature Loadings ({pca.explained_variance_ratio_[1]*100:.1f}% variance)')
    ax2.grid(axis='x', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('zeughauskeller_pca_loadings.png', dpi=300, bbox_inches='tight')
    print(f"✅ Feature loadings plot saved to: zeughauskeller_pca_loadings.png")
    
    # Return results for further analysis
    return {
        'pca_coordinates': X_pca,
        'dish_names': dish_names,
        'pca_model': pca,
        'scaler': scaler,
        'explained_variance': pca.explained_variance_ratio_,
        'feature_loadings': loadings,
        'feature_names': cogs_columns
    }

if __name__ == "__main__":
    results = perform_pca_analysis()