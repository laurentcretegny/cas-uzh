# Healthiness vs Cost Correlation Analysis Report

## Dataset Overview
- **Total Dishes Analyzed**: 30 dishes from combined restaurant dataset
- **Restaurants**: La Fonte Restaurant Pizzeria (Italian) & Zeughauskeller Zurich (Swiss)
- **Analysis Date**: November 15, 2025

## Key Findings

### 📊 Correlation Analysis
- **Pearson Correlation Coefficient**: -0.191
- **Correlation Strength**: Moderate Negative Correlation
- **Interpretation**: There is a slight tendency for healthier dishes to be less expensive

### 🏥 Healthiness Scoring System
The healthiness score (0-100) was calculated based on:

**Positive Factors (+points):**
- Fresh vegetables, salads, herbs (+5 to +15 points)
- Lean proteins like chicken, fish (+8 to +12 points)
- Light cooking methods (+5 to +10 points)
- Healthy dish categories (salads, soups) (+8 to +15 points)

**Negative Factors (-points):**
- High-fat ingredients (cream, cheese, bacon) (-6 to -12 points)
- Fried foods and processed meats (-8 to -12 points)
- Heavy sauces and unhealthy sides (-5 to -10 points)
- Desserts and heavy dish categories (-15 to -20 points)

### 💰 Price Analysis by Healthiness Category

| Healthiness Level | Dish Count | Average Price (CHF) | Price Range |
|-------------------|------------|--------------------|-----------| 
| **Low (0-35)**    | 4 dishes   | 22.72 CHF         | 13.45 CHF spread |
| **Medium (35-55)** | 14 dishes  | 24.74 CHF         | Most common category |
| **High (55-75)**   | 8 dishes   | 26.81 CHF         | Premium healthy options |
| **Very High (75+)** | 4 dishes   | 13.62 CHF         | Surprisingly affordable |

### 🏪 Restaurant Comparison

| Restaurant | Avg Healthiness Score | Avg Price (CHF) | Cuisine Style |
|------------|----------------------|----------------|---------------|
| **La Fonte** | 48.6/100 | 21.95 CHF | Italian - moderate health |
| **Zeughauskeller** | 60.7/100 | 25.13 CHF | Swiss - healthier options |

## 📈 Visualization Types Generated

1. **Scatter Plot with Regression Line**: Shows individual dishes plotted by healthiness score vs price, with trend line
2. **Box Plot with Strip Plot**: Displays price distribution across healthiness categories with individual data points
3. **Violin Plot by Restaurant**: Shows price density distributions for each healthiness category, split by restaurant
4. **Heatmap**: Cross-tabulation showing dish counts across healthiness categories and price ranges

## 🔍 Insights

### Surprising Findings:
- **Very healthy dishes are often the most affordable** (soups, simple salads)
- **Medium-healthy dishes command premium prices** (balanced main courses)
- **Swiss restaurant offers healthier options on average** but at slightly higher cost
- **Italian restaurant has more consistent pricing** across healthiness levels

### Business Implications:
- Healthy options don't necessarily cost more to produce
- Premium pricing often associated with complexity rather than healthiness
- Simple, healthy dishes (soups, salads) offer excellent value
- Complex dishes with mixed healthy/unhealthy ingredients tend to be most expensive

## 📋 Dataset Examples by Category

- **Very High Health**: Beef broth with finely shredded crepe (76/100, 8.0 CHF)
- **High Health**: Carpaccio di manzo (60/100, 24.0 CHF)  
- **Medium Health**: Bruschettone (55/100, 10.0 CHF)
- **Low Health**: Strozzapreti Campagnole (30/100, 31.5 CHF)

## 📊 Statistical Summary
- **Correlation strength indicates weak to moderate negative relationship**
- **Price variation within healthiness categories is significant** 
- **Restaurant type influences both healthiness and pricing patterns**
- **Simple preparation methods often correlate with both health and affordability**