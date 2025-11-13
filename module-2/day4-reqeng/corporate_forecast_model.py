#!/usr/bin/env python3
"""
Corporate Financial Forecasting Model
Converted from Excel formulas to pure Python implementation

This program recreates the financial forecasting calculations 
from the Excel sheet "Forecast" in Corporate Modelling_230421.xlsx
"""

import math
import json
from typing import Dict, List, Union, Optional
from dataclasses import dataclass
from collections import defaultdict


@dataclass
class FinancialData:
    """Container for financial data values"""
    # Base year (2020) values from Excel
    opening_cash: float = 4116
    property_plant_equipment: float = 10558
    goodwill_base: float = 18942
    intangible_assets_base: float = 15999
    non_current_debt: float = 29412
    shareholder_equity: float = 17655
    revenue_2020: float = 50724
    cost_of_sales_2020: float = 28684
    
    # Years for forecasting
    years: List[int] = None
    
    def __post_init__(self):
        if self.years is None:
            self.years = [2020, 2025, 2030, 2035, 2040, 2045, 2050]


class CorporateFinancialModel:
    """
    Pure Python implementation of Excel financial forecasting model
    """
    
    def __init__(self, data: FinancialData):
        self.data = data
        self.calculations = {}
        self.iam_data = self._initialize_iam_data()
        
    def _initialize_iam_data(self):
        """
        Initialize IAM (Integrated Assessment Model) data
        These would come from the IAM sheet in the original Excel
        """
        # Placeholder values - in real implementation, load from IAM sheet
        return {
            'revenue_projections': {
                2020: 50724,
                2025: 55000,  # Example values
                2030: 60000,
                2035: 65000,
                2040: 70000,
                2045: 75000,
                2050: 80000
            }
        }
    
    def calculate_compound_growth_rate(self, start_value: float, end_value: float, years: int) -> float:
        """
        Calculate compound annual growth rate (CAGR)
        Formula: (End Value / Start Value)^(1/Years) - 1
        
        Equivalent to Excel: =(EndValue/StartValue)^(1/Years)-1
        """
        if start_value <= 0 or end_value <= 0 or years <= 0:
            return 0.0
        return (end_value / start_value) ** (1 / years) - 1
    
    def calculate_revenue_growth_rates(self) -> Dict[int, float]:
        """
        Calculate year-over-year revenue growth rates
        Based on Excel formulas: =(IAM!F15/IAM!E15)^(1/5)-1
        """
        growth_rates = {}
        iam_revenue = self.iam_data['revenue_projections']
        
        for i, year in enumerate(self.data.years[1:], 1):  # Skip base year
            prev_year = self.data.years[i-1]
            if prev_year in iam_revenue and year in iam_revenue:
                growth_rates[year] = self.calculate_compound_growth_rate(
                    iam_revenue[prev_year], 
                    iam_revenue[year], 
                    5  # 5-year periods
                )
        
        return growth_rates
    
    def calculate_goodwill_intangible(self) -> float:
        """
        Calculate Goodwill and intangible assets
        Excel formula: =18942+15999
        """
        return self.data.goodwill_base + self.data.intangible_assets_base
    
    def calculate_debt_to_equity_ratio(self) -> float:
        """
        Calculate fixed debt to equity ratio
        Excel formula: =$D10/$D18
        """
        if self.data.shareholder_equity == 0:
            return 0.0
        return self.data.non_current_debt / self.data.shareholder_equity
    
    def calculate_cost_of_sales_ratio(self) -> float:
        """
        Calculate cost of sales as ratio of revenue
        Excel formula: =28684/D15
        """
        if self.data.revenue_2020 == 0:
            return 0.0
        return self.data.cost_of_sales_2020 / self.data.revenue_2020
    
    def forecast_revenue(self, year: int, growth_rate: float, base_revenue: float) -> float:
        """
        Forecast revenue for a given year using growth rate
        Excel equivalent: =PreviousRevenue*(1+GrowthRate)
        """
        return base_revenue * (1 + growth_rate)
    
    def forecast_cost_of_sales(self, revenue: float) -> float:
        """
        Forecast cost of sales based on revenue
        Excel formula: =-$D16*D$32
        """
        cost_ratio = self.calculate_cost_of_sales_ratio()
        return -cost_ratio * revenue  # Negative because it's a cost
    
    def calculate_assets_not_elsewhere_classified(self, total_assets: float, 
                                                property_plant: float, 
                                                goodwill_intangible: float, 
                                                other_sum: float) -> float:
        """
        Calculate assets not elsewhere classified
        Excel formula: =D12-SUM(D50,D8:D9)
        """
        return total_assets - (other_sum + property_plant + goodwill_intangible)
    
    def sum_range(self, values: List[float]) -> float:
        """
        Calculate sum of a range of values
        Excel equivalent: =SUM(range)
        """
        return sum(values)
    
    def calculate_total_assets(self) -> float:
        """
        Calculate total assets (placeholder - would sum all asset components)
        """
        return (self.data.opening_cash + 
                self.data.property_plant_equipment + 
                self.calculate_goodwill_intangible())
    
    def run_full_forecast(self) -> Dict:
        """
        Run the complete financial forecast for all years
        """
        results = {
            'years': self.data.years,
            'revenue_growth_rates': {},
            'revenue_forecast': {},
            'cost_of_sales_forecast': {},
            'key_ratios': {},
            'balance_sheet': {}
        }
        
        # Calculate key ratios (constant across years)
        results['key_ratios'] = {
            'goodwill_and_intangible': self.calculate_goodwill_intangible(),
            'debt_to_equity_ratio': self.calculate_debt_to_equity_ratio(),
            'cost_of_sales_ratio': self.calculate_cost_of_sales_ratio()
        }
        
        # Calculate growth rates
        growth_rates = self.calculate_revenue_growth_rates()
        results['revenue_growth_rates'] = growth_rates
        
        # Forecast for each year
        prev_revenue = self.data.revenue_2020
        for year in self.data.years:
            if year == 2020:  # Base year
                results['revenue_forecast'][year] = self.data.revenue_2020
                results['cost_of_sales_forecast'][year] = self.data.cost_of_sales_2020
            else:
                # Apply growth rate if available
                if year in growth_rates:
                    revenue = self.forecast_revenue(year, growth_rates[year], prev_revenue)
                else:
                    # Use previous year's revenue if no growth rate
                    revenue = prev_revenue
                
                results['revenue_forecast'][year] = revenue
                results['cost_of_sales_forecast'][year] = self.forecast_cost_of_sales(revenue)
                prev_revenue = revenue
        
        # Balance sheet calculations
        debt_ratio = results['key_ratios']['debt_to_equity_ratio']
        for year in self.data.years:
            results['balance_sheet'][year] = {
                'non_current_debt_ratio': debt_ratio,  # Constant ratio across years
                'goodwill_intangible': results['key_ratios']['goodwill_and_intangible']
            }
        
        return results
    
    def print_forecast_summary(self, results: Dict):
        """Print a summary of the forecast results"""
        print("=" * 80)
        print("CORPORATE FINANCIAL FORECAST SUMMARY")
        print("=" * 80)
        
        print("\nKEY RATIOS:")
        print(f"  Goodwill and Intangible Assets: ${results['key_ratios']['goodwill_and_intangible']:,.0f}")
        print(f"  Debt-to-Equity Ratio: {results['key_ratios']['debt_to_equity_ratio']:.3f}")
        print(f"  Cost of Sales Ratio: {results['key_ratios']['cost_of_sales_ratio']:.1%}")
        
        print("\nREVENUE GROWTH RATES:")
        for year, rate in results['revenue_growth_rates'].items():
            print(f"  {year}: {rate:.2%}")
        
        print(f"\nFORECAST BY YEAR:")
        print(f"{'Year':<6} {'Revenue':<12} {'Cost of Sales':<15} {'Gross Profit':<15} {'Margin':<8}")
        print("-" * 60)
        
        for year in results['years']:
            revenue = results['revenue_forecast'][year]
            cost_of_sales = results['cost_of_sales_forecast'][year]
            gross_profit = revenue + cost_of_sales  # Cost of sales is negative
            margin = (gross_profit / revenue) * 100 if revenue != 0 else 0
            
            print(f"{year:<6} ${revenue:<11,.0f} ${cost_of_sales:<14,.0f} ${gross_profit:<14,.0f} {margin:<7.1f}%")


def main():
    """Main function to run the financial forecasting model"""
    print("Corporate Financial Forecasting Model")
    print("Converted from Excel to Pure Python")
    print("=" * 50)
    
    # Initialize financial data
    financial_data = FinancialData()
    
    # Create and run the model
    model = CorporateFinancialModel(financial_data)
    results = model.run_full_forecast()
    
    # Display results
    model.print_forecast_summary(results)
    
    # Save results to JSON for further analysis
    with open('forecast_results.json', 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\nDetailed results saved to 'forecast_results.json'")
    
    print("\n" + "=" * 50)
    print("EXCEL FORMULA IMPLEMENTATIONS:")
    print("=" * 50)
    
    # Demonstrate individual formula calculations
    print(f"\n1. Goodwill + Intangible Assets:")
    print(f"   Excel: =18942+15999")
    print(f"   Python: {model.calculate_goodwill_intangible():,.0f}")
    
    print(f"\n2. Debt-to-Equity Ratio:")
    print(f"   Excel: =$D10/$D18")
    print(f"   Python: {model.calculate_debt_to_equity_ratio():.6f}")
    
    print(f"\n3. Cost of Sales Ratio:")
    print(f"   Excel: =28684/D15")
    print(f"   Python: {model.calculate_cost_of_sales_ratio():.6f}")
    
    print(f"\n4. Compound Growth Rate (Example: 2025):")
    growth_5yr = model.calculate_compound_growth_rate(50724, 55000, 5)
    print(f"   Excel: =(55000/50724)^(1/5)-1")
    print(f"   Python: {growth_5yr:.6f} ({growth_5yr:.2%})")


if __name__ == "__main__":
    main()