from django.shortcuts import render, redirect
from .models import Food, DailyCalorieRecord
from .forms import FoodForm

def home(request):
    foods = Food.objects.all()
    record, created = DailyCalorieRecord.objects.get_or_create(date=request.POST.get('date', None))
    total_calories = record.total_calories if record else 0
    return render(request, 'home.html', {'foods': foods, 'total_calories': total_calories})

def add_food(request):
    if request.method == 'POST':
        form = FoodForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = FoodForm()
    return render(request, 'add_food.html', {'form': form})

def remove_food(request, food_id):
    food = Food.objects.get(id=food_id)
    food.delete()
    return redirect('home')

def reset_calories(request):
    record = DailyCalorieRecord.objects.first()
    if record:
        record.food_items.clear()
        record.total_calories = 0
        record.save()
    return redirect('home')
