# K-Means Clustering Analysis Report: Zeughauskeller COGS Data

## 📊 Analysis Overview
- **Dataset**: Zeughauskeller restaurant dishes COGS analysis  
- **Method**: K-Means clustering with k=4 and k=6
- **Features**: 10 standardized COGS attributes
- **Visualization**: 2D PCA projection with categorical cluster colors
- **Dishes Analyzed**: 39 menu items

## 🎯 Clustering Results Summary

### Quality Metrics
| Metric | K=4 | K=6 | Winner |
|--------|-----|-----|---------|
| **Silhouette Score** | 0.286 | 0.346 | **K=6** ✅ |
| **Inertia (SSE)** | 245.59 | 166.39 | **K=6** ✅ |
| **Interpretation** | Moderate | Better | K=6 preferred |

**Winner**: **K=6 clustering** shows better separation and cohesion.

## 🔍 K=4 Clustering Analysis

### Cluster Profiles

**🥩 Cluster 1: "Premium Meat Dishes" (28 dishes)**
- **Primary COGS**: Meat/Sausage (8.99 CHF), Sauce (1.04 CHF)  
- **Characteristics**: Traditional meat-heavy dishes, sausages, schnitzels
- **Examples**: Viennese schnitzel, Zurich veal bratwurst, Buergermeister Schwert
- **Business Type**: Core revenue generators, traditional Swiss fare

**🥗 Cluster 2: "Fresh Salads" (4 dishes)**  
- **Primary COGS**: Salad Greens (1.48 CHF)
- **Characteristics**: Simple, healthy, low-cost options
- **Examples**: Mixed salad, Butterhead lettuce "Mimosa"
- **Business Type**: Healthy alternatives, high-margin items

**🧀 Cluster 3: "Cheese & Combination Dishes" (6 dishes)**
- **Primary COGS**: Meat/Sausage (3.28 CHF), Cheese (1.47 CHF), Sauce (0.35 CHF)
- **Characteristics**: Dishes combining multiple ingredients, comfort foods
- **Examples**: Cordon bleu varieties, Aelplermagronen, cheese-based dishes
- **Business Type**: Comfort food classics, moderate complexity

**🍖 Cluster 4: "Ultra-Premium Single Item" (1 dish)**
- **Primary COGS**: Meat/Sausage (14.00 CHF), Sauce (2.00 CHF), Rice (0.40 CHF)  
- **Characteristics**: Highest-cost single dish
- **Examples**: Beef pieces
- **Business Type**: Premium offering, potential signature dish

## 🎨 K=6 Clustering Analysis

### Enhanced Granularity Benefits

**🥗 Cluster 1: "Fresh Salads" (4 dishes)**
- Same as K=4 Cluster 2 - pure salad category maintained

**🥩 Cluster 2: "Standard Meat Dishes" (23 dishes)**  
- **Primary COGS**: Meat/Sausage (9.75 CHF), Sauce (1.07 CHF)
- **Refined from K=4**: Separated standard meat dishes from specialty preparations
- **Examples**: Traditional sausages, standard schnitzels, roasts

**🧀 Cluster 3: "Cheese Combinations" (6 dishes)**
- Same as K=4 Cluster 3 - cheese-focused dishes maintained

**🍄 Cluster 4: "Specialty Zurich Veal" (1 dish)**
- **Primary COGS**: Meat/Sausage (6.50 CHF), Mushrooms (2.50 CHF), Sauce (1.50 CHF)
- **New separation**: Isolated the mushroom-heavy Zurich specialty
- **Examples**: Sliced veal in Zurich style

**🍔 Cluster 5: "Modern Preparations" (4 dishes)**  
- **Primary COGS**: Meat/Sausage (5.22 CHF), Sauce (0.71 CHF), Bread/Toast (0.47 CHF)
- **New category**: Contemporary dishes with bread components
- **Examples**: Burgers, tartare preparations

**🍖 Cluster 6: "Ultra-Premium" (1 dish)**
- Same as K=4 Cluster 4 - maintained premium isolation

## 🏪 Business Strategy Insights

### Menu Portfolio Analysis

**Cost Structure Segmentation:**
1. **Low-Cost, High-Margin** (Salads): 10% of menu, healthy positioning
2. **Core Revenue** (Standard Meats): 59% of menu, traditional Swiss cuisine  
3. **Specialty Items** (Cheese combos, Zurich veal): 18% of menu, unique offerings
4. **Premium Tier** (Ultra-premium): 5% of menu, prestige items
5. **Modern Appeal** (Contemporary prep): 10% of menu, younger demographics

### Operational Implications

**K=6 Clustering Advantages:**
- **Better Kitchen Organization**: Separate prep stations for modern vs traditional items
- **Inventory Management**: Distinct sourcing strategies for each cluster
- **Pricing Strategy**: Clear cost basis for each menu category
- **Staff Training**: Specialized skills for different preparation styles

### Market Positioning

**Traditional Swiss Excellence**: Clusters 2,3,4,6 represent authentic Swiss dining
**Health-Conscious Options**: Cluster 1 addresses modern dietary preferences  
**Contemporary Appeal**: Cluster 5 attracts younger, international clientele

## 📈 Visualization Features

### Side-by-Side Comparison
- **Left Panel**: K=4 clustering with 4 distinct categorical colors
- **Right Panel**: K=6 clustering with 6 distinct categorical colors  
- **Cluster Centroids**: Red X markers show cluster centers in PCA space
- **Clear Separation**: Different colors make cluster boundaries obvious

### Technical Quality
- **Standardized Features**: Ensures equal weight for all COGS attributes
- **PCA Projection**: Maintains relative relationships while enabling 2D visualization
- **Categorical Colors**: Optimal visual distinction between clusters
- **Statistical Validation**: Silhouette scores confirm clustering quality

## 🎯 Recommendations

1. **Adopt K=6 Clustering** for operational planning (better silhouette score: 0.346 vs 0.286)
2. **Separate Kitchen Stations** based on cluster characteristics
3. **Targeted Marketing** for each cluster's customer segment
4. **Cost Control** focus on high-COGS clusters (2,4,6)
5. **Menu Engineering** to balance low and high-cost items

---
*Files Generated: zeughauskeller_clustering_analysis.png (side-by-side plots), zeughauskeller_clustering_results.csv (detailed data with cluster assignments)*