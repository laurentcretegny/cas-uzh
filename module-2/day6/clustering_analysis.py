#!/usr/bin/env python3
"""
Perform k-means clustering on COGS attributes and visualize results
using 2D PCA projection with categorical colors for clusters.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import seaborn as sns

def perform_clustering_analysis():
    """Perform k-means clustering with k=4 and k=6 on COGS attributes."""
    
    # Load the data
    df = pd.read_csv('zeughauskeller-cogs.csv')
    
    # Select COGS attributes (columns starting with "COGS_")
    cogs_columns = [col for col in df.columns if col.startswith('COGS_')]
    print(f"📊 Using {len(cogs_columns)} COGS attributes for clustering")
    
    # Extract features and dish names
    X = df[cogs_columns].values
    dish_names = df['Dish Name'].values
    
    # Handle missing values
    if np.any(np.isnan(X)):
        print("⚠️  Warning: Found missing values, filling with 0...")
        X = np.nan_to_num(X, nan=0.0)
    
    # Standardize the features (important for both PCA and k-means)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Perform PCA for visualization
    pca = PCA(n_components=2, random_state=42)
    X_pca = pca.fit_transform(X_scaled)
    
    # Perform k-means clustering with k=4 and k=6
    kmeans_4 = KMeans(n_clusters=4, random_state=42, n_init=10)
    kmeans_6 = KMeans(n_clusters=6, random_state=42, n_init=10)
    
    clusters_4 = kmeans_4.fit_predict(X_scaled)
    clusters_6 = kmeans_6.fit_predict(X_scaled)
    
    print(f"\n🎯 Clustering Results:")
    print(f"  K=4 clustering - Inertia: {kmeans_4.inertia_:.2f}")
    print(f"  K=6 clustering - Inertia: {kmeans_6.inertia_:.2f}")
    
    # Create side-by-side visualization
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8))
    
    # Define color palettes for clusters
    colors_4 = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
    colors_6 = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FECA57', '#B388FF']
    
    # Plot k=4 clustering
    for cluster in range(4):
        mask = clusters_4 == cluster
        ax1.scatter(X_pca[mask, 0], X_pca[mask, 1], 
                   c=colors_4[cluster], 
                   label=f'Cluster {cluster + 1}', 
                   s=80, alpha=0.7, edgecolors='black', linewidth=0.5)
    
    # Add cluster centers for k=4
    centers_4_pca = pca.transform(kmeans_4.cluster_centers_)
    ax1.scatter(centers_4_pca[:, 0], centers_4_pca[:, 1], 
               c='red', marker='x', s=200, linewidths=3, label='Centroids')
    
    ax1.set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]*100:.1f}% variance)', fontsize=12)
    ax1.set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]*100:.1f}% variance)', fontsize=12)
    ax1.set_title('K-Means Clustering (k=4)\nZeughauskeller Dishes by COGS', fontsize=14, fontweight='bold')
    ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    ax1.grid(True, alpha=0.3)
    
    # Plot k=6 clustering
    for cluster in range(6):
        mask = clusters_6 == cluster
        ax2.scatter(X_pca[mask, 0], X_pca[mask, 1], 
                   c=colors_6[cluster], 
                   label=f'Cluster {cluster + 1}', 
                   s=80, alpha=0.7, edgecolors='black', linewidth=0.5)
    
    # Add cluster centers for k=6
    centers_6_pca = pca.transform(kmeans_6.cluster_centers_)
    ax2.scatter(centers_6_pca[:, 0], centers_6_pca[:, 1], 
               c='red', marker='x', s=200, linewidths=3, label='Centroids')
    
    ax2.set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]*100:.1f}% variance)', fontsize=12)
    ax2.set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]*100:.1f}% variance)', fontsize=12)
    ax2.set_title('K-Means Clustering (k=6)\nZeughauskeller Dishes by COGS', fontsize=14, fontweight='bold')
    ax2.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('zeughauskeller_clustering_analysis.png', dpi=300, bbox_inches='tight')
    print(f"\n✅ Clustering visualization saved to: zeughauskeller_clustering_analysis.png")
    
    # Analyze cluster compositions
    print(f"\n" + "="*80)
    print("CLUSTER ANALYSIS RESULTS")
    print("="*80)
    
    # Analysis for k=4
    print(f"\n🔍 K=4 CLUSTERING ANALYSIS:")
    print("-" * 50)
    for cluster in range(4):
        mask = clusters_4 == cluster
        cluster_dishes = dish_names[mask]
        print(f"\nCluster {cluster + 1} ({len(cluster_dishes)} dishes):")
        for dish in cluster_dishes:
            print(f"  • {dish}")
    
    # Analysis for k=6
    print(f"\n🔍 K=6 CLUSTERING ANALYSIS:")
    print("-" * 50)
    for cluster in range(6):
        mask = clusters_6 == cluster
        cluster_dishes = dish_names[mask]
        print(f"\nCluster {cluster + 1} ({len(cluster_dishes)} dishes):")
        for dish in cluster_dishes:
            print(f"  • {dish}")
    
    # Calculate cluster centers in original space and analyze
    print(f"\n📊 CLUSTER CHARACTERISTICS (K=4):")
    print("-" * 60)
    
    # Create DataFrame for easier analysis
    df_analysis = df.copy()
    df_analysis['Cluster_4'] = clusters_4
    df_analysis['Cluster_6'] = clusters_6
    
    # Analyze dominant COGS attributes for each cluster (k=4)
    for cluster in range(4):
        cluster_data = df_analysis[df_analysis['Cluster_4'] == cluster]
        print(f"\nCluster {cluster + 1} (k=4) - Average COGS profile:")
        
        # Calculate mean COGS for this cluster
        cluster_means = cluster_data[cogs_columns].mean()
        
        # Find top 3 COGS categories
        top_cogs = cluster_means.nlargest(3)
        for cogs_type, value in top_cogs.items():
            if value > 0.1:  # Only show meaningful values
                cogs_name = cogs_type.replace('COGS_', '').replace(' (CHF)', '')
                print(f"    {cogs_name}: {value:.2f} CHF")
    
    print(f"\n📊 CLUSTER CHARACTERISTICS (K=6):")
    print("-" * 60)
    
    # Analyze dominant COGS attributes for each cluster (k=6)
    for cluster in range(6):
        cluster_data = df_analysis[df_analysis['Cluster_6'] == cluster]
        if len(cluster_data) > 0:  # Check if cluster has dishes
            print(f"\nCluster {cluster + 1} (k=6) - Average COGS profile:")
            
            # Calculate mean COGS for this cluster
            cluster_means = cluster_data[cogs_columns].mean()
            
            # Find top 3 COGS categories
            top_cogs = cluster_means.nlargest(3)
            for cogs_type, value in top_cogs.items():
                if value > 0.1:  # Only show meaningful values
                    cogs_name = cogs_type.replace('COGS_', '').replace(' (CHF)', '')
                    print(f"    {cogs_name}: {value:.2f} CHF")
    
    # Calculate silhouette scores for cluster quality assessment
    from sklearn.metrics import silhouette_score
    
    sil_score_4 = silhouette_score(X_scaled, clusters_4)
    sil_score_6 = silhouette_score(X_scaled, clusters_6)
    
    print(f"\n📈 CLUSTERING QUALITY METRICS:")
    print("-" * 40)
    print(f"Silhouette Score (k=4): {sil_score_4:.3f}")
    print(f"Silhouette Score (k=6): {sil_score_6:.3f}")
    print(f"Inertia (k=4): {kmeans_4.inertia_:.2f}")
    print(f"Inertia (k=6): {kmeans_6.inertia_:.2f}")
    
    if sil_score_4 > sil_score_6:
        print(f"🏆 Better clustering: k=4 (higher silhouette score)")
    else:
        print(f"🏆 Better clustering: k=6 (higher silhouette score)")
    
    # Save cluster assignments to CSV for further analysis
    df_with_clusters = df.copy()
    df_with_clusters['Cluster_k4'] = clusters_4 + 1  # 1-indexed for readability
    df_with_clusters['Cluster_k6'] = clusters_6 + 1
    df_with_clusters['PCA_PC1'] = X_pca[:, 0]
    df_with_clusters['PCA_PC2'] = X_pca[:, 1]
    
    df_with_clusters.to_csv('zeughauskeller_clustering_results.csv', index=False)
    print(f"\n✅ Detailed results saved to: zeughauskeller_clustering_results.csv")
    
    return {
        'clusters_4': clusters_4,
        'clusters_6': clusters_6,
        'pca_coordinates': X_pca,
        'kmeans_4': kmeans_4,
        'kmeans_6': kmeans_6,
        'silhouette_scores': {'k4': sil_score_4, 'k6': sil_score_6}
    }

if __name__ == "__main__":
    results = perform_clustering_analysis()