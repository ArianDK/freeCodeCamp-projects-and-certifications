import matplotlib.pyplot as plt
import numpy as np
import random
import math
import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class GraphingCalculator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Graphing Calculator")
        self.root.geometry("1200x800")
        
        # Initialize variables
        self.functions = []  # List of (name, expression) tuples
        self.x_min, self.x_max = -10, 10
        self.y_min, self.y_max = -10, 10
        
        self.setup_ui()
        self.create_plot()
        
    def setup_ui(self):
        # Create main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel for controls
        left_panel = ttk.Frame(main_frame, width=300)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # Right panel for graph
        right_panel = ttk.Frame(main_frame)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Function input section
        func_frame = ttk.LabelFrame(left_panel, text="Function Input", padding=10)
        func_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(func_frame, text="Enter function (e.g., x**2, sin(x), 2*x+1):").pack(anchor=tk.W)
        self.func_entry = ttk.Entry(func_frame, width=30)
        self.func_entry.pack(fill=tk.X, pady=(0, 5))
        
        func_buttons = ttk.Frame(func_frame)
        func_buttons.pack(fill=tk.X)
        
        ttk.Button(func_buttons, text="Add Function", command=self.add_function).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(func_buttons, text="Remove Function", command=self.remove_function).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(func_buttons, text="Clear All", command=self.clear_functions).pack(side=tk.LEFT)
        
        # Function list
        ttk.Label(func_frame, text="Functions:").pack(anchor=tk.W, pady=(10, 0))
        self.func_listbox = tk.Listbox(func_frame, height=4)
        self.func_listbox.pack(fill=tk.X, pady=(0, 5))
        
        # Zoom controls
        zoom_frame = ttk.LabelFrame(left_panel, text="Zoom Controls", padding=10)
        zoom_frame.pack(fill=tk.X, pady=(0, 10))
        
        zoom_buttons = ttk.Frame(zoom_frame)
        zoom_buttons.pack(fill=tk.X)
        
        ttk.Button(zoom_buttons, text="Zoom In", command=self.zoom_in).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(zoom_buttons, text="Zoom Out", command=self.zoom_out).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(zoom_buttons, text="Reset View", command=self.reset_view).pack(side=tk.LEFT)
        
        # View range
        range_frame = ttk.LabelFrame(left_panel, text="View Range", padding=10)
        range_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(range_frame, text="X Range:").pack(anchor=tk.W)
        x_range_frame = ttk.Frame(range_frame)
        x_range_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(x_range_frame, text="Min:").pack(side=tk.LEFT)
        self.x_min_entry = ttk.Entry(x_range_frame, width=8)
        self.x_min_entry.pack(side=tk.LEFT, padx=(0, 5))
        self.x_min_entry.insert(0, str(self.x_min))
        
        ttk.Label(x_range_frame, text="Max:").pack(side=tk.LEFT)
        self.x_max_entry = ttk.Entry(x_range_frame, width=8)
        self.x_max_entry.pack(side=tk.LEFT, padx=(0, 5))
        self.x_max_entry.insert(0, str(self.x_max))
        
        ttk.Label(range_frame, text="Y Range:").pack(anchor=tk.W)
        y_range_frame = ttk.Frame(range_frame)
        y_range_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(y_range_frame, text="Min:").pack(side=tk.LEFT)
        self.y_min_entry = ttk.Entry(y_range_frame, width=8)
        self.y_min_entry.pack(side=tk.LEFT, padx=(0, 5))
        self.y_min_entry.insert(0, str(self.y_min))
        
        ttk.Label(y_range_frame, text="Max:").pack(side=tk.LEFT)
        self.y_max_entry = ttk.Entry(y_range_frame, width=8)
        self.y_max_entry.pack(side=tk.LEFT, padx=(0, 5))
        self.y_max_entry.insert(0, str(self.y_max))
        
        ttk.Button(range_frame, text="Update Range", command=self.update_range).pack(pady=(5, 0))
        
        # Special features
        features_frame = ttk.LabelFrame(left_panel, text="Special Features", padding=10)
        features_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(features_frame, text="Show Table", command=self.create_table).pack(fill=tk.X, pady=(0, 5))
        ttk.Button(features_frame, text="Solve System", command=self.solve_system_dialog).pack(fill=tk.X, pady=(0, 5))
        ttk.Button(features_frame, text="Solve Quadratic", command=self.solve_quadratic_dialog).pack(fill=tk.X)
        
        # Graph canvas
        self.fig = Figure(figsize=(8, 6))
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, right_panel)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    def create_plot(self):
        """Create the initial plot with grid and axes"""
        self.ax.clear()
        self.ax.grid(True, alpha=0.3)
        self.ax.axhline(y=0, color='k', linewidth=0.5)
        self.ax.axvline(x=0, color='k', linewidth=0.5)
        self.ax.set_xlim(self.x_min, self.x_max)
        self.ax.set_ylim(self.y_min, self.y_max)
        self.ax.set_xlabel('x')
        self.ax.set_ylabel('y')
        self.ax.set_title('Graphing Calculator')
        self.canvas.draw()
        
    def safe_eval(self, expr, x):
        """Safely evaluate mathematical expressions"""
        # Replace x with the actual value
        expr = expr.replace('x', f'({x})')
        
        # Add common math functions
        safe_dict = {
            'sin': math.sin, 'cos': math.cos, 'tan': math.tan,
            'asin': math.asin, 'acos': math.acos, 'atan': math.atan,
            'sinh': math.sinh, 'cosh': math.cosh, 'tanh': math.tanh,
            'sqrt': math.sqrt, 'log': math.log, 'log10': math.log10,
            'exp': math.exp, 'abs': abs, 'pi': math.pi, 'e': math.e,
            'floor': math.floor, 'ceil': math.ceil, 'round': round
        }
        
        try:
            return eval(expr, {"__builtins__": {}}, safe_dict)
        except:
            return None
            
    def add_function(self):
        """Add a function to the list"""
        func_str = self.func_entry.get().strip()
        if func_str:
            # Check if user provided a custom name (format: CustomName = Function)
            if '=' in func_str:
                parts = func_str.split('=', 1)
                if len(parts) == 2:
                    custom_name = parts[0].strip()
                    expression = parts[1].strip()
                    func_name = custom_name
                else:
                    # Invalid format, treat as regular function
                    expression = func_str
                    func_name = self.generate_function_name()
            else:
                # No custom name, generate automatic name
                expression = func_str
                func_name = self.generate_function_name()
            
            # Add function as (name, expression) tuple
            self.functions.append((func_name, expression))
            display_text = f"{func_name}(x) = {expression}"
            self.func_listbox.insert(tk.END, display_text)
            self.func_entry.delete(0, tk.END)
            self.plot_functions()
    
    def generate_function_name(self):
        """Generate automatic function names: f, g, h, etc."""
        used_names = [func[0] for func in self.functions]
        base_names = ['f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'z']
        
        for name in base_names:
            if name not in used_names:
                return name
        
        # If all single letters are used, use f1, f2, etc.
        counter = 1
        while f"f{counter}" in used_names:
            counter += 1
        return f"f{counter}"
    
    def remove_function(self):
        """Remove the selected function"""
        selection = self.func_listbox.curselection()
        if selection:
            index = selection[0]
            self.functions.pop(index)
            self.func_listbox.delete(index)
            self.plot_functions()
        else:
            messagebox.showwarning("Warning", "Please select a function to remove.")
            
    def clear_functions(self):
        """Clear all functions"""
        self.functions.clear()
        self.func_listbox.delete(0, tk.END)
        self.create_plot()
        
    def plot_functions(self):
        """Plot all functions"""
        self.create_plot()
        
        if not self.functions:
            return
            
        x = np.linspace(self.x_min, self.x_max, 1000)
        colors = ['blue', 'red', 'green', 'orange', 'purple', 'brown', 'pink', 'gray']
        
        for i, (func_name, func_str) in enumerate(self.functions):
            y = []
            for x_val in x:
                y_val = self.safe_eval(func_str, x_val)
                if y_val is not None and not math.isnan(y_val) and not math.isinf(y_val):
                    y.append(y_val)
                else:
                    y.append(None)
            
            # Filter out None values
            valid_points = [(x[j], y[j]) for j in range(len(x)) if y[j] is not None]
            if valid_points:
                x_plot, y_plot = zip(*valid_points)
                color = colors[i % len(colors)]
                self.ax.plot(x_plot, y_plot, color=color, linewidth=2, label=f'{func_name}(x) = {func_str}')
        
        if self.functions:
            self.ax.legend()
        self.canvas.draw()
        

        
    def zoom_in(self):
        """Zoom in on the graph"""
        x_range = self.x_max - self.x_min
        y_range = self.y_max - self.y_min
        
        self.x_min += x_range * 0.1
        self.x_max -= x_range * 0.1
        self.y_min += y_range * 0.1
        self.y_max -= y_range * 0.1
        
        self.update_range_entries()
        self.plot_functions()
        
    def zoom_out(self):
        """Zoom out on the graph"""
        x_range = self.x_max - self.x_min
        y_range = self.y_max - self.y_min
        
        self.x_min -= x_range * 0.1
        self.x_max += x_range * 0.1
        self.y_min -= y_range * 0.1
        self.y_max += y_range * 0.1
        
        self.update_range_entries()
        self.plot_functions()
        
    def reset_view(self):
        """Reset to default view"""
        self.x_min, self.x_max = -10, 10
        self.y_min, self.y_max = -10, 10
        self.update_range_entries()
        self.plot_functions()
        
    def update_range_entries(self):
        """Update the range entry fields"""
        self.x_min_entry.delete(0, tk.END)
        self.x_min_entry.insert(0, str(self.x_min))
        self.x_max_entry.delete(0, tk.END)
        self.x_max_entry.insert(0, str(self.x_max))
        self.y_min_entry.delete(0, tk.END)
        self.y_min_entry.insert(0, str(self.y_min))
        self.y_max_entry.delete(0, tk.END)
        self.y_max_entry.insert(0, str(self.y_max))
        
    def update_range(self):
        """Update the view range from entry fields"""
        try:
            self.x_min = float(self.x_min_entry.get())
            self.x_max = float(self.x_max_entry.get())
            self.y_min = float(self.y_min_entry.get())
            self.y_max = float(self.y_max_entry.get())
            self.plot_functions()
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for the range.")
            
    def create_table(self):
        """Create a table of (x,y) values"""
        if not self.functions:
            messagebox.showwarning("Warning", "No functions to create table for.")
            return
            
        # Create table window
        table_window = tk.Toplevel(self.root)
        table_window.title("Function Table")
        table_window.geometry("600x400")
        
        # Get range for table
        try:
            start_x = float(self.x_min_entry.get())
            end_x = float(self.x_max_entry.get())
        except ValueError:
            start_x, end_x = -10, 10
            
        # Create table
        tree = ttk.Treeview(table_window)
        tree["columns"] = ["x"] + [f"{func[0]}(x)" for func in self.functions]
        
        tree.column("#0", width=0, stretch=tk.NO)
        tree.column("x", anchor=tk.CENTER, width=100)
        for func in self.functions:
            tree.column(f"{func[0]}(x)", anchor=tk.CENTER, width=100)
            
        tree.heading("#0", text="")
        tree.heading("x", text="x")
        for func in self.functions:
            tree.heading(f"{func[0]}(x)", text=f"{func[0]}(x)")
            
        # Generate table data
        x_values = np.linspace(start_x, end_x, 21)  # 21 points
        
        for x_val in x_values:
            row = [f"{x_val:.2f}"]
            for func_name, func_str in self.functions:
                y_val = self.safe_eval(func_str, x_val)
                if y_val is not None and not math.isnan(y_val) and not math.isinf(y_val):
                    row.append(f"{y_val:.4f}")
                else:
                    row.append("undefined")
            tree.insert("", tk.END, values=row)
            
        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_window, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
    def solve_system_dialog(self):
        """Dialog for solving system of equations"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Solve System of Equations")
        dialog.geometry("400x300")
        
        ttk.Label(dialog, text="Enter two linear equations:").pack(pady=10)
        
        ttk.Label(dialog, text="Equation 1 (y = mx + b):").pack(anchor=tk.W, padx=10)
        eq1_frame = ttk.Frame(dialog)
        eq1_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(eq1_frame, text="m:").pack(side=tk.LEFT)
        m1_entry = ttk.Entry(eq1_frame, width=10)
        m1_entry.pack(side=tk.LEFT, padx=5)
        ttk.Label(eq1_frame, text="b:").pack(side=tk.LEFT)
        b1_entry = ttk.Entry(eq1_frame, width=10)
        b1_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(dialog, text="Equation 2 (y = mx + b):").pack(anchor=tk.W, padx=10)
        eq2_frame = ttk.Frame(dialog)
        eq2_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(eq2_frame, text="m:").pack(side=tk.LEFT)
        m2_entry = ttk.Entry(eq2_frame, width=10)
        m2_entry.pack(side=tk.LEFT, padx=5)
        ttk.Label(eq2_frame, text="b:").pack(side=tk.LEFT)
        b2_entry = ttk.Entry(eq2_frame, width=10)
        b2_entry.pack(side=tk.LEFT, padx=5)
        
        def solve_and_graph():
            try:
                m1, b1 = float(m1_entry.get()), float(b1_entry.get())
                m2, b2 = float(m2_entry.get()), float(b2_entry.get())
                
                # Solve system: y = m1*x + b1, y = m2*x + b2
                # m1*x + b1 = m2*x + b2
                # (m1 - m2)*x = b2 - b1
                # x = (b2 - b1) / (m1 - m2)
                
                if abs(m1 - m2) < 1e-10:
                    messagebox.showinfo("Result", "Lines are parallel - no solution")
                    return
                    
                x_solution = (b2 - b1) / (m1 - m2)
                y_solution = m1 * x_solution + b1
                
                # Add functions to main calculator
                self.functions = [("f", f"{m1}*x + {b1}"), ("g", f"{m2}*x + {b2}")]
                self.func_listbox.delete(0, tk.END)
                for func_name, func_expr in self.functions:
                    display_text = f"{func_name}(x) = {func_expr}"
                    self.func_listbox.insert(tk.END, display_text)
                
                # Plot functions
                self.plot_functions()
                
                # Mark intersection point
                self.ax.plot(x_solution, y_solution, 'ro', markersize=8, label=f'Solution: ({x_solution:.3f}, {y_solution:.3f})')
                self.ax.legend()
                self.canvas.draw()
                
                messagebox.showinfo("Solution", f"Intersection point: ({x_solution:.3f}, {y_solution:.3f})")
                dialog.destroy()
                
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers.")
                
        ttk.Button(dialog, text="Solve and Graph", command=solve_and_graph).pack(pady=20)
        
    def solve_quadratic_dialog(self):
        """Dialog for solving quadratic equations"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Solve Quadratic Equation")
        dialog.geometry("400x250")
        
        ttk.Label(dialog, text="Enter coefficients for ax² + bx + c = 0:").pack(pady=10)
        
        coeff_frame = ttk.Frame(dialog)
        coeff_frame.pack(pady=10)
        
        ttk.Label(coeff_frame, text="a:").grid(row=0, column=0, padx=5)
        a_entry = ttk.Entry(coeff_frame, width=10)
        a_entry.grid(row=0, column=1, padx=5)
        a_entry.insert(0, "1")
        
        ttk.Label(coeff_frame, text="b:").grid(row=1, column=0, padx=5)
        b_entry = ttk.Entry(coeff_frame, width=10)
        b_entry.grid(row=1, column=1, padx=5)
        b_entry.insert(0, "0")
        
        ttk.Label(coeff_frame, text="c:").grid(row=2, column=0, padx=5)
        c_entry = ttk.Entry(coeff_frame, width=10)
        c_entry.grid(row=2, column=1, padx=5)
        c_entry.insert(0, "-4")
        
        def solve_and_graph():
            try:
                a, b, c = float(a_entry.get()), float(b_entry.get()), float(c_entry.get())
                
                if abs(a) < 1e-10:
                    messagebox.showerror("Error", "Coefficient 'a' cannot be zero.")
                    return
                    
                # Calculate discriminant
                discriminant = b**2 - 4*a*c
                
                # Find roots
                if discriminant > 0:
                    x1 = (-b + math.sqrt(discriminant)) / (2*a)
                    x2 = (-b - math.sqrt(discriminant)) / (2*a)
                    roots_text = f"Two real roots: x = {x1:.3f} and x = {x2:.3f}"
                elif discriminant == 0:
                    x1 = -b / (2*a)
                    roots_text = f"One real root: x = {x1:.3f}"
                else:
                    real_part = -b / (2*a)
                    imag_part = math.sqrt(-discriminant) / (2*a)
                    roots_text = f"Complex roots: x = {real_part:.3f} ± {imag_part:.3f}i"
                
                # Add quadratic function to main calculator
                func_str = f"{a}*x**2 + {b}*x + {c}"
                self.functions = [("f", func_str)]
                self.func_listbox.delete(0, tk.END)
                display_text = f"f(x) = {func_str}"
                self.func_listbox.insert(tk.END, display_text)
                
                # Plot function
                self.plot_functions()
                
                # Mark real roots if they exist
                if discriminant >= 0:
                    if discriminant > 0:
                        self.ax.plot(x1, 0, 'ro', markersize=8, label=f'Root 1: ({x1:.3f}, 0)')
                        self.ax.plot(x2, 0, 'ro', markersize=8, label=f'Root 2: ({x2:.3f}, 0)')
                    else:
                        self.ax.plot(x1, 0, 'ro', markersize=8, label=f'Root: ({x1:.3f}, 0)')
                    self.ax.legend()
                    self.canvas.draw()
                
                messagebox.showinfo("Solution", roots_text)
                dialog.destroy()
                
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers.")
                
        ttk.Button(dialog, text="Solve and Graph", command=solve_and_graph).pack(pady=20)
        
    def run(self):
        """Start the graphing calculator"""
        self.root.mainloop()

if __name__ == "__main__":
    # Create and run the graphing calculator
    calculator = GraphingCalculator()
    calculator.run()
