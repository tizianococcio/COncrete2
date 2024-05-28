from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline
import pandas as pd
import joblib

# Load and split data
data = pd.read_csv('data.csv')
X = data.drop('co2_emissions', axis=1)
y = data['co2_emissions']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
scaler = joblib.load('model/scaler.joblib')
model = make_pipeline(scaler, PolynomialFeatures(2), LinearRegression())
model.fit(X_train, y_train)

# Save model
joblib.dump(model, 'model/model.pkl')

# Save test data
joblib.dump([X_test, y_test], 'model/test_split.pkl')