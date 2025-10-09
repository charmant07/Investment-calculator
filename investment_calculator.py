import time

def investment_calculator():
    try:
        print("=== INVESTMENT CALCULATOR ===")
        
        P = int(input("What's your initial investment: $"))
        t_years = int(input("In how many years do you want to reach your goal: "))
        
        PMT_response = input("Do you prefer monthly contribution? (yes/no): ").lower().strip()
        
        annual_r = 0.08
        monthly_r = annual_r / 12

        if PMT_response in ["yes", "y"]:
            PMT = int(input("Great! How much per month: $"))
        else:
            PMT = 0

        # Calculate final value
        months = 12 * t_years
        if PMT > 0:
            future_value = P * (1 + monthly_r)**months + PMT * (((1 + monthly_r)**months - 1) / monthly_r)
        else:
            future_value = P * (1 + annual_r)**t_years  # Simpler for yearly without monthly contributions

        print(f"\nFinal value after {t_years} years: ${future_value:,.2f}")
        
        # NEW FEATURE: Yearly breakdown
        breakdown = input("\nDo you want to see yearly growth breakdown? (yes/no): ").lower().strip()
        
        if breakdown in ["yes", "y"]:
            print("\n=== YEARLY GROWTH ===")
            current_value = P
            
            for year in range(1, t_years + 1):
                if PMT > 0:
                    # With monthly contributions - more complex calculation
                    months_passed = 12 * year
                    year_value = P * (1 + monthly_r)**months_passed + PMT * (((1 + monthly_r)**months_passed - 1) / monthly_r)
                else:
                    # Without monthly contributions - simple compound interest
                    year_value = P * (1 + annual_r)**year
                
                growth = year_value - current_value
                print(f"Year {year}: ${year_value:,.2f} (+${growth:,.2f})")
                time.sleep(0.5)  # Pause between years
                
    except ValueError:
        print("Please enter valid numbers!")

investment_calculator()