# PCA Analysis Report: Zeughauskeller COGS Dimensionality Reduction

## 📊 Analysis Overview
- **Dataset**: Zeughauskeller restaurant dishes COGS analysis
- **Method**: Principal Component Analysis (PCA)
- **Features**: 10 COGS (Cost of Goods Sold) attributes
- **Dishes Analyzed**: 39 menu items
- **Dimensionality**: Reduced from 10D to 2D

## 🎯 PCA Results

### Explained Variance
- **PC1**: 23.0% of total variance
- **PC2**: 15.7% of total variance  
- **Combined**: 38.6% of total variance captured in 2D

*Note: 38.6% variance retention indicates moderate complexity in cost structure - dishes have diverse cost patterns that require multiple dimensions to fully capture.*

## 🔍 Component Interpretation

### PC1 (23.0% variance) - "Premium Protein & Sauce Axis"
**Strong Positive Loadings:**
- Meat/Sausage (0.597) - Primary driver
- Sauce (0.578) - Secondary driver
- Rice (0.245)

**Strong Negative Loadings:**  
- Salad Greens (-0.338)
- Cheese (-0.218)
- Pasta/Noodles (-0.206)

**Interpretation**: PC1 separates meat-heavy dishes with rich sauces (right side) from lighter, vegetable-based dishes (left side).

### PC2 (15.7% variance) - "Simple vs Complex Preparation"
**Strong Positive Loadings:**
- Vegetables (0.495)
- Bread/Toast (0.341)

**Strong Negative Loadings:**
- Pasta/Noodles (-0.455)
- Potatoes (-0.459) 
- Cheese (-0.425)

**Interpretation**: PC2 separates dishes with fresh vegetables and bread (top) from starch-heavy dishes with cheese (bottom).

## 🍽️ Extreme Dishes Analysis

### PC1 Extremes (Protein Spectrum)
- **Highest**: "Zeughauskeller Kanonenputzer" - Premium meat dish with complex sauce
- **Lowest**: "Butterhead lettuce Mimosa" - Simple salad with minimal ingredients

### PC2 Extremes (Preparation Complexity)
- **Highest**: "Incredible Burger" - Complex vegetable-based preparation  
- **Lowest**: "Aelplermagronen" - Traditional Swiss dish with pasta, cheese, potatoes

## 📈 Business Insights

### Cost Structure Patterns
1. **High-End Meat Dishes** (Upper right): Premium proteins with elaborate sauces
2. **Simple Salads** (Left side): Low-cost, healthy options
3. **Traditional Swiss Fare** (Lower area): Carb-heavy comfort foods
4. **Modern Preparations** (Upper area): Contemporary dishes with fresh ingredients

### Strategic Implications
- **Menu Diversity**: 38.6% variance capture shows good cost structure diversity
- **Cost Control**: Clear separation between high-cost protein dishes and economical salads
- **Market Positioning**: Balance of premium offerings and accessible options
- **Operational Efficiency**: Clustered dishes suggest shared ingredient sourcing opportunities

## 🎨 Visualization Features
- **Scatter Plot**: Each dish positioned by its cost structure similarity
- **Non-Overlapping Labels**: Automated label positioning prevents text overlap
- **Color Coding**: Distinct colors help identify individual dishes
- **Component Loadings**: Separate plot shows feature importance for each PC

## 📊 Technical Details
- **Standardization**: Features standardized before PCA (essential for cost data)
- **Method**: Singular Value Decomposition via scikit-learn
- **Label Adjustment**: adjustText library for optimal label positioning
- **Reproducibility**: Random seed set for consistent results

---
*Files Generated: zeughauskeller_pca_analysis.png (main scatter plot), zeughauskeller_pca_loadings.png (feature importance)*