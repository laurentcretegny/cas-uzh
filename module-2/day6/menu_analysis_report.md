# LA FONTE RESTAURANT PIZZERIA - EXTRACTED MENU DISHES

## Overview
I have successfully extracted **15 dishes** from the La Fonte Restaurant Pizzeria menu uploaded in the day6 folder. The extraction used a **balanced sampling approach** across different menu categories to provide a representative selection of the restaurant's offerings.

## Structured Data Table

| Restaurant | ID | Dish | Dish Category | Ingredients | Price |
|------------|----|----- |---------------|-------------|-------|
| La Fonte Restaurant Pizzeria | A001 | Bruschettone | Antipasti | Geröstete Brotscheibe, Tomatenwürfel, Knoblauch | 10.00 CHF |
| La Fonte Restaurant Pizzeria | A002 | Carpaccio di manzo | Antipasti | Rindscarpaccio, Rucola, Grana | 24.00 CHF |
| La Fonte Restaurant Pizzeria | S001 | Insalata con pollo | Insalate | Gemischter Blattsalat, Cherry, Pouletstreifen | 14.00 CHF (Klein) / 18.00 CHF (Groß) |
| La Fonte Restaurant Pizzeria | S002 | Caprese | Insalate | Tomaten, Büffelmozzarella | 12.00 CHF (Klein) / 16.00 CHF (Groß) |
| La Fonte Restaurant Pizzeria | P001 | Spaghetti Bolognese | Primi Piatti | Rindsbolognesesauce | 21.90 CHF |
| La Fonte Restaurant Pizzeria | P002 | Strozzapreti Campagnole | Primi Piatti | Speck, schwarzer Trüffel, Rahm | 31.50 CHF |
| La Fonte Restaurant Pizzeria | P003 | Gnocchi Al zafferano | Primi Piatti | Safran, Cherry, Burrata | 29.70 CHF |
| La Fonte Restaurant Pizzeria | PC001 | Pizza Margherita | Pizze Classiche | Tomaten, Mozzarella, Oregano, Basilikum | 16.90 CHF |
| La Fonte Restaurant Pizzeria | PC002 | Pizza Prosciutto e funghi | Pizze Classiche | Tomaten, Mozzarella, Hinterschinken, frische Champignons, Oregano, Basilikum | 19.90 CHF |
| La Fonte Restaurant Pizzeria | PC003 | Pizza 4 Formaggi | Pizze Classiche | Tomaten, Mozzarella, Gorgonzola, Mascarpone, Grana, Oregano, Basilikum | 21.90 CHF |
| La Fonte Restaurant Pizzeria | PS001 | Pizza Anna | Pizze Speciali | Tomaten, Mozzarella, Rohschinken, Cherry, Rucola, Grana, Burrata, Oregano, Basilikum | 29.50 CHF |
| La Fonte Restaurant Pizzeria | PS002 | Pizza Molisana | Pizze Speciali | Mozzarella, Salsiccia scharf, Provola, schwarzer Trüffel, Oregano, Basilikum | 32.00 CHF |
| La Fonte Restaurant Pizzeria | PS003 | Pizza Biancaneve | Pizze Speciali | Mozzarella, Salsiccia scharf, Kartoffeln, Peperoni, Oregano, Basilikum | 24.90 CHF |
| La Fonte Restaurant Pizzeria | C001 | Calzone della Casa | Il Nostro Calzone | Tomaten, Mozzarella, Hinterschinken, frische Champignons, Knoblauch, Ei, Pesto, Grana | 27.50 CHF |
| La Fonte Restaurant Pizzeria | D001 | Tiramisù | I nostri Dessert | Hausgemachtes Tiramisu | 9.50 CHF |

## Balanced Sampling Strategy

The 15 dishes were selected using a balanced sampling approach across 6 menu categories:

### Category Distribution:
- **Primi Piatti**: 3 dishes (20%)
- **Pizze Speciali**: 3 dishes (20%) 
- **Pizze Classiche**: 3 dishes (20%)
- **Insalate**: 2 dishes (13.3%)
- **Antipasti**: 2 dishes (13.3%)
- **Il Nostro Calzone**: 1 dish (6.7%)
- **I nostri Dessert**: 1 dish (6.7%)

### Price Range Analysis:
- **Minimum**: 9.50 CHF (Tiramisù)
- **Maximum**: 32.00 CHF (Pizza Molisana)
- **Average**: ~21.80 CHF
- **Range represents**: Budget-friendly to premium options

### Variety Characteristics:
- **Vegetarian options**: Pizza Margherita, Pizza 4 Formaggi, Caprese, etc.
- **Meat dishes**: Carpaccio di manzo, Pizza Anna (with Rohschinken), etc.
- **Premium ingredients**: Black truffle (Strozzapreti Campagnole, Pizza Molisana), Burrata, Saffron
- **Traditional vs. Specialty**: Mix of classic Italian dishes and restaurant specialties

### Data Quality Notes:
- All ingredient lists extracted from original German menu text
- Prices include Swiss VAT (7.7% MwSt) as stated in original menu
- ID codes assigned systematically by category (A=Antipasti, S=Insalate, P=Primi, PC=Pizze Classiche, PS=Pizze Speciali, C=Calzone, D=Dessert)

## File Outputs
- **CSV file**: `/workspaces/cas-uzh/module-2/day6/la_fonte_menu_dishes.csv`
- **Python script**: `/workspaces/cas-uzh/module-2/day6/menu_dishes_extract.py`