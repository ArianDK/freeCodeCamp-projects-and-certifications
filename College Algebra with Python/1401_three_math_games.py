import random
import math
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.backends.backend_tkagg as tkagg

class MathGames:
    def __init__(self):
        self.score = 0
        self.total_questions = 0
        
    def scatter_plot_game(self):
        """Scatter plot game where player identifies coordinates"""
        print("\n=== SCATTER PLOT GAME ===")
        print("Identify the coordinates of the highlighted point!")
        
        # Generate random points
        x_coords = [random.randint(-10, 10) for _ in range(5)]
        y_coords = [random.randint(-10, 10) for _ in range(5)]
        
        # Choose a random point to highlight
        target_index = random.randint(0, 4)
        target_x = x_coords[target_index]
        target_y = y_coords[target_index]
        
        # Create the plot
        plt.figure(figsize=(8, 6))
        plt.scatter(x_coords, y_coords, c='blue', s=100, alpha=0.6)
        plt.scatter(target_x, target_y, c='red', s=200, marker='*', label='Target Point')
        
        plt.grid(True, alpha=0.3)
        plt.axhline(y=0, color='k', linestyle='-', alpha=0.3)
        plt.axvline(x=0, color='k', linestyle='-', alpha=0.3)
        plt.xlim(-12, 12)
        plt.ylim(-12, 12)
        plt.xlabel('X-axis')
        plt.ylabel('Y-axis')
        plt.title('Scatter Plot Game - Find the Red Star!')
        plt.legend()
        
        # Show the plot
        plt.show()
        
        # Get player's answer
        try:
            player_x = int(input("Enter the X coordinate of the red star: "))
            player_y = int(input("Enter the Y coordinate of the red star: "))
            
            if player_x == target_x and player_y == target_y:
                print("Correct! Well done!")
                self.score += 1
            else:
                print(f"Wrong! The correct answer was ({target_x}, {target_y})")
            
            self.total_questions += 1
            
        except ValueError:
            print("Please enter valid integers!")
    
    def algebra_practice_game(self):
        """Algebra practice game with one-step and two-step equations"""
        print("\n=== ALGEBRA PRACTICE GAME ===")
        print("Solve the equations!")
        
        # Generate random equation
        equation_type = random.choice(['one_step', 'two_step'])
        
        if equation_type == 'one_step':
            # One-step equation: ax + b = c
            a = random.randint(-5, 5)
            while a == 0:  # Avoid division by zero
                a = random.randint(-5, 5)
            b = random.randint(-10, 10)
            c = random.randint(-15, 15)
            
            # Calculate correct answer
            correct_answer = (c - b) / a
            
            print(f"Solve for x: {a}x + {b} = {c}")
            
        else:
            # Two-step equation: ax + b = cx + d
            a = random.randint(-4, 4)
            while a == 0:
                a = random.randint(-4, 4)
            b = random.randint(-8, 8)
            c = random.randint(-4, 4)
            while c == a:  # Avoid same coefficients
                c = random.randint(-4, 4)
            d = random.randint(-8, 8)
            
            # Calculate correct answer
            correct_answer = (d - b) / (a - c)
            
            print(f"Solve for x: {a}x + {b} = {c}x + {d}")
        
        try:
            player_answer = float(input("Enter your answer: "))
            
            # Check if answer is correct (with small tolerance for floating point)
            if abs(player_answer - correct_answer) < 0.01:
                print("Correct! Well done!")
                self.score += 1
            else:
                print(f"Wrong! The correct answer was {correct_answer}")
            
            self.total_questions += 1
            
        except ValueError:
            print("Please enter a valid number!")
    
    def projectile_game(self):
        """Projectile game with parabolic motion"""
        print("\n=== PROJECTILE GAME ===")
        print("Adjust the parabolic path to clear the wall!")
        
        # Generate random wall
        wall_x = random.randint(3, 8)
        wall_height = random.randint(2, 6)
        
        print(f"Wall is at x = {wall_x} with height = {wall_height}")
        
        # Create the game window
        root = tk.Tk()
        root.title("Projectile Game")
        root.geometry("800x600")
        
        # Create matplotlib figure
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Draw the wall
        wall = Rectangle((wall_x, 0), 0.2, wall_height, facecolor='red', alpha=0.7)
        ax.add_patch(wall)
        
        # Set up the plot
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.grid(True, alpha=0.3)
        ax.set_xlabel('Distance')
        ax.set_ylabel('Height')
        ax.set_title('Projectile Game - Clear the Red Wall!')
        
        # Create sliders
        frame = tk.Frame(root)
        frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        a_var = tk.DoubleVar(value=1.0)
        b_var = tk.DoubleVar(value=5.0)
        c_var = tk.DoubleVar(value=0.0)
        
        tk.Label(frame, text="a (coefficient of x²):").pack()
        a_slider = tk.Scale(frame, from_=-2, to=2, resolution=0.1, orient=tk.HORIZONTAL, variable=a_var)
        a_slider.pack(fill=tk.X)
        
        tk.Label(frame, text="b (coefficient of x):").pack()
        b_slider = tk.Scale(frame, from_=0, to=10, resolution=0.1, orient=tk.HORIZONTAL, variable=b_var)
        b_slider.pack(fill=tk.X)
        
        tk.Label(frame, text="c (constant):").pack()
        c_slider = tk.Scale(frame, from_=0, to=5, resolution=0.1, orient=tk.HORIZONTAL, variable=c_var)
        c_slider.pack(fill=tk.X)
        
        # Embed matplotlib in tkinter
        canvas = tkagg.FigureCanvasTkAgg(fig, root)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        
        def update_plot():
            ax.clear()
            
            # Redraw wall
            wall = Rectangle((wall_x, 0), 0.2, wall_height, facecolor='red', alpha=0.7)
            ax.add_patch(wall)
            
            # Plot parabola
            x = np.linspace(0, 10, 100)
            a_val = a_var.get()
            b_val = b_var.get()
            c_val = c_var.get()
            
            y = a_val * x**2 + b_val * x + c_val
            ax.plot(x, y, 'b-', linewidth=2, label=f'y = {a_val:.1f}x² + {b_val:.1f}x + {c_val:.1f}')
            
            # Check if parabola clears the wall
            wall_y = a_val * wall_x**2 + b_val * wall_x + c_val
            if wall_y > wall_height:
                ax.plot(wall_x, wall_y, 'go', markersize=10, label='Success!')
                status = "SUCCESS! Wall cleared!"
            else:
                ax.plot(wall_x, wall_y, 'ro', markersize=10, label='Failed')
                status = "FAILED! Try again!"
            
            ax.set_xlim(0, 10)
            ax.set_ylim(0, 10)
            ax.grid(True, alpha=0.3)
            ax.set_xlabel('Distance')
            ax.set_ylabel('Height')
            ax.set_title(f'Projectile Game - {status}')
            ax.legend()
            
            canvas.draw()
        
        # Update plot when sliders change
        a_slider.config(command=lambda x: update_plot())
        b_slider.config(command=lambda x: update_plot())
        c_slider.config(command=lambda x: update_plot())
        
        # Initial plot
        update_plot()
        
        # Add submit button
        def submit():
            a_val = a_var.get()
            b_val = b_var.get()
            c_val = c_var.get()
            
            wall_y = a_val * wall_x**2 + b_val * wall_x + c_val
            
            if wall_y > wall_height:
                messagebox.showinfo("Success!", "Congratulations! You cleared the wall!")
                self.score += 1
            else:
                messagebox.showinfo("Failed", f"Your projectile hit the wall at height {wall_y:.2f}")
            
            self.total_questions += 1
            plt.close(fig)  # Close the matplotlib figure
            root.destroy()
        
        submit_btn = tk.Button(frame, text="Submit Solution", command=submit)
        submit_btn.pack(pady=10)
        
        # Handle window closing
        def on_closing():
            plt.close(fig)  # Close the matplotlib figure
            root.destroy()
        
        root.protocol("WM_DELETE_WINDOW", on_closing)
        root.mainloop()
    
    def advanced_projectile_game(self):
        """Advanced projectile game where player enters coefficients directly"""
        print("\n=== ADVANCED PROJECTILE GAME ===")
        print("Enter the coefficients a, b, c for the equation y = ax² + bx + c")
        
        # Generate random wall
        wall_x = random.randint(3, 8)
        wall_height = random.randint(2, 6)
        
        print(f"Wall is at x = {wall_x} with height = {wall_height}")
        
        try:
            a = float(input("Enter coefficient a: "))
            b = float(input("Enter coefficient b: "))
            c = float(input("Enter coefficient c: "))
            
            # Calculate if parabola clears the wall
            wall_y = a * wall_x**2 + b * wall_x + c
            
            print(f"Your equation: y = {a}x² + {b}x + {c}")
            print(f"At x = {wall_x}, y = {wall_y}")
            
            if wall_y > wall_height:
                print("SUCCESS! You cleared the wall!")
                self.score += 1
            else:
                print(f"FAILED! Your projectile hit the wall at height {wall_y:.2f}")
            
            self.total_questions += 1
            
        except ValueError:
            print("Please enter valid numbers!")
    
    def show_menu(self):
        """Display the main menu"""
        while True:
            print("\n" + "="*50)
            print("           MATH GAMES MENU")
            print("="*50)
            print("1. Scatter Plot Game")
            print("2. Algebra Practice Game")
            print("3. Projectile Game (with sliders)")
            print("4. Advanced Projectile Game (enter coefficients)")
            print("5. Show Score")
            print("6. Exit")
            print("="*50)
            
            choice = input("Enter your choice (1-6): ")
            
            if choice == '1':
                self.scatter_plot_game()
            elif choice == '2':
                self.algebra_practice_game()
            elif choice == '3':
                self.projectile_game()
            elif choice == '4':
                self.advanced_projectile_game()
            elif choice == '5':
                self.show_score()
            elif choice == '6':
                print("Thanks for playing! Goodbye!")
                break
            else:
                print("Invalid choice! Please enter 1-6.")
    
    def show_score(self):
        """Display current score"""
        if self.total_questions == 0:
            print("No games played yet!")
        else:
            percentage = (self.score / self.total_questions) * 100
            print(f"\nScore: {self.score}/{self.total_questions} ({percentage:.1f}%)")

def main():
    """Main function to run the math games"""
    print("Welcome to the Math Games!")
    print("This program contains three educational math games.")
    
    games = MathGames()
    games.show_menu()

if __name__ == "__main__":
    main()
