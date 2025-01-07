from django.db import models

class Food(models.Model):
    name = models.CharField(max_length=100)
    calorie_count = models.PositiveIntegerField()

    def __str__(self):
        return self.name

class DailyCalorieRecord(models.Model):
    date = models.DateField(auto_now_add=True)
    food_items = models.ManyToManyField(Food)
    total_calories = models.PositiveIntegerField(default=0)

    def update_total_calories(self):
        self.total_calories = sum(food.calorie_count for food in self.food_items.all())
        self.save()

    def __str__(self):
        return f"Record for {self.date}"
