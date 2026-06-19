import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Set seed for reproducibility
np.random.seed(42)

# 1. Define typical Kiryana items and their categories
products = {
    'Aashirvaad Atta 5kg': {'cat': 'Staples', 'price': 260},
    'Fortune Mustard Oil 1L': {'cat': 'Staples', 'price': 175},
    'Maggi Noodles 4-Pack': {'cat': 'Snacks', 'price': 60},
    'Amul Butter 100g': {'cat': 'Dairy', 'price': 56},
    'Surf Excel 1kg': {'cat': 'Household', 'price': 140},
    'Amul Taaza Milk 1L': {'cat': 'Dairy', 'price': 66},
    'Kwality Walls Vanilla 1L': {'cat': 'Ice Cream', 'price': 200}
}

# 2. Generate dates for the last 2 years (approx 730 days)
start_date = datetime(2024, 6, 1)
date_list = [start_date + timedelta(days=x) for x in range(730)]

data_rows = []

for date in date_list:
    is_weekend = date.weekday() in [5, 6]  # Saturday/Sunday
    month = date.month
    
    for prod, info in products.items():
        # Base daily sales volume
        base_sales = np.random.randint(2, 10)
        
        # Add real-world business logic/patterns
        if is_weekend:
            base_sales += np.random.randint(3, 8)  # Weekends are busier
        if info['cat'] == 'Ice Cream' and month in [4, 5, 6, 7]:
            base_sales += np.random.randint(8, 15) # Summer spike for ice cream
        if info['cat'] == 'Staples' and month in [10, 11]:
            base_sales += np.random.randint(5, 12) # Festive season spike (Diwali)
            
        revenue = base_sales * info['price']
        
        # Calculate current stock left arbitrarily for data generation
        current_stock = np.random.randint(0, 30)
        
        data_rows.append([date, prod, info['cat'], base_sales, info['price'], revenue, current_stock])

# 3. Save to CSV
sales_df = pd.DataFrame(data_rows, columns=['Date', 'Product_Name', 'Category', 'Units_Sold', 'Price_Per_Unit', 'Daily_Revenue', 'Current_Stock'])
sales_df.to_csv('kiryana_sales.csv', index=False)
print("Step 1 Complete: 'kiryana_sales.csv' generated successfully!")