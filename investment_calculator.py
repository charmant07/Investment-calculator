import time
import matplotlib.pyplot as plt

def super_investment_calculator():
    try:
        print("=== SUPER INVESTMENT CALCULATOR 2.0 ===")
        print("Now with advanced features! 📈\n")
        
        # 1. USER INPUTS WITH FLEXIBLE INTEREST RATES
        P = int(input("What's your initial investment: $"))
        t_years = int(input("In how many years do you want to reach your goal: "))
        
        # Let user choose interest rate or use default
        rate_choice = input("Use default 8% S&P 500 average? (yes/no): ").lower().strip()
        if rate_choice in ["yes", "y"]:
            annual_r = 0.08
        else:
            annual_r = float(input("Enter your expected annual return (e.g., 7 for 7%): ")) / 100
        
        # 2. INFLATION ADJUSTMENT
        inflation_choice = input("Adjust for inflation? (yes/no): ").lower().strip()
        if inflation_choice in ["yes", "y"]:
            inflation_rate = float(input("Expected annual inflation (e.g., 2.5 for 2.5%): ")) / 100
        else:
            inflation_rate = 0
        
        # Monthly contributions
        PMT_response = input("Do you prefer monthly contribution? (yes/no): ").lower().strip()
        PMT = int(input("How much per month: $")) if PMT_response in ["yes", "y"] else 0
        
        # 3. DIFFERENT INVESTMENT STRATEGIES
        print("\n=== INVESTMENT STRATEGIES ===")
        print("1. Aggressive (Stocks only - Higher risk/return)")
        print("2. Balanced (60% Stocks, 40% Bonds)")
        print("3. Conservative (Bonds only - Lower risk/return)")
        
        strategy_choice = input("Choose strategy (1/2/3) or press Enter for custom: ")
        
        strategies = {
            "1": {"name": "Aggressive", "return": annual_r, "risk": "High"},
            "2": {"name": "Balanced", "return": annual_r * 0.85, "risk": "Medium"}, 
            "3": {"name": "Conservative", "return": annual_r * 0.60, "risk": "Low"}
        }
        
        if strategy_choice in strategies:
            strategy = strategies[strategy_choice]
            print(f"Selected: {strategy['name']} strategy ({strategy['risk']} risk)")
            annual_r = strategy['return']
        else:
            strategy = {"name": "Custom", "risk": "Variable"}
        
        # CALCULATIONS
        monthly_r = annual_r / 12
        months = 12 * t_years
        
        # Future value calculation
        if PMT > 0:
            future_value = P * (1 + monthly_r)**months + PMT * (((1 + monthly_r)**months - 1) / monthly_r)
        else:
            future_value = P * (1 + annual_r)**t_years
        
        # Inflation adjustment
        future_value_real = future_value / ((1 + inflation_rate) ** t_years)
        
        # 4. COMPARE STRATEGIES
        print("\n=== STRATEGY COMPARISON ===")
        comparison_data = []
        
        for strat_name, strat_info in strategies.items():
            strat_return = annual_r if strat_name == "1" else annual_r * (0.85 if strat_name == "2" else 0.60)
            
            if PMT > 0:
                strat_fv = P * (1 + strat_return/12)**months + PMT * (((1 + strat_return/12)**months - 1) / (strat_return/12))
            else:
                strat_fv = P * (1 + strat_return)**t_years
            
            comparison_data.append((strat_info['name'], strat_fv))
            print(f"{strat_info['name']}: ${strat_fv:,.2f}")
        
        # DISPLAY RESULTS
        print(f"\n=== YOUR RESULTS ===")
        print(f"Strategy: {strategy['name']}")
        print(f"Initial investment: ${P:,}")
        print(f"Monthly contribution: ${PMT:,}")
        print(f"Annual return: {annual_r*100:.1f}%")
        print(f"Inflation rate: {inflation_rate*100:.1f}%")
        print(f"Investment period: {t_years} years")
        print(f"Future value (nominal): ${future_value:,.2f}")
        print(f"Future value (real - after inflation): ${future_value_real:,.2f}")
        
        # 5. YEARLY BREAKDOWN
        breakdown = input("\nDo you want to see yearly growth breakdown? (yes/no): ").lower().strip()
        
        if breakdown in ["yes", "y"]:
            print("\n=== YEARLY GROWTH BREAKDOWN ===")
            years_data = []
            current_value = P
            
            for year in range(1, t_years + 1):
                if PMT > 0:
                    months_passed = 12 * year
                    year_value = P * (1 + monthly_r)**months_passed + PMT * (((1 + monthly_r)**months_passed - 1) / monthly_r)
                else:
                    year_value = P * (1 + annual_r)**year
                
                real_value = year_value / ((1 + inflation_rate) ** year)
                growth = year_value - current_value
                
                print(f"Year {year}: ${year_value:,.2f} (Real: ${real_value:,.2f}) (+${growth:,.2f})")
                years_data.append((year, year_value, real_value))
                time.sleep(0.3)
            
            # 6. CREATE CHARTS
            chart_choice = input("\nDo you want to see charts? (yes/no): ").lower().strip()
            if chart_choice in ["yes", "y"]:
                create_charts(years_data, comparison_data, strategy['name'])
        
    except ValueError:
        print("Please enter valid numbers!")

def create_charts(years_data, comparison_data, user_strategy):
    """Create matplotlib charts to visualize the data"""
    
    # Extract data for charts
    years = [data[0] for data in years_data]
    nominal_values = [data[1] for data in years_data]
    real_values = [data[2] for data in years_data]
    
    # Chart 1: Growth Over Time
    plt.figure(figsize=(12, 5))
    
    plt.subplot(1, 2, 1)
    plt.plot(years, nominal_values, 'b-', label='Nominal Value', linewidth=2)
    plt.plot(years, real_values, 'r--', label='Real Value (After Inflation)', linewidth=2)
    plt.xlabel('Years')
    plt.ylabel('Portfolio Value ($)')
    plt.title('Investment Growth Over Time')
    plt.legend()
    plt.grid(True)
    
    # Chart 2: Strategy Comparison
    plt.subplot(1, 2, 2)
    strategy_names = [data[0] for data in comparison_data]
    strategy_values = [data[1] for data in comparison_data]
    
    colors = ['green' if name == user_strategy else 'blue' for name in strategy_names]
    bars = plt.bar(strategy_names, strategy_values, color=colors, alpha=0.7)
    
    plt.xlabel('Investment Strategy')
    plt.ylabel('Final Portfolio Value ($)')
    plt.title('Strategy Comparison')
    plt.xticks(rotation=45)
    
    # Add value labels on bars
    for bar, value in zip(bars, strategy_values):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height(), f'${value:,.0f}', 
                ha='center', va='bottom', fontsize=9)
    
    plt.tight_layout()
    plt.show()

# Run the super calculator
super_investment_calculator()
