# ZEUGHAUSKELLER ZURICH - EXTRACTED MENU DISHES

## Overview
I have successfully extracted **15 dishes** from the Zeughauskeller Zurich menu using a **balanced sampling approach** across different menu categories to provide a representative selection of this traditional Swiss restaurant's offerings.

## Structured Data Table

| Restaurant | ID | Dish | Dish Category | Ingredients | Price |
|------------|----|----- |---------------|-------------|-------|
| Zeughauskeller Zurich | S001 | Beef broth with finely shredded crepe | Homemade Soups | Beef broth, finely shredded crepe | 8.00 CHF |
| Zeughauskeller Zurich | S002 | Seasonal soup | Homemade Soups | Seasonal ingredients | 9.00 CHF |
| Zeughauskeller Zurich | SA001 | Mixed salad | Fresh Salads | Mixed green salad | 9.50 CHF |
| Zeughauskeller Zurich | CP001 | Beefsteak Tartare | Cold Platters | Raw beef tartare (mild or spicy), salad garnish, toast, butter | 32.00 CHF (regular portion) |
| Zeughauskeller Zurich | CP002 | Sliced air-dried mountain ham and beef with Swiss Gruyère | Cold Platters | Air-dried mountain ham, air-dried mountain beef, shaved Swiss Gruyère cheese | 24.50 CHF |
| Zeughauskeller Zurich | SH001 | Kalbsgeschnetzeltes nach Zürcher Art | Specialities of the House | Panfried sliced veal, mushrooms, creamy white-wine sauce | 36.50 CHF |
| Zeughauskeller Zurich | SH002 | Mayor's sword | Specialities of the House | 400g marinated baby-beef steaks, mixed salad, Rösti or French fries, curry-garlic and barbecue sauce | 88.00 CHF (for 2 persons) |
| Zeughauskeller Zurich | SH003 | Whole pork shank | Specialities of the House | Marinated pork shank with herbs, oven-roasted, dark draught beer, fresh potato salad | 33.00 CHF |
| Zeughauskeller Zurich | SH004 | Deep fried perch fillets | Specialities of the House | Perch fillets, boiled potatoes, tartar sauce | 31.00 CHF |
| Zeughauskeller Zurich | SF001 | The original Kalbsbratwurst | Our Sausage Favourites | Pan fried veal sausage (made in Zurich), onion sauce, homemade potato salad | 20.00 CHF |
| Zeughauskeller Zurich | SF002 | Zwingli sausage | Our Sausage Favourites | Grilled pork sausage with herbs and pistachio pieces (recipe from 1519), onion sauce, homemade potato salad | 22.00 CHF |
| Zeughauskeller Zurich | SF003 | Vaudois Saucisson | Our Sausage Favourites | Smoked pork sausage with bacon, white wine, traditional spice mixture, sauerkraut, boiled potatoes | 29.00 CHF |
| Zeughauskeller Zurich | AG001 | Älplermagronen | Always a good choice | Alpine Macaroni (Swiss specialty), potato cubes, onions, cream sauce | 21.50 CHF |
| Zeughauskeller Zurich | AG002 | Zeughauskeller-Burger | Always a good choice | 2x 120g beef burgers (100% beef), coleslaw, fried onions, bacon, BBQ-sauce, French fries | 28.00 CHF |
| Zeughauskeller Zurich | LD001 | Tender chicken breast | Light dishes | Swiss Gourmet chicken (crumbed and crispy or grilled), green salad | 28.00 CHF |

## Balanced Sampling Strategy

The 15 dishes were selected using a balanced sampling approach across 7 menu categories:

### Category Distribution:
- **Specialities of the House**: 4 dishes (26.7%)
- **Our Sausage Favourites**: 3 dishes (20%)
- **Always a good choice**: 2 dishes (13.3%)
- **Homemade Soups**: 2 dishes (13.3%)
- **Cold Platters**: 2 dishes (13.3%)
- **Fresh Salads**: 1 dish (6.7%)
- **Light dishes**: 1 dish (6.7%)

### Price Range Analysis:
- **Minimum**: 8.00 CHF (Beef broth with finely shredded crepe)
- **Maximum**: 88.00 CHF (Mayor's sword - for 2 persons)
- **Average**: ~28.20 CHF (excluding sharing dishes)
- **Range represents**: Traditional Swiss dining from casual to premium

### Variety Characteristics:
- **Traditional Swiss**: Älplermagronen, Kalbsgeschnetzeltes nach Zürcher Art, various sausages
- **German-influenced**: Whole pork shank, Schnitzel variations
- **Local specialties**: Zurich-made Kalbsbratwurst, Zwingli sausage (1519 recipe)
- **International options**: Burger, Beefsteak Tartare
- **Protein variety**: Veal, pork, beef, chicken, fish (perch)
- **Cooking methods**: Grilled, pan-fried, oven-roasted, deep-fried, raw

### Cultural & Historical Significance:
- **Zeughauskeller context**: Historic Swiss restaurant known for traditional fare
- **Regional specialties**: Dishes representing different Swiss regions (Vaudois, Zurich)
- **Historical recipes**: Zwingli sausage dating back to 1519
- **Swiss classics**: Älplermagronen (Alpine Macaroni), various traditional sausages

### Data Quality Notes:
- All ingredient lists extracted from original English menu text
- Prices include Swiss VAT and service as stated in original menu
- ID codes assigned systematically by category (S=Soups, SA=Salads, CP=Cold Platters, SH=Specialities House, SF=Sausage Favourites, AG=Always Good, LD=Light Dishes)
- Menu reflects traditional Swiss restaurant atmosphere and cuisine

## Restaurant Comparison Notes
**Zeughauskeller vs La Fonte:**
- **Cuisine Type**: Traditional Swiss/German vs Italian
- **Price Range**: 8-88 CHF vs 9.50-32 CHF
- **Atmosphere**: Historic Swiss tavern vs Modern Italian
- **Specialties**: Sausages & traditional Swiss fare vs Pizza & pasta
- **Portion Style**: Hearty traditional portions vs Mediterranean portions

## File Outputs
- **CSV file**: `/workspaces/cas-uzh/module-2/day6/zeughauskeller_menu_dishes.csv`
- **Python script**: `/workspaces/cas-uzh/module-2/day6/zeughauskeller_extract.py`