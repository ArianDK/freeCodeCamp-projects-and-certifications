import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import requests
import io
import os
from typing import List, Tuple, Optional

class DataGraphExplorer:
    def __init__(self):
        self.df = None
        self.column_names = []
        
    def load_csv_from_file(self, file_path: str) -> bool:
        """Load CSV file from local computer"""
        try:
            if not os.path.exists(file_path):
                print(f"Error: File '{file_path}' not found.")
                return False
            
            self.df = pd.read_csv(file_path)
            self.column_names = list(self.df.columns)
            print(f"Successfully loaded CSV file: {file_path}")
            return True
        except Exception as e:
            print(f"Error loading file: {e}")
            return False
    
    def load_csv_from_url_input(self) -> bool:
        """Get URL from user input and load CSV"""
        url = input("Enter the URL of the CSV file: ").strip()
        return self.load_csv_from_url(url)
    
    def load_csv_from_url(self, url: str) -> bool:
        """Load CSV file from URL"""
        try:
            print(f"Downloading CSV from: {url}")
            response = requests.get(url)
            response.raise_for_status()
            
            self.df = pd.read_csv(io.StringIO(response.text))
            self.column_names = list(self.df.columns)
            print(f"Successfully loaded CSV from URL")
            return True
        except Exception as e:
            print(f"Error loading from URL: {e}")
            return False
    
    def load_csv_from_hardcoded_url(self) -> bool:
        """Load CSV from a hardcoded URL in the code"""
        # Example URLs - you can modify these
        urls = [
            "https://raw.githubusercontent.com/datasets/gdp/master/data/gdp.csv",
            "https://raw.githubusercontent.com/plotly/datasets/master/iris.csv",
            "https://raw.githubusercontent.com/plotly/datasets/master/tips.csv"
        ]
        
        print("Available hardcoded URLs:")
        for i, url in enumerate(urls, 1):
            print(f"{i}. {url}")
        
        try:
            choice = int(input("Select URL number (1-3): ")) - 1
            if 0 <= choice < len(urls):
                return self.load_csv_from_url(urls[choice])
            else:
                print("Invalid choice.")
                return False
        except ValueError:
            print("Please enter a valid number.")
            return False
    
    def display_data_info(self):
        """Print headings and first two rows"""
        if self.df is None:
            print("No data loaded. Please load a CSV file first.")
            return
        
        print("\n" + "="*50)
        print("DATASET INFORMATION")
        print("="*50)
        
        print(f"Dataset shape: {self.df.shape}")
        print(f"Number of rows: {len(self.df)}")
        print(f"Number of columns: {len(self.column_names)}")
        
        print("\nCOLUMN HEADINGS:")
        for i, col in enumerate(self.column_names, 1):
            print(f"{i:2d}. {col}")
        
        print("\nFIRST TWO ROWS:")
        print(self.df.head(2).to_string(index=False))
        
        print("\nDATA TYPES:")
        print(self.df.dtypes)
        
        print("\nBASIC STATISTICS:")
        print(self.df.describe())
    
    def get_numeric_columns(self) -> List[str]:
        """Get list of numeric columns"""
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
        return numeric_cols
    
    def select_columns(self) -> Tuple[Optional[np.ndarray], Optional[np.ndarray]]:
        """Let user select columns and convert to numpy arrays"""
        if self.df is None:
            print("No data loaded. Please load a CSV file first.")
            return None, None
        
        numeric_cols = self.get_numeric_columns()
        
        if len(numeric_cols) < 1:
            print("No numeric columns found in the dataset.")
            return None, None
        
        print("\nAvailable numeric columns:")
        for i, col in enumerate(numeric_cols, 1):
            print(f"{i}. {col}")
        
        try:
            # Select first column
            choice1 = int(input(f"\nSelect first column (1-{len(numeric_cols)}): ")) - 1
            if not (0 <= choice1 < len(numeric_cols)):
                print("Invalid choice for first column.")
                return None, None
            
            col1_name = numeric_cols[choice1]
            col1_data = self.df[col1_name].dropna().to_numpy()
            
            # Ask if user wants a second column
            use_second = input("Do you want to select a second column? (y/n): ").lower().strip()
            
            if use_second == 'y' and len(numeric_cols) > 1:
                choice2 = int(input(f"Select second column (1-{len(numeric_cols)}): ")) - 1
                if not (0 <= choice2 < len(numeric_cols)) or choice2 == choice1:
                    print("Invalid choice for second column.")
                    return col1_data, None
                
                col2_name = numeric_cols[choice2]
                col2_data = self.df[col2_name].dropna().to_numpy()
                
                # Ensure both arrays have the same length
                min_length = min(len(col1_data), len(col2_data))
                col1_data = col1_data[:min_length]
                col2_data = col2_data[:min_length]
                
                print(f"Selected columns: {col1_name} and {col2_name}")
                return col1_data, col2_data
            else:
                print(f"Selected column: {col1_name}")
                return col1_data, None
                
        except ValueError:
            print("Please enter valid numbers.")
            return None, None
    
    def create_scatter_plot(self, x_data: np.ndarray, y_data: np.ndarray, x_label: str, y_label: str):
        """Create a scatter plot"""
        plt.figure(figsize=(10, 6))
        plt.scatter(x_data, y_data, alpha=0.6, s=50)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.title(f'Scatter Plot: {x_label} vs {y_label}')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()
    
    def create_line_plot(self, x_data: np.ndarray, y_data: np.ndarray, x_label: str, y_label: str):
        """Create a line plot"""
        plt.figure(figsize=(10, 6))
        plt.plot(x_data, y_data, marker='o', linewidth=2, markersize=4)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.title(f'Line Plot: {x_label} vs {y_label}')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()
    
    def create_histogram(self, data: np.ndarray, label: str):
        """Create a histogram"""
        plt.figure(figsize=(10, 6))
        plt.hist(data, bins=30, alpha=0.7, edgecolor='black')
        plt.xlabel(label)
        plt.ylabel('Frequency')
        plt.title(f'Histogram of {label}')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()
    
    def interpret_graph(self, x_data: np.ndarray, y_data: Optional[np.ndarray], x_label: str, y_label: Optional[str]):
        """Provide basic interpretation of the data"""
        print("\n" + "="*50)
        print("DATA INTERPRETATION")
        print("="*50)
        
        print(f"X-axis ({x_label}):")
        print(f"  - Mean: {np.mean(x_data):.2f}")
        print(f"  - Median: {np.median(x_data):.2f}")
        print(f"  - Standard deviation: {np.std(x_data):.2f}")
        print(f"  - Min: {np.min(x_data):.2f}")
        print(f"  - Max: {np.max(x_data):.2f}")
        
        if y_data is not None:
            print(f"\nY-axis ({y_label}):")
            print(f"  - Mean: {np.mean(y_data):.2f}")
            print(f"  - Median: {np.median(y_data):.2f}")
            print(f"  - Standard deviation: {np.std(y_data):.2f}")
            print(f"  - Min: {np.min(y_data):.2f}")
            print(f"  - Max: {np.max(y_data):.2f}")
            
            # Calculate correlation
            correlation = np.corrcoef(x_data, y_data)[0, 1]
            print(f"\nCorrelation between {x_label} and {y_label}: {correlation:.3f}")
            
            if abs(correlation) > 0.7:
                print("  - Strong correlation")
            elif abs(correlation) > 0.3:
                print("  - Moderate correlation")
            else:
                print("  - Weak correlation")
        
        print(f"\nNumber of data points: {len(x_data)}")
    
    def run(self):
        """Main application loop"""
        print("="*60)
        print("DATA GRAPH EXPLORER")
        print("="*60)
        print("This application allows you to explore CSV data and create visualizations.")
        
        while True:
            print("\n" + "="*40)
            print("MAIN MENU")
            print("="*40)
            print("1. Load CSV from local file")
            print("2. Load CSV from URL input")
            print("3. Load CSV from hardcoded URL")
            print("4. Display data information")
            print("5. Create visualizations")
            print("6. Exit")
            
            choice = input("\nSelect an option (1-6): ").strip()
            
            if choice == '1':
                file_path = input("Enter the path to your CSV file: ").strip()
                self.load_csv_from_file(file_path)
                
            elif choice == '2':
                self.load_csv_from_url_input()
                
            elif choice == '3':
                self.load_csv_from_hardcoded_url()
                
            elif choice == '4':
                self.display_data_info()
                
            elif choice == '5':
                if self.df is None:
                    print("Please load a CSV file first (options 1-3).")
                    continue
                
                print("\n" + "="*40)
                print("VISUALIZATION MENU")
                print("="*40)
                print("1. Scatter plot")
                print("2. Line plot")
                print("3. Histogram")
                print("4. Back to main menu")
                
                viz_choice = input("\nSelect visualization type (1-4): ").strip()
                
                if viz_choice in ['1', '2', '3']:
                    col1_data, col2_data = self.select_columns()
                    
                    if col1_data is not None:
                        numeric_cols = self.get_numeric_columns()
                        
                        if viz_choice == '1' and col2_data is not None:
                            # Scatter plot
                            self.create_scatter_plot(col1_data, col2_data, 
                                                   numeric_cols[0], numeric_cols[1])
                            self.interpret_graph(col1_data, col2_data, 
                                               numeric_cols[0], numeric_cols[1])
                            
                        elif viz_choice == '2' and col2_data is not None:
                            # Line plot
                            self.create_line_plot(col1_data, col2_data, 
                                                numeric_cols[0], numeric_cols[1])
                            self.interpret_graph(col1_data, col2_data, 
                                               numeric_cols[0], numeric_cols[1])
                            
                        elif viz_choice == '3':
                            # Histogram
                            self.create_histogram(col1_data, numeric_cols[0])
                            self.interpret_graph(col1_data, None, numeric_cols[0], None)
                            
                        else:
                            print("For scatter and line plots, you need to select two columns.")
                
            elif choice == '6':
                print("Thank you for using Data Graph Explorer!")
                break
                
            else:
                print("Invalid choice. Please select 1-6.")

def main():
    """Main function to run the application"""
    # Set up matplotlib style
    plt.style.use('default')
    sns.set_palette("husl")
    
    # Create and run the explorer
    explorer = DataGraphExplorer()
    explorer.run()

if __name__ == "__main__":
    main()
