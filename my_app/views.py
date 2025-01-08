from django.shortcuts import render, redirect
from .models import Food, DailyCalorieRecord
from .forms import FoodForm
from datetime import date

def home(request):
    # Use filter() to handle multiple records and get the one for today
    record = DailyCalorieRecord.objects.filter(date=date.today()).first()

    # If no record exists for today, create one
    if not record:
        record = DailyCalorieRecord.objects.create(date=date.today())

    # Fetch associated food items
    foods = record.food_items.all()
    total_calories = record.total_calories

    return render(request, 'home.html', {'foods': foods, 'total_calories': total_calories})

def add_food(request):
    if request.method == 'POST':
        form = FoodForm(request.POST)
        if form.is_valid():
            food = form.save()

            # Get or create today's calorie record
            record = DailyCalorieRecord.objects.filter(date=date.today()).first()
            if not record:
                record = DailyCalorieRecord.objects.create(date=date.today())

            # Add the food item to the record and update the total calories
            record.food_items.add(food)
            record.update_total_calories()  # Recalculate total calories
            return redirect('home')
    else:
        form = FoodForm()
    return render(request, 'add_food.html', {'form': form})

def remove_food(request, food_id):
    food = Food.objects.get(id=food_id)

    # Get today's calorie record
    record = DailyCalorieRecord.objects.filter(date=date.today()).first()

    if record:
        # Remove the food item and update total calories
        record.food_items.remove(food)
        record.update_total_calories()

    food.delete()  # Delete the food item itself from the database
    return redirect('home')

def reset_calories(request):
    record = DailyCalorieRecord.objects.filter(date=date.today()).first()
    if record:
        record.food_items.clear()
        record.total_calories = 0
        record.save()
    return redirect('home')
