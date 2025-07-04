import math
import sys
from typing import Union, Tuple

class FinancialCalculator:
    """A comprehensive financial calculator with various financial and mathematical functions."""
    
    def __init__(self):
        self.pi = math.pi
        self.e = math.e
    
    def calculate_annuity(self, principal: float, rate: float, time: float, 
                         compounding: str = "monthly") -> dict:
        """
        Calculate annuity with monthly or continuous growth.
        
        Args:
            principal: Initial amount
            rate: Annual interest rate (as decimal)
            time: Time in years
            compounding: "monthly" or "continuous"
        
        Returns:
            Dictionary with future value and breakdown
        """
        if compounding.lower() == "monthly":
            # Monthly compounding: A = P(1 + r/n)^(nt)
            n = 12  # monthly compounding
            future_value = principal * (1 + rate/n)**(n * time)
            effective_rate = (1 + rate/n)**n - 1
        elif compounding.lower() == "continuous":
            # Continuous compounding: A = Pe^(rt)
            future_value = principal * math.exp(rate * time)
            effective_rate = math.exp(rate) - 1
        else:
            raise ValueError("Compounding must be 'monthly' or 'continuous'")
        
        interest_earned = future_value - principal
        
        return {
            "principal": principal,
            "rate": rate,
            "time": time,
            "compounding": compounding,
            "future_value": future_value,
            "interest_earned": interest_earned,
            "effective_annual_rate": effective_rate
        }
    
    def calculate_mortgage_payment(self, principal: float, rate: float, 
                                 years: int) -> dict:
        """
        Calculate monthly mortgage payment.
        
        Args:
            principal: Loan amount
            rate: Annual interest rate (as decimal)
            years: Loan term in years
        
        Returns:
            Dictionary with payment details
        """
        monthly_rate = rate / 12
        num_payments = years * 12
        
        if monthly_rate == 0:
            monthly_payment = principal / num_payments
        else:
            # P = L[c(1 + c)^n]/[(1 + c)^n - 1]
            # where P = payment, L = loan amount, c = monthly rate, n = number of payments
            monthly_payment = principal * (monthly_rate * (1 + monthly_rate)**num_payments) / \
                             ((1 + monthly_rate)**num_payments - 1)
        
        total_payment = monthly_payment * num_payments
        total_interest = total_payment - principal
        
        return {
            "principal": principal,
            "annual_rate": rate,
            "monthly_rate": monthly_rate,
            "years": years,
            "num_payments": num_payments,
            "monthly_payment": monthly_payment,
            "total_payment": total_payment,
            "total_interest": total_interest
        }
    
    def estimate_retirement_balance(self, monthly_contribution: float, 
                                  current_balance: float, rate: float, 
                                  years: int) -> dict:
        """
        Estimate retirement investment balance.
        
        Args:
            monthly_contribution: Monthly contribution amount
            current_balance: Current retirement balance
            rate: Annual return rate (as decimal)
            years: Years until retirement
        
        Returns:
            Dictionary with retirement planning details
        """
        monthly_rate = rate / 12
        num_months = years * 12
        
        # Future value of current balance
        future_value_current = current_balance * (1 + rate)**years
        
        # Future value of monthly contributions
        if monthly_rate == 0:
            future_value_contributions = monthly_contribution * num_months
        else:
            # FV = PMT * [(1 + r)^n - 1] / r
            future_value_contributions = monthly_contribution * \
                ((1 + monthly_rate)**num_months - 1) / monthly_rate
        
        total_balance = future_value_current + future_value_contributions
        total_contributions = monthly_contribution * num_months
        total_interest = total_balance - current_balance - total_contributions
        
        return {
            "monthly_contribution": monthly_contribution,
            "current_balance": current_balance,
            "annual_rate": rate,
            "years": years,
            "future_value_current": future_value_current,
            "future_value_contributions": future_value_contributions,
            "total_balance": total_balance,
            "total_contributions": total_contributions,
            "total_interest": total_interest
        }
    
    def doubling_time(self, rate: float, compounding: str = "continuous") -> float:
        """
        Determine how long until an amount doubles, given the rate.
        
        Args:
            rate: Annual interest rate (as decimal)
            compounding: "continuous" or "annual"
        
        Returns:
            Time in years for amount to double
        """
        if rate <= 0:
            raise ValueError("Rate must be positive")
        
        if compounding.lower() == "continuous":
            # For continuous compounding: 2 = e^(rt)
            # t = ln(2) / r
            return math.log(2) / rate
        elif compounding.lower() == "annual":
            # For annual compounding: 2 = (1 + r)^t
            # t = log(2) / log(1 + r)
            return math.log(2) / math.log(1 + rate)
        else:
            raise ValueError("Compounding must be 'continuous' or 'annual'")
    
    def solve_logarithmic_equation(self, equation_type: str, **kwargs) -> dict:
        """
        Solve logarithmic equations.
        
        Args:
            equation_type: Type of equation to solve
            **kwargs: Parameters for the specific equation type
        
        Returns:
            Dictionary with solution and steps
        """
        if equation_type == "basic_log":
            # Solve log_b(x) = y for x
            base = kwargs.get('base', 10)
            result = kwargs.get('result')
            if result is None:
                raise ValueError("Result value required")
            solution = base ** result
            return {
                "equation": f"log_{base}(x) = {result}",
                "solution": solution,
                "steps": f"x = {base}^{result} = {solution}"
            }
        
        elif equation_type == "natural_log":
            # Solve ln(x) = y for x
            result = kwargs.get('result')
            if result is None:
                raise ValueError("Result value required")
            solution = math.exp(result)
            return {
                "equation": f"ln(x) = {result}",
                "solution": solution,
                "steps": f"x = e^{result} = {solution}"
            }
        
        elif equation_type == "exponential":
            # Solve a^x = b for x
            base = kwargs.get('base')
            target = kwargs.get('target')
            if base is None or target is None:
                raise ValueError("Base and target values required")
            solution = math.log(target, base)
            return {
                "equation": f"{base}^x = {target}",
                "solution": solution,
                "steps": f"x = log_{base}({target}) = {solution}"
            }
        
        else:
            raise ValueError("Equation type must be 'basic_log', 'natural_log', or 'exponential'")
    
    def to_scientific_notation(self, number: float) -> str:
        """
        Convert number to scientific notation.
        
        Args:
            number: Number to convert
        
        Returns:
            String in scientific notation
        """
        if number == 0:
            return "0.0e+00"
        
        # Handle negative numbers
        sign = "-" if number < 0 else ""
        abs_number = abs(number)
        
        # Calculate exponent
        if abs_number >= 1:
            exponent = int(math.floor(math.log10(abs_number)))
        else:
            exponent = int(math.floor(math.log10(abs_number))) - 1
        
        # Calculate mantissa
        mantissa = abs_number / (10 ** exponent)
        
        # Format to 3 decimal places
        mantissa_str = f"{mantissa:.3f}".rstrip('0').rstrip('.')
        if mantissa_str == "1":
            mantissa_str = "1.000"
        
        return f"{sign}{mantissa_str}e{exponent:+03d}"
    
    def from_scientific_notation(self, sci_notation: str) -> float:
        """
        Convert from scientific notation to decimal.
        
        Args:
            sci_notation: String in scientific notation (e.g., "1.23e+04")
        
        Returns:
            Decimal number
        """
        try:
            return float(sci_notation)
        except ValueError:
            raise ValueError("Invalid scientific notation format")
    
    def format_currency(self, amount: float) -> str:
        """Format amount as currency."""
        return f"${amount:,.2f}"
    
    def format_percentage(self, rate: float) -> str:
        """Format rate as percentage."""
        return f"{rate * 100:.2f}%"


def display_menu():
    """Display the main menu."""
    print("\n" + "="*60)
    print("           FINANCIAL CALCULATOR")
    print("="*60)
    print("1. Calculate Annuity (Monthly/Continuous Growth)")
    print("2. Calculate Monthly Mortgage Payment")
    print("3. Estimate Retirement Investment Balance")
    print("4. Calculate Doubling Time")
    print("5. Solve Logarithmic Equations")
    print("6. Convert to Scientific Notation")
    print("7. Convert from Scientific Notation")
    print("8. Exit")
    print("="*60)


def get_float_input(prompt: str, min_value: float = None, max_value: float = None) -> float:
    """Get valid float input from user."""
    while True:
        try:
            value = float(input(prompt))
            if min_value is not None and value < min_value:
                print(f"Value must be at least {min_value}")
                continue
            if max_value is not None and value > max_value:
                print(f"Value must be at most {max_value}")
                continue
            return value
        except ValueError:
            print("Please enter a valid number.")


def main():
    """Main function to run the financial calculator."""
    calc = FinancialCalculator()
    
    while True:
        display_menu()
        choice = input("\nEnter your choice (1-8): ").strip()
        
        if choice == "1":
            print("\n--- ANNUITY CALCULATOR ---")
            principal = get_float_input("Enter principal amount: $", 0)
            rate = get_float_input("Enter annual interest rate (as decimal, e.g., 0.05 for 5%): ", 0)
            time = get_float_input("Enter time in years: ", 0)
            compounding = input("Enter compounding (monthly/continuous): ").strip().lower()
            
            try:
                result = calc.calculate_annuity(principal, rate, time, compounding)
                print(f"\nResults:")
                print(f"Principal: {calc.format_currency(result['principal'])}")
                print(f"Annual Rate: {calc.format_percentage(result['rate'])}")
                print(f"Time: {result['time']} years")
                print(f"Compounding: {result['compounding']}")
                print(f"Future Value: {calc.format_currency(result['future_value'])}")
                print(f"Interest Earned: {calc.format_currency(result['interest_earned'])}")
                print(f"Effective Annual Rate: {calc.format_percentage(result['effective_annual_rate'])}")
            except ValueError as e:
                print(f"Error: {e}")
        
        elif choice == "2":
            print("\n--- MORTGAGE PAYMENT CALCULATOR ---")
            principal = get_float_input("Enter loan amount: $", 0)
            rate = get_float_input("Enter annual interest rate (as decimal, e.g., 0.045 for 4.5%): ", 0)
            years = int(get_float_input("Enter loan term in years: ", 1, 50))
            
            try:
                result = calc.calculate_mortgage_payment(principal, rate, years)
                print(f"\nResults:")
                print(f"Loan Amount: {calc.format_currency(result['principal'])}")
                print(f"Annual Rate: {calc.format_percentage(result['annual_rate'])}")
                print(f"Loan Term: {result['years']} years")
                print(f"Monthly Payment: {calc.format_currency(result['monthly_payment'])}")
                print(f"Total Payment: {calc.format_currency(result['total_payment'])}")
                print(f"Total Interest: {calc.format_currency(result['total_interest'])}")
            except ValueError as e:
                print(f"Error: {e}")
        
        elif choice == "3":
            print("\n--- RETIREMENT PLANNING CALCULATOR ---")
            monthly_contribution = get_float_input("Enter monthly contribution: $", 0)
            current_balance = get_float_input("Enter current retirement balance: $", 0)
            rate = get_float_input("Enter annual return rate (as decimal, e.g., 0.07 for 7%): ", 0)
            years = int(get_float_input("Enter years until retirement: ", 1, 50))
            
            try:
                result = calc.estimate_retirement_balance(monthly_contribution, current_balance, rate, years)
                print(f"\nResults:")
                print(f"Monthly Contribution: {calc.format_currency(result['monthly_contribution'])}")
                print(f"Current Balance: {calc.format_currency(result['current_balance'])}")
                print(f"Annual Return Rate: {calc.format_percentage(result['annual_rate'])}")
                print(f"Years to Retirement: {result['years']}")
                print(f"Future Value of Current Balance: {calc.format_currency(result['future_value_current'])}")
                print(f"Future Value of Contributions: {calc.format_currency(result['future_value_contributions'])}")
                print(f"Total Retirement Balance: {calc.format_currency(result['total_balance'])}")
                print(f"Total Contributions: {calc.format_currency(result['total_contributions'])}")
                print(f"Total Interest Earned: {calc.format_currency(result['total_interest'])}")
            except ValueError as e:
                print(f"Error: {e}")
        
        elif choice == "4":
            print("\n--- DOUBLING TIME CALCULATOR ---")
            rate = get_float_input("Enter annual interest rate (as decimal, e.g., 0.07 for 7%): ", 0)
            compounding = input("Enter compounding (continuous/annual): ").strip().lower()
            
            try:
                doubling_time = calc.doubling_time(rate, compounding)
                print(f"\nResults:")
                print(f"Annual Rate: {calc.format_percentage(rate)}")
                print(f"Compounding: {compounding}")
                print(f"Doubling Time: {doubling_time:.2f} years")
                print(f"Rule of 72 Approximation: {72 / (rate * 100):.2f} years")
            except ValueError as e:
                print(f"Error: {e}")
        
        elif choice == "5":
            print("\n--- LOGARITHMIC EQUATION SOLVER ---")
            print("Equation types:")
            print("1. Basic logarithm: log_b(x) = y")
            print("2. Natural logarithm: ln(x) = y")
            print("3. Exponential: a^x = b")
            
            eq_type = input("Enter equation type (1/2/3): ").strip()
            
            try:
                if eq_type == "1":
                    base = get_float_input("Enter base: ", 0.1)
                    result = get_float_input("Enter result value: ")
                    solution = calc.solve_logarithmic_equation("basic_log", base=base, result=result)
                elif eq_type == "2":
                    result = get_float_input("Enter result value: ")
                    solution = calc.solve_logarithmic_equation("natural_log", result=result)
                elif eq_type == "3":
                    base = get_float_input("Enter base: ", 0.1)
                    target = get_float_input("Enter target value: ", 0)
                    solution = calc.solve_logarithmic_equation("exponential", base=base, target=target)
                else:
                    print("Invalid choice.")
                    continue
                
                print(f"\nResults:")
                print(f"Equation: {solution['equation']}")
                print(f"Solution: {solution['solution']:.6f}")
                print(f"Steps: {solution['steps']}")
            except ValueError as e:
                print(f"Error: {e}")
        
        elif choice == "6":
            print("\n--- SCIENTIFIC NOTATION CONVERTER ---")
            number = get_float_input("Enter number to convert: ")
            sci_notation = calc.to_scientific_notation(number)
            print(f"\nResults:")
            print(f"Original: {number}")
            print(f"Scientific Notation: {sci_notation}")
        
        elif choice == "7":
            print("\n--- SCIENTIFIC NOTATION CONVERTER ---")
            sci_notation = input("Enter number in scientific notation (e.g., 1.23e+04): ").strip()
            try:
                decimal = calc.from_scientific_notation(sci_notation)
                print(f"\nResults:")
                print(f"Scientific Notation: {sci_notation}")
                print(f"Decimal: {decimal}")
            except ValueError as e:
                print(f"Error: {e}")
        
        elif choice == "8":
            print("\nThank you for using the Financial Calculator!")
            break
        
        else:
            print("Invalid choice. Please enter a number between 1 and 8.")
        
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()
