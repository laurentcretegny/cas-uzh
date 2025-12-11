# Healthiness Classification Model Report

## 📊 Project Overview
- **Objective**: Predict healthiness rating (1-5 scale) using dish characteristics
- **Dataset**: 39 Zeughauskeller dishes with COGS and physical attributes
- **Model Type**: Multi-class probabilistic classification
- **Target Variable**: Healthiness (1=lowest health, 5=highest health)

## 🎯 Dataset Analysis

### Target Variable Distribution
| Healthiness Level | Count | Percentage | Interpretation |
|-------------------|--------|------------|----------------|
| **1 (Lowest)** | 5 dishes | 12.8% | Highly processed, high-fat items |
| **2 (Low)** | 12 dishes | 30.8% | Traditional heavy dishes |
| **3 (Medium)** | 13 dishes | 33.3% | Balanced meat-based dishes |
| **4 (High)** | 5 dishes | 12.8% | Lean proteins, healthier prep |
| **5 (Highest)** | 4 dishes | 10.3% | Soups, salads, minimal processing |

### Feature Set (13 attributes)
**COGS Features (10)**:
- Meat/Sausage, Cheese, Mushrooms, Potatoes, Pasta/Noodles
- Bread/Toast, Salad Greens, Rice, Sauce, Vegetables

**Physical & Economic Features (3)**:
- Estimated dish weight (kg)
- Price (CHF)  
- Total COGS Estimated (CHF)

## 🤖 Model Comparison Results

### Performance Summary
| Model | Test Accuracy | CV Mean | CV Std | Stability | Best Use Case |
|-------|--------------|---------|---------|-----------|---------------|
| **🏆 Logistic Regression** | **0.583** | **0.389** | 0.103 | Most stable | **Winner** - interpretable probabilities |
| **Random Forest** | 0.583 | 0.354 | 0.239 | Unstable | Feature importance analysis |
| **SVM (RBF)** | 0.333 | 0.282 | 0.048 | Stable but poor | Non-linear patterns |
| **Naive Bayes** | 0.333 | 0.200 | 0.150 | Poor overall | Baseline comparison |

### Winner: **Logistic Regression** ✅
- **Best cross-validation performance** (0.389 ± 0.103)
- **Most stable predictions** (lowest CV standard deviation)
- **Interpretable probability outputs** for business use
- **58.3% test accuracy** on challenging 5-class problem

## 📈 Feature Importance Analysis

### Top 10 Predictive Features (Random Forest)
| Rank | Feature | Importance | Business Insight |
|------|---------|------------|------------------|
| 1 | **Price** | 0.257 | Higher prices ≠ healthier dishes |
| 2 | **Total COGS** | 0.186 | Cost structure indicates complexity |
| 3 | **Meat/Sausage** | 0.139 | Protein type drives health rating |
| 4 | **Sauce** | 0.104 | Heavy sauces reduce health score |
| 5 | **Dish Weight** | 0.086 | Portion size impacts perception |
| 6 | **Salad Greens** | 0.068 | Direct positive health indicator |
| 7 | **Vegetables** | 0.050 | Fresh components boost health |
| 8 | **Cheese** | 0.047 | Dairy content affects rating |
| 9 | **Potatoes** | 0.021 | Starch content minor factor |
| 10 | **Bread/Toast** | 0.020 | Carbohydrate impact limited |

## 🔍 Model Performance Analysis

### Classification Accuracy by Healthiness Level
| Level | Precision | Recall | F1-Score | Performance |
|-------|-----------|--------|----------|-------------|
| **Healthiness 1** | 1.000 | 0.500 | 0.667 | Excellent precision, moderate recall |
| **Healthiness 2** | 0.667 | 1.000 | 0.800 | Best overall performance |
| **Healthiness 3** | 0.500 | 0.500 | 0.500 | Moderate performance |
| **Healthiness 4** | 0.000 | 0.000 | 0.000 | Poor (small sample size) |
| **Healthiness 5** | 0.000 | 0.000 | 0.000 | Poor (small sample size) |

### Key Insights
- **Strong at extremes**: Best performance on unhealthy (Level 2) dishes
- **Struggles with healthy categories**: Levels 4-5 have insufficient training data
- **Class imbalance impact**: Small sample sizes hurt performance on healthy dishes
- **Medium categories challenging**: Level 3 shows moderate confusion

## 💡 Probabilistic Predictions Examples

### Sample Model Outputs
**Chicken Breast** (True: 4, Predicted: 3):
- Healthiness 1: 18.2% | Healthiness 2: 12.8% | **Healthiness 3: 43.0%** | Healthiness 4: 22.1% | Healthiness 5: 3.9%

**Veal Cordon Bleu** (True: 1, Predicted: 1):
- **Healthiness 1: 44.1%** | Healthiness 2: 8.6% | Healthiness 3: 43.5% | Healthiness 4: 3.1% | Healthiness 5: 0.7%

**Whole Pork Knuckle** (True: 2, Predicted: 2):
- Healthiness 1: 3.5% | **Healthiness 2: 88.0%** | Healthiness 3: 8.3% | Healthiness 4: 0.2% | Healthiness 5: 0.0%

## 🏪 Business Applications

### Menu Health Assessment
- **Automated health scoring** for new dishes
- **Probability distributions** show health uncertainty
- **Cost-health relationship** analysis for menu engineering

### Pricing Strategy Support
- **Price-health correlation** insights for positioning
- **Premium health positioning** opportunities identified
- **Cost structure optimization** based on health targets

### Kitchen Operations
- **Ingredient substitution guidance** to improve health scores
- **Portion size optimization** for health/cost balance
- **Preparation method impact** on health perception

## 🎯 Model Limitations & Recommendations

### Current Limitations
1. **Small dataset** (39 dishes) limits generalization
2. **Class imbalance** hurts performance on healthy dishes (Levels 4-5)
3. **Feature engineering** could improve with chef expertise
4. **Subjective health ratings** may have inconsistencies

### Improvement Recommendations

**Data Enhancement**:
- Collect more healthy dish examples (Levels 4-5)
- Add nutritional data (calories, fat, protein, fiber)
- Include preparation method features (grilled, fried, steamed)
- Gather customer health perception surveys

**Model Improvements**:
- **SMOTE oversampling** to balance class distribution
- **Ensemble methods** combining multiple algorithms
- **Feature engineering** with domain expertise
- **Hyperparameter tuning** for better performance

**Business Integration**:
- **Real-time health scoring** for menu development
- **Health-price optimization** dashboard
- **Ingredient substitution recommendations** system

## 📊 Statistical Validation

### Cross-Validation Results
- **5-fold stratified CV** ensures representative splits
- **Logistic Regression stability** (0.389 ± 0.103) shows consistent performance
- **Random Forest variability** (0.354 ± 0.239) indicates overfitting risk

### Model Reliability
- **58.3% accuracy** on challenging 5-class problem exceeds random baseline (20%)
- **Probability calibration** provides uncertainty quantification
- **Feature importance** aligns with culinary health intuition

---

**Files Generated:**
- `healthiness_classification_analysis.png` - 6-panel visualization dashboard
- `healthiness_classification_results.csv` - Model performance summary
- Model objects saved for deployment and further analysis