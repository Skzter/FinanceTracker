import os
import django
import random
from decimal import Decimal
from datetime import datetime

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ToDoWebsite.settings")
django.setup()

# Import your model
from ToDoApp.models import Ausgaben  # Replace 'myapp' with your app name

def create_monthly_data():
    # Define categories and their weight for random selection
    categories = {
        'W': 0.25,  # Wohnen
        'L': 0.20,  # Leben
        'H/F': 0.15,  # Hobby/Freizeit
        'M': 0.15,  # Mobilität
        'B': 0.10,  # Bildung
        'S/I': 0.10,  # Sparen/Investieren
        'S': 0.05,  # Sonstiges
    }

    # Create one Einnahmen (income) entry per month
    for month in range(1, 13):  # Loop through all 12 months
        # Create Einnahmen (income)
        Ausgaben.objects.create(
            type='E',
            month=month,
            category='L',
            title="Gehalt",
            amount=Decimal('2500.00')
        )

        # Create 10 Ausgaben (expenses) entries
        total_expenses = Decimal('0.00')
        target_total = Decimal(random.uniform(2000, 2500)).quantize(Decimal('0.01'))  # Random total between 2000 and 2500

        for _ in range(10):
            # Randomly select a category based on weights
            category = random.choices(list(categories.keys()), weights=list(categories.values()))[0]

            # Generate a random amount for the expense
            if total_expenses >= target_total:
                break  # Stop if total expenses reach the target

            # Calculate remaining budget
            remaining_budget = target_total - total_expenses

            # Generate a random amount between 50 and 500, but not exceeding the remaining budget
            amount = Decimal(random.uniform(50, min(500, float(remaining_budget)))).quantize(Decimal('0.01'))

            # Create the expense entry
            Ausgaben.objects.create(
                type='A',
                month=month,
                category=category,
                title=f"Ausgabe {_ + 1}",
                amount=amount
            )

            # Update total expenses
            total_expenses += amount

        print(f"Created data for month {month} with total expenses: {total_expenses}")

if __name__ == "__main__":
    create_monthly_data()
