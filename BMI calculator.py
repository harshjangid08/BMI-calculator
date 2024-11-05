import tkinter as tk
from tkinter import messagebox
import sqlite3
import time

# Create a database to store user data
conn = sqlite3.connect('health_tracker.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS logs (date TEXT, weight REAL, water REAL, calories REAL)''')
conn.commit()

class HealthBMICalculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Smart Health Tracker")
        self.geometry("400x500")
        self.configure(bg="#f0f0f0")  # Light gray background
        
        self.create_widgets()
        self.update_clock()

    def create_widgets(self):
        # Clock Display
        self.clock_frame = tk.Frame(self, bg="#4CAF50", bd=5, relief="groove")  # Green frame for clock
        self.clock_frame.pack(pady=10)

        self.clock_label = tk.Label(self.clock_frame, font=("Arial", 24, 'bold'), bg="#4CAF50", fg="white")  # Smaller font for clock
        self.clock_label.pack(pady=10)

        # Main frame
        main_frame = tk.Frame(self, bg="#f0f0f0")
        main_frame.pack(pady=10, fill="both", expand=True)

        # BMI Section
        bmi_frame = tk.Frame(main_frame, bg="#d0e6f0", bd=2, relief="groove")  # Light blue frame
        bmi_frame.pack(padx=10, pady=10, fill="x")

        tk.Label(bmi_frame, text="BMI Calculator", font=("Arial", 16), bg="#d0e6f0").pack(pady=10)

        tk.Label(bmi_frame, text="Height (cm):", bg="#d0e6f0").pack()
        self.height_entry = tk.Entry(bmi_frame)
        self.height_entry.pack(pady=5)

        tk.Label(bmi_frame, text="Weight (kg):", bg="#d0e6f0").pack()
        self.weight_entry = tk.Entry(bmi_frame)
        self.weight_entry.pack(pady=5)

        # 3D button style
        button_style = {
            'bg': "#4CAF50",
            'fg': "white",
            'activebackground': "#45a049",  # Darker green on click
            'highlightthickness': 0,
            'relief': 'raised'  # Raised effect
        }

        tk.Button(bmi_frame, text="Calculate BMI", command=self.calculate_bmi, **button_style).pack(pady=10)

        self.bmi_result = tk.Label(bmi_frame, text="", font=("Arial", 14), bg="#d0e6f0")
        self.bmi_result.pack(pady=5)

        # Health Tips Section
        tips_frame = tk.Frame(main_frame, bg="#f9f6b8", bd=2, relief="groove")  # Light yellow frame
        tips_frame.pack(padx=10, pady=10, fill="x")

        tk.Label(tips_frame, text="Health Tips", font=("Arial", 16), bg="#f9f6b8").pack(pady=10)
        self.health_tips = tk.Label(tips_frame, text="", font=("Arial", 12), wraplength=300, bg="#f9f6b8")
        self.health_tips.pack(pady=5)

    def update_clock(self):
        current_time = time.strftime("%H:%M:%S")
        self.clock_label.config(text=current_time)
        self.after(1000, self.update_clock)  # Update the clock every second

    def calculate_bmi(self):
        try:
            height_cm = float(self.height_entry.get())
            weight_kg = float(self.weight_entry.get())
            height_m = height_cm / 100  # Convert height to meters
            bmi = weight_kg / (height_m ** 2)
            category = self.get_bmi_category(bmi)
            self.bmi_result.config(text=f"BMI: {bmi:.2f} - {category}")
            self.display_health_tips(category)
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers for height and weight.")

    def get_bmi_category(self, bmi):
        if bmi < 18.5:
            return "Underweight"
        elif 18.5 <= bmi < 24.9:
            return "Normal weight"
        elif 25 <= bmi < 29.9:
            return "Overweight"
        else:
            return "Obesity"

    def display_health_tips(self, category):
        tips = {
            "Underweight": "Consider a balanced diet with more calories. Consult a nutritionist for personalized advice.",
            "Normal weight": "Great job! Maintain a balanced diet and regular exercise.",
            "Overweight": "Focus on a balanced diet and regular physical activity. Consult a healthcare provider for guidance.",
            "Obesity": "Seek advice from a healthcare professional for a tailored weight loss plan and lifestyle changes."
        }
        self.health_tips.config(text=tips[category])

if __name__ == "__main__":
    app = HealthBMICalculator()
    app.mainloop()

    conn.close()
