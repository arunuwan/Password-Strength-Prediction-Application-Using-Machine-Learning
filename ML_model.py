import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib
import os

# Load the dataset with dtype parameter to handle mixed types warning
dataset = pd.read_csv('password_dataset.csv', dtype={'password': str})

# Convert all values in the 'password' column to strings
dataset['password'] = dataset['password'].astype(str)

# Extract features (presence of digits, special symbols, etc.)
dataset['has_digits'] = dataset['password'].apply(lambda x: any(char.isdigit() for char in str(x)))
dataset['has_special_symbols'] = dataset['password'].apply(lambda x: any(char in '!@#$%^&*()-_=+[{]}\\|;:\'",<.>/?' for char in str(x)))
dataset['length'] = dataset['password'].apply(len)  # Add the length feature

# Define features (X) and target variable (y)
X = dataset[['has_digits', 'has_special_symbols', 'length']]
y = dataset['strength']

# Split the dataset into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Random Forest classifier
classifier = RandomForestClassifier(n_estimators=100, random_state=42)
classifier.fit(X_train, y_train)

# Save the trained model to a file with error handling
try:
    joblib.dump(classifier, 'password_strength_model.pkl')
    print("Model saved successfully.")
except Exception as e:
    print(f"Error saving the model: {e}")

# Check if the file exists in the current working directory
if os.path.isfile('password_strength_model.pkl'):
    print("File exists in the current working directory.")
else:
    print("File does not exist in the current working directory.")

# Predict on the test set
y_pred = classifier.predict(X_test)

# Print the classification report
print("Classification Report:")
print(classification_report(y_test, y_pred))
