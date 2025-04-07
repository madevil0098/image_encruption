from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import mean_squared_error
import joblib
import pandas
import numpy
import ast
# Read data from a file
t=pandas.read_csv("test1.csv",low_memory=False)
# Read data from file 
print(t)
# Split data into training and testing sets

y=pandas.DataFrame(t, columns = ["x","y","z"])

try:
    X_train, X_test, y_train, y_test = train_test_split(y,numpy.array(t["key"]),test_size=0.2, random_state=42)
except Exception as e:
    print("red")
# Train a linear regression model

model =LogisticRegression()
model.fit(y,t["key"])

# Save the model
model_filename = "linear_regression_model2.pkl"
joblib.dump(model, model_filename)

# Evaluate the model
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print("Mean Squared Error:", mse)
t=model.score(X_test,y_test)
print(t)
# Other important metrics can be printed here, such as R-squared, MAE, etc.
# For simplicity, let's just print the model coefficients and intercept
print("Model Coefficients:", model.coef_)
print("Model Intercept:", model.intercept_)
