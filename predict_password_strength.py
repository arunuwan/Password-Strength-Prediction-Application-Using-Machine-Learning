import joblib
import numpy as np

# Load the trained model
model = joblib.load('password_strength_model.pkl')
print("Model Loaded Successfully")

# Function to extract features from a given password
def extract_features(password):
    has_digits = any(char.isdigit() for char in password)
    has_special_symbols = any(char in '!@#$%^&*()-_=+[{]}\\|;:\'",<.>/?' for char in password)
    length = len(password)
    return [has_digits, has_special_symbols, length]

# Function to predict password strength
def predict_password_strength(password):
    # Extract features from the given password
    features = extract_features(password)

    # Predict the strength of the password using the trained model
    prediction = model.predict([features])[0]  # Predict the class (Weak, Medium, Strong)
    probabilities = model.predict_proba([features])[0]  # Get probabilities for each class

    # Map prediction to label
    strength_labels = ['Weak', 'Medium', 'Strong']
    predicted_strength = strength_labels[prediction]

    # Print the probabilities for each class
    print(f"Predicted Strength: {predicted_strength}")
    print(f"Probabilities: Weak: {probabilities[0]:.2f}, Medium: {probabilities[1]:.2f}, Strong: {probabilities[2]:.2f}")

    return predicted_strength, probabilities

# Test with a sample password
if __name__ == "__main__":
    user_password = input("Enter a password to check its strength: ")
    predict_password_strength(user_password)
