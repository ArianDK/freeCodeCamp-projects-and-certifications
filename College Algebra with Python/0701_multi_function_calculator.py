import math
import fractions
from typing import Union, Tuple, Optional

class MultiFunctionCalculator:
    def __init__(self):
        self.history = []
    
    def solve_proportion(self, a: float, b: float, c: float) -> float:
        """
        Solve proportion: a/b = c/x
        Returns x = (b * c) / a
        """
        if a == 0:
            raise ValueError("Cannot divide by zero in proportion")
        result = (b * c) / a
        self.history.append(f"Proportion: {a}/{b} = {c}/x → x = {result}")
        return result
    
    def solve_proportion_from_string(self, proportion_str: str) -> float:
        """
        Solve proportion from string format like "a/b = c/d"
        Returns the value of d
        """
        # Clean up the input string
        proportion_str = proportion_str.replace(" ", "").lower()
        
        if "=" not in proportion_str:
            raise ValueError("Invalid proportion format. Use '=' to separate ratios.")
        
        left, right = proportion_str.split("=")
        
        # Parse left side: a/b
        if "/" not in left:
            raise ValueError(f"Invalid left side format '{left}'. Use 'a/b' format.")
        a_str, b_str = left.split("/")
        try:
            a = float(a_str)
            b = float(b_str)
        except ValueError:
            raise ValueError(f"Invalid numbers in left side: {left}")
        
        # Parse right side: c/d
        if "/" not in right:
            raise ValueError(f"Invalid right side format '{right}'. Use 'c/d' format.")
        c_str, d_str = right.split("/")
        try:
            c = float(c_str)
        except ValueError:
            raise ValueError(f"Invalid number in right side: {c_str}")
        
        # If d is a variable (like 'x'), solve for it
        if d_str.lower() in ['x', 'd', '?']:
            result = self.solve_proportion(a, b, c)
            self.history.append(f"Proportion: {proportion_str} → x = {result}")
            return result
        else:
            # If d is a number, verify the proportion
            d = float(d_str)
            expected_d = self.solve_proportion(a, b, c)
            if abs(d - expected_d) < 0.0001:  # Allow for floating point precision
                self.history.append(f"Proportion: {proportion_str} ✓ (verified)")
                return d
            else:
                self.history.append(f"Proportion: {proportion_str} → expected x = {expected_d}")
                return expected_d
    
    def solve_equation_for_x(self, equation: str) -> float:
        """
        Solve simple linear equations for x
        Supports formats like: "2x + 3 = 7", "3x - 5 = 10", "x/2 = 4"
        """
        equation = equation.replace(" ", "").lower()
        
        # Handle different equation formats
        if "=" in equation:
            left, right = equation.split("=")
            
            # Move all terms to left side
            if "x" in right:
                # Swap sides if x is on right
                left, right = right, left
            
            # Parse left side to get coefficient and constant
            coeff, const = self._parse_linear_expression(left)
            
            # Parse right side
            right_val = self._evaluate_expression(right)
            
            # Solve: coeff*x + const = right_val
            # So: coeff*x = right_val - const
            # And: x = (right_val - const) / coeff
            
            if coeff == 0:
                raise ValueError("No x term found in equation")
            
            result = (right_val - const) / coeff
            self.history.append(f"Equation: {equation} → x = {result}")
            return result
        else:
            raise ValueError("Invalid equation format. Use '=' to separate sides.")
    
    def _parse_linear_expression(self, expr: str) -> Tuple[float, float]:
        """Parse expression like '2x+3' or '3x-5' into (coefficient, constant)"""
        coeff = 0
        const = 0
        
        # Handle x term
        if "x" in expr:
            if expr.startswith("x"):
                coeff = 1
                expr = expr[1:]
            elif expr.startswith("-x"):
                coeff = -1
                expr = expr[2:]
            else:
                # Find coefficient before x
                x_index = expr.find("x")
                coeff_str = expr[:x_index]
                if coeff_str == "":
                    coeff = 1
                elif coeff_str == "-":
                    coeff = -1
                else:
                    coeff = float(coeff_str)
                expr = expr[x_index + 1:]
        
        # Handle constant term
        if expr:
            if expr.startswith("+"):
                const = float(expr[1:])
            elif expr.startswith("-"):
                const = -float(expr[1:])
            else:
                const = float(expr)
        
        return coeff, const
    
    def _evaluate_expression(self, expr: str) -> float:
        """Evaluate simple numeric expressions"""
        # Handle basic operations
        expr = expr.replace(" ", "")
        
        # Handle division
        if "/" in expr:
            num, denom = expr.split("/")
            return float(num) / float(denom)
        
        return float(expr)
    
    def factor_square_root(self, number: int) -> str:
        """
        Factor square root into simplified form
        Returns string like "2√3" for √12
        """
        if number < 0:
            raise ValueError("Cannot factor negative square root")
        
        if number == 0:
            return "0"
        
        # Find perfect square factors
        perfect_square = 1
        remaining = number
        
        for i in range(2, int(math.sqrt(number)) + 1):
            while remaining % (i * i) == 0:
                perfect_square *= i
                remaining //= (i * i)
        
        if perfect_square == 1:
            result = f"√{number}"
        elif remaining == 1:
            result = str(perfect_square)
        else:
            result = f"{perfect_square}√{remaining}"
        
        self.history.append(f"√{number} = {result}")
        return result
    
    def decimal_to_fraction(self, decimal: float) -> str:
        """Convert decimal to fraction"""
        frac = fractions.Fraction(decimal).limit_denominator(1000)
        result = f"{frac.numerator}/{frac.denominator}"
        self.history.append(f"{decimal} = {result}")
        return result
    
    def decimal_to_percent(self, decimal: float) -> str:
        """Convert decimal to percent"""
        percent = decimal * 100
        result = f"{percent}%"
        self.history.append(f"{decimal} = {result}")
        return result
    
    def fraction_to_decimal(self, numerator: int, denominator: int) -> float:
        """Convert fraction to decimal"""
        if denominator == 0:
            raise ValueError("Denominator cannot be zero")
        result = numerator / denominator
        self.history.append(f"{numerator}/{denominator} = {result}")
        return result
    
    def fraction_to_percent(self, numerator: int, denominator: int) -> str:
        """Convert fraction to percent"""
        decimal = self.fraction_to_decimal(numerator, denominator)
        return self.decimal_to_percent(decimal)
    
    def percent_to_decimal(self, percent: float) -> float:
        """Convert percent to decimal"""
        result = percent / 100
        self.history.append(f"{percent}% = {result}")
        return result
    
    def percent_to_fraction(self, percent: float) -> str:
        """Convert percent to fraction"""
        decimal = self.percent_to_decimal(percent)
        return self.decimal_to_fraction(decimal)
    
    def show_history(self):
        """Display calculation history"""
        if not self.history:
            print("No calculations performed yet.")
            return
        
        print("\n=== Calculation History ===")
        for i, calc in enumerate(self.history, 1):
            print(f"{i}. {calc}")
    
    def clear_history(self):
        """Clear calculation history"""
        self.history.clear()
        print("History cleared.")

def main():
    calc = MultiFunctionCalculator()
    
    print("=== Multi-Function Calculator ===")
    print("Available operations:")
    print("1. Solve proportions")
    print("2. Solve equations for x")
    print("3. Factor square roots")
    print("4. Convert decimal to fraction")
    print("5. Convert decimal to percent")
    print("6. Convert fraction to decimal")
    print("7. Convert fraction to percent")
    print("8. Convert percent to decimal")
    print("9. Convert percent to fraction")
    print("10. Show history")
    print("11. Clear history")
    print("0. Exit")
    
    while True:
        try:
            choice = input("\nEnter your choice (0-11): ").strip()
            
            if choice == "0":
                print("Goodbye!")
                break
            
            elif choice == "1":
                print("Solve proportion: a/b = c/x")
                print("Enter the proportion as a string (e.g., '9/33 = 11/x' or '11/34 = 33/31'):")
                proportion_input = input("Enter proportion: ").strip()
                
                # Check if user entered separate values (old format)
                if proportion_input.replace(".", "").replace("-", "").isdigit():
                    print("Detected single number. Please enter the full proportion as a string.")
                    print("Example: '9/33 = 11/x' or '11/34 = 33/31'")
                    proportion_input = input("Enter proportion: ").strip()
                
                result = calc.solve_proportion_from_string(proportion_input)
                print(f"x = {result}")
            
            elif choice == "2":
                print("Solve equation for x (e.g., '2x + 3 = 7')")
                equation = input("Enter equation: ")
                result = calc.solve_equation_for_x(equation)
                print(f"x = {result}")
            
            elif choice == "3":
                number = int(input("Enter number to factor square root: "))
                result = calc.factor_square_root(number)
                print(f"√{number} = {result}")
            
            elif choice == "4":
                decimal = float(input("Enter decimal: "))
                result = calc.decimal_to_fraction(decimal)
                print(f"{decimal} = {result}")
            
            elif choice == "5":
                decimal = float(input("Enter decimal: "))
                result = calc.decimal_to_percent(decimal)
                print(f"{decimal} = {result}")
            
            elif choice == "6":
                num = int(input("Enter numerator: "))
                denom = int(input("Enter denominator: "))
                result = calc.fraction_to_decimal(num, denom)
                print(f"{num}/{denom} = {result}")
            
            elif choice == "7":
                num = int(input("Enter numerator: "))
                denom = int(input("Enter denominator: "))
                result = calc.fraction_to_percent(num, denom)
                print(f"{num}/{denom} = {result}")
            
            elif choice == "8":
                percent = float(input("Enter percent: "))
                result = calc.percent_to_decimal(percent)
                print(f"{percent}% = {result}")
            
            elif choice == "9":
                percent = float(input("Enter percent: "))
                result = calc.percent_to_fraction(percent)
                print(f"{percent}% = {result}")
            
            elif choice == "10":
                calc.show_history()
            
            elif choice == "11":
                calc.clear_history()
            
            else:
                print("Invalid choice. Please enter a number between 0 and 11.")
                
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
