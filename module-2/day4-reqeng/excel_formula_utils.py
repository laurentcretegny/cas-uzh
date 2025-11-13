#!/usr/bin/env python3
"""
Excel Formula Utilities - Specific implementations of Excel functions
This module provides pure Python equivalents of common Excel formulas
"""

import math
from typing import List, Union, Optional


class ExcelFormulas:
    """
    A collection of Python functions that replicate Excel formula behavior
    """
    
    @staticmethod
    def sum_range(values: List[Union[int, float]]) -> float:
        """
        Equivalent to Excel SUM() function
        Usage: =SUM(A1:A10) becomes sum_range([A1, A2, ..., A10])
        """
        return sum(v for v in values if isinstance(v, (int, float)))
    
    @staticmethod
    def compound_growth_rate(start_value: float, end_value: float, periods: int) -> float:
        """
        Equivalent to Excel: =(end_value/start_value)^(1/periods)-1
        Calculates compound annual growth rate
        """
        if start_value <= 0 or periods <= 0:
            return 0.0
        return (end_value / start_value) ** (1 / periods) - 1
    
    @staticmethod
    def power(base: float, exponent: float) -> float:
        """
        Equivalent to Excel POWER() or ^ operator
        Usage: =A1^2 becomes power(A1, 2)
        """
        return base ** exponent
    
    @staticmethod
    def percentage_change(old_value: float, new_value: float) -> float:
        """
        Calculate percentage change between two values
        Equivalent to: =(new_value - old_value) / old_value
        """
        if old_value == 0:
            return 0.0
        return (new_value - old_value) / old_value
    
    @staticmethod
    def ratio(numerator: float, denominator: float) -> float:
        """
        Simple ratio calculation with zero-division protection
        Equivalent to Excel: =A1/B1
        """
        if denominator == 0:
            return 0.0
        return numerator / denominator
    
    @staticmethod
    def multiply_range(multiplier: float, values: List[float]) -> List[float]:
        """
        Multiply a value by a range of values
        Equivalent to Excel: =$A$1*B1:B10
        """
        return [multiplier * value for value in values]
    
    @staticmethod
    def if_condition(condition: bool, true_value, false_value):
        """
        Equivalent to Excel IF() function
        Usage: =IF(A1>0, "Positive", "Not Positive")
        """
        return true_value if condition else false_value
    
    @staticmethod
    def vlookup_simple(lookup_value, table_dict: dict, default_value=None):
        """
        Simplified version of Excel VLOOKUP
        Usage: vlookup_simple("key", {"key": "value"}, "default")
        """
        return table_dict.get(lookup_value, default_value)


class FinancialFormulas:
    """
    Specific financial formulas commonly used in corporate modeling
    """
    
    @staticmethod
    def present_value(future_value: float, rate: float, periods: int) -> float:
        """
        Calculate present value
        Equivalent to Excel PV function
        Formula: FV / (1 + rate)^periods
        """
        return future_value / (1 + rate) ** periods
    
    @staticmethod
    def future_value(present_value: float, rate: float, periods: int) -> float:
        """
        Calculate future value
        Equivalent to Excel FV function
        Formula: PV * (1 + rate)^periods
        """
        return present_value * (1 + rate) ** periods
    
    @staticmethod
    def npv(rate: float, cash_flows: List[float]) -> float:
        """
        Net Present Value calculation
        Equivalent to Excel NPV function
        """
        npv_value = 0
        for i, cf in enumerate(cash_flows):
            npv_value += cf / (1 + rate) ** (i + 1)
        return npv_value
    
    @staticmethod
    def irr_newton_raphson(cash_flows: List[float], initial_guess: float = 0.1, 
                          max_iterations: int = 100, tolerance: float = 1e-6) -> Optional[float]:
        """
        Internal Rate of Return using Newton-Raphson method
        Simplified equivalent to Excel IRR function
        """
        def npv_function(rate):
            return sum(cf / (1 + rate) ** (i + 1) for i, cf in enumerate(cash_flows))
        
        def npv_derivative(rate):
            return sum(-cf * (i + 1) / (1 + rate) ** (i + 2) for i, cf in enumerate(cash_flows))
        
        rate = initial_guess
        for _ in range(max_iterations):
            npv_val = npv_function(rate)
            if abs(npv_val) < tolerance:
                return rate
            
            npv_deriv = npv_derivative(rate)
            if abs(npv_deriv) < tolerance:
                return None  # Derivative too small
            
            rate = rate - npv_val / npv_deriv
        
        return None  # Failed to converge
    
    @staticmethod
    def debt_service_coverage_ratio(net_operating_income: float, 
                                   debt_service: float) -> float:
        """
        Calculate Debt Service Coverage Ratio
        Formula: Net Operating Income / Total Debt Service
        """
        if debt_service == 0:
            return float('inf')
        return net_operating_income / debt_service
    
    @staticmethod
    def return_on_equity(net_income: float, shareholders_equity: float) -> float:
        """
        Calculate Return on Equity
        Formula: Net Income / Shareholders' Equity
        """
        if shareholders_equity == 0:
            return 0.0
        return net_income / shareholders_equity


def demonstrate_formula_conversions():
    """
    Demonstrate specific Excel formula conversions from the Corporate Modelling file
    """
    print("=" * 70)
    print("EXCEL FORMULA CONVERSIONS - CORPORATE MODELLING EXAMPLES")
    print("=" * 70)
    
    # Original values from Excel
    goodwill_base = 18942
    intangible_base = 15999
    debt = 29412
    equity = 17655
    revenue_2020 = 50724
    cost_2020 = 28684
    
    excel = ExcelFormulas()
    financial = FinancialFormulas()
    
    print("\n1. GOODWILL AND INTANGIBLE ASSETS")
    print("   Excel Formula: =18942+15999")
    result1 = goodwill_base + intangible_base
    print(f"   Python Result: {result1:,}")
    
    print("\n2. DEBT-TO-EQUITY RATIO")
    print("   Excel Formula: =$D10/$D18")
    result2 = excel.ratio(debt, equity)
    print(f"   Python Result: {result2:.6f}")
    
    print("\n3. COST OF SALES RATIO")
    print("   Excel Formula: =28684/D15")
    result3 = excel.ratio(cost_2020, revenue_2020)
    print(f"   Python Result: {result3:.6f} ({result3:.1%})")
    
    print("\n4. COMPOUND GROWTH CALCULATION")
    print("   Excel Formula: =(IAM!F15/IAM!E15)^(1/5)-1")
    # Example with hypothetical values
    start_val, end_val = 50000, 55000
    result4 = excel.compound_growth_rate(start_val, end_val, 5)
    print(f"   Python Result: {result4:.6f} ({result4:.2%})")
    
    print("\n5. ASSETS NOT ELSEWHERE CLASSIFIED")
    print("   Excel Formula: =D12-SUM(D50,D8:D9)")
    total_assets = 67659  # From Excel
    ppe = 10558
    goodwill_intangible = result1
    other_assets = 4116  # Opening cash
    result5 = total_assets - excel.sum_range([other_assets, ppe, goodwill_intangible])
    print(f"   Python Result: {result5:,}")
    
    print("\n6. REVENUE PROJECTION WITH GROWTH")
    print("   Excel Pattern: =PreviousRevenue*(1+GrowthRate)^Years")
    growth_rate = 0.02  # 2% annual growth
    years = 5
    result6 = financial.future_value(revenue_2020, growth_rate, years)
    print(f"   Python Result: {result6:,.0f}")
    
    print("\n7. MULTIPLE CELL REFERENCES (SUM EXAMPLE)")
    print("   Excel Formula: =SUM(D37,D39:D41)")
    # Example values that might be in those cells
    sample_values = [1000, 1500, 2000, 2500]
    result7 = excel.sum_range(sample_values)
    print(f"   Python Result: {result7:,}")
    
    print("\n8. CONDITIONAL CALCULATION")
    print("   Excel Formula: =IF(Revenue>0, Revenue*0.1, 0)")
    revenue = 50724
    result8 = excel.if_condition(revenue > 0, revenue * 0.1, 0)
    print(f"   Python Result: {result8:,.0f}")
    
    print(f"\n{'=' * 70}")
    print("All Excel formulas successfully converted to Python!")


if __name__ == "__main__":
    demonstrate_formula_conversions()