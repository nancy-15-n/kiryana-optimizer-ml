import pandas as pd

df = pd.read_csv('kiryana_sales.csv')
df['Date'] = pd.to_datetime(df['Date'])

# Extract basic time features
df['Month'] = df['Date'].dt.month
df['Day_of_Week'] = df['Date'].dt.dayofweek
df['Is_Weekend'] = df['Day_of_Week'].isin([5, 6]).astype(int)
# Group by product and calculate a 7-day rolling sum of units sold, shifted backward
df['Next_7_Day_Demand'] = df.groupby('Product_Name')['Units_Sold'].transform(
    lambda x: x.rolling(window=7, min_periods=1).sum().shift(-7)
)

# Drop rows where the future target is NaN (the last 7 days of our dataset)
df = df.dropna()
# Convert categorical features into numeric columns
df = pd.get_dummies(df, columns=['Category', 'Product_Name'], drop_first=True)
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import joblib

# 1. Separate Features (X) and Target (y)
# We drop 'Date' because models can't handle raw datetime values directly
X = df.drop(columns=['Date', 'Next_7_Day_Demand', 'Daily_Revenue', 'Units_Sold'])
y = df['Next_7_Day_Demand']

# 2. Split into Training and Testing sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. Initialize and train the model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 4. Evaluate the model performance
predictions = model.predict(X_test)
mae = mean_absolute_error(y_test, predictions)
print(f"Model Training Complete! On average, predictions are off by: {round(mae, 2)} units.")

# 5. Save the trained model and the feature list for the web application
joblib.dump(model, 'kiryana_model.pkl')
joblib.dump(X_train.columns.tolist(), 'model_features.pkl')