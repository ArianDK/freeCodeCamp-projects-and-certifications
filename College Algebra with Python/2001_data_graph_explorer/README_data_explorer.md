# Data Graph Explorer

A comprehensive Python application for exploring CSV data and creating various types of visualizations.

## Features

### CSV Loading Options
1. **Local File Upload**: Load CSV files from your local computer
2. **URL Input**: Enter a URL to download and load CSV data
3. **Hardcoded URLs**: Use pre-defined URLs for quick testing

### Data Analysis
- Display dataset information (shape, columns, data types)
- Show first two rows of data
- Basic statistical analysis
- Column selection and conversion to NumPy arrays

### Visualization Types
- **Scatter Plots**: Visualize relationships between two variables
- **Line Plots**: Show trends over time or ordered data
- **Histograms**: Display distribution of single variables

### Data Interpretation
- Statistical summaries (mean, median, standard deviation, min/max)
- Correlation analysis between variables
- Automatic interpretation of correlation strength

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the application:
```bash
python 2001_data_graph_explorer.py
```

2. Follow the interactive menu to:
   - Load your CSV data
   - Explore the dataset
   - Create visualizations
   - Interpret the results

## Example Workflow

1. **Load Data**: Choose option 1, 2, or 3 to load a CSV file
2. **Explore Data**: Use option 4 to see dataset information
3. **Create Visualizations**: Use option 5 to create graphs
4. **Interpret Results**: The application automatically provides statistical analysis

## Sample Datasets

The application includes several sample datasets via hardcoded URLs:
- GDP data
- Iris flower dataset
- Restaurant tips dataset

## Requirements

- Python 3.7+
- pandas
- numpy
- matplotlib
- seaborn
- requests

## Features in Detail

### CSV Loading Methods

**Method 1: Local File**
- Enter the full path to your CSV file
- Supports any CSV format

**Method 2: URL Input**
- Enter any publicly accessible CSV URL
- Automatically downloads and processes the data

**Method 3: Hardcoded URLs**
- Quick access to sample datasets
- No need to find or download files manually

### Data Processing

- Automatically detects numeric columns
- Handles missing values (NaN)
- Ensures data compatibility for plotting
- Converts data to NumPy arrays for efficient processing

### Visualization Features

- **Scatter Plots**: Perfect for correlation analysis
- **Line Plots**: Ideal for time series or sequential data
- **Histograms**: Great for understanding data distributions
- Professional styling with grids and proper labeling

### Statistical Analysis

- Descriptive statistics for all variables
- Correlation coefficients between variables
- Automatic interpretation of correlation strength
- Data point counts and validation

## Tips for Best Results

1. **Data Quality**: Ensure your CSV has clean, numeric data for best visualizations
2. **Column Selection**: Choose meaningful variable pairs for scatter/line plots
3. **Interpretation**: Pay attention to correlation values and their interpretation
4. **Multiple Views**: Try different visualization types on the same data

## Troubleshooting

- **File Not Found**: Double-check the file path for local files
- **URL Errors**: Ensure the URL is publicly accessible and returns CSV data
- **No Numeric Columns**: The application only works with numeric data for plotting
- **Empty Plots**: Check that your selected columns contain valid numeric data

## Educational Value

This application is perfect for:
- Learning data analysis concepts
- Understanding statistical relationships
- Practicing data visualization
- Exploring real-world datasets
- Understanding correlation and causation

Enjoy exploring your data! 