import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import joblib  # Import joblib to load the model

# Step 1: Load the trained model
model = joblib.load('password_strength_model.pkl')  # Update to use joblib and load the .pkl model
print("Model Loaded Successfully")

# Step 2: Function to extract features from a given password
def extract_features(password):
    has_digits = any(char.isdigit() for char in password)
    has_special_symbols = any(char in '!@#$%^&*()-_=+[{]}\|;:",<.>/?' for char in password)
    length = len(password)
    return {
        'has_digits': has_digits,
        'has_special_symbols': has_special_symbols,
        'length': length
    }

# Step 3: Function to predict password strength, display suggestions, and plot probabilities
def predict_password_strength():
    password = entry.get()
    if not password:
        messagebox.showwarning("Input Error", "Please enter a password.")
        return

    # Extract features from the given password
    features = extract_features(password)

    # Create a DataFrame for the extracted features
    features_df = pd.DataFrame([features])

    # Predict the strength of the password using the trained model
    prediction = model.predict(features_df)[0]  # Predict the class (Weak, Medium, Strong)
    probabilities = model.predict_proba(features_df)[0]  # Get probabilities for each class

    # Map prediction to label
    strength_labels = ['Weak', 'Medium', 'Strong']
    predicted_strength = strength_labels[prediction]

    # Update the GUI with the prediction
    result_label.config(text=f"Password Strength: {predicted_strength}")

    # Adjust the progress bar based on the predicted strength
    update_strength_meter(predicted_strength)

    # Display suggestions to improve password strength
    display_password_suggestions(predicted_strength)

    # Plot the prediction probabilities inside the Tkinter window
    plot_prediction_probabilities(probabilities, strength_labels)

    # Plot the password criteria breakdown
    plot_password_criteria(password)

    # Update the checklist for password criteria
    update_password_checklist(password)

    # Plot the detailed character criteria analysis
    plot_character_criteria(password)

# Step 4: Function to update the strength meter with correct values and colors
def update_strength_meter(strength):
    if strength == 'Weak':
        strength_meter['value'] = 30  # 30% for weak passwords
        strength_meter.config(style="Red.Horizontal.TProgressbar")
    elif strength == 'Medium':
        strength_meter['value'] = 60  # 60% for medium passwords
        strength_meter.config(style="Orange.Horizontal.TProgressbar")
    else:
        strength_meter['value'] = 90  # 90% for strong passwords
        strength_meter.config(style="Green.Horizontal.TProgressbar")

# Step 5: Function to display suggestions to improve password strength
def display_password_suggestions(strength):
    if strength == 'Weak':
        suggestion_text = (
            "Suggestions to improve password strength:\n"
            "- Use at least 12 characters.\n"
            "- Include uppercase letters, numbers, and symbols.\n"
            "- Avoid common patterns like '123456'."
        )
    elif strength == 'Medium':
        suggestion_text = (
            "Suggestions to make your password stronger:\n"
            "- Increase the length to more than 12 characters.\n"
            "- Add more symbols and numbers.\n"
            "- Use a mix of uppercase and lowercase letters."
        )
    else:
        suggestion_text = (
            "Your password is strong, but always avoid reusing passwords across different accounts."
        )
    suggestion_label.config(text=suggestion_text)

# Step 6: Function to plot prediction probabilities inside the GUI
def plot_prediction_probabilities(probabilities, labels):
    # Clear the existing plot if there is one
    for widget in chart_frame.winfo_children():
        widget.destroy()

    # Create the figure for plotting
    fig, ax = plt.subplots(figsize=(4, 3), dpi=100)
    ax.bar(labels, probabilities, color=['red', 'orange', 'green'])
    ax.set_xlabel('Password Strength')
    ax.set_ylabel('Probability')
    ax.set_title('Password Strength Prediction Probabilities')
    ax.set_ylim(0, 1)

    # Embed the figure into the Tkinter window using FigureCanvasTkAgg
    canvas = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

# Step 7: Function to plot password criteria breakdown inside the GUI
def plot_password_criteria(password):
    # Clear the existing plot if there is one
    for widget in criteria_chart_frame.winfo_children():
        widget.destroy()

    # Extract criteria features
    has_digits = any(char.isdigit() for char in password)
    has_special_symbols = any(char in '!@#$%^&*()-_=+[{]}\|;:",<.>/?' for char in password)
    length = len(password)

    # Criteria to plot
    criteria = ['Has Digits', 'Has Special Symbols', 'Length >= 12']
    values = [has_digits, has_special_symbols, length >= 12]
    colors = ['green' if v else 'red' for v in values]

    # Create the figure for plotting
    fig, ax = plt.subplots(figsize=(4, 3), dpi=100)
    ax.bar(criteria, values, color=colors)
    ax.set_xlabel('Criteria')
    ax.set_ylabel('Met (1 = Yes, 0 = No)')
    ax.set_title('Password Criteria Breakdown')
    ax.set_ylim(0, 1)

    # Embed the figure into the Tkinter window using FigureCanvasTkAgg
    canvas = FigureCanvasTkAgg(fig, master=criteria_chart_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

# Step 8: Function to toggle password visibility
def toggle_password_visibility():
    if entry.cget('show') == '*':
        entry.config(show='')  # Show the password
        toggle_button.config(text='Hide Password')
    else:
        entry.config(show='*')  # Mask the password
        toggle_button.config(text='Show Password')

# Step 9: Function to update the password criteria checklist dynamically
def update_password_checklist(password):
    has_uppercase = any(char.isupper() for char in password)
    has_lowercase = any(char.islower() for char in password)
    has_digit = any(char.isdigit() for char in password)
    has_special = any(char in '!@#$%^&*()-_=+[{]}\|;:",<.>/?' for char in password)
    length_valid = len(password) >= 8

    # Update checklist labels
    checklist_items = {
        'Length >= 8 characters': length_valid,
        'Contains uppercase letter': has_uppercase,
        'Contains lowercase letter': has_lowercase,
        'Contains digit': has_digit,
        'Contains special character': has_special
    }

    # Clear existing checklist
    for widget in checklist_frame.winfo_children():
        widget.destroy()

    # Add updated checklist
    for text, is_met in checklist_items.items():
        color = "green" if is_met else "red"
        label = tk.Label(checklist_frame, text=f"{text}", font=("Helvetica", 12), fg=color)
        label.pack(anchor='w')

# Step 10: Function to provide real-time feedback when typing
def update_realtime_password_feedback(event):
    password = entry.get()
    update_password_checklist(password)

# Step 11: Function to plot detailed character criteria analysis
def plot_character_criteria(password):
    # Clear the existing plot if there is one
    for widget in character_chart_frame.winfo_children():
        widget.destroy()

    # Extract character features
    length = len(password)
    has_uppercase = any(char.isupper() for char in password)
    has_lowercase = any(char.islower() for char in password)
    has_digit = any(char.isdigit() for char in password)
    has_special = any(char in '!@#$%^&*()-_=+[{]}\|;:",<.>/?' for char in password)

    # Criteria to plot
    criteria = ['Length of Characters', 'Contains Uppercase Letters', 'Contains Lowercase Letters', 'Contains Digit', 'Contains Special Character']
    values = [length, has_uppercase, has_lowercase, has_digit, has_special]
    colors = ['green' if v else 'red' for v in values]

    # Create the figure for plotting
    fig, ax = plt.subplots(figsize=(5, 3), dpi=100)
    ax.bar(criteria, values, color=colors)
    ax.set_xlabel('Criteria')
    ax.set_ylabel('Met (1 = Yes, 0 = No) / Length')
    ax.set_title('Detailed Character Criteria Analysis')
    ax.set_ylim(0, max(12, length))

    # Embed the figure into the Tkinter window using FigureCanvasTkAgg
    canvas = FigureCanvasTkAgg(fig, master=character_chart_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

# Step 12: Create the Tkinter GUI
window = tk.Tk()
window.title("Password Strength Checker")
window.geometry("800x1200")  # Increased window width for better spacing

# Password Entry Label
label = tk.Label(window, text="Enter a Password:", font=("Helvetica", 14))
label.pack(pady=10)

# Password Entry Box
entry = tk.Entry(window, show="*", width=50, font=("Helvetica", 12))  # Increased width for better appearance
entry.pack(pady=5)
entry.bind("<KeyRelease>", update_realtime_password_feedback)  # Bind key release event for real-time feedback

# Toggle Password Visibility Button
toggle_button = tk.Button(window, text="Show Password", command=toggle_password_visibility, font=("Helvetica", 10), bg="#f0f0f0", relief="solid", bd=1)
toggle_button.pack(pady=5)

# Button to check strength
predict_button = tk.Button(window, text="Check Strength", command=predict_password_strength, font=("Helvetica", 14, "bold"), bg="#007bff", fg="white", activebackground="#0056b3", activeforeground="white", relief="raised", bd=3, padx=10, pady=5)
predict_button.pack(pady=10)

# Result Label to display password strength
result_label = tk.Label(window, text="", font=("Helvetica", 16, "bold"), fg="#333333")
result_label.pack(pady=10)

# Strength Meter (Progress Bar)
style = ttk.Style()
style.theme_use('default')
style.configure("Red.Horizontal.TProgressbar", troughcolor='gray', background='red', thickness=20)
style.configure("Orange.Horizontal.TProgressbar", troughcolor='gray', background='orange', thickness=20)
style.configure("Green.Horizontal.TProgressbar", troughcolor='gray', background='green', thickness=20)

strength_meter = ttk.Progressbar(window, orient='horizontal', length=400, mode='determinate')
strength_meter.pack(pady=10)

# Suggestions Label to display suggestions
suggestion_label = tk.Label(window, text="", font=("Helvetica", 12), wraplength=700, justify="left")
suggestion_label.pack(pady=20)

# Frame to embed the probability chart
chart_frame = tk.Frame(window, bg="#e6e6e6", relief="groove", bd=2)
chart_frame.pack(side="left", padx=20, pady=20)

# Frame to embed the password criteria breakdown chart
criteria_chart_frame = tk.Frame(window, bg="#e6e6e6", relief="groove", bd=2)
criteria_chart_frame.pack(side="right", padx=20, pady=20)

# Checklist Frame to display password requirements dynamically
checklist_frame = tk.Frame(window, bg="#f9f9f9", relief="ridge", bd=2)
checklist_frame.pack(pady=20, anchor='w')

# Frame to embed the detailed character criteria analysis chart
character_chart_frame = tk.Frame(window, bg="#e6e6e6", relief="groove", bd=2)
character_chart_frame.pack(pady=20)

# Run the Tkinter event loop
window.mainloop()

